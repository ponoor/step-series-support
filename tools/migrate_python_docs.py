#!/usr/bin/env python3
"""Move the hand-written docstrings of python-step-series into `_docstrings.py` (done once for v2.2.0),
and check afterwards that no prose of the old docstrings was lost.

    python tools/migrate_python_docs.py migrate <library> [--ref main]   # write src/stepseries/_docstrings.py
    python tools/migrate_python_docs.py check   <library> [--ref main]   # compare the old docstrings with the current modules

`--ref` is the git ref of the library that holds the old modules (default `main`).

The old docstrings are split into paragraphs (blank-line separated blocks).

- Tables (the `Executable Timing` table, the range / value tables of the arguments) are not moved:
  the timing table is written again by gen_python.py and the argument tables are added from the YAML when
  the Sphinx documentation is built.
- A prose paragraph is dropped only if the YAML description says (almost) the same, i.e. if at least
  COVER of its content words are in the YAML text of that class or argument. Every other paragraph is moved
  unchanged to `_docstrings.py`; gen_python.py appends it to the text taken from the YAML.
- RST hyperlink targets (`.. _Config Tool: ...`) are always moved.

`check` reports, per old paragraph, whether it is in the current docstring word for word, covered by the
text of the current docstring, or missing. It exits with 1 if any paragraph is missing.
"""

from __future__ import annotations

import argparse
import ast
import inspect
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_python as gp  # noqa: E402
from spec import Spec  # noqa: E402

MODULES = ("commands", "responses")


def read_old(lib: Path, ref: str, module: str) -> str:
    return subprocess.run(
        ["git", "-C", str(lib), "show", f"{ref}:src/stepseries/{module}.py"],
        check=True, capture_output=True, text=True,
    ).stdout


def extract(source: str) -> dict[str, dict]:
    """{class: {"class": docstring, "fields": {field: docstring}}} of a module source."""
    out: dict[str, dict] = {}
    for node in ast.parse(source).body:
        if not isinstance(node, ast.ClassDef):
            continue
        entry = {"class": ast.get_docstring(node, clean=True) or "", "fields": {}}
        body = node.body
        for i, n in enumerate(body):
            if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
                doc = ""
                if i + 1 < len(body):
                    nxt = body[i + 1]
                    if isinstance(nxt, ast.Expr) and isinstance(nxt.value, ast.Constant) and isinstance(nxt.value.value, str):
                        doc = inspect.cleandoc(nxt.value.value)
                entry["fields"][n.target.id] = doc
        out[node.name] = entry
    return out


def prose(text: str) -> list[str]:
    """The paragraphs of a docstring that are not tables."""
    return [p for p in gp.paragraphs(text) if not gp.is_table(p)]


def yaml_texts(gen: gp.Gen, spec: Spec) -> dict[str, dict]:
    """For every class (`commands.X`, `responses.X`): the YAML paragraphs of the class and of each field."""
    out: dict[str, dict] = {}
    for mod, items, names in (("commands", spec.commands, gen.cmd_class), ("responses", spec.messages, gen.msg_class)):
        for item in items:
            desc = item.get("description")
            cls_paras = gp.yaml_paragraphs(desc["en"] if isinstance(desc, dict) else desc, gen.refs) if desc else []
            fields = {f["name"]: f["doc"] for f in gen.fields_of(item, mod) if "name" in f}
            out[f"{mod}.{names[item['address']]}"] = {"class": cls_paras, "fields": fields}
    return out


def build(lib: Path, ref: str) -> tuple[dict, list[dict]]:
    spec = Spec.load()
    compat = yaml.safe_load(gp.COMPAT_PATH.read_text(encoding="utf-8"))
    gen = gp.Gen(spec, compat, {})
    yt = yaml_texts(gen, spec)
    overrides: dict[str, dict] = {}
    log: list[dict] = []
    for mod in MODULES:
        old = extract(read_old(lib, ref, mod))
        for cname, entry in old.items():
            qual = f"{mod}.{cname}"
            y = yt.get(qual, {"class": [], "fields": {}})
            targets = [("class", None, entry["class"], " ".join(y["class"]))]
            for fname, doc in entry["fields"].items():
                targets.append(("field", fname, doc, " ".join(y["fields"].get(fname, []))))
            for kind, fname, doc, ytext in targets:
                for p in gp.paragraphs(doc):
                    if gp.is_table(p):
                        log.append({"class": qual, "field": fname, "status": "table", "text": p})
                        continue
                    r = gp.recall(p, ytext)
                    if gp.is_target(p) or r < gp.COVER:
                        slot = overrides.setdefault(qual, {"class": [], "fields": {}})
                        (slot["class"] if kind == "class" else slot["fields"].setdefault(fname, [])).append(p)
                        log.append({"class": qual, "field": fname, "status": "moved", "recall": round(r, 2), "text": p})
                    else:
                        log.append({"class": qual, "field": fname, "status": "covered", "recall": round(r, 2), "text": p})
    return overrides, log


