"""Tests of the Japanese wording checks in tools/validate_spec.py.

    python -m unittest discover -s tests -v
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import validate_spec  # noqa: E402
from spec import Spec  # noqa: E402

GLOSSARY = {
    "terms": [
        {"use": "解放", "avoid": ["開放"]},
        {"use": "返信", "avoid": ["応答", "報告"], "allow": ["ARPの応答"]},
        {"use": "速度", "avoid": ["最大速さ", "速さ"]},
    ],
    "spacing": {"no_space_between_ascii_and_ja": True},
}


GLOSSARY_LEVELS = {
    "terms": [
        {"use": "解放", "avoid": ["開放"]},
        {"use": "保持", "level": "review", "avoid": ["保持"], "unless_sentence": ["ブレーキ"]},
        {"use": "無励磁", "level": "review", "avoid_regex": ["(?<![A-Za-z0-9/_])HiZ(?![A-Za-z0-9_])"]},
    ],
    "spacing": {"no_space_between_ascii_and_ja": True},
}


def check(text):
    return [(k, d) for k, d, _ in validate_spec.check_wording(text, GLOSSARY)]


class AvoidTest(unittest.TestCase):
    def test_avoid_word(self):
        self.assertEqual(check("ブレーキを開放します。"), [("avoid", "開放")])

    def test_allow_context(self):
        self.assertEqual(check("ARPの応答を待ちます。"), [])
        self.assertEqual(check("ARPの応答と、応答を待ちます。"), [("avoid", "応答")])

    def test_longer_word_of_the_same_term_counts_once(self):
        self.assertEqual(check("最大速さ"), [("avoid", "最大速さ")])

    def test_inline_code_and_links_are_skipped(self):
        self.assertEqual(check("`開放`と[[/報告]]とhttps://example.com/応答"), [])

    def test_code_block_comment_and_generated_block_are_skipped(self):
        text = "```\n開放\n```\n<!-- 開放 -->\n<!-- generated:begin osc /a -->\n開放\n<!-- generated:end osc /a -->\n"
        self.assertEqual(check(text), [])

    def test_line_number_survives_stripping(self):
        text = "```\na\nb\n```\nx\n開放\n"
        (_, _, line), = validate_spec.check_wording(text, GLOSSARY)
        self.assertEqual(line, 6)


class SpacingTest(unittest.TestCase):
    def test_space_between_ascii_and_japanese(self):
        self.assertEqual([k for k, _ in check("USB シリアル")], ["space"])
        self.assertEqual([k for k, _ in check("カードの JSON")], ["space"])
        self.assertEqual([k for k, _ in check("STEP400 と STEP800")], ["space", "space"])

    def test_fullwidth_punctuation_counts_as_japanese(self):
        self.assertEqual([k for k, _ in check("5 ms（約")], [])
        self.assertEqual([k for k, _ in check("値（ A ）")], ["space", "space"])

    def test_ascii_to_ascii_is_not_checked(self):
        self.assertEqual(check("5 ms"), [])
        self.assertEqual(check("1 LSB"), [])
        self.assertEqual(check("STEP400: 0x1F"), [])
        self.assertEqual(check("a  b"), [])

    def test_inline_code_counts_as_ascii(self):
        self.assertEqual([k for k, _ in check("`/setDestIp` を送る")], ["space"])
        self.assertEqual([k for k, _ in check("送る `/setDestIp`")], ["space"])
        self.assertEqual([k for k, _ in check("[[/run]] の")], ["space"])
        self.assertEqual(check("`/setDestIp`を送る"), [])
        self.assertEqual(check("送る\n`/setDestIp`"), [])

    def test_space_inside_inline_code_is_ignored(self):
        self.assertEqual(check("`USB シリアル`"), [])


class LevelTest(unittest.TestCase):
    def kinds(self, text):
        return [(k, d) for k, d, _ in validate_spec.check_wording(text, GLOSSARY_LEVELS)]

    def test_default_level_is_error(self):
        self.assertEqual(self.kinds("ブレーキを開放"), [("avoid", "開放")])

    def test_review_level(self):
        self.assertEqual(self.kinds("モータの位置を保持する"), [("review", "保持")])

    def test_unless_sentence(self):
        self.assertEqual(self.kinds("ブレーキの保持。"), [])
        self.assertEqual(self.kinds("ブレーキの状態。位置を保持する。"), [("review", "保持")])

    def test_avoid_regex_skips_code_and_names(self):
        self.assertEqual(self.kinds("モータがHiZになる"), [("review", "HiZ")])
        self.assertEqual(self.kinds("`HiZ`とMotorNotHiZと/HiZ"), [])

    def test_space_between_japanese_characters(self):
        self.assertEqual([k for k, _ in self.kinds("モータは 無励磁 です")], ["space", "space"])
        self.assertEqual([k for k, _ in self.kinds("設定値については 電圧モード を参照")], ["space", "space"])
        self.assertEqual(self.kinds("モータは無励磁です"), [])


GLOSSARY_UNITS = {
    "terms": [],
    "spacing": {"no_space_between_ascii_and_ja": True,
                "units": ["ms", "mA", "A", "V/us", "step/s", "LSB", "microstep", "%"]},
}


class UnitSpacingTest(unittest.TestCase):
    def kinds(self, text):
        return [(k, d) for k, d, _ in validate_spec.check_wording(text, GLOSSARY_UNITS)]

    def test_japanese_sentence(self):
        self.assertEqual([k for k, _ in self.kinds("処理を約41 ms止めます")], ["space"])
        self.assertEqual([k for k, _ in self.kinds("0〜5 ms後と980 V/usと1 LSB")], ["space", "space", "space"])
        self.assertEqual(self.kinds("処理を約41ms止めます"), [])

    def test_range_unit(self):
        self.assertEqual([k for k, _ in self.kinds("0〜65535 msの範囲")], ["space"])

    def test_english_string_and_ja_without_japanese(self):
        self.assertEqual(self.kinds("It takes 5 ms."), [])
        self.assertEqual(self.kinds("5 ms"), [])

    def test_only_the_japanese_line_of_a_paragraph(self):
        self.assertEqual(len(self.kinds("English 5 ms\n\n日本語の5 ms")), 1)

    def test_generated_range_column_is_not_read(self):
        # "0-65535 ms" of the range / unit column is made by generate.py, in pages that are not checked
        where = [w for w, _ in validate_spec.japanese_texts()]
        self.assertFalse(any(w.endswith("connections/configuration-items.md") for w in where))

    def test_code_and_links_are_skipped(self):
        self.assertEqual(self.kinds("`5 ms`と[[/a 5 ms]]のこと"), [])

    def test_a_word_between_letters_and_digits_is_not_a_unit_space(self):
        self.assertEqual(self.kinds("TCC 375ns、ID 154、STEP400: 0x1Fの値"), [])
        self.assertEqual(self.kinds("1 Amp"), [])

    def test_value_name_with_a_fraction(self):
        self.assertEqual(self.kinds("Full-stepから1/16 microstepまで"), [])

    def test_percent(self):
        self.assertEqual([k for k, _ in self.kinds("約4.9 %小さく")], ["space"])


GLOSSARY_PAREN = {"terms": [{"use": "従って", "avoid": ["にしたがって"]}, {"use": "すべて", "avoid": ["全て"]}],
                  "spacing": {"no_space_between_ascii_and_ja": True, "fullwidth_parentheses": True}}


class ParenthesesTest(unittest.TestCase):
    def kinds(self, text):
        return [(k, d) for k, d, _ in validate_spec.check_wording(text, GLOSSARY_PAREN)]

    def test_halfwidth_parentheses_next_to_japanese(self):
        self.assertEqual(len(self.kinds("動作状態(MOT_STATUS)を取得")), 1)
        self.assertEqual(len(self.kinds("モータドライバ(PowerSTEP01/L6470)の")), 1)
        self.assertEqual(len(self.kinds("(Falling Edge)に自動で")), 1)

    def test_spaces_are_skipped_when_looking_for_the_neighbour(self):
        self.assertEqual(len(self.kinds("定電流制御モード (current mode) では")), 1)

    def test_fullwidth_and_english_are_fine(self):
        self.assertEqual(self.kinds("動作状態（MOT_STATUS）を取得"), [])
        self.assertEqual(self.kinds("see (the manual) for details"), [])

    def test_inline_code_is_not_changed(self):
        self.assertEqual(self.kinds("`f(x)`の値"), [])

    def test_pair_is_found_with_a_code_span_inside(self):
        self.assertEqual(len(self.kinds("現在位置(`ABS_POS`)を")), 1)

    def test_japanese_parens_returns_the_pairs(self):
        self.assertEqual(validate_spec.japanese_parens("状態(A)と b (c) d"), [(2, 4)])

    def test_words(self):
        self.assertEqual(self.kinds("プロファイルにしたがって"), [("avoid", "にしたがって")])
        self.assertEqual(self.kinds("全ての値"), [("avoid", "全て")])
        self.assertEqual(self.kinds("プロファイルに従って、すべての値"), [])


class ReviewedTest(unittest.TestCase):
    SPEC = Spec({"commands": [{"address": "/a", "description": {"en": "x", "ja": "モータの位置を保持する。ほかの文。"}}]})

    def run_(self, reviewed):
        return validate_spec.japanese_findings(self.SPEC, GLOSSARY_LEVELS, reviewed, files=False)

    def test_listed_without_record(self):
        findings, stale = self.run_([])
        self.assertEqual([(f["level"], f["word"], f["where"]) for f in findings], [("review", "保持", "commands[/a].description.ja")])
        self.assertEqual(stale, [])

    def test_reviewed_record_hides_the_finding(self):
        rec = {"where": "commands[/a].description.ja", "term": "保持", "text": "位置を保持する", "note": "ok"}
        findings, stale = self.run_([rec])
        self.assertEqual(findings, [])
        self.assertEqual(stale, [])

    def test_stale_record_is_reported_and_the_finding_comes_back(self):
        rec = {"where": "commands[/a].description.ja", "term": "保持", "text": "位置を保つ", "note": "old"}
        findings, stale = self.run_([rec])
        self.assertEqual(len(findings), 1)
        self.assertEqual(len(stale), 1)
        self.assertIn("stale", stale[0])

    def test_record_for_a_missing_place_is_stale(self):
        rec = {"where": "commands[/gone].description.ja", "term": "保持", "text": "x", "note": ""}
        self.assertEqual(len(self.run_([rec])[1]), 1)

    def test_error_level_is_never_hidden_by_a_record(self):
        spec = Spec({"commands": [{"address": "/a", "description": {"en": "x", "ja": "開放する"}}]})
        rec = {"where": "commands[/a].description.ja", "term": "開放", "text": "開放する", "note": ""}
        findings, _ = validate_spec.japanese_findings(spec, GLOSSARY_LEVELS, [rec], files=False)
        self.assertEqual([f["level"] for f in findings], ["error"])


class FilesTest(unittest.TestCase):
    def test_glossary_file_loads(self):
        g = validate_spec.load_glossary()
        self.assertTrue(g["terms"])
        self.assertTrue(g["spacing"]["no_space_between_ascii_and_ja"])
        self.assertTrue({t.get("level", "error") for t in g["terms"]} <= {"error", "review"})

    def test_reviewed_file_loads(self):
        self.assertIsInstance(validate_spec.load_reviewed(), list)

    def test_generate_py_texts_expand_placeholders(self):
        texts = dict(validate_spec.generate_py_texts())
        self.assertTrue(any("のみ" in t for t in texts.values()))
        self.assertFalse(any("{boards}" in t for t in texts.values()))


if __name__ == "__main__":
    unittest.main()
