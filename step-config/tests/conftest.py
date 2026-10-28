"""Fixtures: the page, the fake board behind the serial shim, dialogs and console errors."""
import json
import pathlib
import re
import sys
import time

import pytest
from playwright.sync_api import sync_playwright, expect

from testlib import HERE, TOOL, TEMPLATES, OUT, SHIM, FakeBoard, Card  # noqa: E402
from serial_backend import SerialBackend  # noqa: E402

_results = []


def pytest_configure(config):
    for d in ('screens', 'logs', 'downloads'):
        (OUT / d).mkdir(parents=True, exist_ok=True)


def pytest_runtest_logreport(report):
    if report.when == 'call' or (report.when in ('setup', 'teardown') and report.outcome != 'passed'):
        _results.append(dict(nodeid=report.nodeid, when=report.when, outcome=report.outcome,
                             wasxfail=getattr(report, 'wasxfail', None),
                             rows=getattr(report, '_rows', [])))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    out = yield
    rep = out.get_result()
    rep._rows = [str(a) for m in item.iter_markers('checklist') for a in m.args]


def pytest_sessionfinish(session, exitstatus):
    with open(OUT / 'checklist_results.json', 'w') as f:
        json.dump(_results, f, indent=1)


def _slug(s):
    return re.sub(r'[^A-Za-z0-9_.-]+', '_', s)


# --------------------------------------------------------------------- browsers
@pytest.fixture(scope='session')
def pw():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope='session')
def chromium(pw):
    b = pw.chromium.launch()
    yield b
    b.close()


@pytest.fixture(scope='session')
def webkit(pw):
    b = pw.webkit.launch()
    b.name_ = 'webkit'
    yield b
    b.close()


@pytest.fixture(scope='session')
def firefox(pw):
    b = pw.firefox.launch()
    b.name_ = 'firefox'
    yield b
    b.close()


@pytest.fixture(scope='session', params=['firefox', 'webkit'])
def other_browser(pw, request):
    b = getattr(pw, request.param).launch()
    b.name_ = request.param
    yield b
    b.close()


# --------------------------------------------------------------------- the page
class Dialogs:
    """confirm() answers, in order. A dialog with no answer waiting is dismissed and counted as
    unexpected (the test fails at the end)."""

    def __init__(self):
        self.answers = []
        self.messages = []
        self.unexpected = []

    def handle(self, dialog):
        self.messages.append(dialog.message)
        if self.answers:
            ok = self.answers.pop(0)
            dialog.accept() if ok else dialog.dismiss()
        else:
            self.unexpected.append(dialog.message)
            dialog.dismiss()


class Env:
    def __init__(self, page, backend, board, name):
        self.page = page
        self.backend = backend
        self.board = board
        self.name = name
        self.dialogs = Dialogs()
        self.console_errors = []
        self.console_log = []
        self.allowed = []
        page.on('dialog', self.dialogs.handle)
        page.on('console', self._console)
        page.on('pageerror', lambda e: self.console_errors.append('pageerror: ' + str(e)))

    def _console(self, m):
        self.console_log.append((m.type, m.text))
        if m.type == 'error':
            self.console_errors.append(m.text)

    def allow_console_error(self, pattern):
        self.allowed.append(pattern)

    def expect_unplug(self):
        """Errors that come with a lost device: Chromium logs a refused WebSocket handshake
        (the backend refuses while 'unplugged'), and the pipe of the port stream rejects."""
        self.allow_console_error('WebSocket connection')
        self.allow_console_error('pageerror: The device has been lost')

    def unexpected_console_errors(self):
        return [e for e in self.console_errors if not any(p in e for p in self.allowed)]

    # ---- helpers
    def open(self, expand=True):
        self.page.goto(TOOL.as_uri())
        if expand:     # the panels start closed; fields in a closed <details> cannot be filled
            self.page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
        return self

    def status(self):
        return self.page.locator('#status-msg').inner_text()

    def err(self):
        el = self.page.locator('#err-banner')
        return el.inner_text() if el.is_visible() else ''

    def wait_status(self, text, timeout=8000):
        expect(self.page.locator('#status-msg')).to_contain_text(text, timeout=timeout)

    def wait_err(self, text, timeout=8000):
        expect(self.page.locator('#err-banner')).to_contain_text(text, timeout=timeout)

    def connect(self, wait_status='Config loaded from board'):
        self.page.click('#btn-connect')
        if wait_status:
            self.wait_status(wait_status)
        return self

    def val(self, sel):
        return self.page.locator(sel).input_value()

    def set(self, sel, value):
        self.page.fill(sel, str(value))

    def fn(self, name):
        """Set the save-file-name field (fires 'input' like typing)."""
        self.page.fill('#sd-filename', name)

    def fn_color(self):
        return self.page.eval_on_selector('#sd-filename', 'e => e.style.borderColor')

    def shot(self, name):
        p = OUT / 'screens' / f'{_slug(name)}.png'
        self.page.screenshot(path=str(p), full_page=True)
        return p

    def options(self, sel):
        return self.page.eval_on_selector_all(f'{sel} option', 'os => os.map(o => [o.value, o.textContent])')

    def visible_rows(self, table_sel):
        return self.page.eval_on_selector_all(f'{table_sel} tbody tr', 'rs => rs.map(r => r.cells[0].innerText.replace(/ \\?$/, ""))')

    def header_cells(self, table_sel):
        return self.page.eval_on_selector_all(f'{table_sel} thead th', 'hs => hs.map(h => h.innerText)')

    def load_file(self, path):
        self.page.set_input_files('#file-input', str(path))

    def download(self):
        with self.page.expect_download() as d:
            self.page.click('#btn-download')
        path = OUT / 'downloads' / _slug(self.name + '_' + d.value.suggested_filename)
        d.value.save_as(str(path))
        return d.value.suggested_filename, json.loads(path.read_text())


