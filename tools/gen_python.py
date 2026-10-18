#!/usr/bin/env python3
"""Generate the classes of the Python library (python-step-series) from spec/osc-commands.yaml.

    python tools/gen_python.py <path to python-step-series>            # write
    python tools/gen_python.py <path> --check                          # write nothing, exit 1 if a file would change

Writes `src/stepseries/commands.py` (one dataclass per command) and `src/stepseries/responses.py`
(one dataclass per message). Both start with a notice that they are generated.

Inputs
- spec/osc-commands.yaml: addresses, arguments, descriptions (English), timings, notifications.
- tools/python_compat.yaml: the class and field names that already existed in the library
  (they never change), and the few places where the library differs from the YAML.
- tools/python_templates/*_header.py: the hand-written start of each module (base classes,
  the response parser).
- <library>/src/stepseries/_docstrings.py: prose of the old hand-written docstrings that the YAML
  does not say. Kept in the library, appended after the YAML text. Made once by
  tools/migrate_python_docs.py.

Argument tables are not written into the docstrings. The Sphinx extension of the library
(docs/_ext/osc_spec.py) adds them from the YAML when the documentation is built.
"""

from __future__ import annotations

import argparse
import keyword
import re
import runpy
import sys
import textwrap
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec import LINK_RE, Spec  # noqa: E402

TOOLS = Path(__file__).resolve().parent
COMPAT_PATH = TOOLS / "python_compat.yaml"
TEMPLATES = TOOLS / "python_templates"

BANNER = (
    "# This file is generated. Do not edit it directly.\n"
    "# Source: spec/osc-commands.yaml of the step-series-support repository,\n"
    "# tools/gen_python.py (run it again to update this file).\n"
    "# Extra prose of the docstrings: _docstrings.py.\n"
)

PY_TYPES = {"int": "int", "float": "float", "bool": "bool", "string": "str"}
WRAP = 72

# ---------------------------------------------------------------------------
# Text helpers (shared with migrate_python_docs.py)


def paragraphs(text: str) -> list[str]:
    """Blank-line separated blocks, de-indented and stripped. Empty blocks are dropped."""
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [ln.rstrip() for ln in block.strip("\n").split("\n")]
        block = textwrap.dedent("\n".join(lines)).strip("\n")
        if block.strip():
            out.append(block)
    return out


def is_table(block: str) -> bool:
    """RST grid table or simple table."""
    first = block.lstrip().split("\n")[0]
    return first.startswith("+-") or first.startswith("+=") or re.match(r"^=+(\s+=+)+\s*$", first) is not None


def is_target(block: str) -> bool:
    """An RST hyperlink target (`.. _name: url`), which must stay with the text that uses it."""
    return block.lstrip().startswith(".. _")


_STOP = {"the", "a", "an", "of", "to", "is", "are", "be", "in", "on", "and", "or", "for", "with", "as", "by", "it",
         "this", "that", "will", "can", "if", "when", "at", "from", "its", "not"}


def tokens(text: str) -> list[str]:
    """Lower-case content words, with a trailing plural/verb `s` removed."""
    words = re.findall(r"[a-z0-9_./]+", text.lower().replace("``", " "))
    out = []
    for w in words:
        w = w.strip("./_")
        if not w or w in _STOP:
            continue
        if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        out.append(w)
    return out


def recall(old: str, new: str) -> float:
    """Share of the content words of `old` that `new` has."""
    o = tokens(old)
    if not o:
        return 1.0
    n = set(tokens(new))
    return sum(1 for w in o if w in n) / len(o)


COVER = 0.9  # an old paragraph is covered by the YAML text if this share of its words is in it


def md_to_rst(text: str, refs: dict[str, str]) -> str:
    """The Markdown subset of the YAML (`code`, [[/address]]) as reStructuredText."""

    def link(m: re.Match) -> str:
        ref = refs.get(m.group(1))
        return f":py:class:`~{ref}`" if ref else f"``{m.group(1)}``"

    text = LINK_RE.sub(link, text)
    parts = re.split(r"(``[^`]*``|:py:class:`[^`]*`|`[^`]+`)", text)
    out = []
    for p in parts:
        if p.startswith(":py:class:") or p.startswith("``"):
            out.append(p)
        elif p.startswith("`") and p.endswith("`") and len(p) > 2:
            out.append("``" + p[1:-1] + "``")
        else:
            # a word that ends with an underscore would be read as a reference
            out.append(re.sub(r"(?<=\w)_(?=\s|[.,;:)]|$)", r"\\_", p))
    return "".join(out)


