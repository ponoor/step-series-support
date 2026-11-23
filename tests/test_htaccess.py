"""deploy/htaccess/*.htaccess (tools/gen_htaccess.py): up to date, every old URL has one 301 to a page that exists, no two-step redirects, no clash with the new site."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import gen_htaccess as g  # noqa: E402

SITE = g.site_url()
ORIGIN = SITE.split("/", 3)[0] + "//" + SITE.split("/", 3)[2]
SITE_PATH = "/" + SITE.split("/", 3)[3]          # /docs/step-series/
FILES = ("root-snippet.htaccess", "docs.htaccess", "docs-step-series.htaccess")
RULE_RE = re.compile(r"^RewriteRule (\S+) (\S+) \[NC,R=301,L\]$", re.M)


def parsed(name: str) -> list[tuple[str, str]]:
    return RULE_RE.findall((g.OUT_DIR / name).read_text(encoding="utf-8"))


def matches(old_path: str, upper: bool = False) -> list[tuple[str, str]]:
    """What Apache would do with an old URL: the rules of the .htaccess of its directory that match (case-insensitive)."""
    name, rel = g.group(g.Rule(old_path, "", ""))
    rel = rel.upper() if upper else rel
    return [(pat, tgt) for pat, tgt in parsed(name) if re.search(pat, rel, re.I) or (pat == "^/?$" and rel == "")]


def new_page_paths() -> set[str]:
    """Paths (under the site, no leading slash, with trailing slash; "" is the top) of the pages of the new site."""
    out = set()
    for lang in ("ja", "en"):
        for md in (ROOT / "docs" / lang).rglob("*.md"):
            rel = md.relative_to(ROOT / "docs" / lang).with_suffix("").as_posix()
            rel = "" if rel == "index" else rel[:-len("/index")] + "/" if rel.endswith("/index") else rel + "/"
            out.add(("en/" if lang == "en" else "") + rel)
    out.add("en/")
    return out


class HtaccessTest(unittest.TestCase):
    def test_files_are_up_to_date(self):
        for path, text in g.generate().items():
            self.assertTrue(path.exists(), path)
            self.assertEqual(path.read_text(encoding="utf-8"), text, f"{path.name}: run python tools/gen_htaccess.py")

    def test_every_row_and_extra_rule_once(self):
        rules, identities = g.build_rules()
        rows = g.map_rows()
        self.assertEqual(len(rows), 92)
        self.assertEqual(identities, ["/docs/step-series/"])          # the Japanese top page is the new top page
        olds = [r.old for r in rules]
        self.assertEqual(len(olds), len(set(olds)))
        for _lang, old, _new in rows:
            if old in identities:
                continue
            self.assertIn(old, olds)
        for old in list(g.ALIASES) + list(g.EXTRA):
            self.assertIn(old, olds)
        self.assertEqual(len(rules), len(rows) - 1 + len(g.ALIASES) + len(g.EXTRA))
        # in the files: one RewriteRule per rule, each old URL is matched by exactly one of them
        self.assertEqual(sum(len(parsed(n)) for n in FILES), len(rules))
        for r in rules:
            self.assertEqual(len(matches(r.old)), 1, r.old)
            self.assertEqual(matches(r.old)[0][1], r.target, r.old)
            self.assertEqual(len(matches(r.old.rstrip("/"))), 1, r.old + " (no trailing slash)")

    def test_aliases_lead_to_rows(self):
        table = {old for _l, old, _n in g.map_rows()}
        for alias, via in g.ALIASES.items():
            self.assertNotIn(alias, table, alias)
            self.assertIn(via, table, alias)

    def test_targets_exist(self):
        pages = new_page_paths()
        rules, _ = g.build_rules()
        for r in rules:
            self.assertTrue(r.target.startswith(SITE), r.target)
            self.assertIn(r.target[len(SITE):], pages, f"{r.old} -> {r.target}")

    def test_no_two_step_redirects(self):
        rules, _ = g.build_rules()
        olds = {r.old for r in rules}
        for r in rules:
            self.assertNotIn(r.target[len(ORIGIN):], olds, f"{r.old} -> {r.target} is redirected again")

    def test_no_clash_with_the_new_site(self):
        # an old URL under the new site must not be a page, a directory of pages, or a file of the new site
        pages = new_page_paths()
        taken = set()
        for p in pages:
            parts = p.strip("/").split("/") if p else []
            for i in range(1, len(parts) + 1):
                taken.add("/".join(parts[:i]))
        taken |= {"assets", "search", "sitemap.xml", "sitemap.xml.gz", "404.html", "llms.txt", "llms-full.txt", "en"}
        rules, _ = g.build_rules()
        for r in rules:
            if r.old.startswith(SITE_PATH):
                rel = r.old[len(SITE_PATH):].strip("/")
                self.assertNotIn(rel, taken, f"{r.old} is also a page or directory of the new site")
            self.assertNotEqual(r.old.rstrip("/") + "/", SITE_PATH, "a redirect of the top page loops")

    def test_wordpress_fallback(self):
        for n in ("docs.htaccess", "docs-step-series.htaccess", "docs-preview.htaccess"):
            text = (g.OUT_DIR / n).read_text(encoding="utf-8")
            self.assertIn("RewriteCond %{REQUEST_FILENAME} !-f\nRewriteCond %{REQUEST_FILENAME} !-d\nRewriteRule . /index.php [L]", text, n)
            self.assertNotIn("RewriteBase", text)
        # the fallback is after the 301 rules
        text = (g.OUT_DIR / "docs.htaccess").read_text(encoding="utf-8")
        self.assertLess(text.rindex("R=301"), text.index("!-f"))

    def test_root_proposed(self):
        cur = g.ROOT_CURRENT.read_text(encoding="utf-8")
        new = (g.OUT_DIR / "root.htaccess.proposed").read_text(encoding="utf-8")
        snippet = (g.OUT_DIR / "root-snippet.htaccess").read_text(encoding="utf-8")
        self.assertEqual(new.count(g.WP_BEGIN), 1)  # the comment of the snippet does not repeat the marker
        self.assertLess(new.index("BEGIN STEP series docs"), new.index(g.WP_BEGIN))
        self.assertEqual(new.replace(snippet + "\n", "", 1), cur)   # nothing else changed
        self.assertTrue(new.startswith(snippet))
        for keep in ("php_value memory_limit 128M", "SiteGuard_User_ExcludeSig", "RewriteRule . /index.php [L]"):
            self.assertIn(keep, new)


if __name__ == "__main__":
    unittest.main()
