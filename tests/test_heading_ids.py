"""Every `##` and `###` heading of the pages in docs/en and docs/ja has an id `{#id}` that is the same in both languages.

A link to a page must not depend on the language, and the automatic id of MkDocs is made from the title (so it is
not the same in Japanese). The pages are read as they are in the repository: the generated blocks and the generated
pages are already expanded in the files (tools/generate.py --check keeps them up to date).

The rule of an id: lower-case letters, digits, hyphens and underscores (`[a-z0-9_-]+`). `####` and below are not checked
(they may have an id). Lines in a code block are skipped.

    python -m unittest tests.test_heading_ids -v
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FENCE = re.compile(r"^\s*(```|~~~)")
HEADING = re.compile(r"^(#{2,3}) (.*?)\s*$")
WITH_ID = re.compile(r"^(.*?) \{#([^}\s]+)\}$")
ID_RULE = re.compile(r"[a-z0-9_-]+")


def headings(page: Path) -> list[tuple[int, int, str, str | None]]:
    """(line number, level, text, id or None) of the ## and ### headings outside code blocks."""
    out = []
    in_code = False
    for n, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
        if FENCE.match(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = HEADING.match(line)
        if not m:
            continue
        w = WITH_ID.match(m.group(2))
        out.append((n, len(m.group(1)), w.group(1) if w else m.group(2), w.group(2) if w else None))
    return out


def pages(lang: str) -> dict[str, Path]:
    base = ROOT / "docs" / lang
    return {str(p.relative_to(base)): p for p in sorted(base.rglob("*.md"))}


class HeadingIdTest(unittest.TestCase):
    def test_every_heading_has_an_id(self):
        missing = []
        for lang in ("en", "ja"):
            for rel, page in pages(lang).items():
                for n, level, text, hid in headings(page):
                    if hid is None:
                        missing.append(f"docs/{lang}/{rel}:{n}: {'#' * level} {text}")
        self.assertEqual(missing, [], "add {#id} (the same in en and ja):\n" + "\n".join(missing))

    def test_id_characters(self):
        bad = []
        for lang in ("en", "ja"):
            for rel, page in pages(lang).items():
                for n, _, _, hid in headings(page):
                    if hid is not None and not ID_RULE.fullmatch(hid):
                        bad.append(f"docs/{lang}/{rel}:{n}: {hid}")
        self.assertEqual(bad, [], "an id is made of a-z, 0-9, - and _ only:\n" + "\n".join(bad))

    def test_same_ids_in_en_and_ja(self):
        en, ja = pages("en"), pages("ja")
        diff = []
        for rel in sorted(set(en) & set(ja)):
            a = [(lv, i) for _, lv, _, i in headings(en[rel])]
            b = [(lv, i) for _, lv, _, i in headings(ja[rel])]
            if a != b:
                diff.append(f"{rel}: en {[i for _, i in a]} / ja {[i for _, i in b]}")
        self.assertEqual(diff, [], "the levels and ids of ## and ### must be the same in en and ja:\n" + "\n".join(diff))

    def test_no_duplicate_id_in_a_page(self):
        dup = []
        for lang in ("en", "ja"):
            for rel, page in pages(lang).items():
                ids = [i for _, _, _, i in headings(page) if i]
                dup += [f"docs/{lang}/{rel}: {i}" for i in sorted({i for i in ids if ids.count(i) > 1})]
        self.assertEqual(dup, [], "\n".join(dup))


if __name__ == "__main__":
    unittest.main()
