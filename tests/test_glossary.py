"""Tests of the Japanese wording checks in tools/validate_spec.py.

    python -m unittest discover -s tests -v
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import validate_spec  # noqa: E402

GLOSSARY = {
    "terms": [
        {"use": "解放", "avoid": ["開放"]},
        {"use": "返信", "avoid": ["応答", "報告"], "allow": ["ARPの応答"]},
        {"use": "速度", "avoid": ["最大速さ", "速さ"]},
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


class FilesTest(unittest.TestCase):
    def test_glossary_file_loads(self):
        g = validate_spec.load_glossary()
        self.assertTrue(g["terms"])
        self.assertTrue(g["spacing"]["no_space_between_ascii_and_ja"])

    def test_generate_py_texts_expand_placeholders(self):
        texts = dict(validate_spec.generate_py_texts())
        self.assertTrue(any("のみ" in t for t in texts.values()))
        self.assertFalse(any("{boards}" in t for t in texts.values()))


if __name__ == "__main__":
    unittest.main()
