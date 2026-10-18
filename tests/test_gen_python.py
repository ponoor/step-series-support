"""Tests of tools/gen_python.py and tools/migrate_python_docs.py.

    python -m unittest discover -s tests -v

They generate into a temporary directory (no python-step-series checkout needed) and read the generated
modules with `ast`, so python-osc does not have to be installed.
"""

import ast
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import gen_python as gp  # noqa: E402
import migrate_python_docs as mig  # noqa: E402
from spec import Spec  # noqa: E402

SPEC = Spec.load()
COMPAT = yaml.safe_load(gp.COMPAT_PATH.read_text(encoding="utf-8"))


def generate_into(lib: Path) -> dict:
    (lib / "src" / "stepseries").mkdir(parents=True)
    out = gp.generate(SPEC, lib)
    return {p.name: text for p, text in out.items()}


def classes(source: str) -> dict:
    """{class name: {"bases": [...], "fields": [...], "address": str | None}}"""
    out = {}
    for node in ast.parse(source).body:
        if isinstance(node, ast.ClassDef):
            fields, address = [], None
            for n in node.body:
                if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
                    fields.append(n.target.id)
                    if n.target.id == "address" and isinstance(n.value, ast.Call):
                        address = n.value.keywords[0].value.value
            out[node.name] = {"bases": [ast.unparse(b) for b in node.bases], "fields": fields, "address": address}
    return out


class TestGenerate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.lib = Path(cls.tmp.name)
        cls.out = generate_into(cls.lib)
        cls.cmds = classes(cls.out["commands.py"])
        cls.msgs = classes(cls.out["responses.py"])

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_modules_parse_and_say_they_are_generated(self):
        for name, text in self.out.items():
            ast.parse(text)
            self.assertTrue(text.startswith("# This file is generated. Do not edit it directly."), name)

    def test_second_run_gives_the_same_text(self):
        with tempfile.TemporaryDirectory() as d:
            again = generate_into(Path(d))
        self.assertEqual(again, self.out)

    def test_every_address_has_one_class(self):
        by_addr = {v["address"]: k for k, v in self.cmds.items() if v["address"]}
        self.assertEqual(sorted(by_addr), sorted(c["address"] for c in SPEC.commands))
        by_addr = {v["address"]: k for k, v in self.msgs.items() if v["address"]}
        self.assertEqual(sorted(by_addr), sorted(m["address"] for m in SPEC.messages))

    def test_existing_class_names_are_kept(self):
        for addr, entry in COMPAT["commands"].items():
            self.assertEqual(self.cmds[entry["class"]]["address"], addr)
        for addr, entry in COMPAT["messages"].items():
            self.assertEqual(self.msgs[entry["class"]]["address"], addr)

    def test_existing_kinds_are_kept(self):
        for addr, entry in COMPAT["commands"].items():
            base = self.cmds[entry["class"]]["bases"]
            self.assertEqual(base, [f"OSC{entry['kind']}Command"], addr)

    def test_new_names_follow_the_address(self):
        self.assertIn("CombineGoTo", self.cmds)
        self.assertIn("SetAccRaw", self.cmds)
        self.assertIn("GetBrakeStatus", self.cmds)
        self.assertEqual(self.cmds["SaveConfig"]["bases"], ["OSCGetCommand"])
        self.assertEqual(self.msgs["ErrorSaveConfig"]["bases"], ["OSCResponse", "Exception"])
        self.assertEqual(self.msgs["ErrorCommand"]["bases"], ["OSCResponse", "Exception"])

    def test_fields(self):
        self.assertEqual(self.cmds["SetTval"]["fields"], ["address", "motorID", "holdTVAL", "runTVAL", "accTVAL", "setDecTVAL"])
        self.assertEqual(self.cmds["SetTargetPositionList"]["fields"][:3], ["address", "position1", "position2"])
        self.assertEqual(self.cmds["SetTargetPositionList"]["fields"][-1], "position8")
        self.assertEqual(self.msgs["Booted"]["fields"], ["address", "deviceID", "resetCause"])
        self.assertEqual(self.msgs["DestIP"]["fields"][1:5], ["destIp0", "destIp1", "destIp2", "destIp3"])
        self.assertEqual(self.msgs["ErrorOSC"]["fields"], ["address", "errorText", "motorID"])
        self.assertEqual(self.cmds["EnableBusyReport"]["fields"], ["address", "response_cls", "motorID", "enable", "callback"])

    def test_optional_arguments_have_a_default(self):
        text = self.out["responses.py"]
        self.assertIn("resetCause: int = None", text)
        self.assertIn("configFilename: str = None", text)
        self.assertIn("position5: int = None", text)
        self.assertNotIn("position4: int = None", text)

    def test_no_argument_table_in_the_docstrings(self):
        # The argument tables are added from the YAML by the Sphinx extension
        for text in self.out.values():
            self.assertNotIn("Valid Range", text)
            self.assertNotIn("STEP400|1-4", text)

    def test_step400_only_list_follows_the_yaml(self):
        tree = ast.parse(self.out["commands.py"])
        node = next(n for n in tree.body if isinstance(n, ast.AnnAssign) and n.target.id == "STEP400_ONLY")
        names = [e.id for e in node.value.elts]
        expected = [c["address"] for c in SPEC.commands if "STEP800" not in SPEC.boards_of(c)]
        self.assertEqual([self.cmds[n]["address"] for n in names], expected)
        self.assertIn("SetTval", names)
        self.assertNotIn("SetMicrostepMode", names)

    def test_timing_table(self):
        self.assertIn("|Executable Timing|Always|", self.out["commands.py"])

    def test_names_are_checked(self):
        self.assertEqual(gp.Gen(SPEC, COMPAT, {}).check_names(), [])


