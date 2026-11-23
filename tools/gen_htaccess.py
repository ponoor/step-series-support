#!/usr/bin/env python3
"""Make the .htaccess files of the redirects (old WordPress URLs -> the new site) in deploy/htaccess/.

    python tools/gen_htaccess.py            write the files
    python tools/gen_htaccess.py --check    write nothing; exit 1 if a file would change

Input: the table in docs/_redirects_map.md (92 rows) and the extra rules below (ALIASES, EXTRA).
`site_url` comes from mkdocs.yml; the new URL of a row is site_url + its `New URL` (`./` = the top).

Output (deploy/htaccess/):
  root-snippet.htaccess        for ~/web/ponoor.com/.htaccess, before "# BEGIN WordPress": the /en/docs/... redirects
  docs.htaccess                for ~/web/ponoor.com/docs/.htaccess: /docs/, /docs/step400/..., /docs/emb-step400/..., /docs/step100-200/...
  docs-step-series.htaccess    for ~/web/ponoor.com/docs/step-series/.htaccess: the old Japanese pages under /docs/step-series/...
  docs-preview.htaccess        for ~/web/ponoor.com/docs-preview/.htaccess: only the hand-over to WordPress (no redirects)
  root.htaccess.proposed       root.htaccess.current (the server on 2026-11-23) with root-snippet.htaccess put in
Every redirect is one 301 to the final page (no two-step redirect). What is not listed goes to WordPress.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MAP_PATH = REPO_ROOT / "docs" / "_redirects_map.md"
MKDOCS_PATH = REPO_ROOT / "mkdocs.yml"
OUT_DIR = REPO_ROOT / "deploy" / "htaccess"
ROOT_CURRENT = OUT_DIR / "root.htaccess.current"
WP_BEGIN = "# BEGIN WordPress"

SITE_PATH = "/docs/step-series/"          # where the new site is (the path of site_url)

# Old URLs that are not in the table. Each one is sent to the new page of the table row it leads to today
# (checked with `curl -I` on 2026-11-23: WordPress redirects it, or it still opens): alias -> old URL of a row.
# `/docs/step400/<x>` and `/en/docs/step400/<x>` are WordPress redirects to `.../step-series/<x>`;
# `.../setup/<x>` goes to `.../settings/<x>`.
_STEP400_PAGES = [
    "osc-command-reference/automatically-sent-messages-from-step-400/",
    "osc-command-reference/brake/",
    "osc-command-reference/homing/",
    "osc-command-reference/motor-control/",
    "osc-command-reference/speed-profile/",
]
_SETUP_PAGES = [
    "example-parameter-values-for-example-steppers/",
    "network-and-dip-switch/",
    "power-supply-and-motor/",
    "sensor-and-switch/",
    "setup-with-a-microsd-card/",
]
ALIASES: dict[str, str] = {
    # English
    "/en/docs/step400/": "/en/docs/step-series/",      # the QR code of the STEP400 (WordPress redirect id 2)
    **{f"/en/docs/step400/{p}": f"/en/docs/step-series/{p}" for p in _STEP400_PAGES},
    **{f"/en/docs/step-series/setup/{p}": f"/en/docs/step-series/settings/{p}" for p in _SETUP_PAGES},
    "/en/docs/step-series/osc-command-reference/absolute-position-management/":
        "/en/docs/step-series/osc-command-reference/position-management/",
    "/en/docs/step-series/osc-command-reference/home-limit-sensors/":
        "/en/docs/step-series/osc-command-reference/home-and-limit-sensers/",
    "/en/docs/step-series/osc-command-reference/motordriver-settings/":
        "/en/docs/step-series/osc-command-reference/motor-driver-settings/",
    # Japanese
    "/docs/step400/": "/docs/step-series/",             # WordPress redirect id 1
    **{f"/docs/step400/{p}": f"/docs/step-series/{p}" for p in _STEP400_PAGES + [
        "functional-description/homing-and-position-management/",
        "functional-description/servo-mode/",
        "functional-description/voltage-mode-and-current-mode/",
        "osc-command-reference/absolute-position-management/",
        "osc-command-reference/voltage-and-current-mode-settings/",
    ]},
    **{f"/docs/step-series/setup/{p}": f"/docs/step-series/settings/{p}" for p in _SETUP_PAGES},
    "/docs/en/step-series/settings/setup-with-a-microsd-card/":
        "/docs/step-series/settings/setup-with-a-microsd-card/",
    "/docs/step-series/osc-command-reference/motor-driver-settings/":
        "/docs/step-series/osc-command-reference/motordriver-settings/",
    "/docs/step-series/functional-description/homing-and-absolute-position-management/":
        "/docs/step-series/functional-description/homing-and-position-management/",
}

# Rules to a page of the new site that no old URL leads to: old URL -> New URL (as in the table).
EXTRA: dict[str, str] = {
    "/docs/": "./",           # the list page of WordPress
    "/en/docs/": "en/",
}


@dataclass(frozen=True)
class Rule:
    old: str          # path of the old URL, e.g. /en/docs/step-series/settings/
    target: str       # the absolute URL of the new page
    note: str         # where it comes from (a comment in the file)


def site_url() -> str:
    import yaml
    mk = yaml.safe_load(MKDOCS_PATH.read_text(encoding="utf-8"))
    url = str(mk["site_url"])
    if not url.endswith("/"):
        url += "/"
    return url


def map_rows() -> list[tuple[str, str, str]]:
    """[(language, old URL path, New URL)] of the table of docs/_redirects_map.md."""
    rows = []
    for line in MAP_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith(("| en ", "| ja ")):
            c = [x.strip().strip("`") for x in line.strip().strip("|").split("|")]
            rows.append((c[0], c[1], c[4]))
    return rows


def absolute(site: str, new_url: str) -> str:
    return site if new_url == "./" else site + new_url


def build_rules(site: str | None = None) -> tuple[list[Rule], list[str]]:
    """(rules, identities): identities are old URLs that are the new URL itself (no redirect)."""
    site = site or site_url()
    origin = site.split("/", 3)[0] + "//" + site.split("/", 3)[2]
    table = {old: absolute(site, new) for _lang, old, new in map_rows()}
    rules: list[Rule] = []
    identities: list[str] = []

    def add(old: str, target: str, note: str):
        if origin + old == target:
            identities.append(old)
        else:
            rules.append(Rule(old, target, note))

    for _lang, old, new in map_rows():
        add(old, absolute(site, new), "table")
    for old, via in ALIASES.items():
        add(old, table[via], "alias")
    for old, new in EXTRA.items():
        add(old, absolute(site, new), "extra")
    return sorted(rules, key=lambda r: r.old), sorted(identities)


def group(rule: Rule) -> tuple[str, str]:
    """(file, path relative to the directory of that file's .htaccess, without a leading or trailing slash)."""
    p = rule.old.rstrip("/") + "/"
    if p.startswith("/en/"):
        return "root-snippet.htaccess", p[1:].strip("/")
    if p.startswith(SITE_PATH):
        return "docs-step-series.htaccess", p[len(SITE_PATH):].strip("/")
    if p.startswith("/docs/"):
        return "docs.htaccess", p[len("/docs/"):].strip("/")
    raise ValueError(f"old URL outside /docs/ and /en/: {p}")


def pattern(rel: str) -> str:
    return "^" + re.sub(r"([.+?()\[\]{}|\\^$])", r"\\\1", rel) + "/?$"


FALLBACK = """\
# Anything that is not a file or a directory here goes to WordPress (its old-slug redirects and its 404 page).
# Without this, RewriteEngine On in this directory would hide the rules of the top-level .htaccess.
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
"""


def render(name: str, rules: list[Rule], identities: list[str], site: str) -> str:
    where = {
        "root-snippet.htaccess": "~/web/ponoor.com/.htaccess, before the WordPress block (the line BEGIN WordPress)",
        "docs.htaccess": "~/web/ponoor.com/docs/.htaccess",
        "docs-step-series.htaccess": "~/web/ponoor.com/docs/step-series/.htaccess",
    }[name]
    head = [f"# STEP series docs: old WordPress URLs -> the new site (301). Put this in {where}.",
            "# Generated by tools/gen_htaccess.py from docs/_redirects_map.md. Do not edit by hand.",
            ]
    if name == "root-snippet.htaccess":
        body = ["# BEGIN STEP series docs", "<IfModule mod_rewrite.c>", "RewriteEngine On"]
    else:
        body = ["<IfModule mod_rewrite.c>", "RewriteEngine On"]
    for r in rules:
        f, rel = group(r)
        if f != name:
            continue
        body.append(f"RewriteRule {pattern(rel)} {r.target} [NC,R=301,L]")
    for old in identities:
        if group(Rule(old, "", ""))[0] == name:
            body.append(f"# {old} is the top page of the new site: no redirect.")
    if name != "root-snippet.htaccess":
        body.append("")
        body += FALLBACK.rstrip("\n").split("\n")
    body.append("</IfModule>")
    if name == "root-snippet.htaccess":
        body.append("# END STEP series docs")
    return "\n".join(head + [""] + body) + "\n"


def render_preview() -> str:
    return "\n".join([
        "# STEP series docs, trial publication. Put this in ~/web/ponoor.com/docs-preview/.htaccess.",
        "# Generated by tools/gen_htaccess.py. Do not edit by hand. No old-URL redirects here (this is outside /docs/).",
        "<IfModule mod_rewrite.c>",
        "RewriteEngine On",
        FALLBACK.rstrip("\n"),
        "</IfModule>",
        "# Belt and braces with the <meta name=\"robots\" content=\"noindex\"> of every page.",
        "<IfModule mod_headers.c>",
        "Header set X-Robots-Tag \"noindex\"",
        "</IfModule>",
    ]) + "\n"


def render_proposed(snippet: str) -> str:
    current = ROOT_CURRENT.read_text(encoding="utf-8")
    i = current.index(WP_BEGIN)
    return current[:i] + snippet + "\n" + current[i:]


def generate() -> dict[Path, str]:
    site = site_url()
    rules, identities = build_rules(site)
    out = {n: render(n, rules, identities, site) for n in ("root-snippet.htaccess", "docs.htaccess", "docs-step-series.htaccess")}
    out["docs-preview.htaccess"] = render_preview()
    out["root.htaccess.proposed"] = render_proposed(out["root-snippet.htaccess"])
    return {OUT_DIR / n: t for n, t in out.items()}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="write nothing; exit 1 if a file would change")
    args = ap.parse_args(argv)
    bad = 0
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for path, text in generate().items():
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old != text:
            if args.check:
                print(f"would change {path.relative_to(REPO_ROOT).as_posix()}")
                bad += 1
            else:
                path.write_text(text, encoding="utf-8", newline="\n")
                print(f"changed {path.relative_to(REPO_ROOT).as_posix()}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
