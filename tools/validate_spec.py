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
Warnings (not failures): empty texts (missing Japanese etc.), messages without description.
Exit code 1 if any check fails.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec import SCHEMA_PATH, SPEC_PATH, Spec  # noqa: E402


class Report:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)


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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=str(SPEC_PATH))
    ap.add_argument("-q", "--quiet", action="store_true", help="print warning counts only")
    args = ap.parse_args()

    spec = Spec.load(args.path)
    rep = Report()
    check_schema(spec, rep)
    if not rep.errors:
        check_board_keys(spec, rep)
        check_references(spec, rep)
    check_warnings(spec, rep)

    for e in rep.errors:
        print(f"ERROR   {e}")
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
