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
if HAVE_MKDOCS:
    sys.path.insert(0, str(ROOT / "tools"))
    import mkdocs_hooks as hooks


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

    def config(self, rel):
        return json.loads((self.site / rel).read_text(encoding="utf-8"))["config"]

    def test_config_lang_and_separator_per_language(self):
        ja, en = self.config("search/search_index.json"), self.config("en/search/search_index.json")
        # lang stays ['en', 'ja'] in both: with ['en'] or ['ja'] alone "setSpeedProfile" is not found (tools/search_probe.py)
        self.assertEqual(ja["lang"], ["en", "ja"])
        self.assertEqual(en["lang"], ["en", "ja"])
        self.assertEqual(en["separator"], r"[\s\-]+")   # English: the plugin's own separator, unchanged
        self.assertEqual(ja["separator"], hooks.JA_SEPARATOR)
        self.assertNotEqual(ja["separator"], en["separator"])

    def test_japanese_separator_cuts_between_scripts(self):
        # The separator is a JavaScript regular expression; these patterns mean the same in Python's re.
        sep = re.compile(self.config("search/search_index.json")["separator"])
        cut = lambda text: [w for w in sep.split(text) if w]
        for text, words in {
            "電磁ブレーキ": ["電磁", "ブレーキ"],
            "設定ファイル": ["設定", "ファイル"],
            "ブラウザ設定ツール": ["ブラウザ", "設定", "ツール"],
            "電圧モード": ["電圧", "モード"],
            "microSDカード": ["microSD", "カード"],
            "HOMEスイッチ": ["HOME", "スイッチ"],
            "5V電源": ["5V", "電源"],
            "move to-home": ["move", "to", "home"],           # whitespace and hyphen as before
        }.items():
            self.assertEqual(cut(text), words, text)
        # whole words that must not be cut
        for text in ("原点復帰", "ファームウェア", "ステッピングモータ", "STEP400", "setSpeedProfile", "切り替え"):
            self.assertEqual(cut(text), [text], text)


if __name__ == "__main__":
    unittest.main()
