"""Tests of tools/generate.py.

    python -m unittest discover -s tests -v

They use a small docs tree in a temporary directory and the real spec.
"""

import io
import re
from collections import Counter
from decimal import Decimal
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

    def _related_page(self, related: str, settings: str) -> str:
        page = self.docs / "en" / "reference" / "plain.md"
        page.write_text(f"<!-- osc-related: {related} -->\n\n<!-- osc-settings: {settings} -->\n", encoding="utf-8")
        run(self.docs)
        return page.read_text(encoding="utf-8")

    def test_related_accepts_commands_and_settings_in_the_given_order_without_repeats(self):
        text = self._related_page("/setKval, brake, /setKval, /getKval",
                                  "driverSettings.brakeTransitionDuration, driverSettings.isCurrentMode, "
                                  "driverSettings.brakeTransitionDuration")
        self.assertEqual(text.count("[`/setKval`]"), 1)
        self.assertLess(text.index("[`/setKval`]"), text.index("[`/activate`]"))
        self.assertLess(text.index("[`/activate`]"), text.index("[`/getKval`]"))
        self.assertEqual(text.count("[`driverSettings.brakeTransitionDuration`]"), 1)
        self.assertLess(text.index("[`driverSettings.brakeTransitionDuration`]"),
                        text.index("[`driverSettings.isCurrentMode`]"))
        self.assertNotIn("[`driverSettings.homingAtStartup`]", text)     # only the two settings, not the section

    def test_related_group_after_command_is_not_listed_twice(self):
        text = self._related_page("/activate, brake", "speedProfile")
        self.assertEqual(text.count("[`/activate`]"), 1)
        self.assertLess(text.index("[`/activate`]"), text.index("[`/free`]"))

    def test_unknown_related_command_and_setting_are_errors(self):
        page = self.docs / "en" / "reference" / "plain.md"
        page.write_text("<!-- osc-related: /noSuchCommand -->\n<!-- osc-settings: driverSettings.noSuch -->\n",
                        encoding="utf-8")
        code, text = run(self.docs)
        self.assertEqual(code, 1)
        self.assertIn("unknown command address /noSuchCommand", text)
        self.assertIn("unknown settings section 'driverSettings.noSuch'", text)

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
        self.required = generate.standalone_messages(SPEC)
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

    def test_standalone_messages(self):
        listed = {a for c in SPEC.commands for a in SPEC.response_messages(c)}
        notified = {n if isinstance(n, str) else n["message"] for c in SPEC.commands for n in c.get("notifies", []) or []}
        self.assertEqual(len(notified), 16)        # the 15 of the task and /homingStatus
        for a in ("/booted", *generate.STANDALONE_MESSAGES):                 # 1 and 2
            self.assertIn(a, self.required)
        self.assertIn("/booted", self.required)
        self.assertTrue(all(a in self.required for a in notified))           # 3
        self.assertIn("/homingStatus", notified)
        for a in ("/version", "/configName", "/brakeStatus"):
            self.assertIn(a, listed)
            self.assertNotIn(a, self.required)
        expected = {m["address"] for m in SPEC.messages
                    if m["address"] not in listed | notified} | set(generate.STANDALONE_MESSAGES) | notified
        self.assertEqual(set(self.required), expected)

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

    def test_marker_of_a_message_outside_the_set_is_an_error(self):
        msgs = self.page("en", generate.MESSAGES_PAGE)
        base = msgs.read_text(encoding="utf-8")
        msgs.write_text(base + "\n<!-- osc-message: /version -->\n", encoding="utf-8")
        self.assertEqual(generate.check_coverage(self.docs, SPEC),
                         ["[en] /version: marker not allowed (not a standalone message; it is shown in the response of its commands)"])
        msgs.write_text(base, encoding="utf-8")
        other = self.page("ja", "system-settings")
        other.write_text(other.read_text(encoding="utf-8") + "\n<!-- osc-message: /version -->\n", encoding="utf-8")
        self.assertEqual(len(generate.check_coverage(self.docs, SPEC)), 1)
        self.assertIn("[ja] /version: marker not allowed", generate.check_coverage(self.docs, SPEC)[0])

    def test_standalone_message_marker_in_another_page_is_misplaced(self):
        other = self.page("ja", "system-settings")
        msgs = self.page("ja", generate.MESSAGES_PAGE)
        msgs.write_text(msgs.read_text(encoding="utf-8").replace("<!-- osc-message: /busy -->", ""), encoding="utf-8")
        other.write_text(other.read_text(encoding="utf-8") + "\n<!-- osc-message: /busy -->\n", encoding="utf-8")
        self.assertEqual(generate.check_coverage(self.docs, SPEC),
                         ["[ja] /busy: marker in system-settings, expected the page of the messages (automatically-sent-messages)"])

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


