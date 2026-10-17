#!/usr/bin/env python3
"""Record the public classes of stepseries.commands and stepseries.responses as JSON.

    python tools/snapshot_python_api.py <path to python-step-series> <out.json>

For every dataclass of the two modules: base classes, and per field the name, type, default and
whether it is an init argument. The library's compatibility test compares the live modules with
a snapshot of an older release (tests/compat/api_v1.0.0.json), so names, the order of fields and
defaults never change by accident.
"""

from __future__ import annotations

import dataclasses
import json
import re
import sys
from pathlib import Path


def type_name(t) -> str:
    """A name for the type that does not depend on the Python version (`X | None` is `Optional[X]`)."""
    if isinstance(t, str):
        name = t
    elif isinstance(t, type):
        name = t.__name__
    else:
        name = str(t)
    name = name.replace("typing.", "").replace("NoneType", "None")
    m = re.fullmatch(r"(.*) \| None", name) or re.fullmatch(r"Union\[(.*), None\]", name)
    return f"Optional[{m.group(1)}]" if m else name


def default_of(f: dataclasses.Field) -> str:
    if f.default is not dataclasses.MISSING:
        return repr(f.default)
    if f.default_factory is not dataclasses.MISSING:
        return "<factory>"
    return "<required>"


def snapshot(lib: Path) -> dict:
    sys.path.insert(0, str(lib / "src"))
    from stepseries import commands, responses  # noqa: E402

    out: dict = {}
    for mod in (commands, responses):
        entries = {}
        for name, cls in vars(mod).items():
            if isinstance(cls, type) and dataclasses.is_dataclass(cls) and cls.__module__ == mod.__name__:
                entries[name] = {
                    "bases": [b.__name__ for b in cls.__bases__],
                    "fields": [
                        {"name": f.name, "type": type_name(f.type), "default": default_of(f), "init": f.init}
                        for f in dataclasses.fields(cls)
                    ],
                }
        out[mod.__name__.split(".")[-1]] = entries
    return out


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    data = snapshot(Path(sys.argv[1]).resolve())
    Path(sys.argv[2]).write_text(json.dumps(data, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print({k: len(v) for k, v in data.items()})
    return 0


if __name__ == "__main__":
    sys.exit(main())
