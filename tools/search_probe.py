#!/usr/bin/env python3
"""Probe the site search in a headless browser: type words into the Material search box and print the number of matching
pages and the top 5 page URLs. Not run in CI (needs Playwright and a browser).

    python tools/search_probe.py                       # serves site/ on a local port and probes it
    python tools/search_probe.py --site site-preview
    python tools/search_probe.py --url https://ponoor.com/docs-preview/step-series/
    python tools/search_probe.py --json out.json       # also write the results as JSON
    python tools/search_probe.py --words 電磁ブレーキ,設定ファイル   # Japanese pages only (override the word list)

Playwright is not a dependency of this repository. Install it where you like (pip install playwright), then either
`playwright install chromium` or give an existing Chromium with --browser or $SEARCH_PROBE_BROWSER.
"""
import argparse
import functools
import http.server
import json
import os
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

JA_WORDS = [
    # known not to work before the fix
    "電磁ブレーキ", "設定ファイル",
    # the same, split
    "電磁", "ブレーキ", "設定", "ファイル",
    # long katakana
    "ブラウザ設定ツール", "マイクロステップ", "スルーレート", "ウォッチドッグ", "ステッピングモータ",
    # kanji compounds
    "原点復帰", "過電流", "電源電圧", "電圧モード", "電流モード", "位置管理", "移行ガイド", "変更履歴",
    # mixed with alphanumerics
    "microSDカード", "HOMEスイッチ", "LIMITスイッチ", "DIPスイッチ", "STEP400", "/setSpeedProfile", "setSpeedProfile",
    # more words a reader may type (guards against regressions)
    "ファームウェア更新", "OSCメッセージ", "IPアドレス", "サーボモード", "ブレーキ解除", "アラーム", "5V電源",
    # katakana-only compounds that occur in the pages
    "スピードプロファイル", "モータドライバ", "ドライバライブラリ", "モーションコマンド", "マイクロステップモード", "シリアルポート",
    "ファームウェア", "トラブルシューティング", "ブロードキャスト", "データシート",
]
EN_WORDS = ["electromagnetic brake", "configuration file", "homing", "microSD", "setSpeedProfile"]


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve(directory):
    handler = functools.partial(_Quiet, directory=str(directory))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{httpd.server_address[1]}/"


READY = """() => { const m = document.querySelector('.md-search-result__meta');
                   return !!m && !!m.textContent.trim() && !/Initializ|初期化|Type to start|検索キーワードを入力/.test(m.textContent); }"""


def probe(page, start_url, word):
    page.goto(start_url, wait_until="networkidle")
    box = page.locator("input[data-md-component=search-query]")
    box.click()
    # Material drops what is typed before its search worker has the index; if nothing shows up, clear the box and type again.
    for attempt in range(4):
        page.wait_for_timeout(1000)
        box.fill("")
        box.type(word, delay=20)
        page.keyboard.press("End")  # Material listens to keyup; typing non-ASCII text sends none
        try:
            page.wait_for_function(READY, timeout=3000)
            break
        except Exception:
            pass
    # the worker answers every keystroke; wait until the answer stops changing
    last, same = None, 0
    while same < 4:
        page.wait_for_timeout(250)
        now = page.evaluate("document.querySelector('.md-search-result__list').innerText + document.querySelector('.md-search-result__meta').innerText")
        same = same + 1 if now == last else 0
        last = now
    meta = page.locator(".md-search-result__meta").inner_text().strip()
    # one <li> per page; its first link is the page, the others are sections of it
    urls = page.eval_on_selector_all(
        "li.md-search-result__item > a.md-search-result__link:first-child",
        "els => els.slice(0, 5).map(e => e.href)",
    )
    titles = page.eval_on_selector_all(
        "li.md-search-result__item > a.md-search-result__link:first-child",
        "els => els.slice(0, 5).map(e => (e.querySelector('h1,h2') || {}).textContent || '')",
    )
    total = page.eval_on_selector_all("li.md-search-result__item > a.md-search-result__link:first-child", "els => els.length")
    return {"word": word, "meta": meta, "pages": total, "top": [{"url": u, "title": t.strip()} for u, t in zip(urls, titles)]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--site", default="site", help="built site directory to serve (default: site)")
    ap.add_argument("--url", help="probe this site root instead (e.g. https://ponoor.com/docs-preview/step-series/)")
    ap.add_argument("--words", help="comma-separated words; replaces the lists (probed on the Japanese pages)")
    ap.add_argument("--en-words", help="comma-separated words for the English pages")
    ap.add_argument("--browser", default=os.environ.get("SEARCH_PROBE_BROWSER"), help="path of a Chromium executable")
    ap.add_argument("--json", help="write the results to this file")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("playwright is not installed (pip install playwright); it is not a dependency of this repository")

    httpd = None
    if args.url:
        root = args.url if args.url.endswith("/") else args.url + "/"
    else:
        httpd, root = serve((ROOT / args.site).resolve())
    ja_words = args.words.split(",") if args.words else JA_WORDS
    en_words = args.en_words.split(",") if args.en_words else ([] if args.words else EN_WORDS)

    results = {"root": root, "ja": [], "en": []}
    with sync_playwright() as p:
        kw = {"executable_path": args.browser} if args.browser else {}
        browser = p.chromium.launch(**kw)
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        for key, start, words in (("ja", root, ja_words), ("en", root + "en/", en_words)):
            for w in words:
                r = probe(page, start, w)
                results[key].append(r)
                print(f"[{key}] {w!r}: {r['meta']} | " + " ".join(t["url"].replace(root, "/") for t in r["top"]))
        browser.close()
    if httpd:
        httpd.shutdown()
    if args.json:
        Path(args.json).write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