@pytest.fixture
def make_env(request, chromium):
    created = []

    def make(product='STEP400', *, scheme='light', browser=None, shim=True, board=None,
             viewport=(1500, 1000), **board_kwargs):
        name = _slug(request.node.name)
        brd = board or FakeBoard(product, **board_kwargs)
        backend = SerialBackend(brd, log_path=OUT / 'logs' / f'{name}.jsonl').start()
        ctx = (browser or chromium).new_context(accept_downloads=True, color_scheme=scheme,
                                                viewport={'width': viewport[0], 'height': viewport[1]})
        if shim:
            ctx.add_init_script(f'window.__SERIAL_WS_URL__ = {json.dumps(backend.url)};\n' + SHIM)
        page = ctx.new_page()
        env = Env(page, backend, brd, name)
        created.append((env, ctx, backend))
        return env

    yield make
    problems = []
    for env, ctx, backend in created:
        errs = env.unexpected_console_errors()
        if errs:
            problems.append('console errors: ' + '; '.join(errs[:5]))
        if env.dialogs.unexpected:
            problems.append('unexpected dialogs: ' + '; '.join(env.dialogs.unexpected[:3]))
        try:
            ctx.close()
        except Exception:
            pass
        backend.stop()
    if problems:
        pytest.fail(' | '.join(problems), pytrace=False)


@pytest.fixture
def env400(make_env):
    return make_env('STEP400')


@pytest.fixture
def env800(make_env):
    return make_env('STEP800')


# --------------------------------------------------------------------- real boards (pytest -m hw)
class Hw:
    """The two boards on the bench, a backup of each taken before the first change, and a place
    for results. At the end of the session both boards are put back (restore)."""

    def __init__(self, boards, backups):
        self.boards = boards
        self.backups = backups
        self.results = {}
        self.restores = {}

    def rec(self, key, value):
        self.results[key] = value

    def restore(self, board):
        import hw_protocol
        d = hw_protocol.restore(self.backups[board.product])
        board.refresh()
        board.osc_set_dest()
        self.restores[board.product] = d
        return d


@pytest.fixture(scope='session')
def hw():
    import hw_protocol
    boards = hw_protocol.find_boards()
    for p, b in boards.items():
        assert b.G['board']['firmwareVersion'] == [2, 2, 0], p
        assert b.T['board']['sdInitialized'] is True, p + ': no usable card'
    assert boards['STEP400'].my_ip != boards['STEP800'].my_ip
    # The reference state is the golden backup taken before the first change (out/golden_<product>.json);
    # a new backup of the state found now is saved too. If a run was cut off and left a change, the
    # board is put back to the golden state first.
    backups = {}
    for p, b in boards.items():
        golden = OUT / f'golden_{p}.json'
        if not golden.exists():
            import shutil
            shutil.copy(hw_protocol.backup(b), golden)
        else:
            hw_protocol.backup(b)
        backups[p] = str(golden)
    h = Hw(boards, backups)
    for p, b in boards.items():
        want = json.loads(open(backups[p]).read())['G']
        d = hw_protocol.diff(hw_protocol._strip_volatile(want), hw_protocol._strip_volatile(b.G))
        d = [x for x in d if 'canSendMsgBeforeDestIp' not in x]   # follows /setDestIp at run time
        if d or b.G['board']['configFilename'] != want['board']['configFilename']:
            h.results[f'found_changed_{p}'] = d
            h.restore(b)
        b.osc_set_dest()
    yield h
    errs = {}
    for p, b in boards.items():
        try:
            errs[p] = h.restore(b)
        except Exception as e:      # noqa: BLE001
            errs[p] = [f'restore failed: {e!r}']
    h.results['final_restore'] = errs
    with open(OUT / 'hw_results.json', 'w') as f:
        json.dump(h.results, f, indent=1, default=str)
    assert all(not v for v in errs.values()), errs


@pytest.fixture(params=['STEP400', 'STEP800'])
def board(hw, request):
    return hw.boards[request.param]


@pytest.fixture
def real(hw, make_env):
    """Factory: the tool in a browser, connected through the serial bridge to a real board.
    `env.dirty = True` makes the teardown put the board back (after the page let go of the port)."""
    import hw_protocol
    from serial_backend import SerialBridge
    made = []

    def make(product, scheme='light', viewport=(1500, 1000), settle=0.8):
        b = hw.boards[product]
        bridge = SerialBridge(b.device, resolver=lambda: b.find_again(25)['device'], settle=settle)
        env = make_env(product, scheme=scheme, board=bridge, viewport=viewport)
        env.hw, env.hws, env.dirty = b, hw, False
        made.append(env)
        return env

    yield make
    for env in made:
        try:
            env.page.context.close()
        except Exception:
            pass
        end = time.time() + 8
        while time.time() < end and hw_protocol.port_holders(env.hw.device):
            time.sleep(0.1)
        if env.dirty:
            d = hw.restore(env.hw)
            assert not d, d
