#!/usr/bin/env python3
"""Validate spec/osc-commands.yaml.

    python tools/validate_spec.py [path/to/osc-commands.yaml]

Checks
  - the format, with spec/osc-commands.schema.json
  - references: group, timing, use, response / notifies (-> messages),
    see_also and [[...]] links (-> commands / messages), setting (-> settings),
    settings.*.commands (-> commands), errors (-> values of /error/command)
  - duplicated addresses and setting keys
  - keys of board-specific values are boards defined in `boards`
  - Japanese wording (spec/glossary_ja.yaml): words to avoid, and a space between an ASCII
    letter/digit and a Japanese character. Checked in every `ja` text of the spec, in docs/ja/**/*.md
    (not the pages in exclude_docs, and not the pages generated from the spec), in the Japanese
    nav_translations of mkdocs.yml and in the Japanese fixed texts of tools/generate.py.
    Inline code, code blocks, [[...]] links, URLs, HTML comments and generated blocks are left out
    (code and links count as one ASCII word for the spacing check).
Warnings (not failures): empty texts (missing Japanese etc.), values with en but no ja, messages without description.
Exit code 1 if any check fails.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec import REPO_ROOT, SCHEMA_PATH, SPEC_PATH, Spec  # noqa: E402

GLOSSARY_PATH = REPO_ROOT / "spec" / "glossary_ja.yaml"
MKDOCS_PATH = REPO_ROOT / "mkdocs.yml"
DOCS_JA = REPO_ROOT / "docs" / "ja"
GENERATE_PATH = REPO_ROOT / "tools" / "generate.py"

# A stripped piece (code, link, URL, placeholder) counts as one ASCII word for the spacing check.
SENTINEL = "\ue000"
_STRIP = [
    (re.compile(r"<!--.*?-->", re.S), True),                       # comments, generated blocks (see below)
    (re.compile(r"^(```|~~~).*?^\1[^\n]*$", re.S | re.M), True),     # code blocks
    (re.compile(r"`[^`\n]*`"), False),                             # inline code
    (re.compile(r"\[\[[^\]\n]*\]\]"), False),                      # [[/address]] links
    (re.compile(r"https?://[^\s)>\]]+"), False),                   # URLs
]
GENERATED_BLOCK_RE = re.compile(r"<!-- generated:begin .*?<!-- generated:end [^\n]*-->", re.S)
# ASCII letters and digits (and a stripped piece) next to a Japanese character with spaces between
_JA = "\u3000-\u30ff\u3400-\u9fff\uff00-\uffef"
_ASCII = f"A-Za-z0-9{SENTINEL}"
SPACE_RE = re.compile(rf"(?:(?<=[{_ASCII}]) +(?=[{_JA}])|(?<=[{_JA}]) +(?=[{_ASCII}]))")


class Report:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.glossary_hits: Counter = Counter()  # Japanese wording errors, by word

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    def glossary(self, msg: str, key: str):
        self.errors.append(msg)
        self.glossary_hits[key] += 1


def check_schema(spec: Spec, rep: Report):
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(spec.data), key=lambda e: list(e.absolute_path)):
        path = "/".join(str(p) for p in err.absolute_path)
        rep.error(f"schema: {path}: {err.message[:300]}")


def check_board_keys(spec: Spec, rep: Report):
    boards = set(spec.board_names)

    def walk(node, where):
        if isinstance(node, dict):
            if spec.is_board_map(node):
                for k in node:
                    if k not in boards:
                        rep.error(f"{where}: unknown board '{k}'")
            for k, v in node.items():
                walk(v, f"{where}.{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{where}[{i}]")

    for section in ("params", "settings", "commands", "messages"):
        walk(spec.data.get(section), section)
    for section in ("settings", "commands", "messages"):
        for item in spec.data.get(section) or []:
            name = item.get("address") or item.get("key")
            for field in ("boards", "routed_on"):
                for b in item.get(field, []):
                    if b not in boards:
                        rep.error(f"{name}: {field}: unknown board '{b}'")
            for a in item.get("args", []):
                for v in a.get("values", []) if isinstance(a.get("values"), list) else []:
                    for b in v.get("boards", []):
                        if b not in boards:
                            rep.error(f"{name}: value {v.get('value')}: unknown board '{b}'")


def check_references(spec: Spec, rep: Report):
    cmd_addrs = [c["address"] for c in spec.commands]
    msg_addrs = [m["address"] for m in spec.messages]
    setting_keys = [s["key"] for s in spec.settings]
    for kind, names in (("command", cmd_addrs), ("message", msg_addrs), ("setting", setting_keys)):
        for name, n in Counter(names).items():
            if n > 1:
                rep.error(f"duplicated {kind}: {name} ({n} times)")
    aliases = [a for s in spec.settings for a in s.get("aliases", [])]
    for a in aliases:
        if a in setting_keys:
            rep.error(f"setting alias '{a}' is also a setting key")

    cmd_set, msg_set = set(cmd_addrs), set(msg_addrs)
    all_addrs = cmd_set | msg_set
    setting_set = set(setting_keys)

    error_msg = spec.message("/error/command")
    error_names: set[str] = set()
    if error_msg:
        for a in spec.args(error_msg):
            if isinstance(a.get("values"), list):
                error_names |= {str(v["value"]) for v in a["values"]}
                break

    def check_args(owner: str, args: list):
        for raw in args:
            if "use" in raw and raw["use"] not in spec.params:
                rep.error(f"{owner}: use '{raw['use']}' is not in params")
                continue
            if "setting" in raw and raw["setting"] not in setting_set:
                rep.error(f"{owner}: setting '{raw['setting']}' is not in settings")

    for c in spec.commands:
        a = c["address"]
        if c.get("group") not in spec.groups:
            rep.error(f"{a}: group '{c.get('group')}' is not in groups")
        timing = c.get("timing")
        for t in timing if isinstance(timing, list) else [timing]:
            if t not in spec.timings:
                rep.error(f"{a}: timing '{t}' is not in timings")
        check_args(a, c.get("args", []))
        for m in spec.response_messages(c):
            if m not in msg_set:
                rep.error(f"{a}: response '{m}' is not in messages")
        for m in c.get("notifies", []):
            if m not in msg_set:
                rep.error(f"{a}: notifies '{m}' is not in messages")
        for s in c.get("see_also", []):
            if s not in all_addrs:
                rep.error(f"{a}: see_also '{s}' is not in commands or messages")
            if s == a:
                rep.error(f"{a}: see_also refers to itself")
        for e in c.get("errors", []):
            if e not in error_names:
                rep.error(f"{a}: error '{e}' is not a value of /error/command")
        routed = c.get("routed_on")
        if routed and set(spec.boards_of(c)) - set(routed):
            rep.error(f"{a}: boards {c.get('boards')} include boards not in routed_on {routed}")

    for m in spec.messages:
        check_args(m["address"], m.get("args", []))

    for s in spec.settings:
        for c in s.get("commands", []):
            if c not in cmd_set:
                rep.error(f"setting {s['key']}: command '{c}' is not in commands")
        if s.get("section") != s["key"].split(".")[0]:
            rep.error(f"setting {s['key']}: section '{s.get('section')}' does not match the key")

    for where, lang, text in spec.iter_texts():
        for link in spec.links(text):
            if link not in all_addrs:
                rep.error(f"{where} ({lang}): link [[{link}]] is not in commands or messages")


def check_warnings(spec: Spec, rep: Report):
    for where, lang, text in spec.iter_texts():
        if not text.strip():
            rep.warn(f"empty {lang} text: {where}")
    for m in spec.messages:
        if "description" not in m:
            rep.warn(f"message without description: {m['address']}")
    # `values` entries write en / ja next to `value`; the schema does not require ja
    def values_of(owner: str, args: list, kind: str):
        for a in args:
            vals = spec.expand_arg(a).get("values") if "use" in a else a.get("values")
            lists = list(vals.values()) if spec.is_board_map(vals) else [vals]
            for lst in lists:
                for v in lst or []:
                    yield f"{owner}.{a.get('name', a.get('use'))}.{v['value']}", v

    owners = [(c["address"], c.get("args", [])) for c in spec.commands]
    owners += [(m["address"], m.get("args", [])) for m in spec.messages]
    for owner, args in owners:
        for where, v in values_of(owner, args, "arg"):
            if v.get("en", "").strip() and "ja" not in v:
                rep.warn(f"missing ja text: {where}")
    for s in spec.settings:
        lists = list(s["values"].values()) if spec.is_board_map(s.get("values")) else [s.get("values")]
        for lst in lists:
            for v in lst or []:
                if v.get("en", "").strip() and "ja" not in v:
                    rep.warn(f"missing ja text: {s['key']}.{v['value']}")


# ----------------------------------------------------------------------
# Japanese wording


def load_glossary(path: Path = GLOSSARY_PATH) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def strip_markup(text: str, placeholder: str = SENTINEL) -> str:
    """Replace what the wording checks skip. Line breaks are kept, so line numbers stay right."""
    def blank(m, keep_one):
        s = m.group(0)
        return (placeholder if keep_one else "") + "\n" * s.count("\n")

    text = GENERATED_BLOCK_RE.sub(lambda m: blank(m, False), text)
    for rx, comment_like in _STRIP:
        text = rx.sub(lambda m, c=comment_like: blank(m, not c), text)
    return text


def check_wording(text: str, glossary: dict) -> list[tuple[str, str, int]]:
    """[(kind, detail, line)] for one text (line from 1). kind: 'avoid' (detail: the word) or 'space'."""
    plain = strip_markup(text)
    found: list[tuple[str, str, int]] = []
    # words are looked up with the spaces next to ASCII removed ("HOME センサ" is "HOMEセンサ"); line breaks stay
    words = SPACE_RE.sub("", plain)
    for term in glossary.get("terms", []):
        allowed = [m.span() for pat in term.get("allow", []) for m in re.finditer(pat, words)]
        hits = [(m.span(), word) for word in term.get("avoid", []) for m in re.finditer(re.escape(word), words)]
        for (a, b), word in hits:
            if any(x <= a and b <= y for x, y in allowed):
                continue
            if any((x, y) != (a, b) and x <= a and b <= y for (x, y), _ in hits):
                continue  # inside a longer word of the same term (最大速さ / 速さ)
            found.append(("avoid", word, words.count("\n", 0, a) + 1))
    if glossary.get("spacing", {}).get("no_space_between_ascii_and_ja"):
        for m in SPACE_RE.finditer(plain):
            ctx = plain[max(0, m.start() - 6):m.end() + 6].replace(SENTINEL, "`…`").replace("\n", " ")
            found.append(("space", ctx, plain.count("\n", 0, m.start()) + 1))
    return found


def _is_excluded(rel: str, patterns: list[str]) -> bool:
    for pat in patterns:
        pat = pat.strip()
        if not pat or pat.startswith("#"):
            continue
        if pat.startswith("/"):
            pat = pat.lstrip("/")
            if rel == pat.rstrip("/") or rel.startswith(pat.rstrip("/") + "/") or Path(rel).match(pat):
                return True
        elif Path(rel).match(pat) or any(Path(part).match(pat) for part in Path(rel).parts):
            return True
    return False


def japanese_texts() -> list[tuple[str, str]]:
    """(where, text) for the texts outside the spec that the wording checks read."""
    out: list[tuple[str, str]] = []
    mk = yaml.safe_load(MKDOCS_PATH.read_text(encoding="utf-8")) if MKDOCS_PATH.exists() else {}
    patterns = str(mk.get("exclude_docs") or "").splitlines()

    for md in sorted(DOCS_JA.rglob("*.md")):
        rel = md.relative_to(REPO_ROOT / "docs").as_posix()
        if _is_excluded(rel, patterns):
            continue
        text = md.read_text(encoding="utf-8")
        if "This page is generated from spec/osc-commands.yaml" in text:
            continue  # made from the spec; the `ja` texts are checked there
        out.append((f"docs/{rel}", text))

    for plugin in mk.get("plugins") or []:
        if isinstance(plugin, dict) and "i18n" in plugin:
            for lang in plugin["i18n"].get("languages") or []:
                if lang.get("locale") == "ja":
                    for k, v in (lang.get("nav_translations") or {}).items():
                        out.append((f"mkdocs.yml nav_translations.{k}", str(v)))

    out.extend(generate_py_texts())
    return out


def generate_py_texts(path: Path = GENERATE_PATH) -> list[tuple[str, str]]:
    """Japanese string constants of tools/generate.py (docstrings excluded).

    An f-string counts as one text with {} for each value."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
                docstrings.add(id(node.body[0].value))
    ja = re.compile(rf"[{_JA}]")
    out: list[tuple[str, str]] = []

    def text_of(s: str) -> str:
        return re.sub(r"\{[A-Za-z_]*\}", SENTINEL, s)  # "{boards} のみ" is "STEP400 のみ" when shown

    def visit(node):
        if isinstance(node, ast.JoinedStr):
            s = "".join(v.value if isinstance(v, ast.Constant) else SENTINEL for v in node.values)
            if ja.search(s):
                out.append((f"tools/generate.py:{node.lineno}", text_of(s)))
            return
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstrings:
            if ja.search(node.value):
                out.append((f"tools/generate.py:{node.lineno}", text_of(node.value)))
            return
        for child in ast.iter_child_nodes(node):
            visit(child)

    visit(tree)
    return out


