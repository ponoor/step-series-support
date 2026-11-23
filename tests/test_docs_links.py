"""Tests of the hand-written pages in docs/en and docs/ja.

    python -m unittest discover -s tests -v
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# An absolute URL of a page of the old docs on ponoor.com (https://ponoor.com/en/docs/..., /ja/docs/..., /docs/...).
OLD_DOCS_URL = re.compile(r"https?://(?:www\.)?ponoor\.com/(?:(?:en|ja)/)?docs/[^\s)\"'>]*")

# An image or file on WordPress (wp-content/, any host or form of the URL): the pages must not depend on it.
WORDPRESS_FILE_URL = re.compile(r"[^\s(\"'<]*wp-content/[^\s)\"'>]*", re.IGNORECASE)

# An image whose URL is outside the repository: ![alt](URL) or <img src="URL"> with http://, https:// or //.
EXTERNAL_IMAGE = re.compile(r"!\[[^\]]*\]\(\s*(?:https?:)?//[^\s)]*|<img\b[^>]*\bsrc\s*=\s*[\"']?(?:https?:)?//[^\s\"'>]*", re.IGNORECASE)


class DocsLinkTest(unittest.TestCase):
    def test_no_absolute_url_of_the_old_docs_pages(self):
        found = []
        for lang in ("en", "ja"):
            for page in sorted((ROOT / "docs" / lang).rglob("*.md")):
                for n, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
                    for m in OLD_DOCS_URL.finditer(line):
                        found.append(f"{page.relative_to(ROOT)}:{n}: {m.group(0)}")
        self.assertEqual(found, [], "link to the new pages with a relative link:\n" + "\n".join(found))

    def test_no_image_or_file_on_wordpress(self):
        found = []
        for lang in ("en", "ja"):
            for page in sorted((ROOT / "docs" / lang).rglob("*.md")):
                for n, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
                    for m in WORDPRESS_FILE_URL.finditer(line):
                        found.append(f"{page.relative_to(ROOT)}:{n}: {m.group(0)}")
        self.assertEqual(found, [], "put the file in docs/assets/ and link to it with a relative path:\n" + "\n".join(found))

    def test_no_external_image(self):
        found = []
        for lang in ("en", "ja"):
            for page in sorted((ROOT / "docs" / lang).rglob("*.md")):
                for n, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
                    for m in EXTERNAL_IMAGE.finditer(line):
                        found.append(f"{page.relative_to(ROOT)}:{n}: {m.group(0)}")
        self.assertEqual(found, [], "put the image in docs/assets/images/ and link to it with a relative path:\n" + "\n".join(found))


if __name__ == "__main__":
    unittest.main()
