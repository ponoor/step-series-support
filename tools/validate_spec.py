#!/usr/bin/env python3
"""Validate spec/osc-commands.yaml.

    python tools/validate_spec.py [path/to/osc-commands.yaml]

Checks
  - the format, with spec/osc-commands.schema.json
  - references: group, timing, use, response / notifies (-> messages),
    see_also and [[...]] links (-> commands / messages; `[[network.destIp]]` -> settings), setting (-> settings),
    settings.*.commands (-> commands), errors (-> values of /error/command)
  - duplicated addresses and setting keys
  - keys of board-specific values are boards defined in `boards`
  - Japanese wording (spec/glossary_ja.yaml), in two levels:
      error   words that are never used (level omitted in the glossary), and a space between an ASCII
              letter/digit and a Japanese character, between two Japanese characters, or between a number
              and its unit (spacing.units) in a Japanese sentence, and half-width parentheses next to a
              Japanese character (they must be （ ）). Fails the check.
      review  words that are right in some contexts (`level: review`). Listed for a person to read; never
              fails. A listed place that was read and judged fine goes to spec/glossary_ja_reviewed.yaml
              (where / term / text / note); it is not listed again while `text` is in the sentence, and
              a record whose `text` is gone gives the warning "reviewed record is stale".
    Checked in every `ja` text of the spec, in docs/ja/**/*.md (not the pages in exclude_docs, and not
    the pages generated from the spec), in the Japanese nav_translations of mkdocs.yml and in the
    Japanese fixed texts of tools/generate.py. Inline code, code blocks, [[...]] links, URLs, HTML
    comments and generated blocks are left out (code and links count as one ASCII word for spacing);
    the target of a Markdown link `[text](target)` is left out. A signed number (-1, +5) counts as ASCII for
    the spacing; in a table row the unit check reads only the cells with Japanese (the range / unit column
    is left out).

    python tools/validate_spec.py --ja                  only the Japanese checks, one finding per line
                                                        (YAML line, place, word, context)
    python tools/validate_spec.py --ja --review-only    only the review findings

The commit hook tools/hooks/pre-commit runs `validate_spec.py -q` and `generate.py --check`. To turn it on
(once per clone):  git config core.hooksPath tools/hooks
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
    (re.compile(r"(?<=\])\([^()\s]*\)"), True),                    # the target of a Markdown link: [text](target)
]
GENERATED_BLOCK_RE = re.compile(r"<!-- generated:begin .*?<!-- generated:end [^\n]*-->", re.S)
# ASCII letters and digits (and a stripped piece) next to a Japanese character with spaces between
_JA = "\u3000-\u30ff\u3400-\u9fff\uff00-\uffef"
_ASCII = f"A-Za-z0-9{SENTINEL}"
# A signed number ("-1", "+5") is ASCII too: "を -1として" has a space between a Japanese character and "-1".
# The sign counts only when a digit follows and no letter, digit or Japanese character is before it
# (so a list marker "- 1" and a dash are not taken).
SPACE_RE = re.compile(rf"(?:(?<=[{_ASCII}]) +(?=[{_JA}])|(?<=[{_JA}]) +(?=[{_ASCII}]|[-+]\d))")
JJ_SPACE_RE = re.compile(rf"(?<=[{_JA}]) +(?=[{_JA}])")      # between two Japanese characters
_KANJI_KANA = re.compile("[\u3040-\u30ff\u3400-\u9fff]")


def unit_space_re(units: list[str]):
    """A space between a digit and a unit ("64 mA"), for the units of the glossary (spacing.units)."""
    alt = "|".join(re.escape(u) for u in sorted(units, key=len, reverse=True))
    # not after a fraction: "1/16 microstep" is the name of a value
    return re.compile(rf"(?<!/\d)(?<!/\d\d)(?<!/\d\d\d)(?<=\d) +(?=(?:{alt})(?![A-Za-z0-9_]))")


def paren_pairs(text: str) -> list[tuple[int, int]]:
    """Matched pairs (i, j) of half-width parentheses in `text`."""
    stack: list[int] = []
    pairs: list[tuple[int, int]] = []
    for i, ch in enumerate(text):
        if ch == "(":
            stack.append(i)
        elif ch == ")" and stack:
            pairs.append((stack.pop(), i))
    return pairs


def japanese_parens(text: str) -> list[tuple[int, int]]:
    """Pairs of half-width parentheses that must be full-width: a Japanese character (spaces skipped) is
    next to the pair on either side, outside or inside."""
    ja = re.compile(f"[{_JA}]")

    def near(i: int, step: int) -> bool:
        i += step
        while 0 <= i < len(text) and text[i] == " ":
            i += step
        return 0 <= i < len(text) and bool(ja.match(text[i]))

    return [(i, j) for i, j in paren_pairs(text) if near(i, -1) or near(i, 1) or near(j, -1) or near(j, 1)]


REVIEWED_PATH = REPO_ROOT / "spec" / "glossary_ja_reviewed.yaml"


class Report:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.glossary_hits: Counter = Counter()  # Japanese wording errors, by word
        self.review: list[dict] = []             # Japanese wording findings to read (never fail)

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

    setting_keys = {s["key"] for s in spec.settings}
    for where, lang, text in spec.iter_texts():
        for link in spec.links(text):
            if link not in all_addrs:
                rep.error(f"{where} ({lang}): link [[{link}]] is not in commands or messages")
        for link in spec.setting_links(text):
            if link not in setting_keys:
                rep.error(f"{where} ({lang}): link [[{link}]] is not in settings")


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


def _sentence(words: str, a: int, b: int) -> str:
    s = max(words.rfind("。", 0, a), words.rfind("\n", 0, a)) + 1
    ends = [i for i in (words.find("。", b), words.find("\n", b)) if i >= 0]
    return words[s:(min(ends) + 1 if ends else len(words))]


def find_wording(text: str, glossary: dict) -> list[dict]:
    """Findings of one text: {level: error|review, kind: avoid|space, word, line, span, ctx, words}.

    `words` is the text without code and links and without the spaces next to ASCII (the string the spans refer to)."""
    plain = strip_markup(text)
    found: list[dict] = []
    # words are looked up with the spaces next to ASCII removed ("HOME センサ" is "HOMEセンサ"); line breaks stay
    words = SPACE_RE.sub("", plain)

    def ctx_of(a: int, b: int) -> str:
        return words[max(0, a - 20):b + 20].replace(SENTINEL, "`…`").replace("\n", " ")

    for term in glossary.get("terms", []):
        level = term.get("level", "error")
        allowed = [m.span() for pat in term.get("allow", []) for m in re.finditer(pat, words)]
        hits = [(m.span(), word) for word in term.get("avoid", []) for m in re.finditer(re.escape(word), words)]
        hits += [(m.span(), m.group(0)) for pat in term.get("avoid_regex", []) for m in re.finditer(pat, words)]
        for (a, b), word in hits:
            if any(x <= a and b <= y for x, y in allowed):
                continue
            if any((x, y) != (a, b) and x <= a and b <= y for (x, y), _ in hits):
                continue  # inside a longer word of the same term (最大速さ / 速さ)
            if any(re.search(pat, _sentence(words, a, b)) for pat in term.get("unless_sentence", [])):
                continue
            found.append({"level": level, "kind": "avoid", "word": word, "line": words.count("\n", 0, a) + 1,
                          "span": (a, b), "ctx": ctx_of(a, b), "words": words, "term": term.get("use")})
    if glossary.get("spacing", {}).get("no_space_between_ascii_and_ja"):
        for rx in (SPACE_RE, JJ_SPACE_RE):
            for m in rx.finditer(plain):
                ctx = plain[max(0, m.start() - 12):m.end() + 12].replace(SENTINEL, "`…`").replace("\n", " ")
                found.append({"level": "error", "kind": "space", "word": "(空白)", "line": plain.count("\n", 0, m.start()) + 1,
                              "span": m.span(), "ctx": ctx, "words": plain, "term": None})
    if glossary.get("spacing", {}).get("fullwidth_parentheses"):
        for i, j in japanese_parens(plain):
            ctx = plain[max(0, i - 8):j + 8].replace(SENTINEL, "`…`").replace("\n", " ")
            found.append({"level": "error", "kind": "space", "word": "(半角の括弧)", "line": plain.count("\n", 0, i) + 1,
                          "span": (i, j + 1), "ctx": ctx, "words": plain, "term": None})
    units = glossary.get("spacing", {}).get("units")
    if units:
        # inside a Japanese sentence (a line with kana or kanji) the unit follows the number without a space
        offset = 0
        unit_re = unit_space_re(units)
        for line in plain.split("\n"):
            # a table row is checked cell by cell: a cell without Japanese (the range / unit column) is left out
            cells = [(m.start(), m.group(0)) for m in re.finditer(r"[^|]+", line)] if line.lstrip().startswith("|") else [(0, line)]
            for start, text in cells:
                if not _KANJI_KANA.search(text):
                    continue
                for m in unit_re.finditer(text):
                    a = offset + start + m.start()
                    ctx = plain[max(0, a - 12):a + 14].replace(SENTINEL, "`…`").replace("\n", " ")
                    found.append({"level": "error", "kind": "space", "word": "(数字と単位)", "line": plain.count("\n", 0, a) + 1,
                                  "span": (a, offset + start + m.end()), "ctx": ctx, "words": plain, "term": None})
            offset += len(line) + 1
    return found


def check_wording(text: str, glossary: dict) -> list[tuple[str, str, int]]:
    """[(kind, detail, line)] for one text (line from 1). kind: 'avoid' (error level, detail: the word),
    'review' (review level, detail: the word) or 'space'."""
    out = []
    for f in find_wording(text, glossary):
        kind = "space" if f["kind"] == "space" else ("avoid" if f["level"] == "error" else "review")
        out.append((kind, f["ctx"] if kind == "space" else f["word"], f["line"]))
    return out


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


def yaml_lines(path: Path) -> dict[str, int]:
    """{where: first line of the `ja` text in the YAML file}, with `where` spelled as Spec.iter_texts does."""
    lines: dict[str, int] = {}

    def label(node, i):
        if isinstance(node, yaml.MappingNode):
            d = {k.value: v for k, v in node.value if isinstance(k, yaml.ScalarNode) and isinstance(v, yaml.ScalarNode)}
            for key in ("address", "key", "name"):
                if d.get(key) is not None and d[key].value != "":
                    return d[key].value
        return str(i)

    def walk(node, where):
        if isinstance(node, yaml.MappingNode):
            for k, val in node.value:
                key = k.value
                if key == "ja" and isinstance(val, yaml.ScalarNode):
                    lines[where] = val.start_mark.line + 1 + (1 if val.style in ("|", ">") else 0)
                elif key != "en":
                    walk(val, f"{where}.{key}" if where else str(key))
        elif isinstance(node, yaml.SequenceNode):
            for i, val in enumerate(node.value):
                walk(val, f"{where}[{label(val, i)}]")

    walk(yaml.compose(Path(path).read_text(encoding="utf-8")), "")
    return lines


def load_reviewed(path: Path = REVIEWED_PATH) -> list[dict]:
    if not path.exists():
        return []
    return yaml.safe_load(path.read_text(encoding="utf-8")) or []


def _norm(text: str) -> str:
    return SPACE_RE.sub("", strip_markup(text))


def japanese_findings(spec: Spec, glossary: dict | None = None, reviewed: list[dict] | None = None, files: bool = True):
    """(findings, stale): findings are dicts {level, kind, word, ctx, file, where, ...}; level 'review' findings that
    a reviewed record covers are left out. stale: messages for records whose text is no longer there."""
    glossary = glossary or load_glossary()
    reviewed = load_reviewed() if reviewed is None else reviewed
    try:
        rel = Path(spec.path).resolve().relative_to(REPO_ROOT).as_posix()
    except (TypeError, ValueError):
        rel = str(spec.path)
    lines = yaml_lines(spec.path) if spec.path else {}
    texts: dict[str, str] = {}
    out: list[dict] = []

    def add(file: str, where: str, text: str, line_base: int | None):
        for f in find_wording(text, glossary):
            f["file"] = f"{file}:{line_base + f['line'] - 1}" if line_base else file
            f["where"] = where
            out.append(f)

    for where, lang, text in spec.iter_texts():
        if lang != "ja" or where.endswith(".label"):
            continue  # configuration item labels stay English
        texts[f"{where}.ja"] = text
        add(rel, f"{where}.ja", text, lines.get(where))
    for where, text in (japanese_texts() if files else []):
        texts[where] = text
        if where.startswith("docs/"):
            add(where, where, text, 1)
        else:
            for f in find_wording(text, glossary):
                f["file"] = where
                f["where"] = where
                out.append(f)

    stale: list[str] = []
    covered_ids: set[int] = set()
    for rec in reviewed:
        where, term, want = rec.get("where"), rec.get("term"), rec.get("text", "")
        have = _norm(texts[where]) if where in texts else None
        want_n = _norm(want)
        if have is None or want_n not in have:
            stale.append(f"reviewed record is stale: {where} [{term}] {want!r}")
            continue
        spans = [(m.start(), m.end()) for m in re.finditer(re.escape(want_n), have)]
        for i, f in enumerate(out):
            if f["level"] == "review" and f["where"] == where and f.get("word") == term:
                if any(a <= f["span"][0] and f["span"][1] <= b for a, b in spans):
                    covered_ids.add(i)
    return [f for i, f in enumerate(out) if i not in covered_ids], stale


def check_japanese_wording(spec: Spec, rep: Report):
    findings, stale = japanese_findings(spec)
    for f in findings:
        if f["level"] == "error":
            if f["kind"] == "avoid":
                rep.glossary(f"wording: {f['file']}: {f['where']}: avoid '{f['word']}': …{f['ctx']}…", f["word"])
            else:
                rep.glossary(f"spacing: {f['file']}: {f['where']}: space between ASCII and Japanese, two Japanese characters, a number and its unit, or half-width parentheses in a Japanese sentence: …{f['ctx']}…", "(空白)")
        else:
            rep.review.append(f)
    for s in stale:
        rep.warn(s)


def print_findings(spec: Spec, review_only: bool) -> int:
    findings, stale = japanese_findings(spec)
    n_err = n_rev = 0
    for f in findings:
        if f["level"] == "error":
            n_err += 1
            if review_only:
                continue
        else:
            n_rev += 1
        print(f"{f['level']:<6} {f['file']:<42} {'' if f['file'].startswith(f['where']) else f['where']:<46} [{f['word']}] …{f['ctx']}…")
    for s in stale:
        print(f"warning {s}")
    print()
    print(f"error: {n_err}  review: {n_rev}  stale records: {len(stale)}")
    return 1 if n_err else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=str(SPEC_PATH))
    ap.add_argument("-q", "--quiet", action="store_true", help="print counts only (warnings, Japanese wording errors)")
    ap.add_argument("--ja", action="store_true", help="only the Japanese wording checks, one finding per line")
    ap.add_argument("--review-only", action="store_true", help="with --ja: only the findings to review")
    args = ap.parse_args()

    spec = Spec.load(args.path)
    if args.ja:
        return print_findings(spec, args.review_only)
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
    if rep.review:
        print(f"Japanese wording to review: {len(rep.review)} (python tools/validate_spec.py --ja --review-only)")
    print(f"commands: {len(spec.commands)}  messages: {len(spec.messages)}  settings: {len(spec.settings)}")
    print(f"errors: {len(rep.errors)}  warnings: {len(rep.warnings)}"
          + (" (" + ", ".join(f"{k}: {n}" for k, n in sorted(kinds.items())) + ")" if kinds else ""))
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