_BAD_START = re.compile(r"^(?:[-*+•]|\d+[.)]|\(?[A-Za-z][.)]|\.\.|[|:>#]|=+|-{2,})$")


def wrap_paragraph(text: str) -> str:
    """Re-flow one paragraph to WRAP columns without starting a line with an RST list marker."""
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > WRAP and not _BAD_START.match(w):
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def yaml_paragraphs(text: str, refs: dict[str, str]) -> list[str]:
    return [wrap_paragraph(" ".join(p.split("\n"))) for p in paragraphs(md_to_rst(text, refs))]


def grid_table(rows: list[list[str]]) -> str:
    widths = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]
    sep = "+" + "+".join("-" * w for w in widths) + "+"
    lines = [sep]
    for r in rows:
        lines.append("|" + "|".join(c.ljust(w) for c, w in zip(r, widths)) + "|")
        lines.append(sep)
    return "\n".join(lines)


def py_doc(blocks: list[str], indent: str) -> list[str]:
    """Lines of a docstring (triple quoted) for the given paragraph blocks, indented."""
    body = "\n\n".join(blocks)
    body = body.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    lines = body.split("\n")
    if len(lines) == 1 and not lines[0].endswith('"'):
        return [f'{indent}"""{lines[0]}"""']
    out = [f'{indent}"""{lines[0]}']
    out += [(indent + ln) if ln else "" for ln in lines[1:]]
    out.append(f'{indent}"""')
    return out


# ---------------------------------------------------------------------------
# Names


def camel(address: str) -> str:
    """`/combine/goTo` -> `CombineGoTo`: the first letter of each part in upper case."""
    return "".join(p[:1].upper() + p[1:] for p in address.strip("/").split("/"))


def field_name(arg_name: str) -> str:
    return re.sub(r"\[(\d+)\]", r"\1", arg_name)


