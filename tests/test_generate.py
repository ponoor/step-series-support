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
        ref = self.docs / "en" / "reference"
        ref.mkdir(parents=True)
        (ref / "system-settings.md").write_text(PAGE_EN, encoding="utf-8")
        (ref / "plain.md").write_text(PLAIN, encoding="utf-8")
        refja = self.docs / "ja" / "reference"
        refja.mkdir(parents=True)
        (refja / "system-settings.md").write_text(PAGE_EN.replace("System settings", "基板全体の設定"), encoding="utf-8")

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
        text = (self.docs / "en" / "reference" / "system-settings.md").read_text(encoding="utf-8")
        self.assertIn("<!-- osc: /getVersion -->\n<!-- generated:begin osc /getVersion -->\n### `/getVersion`", text)
        self.assertIn("{#getversion}", text)
        self.assertIn("{#setmicrostepmode}", text)
        self.assertIn("resetCause", text)               # /booted message block
        self.assertIn("Hand-written text between.", text)
        self.assertIn("Hand-written text after.", text)
        self.assertEqual(text.count("generated:begin"), 5)
        self.assertEqual(text.count("generated:end"), 5)

    def test_page_without_markers_is_not_touched(self):
        before = (self.docs / "en" / "reference" / "plain.md").read_bytes()
        run(self.docs)
        self.assertEqual((self.docs / "en" / "reference" / "plain.md").read_bytes(), before)

    def test_unknown_address_is_an_error_and_nothing_is_written(self):
        page = self.docs / "en" / "reference" / "system-settings.md"
        page.write_text(PAGE_EN.replace("/getVersion", "/noSuchCommand"), encoding="utf-8")
        before = tree(self.docs)
        code, text = run(self.docs)
        self.assertEqual(code, 1)
        self.assertIn("unknown command address /noSuchCommand", text)
        self.assertEqual(tree(self.docs), before)

    def test_unknown_message_and_group_are_errors(self):
        page = self.docs / "en" / "reference" / "plain.md"
        page.write_text("<!-- osc-message: /noSuchMessage -->\n<!-- osc-related: nogroup -->\n", encoding="utf-8")
        code, text = run(self.docs)
        self.assertEqual(code, 1)
        self.assertIn("unknown message address /noSuchMessage", text)
        self.assertIn("unknown group 'nogroup'", text)

    def test_stale_generated_block_is_replaced(self):
        run(self.docs)
        page = self.docs / "en" / "reference" / "system-settings.md"
        text = page.read_text(encoding="utf-8")
        page.write_text(text.replace("### `/getVersion`", "### EDITED BY HAND"), encoding="utf-8")
        code, _ = run(self.docs, check=True)
        self.assertEqual(code, 1)                      # the edit is detected
        run(self.docs)
        self.assertNotIn("EDITED BY HAND", page.read_text(encoding="utf-8"))

    def test_generated_pages_exist_in_both_languages(self):
        run(self.docs)
        for name in ("en/reference/command-list.md", "ja/reference/command-list.md",
                     "en/reference/differences-step400-step800.md", "ja/reference/differences-step400-step800.md",
                     "en/connections/configuration-items.md", "ja/connections/configuration-items.md"):
            text = (self.docs / name).read_text(encoding="utf-8")
            self.assertIn("generated from spec/osc-commands.yaml", text, name)

    def test_front_matter_of_an_existing_page_is_kept(self):
        page = self.docs / "en" / "reference" / "command-list.md"
        page.write_text("---\ntitle: Command list\nwp_id: 123\nlink: \"https://example.org/old/\"\n---\n\nold body\n", encoding="utf-8")
        run(self.docs)
        text = page.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\ntitle: Command list\nwp_id: 123\n"))
        self.assertNotIn("old body", text)

    def test_every_command_is_in_the_command_list(self):
        run(self.docs)
        text = (self.docs / "en" / "reference" / "command-list.md").read_text(encoding="utf-8")
        for c in SPEC.commands:
            self.assertIn(f"`{c['address']}`", text, c["address"])

    def test_defaults_option(self):
        outs = {}
        for mode in ("firmware", "template", "both"):
            d = Path(self._tmp.name) / f"docs_{mode}"
            shutil.copytree(self.docs, d)
            run(d, defaults=mode)
            outs[mode] = (d / "en" / "connections" / "configuration-items.md").read_text(encoding="utf-8")
        acc = [l for l in outs["both"].splitlines() if "`acc`" in l][0]
        self.assertIn("1000 (firmware) / 2000 (template)", acc)
        self.assertIn("| 1000 |", [l for l in outs["firmware"].splitlines() if "`acc`" in l][0])
        self.assertIn("| 2000 |", [l for l in outs["template"].splitlines() if "`acc`" in l][0])

    def test_japanese_falls_back_to_english_and_is_counted(self):
        """A Japanese text that is empty is filled with the English one and counted."""
        import copy
        data = copy.deepcopy(SPEC.data)
        msg = next(m for m in data["messages"] if m["address"] == "/booted")
        change = msg["changes"][0]
        change["ja"] = ""
        out = io.StringIO()
        self.assertEqual(generate.run(self.docs, Spec(data), out=out), 0)
        text = out.getvalue()
        page = (self.docs / "ja" / "reference" / "system-settings.md").read_text(encoding="utf-8")
        self.assertIn("実行可能タイミング", page)       # labels are Japanese
        self.assertIn(change["en"], page)                # the English text is used
        self.assertIn("Japanese texts filled with English: 1 (change 1)", text)

    def test_repository_spec_has_no_empty_japanese_text(self):
        """Every text of the spec has a Japanese draft (the warnings of validate_spec.py)."""
        import validate_spec
        rep = validate_spec.Report()
        validate_spec.check_warnings(SPEC, rep)
        missing = [w for w in rep.warnings if w.startswith(("empty", "missing ja"))]
        self.assertEqual(missing, [])

    def test_since_and_changes_of_values_and_settings(self):
        """`since` / `changes` of a value, an error and a configuration item are shown like those of a command."""
        import copy
        data = copy.deepcopy(SPEC.data)
        msg = next(m for m in data["messages"] if m["address"] == "/error/command")
        vals = msg["args"][0]["values"]
        vals[0]["since"] = "9.9.9"
        vals[0]["changes"] = [{"version": "9.9.9", "en": "Changed text of a value.", "ja": "値の変更。"}]
        setting = next(x for x in data["settings"] if x["key"] == "driverSettings.homingAtStartup")
        setting["since"] = "9.9.9"
        setting["changes"] = [{"version": "9.9.9", "en": "Changed text of a setting.", "ja": ""}]
        spec = Spec(data)
        page = self.docs / "en" / "reference" / "system-settings.md"
        page.write_text(PAGE_EN.replace("<!-- osc: /getVersion -->", "<!-- osc-message: /error/command -->"), encoding="utf-8")
        out = io.StringIO()
        self.assertEqual(generate.run(self.docs, spec, out=out), 0, out.getvalue())
        text = page.read_text(encoding="utf-8")
        self.assertIn("Added in v9.9.9.", text)
        self.assertIn("**v9.9.9**: Changed text of a value.", text)
        settings_en = (self.docs / "en" / "connections" / "configuration-items.md").read_text(encoding="utf-8")
        line = [l for l in settings_en.splitlines() if "`homingAtStartup`" in l][0]
        self.assertIn("Added in v9.9.9.", line)
        self.assertIn("**v9.9.9**: Changed text of a setting.", line)
        settings_ja = (self.docs / "ja" / "connections" / "configuration-items.md").read_text(encoding="utf-8")
        line = [l for l in settings_ja.splitlines() if "`homingAtStartup`" in l][0]
        self.assertIn("v9.9.9で追加。", line)
        self.assertIn("Changed text of a setting.", line)    # no Japanese yet: English is used

    def test_coverage_check_reports_missing_markers(self):
        code, text = run(self.docs, coverage=True)
        self.assertEqual(code, 1)
        self.assertIn("/setDestIp: marker found 0 times", text)