class TestText(unittest.TestCase):
    refs = {"/getBusy": "stepseries.commands.GetBusy"}

    def test_markdown_to_rst(self):
        self.assertEqual(gp.md_to_rst("Use `x` or [[/getBusy]].", self.refs),
                         "Use ``x`` or :py:class:`~stepseries.commands.GetBusy`.")
        self.assertEqual(gp.md_to_rst("see [[/unknown]]", self.refs), "see ``/unknown``")
        self.assertEqual(gp.md_to_rst("a ``b`` c", self.refs), "a ``b`` c")
        self.assertEqual(gp.md_to_rst("ends_ here", self.refs), "ends\\_ here")
        self.assertEqual(gp.md_to_rst("snake_case stays", self.refs), "snake_case stays")

    def test_wrap_does_not_start_a_line_with_a_list_marker(self):
        text = " ".join(["word"] * 17 + ["-", "next", "1.", "x"])
        for line in gp.wrap_paragraph(text).split("\n"):
            self.assertFalse(line.startswith(("- ", "1. ")), line)
            self.assertLessEqual(len(line), gp.WRAP + 6)

    def test_grid_table(self):
        self.assertEqual(gp.grid_table([["Executable Timing", "Always"]]),
                         "+-----------------+------+\n|Executable Timing|Always|\n+-----------------+------+")

    def test_paragraphs_and_tables(self):
        text = "One.\n\n+--+\n|a |\n+--+\n\n.. _x: http://example.com"
        blocks = gp.paragraphs(text)
        self.assertEqual([gp.is_table(b) for b in blocks], [False, True, False])
        self.assertTrue(gp.is_target(blocks[2]))

    def test_recall(self):
        self.assertGreaterEqual(gp.recall("Sets the speed.", "It sets the speed of the motor."), 0.9)
        self.assertLess(gp.recall("Something else entirely.", "It sets the speed of the motor."), 0.5)

    def test_docstring_is_escaped(self):
        lines = gp.py_doc(['a \\ b """ c'], "")
        self.assertEqual(ast.literal_eval("\n".join(lines)), 'a \\ b """ c')


class TestMigrate(unittest.TestCase):
    def test_literal_roundtrip(self):
        text = 'line one\n  indented "quoted" \\ back\nlast'
        src = "(" + " ".join(mig.literal(text)) + ")"
        self.assertEqual(ast.literal_eval(src), text)


if __name__ == "__main__":
    unittest.main()