class Gen:
    def __init__(self, spec: Spec, compat: dict, overrides: dict):
        self.spec = spec
        self.compat = compat
        self.overrides = overrides
        self.cmd_class: dict[str, str] = {}
        self.msg_class: dict[str, str] = {}
        for c in spec.commands:
            self.cmd_class[c["address"]] = compat["commands"].get(c["address"], {}).get("class") or camel(c["address"])
        for m in spec.messages:
            self.msg_class[m["address"]] = compat["messages"].get(m["address"], {}).get("class") or camel(m["address"])
        # [[/address]] -> importable name (a command wins over a message with the same address)
        self.refs = {a: f"stepseries.responses.{n}" for a, n in self.msg_class.items()}
        self.refs.update({a: f"stepseries.commands.{n}" for a, n in self.cmd_class.items()})
        motors = [b["motors"] for b in spec.boards.values()]
        self.min_motors, self.max_motors = min(motors), max(motors)

    # -- checks ------------------------------------------------------------

    def check_names(self) -> list[str]:
        problems = []
        for what, mapping in (("commands", self.cmd_class), ("responses", self.msg_class)):
            seen: dict[str, str] = {}
            for addr, name in mapping.items():
                if name in seen:
                    problems.append(f"{what}: class name {name} is used by {seen[name]} and {addr}")
                seen[name] = addr
                if not name.isidentifier() or keyword.iskeyword(name):
                    problems.append(f"{what}: {addr}: {name} is not a usable class name")
        for addr in list(self.compat["commands"]):
            if self.spec.command(addr) is None:
                problems.append(f"python_compat.yaml: command {addr} is not in the YAML (deprecate it by hand)")
        for addr in list(self.compat["messages"]):
            if self.spec.message(addr) is None:
                problems.append(f"python_compat.yaml: message {addr} is not in the YAML (deprecate it by hand)")
        return problems

    # -- fields ------------------------------------------------------------

    def fields_of(self, item: dict, kind: str) -> list[dict]:
        """[{name, type, default, doc (YAML paragraphs), raw}] of a command or message."""
        addr = item["address"]
        table = self.compat.get("fields", {}).get(addr)
        out: list[dict] = []
        if table is not None:
            for f in table:
                if "raw" in f:
                    out.append({"raw": f["raw"]})
                else:
                    out.append({"name": f["name"], "type": f["type"], "default": f.get("default"),
                                "doc": [f["doc"]] if f.get("doc") else []})
            return out
        renames = self.compat.get("field_names", {}).get(addr, {})
        optional = set(self.compat.get("optional", {}).get(addr, []))
        for a in self.spec.args(item):
            ty = PY_TYPES[a["type"]]
            desc = a.get("description")
            doc = yaml_paragraphs(desc["en"] if isinstance(desc, dict) else desc, self.refs) if desc else []
            if a.get("repeat") == "motors":
                for i in range(1, self.max_motors + 1):
                    out.append({"name": f"{a['name']}{i}", "type": ty,
                                "default": None if i <= self.min_motors else "None",
                                "doc": doc, "yaml": a["name"]})
                continue
            raw_name = a["name"]
            name = renames.get(raw_name) or field_name(raw_name)
            default = "None" if ("since" in a or raw_name in optional or name in optional) else None
            out.append({"name": name, "type": ty, "default": default, "doc": doc, "yaml": raw_name})
        for f in self.compat.get("extra_fields", {}).get(addr, []):
            out.append({"name": f["name"], "type": f["type"], "default": f.get("default"),
                        "doc": [f["doc"]] if f.get("doc") else []})
        for f in out:
            if "name" in f and (keyword.iskeyword(f["name"]) or not f["name"].isidentifier()):
                raise ValueError(f"{addr}: {f['name']} is not a usable field name")
        return out

    def field_lines(self, f: dict, qualname: str) -> list[str]:
        if "raw" in f:
            return ["    " + ln if ln else "" for ln in f["raw"].rstrip("\n").split("\n")]
        line = f"    {f['name']}: {f['type']}" + (f" = {f['default']}" if f.get("default") else "")
        lines = [line]
        extra = self.overrides.get(qualname, {}).get("fields", {}).get(f["name"], [])
        blocks = list(f["doc"]) + [e for e in extra if e not in f["doc"]]
        if blocks:
            lines += py_doc(blocks, "    ")
        return lines

    # -- one class -----------------------------------------------------------

    def class_doc(self, item: dict, qualname: str, with_timing: bool) -> list[str]:
        desc = item.get("description")
        blocks = yaml_paragraphs(desc["en"] if isinstance(desc, dict) else desc, self.refs) if desc else []
        blocks += self.overrides.get(qualname, {}).get("class", [])
        if with_timing and item.get("timing"):
            names = item["timing"] if isinstance(item["timing"], list) else [item["timing"]]
            label = " / ".join(self.spec.timings[t]["en"] for t in names)
            blocks.append(grid_table([["Executable Timing", label]]))
        return py_doc(blocks, "    ") if blocks else []

    def response_classes(self, addrs: list[str]) -> list[str]:
        return [self.msg_class[a] for a in addrs]

    def command_kind(self, c: dict) -> str:
        addr = c["address"]
        entry = self.compat["commands"].get(addr) or self.compat.get("new_commands", {}).get(addr) or {}
        if entry.get("kind"):
            return entry["kind"]
        unconditional = [r for r in c.get("response", []) if isinstance(r, str) or "when" not in r]
        return "Get" if unconditional else "Set"

    def command_class(self, c: dict) -> list[str]:
        addr = c["address"]
        name = self.cmd_class[addr]
        qual = f"commands.{name}"
        kind = self.command_kind(c)
        lines = ["@dataclass", f"class {name}(OSC{kind}Command):"]
        doc = self.class_doc(c, qual, True)
        if doc:
            lines += doc + [""]
        lines.append(f'    address: str = field(default="{addr}", init=False)')
        resp = self.response_classes(self.spec.response_messages(c)) if kind == "Get" else []
        notifies = c.get("notifies", [])
        if kind == "Set" and notifies:
            resp = self.response_classes(notifies)
        fixed = self.compat.get("response_cls", {}).get(addr)
        if fixed:
            resp = self.response_classes(fixed)
        if resp:
            lines += self.response_cls_lines(resp)
        for f in self.fields_of(c, "command"):
            lines += self.field_lines(f, qual)
        if notifies:
            lines.append("    callback: Optional[Callable[..., None]] = None")
        return lines

    @staticmethod
    def response_cls_lines(classes: list[str]) -> list[str]:
        if len(classes) == 1:
            n = classes[0]
            one = f"    response_cls: responses.{n} = field(default=responses.{n}, init=False)"
            if len(one) <= 88:
                return [one]
            return [f"    response_cls: responses.{n} = field(", f"        default=responses.{n}, init=False", "    )"]
        types = ", ".join(f"responses.{n}" for n in classes)
        return [f"    response_cls: Tuple[{types}] = field(",
                f"        default_factory=lambda: ({types}),",
                "        init=False,",
                "    )"]

    def message_class(self, m: dict) -> list[str]:
        addr = m["address"]
        name = self.msg_class[addr]
        qual = f"responses.{name}"
        bases = "OSCResponse, Exception" if addr.startswith("/error/") else "OSCResponse"
        lines = ["@dataclass", f"class {name}({bases}):"]
        doc = self.class_doc(m, qual, False)
        if doc:
            lines += doc + [""]
        lines.append(f'    address: str = field(default="{addr}", init=False)')
        for f in self.fields_of(m, "message"):
            lines += self.field_lines(f, qual)
        return lines

    # -- modules -----------------------------------------------------------

    def commands_module(self) -> str:
        orphans = [c for c in self.spec.commands if c.get("group") not in self.spec.groups]
        if orphans:
            raise ValueError("commands without a known group: " + ", ".join(c["address"] for c in orphans))
        parts = [self.header("commands_header.py")]
        for gkey, g in self.spec.groups.items():
            cmds = [c for c in self.spec.commands if c.get("group") == gkey]
            if cmds:
                parts.append(f"# {g['en']}")
                parts += ["\n".join(self.command_class(c)) for c in cmds]
        parts.append(self.board_lists())
        return "\n\n\n".join(parts).rstrip("\n") + "\n"

    @staticmethod
    def header(name: str) -> str:
        """The banner and the hand-written start of a module (its docstring comes first)."""
        return BANNER + (TEMPLATES / name).read_text(encoding="utf-8").rstrip("\n")

    def board_lists(self) -> str:
        """`STEP400_ONLY`: the commands the STEP800 does not have (STEP800 refuses them)."""
        names = [self.cmd_class[c["address"]] for c in self.spec.commands if "STEP800" not in self.spec.boards_of(c)]
        lines = ["# Commands that only the STEP400 has", "STEP400_ONLY: Tuple[Type[OSCCommand], ...] = ("]
        lines += [f"    {n}," for n in names]
        lines.append(")")
        return "\n".join(lines)

    def responses_module(self) -> str:
        parts = [self.header("responses_header.py"), "# Messages"]
        parts += ["\n".join(self.message_class(m)) for m in self.spec.messages]
        return "\n\n\n".join(parts).rstrip("\n") + "\n"