class MarkerCoverageTest(unittest.TestCase):
    """Markers of the commands and of the messages (docs/en and docs/ja only)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.docs = Path(self._tmp.name) / "docs"
        self.required = generate.required_messages(SPEC)
        for lang in generate.LANGS:
            pages: dict[str, list[str]] = {}
            for c in SPEC.commands:
                pages.setdefault(SPEC.groups[c["group"]]["page"], []).append(f"<!-- osc: {c['address']} -->")
            pages[generate.MESSAGES_PAGE] = [f"<!-- osc-message: {a} -->" for a in self.required]
            for page, lines in pages.items():
                path = self.docs / lang / "reference" / f"{page}.md"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# page\n\n" + "\n\n".join(lines) + "\n", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def page(self, lang: str, name: str) -> Path:
        return self.docs / lang / "reference" / f"{name}.md"

    def test_required_messages(self):
        self.assertIn("/booted", self.required)
        for a in generate.STANDALONE_MESSAGES:
            self.assertIn(a, self.required)
        listed = {a for c in SPEC.commands for a in SPEC.response_messages(c)}
        self.assertNotIn("/version", self.required)
        self.assertIn("/version", listed)

    def test_complete_set_has_no_problem(self):
        self.assertEqual(generate.check_coverage(self.docs, SPEC), [])
        code, text = run(self.docs, coverage=True)
        self.assertEqual(code, 0, text)

    def test_missing_command_and_required_message(self):
        page = self.page("ja", "system-settings")
        page.write_text(page.read_text(encoding="utf-8").replace("<!-- osc: /getVersion -->", ""), encoding="utf-8")
        msgs = self.page("en", generate.MESSAGES_PAGE)
        msgs.write_text(msgs.read_text(encoding="utf-8").replace("<!-- osc-message: /booted -->", ""), encoding="utf-8")
        errors = generate.check_coverage(self.docs, SPEC)
        self.assertEqual(sorted(errors), sorted([
            "[ja] /getVersion: marker found 0 times (expected once in system-settings)",
            "[en] /booted: marker found 0 times (expected once in automatically-sent-messages)",
        ]))

    def test_optional_message_is_allowed_once_on_the_messages_page_only(self):
        msgs = self.page("en", generate.MESSAGES_PAGE)
        base = msgs.read_text(encoding="utf-8")
        msgs.write_text(base + "\n<!-- osc-message: /version -->\n", encoding="utf-8")
        self.assertEqual(generate.check_coverage(self.docs, SPEC), [])
        msgs.write_text(base + "\n<!-- osc-message: /version -->\n\n<!-- osc-message: /version -->\n", encoding="utf-8")
        self.assertEqual(generate.check_coverage(self.docs, SPEC),
                         ["[en] /version: marker found 2 times (expected at most once in automatically-sent-messages)"])
        msgs.write_text(base, encoding="utf-8")
        other = self.page("ja", "system-settings")
        other.write_text(other.read_text(encoding="utf-8") + "\n<!-- osc-message: /version -->\n", encoding="utf-8")
        self.assertEqual(generate.check_coverage(self.docs, SPEC),
                         ["[ja] /version: marker in system-settings, expected the page of the messages (automatically-sent-messages)"])

    def test_misplaced_and_duplicated_commands(self):
        ss = self.page("en", "system-settings")
        ss.write_text(ss.read_text(encoding="utf-8") + "\n<!-- osc: /getVersion -->\n", encoding="utf-8")
        msgs = self.page("ja", generate.MESSAGES_PAGE)
        msgs.write_text(msgs.read_text(encoding="utf-8").replace("<!-- osc-message: /booted -->", "<!-- osc-message: /booted -->\n\n<!-- osc: /getVersion -->"), encoding="utf-8")
        errors = generate.check_coverage(self.docs, SPEC)
        self.assertIn("[en] /getVersion: marker found 2 times (expected once in system-settings)", errors)
        self.assertTrue(any(e.startswith("[ja] /getVersion: marker found 2 times") for e in errors), errors)

    def test_other_directories_are_not_counted(self):
        old = self.docs / "osc-command-references" / "system-settings_en.md"
        old.parent.mkdir(parents=True)
        old.write_text("<!-- osc: /getVersion -->\n", encoding="utf-8")
        self.assertEqual(generate.check_coverage(self.docs, SPEC), [])

    def test_usual_run_warns_with_numbers_and_keeps_the_exit_code(self):
        empty = Path(self._tmp.name) / "empty"
        (empty / "en" / "reference").mkdir(parents=True)
        (empty / "en" / "reference" / "plain.md").write_text(PLAIN, encoding="utf-8")
        code, text = run(empty)
        self.assertEqual(code, 0)
        n, m = len(SPEC.commands), len(self.required)
        for lang in generate.LANGS:
            self.assertIn(f"WARNING [{lang}] markers: commands 0/{n}, messages 0/{m} required; 0 misplaced, 0 duplicated "
                          "(run with --coverage for the list)", text)
        code, text = run(empty, check=True)
        self.assertEqual(code, 0)                              # --check: nothing would change, the warning does not matter
        self.assertNotIn("ERROR", text)
        code, text = run(self.docs)
        self.assertEqual(code, 0)
        self.assertIn(f"commands {n}/{n}, messages {m}/{m} required; 0 misplaced, 0 duplicated", text)
        code, text = run(empty, coverage=True)
        self.assertEqual(code, 1)
        self.assertNotIn("WARNING", text)


class RealDocsTest(unittest.TestCase):
    def test_generated_pages_of_the_repository_are_up_to_date(self):
        """The committed generated pages equal what generate.py writes now."""
        code, text = run(ROOT / "docs", check=True)
        self.assertEqual(code, 0, text)


if __name__ == "__main__":
    unittest.main()
