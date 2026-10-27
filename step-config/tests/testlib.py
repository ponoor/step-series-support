import time
"""Shared constants and helpers for the tests."""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
TOOL = HERE.parent / 'index.html'
TEMPLATES = HERE.parent.parent / 'configGenerator'
OUT = HERE / 'out'
SHIM = (HERE / 'serial_shim.js').read_text()

from fake_board import Card, FakeBoard  # noqa: E402,F401

# computed colours of the tool's CSS variables (light theme)
RED = 'rgb(207, 34, 46)'        # --err  #cf222e
ORANGE = 'rgb(154, 103, 0)'     # --warn #9a6700
NORMAL = 'rgb(204, 204, 204)'   # --border #cccccc


def tmpl(product):
    return json.loads((TEMPLATES / f'configTemplate_{product.lower()}.json').read_text())


def card_cfg(product, name='cardname'):
    d = tmpl(product)
    d['information']['configName'] = name
    return json.dumps(d).encode()


def make_card(product='STEP400', state='fat32', files=None, name='cardname'):
    c = Card(state)
    if files is None:
        files = {'/config.txt': card_cfg(product, name)}
    for k, v in files.items():
        c.write(k, v if isinstance(v, bytes) else json.dumps(v).encode())
    return c


def sent_json(backend, mark):
    """The configuration JSON the page sent with `{` since `mark`, or None."""
    text = backend.sent(mark)
    i = text.find('{')
    return json.loads(text[i:]) if i >= 0 else None


def poll_until(fn, timeout=5.0, step=0.05):
    end = time.time() + timeout
    while time.time() < end:
        v = fn()
        if v:
            return v
        time.sleep(step)
    return fn()


def wait_boot(env, count, timeout=6):
    assert poll_until(lambda: env.board.boot_count >= count and env.board.up and env.backend.plugged, timeout), 'board did not restart'


