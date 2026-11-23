"""The network values of the quick start (docs/en and docs/ja getting-started/quickstart.md).

    python -m unittest discover -s tests -v

The quick start gives the network values as numbers, so that a reader can type them. They are the
initial values of the firmware (`network` in spec/osc-commands.yaml) for ID 1. This test fails when
a number of the page differs from the value calculated from the YAML.

In the page, each value of the table is followed by a comment `<!-- qs-network: name -->`.
"""

import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

ID = 1  # the DIP switch of the quick start

MARK = re.compile(r"([0-9][0-9.]*)\s*<!-- qs-network: (\w+) -->")


def expected():
    spec = yaml.safe_load((ROOT / "spec" / "osc-commands.yaml").read_text(encoding="utf-8"))
    d = {s["key"]: s for s in spec["settings"]}

    def default(key):
        s = d[key]
        # the quick start is for a board without a card: the initial value of the firmware, not the template
        assert "template" not in s or s["template"] == s["default"], f"{key}: the template differs from the default"
        return s["default"]

    ip = lambda a: ".".join(str(x) for x in a)
    my_ip = list(default("network.myIp"))
    assert default("network.isMyIpAddId") is True
    my_ip[3] += ID
    assert default("network.isOutPortAddId") is True
    return {
        "boardIp": ip(my_ip),
        "pcIp": ip(default("network.destIp")),
        "subnet": ip(default("network.subnet")),
        "boardPort": str(default("network.inPort")),
        "pcPort": str(default("network.outPort") + ID),
    }


class QuickstartNetworkTest(unittest.TestCase):
    def test_values_match_the_yaml(self):
        want = expected()
        for lang in ("en", "ja"):
            page = ROOT / "docs" / lang / "getting-started" / "quickstart.md"
            text = page.read_text(encoding="utf-8")
            found = {name: value for value, name in MARK.findall(text)}
            self.assertEqual(found, want, f"{page.relative_to(ROOT)}")

    def test_every_address_and_port_on_the_page_is_one_of_them(self):
        want = expected()
        ips = {want["boardIp"], want["pcIp"], want["subnet"]}
        ports = {want["boardPort"], want["pcPort"]}
        for lang in ("en", "ja"):
            page = ROOT / "docs" / lang / "getting-started" / "quickstart.md"
            # outside the code of the links
            text = re.sub(r"\]\([^)]*\)|https?://\S+", "", page.read_text(encoding="utf-8"))
            for ip in re.findall(r"(?<![\d.])\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?![\d.])", text):
                self.assertIn(ip, ips, f"{page.relative_to(ROOT)}: {ip}")
            for port in re.findall(r"(?<![\d.])\d{5}(?![\d.])", text):
                self.assertIn(port, ports, f"{page.relative_to(ROOT)}: {port}")


if __name__ == "__main__":
    unittest.main()
