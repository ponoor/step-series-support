#!/usr/bin/env python3
"""Compare spec/osc-commands.yaml with the firmware source.

    python tools/check_firmware.py --firmware <step-series-unified-firmware> --ref v2.1.0
    python tools/check_firmware.py --firmware ... --ref v2.1.0 --templates configGenerator

Files are read with `git -C <firmware> show <ref>:<file>`, so the working tree and
the checked-out branch of the firmware repository do not matter.

Checks
  - OSC addresses: `OSC_ROUTE("/addr", handler)` in src/oscRoutes.h if the ref has it,
    otherwise `msgIN.route("/addr", handler)` in src/oscListeners.cpp. #ifdef / #if /
    #elif / #else / #endif are evaluated per board with the macros of the board's block
    in src/boardsDef.h (STEP400 -> STEP400_R1, STEP800 -> STEP800_R1).
    Reported: addresses missing in the YAML, addresses missing in the firmware, and
    board differences (compared with `routed_on`, else `boards`, else all boards).
  - Sent messages: addresses sent by src/*.cpp (OSCMessage / OscWriter constructors and send*()
    helpers) compared with the YAML `messages`.
  - Settings: keys read by src/loadConfig.cpp and their built-in defaults (`| value`),
    compared with `settings` (key or aliases, boards, default). Lines whose default
    cannot be evaluated are listed as "not checked" and do not count as mismatches.
  - Templates (--templates): keys and values of configTemplate_*.json compared with
    `settings` (`template`, else `default`). Template keys the firmware does not read,
    and settings missing from a template, are listed as notes; value differences count
    as mismatches.
Exit code 1 if any mismatch is found.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec import Spec  # noqa: E402

BOARD_MACROS = {"STEP400": "STEP400_R1", "STEP800": "STEP800_R1"}

# Constants used as defaults in loadConfig.cpp (driver library headers)
KNOWN_CONSTANTS = {
    "true": True, "false": False,
    "FWD": 1, "REV": 0,
    "STEP_SEL_1": 0, "STEP_SEL_1_2": 1, "STEP_SEL_1_4": 2, "STEP_SEL_1_8": 3,
    "STEP_SEL_1_16": 4, "STEP_SEL_1_32": 5, "STEP_SEL_1_64": 6, "STEP_SEL_1_128": 7,
    "STEP_FS": 0, "STEP_FS_2": 1, "STEP_FS_4": 2, "STEP_FS_8": 3,
    "STEP_FS_16": 4, "STEP_FS_32": 5, "STEP_FS_64": 6, "STEP_FS_128": 7,
}


# ---------------------------------------------------------------------------
# git

class Firmware:
    def __init__(self, path: str, ref: str):
        self.path = path
        self.ref = ref

    def read(self, file: str) -> str | None:
        r = subprocess.run(
            ["git", "-C", self.path, "show", f"{self.ref}:{file}"],
            capture_output=True, text=True,
        )
        return r.stdout if r.returncode == 0 else None

    def list_src(self) -> list[str]:
        r = subprocess.run(
            ["git", "-C", self.path, "ls-tree", "--name-only", self.ref, "src/"],
            capture_output=True, text=True, check=True,
        )
        return [l for l in r.stdout.splitlines() if l.endswith((".cpp", ".h"))]


# ---------------------------------------------------------------------------
# preprocessor

def strip_comments(src: str) -> str:
    """Remove comments and join lines continued with a backslash (line numbers are kept)."""
    src = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), src, flags=re.S)
    src = re.sub(r"//[^\n]*", "", src)
    out: list[str] = []
    pending: list[str] = []
    for line in src.split("\n"):
        if line.rstrip().endswith("\\"):
            pending.append(line.rstrip()[:-1])
            continue
        out.append(" ".join(pending + [line]))
        out.extend([""] * len(pending))  # keep the line count
        pending = []
    out.extend(pending)
    return "\n".join(out)


def board_macros(boards_def: str, product_macro: str) -> set[str]:
    """Macros defined in the `#ifdef PRODUCT` / `#elif defined(PRODUCT)` block of boardsDef.h.

    Only a block whose condition is the product macro alone is used (not, for example,
    `#if !defined(STEP400_R1) && !defined(STEP800_R1)` that picks a default board).
    """
    macros = {product_macro}
    inside = False
    depth = 0
    block_start = re.compile(
        rf"#\s*(?:ifdef\s+{product_macro}|(?:el)?if\s+defined\s*\(?\s*{product_macro}\s*\)?)\s*$"
    )
    for line in strip_comments(boards_def).splitlines():
        s = line.strip()
        m = re.match(r"#\s*(ifdef|ifndef|if|elif|else|endif)\b(.*)", s)
        if m:
            kw, rest = m.group(1), m.group(2)
            if inside:
                if kw in ("ifdef", "ifndef", "if"):
                    depth += 1
                elif kw == "endif":
                    if depth == 0:
                        break
                    depth -= 1
                elif kw in ("elif", "else") and depth == 0:
                    break
                continue
            if block_start.match(s):
                inside = True
                depth = 0
            continue
        if inside and depth == 0:
            d = re.match(r"#\s*define\s+(\w+)", s)
            if d:
                macros.add(d.group(1))
    return macros


def eval_condition(expr: str, defined: set[str]) -> bool:
    """Evaluate an #if expression: defined(X), defined X, ||, &&, !, parentheses.
    Other identifiers count as 0 (as in the C preprocessor); numbers and comparisons are kept."""
    e = re.sub(r"defined\s*\(\s*(\w+)\s*\)", lambda m: " 1 " if m.group(1) in defined else " 0 ", expr)
    e = re.sub(r"defined\s+(\w+)", lambda m: " 1 " if m.group(1) in defined else " 0 ", e)
    e = e.replace("||", " or ").replace("&&", " and ")
    e = re.sub(r"!(?!=)", " not ", e)
    e = re.sub(r"\b(?!and\b|or\b|not\b)[A-Za-z_]\w*\b", " 0 ", e)
    try:
        return bool(eval(e, {"__builtins__": {}}, {}))
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"cannot evaluate #if expression: {expr!r}") from exc


def active_lines(src: str, defined: set[str]) -> list[tuple[int, str]]:
    """(line number, text) of the lines that are compiled with `defined` macros."""
    out = []
    # stack of (this branch active, some branch already taken, parent active)
    stack: list[list[bool]] = []
    active = True
    for no, line in enumerate(strip_comments(src).splitlines(), 1):
        s = line.strip()
        m = re.match(r"#\s*(ifdef|ifndef|if|elif|else|endif)\b(.*)", s)
        if m:
            kw, rest = m.group(1), m.group(2).strip()
            if kw in ("ifdef", "ifndef", "if"):
                if kw == "ifdef":
                    cond = rest.split()[0] in defined
                elif kw == "ifndef":
                    cond = rest.split()[0] not in defined
                else:
                    cond = eval_condition(rest, defined)
                stack.append([cond, cond, active])
                active = active and cond
            elif kw == "elif":
                top = stack[-1]
                cond = (not top[1]) and eval_condition(rest, defined)
                top[0] = cond
                top[1] = top[1] or cond
                active = top[2] and cond
            elif kw == "else":
                top = stack[-1]
                cond = not top[1]
                top[0] = cond
                top[1] = True
                active = top[2] and cond
            elif kw == "endif":
                top = stack.pop()
                active = top[2]
            continue
        if active:
            out.append((no, line))
    return out


# ---------------------------------------------------------------------------
# extraction

ROUTE_RE = {
    "oscRoutes.h": re.compile(r'OSC_ROUTE\s*\(\s*"(/[^"]*)"'),
    "oscListeners.cpp": re.compile(r'msgIN\.route\s*\(\s*"(/[^"]*)"'),
}
SEND_RE = re.compile(
    r'(?:(?:OSCMessage|OscWriter)\s+\w+\s*\(\s*|send\w*\s*\(\s*(?:F\(\s*)?)"(/[^"]+)"'
)


def routes(fw: Firmware, defined: set[str]) -> tuple[str, set[str]]:
    for name in ("oscRoutes.h", "oscListeners.cpp"):
        src = fw.read(f"src/{name}")
        if src is None:
            continue
        found = set()
        for _, line in active_lines(src, defined):
            found.update(ROUTE_RE[name].findall(line))
        if found or name == "oscListeners.cpp":
            return name, found
    raise SystemExit("no route table found")


def sent_messages(fw: Firmware, defined: set[str]) -> set[str]:
    found = set()
    for file in fw.list_src():
        src = fw.read(file)
        if src is None:
            continue
        for _, line in active_lines(src, defined):
            found.update(SEND_RE.findall(line))
    return found


def parse_literal(text: str, globals_src: str):
    """A default value written after `|` in loadConfig.cpp. None if it cannot be evaluated."""
    t = text.strip()
    if t in KNOWN_CONSTANTS:
        return KNOWN_CONSTANTS[t]
    if re.fullmatch(r'"[^"]*"', t):
        return t[1:-1]
    if re.fullmatch(r"0[xX][0-9a-fA-F]+", t):
        return int(t, 16)
    if re.fullmatch(r"-?\d+", t):
        return int(t)
    if re.fullmatch(r"-?\d+\.\d*|-?\.\d+", t):
        return float(t)
    m = re.fullmatch(r"(\w+)\[i\]", t)
    if m:  # an array initialized in globals.cpp: IPAddress name(a, b, c, d) or name[] = {...}
        name = m.group(1)
        g = re.search(rf"\b{name}\s*\(([^)]*)\)", globals_src) or re.search(rf"\b{name}\s*\[\s*\]\s*=\s*\{{([^}}]*)\}}", globals_src)
        if g:
            items = [parse_literal(x, "") for x in g.group(1).split(",")]
            if all(isinstance(x, int) for x in items):
                return items
    return None


def config_keys(fw: Firmware, defined: set[str]):
    """Keys read by loadConfig.cpp -> (keys {key: default}, aliases {alias: key}, not_checked [lines])."""
    src = fw.read("src/loadConfig.cpp") or ""
    globals_src = fw.read("src/globals.cpp") or ""
    objects: dict[str, str] = {}   # C++ variable -> JSON section
    arrays: dict[str, str] = {}    # C++ variable -> JSON key
    keys: dict[str, object] = {}
    aliases: dict[str, str] = {}
    not_checked: list[str] = []
    for no, line in active_lines(src, defined):
        s = line.strip()
        m = re.match(r'JsonObject\s+(\w+)\s*=\s*doc\["(\w+)"\]', s)
        if m:
            objects[m.group(1)] = m.group(2)
            continue
        m = re.match(r'JsonArray\s+(\w+)\s*=\s*(\w+)\["(\w+)"\]', s)
        if m and m.group(2) in objects:
            arrays[m.group(1)] = f"{objects[m.group(2)]}.{m.group(3)}"
            continue
        m = re.match(r'(\w+)\s*=\s*(\w+)\["(\w+)"\]\s*;', s)
        if m and m.group(1) in arrays and m.group(2) in objects:
            aliases[f"{objects[m.group(2)]}.{m.group(3)}"] = arrays[m.group(1)]
            continue
        # scalar: x = section["key"] | default;  or  section["key"][i] | default
        for obj, key, idx, default in re.findall(r'\b(\w+)\["(\w+)"\](\[i\])?\s*\|\s*([^;)]+)', s):
            if obj not in objects:
                continue
            k = f"{objects[obj]}.{key}"
            val = parse_literal(default, globals_src)
            if val is None:
                not_checked.append(f"loadConfig.cpp:{no}: {s}")
                keys.setdefault(k, None)
            else:
                keys[k] = [val, val] if idx and k == "information.configVersion" else val
        # per motor / per element: x[i] = array[i] | default
        for arr, default in re.findall(r'\b(\w+)\[i\]\s*\|\s*([^;)]+)', s):
            if arr not in arrays:
                continue
            k = arrays[arr]
            val = parse_literal(default, globals_src)
            if val is None:
                not_checked.append(f"loadConfig.cpp:{no}: {s}")
                keys.setdefault(k, None)
            else:
                keys[k] = val
    # arrays that were declared but never read with `|`
    for k in arrays.values():
        if k not in keys:
            not_checked.append(f"loadConfig.cpp: {k}: read without a `|` default")
            keys[k] = None
    return keys, aliases, not_checked


# ---------------------------------------------------------------------------
# comparison helpers

def same(a, b) -> bool:
    if isinstance(a, bool) or isinstance(b, bool):
        return bool(a) == bool(b) and type(a) is type(b)
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(float(a) - float(b)) < 1e-9
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def scalar_of_template(value, per_motor: bool):
    """Collapse a per-motor array of a template into one value (None if the motors differ)."""
    if per_motor and isinstance(value, list):
        if all(same(v, value[0]) for v in value):
            return value[0]
        return ("per-motor values differ", value)
    return value


# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--firmware", required=True, help="path to the step-series-unified-firmware repository")
    ap.add_argument("--ref", required=True, help="git ref (tag or branch) to read")
    ap.add_argument("--spec", default=None, help="spec YAML (default: spec/osc-commands.yaml)")
    ap.add_argument("--templates", default=None, help="directory with configTemplate_*.json")
    args = ap.parse_args()

    spec = Spec.load(args.spec) if args.spec else Spec.load()
    fw = Firmware(args.firmware, args.ref)
    boards_def = fw.read("src/boardsDef.h")
    if boards_def is None:
        raise SystemExit(f"cannot read src/boardsDef.h at {args.ref}")

    mismatches: list[str] = []
    notes: list[str] = []
    print(f"firmware: {args.firmware} @ {args.ref}")

    board_defs = {b: board_macros(boards_def, macro) for b, macro in BOARD_MACROS.items() if b in spec.boards}

    # --- addresses -------------------------------------------------------
    fw_routes: dict[str, set[str]] = {}
    for b, defined in board_defs.items():
        source, found = routes(fw, defined)
        fw_routes[b] = found
    print(f"route table: src/{source}")
    all_fw = set().union(*fw_routes.values())
    yaml_cmds = {c["address"]: c for c in spec.commands}
    print(f"addresses: firmware {len(all_fw)} ("
          + ", ".join(f"{b} {len(v)}" for b, v in fw_routes.items())
          + f"), YAML {len(yaml_cmds)}")

    for a in sorted(all_fw - set(yaml_cmds)):
        on = [b for b in fw_routes if a in fw_routes[b]]
        mismatches.append(f"address not in YAML: {a} (routed on {', '.join(on)})")
    for a in sorted(set(yaml_cmds) - all_fw):
        mismatches.append(f"address not in firmware: {a}")
    for a in sorted(set(yaml_cmds) & all_fw):
        c = yaml_cmds[a]
        expected = set(spec.routed_on(c))
        actual = {b for b in fw_routes if a in fw_routes[b]}
        if expected != actual:
            field = "routed_on" if c.get("routed_on") else ("boards" if c.get("boards") else "all boards")
            mismatches.append(f"boards differ: {a}: YAML {field} {sorted(expected)}, firmware {sorted(actual)}")

    # --- messages --------------------------------------------------------
    fw_msgs: dict[str, set[str]] = {b: sent_messages(fw, d) for b, d in board_defs.items()}
    all_msgs = set().union(*fw_msgs.values())
    yaml_msgs = {m["address"] for m in spec.messages}
    print(f"sent messages: firmware {len(all_msgs)}, YAML {len(yaml_msgs)}")
    for a in sorted(all_msgs - yaml_msgs):
        mismatches.append(f"sent message not in YAML: {a}")
    for a in sorted(yaml_msgs - all_msgs):
        mismatches.append(f"message not sent by firmware: {a}")

    # --- settings --------------------------------------------------------
    fw_settings = {}
    for b, defined in board_defs.items():
        keys, aliases, not_checked = config_keys(fw, defined)
        fw_settings[b] = (keys, aliases)
        for line in not_checked:
            if line not in notes:
                notes.append(f"setting not checked ({b}): {line}")
    for b, (keys, aliases) in fw_settings.items():
        yaml_for_board = {s["key"]: s for s in spec.settings_for(b)}
        known = set(yaml_for_board) | {a for s in yaml_for_board.values() for a in s.get("aliases", [])}
        for k in sorted(set(keys) - known):
            mismatches.append(f"setting not in YAML ({b}): {k}")
        for k in sorted(set(yaml_for_board) - set(keys)):
            mismatches.append(f"setting not read by firmware ({b}): {k}")
        for alias, key in aliases.items():
            s = yaml_for_board.get(key)
            if s is not None and alias not in s.get("aliases", []):
                mismatches.append(f"alias not in YAML ({b}): {alias} -> {key}")
        for k, fw_default in keys.items():
            s = yaml_for_board.get(k)
            if s is None or fw_default is None:
                continue
            yd = spec.for_board(s["default"], b)
            if not same(yd, fw_default):
                mismatches.append(f"default differs ({b}): {k}: YAML {yd!r}, firmware {fw_default!r}")
    print(f"settings: firmware {', '.join(f'{b} {len(v[0])}' for b, v in fw_settings.items())}, YAML {len(spec.settings)}")

    # --- templates -------------------------------------------------------
    if args.templates:
        tdir = Path(args.templates)
        for b in spec.board_names:
            path = tdir / f"configTemplate_{b.lower()}.json"
            if not path.exists():
                notes.append(f"template not found: {path}")
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            flat = {f"{sec}.{k}": v for sec, items in data.items() for k, v in items.items()}
            yaml_for_board = {s["key"]: s for s in spec.settings_for(b)}
            by_name = {}
            for s in yaml_for_board.values():
                by_name[s["key"]] = s
                for a in s.get("aliases", []):
                    by_name[a] = s
            used = set()
            for k, v in flat.items():
                s = by_name.get(k)
                if s is None:
                    notes.append(f"template key not read by firmware ({path.name}): {k}")
                    continue
                if k != s["key"]:
                    notes.append(f"template uses the alias ({path.name}): {k} (key {s['key']})")
                used.add(s["key"])
                expected = spec.for_board(s.get("template"), b) if "template" in s else None
                if expected is None:
                    expected = spec.for_board(s["default"], b)
                actual = scalar_of_template(v, bool(s.get("per_motor")))
                if isinstance(actual, tuple):
                    mismatches.append(f"template ({path.name}): {k}: {actual[0]}: {actual[1]}")
                elif not same(expected, actual):
                    mismatches.append(f"template value differs ({path.name}): {k}: YAML {expected!r}, template {actual!r}")
            for k in sorted(set(yaml_for_board) - used):
                notes.append(f"setting missing from template ({path.name}): {k}")

    # --- report ----------------------------------------------------------
    print()
    if notes:
        print(f"notes ({len(notes)}):")
        for n in notes:
            print(f"  - {n}")
        print()
    print(f"mismatches ({len(mismatches)}):")
    for m in mismatches:
        print(f"  - {m}")
    if not mismatches:
        print("  none")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