def load_overrides(lib: Path) -> dict:
    path = lib / "src" / "stepseries" / "_docstrings.py"
    if not path.exists():
        return {}
    return runpy.run_path(str(path)).get("DOCSTRINGS", {})


def generate(spec: Spec, lib: Path) -> dict[Path, str]:
    compat = yaml.safe_load(COMPAT_PATH.read_text(encoding="utf-8"))
    gen = Gen(spec, compat, load_overrides(lib))
    problems = gen.check_names()
    if problems:
        raise SystemExit("\n".join(problems))
    base = lib / "src" / "stepseries"
    return {base / "commands.py": gen.commands_module(), base / "responses.py": gen.responses_module()}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("library", help="path of the python-step-series repository")
    ap.add_argument("--spec", default=None, help="spec/osc-commands.yaml (default: this repository's)")
    ap.add_argument("--check", action="store_true", help="write nothing; exit 1 if a file would change")
    args = ap.parse_args(argv)
    lib = Path(args.library).expanduser().resolve()
    if not (lib / "src" / "stepseries").is_dir():
        print(f"{lib}: no src/stepseries here", file=sys.stderr)
        return 2
    spec = Spec.load(args.spec) if args.spec else Spec.load()
    changed = 0
    for path, text in generate(spec, lib).items():
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old != text:
            changed += 1
            print(("would change " if args.check else "wrote ") + str(path.relative_to(lib)))
            if not args.check:
                path.write_text(text, encoding="utf-8")
    if not changed:
        print("no changes")
    return 1 if (args.check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
