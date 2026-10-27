#!/usr/bin/env python3
"""Generate Markdown from spec/osc-commands.yaml.

    python tools/generate.py                      # write
    python tools/generate.py --check              # write nothing, exit 1 if a file would change
    python tools/generate.py --defaults firmware  # initial values: firmware | template | both (default)

What it does (docs directory: --docs, default `docs/`)

1. Expands the markers in the hand-written Markdown pages. A marker is a line of its own:

       <!-- osc: /setMicrostepMode -->            reference block of a command
       <!-- osc-message: /booted -->              reference block of a message
       <!-- osc-related: motion, position -->     list of the commands of these groups
       <!-- osc-settings: speedProfile -->        list of the settings of these sections

   The generated text goes right below the marker, between
   `<!-- generated:begin ... -->` and `<!-- generated:end ... -->`. The marker itself stays,
   so running the script again replaces the block with the same text (idempotent). A page without
   markers is never touched. A marker with an unknown address is an error and nothing is written.
   The language of a page comes from the `en` / `ja` directory in its path (docs/en/..., docs/ja/...)
   or from its name (`_en.md` / `_jp.md`, `.en.md` / `.ja.md`).

2. Writes the generated pages (first line says they are generated; do not edit them):
   command list, differences between STEP400 and STEP800 (both under
   `<lang>/reference/`), and the list of configuration items
   (`<lang>/connections/`). English and Japanese. An existing front matter is kept.

Japanese texts are taken from the YAML. A Japanese text that does not exist yet is filled with
the English one; the number of such texts is printed.

Initial values (`--defaults`): `firmware` shows the built-in value of the firmware, `template`
the value of configGenerator/configTemplate_*.json, `both` (default) shows both when they differ.

Markers are counted in docs/en/ and docs/ja/ only (the old pages are not counted; the expansion above looks at all of
`docs/`). The usual run prints one WARNING line per language with the numbers and does not change the exit code;
`--coverage` (also in the commit hook) lists every missing, duplicated or misplaced marker as an error.

Exit code 1 on an error (unknown address, broken `[[link]]`, changes with --check).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec import LINK_RE, REPO_ROOT, SPEC_PATH, Spec, anchor  # noqa: E402

# ---------------------------------------------------------------------------
# Layout of the pages. Change here when the site structure changes.

REF_DIR = "reference"                                    # reference pages of the groups (under docs/<lang>/)
MESSAGES_PAGE = "automatically-sent-messages"            # page of the messages
COMMAND_LIST_PAGE = "command-list"
DIFF_PAGE = "differences-step400-step800"
SETTINGS_DIR = "connections"
SETTINGS_PAGE = "configuration-items"
# The Japanese file of a page that has another name than the English one (none now)
JP_PAGE_NAMES: dict[str, str] = {}
# Messages that are described on their own in the page of the messages, besides the ones that no command
# lists in `response` / `notifies` and the ones that some command lists in `notifies` (standalone_messages()).
STANDALONE_MESSAGES = ("/booted", "/error/osc", "/error/command")

LANGS = ("en", "ja")                                      # docs/en/..., docs/ja/... (mkdocs-static-i18n, folder structure)
SUFFIX = {"en": ".md", "ja": ".md"}

GENERATED_NOTE = {
    "en": "<!-- This page is generated from spec/osc-commands.yaml by tools/generate.py. Do not edit it directly. -->",
    "ja": "<!-- This page is generated from spec/osc-commands.yaml by tools/generate.py. Do not edit it directly. (自動生成・直接編集しない) -->",
}
GENERATED_FILE_MARK = "This page is generated from spec/osc-commands.yaml"

LABELS = {
    "en": {
        "argument": "Argument", "none": "None", "type": "Type", "range": "Range", "description": "Description",
        "value": "Value", "meaning": "Meaning", "timing": "Executable timing", "response": "Response",
        "errors": "Errors", "initial": "Initial value", "changes": "Changes", "see_also": "See also",
        "only": "Available on {boards} only.", "added": "Added in v{v}.", "all_motors": "all motors",
        "firmware": "firmware", "template": "template", "when": "When",
        "command": "Command", "arguments": "Arguments", "since": "Since", "key": "Key", "label": "Name",
        "unit": "Unit", "initial_col": "Initial value", "commands_col": "Commands", "per_motor": "per motor",
        "list_title": "Command list", "list_intro": "All OSC commands in the order of the reference pages. Click a command to go to its reference.",
        "diff_title": "Differences between STEP400 and STEP800",
        "diff_only": "Commands available on {boards} only", "diff_msg_only": "Messages sent by {boards} only",
        "diff_values": "Commands with board-specific values", "diff_msg_values": "Messages with board-specific values",
        "diff_settings": "Configuration items with board-specific values", "diff_set_only": "Configuration items of {boards} only",
        "diff_tables": "Board-specific tables", "none_found": "None.",
        "settings_title": "Configuration items", "settings_intro": "Items of the configuration file (JSON on the microSD card). The initial value is the one used when the file or the key is missing.",
        "related": "Related commands", "related_settings": "Related configuration items",
        "all": "all", "motors": "motors", "first": "Initial value of the firmware", "boards_only": "{boards} only",
    },
    "ja": {
        "argument": "引数", "none": "なし", "type": "型", "range": "範囲", "description": "説明",
        "value": "値", "meaning": "意味", "timing": "実行可能タイミング", "response": "返信",
        "errors": "エラー", "initial": "初期値", "changes": "変更", "see_also": "関連",
        "only": "{boards}のみ。", "added": "v{v}で追加。", "all_motors": "全モータ",
        "firmware": "ファームウェア", "template": "テンプレート", "when": "条件",
        "command": "コマンド", "arguments": "引数", "since": "追加", "key": "キー", "label": "名称",
        "unit": "単位", "initial_col": "初期値", "commands_col": "コマンド", "per_motor": "モータごと",
        "list_title": "コマンド一覧", "list_intro": "すべてのOSCコマンドを、リファレンスのページの順に並べています。コマンド名から詳細へ移動できます。",
        "diff_title": "STEP400とSTEP800の違い",
        "diff_only": "{boards}のみで使えるコマンド", "diff_msg_only": "{boards}のみが送信するメッセージ",
        "diff_values": "ボードによって値が異なるコマンド", "diff_msg_values": "ボードによって値が異なるメッセージ",
        "diff_settings": "ボードによって値が異なる設定項目", "diff_set_only": "{boards}のみの設定項目",
        "diff_tables": "ボード別の表", "none_found": "なし。",
        "settings_title": "設定項目一覧", "settings_intro": "設定ファイル（microSDカードのJSON）の項目です。初期値は、設定ファイルまたはそのキーがないときの値です。",
        "related": "関連するコマンド", "related_settings": "関連する設定項目",
        "all": "すべて", "motors": "モータ", "first": "ファームウェアの初期値", "boards_only": "{boards}のみ",
    },
}

MARKER_RE = re.compile(
    r"^<!--\s*(osc|osc-message|osc-related|osc-settings)\s*:\s*(.+?)\s*-->[ \t]*(?:\n|\Z)"
    r"(?:<!-- generated:begin [^\n]*-->\n.*?<!-- generated:end [^\n]*-->(?:\n|\Z))?",
    re.M | re.S,
)


class GenerateError(Exception):
    pass


# ---------------------------------------------------------------------------
# context

class Ctx:
    """Everything a renderer needs: the spec, the language, the options and the counters."""

    def __init__(self, spec: Spec, lang: str, defaults: str, counter: Counter, errors: list[str]):
        self.spec = spec
        self.lang = lang
        self.defaults = defaults
        self.counter = counter
        self.errors = errors
        self.L = LABELS[lang]
        self.page_dir = REF_DIR        # directory (under docs/<lang>/) of the page being written
        self.rel_from = Path(REF_DIR)  # directory (under docs/<lang>/) links are relative to
        self.where = ""
        self.block_anchor: str | None = None   # anchor of the command / message block being written (no link to itself)

    # -- texts ------------------------------------------------------------
    def tx(self, value: Any, kind: str = "text") -> str:
        """A language-neutral string, or {en, ja}. Japanese falls back to English (counted)."""
        if value is None:
            return ""
        if isinstance(value, str):
            return value
        if isinstance(value, (int, float, bool)):
            return fmt(value)
        text = value.get(self.lang) or ""
        en = value.get("en") or ""
        if self.lang == "ja" and not text:
            if en:
                self.counter[kind] += 1
            return en
        return text

    def item_text(self, item: dict, kind: str) -> str:
        """en / ja written next to other fields (values, changes)."""
        return self.tx({"en": item.get("en", ""), "ja": item.get("ja", "")}, kind)

    # -- joining (Japanese: no space next to a Japanese character; full-width parentheses) -------
    def paren(self, text: str) -> str:
        """A parenthetical to append to a text: " (text)" in English, "（text）" in Japanese."""
        return f" ({text})" if self.lang == "en" else f"（{text}）"

    @property
    def comma(self) -> str:
        return ", " if self.lang == "en" else "、"

    def join(self, *parts: str) -> str:
        """The non-empty parts in a row: separated by a space in English; in Japanese by a space only where both
        sides are not Japanese."""
        return join_texts([p for p in parts if p], self.lang)

    def oneline(self, text: str) -> str:
        """A text on one line (table cell, list item). Line breaks become a space (English) or nothing between
        Japanese characters (Japanese)."""
        return join_lines(text, self.lang)

    # -- links ------------------------------------------------------------
    def page_file(self, page: str) -> Path:
        name = JP_PAGE_NAMES.get(page, page) if self.lang == "ja" else page
        return Path(REF_DIR) / f"{name}{SUFFIX[self.lang]}"

    def link_to(self, address: str, prefer: str = "command") -> str | None:
        """Relative link (file#anchor) to the heading of a command / message.

        A message that is not standalone (standalone_messages()) is shown in the response of the first command
        that lists it in `response`; the link goes to that command.
        """
        spec = self.spec
        cmd, msg = spec.command(address), spec.message(address)
        use_message = msg is not None and (prefer == "message" or cmd is None)
        if use_message and address not in standalone_messages(spec):
            owner = response_owner(spec, address)
            if owner is not None:
                cmd, use_message = owner, False
                address = owner["address"]
        if use_message:
            target = Path(REF_DIR) / f"{MESSAGES_PAGE}{SUFFIX[self.lang]}"
        elif cmd is not None:
            target = self.page_file(spec.groups[cmd["group"]]["page"])
        else:
            return None
        rel = Path(_relpath(target, self.rel_from)).as_posix()
        return f"{rel}#{anchor(address)}"

    def md(self, text: str) -> str:
        """Text of a description: `[[/address]]` -> link; single line breaks kept as line breaks."""
        def repl(m: re.Match) -> str:
            addr = m.group(1)
            href = self.link_to(addr)
            if href is None:
                self.errors.append(f"{self.where}: broken link [[{addr}]]")
                return f"`{addr}`"
            if self.block_anchor and href.endswith("#" + self.block_anchor):
                return f"`{addr}`"   # the block links to itself: code, not a link
            return f"[`{addr}`]({href})"

        text = LINK_RE.sub(repl, text.strip("\n"))
        lines = text.split("\n")
        out = []
        for i, ln in enumerate(lines):
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if ln.strip() and nxt.strip() and not ln.endswith("  ") and not _is_block_line(ln, nxt):
                ln += "  "
            out.append(ln)
        return "\n".join(out)


_JA_CHAR = "\u3000-\u30ff\u3400-\u9fff\uff00-\uffef"
_JA_END = re.compile(f"[{_JA_CHAR}]$")
_JA_START = re.compile(f"^[{_JA_CHAR}]")


def join_texts(parts: list[str], lang: str) -> str:
    """Join texts with a space (English). Japanese: no space next to a Japanese character (full-width
    parentheses and punctuation included), so "。" + "v2.2.0で追加。" stays "。v2.2.0で追加。"."""
    out = ""
    for p in parts:
        if out and (lang == "en" or not (_JA_END.search(out) or _JA_START.match(p))):
            out += " "
        out += p
    return out


def join_lines(text: str, lang: str) -> str:
    """The lines of a text on one line (see Ctx.oneline)."""
    if lang == "en":
        return text.replace("\n", " ")
    return join_texts([ln.strip() for ln in text.split("\n") if ln.strip()], lang)


def _relpath(target: Path, start: Path) -> str:
    import os
    return os.path.relpath(target.as_posix(), start.as_posix())


def _is_block_line(line: str, nxt: str) -> bool:
    """Lines where a hard break would be wrong: lists, tables, code fences."""
    s = line.lstrip()
    n = nxt.lstrip()
    return s.startswith(("```", "|", "- ", "* ", "#")) or n.startswith(("```", "|", "- ", "* "))


# ---------------------------------------------------------------------------
# formatting helpers

def fmt(v: Any) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        return str(int(v)) if v.is_integer() else f"{v:g}"
    if isinstance(v, list):
        return ", ".join(fmt(x) for x in v)
    return str(v)


def cell(text: Any) -> str:
    text = re.sub(f"(?:(?<=[{_JA_CHAR}]) *\n *| *\n *(?=[{_JA_CHAR}]))", "", str(text))
    return text.replace("|", "\\|").replace("\n", " ").strip()


def table(header: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(cell(h) for h in header) + " |", "|" + "|".join(" --- " for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join(cell(c) for c in r) + " |")
    return "\n".join(out)


def ip_or_value(setting_type: str, v: Any) -> str:
    if setting_type == "ip" and isinstance(v, list):
        return ".".join(str(x) for x in v)
    if setting_type == "mac" and isinstance(v, list):
        return ":".join(f"{x:02X}" for x in v)
    if setting_type == "version" and isinstance(v, list):
        return ".".join(str(x) for x in v)
    if v == "":
        return '""'
    return fmt(v)


def boards_text(spec: Spec, boards: list[str]) -> str:
    return ", ".join(boards)


def board_sorted(spec: Spec, boards) -> list[str]:
    return [b for b in spec.board_names if b in boards]


# ---------------------------------------------------------------------------
# arguments

def arg_type_name(a: dict) -> str:
    return {"int": "int", "float": "float", "bool": "bool", "string": "string"}.get(a.get("type"), str(a.get("type")))


def arg_heading(spec: Spec, cmd_or_msg: dict) -> str:
    parts = []
    for a in spec.args(cmd_or_msg):
        name = a.get("name", a.get("use", "?"))
        if a.get("repeat") == "motors":
            parts.append(f"({arg_type_name(a)}){name}1 ... ({arg_type_name(a)}){name}N")
        else:
            parts.append(f"({arg_type_name(a)}){name}")
    return " ".join(parts)


def range_text(ctx: Ctx, a: dict, in_message: bool) -> str:
    spec = ctx.spec
    rng = a.get("range")
    parts = []
    if rng is not None:
        if spec.is_board_map(rng):
            texts = {b: _rng(spec.for_board(rng, b)) for b in spec.board_names if spec.for_board(rng, b) is not None}
            if len(set(texts.values())) == 1 and len(texts) == len(spec.board_names):
                parts.append(next(iter(texts.values())))
            else:
                parts.append(ctx.comma.join(f"{t}{ctx.paren(b)}" for b, t in texts.items()))
        else:
            parts.append(_rng(rng))
    all_value = a.get("all")
    if not in_message and isinstance(all_value, int) and not isinstance(all_value, bool):
        parts.append(f"{all_value}{ctx.paren(ctx.L['all_motors'])}")
    text = ctx.comma.join(parts)
    if text and a.get("unit"):
        text = ctx.join(text, a["unit"])
    elif a.get("unit"):
        text = a["unit"]
    return text


def _rng(r: list) -> str:
    return f"{fmt(r[0])}-{fmt(r[1])}"


def values_for_board(spec: Spec, values: Any, board: str | None) -> list[dict]:
    if values is None:
        return []
    if spec.is_board_map(values):
        return values.get(board, []) if board else []
    return values


def render_values_tables(ctx: Ctx, a: dict, name: str) -> list[str]:
    """Tables of `values` of an argument (one per board if the values are board-specific)."""
    spec, L = ctx.spec, ctx.L
    values = a.get("values")
    if not values:
        return []
    out = []
    variants: list[tuple[str | None, list[dict]]]
    if spec.is_board_map(values):
        variants = [(b, values[b]) for b in spec.board_names if b in values]
    else:
        variants = [(None, values)]
    for board, items in variants:
        rows = []
        for it in items:
            only = it.get("boards")
            meaning = ctx.md(ctx.item_text(it, "value"))
            if only and set(only) != set(spec.board_names):
                meaning += ctx.paren(L['boards_only'].format(boards=boards_text(spec, board_sorted(spec, only))))
            notes = inline_notes(ctx, it)
            if notes:
                meaning = ctx.join(meaning, notes)
            rows.append([fmt(it["value"]), meaning])
        title = f"`{name}`" + (f" - {board}" if board else "")
        out.append(f"{title}\n\n" + table([L["value"], L["meaning"]], rows))
    return out


def render_args(ctx: Ctx, item: dict, in_message: bool = False) -> str:
    """Table of the arguments plus the tables of values."""
    L = ctx.L
    args = ctx.spec.args(item)
    if not args:
        return L["none"]
    rows, extra = [], []
    for a in args:
        name = a.get("name", a.get("use", "?"))
        if a.get("repeat") == "motors":
            name = f"{name}1 ... {name}N"
        desc = ctx.md(ctx.tx(a.get("description"), "arg"))
        if a.get("value") is not None:
            desc = ctx.join(desc, f"`{a['value']}`")
        if a.get("since"):
            added = ctx.paren(L['added'].format(v=a['since']))
            desc = ctx.join(desc, added.lstrip()) if ctx.lang == "en" else desc + added
        rows.append([name, arg_type_name(a), range_text(ctx, a, in_message), desc])
        extra.extend(render_values_tables(ctx, a, a.get("name", name)))
    out = table([L["argument"], L["type"], L["range"], L["description"]], rows)
    if extra:
        out += "\n\n" + "\n\n".join(extra)
    return out


# ---------------------------------------------------------------------------
# initial values

def default_texts(ctx: Ctx, a: dict) -> dict[str, str] | None:
    """{board: text} of the initial value of an (expanded) argument, or None if it has none."""
    spec, L = ctx.spec, ctx.L
    setting = spec.setting(a["setting"]) if "setting" in a else None
    out: dict[str, str] = {}
    for b in spec.board_names:
        if setting is not None and b not in spec.boards_of(setting):
            continue
        base = spec.arg_default(a, b)
        if base is None:
            continue
        shown = _with_meaning(ctx, a, base, setting)
        if setting is not None and "template" in setting and ctx.defaults != "firmware":
            t = spec.for_board(setting["template"], b, missing=base)
            if t is not None and t != base:
                tshown = _with_meaning(ctx, a, t, setting)
                if ctx.defaults == "template":
                    shown = tshown
                else:
                    shown = (f"{shown}{ctx.paren(L['firmware'])} / {tshown}{ctx.paren(L['template'])}" if ctx.lang == "en"
                             else f"{shown}{ctx.paren(L['firmware'])}、{tshown}{ctx.paren(L['template'])}")
        out[b] = shown
    return out or None


def _with_meaning(ctx: Ctx, a: dict, v: Any, setting: dict | None) -> str:
    spec = ctx.spec
    stype = (setting or {}).get("type", a.get("type", ""))
    text = ip_or_value(stype, v)
    for it in (a.get("values") or []) if not spec.is_board_map(a.get("values")) else []:
        if it["value"] == v or (isinstance(v, bool) and it["value"] == int(v)):
            name = it.get(ctx.lang) or it.get("en")
            if name:
                return f"{text}{ctx.paren(name)}"
    return text


def render_initial(ctx: Ctx, item: dict) -> str:
    spec, L = ctx.spec, ctx.L
    lines = []
    for a in spec.args(item):
        if a.get("use") == "motorID":
            continue
        texts = default_texts(ctx, a)
        if not texts:
            continue
        name = a.get("name", a.get("use", "?"))
        if len(set(texts.values())) == 1 and len(texts) == len(spec.board_names):
            body = next(iter(texts.values()))
        elif len(set(texts.values())) == 1 and len(texts) == 1:
            body = next(iter(texts.values()))
        else:
            body = ("; " if ctx.lang == "en" else "；").join(f"{b}: {t}" for b, t in texts.items())
        link = ""
        if "setting" in a:
            link = ctx.paren(f"[{a['setting']}]({_settings_href(ctx, a['setting'])})")
        lines.append(f"- `{name}`: {body}{link}")
    return "\n".join(lines)


def setting_anchor(key: str) -> str:
    return key.replace(".", "-").lower()


# ---------------------------------------------------------------------------
# reference block of a command / message

def render_tables(ctx: Ctx, item: dict, level: int = 5) -> list[str]:
    spec = ctx.spec
    out = []
    for t in item.get("tables", []) or []:
        title = ctx.tx(t.get("title"), "table") if t.get("title") else ""
        cols = [ctx.tx(c, "table") for c in t["columns"]]
        rows = t["rows"]
        variants = [(None, rows)] if isinstance(rows, list) else [(b, rows[b]) for b in spec.board_names if b in rows]
        for board, rws in variants:
            head = title + (f" - {board}" if board else "")
            body = table(cols, [[ctx.md(ctx.tx(c, "table")) if not isinstance(c, (int, float, bool)) else fmt(c) for c in r] for r in rws])
            out.append((f"{'#' * level} {head}\n\n" if head else "") + body)
    return out


def render_message_block(ctx: Ctx, addr: str) -> str:
    """Full reference of a message (own heading)."""
    spec, L = ctx.spec, ctx.L
    msg = spec.message(addr)
    ctx.where = f"message {addr}"
    ctx.block_anchor = anchor(addr)
    parts = [f"### `{addr}` {arg_heading(spec, msg)} {{#{anchor(addr)}}}".replace("  ", " ")]
    parts += _notes(ctx, msg)
    parts.append(f"#### {L['argument']}\n\n" + render_args(ctx, msg, in_message=True))
    if msg.get("description"):
        parts.append(f"#### {L['description']}\n\n" + ctx.md(ctx.tx(msg["description"], "description")))
    parts += render_tables(ctx, msg)
    ch = render_changes(ctx, msg)
    if ch:
        parts.append(ch)
    return "\n\n".join(parts) + "\n"


def _notes(ctx: Ctx, item: dict) -> list[str]:
    spec, L = ctx.spec, ctx.L
    notes = []
    boards = item.get("boards")
    if boards and set(boards) != set(spec.board_names):
        notes.append(L["only"].format(boards=boards_text(spec, board_sorted(spec, boards))))
    if item.get("since"):
        notes.append(L["added"].format(v=item["since"]))
    return [ctx.join(*notes)] if notes else []


def render_changes(ctx: Ctx, item: dict, level: int = 4) -> str:
    ch = item.get("changes")
    if not ch:
        return ""
    lines = []
    for c in ch:
        lines.append(f"- **v{c['version']}**: " + ctx.md(ctx.item_text(c, "change")).replace("\n", "\n  "))
    return f"{'#' * level} {ctx.L['changes']}\n\n" + "\n".join(lines)


def inline_notes(ctx: Ctx, item: dict) -> str:
    """`since` and `changes` of a value or a configuration item, on one line (for table cells and lists)."""
    parts = []
    if item.get("since"):
        parts.append(ctx.L["added"].format(v=item["since"]))
    for c in item.get("changes") or []:
        parts.append(f"**v{c['version']}**: " + ctx.oneline(ctx.md(ctx.item_text(c, "change"))))
    return ctx.join(*parts)


def render_command_block(ctx: Ctx, addr: str) -> str:
    spec, L = ctx.spec, ctx.L
    cmd = spec.command(addr)
    ctx.where = f"command {addr}"
    ctx.block_anchor = anchor(addr)
    parts = [f"### `{addr}` {arg_heading(spec, cmd)} {{#{anchor(addr)}}}".replace("  ", " ")]
    parts += _notes(ctx, cmd)
    parts.append(f"#### {L['argument']}\n\n" + render_args(ctx, cmd))
    timings = cmd["timing"] if isinstance(cmd["timing"], list) else [cmd["timing"]]
    parts.append(f"#### {L['timing']}\n\n" + ", ".join(ctx.tx(spec.timings[t], "timing") for t in timings))
    desc = ctx.tx(cmd.get("description"), "description")
    if desc.strip():
        parts.append(f"#### {L['description']}\n\n" + ctx.md(desc))
    ch = render_changes(ctx, cmd)
    if ch:
        parts.append(ch)
    resp = cmd.get("response") or []
    notif = cmd.get("notifies") or []
    if resp or notif:
        blocks = []
        for r in resp:
            maddr, when = (r, None) if isinstance(r, str) else (r["message"], r.get("when"))
            blocks.append(_render_response(ctx, maddr, when))
        for n in notif:
            blocks.append(_render_response(ctx, n, None))
        parts.append(f"#### {L['response']}\n\n" + "\n\n".join(blocks))
    errs = cmd.get("errors") or []
    if errs:
        parts.append(f"#### {L['errors']}\n\n" + "\n".join(_error_line(ctx, e) for e in errs))
    init = render_initial(ctx, cmd)
    if init:
        parts.append(f"#### {L['initial']}\n\n{init}")
    parts += render_tables(ctx, cmd)
    see = cmd.get("see_also") or []
    if see:
        links = []
        for s in see:
            href = ctx.link_to(s)
            links.append(f"[`{s}`]({href})" if href else f"`{s}`")
        parts.append(f"#### {L['see_also']}\n\n" + ", ".join(links))
    return "\n\n".join(parts) + "\n"


def _render_response(ctx: Ctx, maddr: str, when: Any) -> str:
    """A message in the response of a command. A standalone message: link, form, arguments. Any other message
    is described here in full (description, tables, changes one level below the message block)."""
    spec, L = ctx.spec, ctx.L
    msg = spec.message(maddr)
    head = ""
    if when:
        head = f"{L['when']}: {ctx.tx(when, 'when')}\n\n"
    standalone = maddr in standalone_messages(spec)
    href = ctx.link_to(maddr, prefer="message") if standalone else None
    code = f"```\n{maddr} {arg_heading(spec, msg)}\n```".replace("  ", " ")
    link = f"[`{maddr}`]({href})\n\n" if href else ""
    note = ctx.join(*_notes(ctx, msg))
    out = head + link + (note + "\n\n" if note else "") + code + "\n\n" + render_args(ctx, msg, in_message=True)
    if not standalone:
        where, ctx.where = ctx.where, f"message {maddr} (in the response of {where_name(ctx.where)})"
        extra = []
        if msg.get("description"):
            extra.append(f"##### {L['description']}\n\n" + ctx.md(ctx.tx(msg["description"], "description")))
        extra += render_tables(ctx, msg, level=5)
        ch = render_changes(ctx, msg, level=5)
        if ch:
            extra.append(ch)
        ctx.where = where
        if extra:
            out += "\n\n" + "\n\n".join(extra)
    return out


def where_name(where: str) -> str:
    return where.removeprefix("command ")


def _error_line(ctx: Ctx, name: str) -> str:
    msg = ctx.spec.message("/error/command")
    text = ""
    for v in msg["args"][0].get("values", []):
        if v["value"] == name:
            text = ctx.item_text(v, "error")
            notes = inline_notes(ctx, v)
            if notes:
                text = ctx.join(text, notes)
    return f"- `{name}`" + (f": {text}" if text else "")


# ---------------------------------------------------------------------------
# related lists

def first_sentence(text: str) -> str:
    text = " ".join(text.strip().split("\n\n")[0].split())
    m = re.search(r"(.+?[.。])(\s|$)", text)
    return (m.group(1) if m else text)[:200]


def render_related(ctx: Ctx, groups: list[str]) -> str:
    spec, L = ctx.spec, ctx.L
    for g in groups:
        if g not in spec.groups:
            raise GenerateError(f"unknown group '{g}'")
    rows = []
    for g in groups:
        for c in spec.commands:
            if c["group"] != g:
                continue
            href = ctx.link_to(c["address"])
            desc = first_sentence(ctx.tx(c.get("description"), "description"))
            desc = LINK_RE.sub(lambda m: f"`{m.group(1)}`", desc)
            rows.append([f"[`{c['address']}`]({href})", arg_heading(spec, c) or "-", desc])
    return f"**{L['related']}**\n\n" + table([L["command"], L["arguments"], L["description"]], rows) + "\n"


def render_related_settings(ctx: Ctx, sections: list[str]) -> str:
    spec, L = ctx.spec, ctx.L
    known = {s["section"] for s in spec.settings}
    for s in sections:
        if s not in known:
            raise GenerateError(f"unknown settings section '{s}'")
    rows = []
    for s in spec.settings:
        if s["section"] in sections:
            href = f"{_relpath(Path(SETTINGS_DIR) / f'{SETTINGS_PAGE}{SUFFIX[ctx.lang]}', ctx.rel_from)}#{setting_anchor(s['key'])}"
            rows.append([f"[`{s['key']}`]({href})", ctx.tx(s.get("label"), "label"),
                         ", ".join(f"`{c}`" for c in s.get("commands", []))])
    return f"**{L['related_settings']}**\n\n" + table([L["key"], L["label"], L["commands_col"]], rows) + "\n"


# ---------------------------------------------------------------------------
# marker expansion

def lang_of(path: Path) -> str:
    n = path.name
    if re.search(r"(_jp|\.ja|\.jp)\.md$", n):
        return "ja"
    if re.search(r"(_en|\.en)\.md$", n):
        return "en"
    if any(p in ("ja", "jp") for p in path.parts):
        return "ja"
    return "en"


def expand_text(text: str, ctx: Ctx, path: Path) -> str:
    spec = ctx.spec

    def repl(m: re.Match) -> str:
        kind, arg = m.group(1), m.group(2).strip()
        lineno = text.count("\n", 0, m.start()) + 1
        ctx.where = f"{path}:{lineno}"
        try:
            if kind == "osc":
                if spec.command(arg) is None:
                    raise GenerateError(f"{path}:{lineno}: unknown command address {arg}")
                body = render_command_block(ctx, arg)
            elif kind == "osc-message":
                if spec.message(arg) is None:
                    raise GenerateError(f"{path}:{lineno}: unknown message address {arg}")
                body = render_message_block(ctx, arg)
            elif kind == "osc-related":
                body = render_related(ctx, [x.strip() for x in arg.split(",") if x.strip()])
            else:
                body = render_related_settings(ctx, [x.strip() for x in arg.split(",") if x.strip()])
        except GenerateError as e:
            msg = str(e)
            ctx.errors.append(msg if msg.startswith(str(path)) else f"{path}:{lineno}: {msg}")
            return m.group(0)
        marker = f"<!-- {kind}: {arg} -->"
        return (f"{marker}\n<!-- generated:begin {kind} {arg} -->\n"
                f"{body.rstrip(chr(10))}\n<!-- generated:end {kind} {arg} -->\n")

    return MARKER_RE.sub(repl, text)


# ---------------------------------------------------------------------------
# generated pages

def front_matter_of(existing: str | None, title: str, lang: str) -> str:
    if existing and existing.startswith("---\n"):
        end = existing.find("\n---\n", 4)
        if end > 0:
            return existing[: end + 5]
    return f"---\ntitle: {title}\nlang: {lang}\n---\n"


def page_command_list(ctx: Ctx) -> str:
    spec, L = ctx.spec, ctx.L
    out = [f"# {L['list_title']}", "", GENERATED_NOTE[ctx.lang], "", L["list_intro"], ""]
    for gkey, g in spec.groups.items():
        cmds = [c for c in spec.commands if c["group"] == gkey]
        if not cmds:
            continue
        ctx.where = f"command list {gkey}"
        out += [f"## {ctx.tx(g, 'group')}", ""]
        rows = []
        for c in cmds:
            href = ctx.link_to(c["address"])
            marks = [("✓" if b in spec.boards_of(c) else "") for b in spec.board_names]
            rows.append([f"[`{c['address']}`]({href})", arg_heading(spec, c) or "-", *marks, c.get("since", "")])
        out += [table([L["command"], L["arguments"], *spec.board_names, L["since"]], rows), ""]
    return "\n".join(out)


def page_diff(ctx: Ctx) -> str:
    spec, L = ctx.spec, ctx.L
    boards = spec.board_names
    out = [f"# {L['diff_title']}", "", GENERATED_NOTE[ctx.lang], ""]

    def cmd_link(c: dict) -> str:
        return f"[`{c['address']}`]({ctx.link_to(c['address'])})"

    def msg_link(m: dict) -> str:
        return f"[`{m['address']}`]({ctx.link_to(m['address'], prefer='message')})"

    # 1. only on some boards
    for b in boards:
        only = [c for c in spec.commands if b in spec.boards_of(c) and set(spec.boards_of(c)) != set(boards)]
        out += [f"## {L['diff_only'].format(boards=b)}", ""]
        out += ["\n".join(f"- {cmd_link(c)} {arg_heading(spec, c)}".rstrip() + _routed_note(ctx, c) for c in only) or L["none_found"], ""]
        msgs = [m for m in spec.messages if m.get("boards") and b in m["boards"] and set(m["boards"]) != set(boards)]
        out += [f"## {L['diff_msg_only'].format(boards=b)}", ""]
        out += ["\n".join(f"- {msg_link(m)} {arg_heading(spec, m)}".rstrip() for m in msgs) or L["none_found"], ""]
    # 2. board-specific values of arguments
    rows = _board_value_rows(ctx, spec.commands, "command")
    out += [f"## {L['diff_values']}", ""]
    out += [table([L["command"], L["argument"], *boards], rows) if rows else L["none_found"], ""]
    rows = _board_value_rows(ctx, spec.messages, "message")
    out += [f"## {L['diff_msg_values']}", ""]
    out += [table([L["command"], L["argument"], *boards], rows) if rows else L["none_found"], ""]
    # 3. board-specific tables
    out += [f"## {L['diff_tables']}", ""]
    tbl = []
    for kind, items in (("command", spec.commands), ("message", spec.messages)):
        for it in items:
            for t in it.get("tables", []) or []:
                if isinstance(t["rows"], dict):
                    link = cmd_link(it) if kind == "command" else msg_link(it)
                    tbl.append([link, ctx.tx(t.get("title"), "table") if t.get("title") else ""])
    out += [table([L["command"], L["description"]], tbl) if tbl else L["none_found"], ""]
    # 4. settings
    for b in boards:
        only = [s for s in spec.settings if b in spec.boards_of(s) and set(spec.boards_of(s)) != set(boards)]
        out += [f"## {L['diff_set_only'].format(boards=b)}", ""]
        out += ["\n".join(f"- [`{s['key']}`]({_settings_href(ctx, s['key'])})" for s in only) or L["none_found"], ""]
    srows = []
    for s in spec.settings:
        vals = {}
        for field in ("default", "template", "range"):
            if field in s and spec.is_board_map(s[field]):
                vals[field] = s[field]
        if not vals:
            continue
        for field, v in vals.items():
            cells = []
            for b in boards:
                x = spec.for_board(v, b)
                cells.append("-" if x is None else (_rng(x) if field == "range" else ip_or_value(s["type"], x)))
            srows.append([f"[`{s['key']}`]({_settings_href(ctx, s['key'])})", field, *cells])
    out += [f"## {L['diff_settings']}", ""]
    out += [table([L["key"], L["description"], *boards], srows) if srows else L["none_found"], ""]
    return "\n".join(out)


def _routed_note(ctx: Ctx, c: dict) -> str:
    spec = ctx.spec
    extra = board_sorted(spec, set(c.get("routed_on") or []) - set(spec.boards_of(c)))
    if not extra:
        return ""
    on = ", ".join(extra)
    if ctx.lang == "ja":
        return f"（ファームウェアは{on}でも受け付けますが、意味のある値は得られません）"
    return f" (the firmware also accepts it on {on}, but the value is meaningless there)"


def _settings_href(ctx: Ctx, key: str) -> str:
    return f"{_relpath(Path(SETTINGS_DIR) / f'{SETTINGS_PAGE}{SUFFIX[ctx.lang]}', ctx.rel_from)}#{setting_anchor(key)}"


def _board_value_rows(ctx: Ctx, items: list[dict], kind: str) -> list[list[str]]:
    spec = ctx.spec
    boards = spec.board_names
    rows = []
    for it in items:
        if kind == "command" and set(spec.boards_of(it)) != set(boards):
            continue
        if kind == "message" and it.get("boards") and set(it["boards"]) != set(boards):
            continue
        for a in spec.args(it):
            if a.get("use") == "motorID":
                continue
            name = a.get("name", "?")
            link = f"[`{it['address']}`]({ctx.link_to(it['address'], prefer=kind)})"
            if "range" in a and spec.is_board_map(a["range"]):
                rows.append([link, f"{name}{ctx.paren(ctx.L['range'])}",
                             *[("-" if spec.for_board(a["range"], b) is None else _rng(spec.for_board(a["range"], b))) for b in boards]])
            if kind == "command":
                texts = default_texts(ctx, a) if ("setting" in a or "default" in a) else None
                if texts and len(set(texts.values())) > 1:
                    rows.append([link, f"{name}{ctx.paren(ctx.L['initial'])}", *[texts.get(b, "-") for b in boards]])
            if a.get("values") and spec.is_board_map(a["values"]):
                rows.append([link, f"{name}{ctx.paren(ctx.L['value'])}",
                             *[", ".join(f"{fmt(v['value'])}: {ctx.item_text(v, 'value')}" for v in a["values"].get(b, [])) or "-" for b in boards]])
    return rows


def page_settings(ctx: Ctx) -> str:
    spec, L = ctx.spec, ctx.L
    out = [f"# {L['settings_title']}", "", GENERATED_NOTE[ctx.lang], "", L["settings_intro"], ""]
    sections: dict[str, list[dict]] = {}
    for s in spec.settings:
        sections.setdefault(s["section"], []).append(s)
    for sec, items in sections.items():
        out += [f"## {sec} {{#{sec.lower()}}}", ""]
        rows = []
        for s in items:
            ctx.where = f"setting {s['key']}"
            key = s["key"].split(".", 1)[1]
            name = f"<a id=\"{setting_anchor(s['key'])}\"></a>`{key}`"
            label = ctx.tx(s.get("label"), "label")
            if s.get("per_motor"):
                label += ctx.paren(L['per_motor']) if label else L["per_motor"]
            only = s.get("boards")
            if only and set(only) != set(spec.board_names):
                label += ctx.paren(L['boards_only'].format(boards=boards_text(spec, board_sorted(spec, only))))
            init = _setting_initial(ctx, s)
            rng = range_text(ctx, {"range": s.get("range"), "unit": s.get("unit")}, True) if (s.get("range") or s.get("unit")) else ""
            cmds = ", ".join(f"[`{c}`]({ctx.link_to(c)})" for c in s.get("commands", []))
            desc = ctx.tx(s.get("description"), "description") if s.get("description") else ""
            desc = ctx.oneline(ctx.md(desc)) if desc else ""
            notes = inline_notes(ctx, s)
            if notes:
                desc = ctx.join(desc, notes)
            rows.append([name, label, s["type"], init, rng, cmds, desc])
        out += [table([L["key"], L["label"], L["type"], L["initial_col"], f"{L['range']} / {L['unit']}", L["commands_col"], L["description"]], rows), ""]
    return "\n".join(out)


def _setting_initial(ctx: Ctx, s: dict) -> str:
    spec, L = ctx.spec, ctx.L
    texts = {}
    for b in spec.board_names:
        if b not in spec.boards_of(s):
            continue
        d = spec.for_board(s["default"], b)
        if d is None:
            continue
        shown = _setting_value(ctx, s, d)
        if "template" in s and ctx.defaults != "firmware":
            t = spec.for_board(s["template"], b, missing=d)
            if t is not None and t != d:
                ts = _setting_value(ctx, s, t)
                shown = ts if ctx.defaults == "template" else (
                    f"{shown}{ctx.paren(L['firmware'])} / {ts}{ctx.paren(L['template'])}" if ctx.lang == "en"
                    else f"{shown}{ctx.paren(L['firmware'])}、{ts}{ctx.paren(L['template'])}")
        texts[b] = shown
    if not texts:
        return ""
    if len(set(texts.values())) == 1:
        return next(iter(texts.values()))
    return "; ".join(f"{b}: {t}" for b, t in texts.items())


def _setting_value(ctx: Ctx, s: dict, v: Any) -> str:
    spec = ctx.spec
    text = ip_or_value(s["type"], v)
    values = s.get("values")
    if values:
        # board-specific values: the caller does not know the board; look in every variant
        lists = list(values.values()) if spec.is_board_map(values) else [values]
        for lst in lists:
            for it in lst:
                if it["value"] == v and it.get("en"):
                    return f"{text}{ctx.paren(it.get(ctx.lang) or it['en'])}"
    return text


PAGES = (
    (REF_DIR, COMMAND_LIST_PAGE, "Command list", page_command_list),
    (REF_DIR, DIFF_PAGE, "Differences between STEP400 and STEP800", page_diff),
    (SETTINGS_DIR, SETTINGS_PAGE, "Configuration items", page_settings),
)


def generate_pages(docs: Path, spec: Spec, defaults: str, counter: Counter, errors: list[str]) -> dict[Path, str]:
    out: dict[Path, str] = {}
    for lang in LANGS:
        for directory, page, title, fn in PAGES:
            ctx = Ctx(spec, lang, defaults, counter, errors)
            ctx.page_dir = directory
            ctx.rel_from = Path(directory)
            name = JP_PAGE_NAMES.get(page, page) if lang == "ja" else page
            path = docs / lang / directory / f"{name}{SUFFIX[lang]}"
            existing = path.read_text(encoding="utf-8") if path.exists() else None
            ttl = {"en": title, "ja": LABELS["ja"]["list_title"] if page == COMMAND_LIST_PAGE else
                   LABELS["ja"]["diff_title"] if page == DIFF_PAGE else LABELS["ja"]["settings_title"]}[lang]
            body = fn(ctx).rstrip("\n") + "\n"
            out[path] = front_matter_of(existing, ttl, lang) + "\n" + body
    return out


def generate_markers(docs: Path, spec: Spec, defaults: str, counter: Counter, errors: list[str],
                     skip: set[Path]) -> dict[Path, str]:
    out: dict[Path, str] = {}
    for path in sorted(docs.rglob("*.md")):
        if path in skip:
            continue
        text = path.read_text(encoding="utf-8")
        if GENERATED_FILE_MARK in text or not MARKER_RE.search(text):
            continue
        lang = lang_of(path.relative_to(docs))
        ctx = Ctx(spec, lang, defaults, counter, errors)
        rel = path.relative_to(docs)
        ctx.rel_from = Path(*rel.parts[1:-1]) if rel.parts[0] in LANGS else rel.parent
        new = expand_text(text, ctx, rel)
        if new != text:
            out[path] = new
    return out


def run(docs: Path, spec: Spec, defaults: str = "both", check: bool = False,
        coverage: bool = False, out=sys.stdout) -> int:
    counter: Counter = Counter()
    errors: list[str] = []
    pages = generate_pages(docs, spec, defaults, counter, errors)
    marked = generate_markers(docs, spec, defaults, counter, errors, set(pages))
    if coverage:
        errors += check_coverage(docs, spec)
    if errors:
        for e in dict.fromkeys(errors):
            print(f"ERROR   {e}", file=out)
        print("nothing written", file=out)
        return 1
    changed = []
    for path, text in {**pages, **marked}.items():
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old != text:
            changed.append(path)
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
    ja_missing = sum(counter.values())
    print(f"generated pages: {len(pages)}, pages with markers expanded: {len(marked)}, "
          f"{'would change' if check else 'changed'}: {len(changed)}", file=out)
    for p in changed:
        print(f"  {p.relative_to(docs)}", file=out)
    print(f"Japanese texts filled with English: {ja_missing} "
          f"({', '.join(f'{k} {v}' for k, v in sorted(counter.items())) or 'none'})", file=out)
    if not coverage:
        for line in marker_summary(docs, spec):
            print(line, file=out)
    return 1 if (check and changed) else 0


def standalone_messages(spec: Spec) -> list[str]:
    """Messages described on their own in the page of the messages (decided from the YAML only):
    the ones that no command lists in `response` / `notifies`, STANDALONE_MESSAGES, and the ones that
    some command lists in `notifies`. The other messages are shown in the `response` of the commands."""
    listed: set[str] = set()
    notified: set[str] = set()
    for c in spec.commands:
        listed.update(Spec.response_messages(c))
        for n in c.get("notifies", []) or []:
            notified.add(n if isinstance(n, str) else n["message"])
    listed |= notified
    return [m["address"] for m in spec.messages
            if m["address"] not in listed or m["address"] in STANDALONE_MESSAGES or m["address"] in notified]


def response_owner(spec: Spec, address: str) -> dict | None:
    """The first command (YAML order) that lists the message in `response`."""
    return next((c for c in spec.commands if address in Spec.response_messages(c)), None)


def scan_markers(docs: Path, kind: str, lang: str) -> dict[str, list[str]]:
    """{address: [file stem, ...]} of the `kind` markers in docs/<lang>/ (the pages of other directories are not counted)."""
    found: dict[str, list[str]] = {}
    base = docs / lang
    for path in sorted(base.rglob("*.md")) if base.is_dir() else []:
        for m in MARKER_RE.finditer(path.read_text(encoding="utf-8")):
            if m.group(1) == kind:
                found.setdefault(m.group(2).strip(), []).append(path.stem)
    return found


def marker_report(docs: Path, spec: Spec) -> dict[str, dict]:
    """Per language: the problems of the markers and the counts.

    commands: each has `<!-- osc: /address -->` once, in the page of its group.
    messages: each of standalone_messages() has `<!-- osc-message: /address -->` once, in the page of the messages;
    any other message must not have one (it is shown in the response of its commands).
    Unknown addresses are errors of the expansion, not counted here.
    """
    report = {}
    for lang in LANGS:
        errors: list[str] = []
        counts = {"commands_ok": 0, "commands": len(spec.commands), "messages_ok": 0, "misplaced": 0, "duplicated": 0}
        required = standalone_messages(spec)
        counts["messages"] = len(required)
        found_cmd = scan_markers(docs, "osc", lang)
        found_msg = scan_markers(docs, "osc-message", lang)

        def judge(address: str, names: list[str], page: str, key: str) -> bool:
            expected = JP_PAGE_NAMES.get(page, page) if lang == "ja" else page
            if not names:
                errors.append(f"[{lang}] {address}: marker found 0 times (expected once in {page})")
                return False
            if len(names) > 1:
                counts["duplicated"] += 1
                errors.append(f"[{lang}] {address}: marker found {len(names)} times (expected once in {page})")
                return False
            if names[0] != expected:
                counts["misplaced"] += 1
                errors.append(f"[{lang}] {address}: marker in {names[0]}, expected {key} ({page})")
                return False
            return True

        for c in spec.commands:
            page = spec.groups[c["group"]]["page"]
            if judge(c["address"], found_cmd.get(c["address"], []), page, f"the page of group '{c['group']}'"):
                counts["commands_ok"] += 1
        for address in required:
            if judge(address, found_msg.get(address, []), MESSAGES_PAGE, "the page of the messages"):
                counts["messages_ok"] += 1
        for address, names in found_msg.items():
            if address not in required and spec.message(address) is not None:
                errors.append(f"[{lang}] {address}: marker not allowed (not a standalone message; "
                              "it is shown in the response of its commands)")
        report[lang] = {"errors": errors, **counts}
    return report


def check_coverage(docs: Path, spec: Spec) -> list[str]:
    """The markers of the commands and of the standalone messages, as errors (both languages, docs/en and docs/ja only)."""
    return [e for r in marker_report(docs, spec).values() for e in r["errors"]]


def marker_summary(docs: Path, spec: Spec) -> list[str]:
    """One WARNING line per language with the counts (the usual run; it never changes the exit code)."""
    return [f"WARNING [{lang}] markers: commands {r['commands_ok']}/{r['commands']}, "
            f"messages {r['messages_ok']}/{r['messages']} required; {r['misplaced']} misplaced, "
            f"{r['duplicated']} duplicated (run with --coverage for the list)"
            for lang, r in marker_report(docs, spec).items()]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", default=str(SPEC_PATH))
    ap.add_argument("--docs", default=str(REPO_ROOT / "docs"))
    ap.add_argument("--defaults", choices=["firmware", "template", "both"], default="both",
                    help="initial values to show (default: both)")
    ap.add_argument("--check", action="store_true", help="write nothing; exit 1 if a file would change")
    ap.add_argument("--coverage", action="store_true",
                    help="also require the markers: every command once in the page of its group, the standalone messages "
                         "(see standalone_messages) once in the page of the messages, no marker for any other message; "
                         "list each problem as an error")
    args = ap.parse_args(argv)
    spec = Spec.load(args.spec)
    return run(Path(args.docs), spec, args.defaults, args.check, args.coverage)


if __name__ == "__main__":
    sys.exit(main())