def literal(text: str) -> list[str]:
    """Python source lines for a (possibly multi-line) string, one literal per line."""
    lines = text.split("\n")
    return [json.dumps(ln + ("\n" if i < len(lines) - 1 else ""), ensure_ascii=False) for i, ln in enumerate(lines)]


def emit(overrides: dict) -> str:
    out = ['"""Prose of the docstrings of v1.0.0 that spec/osc-commands.yaml does not say.',
           "",
           "tools/gen_python.py (step-series-support) appends these paragraphs to the text it takes from the YAML.",
           "Edit this file by hand; commands.py and responses.py are generated.",
           '"""',
           "",
           "DOCSTRINGS = {"]

    def para_block(p: str, indent: str) -> list[str]:
        lines = literal(p)
        if len(lines) == 1:
            return [f"{indent}{lines[0]},"]
        return [f"{indent}("] + [f"{indent}    {ln}" for ln in lines] + [f"{indent}),"]

    for qual in sorted(overrides):
        slot = overrides[qual]
        out.append(f'    "{qual}": {{')
        if slot["class"]:
            out.append('        "class": [')
            for p in slot["class"]:
                out += para_block(p, "            ")
            out.append("        ],")
        if slot["fields"]:
            out.append('        "fields": {')
            for fname, paras in slot["fields"].items():
                out.append(f'            "{fname}": [')
                for p in paras:
                    out += para_block(p, "                ")
                out.append("            ],")
            out.append("        },")
        out.append("    },")
    out.append("}")
    return "\n".join(out) + "\n"


def new_docs(lib: Path) -> dict[str, dict]:
    base = lib / "src" / "stepseries"
    return {mod: extract((base / f"{mod}.py").read_text(encoding="utf-8")) for mod in MODULES}


def check(lib: Path, ref: str, verbose: bool) -> int:
    new = new_docs(lib)
    counts = {"verbatim": 0, "covered": 0, "missing": 0, "table": 0}
    weak: list[str] = []
    missing: list[str] = []
    for mod in MODULES:
        old = extract(read_old(lib, ref, mod))
        for cname, entry in old.items():
            cur = new[mod].get(cname)
            if cur is None:
                missing.append(f"{mod}.{cname}: class is gone")
                continue
            pairs = [(None, entry["class"], cur["class"])]
            pairs += [(f, d, cur["fields"].get(f, "")) for f, d in entry["fields"].items()]
            for fname, old_doc, new_doc in pairs:
                new_paras = gp.paragraphs(new_doc)
                for p in gp.paragraphs(old_doc):
                    where = f"{mod}.{cname}" + (f".{fname}" if fname else "")
                    if gp.is_table(p):
                        counts["table"] += 1
                    elif p in new_paras:
                        counts["verbatim"] += 1
                    else:
                        r = gp.recall(p, new_doc)
                        if r >= gp.COVER:
                            counts["covered"] += 1
                            if r < 0.95:
                                weak.append(f"{where}  recall {r:.2f}: {p[:100]!r}")
                        else:
                            counts["missing"] += 1
                            missing.append(f"{where}  recall {r:.2f}: {p[:100]!r}")
    print(json.dumps(counts))
    if verbose:
        print(f"{len(weak)} covered with recall below 0.95:")
        print("\n".join(weak))
    if missing:
        print("MISSING:")
        print("\n".join(missing))
    return 1 if missing else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["migrate", "check"])
    ap.add_argument("library")
    ap.add_argument("--ref", default="main")
    ap.add_argument("--log", help="migrate: write the per-paragraph log (JSON) here")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)
    lib = Path(args.library).expanduser().resolve()
    if args.command == "migrate":
        overrides, log = build(lib, args.ref)
        (lib / "src" / "stepseries" / "_docstrings.py").write_text(emit(overrides), encoding="utf-8")
        if args.log:
            Path(args.log).write_text(json.dumps(log, indent=1, ensure_ascii=False), encoding="utf-8")
        stats: dict[str, int] = {}
        for e in log:
            stats[e["status"]] = stats.get(e["status"], 0) + 1
        print(stats, "classes with moved text:", len(overrides))
        return 0
    return check(lib, args.ref, args.verbose)


if __name__ == "__main__":
    sys.exit(main())