class ResponseTest(unittest.TestCase):
    """Messages that are not standalone are shown in full in the response; links in argument descriptions."""

    def expand(self, lang: str, marker: str) -> str:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            page = docs / lang / "reference" / "system-settings.md"
            page.parent.mkdir(parents=True)
            page.write_text(f"# page\n\n{marker}\n", encoding="utf-8")
            out = io.StringIO()
            self.assertEqual(generate.run(docs, SPEC, out=out), 0, out.getvalue())
            return page.read_text(encoding="utf-8")

    def test_response_shows_description_tables_and_changes_of_a_message(self):
        text = self.expand("en", "<!-- osc: /getConfigName -->")
        resp = text[text.index("#### Response"):]
        self.assertIn("##### Combinations of configFileOpenSucceeded", resp)    # table of the message
        self.assertNotIn("######", resp)                                          # headings do not skip a level
        self.assertIn("##### Changes", resp)
        self.assertNotIn("automatically-sent-messages", resp)
        text = self.expand("ja", "<!-- osc: /getBrakeStatus -->")
        resp = text[text.index("#### 返信"):]
        self.assertIn("##### 説明", resp)

    def test_standalone_message_in_a_response_is_a_link_only(self):
        text = self.expand("en", "<!-- osc: /getHomingStatus -->")
        resp = text[text.index("#### Response"):]
        self.assertIn("automatically-sent-messages", resp)
        self.assertNotIn("##### Description", resp)

    def test_link_to_a_message_that_is_not_standalone_goes_to_its_command(self):
        ctx = generate.Ctx(SPEC, "en", "both", Counter(), [])
        first = generate.response_owner(SPEC, "/configName")
        href = ctx.link_to("/configName", prefer="message")
        self.assertTrue(href.endswith("#" + generate.anchor(first["address"])), href)
        self.assertIn(SPEC.groups[first["group"]]["page"], href)
        self.assertIn("automatically-sent-messages.md#busy", ctx.link_to("/busy", prefer="message"))

    def test_links_in_argument_descriptions_and_values_are_expanded(self):
        text = self.expand("en", "<!-- osc-message: /booted -->")
        self.assertNotIn("[[", text)
        text = self.expand("en", "<!-- osc: /saveConfig -->\n\n<!-- osc: /getConfigName -->")
        self.assertNotIn("[[", text)
        self.assertRegex(text, r"\[`/setConfigName`\]\([^)]*#setconfigname\)")


class JapaneseOutputTest(unittest.TestCase):
    """The Japanese text that generate.py puts together follows the spacing rules of the glossary
    (validate_spec.find_wording, the same function as the check of the hand-written pages)."""

    @classmethod
    def setUpClass(cls):
        import validate_spec
        cls.validate_spec = validate_spec
        cls.spacing = {"spacing": validate_spec.load_glossary()["spacing"]}
        cls.texts: dict[str, str] = {}
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            page = docs / "ja" / "reference" / "all.md"
            page.parent.mkdir(parents=True)
            marks = [f"<!-- osc: {c['address']} -->" for c in SPEC.commands]
            marks += [f"<!-- osc-message: {a} -->" for a in generate.standalone_messages(SPEC)]
            page.write_text("# all\n\n" + "\n\n".join(marks) + "\n", encoding="utf-8")
            out = io.StringIO()
            assert generate.run(docs, SPEC, out=out) == 0, out.getvalue()
            for path in (docs / "ja").rglob("*.md"):
                cls.texts[path.name] = path.read_text(encoding="utf-8")

    def findings(self, name: str) -> list[str]:
        import re
        text = re.sub(r"<!--.*?-->", "", self.texts[name], flags=re.S)       # the markers and the generated notes
        return [f"{name}: {f['word']}: ...{f['ctx']}..." for f in self.validate_spec.find_wording(text, self.spacing)]

    def test_all_commands_and_standalone_messages(self):
        self.assertEqual(self.findings("all.md"), [])

    def test_generated_pages(self):
        for name in ("command-list.md", "differences-step400-step800.md", "configuration-items.md"):
            self.assertEqual(self.findings(name), [], name)

    def test_forms(self):
        text = self.texts["all.md"]
        self.assertIn("1-4（STEP400）、1-8（STEP800）、255（全モータ）", text)
        self.assertIn("（ファームウェア）、", text)
        self.assertNotRegex(text, r"。 v\d")

    def test_english_is_unchanged(self):
        ctx = generate.Ctx(SPEC, "en", "both", Counter(), [])
        self.assertEqual(ctx.paren("x"), " (x)")
        self.assertEqual(ctx.join("a.", "b"), "a. b")
        self.assertEqual(generate.cell("a  \nb"), "a   b")


