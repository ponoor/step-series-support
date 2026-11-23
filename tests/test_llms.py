"""Tests of the generation of docs/llms.txt and docs/llms-full.txt (tools/generate.py, English only)."""

import io
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import generate  # noqa: E402
from spec import Spec  # noqa: E402

SPEC = Spec.load()
DOCS = ROOT / "docs"
MK = generate.load_mkdocs(DOCS)
SECTIONS = generate.nav_sections(MK["nav"])
NAV_PAGES = [p for _, pages in SECTIONS for p in pages]


def make(docs: Path = DOCS) -> dict[str, str]:
    errors: list[str] = []
    out = generate.generate_llms(docs, SPEC, "both", errors)
    assert not errors, errors
    return {p.name: t for p, t in out.items()}


class LlmsTest(unittest.TestCase):
    def test_llms_txt_has_all_nav_pages_in_order(self):
        text = make()[generate.LLMS_FILE]
        self.assertTrue(text.startswith("# STEP Series\n\n> "))
        links = re.findall(r"^- \[[^\]]*\]\(([^)]*)\)", text, re.M)
        expected = [generate.page_url(p) for p in NAV_PAGES] + [generate.LLMS_FULL_FILE]
        self.assertEqual(links, expected)
        heads = re.findall(r"^## (.*)$", text, re.M)
        self.assertEqual(heads, [name for name, _ in SECTIONS] + ["Optional"])
        self.assertIn(MK["site_url"], text)

    def test_links_point_to_existing_pages(self):
        for page in NAV_PAGES:
            self.assertTrue((DOCS / "en" / page).is_file(), page)
        # what mkdocs makes of them (use_directory_urls: true)
        self.assertTrue(MK["use_directory_urls"])
        self.assertEqual(generate.page_url("index.md"), "./")
        self.assertEqual(generate.page_url("reference/index.md"), "reference/")
        self.assertEqual(generate.page_url("guides/servo-mode.md"), "guides/servo-mode/")
        self.assertTrue((DOCS / generate.LLMS_FULL_FILE).is_file())

    def test_full_has_every_command_and_message(self):
        text = make()[generate.LLMS_FULL_FILE]
        heads = set(re.findall(r"^#### (/\S+)$", text, re.M))
        for c in SPEC.commands:
            self.assertIn(c["address"], heads)
        for m in SPEC.messages:
            self.assertIn(m["address"], heads)
        for s in SPEC.settings:
            self.assertIn(f"`{s['key']}`", text)
        self.assertNotIn("](", text.split("## Functional guides")[0])
        self.assertNotIn("{#", text)
        self.assertNotIn("<!--", text)
        self.assertNotIn("\r", text)

    def test_same_output_twice(self):
        self.assertEqual(make(), make())

    def test_check_finds_a_difference(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            shutil.copy(ROOT / "mkdocs.yml", root / "mkdocs.yml")
            docs = root / "docs"
            shutil.copytree(DOCS / "en", docs / "en")
            shutil.copytree(DOCS / "ja", docs / "ja")
            run = lambda **kw: (generate.run(docs, SPEC, out=(buf := io.StringIO()), llms=True, **kw), buf.getvalue())[0:2]
            code, _ = run()
            self.assertEqual(code, 0)
            code, out = run(check=True)
            self.assertEqual(code, 0, out)
            (docs / generate.LLMS_FILE).write_text("old\n", encoding="utf-8")
            code, out = run(check=True)
            self.assertEqual(code, 1)
            self.assertIn("would change docs/llms.txt", out)
            self.assertEqual((docs / generate.LLMS_FILE).read_text(encoding="utf-8"), "old\n")
            (docs / generate.LLMS_FILE).unlink()
            (docs / generate.LLMS_FULL_FILE).write_text("old\n", encoding="utf-8")
            code, out = run(check=True)
            self.assertEqual(code, 1)
            self.assertIn("would change docs/llms-full.txt", out)


if __name__ == "__main__":
    unittest.main()
