"""Tests of the hand-written pages in docs/en and docs/ja.

    python -m unittest discover -s tests -v
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# An absolute URL of a page of the old docs on ponoor.com (https://ponoor.com/en/docs/..., /ja/docs/..., /docs/...).
OLD_DOCS_URL = re.compile(r"https?://(?:www\.)?ponoor\.com/(?:(?:en|ja)/)?docs/[^\s)\"'>]*")


class DocsLinkTest(unittest.TestCase):
    def test_no_absolute_url_of_the_old_docs_pages(self):
        found = []
        for lang in ("en", "ja"):
            for page in sorted((ROOT / "docs" / lang).rglob("*.md")):
                for n, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
                    for m in OLD_DOCS_URL.finditer(line):
                        found.append(f"{page.relative_to(ROOT)}:{n}: {m.group(0)}")
        self.assertEqual(found, [], "link to the new pages with a relative link:\n" + "\n".join(found))


if __name__ == "__main__":
    unittest.main()
