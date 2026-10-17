"""Tests of tools/generate.py.

    python -m unittest discover -s tests -v

They use a small docs tree in a temporary directory and the real spec.
"""

import io
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

PAGE_EN = """\
---
title: System settings
---

# System settings

Hand-written text before.

<!-- osc: /getVersion -->

Hand-written text between.

<!-- osc: /setMicrostepMode -->

<!-- osc-message: /booted -->

<!-- osc-related: motion -->

<!-- osc-settings: speedProfile -->

Hand-written text after.
"""

PLAIN = "# A page without markers\n\nSome text with `/getVersion` and <!-- a comment -->.\n"


def run(docs: Path, **kw) -> tuple[int, str]:
    out = io.StringIO()
    code = generate.run(docs, SPEC, out=out, **kw)
    return code, out.getvalue()


def tree(docs: Path) -> dict[str, bytes]:
    return {str(p.relative_to(docs)): p.read_bytes() for p in sorted(docs.rglob("*")) if p.is_file()}


class GenerateTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.docs = Path(self._tmp.name) / "docs"
        ref = self.docs / "osc-command-references"
        ref.mkdir(parents=True)
        (ref / "system-settings_en.md").write_text(PAGE_EN, encoding="utf-8")
        (ref / "system-settings_jp.md").write_text(PAGE_EN.replace("System settings", "基板全体の設定"), encoding="utf-8")
        (ref / "plain_en.md").write_text(PLAIN, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_idempotent(self):
        code, _ = run(self.docs)
        self.assertEqual(code, 0)
        first = tree(self.docs)
        code, text = run(self.docs)
        self.assertEqual(code, 0)
        self.assertIn("changed: 0", text)
        self.assertEqual(tree(self.docs), first)
        code, _ = run(self.docs, check=True)
        self.assertEqual(code, 0)

    def test_marker_is_kept_and_text_expanded(self):
        run(self.docs)
        text = (self.docs / "osc-command-references" / "system-settings_en.md").read_text(encoding="utf-8")
        self.assertIn("<!-- osc: /getVersion -->\n<!-- generated:begin osc /getVersion -->\n### `/getVersion`", text)
        self.assertIn("{#getversion}", text)
        self.assertIn("{#setmicrostepmode}", text)
        self.assertIn("resetCause", text)               # /booted message block
        self.assertIn("Hand-written text between.", text)
        self.assertIn("Hand-written text after.", text)
        self.assertEqual(text.count("generated:begin"), 5)
        self.assertEqual(text.count("generated:end"), 5)

    def test_page_without_markers_is_not_touched(self):
        before = (self.docs / "osc-command-references" / "plain_en.md").read_bytes()
        run(self.docs)
        self.assertEqual((self.docs / "osc-command-references" / "plain_en.md").read_bytes(), before)

    def test_unknown_address_is_an_error_and_nothing_is_written(self):
        page = self.docs / "osc-command-references" / "system-settings_en.md"
        page.write_text(PAGE_EN.replace("/getVersion", "/noSuchCommand"), encoding="utf-8")
        before = tree(self.docs)
        code, text = run(self.docs)
        self.assertEqual(code, 1)
        self.assertIn("unknown command address /noSuchCommand", text)
        self.assertEqual(tree(self.docs), before)

    def test_unknown_message_and_group_are_errors(self):
        page = self.docs / "osc-command-references" / "plain_en.md"
        page.write_text("<!-- osc-message: /noSuchMessage -->\n<!-- osc-related: nogroup -->\n", encoding="utf-8")
        code, text = run(self.docs)
        self.assertEqual(code, 1)
        self.assertIn("unknown message address /noSuchMessage", text)
        self.assertIn("unknown group 'nogroup'", text)

    def test_stale_generated_block_is_replaced(self):
        run(self.docs)
        page = self.docs / "osc-command-references" / "system-settings_en.md"
        text = page.read_text(encoding="utf-8")
        page.write_text(text.replace("### `/getVersion`", "### EDITED BY HAND"), encoding="utf-8")
        code, _ = run(self.docs, check=True)
        self.assertEqual(code, 1)                      # the edit is detected
        run(self.docs)
        self.assertNotIn("EDITED BY HAND", page.read_text(encoding="utf-8"))

    def test_generated_pages_exist_in_both_languages(self):
        run(self.docs)
        for name in ("osc-command-references/command-list_en.md", "osc-command-references/command-list_jp.md",
                     "osc-command-references/diff_400_800_command_en.md", "osc-command-references/diff_400_800_command_jp.md",
                     "connections-and-settings/configuration-items_en.md", "connections-and-settings/configuration-items_jp.md"):
            text = (self.docs / name).read_text(encoding="utf-8")
            self.assertIn("generated from spec/osc-commands.yaml", text, name)

    def test_front_matter_of_an_existing_page_is_kept(self):
        page = self.docs / "osc-command-references" / "command-list_en.md"
        page.write_text("---\ntitle: Command list\nwp_id: 123\nlink: \"https://example.org/old/\"\n---\n\nold body\n", encoding="utf-8")
        run(self.docs)
        text = page.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\ntitle: Command list\nwp_id: 123\n"))
        self.assertNotIn("old body", text)

    def test_every_command_is_in_the_command_list(self):
        run(self.docs)
        text = (self.docs / "osc-command-references" / "command-list_en.md").read_text(encoding="utf-8")
        for c in SPEC.commands:
            self.assertIn(f"`{c['address']}`", text, c["address"])

    def test_defaults_option(self):
        outs = {}
        for mode in ("firmware", "template", "both"):
            d = Path(self._tmp.name) / f"docs_{mode}"
            shutil.copytree(self.docs, d)
            run(d, defaults=mode)
            outs[mode] = (d / "connections-and-settings" / "configuration-items_en.md").read_text(encoding="utf-8")
        acc = [l for l in outs["both"].splitlines() if "`acc`" in l][0]
        self.assertIn("1000 (firmware) / 2000 (template)", acc)
        self.assertIn("| 1000 |", [l for l in outs["firmware"].splitlines() if "`acc`" in l][0])
        self.assertIn("| 2000 |", [l for l in outs["template"].splitlines() if "`acc`" in l][0])

    def test_japanese_falls_back_to_english_and_is_counted(self):
        code, text = run(self.docs)
        self.assertEqual(code, 0)
        page = (self.docs / "osc-command-references" / "system-settings_jp.md").read_text(encoding="utf-8")
        self.assertIn("実行可能タイミング", page)       # labels are Japanese
        self.assertIn("Japanese texts filled with English:", text)
        n = int(text.split("Japanese texts filled with English:")[1].split()[0])
        self.assertGreater(n, 0)                          # /booted resetCause etc. have no ja

    def test_coverage_check_reports_missing_markers(self):
        code, text = run(self.docs, coverage=True)
        self.assertEqual(code, 1)
        self.assertIn("/setDestIp: marker found 0 times", text)


class RealDocsTest(unittest.TestCase):
    def test_generated_pages_of_the_repository_are_up_to_date(self):
        """The committed generated pages equal what generate.py writes now."""
        code, text = run(ROOT / "docs", check=True)
        self.assertEqual(code, 0, text)


if __name__ == "__main__":
    unittest.main()
