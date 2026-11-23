"""The search index is split per language (tools/mkdocs_hooks.py): the Japanese pages (top) and the English pages (en/) each get
their own search/search_index.json, and the English pages read theirs (base in __config is the en/ root).
The test builds the site into a temporary directory (mkdocs build, about 10 s); it is skipped when mkdocs is not installed."""
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

try:
    import mkdocs  # noqa: F401
    import material  # noqa: F401
    HAVE_MKDOCS = True
except ImportError:
    HAVE_MKDOCS = False


@unittest.skipUnless(HAVE_MKDOCS, "mkdocs / mkdocs-material is not installed")
class SearchIndexTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.site = Path(cls._tmp.name) / "site"
        r = subprocess.run([sys.executable, "-m", "mkdocs", "build", "-q", "-d", str(cls.site)], cwd=ROOT, capture_output=True, text=True)
        assert r.returncode == 0, r.stderr[-2000:]

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def load(self, rel):
        return json.loads((self.site / rel).read_text(encoding="utf-8"))["docs"]

    def test_japanese_index_has_no_english(self):
        docs = self.load("search/search_index.json")
        self.assertTrue(docs)
        self.assertFalse([d["location"] for d in docs if d["location"].startswith("en/")])

    def test_english_index_has_only_english_relative_to_en(self):
        docs = self.load("en/search/search_index.json")
        self.assertTrue(docs)
        for d in docs:
            self.assertFalse(d["location"].startswith("en/"), d["location"])
            page = d["location"].split("#")[0]
            self.assertTrue((self.site / "en" / page / "index.html").is_file(), d["location"])

    def test_locations_point_to_real_pages(self):
        for rel, base in (("search/search_index.json", self.site), ("en/search/search_index.json", self.site / "en")):
            for d in self.load(rel):
                page = d["location"].split("#")[0]
                self.assertTrue((base / page / "index.html").is_file(), f"{rel}: {d['location']}")

    def test_config_base(self):
        def base(rel):
            html = (self.site / rel).read_text(encoding="utf-8")
            return re.search(r'"base": "([^"]*)"', html).group(1)
        self.assertEqual(base("index.html"), ".")
        self.assertEqual(base("guides/homing-and-position/index.html"), "../..")
        self.assertEqual(base("en/index.html"), ".")          # the en/ root, where search/ is
        self.assertEqual(base("en/guides/homing-and-position/index.html"), "../..")  # -> en/ (not the site root)


if __name__ == "__main__":
    unittest.main()
