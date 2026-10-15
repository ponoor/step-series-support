"""Shared helpers for spec/osc-commands.yaml.

Used by validate_spec.py, check_firmware.py and (later) generate.py.

    from spec import Spec
    spec = Spec.load()                       # spec/osc-commands.yaml
    for cmd in spec.commands_for("STEP800"):
        for arg in spec.args(cmd):           # `use:` expanded
            rng = spec.for_board(arg.get("range"), "STEP800")
"""

from __future__ import annotations

import copy
import re
from pathlib import Path
from typing import Any, Iterator

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = REPO_ROOT / "spec" / "osc-commands.yaml"
SCHEMA_PATH = REPO_ROOT / "spec" / "osc-commands.schema.json"

# `[[/address]]` in a description links to a command or message.
LINK_RE = re.compile(r"\[\[(/[^\]\s]+)\]\]")


class Spec:
    def __init__(self, data: dict, path: Path | None = None):
        self.data = data
        self.path = path
        self.boards: dict = data.get("boards", {})
        self.params: dict = data.get("params", {})
        self.timings: dict = data.get("timings", {})
        self.groups: dict = data.get("groups", {})
        self.commands: list = data.get("commands", [])
        self.messages: list = data.get("messages", [])
        self.settings: list = data.get("settings", [])

    @classmethod
    def load(cls, path: str | Path = SPEC_PATH) -> "Spec":
        path = Path(path)
        with path.open(encoding="utf-8") as f:
            return cls(yaml.safe_load(f), path)

    # ------------------------------------------------------------------
    # Board-specific values

    @property
    def board_names(self) -> list[str]:
        return list(self.boards)

    def is_board_map(self, value: Any) -> bool:
        """True if `value` is {STEP400: ..., STEP800: ...} (keys look like board names)."""
        return (
            isinstance(value, dict)
            and len(value) > 0
            and all(isinstance(k, str) and re.fullmatch(r"STEP[0-9]+", k) for k in value)
        )

    def for_board(self, value: Any, board: str, missing: Any = None) -> Any:
        """The value for `board`. A plain value applies to every board.

        For a board map without `board`, returns `missing`.
        """
        if self.is_board_map(value):
            return value.get(board, missing)
        return value

    def per_board(self, value: Any) -> dict[str, Any]:
        """{board: value} for every board (None where a board map has no entry)."""
        return {b: self.for_board(value, b) for b in self.board_names}

    # ------------------------------------------------------------------
    # Lookups

    def command(self, address: str) -> dict | None:
        return next((c for c in self.commands if c["address"] == address), None)

    def message(self, address: str) -> dict | None:
        return next((m for m in self.messages if m["address"] == address), None)

    def setting(self, key: str) -> dict | None:
        """The setting whose key (or one of its aliases) is `key`."""
        for s in self.settings:
            if s["key"] == key or key in s.get("aliases", []):
                return s
        return None

    # ------------------------------------------------------------------
    # Boards of a command / message / setting

    def boards_of(self, item: dict) -> list[str]:
        """Boards on which the item is documented as usable (`boards`, else all)."""
        return list(item.get("boards") or self.board_names)

    def routed_on(self, item: dict) -> list[str]:
        """Boards on which the firmware accepts the command (`routed_on`, else `boards`, else all)."""
        return list(item.get("routed_on") or item.get("boards") or self.board_names)

    def commands_for(self, board: str) -> list[dict]:
        return [c for c in self.commands if board in self.boards_of(c)]

    def settings_for(self, board: str) -> list[dict]:
        return [s for s in self.settings if board in self.boards_of(s)]

    # ------------------------------------------------------------------
    # Arguments

    def expand_arg(self, arg: dict) -> dict:
        """Apply `use:`. Fields written on the argument override the shared definition."""
        if "use" not in arg:
            return copy.deepcopy(arg)
        key = arg["use"]
        if key not in self.params:
            raise KeyError(f"params has no '{key}'")
        out = copy.deepcopy(self.params[key])
        out.setdefault("name", key)
        for k, v in arg.items():
            if k != "use":
                out[k] = copy.deepcopy(v)
        out["use"] = key
        return out

    def args(self, item: dict) -> list[dict]:
        return [self.expand_arg(a) for a in item.get("args", [])]

    def arg_default(self, arg: dict, board: str) -> Any:
        """Initial value of an (expanded) argument: from its setting, else `default`."""
        if "setting" in arg:
            s = self.setting(arg["setting"])
            return None if s is None else self.for_board(s.get("default"), board)
        return self.for_board(arg.get("default"), board)

    # ------------------------------------------------------------------
    # Responses

    @staticmethod
    def response_messages(cmd: dict) -> list[str]:
        """Addresses in `response` (plain strings or {message, when})."""
        out = []
        for r in cmd.get("response", []):
            out.append(r if isinstance(r, str) else r["message"])
        return out

    # ------------------------------------------------------------------
    # Texts

    def iter_texts(self) -> Iterator[tuple[str, str, str]]:
        """Yield (where, language, text) for every localized text in the spec."""

        def walk(node: Any, where: str):
            if isinstance(node, dict):
                # {en, ja} texts, and en/ja next to other fields (values, changes)
                for lang in ("en", "ja"):
                    if isinstance(node.get(lang), str):
                        yield where, lang, node[lang]
                for k, v in node.items():
                    if k not in ("en", "ja"):
                        yield from walk(v, f"{where}.{k}" if where else str(k))
            elif isinstance(node, list):
                for i, v in enumerate(node):
                    label = v.get("address") or v.get("key") or v.get("name") if isinstance(v, dict) else None
                    yield from walk(v, f"{where}[{label if label else i}]")

        yield from walk(self.data, "")

    @staticmethod
    def links(text: str) -> list[str]:
        return LINK_RE.findall(text)


def anchor(address: str) -> str:
    """Heading anchor made from the address only (`/combine/run` -> `combine-run`)."""
    return address.strip("/").replace("/", "-").lower()
