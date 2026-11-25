"""mkdocs hooks (mkdocs.yml: hooks:). One search index per language.

mkdocs-static-i18n builds one search/search_index.json with every language in it. Material reads the index from
<base>/search/search_index.json and opens a result at <base>/<location>. So:

* on_post_page: in a page of a non-default language (en/...), "base" in the __config script is changed from the
  site root to that language's root (en/). Only that value changes (the assets are read through base_url, not base).
* on_post_build: the index is split. site/search/search_index.json keeps the default language (no prefix);
  site/en/search/search_index.json gets the English entries, with `location` relative to en/.
  Both indexes get a `config.separator` set here: EN_SEPARATOR (the plugin's, plus "/") for English, JA_SEPARATOR for Japanese.

Runs for both mkdocs.yml and mkdocs.preview.yml (it inherits `hooks`).
"""
import json
import re
from pathlib import Path

from mkdocs.plugins import event_priority

# Search separator of the Japanese index. Material splits the text of the index into words with the separator, then cuts
# Japanese words with TinySegmenter. A search query, however, is cut only with the separator (and, for runs of kanji, by
# the words of the index), never with TinySegmenter. So "電磁ブレーキ" in a query stays one word while the index has
# "電磁" and "ブレーキ", and nothing is found. The separator is applied to both sides, so it also cuts where the kind of
# character changes between katakana, kanji and ASCII letters/digits: "電磁|ブレーキ", "設定|ファイル", "microSD|カード".
# Hiragana is not a boundary (a particle would become a word of its own). Zero-width cuts need a lookbehind (Chrome,
# Firefox, Safari 16.4+; in older Safari the Japanese search does not start at all, the English one is not affected). The patterns are also valid in Python's re (tests/test_search_index.py uses that).
# "/" is a separator in both languages, so that "/setSpeedProfile" (an OSC address, as written in the pages) finds the same
# as "setSpeedProfile". The Japanese index also cuts at the middle dot "・" (U+30FB) and its half-width form "･" (U+FF65):
# "オン・オフ" -> "オン", "オフ".
EN_SEPARATOR = r"[\s\-/]+"
_KATAKANA = r"\u30A0-\u30FF"
_KANJI = r"\u3400-\u4DBF\u4E00-\u9FFF\u3005"
_ASCII = r"A-Za-z0-9"
JA_SEPARATOR = "|".join([
    r"[\s\-/\u30FB\uFF65]+",  # the plugin's own separator, "/", and the middle dots
    rf"(?<=[{_KATAKANA}])(?=[{_KANJI}{_ASCII}])",
    rf"(?<=[{_KANJI}])(?=[{_KATAKANA}{_ASCII}])",
    rf"(?<=[{_ASCII}])(?=[{_KATAKANA}{_KANJI}])",
])

_CONFIG_BASE = re.compile(r'(<script id="__config" type="application/json">\{[^<]*?"base": ")([^"]*)(")')


def _non_default_locales(config):
    i18n = config.plugins.get("i18n")
    if i18n is None:
        return []
    return [lang.locale for lang in i18n.config.languages if not lang.default and lang.build]


def _locale_of(page_url, locales):
    for loc in locales:
        if page_url.startswith(loc + "/"):
            return loc
    return None


def on_post_page(output, page, config):
    loc = _locale_of(page.file.url, _non_default_locales(config))
    if loc is None:
        return output
    # base is relative to the page: "../.." (two levels deep) -> the language root is one level less: "..".
    def fix(m):
        base = m.group(2)
        root = base[:-3] if base.endswith("/..") else "."  # ".." -> "."
        return m.group(1) + root + m.group(3)

    new, n = _CONFIG_BASE.subn(fix, output, count=1)
    if n != 1:
        raise RuntimeError(f"mkdocs_hooks: no __config base in {page.file.url}")
    return new


@event_priority(-100)  # after the i18n plugin has rebuilt the index in its own on_post_build
def on_post_build(config):
    locales = _non_default_locales(config)
    site = Path(config["site_dir"])
    src = site / "search" / "search_index.json"
    index = json.loads(src.read_text(encoding="utf-8"))
    default_docs = []
    by_locale = {loc: [] for loc in locales}
    for doc in index["docs"]:
        loc = _locale_of(doc["location"], locales)
        if loc is None:
            default_docs.append(doc)
        else:
            by_locale[loc].append({**doc, "location": doc["location"][len(loc) + 1:]})
    # The default language (no prefix) is Japanese here; JA_SEPARATOR is for that index, EN_SEPARATOR for the English ones.
    # config.lang stays ['en', 'ja'] in both: with ['en'] or ['ja'] alone, "setSpeedProfile" is not found any more.
    default_config = {**index["config"], "separator": JA_SEPARATOR}
    en_config = {**index["config"], "separator": EN_SEPARATOR}
    outputs = [(src, default_docs, default_config)]
    for loc, docs in by_locale.items():
        outputs.append((site / loc / "search" / "search_index.json", docs, en_config))
    for path, docs, cfg in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({**index, "config": cfg, "docs": docs}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
