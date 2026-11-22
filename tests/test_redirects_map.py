"""docs/_redirects_map.md: every New page exists and New URL is made from it (use_directory_urls, relative to the top of the site)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP = ROOT / "docs" / "_redirects_map.md"


def rows():
    out = []
    for line in MAP.read_text(encoding="utf-8").splitlines():
        if line.startswith(("| en ", "| ja ")):
            out.append([c.strip().strip("`") for c in line.strip().strip("|").split("|")])
    return out


def url_of(page: str) -> str:
    lang, *rest = page[:-3].split("/")
    if rest[-1] == "index":
        rest = rest[:-1]
    path = "/".join(rest) + "/" if rest else ""
    return (path or "./") if lang == "en" else "ja/" + path


class RedirectsMapTest(unittest.TestCase):
    def test_rows_exist(self):
        self.assertEqual(len(rows()), 92)

    def test_new_pages_exist_and_urls_match(self):
        for lang, old_url, _title, page, new_url, old_file in rows():
            self.assertTrue(page.startswith(lang + "/"), page)
            self.assertTrue((ROOT / "docs" / page).is_file(), f"missing: {page}")
            self.assertEqual(new_url, url_of(page), page)
            self.assertTrue((ROOT / old_file).is_file(), f"missing: {old_file}")

    def test_old_urls_are_unique(self):
        keys = [(r[0], r[1]) for r in rows()]
        self.assertEqual(len(keys), len(set(keys)))


if __name__ == "__main__":
    unittest.main()