def check_japanese_wording(spec: Spec, rep: Report):
    glossary = load_glossary()

    def report(where: str, text: str, line_of: bool):
        for kind, detail, line in check_wording(text, glossary):
            loc = f"{where}:{line}" if line_of else where
            if kind == "avoid":
                rep.glossary(f"wording: {loc}: avoid '{detail}'", detail)
            else:
                rep.glossary(f"spacing: {loc}: space between ASCII and Japanese: …{detail}…", "(空白)")

    for where, lang, text in spec.iter_texts():
        if lang == "ja":
            report(where, text, False)
    for where, text in japanese_texts():
        report(where, text, where.startswith("docs/"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=str(SPEC_PATH))
    ap.add_argument("-q", "--quiet", action="store_true", help="print counts only (warnings, Japanese wording errors)")
    args = ap.parse_args()

    spec = Spec.load(args.path)
    rep = Report()
    check_schema(spec, rep)
    if not rep.errors:
        check_board_keys(spec, rep)
        check_references(spec, rep)
    check_warnings(spec, rep)
    check_japanese_wording(spec, rep)

    for e in rep.errors:
        if args.quiet and e.startswith(("wording:", "spacing:")):
            continue
        print(f"ERROR   {e}")
    if args.quiet and rep.glossary_hits:
        print("Japanese wording errors: " + ", ".join(f"{k}: {n}" for k, n in sorted(rep.glossary_hits.items())))
    if not args.quiet:
        for w in rep.warnings:
            print(f"warning {w}")

    kinds = Counter(w.split(":")[0] for w in rep.warnings)
    print()
    print(f"commands: {len(spec.commands)}  messages: {len(spec.messages)}  settings: {len(spec.settings)}")
    print(f"errors: {len(rep.errors)}  warnings: {len(rep.warnings)}"
          + (" (" + ", ".join(f"{k}: {n}" for k, n in sorted(kinds.items())) + ")" if kinds else ""))
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