class SelfLinkTest(unittest.TestCase):
    def expand(self, lang: str, marker: str) -> str:
        return ResponseTest.expand(ResponseTest(), lang, marker)

    def test_a_block_does_not_link_to_itself(self):
        text = self.expand("en", "<!-- osc: /getConfigName -->")
        self.assertNotIn("](system-settings.md#getconfigname)", text.split("### `/getConfigName`", 1)[1])
        self.assertIn("`/configName`", text)
        text = self.expand("ja", "<!-- osc: /getBrakeStatus -->")
        self.assertNotIn("](brake.md#getbrakestatus)", text)
        self.assertIn("`/getBrakeStatus`", text)

    def test_a_link_to_another_block_stays_a_link(self):
        text = self.expand("en", "<!-- osc: /getConfigName -->")
        self.assertRegex(text, r"\[`/setConfigName`\]\(system-settings\.md#setconfigname\)")


class SettingLinkTest(unittest.TestCase):
    """`[[network.destIp]]` (a `key` of `settings`) is a link to the list of the configuration items."""

    def ctx(self, lang: str) -> "generate.Ctx":
        ctx = generate.Ctx(SPEC, lang, "both", Counter(), [])
        ctx.where = "test"
        return ctx

    def test_a_setting_key_becomes_a_link(self):
        for lang in ("en", "ja"):
            ctx = self.ctx(lang)
            text = ctx.md("See [[network.destIp]].")
            self.assertIn("[`network.destIp`](../connections/configuration-items.md#network-destip)", text)
            self.assertEqual(ctx.errors, [])

    def test_an_unknown_key_is_an_error(self):
        ctx = self.ctx("en")
        self.assertIn("`network.nothing`", ctx.md("[[network.nothing]]"))
        self.assertEqual(len(ctx.errors), 1)

    def test_set_dest_ip_links_to_the_settings_in_both_languages(self):
        for lang in ("en", "ja"):
            text = (ROOT / "docs" / lang / "reference" / "system-settings.md").read_text(encoding="utf-8")
            body = text.split("### `/setDestIp`", 1)[1].split("### `/", 1)[0]
            self.assertIn("configuration-items.md#network-cansendmsgbeforedestip", body)
            self.assertIn("configuration-items.md#network-destip", body)


class CurrentTest(unittest.TestCase):
    """`current_step_mA` of a setting: (value + 1) x step, shown next to the initial value."""

    @staticmethod
    def parse(text: str) -> tuple[Decimal, int, Decimal]:
        """(value in the unit shown, digits after the point, mA per unit)"""
        m = re.fullmatch(r"([\d,]+(?:\.(\d+))?)(mA|A)", text)
        shown = Decimal(m.group(1).replace(",", ""))
        return shown, len(m.group(2) or ""), Decimal(1000 if m.group(3) == "A" else 1)

    def test_format(self):
        from spec import format_current
        for mA, expected in ((312.5, "312.5mA"), (5000, "5A"), (9687.5, "9.688A"), (999, "999mA"),
                              (1000, "1A"), (78.125, "78.125mA"), (1328.125, "1.328A"), (31.25, "31.25mA"), (3968.75, "3.969A"), (5078.125, "5.078A")):
            self.assertEqual(format_current(Decimal(str(mA))), expected)

    def test_the_formula_reproduces_the_rows_of_the_tables(self):
        """Every row (not "...") of the tables of the commands of a setting with `current_step_mA`.
        The tables round to the digits they show."""
        different = set()
        checked = 0
        for s in SPEC.settings:
            if "current_step_mA" not in s:
                continue
            for addr in s["commands"]:
                for t in SPEC.command(addr).get("tables", []):
                    rows = t["rows"]
                    per_board = rows if SPEC.is_board_map(rows) else {b: rows for b in SPEC.boards_of(s)}
                    for board, rs in per_board.items():
                        for value, text in (r for r in rs if r[0] != "..."):
                            checked += 1
                            shown, digits, unit = self.parse(text)
                            got = Decimal(str(SPEC.for_board(s["current_step_mA"], board))) * (value + 1) / unit
                            if round(got, digits) != shown:
                                different.add((s["key"], addr, board, value, text))
        self.assertGreater(checked, 20)
        self.assertEqual(different, set())

    def test_initial_values_show_the_current(self):
        for lang, (a, b) in (("en", (" (", ")")), ("ja", ("（", "）"))):
            ctx = SettingLinkTest.ctx(None, lang)
            oc = SPEC.setting("alarmAndReport.OCThreshold")
            self.assertEqual(generate._setting_value(ctx, oc, 15, "STEP400"), f"15{a}5A{b}")
            self.assertEqual(generate._setting_value(ctx, oc, 15, "STEP800"), f"15{a}6A{b}")
            stall = SPEC.setting("voltageMode.STALL_TH")
            self.assertEqual(generate._setting_value(ctx, stall, 127, "STEP800"), f"127{a}4A{b}")
            tval = SPEC.setting("currentMode.TVAL_RUN")
            self.assertEqual(generate._setting_value(ctx, tval, 16, "STEP400"), f"16{a}1.328A{b}")

    def test_a_setting_without_the_field_shows_the_value_only(self):
        ctx = SettingLinkTest.ctx(None, "en")
        self.assertEqual(generate._setting_value(ctx, SPEC.setting("currentMode.T_FAST"), 20, "STEP400").split(" ")[0], "20")
        self.assertIsNone(SPEC.current_text(SPEC.setting("currentMode.T_FAST"), "STEP400", 20))


class ReferencePagesTest(unittest.TestCase):
    """The hand-written reference pages (docs/<lang>/reference/) agree with the YAML."""

    def read(self, lang: str, name: str) -> str:
        return (ROOT / "docs" / lang / "reference" / f"{name}.md").read_text(encoding="utf-8")

    def test_every_timing_is_explained_in_the_common_rules(self):
        for lang in generate.LANGS:
            text = self.read(lang, "index")
            for key, names in SPEC.timings.items():
                self.assertIn(names[lang], text, f"[{lang}] timing '{key}' ({names[lang]}) is not in index.md")

    def test_titles_of_the_group_pages_are_the_names_of_the_groups(self):
        import re
        for lang in generate.LANGS:
            for key, g in SPEC.groups.items():
                text = self.read(lang, g["page"])
                m = re.match(r"---\ntitle: (.+)\n(?:[a-z]+: .*\n)*---\n", text)
                self.assertIsNotNone(m, f"[{lang}] {g['page']}: no title in the front matter")
                self.assertEqual(m.group(1).strip().strip('"'), g[lang], f"[{lang}] {g['page']}: title")
                h1 = re.search(r"^# (.+)$", text, re.M)
                self.assertIsNotNone(h1, f"[{lang}] {g['page']}: no # heading")
                self.assertEqual(h1.group(1).strip(), g[lang], f"[{lang}] {g['page']}: # heading")


class RealDocsTest(unittest.TestCase):
    def test_generated_pages_of_the_repository_are_up_to_date(self):
        """The committed generated pages equal what generate.py writes now."""
        code, text = run(ROOT / "docs", check=True)
        self.assertEqual(code, 0, text)


if __name__ == "__main__":
    unittest.main()


class DifferencePageRuleTest(unittest.TestCase):
    """The rule for the commands of one board only, at the top of the sections of the difference page."""

    def sections(self, lang: str) -> dict[str, str]:
        ctx = generate.Ctx(SPEC, lang, "both", Counter(), [])
        text = generate.page_diff(ctx)
        parts = re.split(r"^## ", text, flags=re.M)[1:]
        return {p.split("\n", 1)[0]: p.split("\n", 1)[1] for p in parts}

    def only_sections(self, lang: str) -> tuple[str, str]:
        sec = self.sections(lang)
        key = "Commands available on {} only" if lang == "en" else "{}のみで使えるコマンド"
        return sec[key.format("STEP400")], sec[key.format("STEP800")]

    def test_the_rule_opens_the_section_that_has_commands(self):
        s400, _ = self.only_sections("en")
        first = s400.strip().split("\n")[0]
        self.assertIn("do not exist on the other board", first)
        self.assertIn("[`/error/osc`](automatically-sent-messages.md#error-osc) `MessageNotMatch`", first)
        self.assertIn("executes nothing", first)
        self.assertIn("(system-settings.md#reporterror)", first)
        s400, _ = self.only_sections("ja")
        first = s400.strip().split("\n")[0]
        self.assertIn("もう一方のボードにはありません", first)
        self.assertIn("(automatically-sent-messages.md#error-osc)で`MessageNotMatch`を返し", first)

    def test_the_exception_of_the_routed_command_is_named(self):
        for lang, word in (("en", "is the exception"), ("ja", "例外")):
            s400, _ = self.only_sections(lang)
            self.assertIn(word, s400.split("\n- ")[0])

    def test_a_section_without_commands_has_no_rule(self):
        for lang in ("en", "ja"):
            _, s800 = self.only_sections(lang)
            self.assertEqual(s800.strip(), "None." if lang == "en" else "なし。")
