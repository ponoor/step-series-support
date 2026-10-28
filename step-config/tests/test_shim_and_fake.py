"""Tests of the test harness itself: the Web Serial shim, the backend, and the fake board."""
import asyncio
import json

import pytest
from playwright.sync_api import expect
from websockets.sync.client import connect as ws_connect

from fake_board import FakeBoard, Card, MAX_CONFIG_FILENAME
from serial_backend import SerialBackend, SerialBridge
from testlib import make_card, card_cfg, tmpl


# ------------------------------------------------------------------ the shim
def js(env, code):
    return env.page.evaluate(code)


def test_shim_opens_once_and_closes(env400):
    env = env400.open()
    r = js(env, """async () => {
      const out = [];
      const port = await navigator.serial.requestPort();
      out.push([port.readable, port.writable]);
      await port.open({baudRate: 9600});
      out.push([port.readable instanceof ReadableStream, port.writable instanceof WritableStream]);
      try { await port.open({baudRate: 9600}); out.push('no error'); } catch (e) { out.push(e.name); }
      try { await port.open({}); } catch (e) { out.push(e.name); }
      const r = port.readable.getReader();
      try { await port.close(); out.push('closed with a locked reader'); } catch (e) { out.push(e.name); }
      r.releaseLock();
      await port.close();
      out.push([port.readable, port.writable]);
      out.push((await navigator.serial.getPorts()).length);
      return out;
    }""")
    assert r == [[None, None], [True, True], 'InvalidStateError', 'TypeError', 'TypeError', [None, None], 1]


def test_shim_lost_device_errors_the_read_and_nulls_the_streams(env400):
    env = env400.open()
    env.expect_unplug()
    js(env, """async () => {
      const port = await navigator.serial.requestPort();
      window.__p = port;
      await port.open({baudRate: 9600});
      window.__r = port.readable.getReader();
      window.__res = null;
      (async () => { try { while (true) { await window.__r.read(); } } catch (e) { window.__res = [e.name]; } })();
      window.__events = [];
      port.addEventListener('disconnect', () => window.__events.push('port'));
      navigator.serial.addEventListener('disconnect', () => window.__events.push('serial'));
    }""")
    env.backend.disconnect(stay_unplugged=True)
    env.page.wait_for_function('window.__res !== null')
    assert js(env, 'window.__res') == ['NetworkError']
    assert js(env, 'window.__events') == ['port', 'serial']
    assert js(env, 'window.__p.readable === null && window.__p.writable === null') is True
    # away: nothing listed, the dead object cannot be opened (NetworkError) or closed (InvalidStateError)
    assert js(env, 'navigator.serial.getPorts().then(p => p.length)') == 0
    assert js(env, 'window.__p.connected') is False
    assert js(env, "window.__p.open({baudRate: 9600}).then(() => 'opened', e => e.name)") == 'NetworkError'
    assert js(env, "window.__p.close().then(() => 'closed', e => e.name)") == 'InvalidStateError'
    # plugged again: a NEW object, listed by getPorts(), announced by a connect event
    env.backend.plug()
    js(env, "window.__connects = []; navigator.serial.addEventListener('connect', e => window.__connects.push(e.target === window.__serialShim.port))")
    js(env, '__serialShim.plugIn()')
    assert js(env, 'window.__connects') == [True]
    assert js(env, 'navigator.serial.getPorts().then(p => p.length === 1 && p[0] !== window.__p && p[0].connected)') is True
    ok = js(env, "navigator.serial.getPorts().then(p => p[0].open({baudRate: 9600}).then(() => 'opened', e => e.name))")
    assert ok == 'opened'


@pytest.mark.parametrize('chunk', [1, 3, 'whole'])
def test_pieces_arrive_as_sent_and_the_tool_assembles_lines(make_env, chunk):
    env = make_env('STEP800', chunk=chunk, noise=True).open().connect()
    assert env.status() == 'Config loaded from board'
    assert env.page.locator('#bi-product').inner_text() == 'STEP800'
    # pieces of 1 byte really are separate chunks in the record
    rx = env.backend.since(0, 'rx')
    if chunk == 1:
        assert max(len(e['data']) for e in rx) == 1
    if chunk == 'whole':
        assert any(len(e['data']) > 2000 for e in rx)
    assert any('[serial]' in x for t, x in env.console_log)       # the noise line was seen and ignored


def test_random_pieces_are_seeded(make_env):
    a = make_env('STEP400', seed=5).open().connect()
    b = make_env('STEP400', seed=5).open().connect()
    sa = [len(e['data']) for e in a.backend.since(0, 'rx')]
    sb = [len(e['data']) for e in b.backend.since(0, 'rx')]
    assert sa == sb and len(set(sa)) > 3


def test_second_page_is_refused_while_one_is_connected(make_env):
    env = make_env('STEP400').open().connect()
    other = env.page.context.new_page()
    other.goto(env.page.url)
    other.evaluate('window.__x = null')
    res = other.evaluate("""async () => { const p = await navigator.serial.requestPort();
        try { await p.open({baudRate: 9600}); return 'opened'; } catch (e) { return e.name; } }""")
    assert res == 'NetworkError'
    env.allow_console_error('WebSocket connection')
    other.close()


# ------------------------------------------------------------------ the backend
def test_backend_bridge_loop_url_echoes_bytes():
    pytest.importorskip('serial')
    b = SerialBackend(SerialBridge('loop://')).start()
    try:
        with ws_connect(b.url) as ws:
            ws.send(b'G')
            ws.send(b'hello\n')
            got = b''
            while len(got) < 7:
                got += ws.recv(timeout=3)
        assert got == b'Ghello\n'
        assert b.sent() == 'Ghello\n'
        assert [e['dir'] for e in b.entries if e['dir'] != 'ev'][:2] == ['tx', 'tx']
    finally:
        b.stop()


# ------------------------------------------------------------------ the fake board itself
def arun(coro):
    """asyncio.run() in a thread: the Playwright sync API keeps a loop running in the main one."""
    import threading
    box = {}

    def go():
        try:
            box['v'] = asyncio.run(coro)
        except BaseException as e:      # noqa: BLE001
            box['e'] = e
    t = threading.Thread(target=go)
    t.start()
    t.join(30)
    if 'e' in box:
        raise box['e']
    return box['v']


class Io:
    def __init__(self):
        self.out = bytearray()
        self.plugged = True
        self.dropped = 0

    async def write(self, data):
        self.out += data

    async def set_plugged(self, on):
        self.plugged = on

    async def drop_connection(self):
        self.dropped += 1


def run_board(board, script):
    """script(board, io) is a coroutine that sends bytes and sleeps."""
    async def main():
        io = Io()
        board.start()
        board.attach(io)
        await asyncio.sleep(0.01)
        io.out.clear()
        await script(board, io)
        await board.stop()
        return io
    return arun(main())


def lines(io):
    return [json.loads(l) for l in io.out.decode().splitlines() if l.startswith('{')]


def test_fake_G_and_T_shape():
    b = FakeBoard('STEP400', chunk='whole', emit_boot_lines=False)
    async def s(b, io):
        b.feed(b'GT')
        await asyncio.sleep(0.2)
    io = run_board(b, s)
    g, t = lines(io)
    assert list(g)[:3] == ['board', 'information', 'network']
    assert g['board'] == {'product': 'STEP400', 'numMotors': 4, 'firmwareVersion': [2, 2, 0],
                          'configFilename': '/config.txt'}
    assert list(g['driverSettings']) == ['homingAtStartup', 'homingDirection', 'homingSpeed', 'homeSwMode',
        'prohibitMotionOnHomeSw', 'limitSwMode', 'prohibitMotionOnLimitSw', 'goUntilTimeout', 'releaseSwTimeout',
        'stepMode', 'isCurrentMode', 'slewRate', 'electromagnetBrakeEnable', 'brakeTransitionDuration']
    assert 'currentMode' in g and 'reportLimitSwStatus' in g['alarmAndReport']
    assert t['board']['product'] == 'STEP400' and len(t['motors']) == 4
    assert all(m['ocd'] is False and m['stall'] is False for m in t['motors'])


def test_fake_step800_has_no_current_or_limit_keys():
    g = json.loads(FakeBoard('STEP800').config_json())
    assert 'currentMode' not in g
    assert 'limitSwMode' not in g['driverSettings'] and 'isCurrentMode' not in g['driverSettings']
    assert 'reportLimitSwStatus' not in g['alarmAndReport']
    assert g['board']['numMotors'] == 8 and len(g['voltageMode']['KVAL_RUN']) == 8


def test_fake_startup_file_order():
    def boot(files, state='fat32'):
        c = Card(state)
        for k, v in files.items():
            c.write(k, v if isinstance(v, bytes) else json.dumps(v).encode())
        b = FakeBoard('STEP400', card=c)
        return b
    mk = lambda name: tmpl('STEP400') | {'information': {'configName': name, 'configVersion': [1, 2], 'targetProduct': 'STEP400'}}
    # config.txt first, even if a *.json comes earlier in the alphabet
    b = boot({'/config.txt': mk('C'), '/a.json': mk('A')})
    assert (b.config_filename, b.config_name) == ('/config.txt', 'C')
    # without config.txt: the alphabetically first .json (case-insensitive)
    b = boot({'/zzz.json': mk('Z'), '/Abc.JSON': mk('A'), '/b.json': mk('B')})
    assert (b.config_filename, b.config_name) == ('/Abc.JSON', 'A')
    # hidden files are skipped; other extensions are skipped
    b = boot({'/._a.json': mk('X'), '/foo.txt': mk('T'), '/b.json': mk('B')})
    assert b.config_filename == '/b.json'
    # the first .json is invalid (no configVersion): no fallback to the next one
    bad = mk('bad'); del bad['information']['configVersion']
    b = boot({'/a.json': bad, '/b.json': mk('B')})
    assert not b.config_file_parse and b.config_name == 'Default' and b.config_filename == '/config.txt'
    # config.txt that is not JSON, but a valid json exists
    b = boot({'/config.txt': b'{ not json', '/b.json': mk('B')})
    assert b.config_filename == '/b.json' and b.config_file_parse
    # config.txt opens but does not parse and there is no json: open 1, parse 0
    b = boot({'/config.txt': b'{ not json'})
    assert b.config_file_open and not b.config_file_parse
    # exFAT and no card: no card
    assert not boot({'/config.txt': mk('C')}, 'exfat').sd_initialized
    assert not boot({'/config.txt': mk('C')}, 'none').sd_initialized
    # a name with spaces
    b = boot({'/My Config.json': mk('S')})
    assert b.config_filename == '/My Config.json'


def test_fake_filename_rules():
    async def s(b, io):
        for cmd in (b'Fnoslash.json\n', b'F/a.csv\n', b'F/\n', b'F/ok.JSON\n', b'F/' + b'y' * 80 + b'.json\n',
                    b'F/' + b'z' * 70 + b'\n'):
            b.feed(cmd)
            await asyncio.sleep(0.05)
    b = FakeBoard('STEP400', chunk='whole', emit_boot_lines=False)
    io = run_board(b, s)
    r = lines(io)
    assert r[0] == {'result': 'error', 'message': 'Filename must start with /'}
    assert r[1] == {'result': 'error', 'message': 'Filename must end with .json or .txt'}
    assert r[2]['message'] == 'Filename must start with /'                      # "/" alone: idx < 2
    assert r[3] == {'result': 'ok', 'configFilename': '/ok.JSON'}
    # 82 bytes sent: cut at 63 -> "/yyy..." without the ending -> must end with .json or .txt
    assert r[4]['message'] == 'Filename must end with .json or .txt'
    assert len(b.config_filename) <= MAX_CONFIG_FILENAME - 1


def test_fake_brace_overflow_and_timeout_and_garbage():
    async def s(b, io):
        b.feed(b'{' + b'x' * 4200)
        await asyncio.sleep(0.1)
        b.feed(b'{"a":')
        await asyncio.sleep(0.4)           # no end: timeout
        b.feed(b'G')
        await asyncio.sleep(0.1)
    b = FakeBoard('STEP400', chunk='whole', emit_boot_lines=False, brace_timeout=0.25)
    io = run_board(b, s)
    r = lines(io)
    assert r[0]['message'] == 'Buffer overflow'
    assert r[1]['message'] == 'Timeout'
    assert 'board' in r[2]                  # the board is alive and answers G again


def test_fake_brace_limit_is_4095_bytes():
    pad = lambda n: '{"information":{"configName":"' + 'a' * n + '"}}'
    async def s(b, io):
        b.feed(pad(4095 - len(pad(0))).encode())
        await asyncio.sleep(0.3)
        b.feed(pad(4096 - len(pad(0))).encode())
        await asyncio.sleep(0.3)
    b = FakeBoard('STEP400', chunk='whole', emit_boot_lines=False)
    io = run_board(b, s)
    r = lines(io)
    assert r[0]['result'] == 'ok'
    assert r[1]['message'] == 'Buffer overflow'


def test_fake_save_and_reboot_cycle():
    async def s(b, io):
        cfg = tmpl('STEP400')
        cfg['network']['myIp'] = [10, 0, 0, 110]
        cfg['information']['configName'] = 'cyc'
        b.feed(b'F/config.txt\n' + json.dumps(cfg, separators=(',', ':')).encode())
        await asyncio.sleep(0.4)
        assert b.running_my_ip == [10, 0, 0, 100]                     # not changed until the reboot
        b.feed(b'R')
        await asyncio.sleep(0.4)
        assert not b.up and io.dropped == 1 and not io.plugged
        await asyncio.sleep(0.8)
    b = FakeBoard('STEP400', chunk='whole', boot_time=0.5, emit_boot_lines=False)
    io = run_board(b, s)
    r = lines(io)
    assert r[0]['result'] == 'ok'
    assert r[1]['message'] == "Saved to SD. Reboot (send 'R') to apply."
    assert r[2]['message'] == 'Rebooting...'
    assert b.up and io.plugged and b.boot_count == 2
    assert b.running_my_ip == [10, 0, 0, 110] and b.config_name == 'cyc'
    data = b.card.read('/config.txt').decode()
    assert data.count('\n') == 1 and json.loads(data)['information']['configName'] == 'cyc'


def test_fake_boot_lines_and_write_fixtures(tmp_path):
    async def s(b, io):
        pass
    b = FakeBoard('STEP800', chunk='whole')
    async def main():
        io = Io()
        b.start()
        b.attach(io)
        await asyncio.sleep(0.05)
        await b.stop()
        return bytes(io.out)
    out = arun(main())
    assert out == b'myId:0\r\neth ok\r\n'
    b.write_fixtures(tmp_path)
    assert json.loads((tmp_path / 'STEP800_G.json').read_text())['board']['product'] == 'STEP800'
    assert json.loads((tmp_path / 'STEP800_T.json').read_text())['board']['product'] == 'STEP800'


def test_fake_legacy_spelling_only_when_the_file_is_read_at_start_up():
    """loadConfig.cpp reads goUnitlTimeout when goUntilTimeout is missing; receiveConfigJson() does not."""
    d = tmpl('STEP400')
    d['driverSettings']['goUnitlTimeout'] = [111, 222, 333, 444]
    del d['driverSettings']['goUntilTimeout']
    b = FakeBoard('STEP400', card=make_card(files={'/config.txt': d}))
    assert b.cfg['driverSettings']['goUntilTimeout'] == [111, 222, 333, 444]
    b._apply_sections({'driverSettings': {'goUnitlTimeout': [1, 2, 3, 4]}})
    assert b.cfg['driverSettings']['goUntilTimeout'] == [111, 222, 333, 444]


def test_fake_step800_default_overcurrent_is_7_after_the_template_fix():
    b = FakeBoard('STEP800')
    assert b.cfg['alarmAndReport']['OCThreshold'] == [7] * 8


def test_shim_close_with_locked_writer_fails_and_reader_cancel_keeps_the_writable(env400):
    env = env400.open()
    r = js(env, """async () => {
      const out = [];
      const port = await navigator.serial.requestPort();
      await port.open({baudRate: 9600});
      const w = port.writable.getWriter();                       // locked writable
      try { await port.close(); out.push('closed'); } catch (e) { out.push(e.name); }
      w.releaseLock();
      const rd = port.readable.getReader();
      await rd.cancel();                                         // the readable ends, nothing else
      out.push([port.readable, port.writable !== null]);
      try { await port.open({baudRate: 9600}); out.push('reopened'); } catch (e) { out.push(e.name); }
      await port.close();                                        // writable unlocked now
      out.push([port.readable, port.writable]);
      await port.open({baudRate: 9600});                         // works after a real close
      out.push('open again');
      await port.close();
      return out;
    }""")
    assert r == ['TypeError', [None, True], 'InvalidStateError', [None, None], 'open again']
    assert poll_until_conn_closed(env)


def poll_until_conn_closed(env):
    from testlib import poll_until
    return poll_until(lambda: env.backend._ws is None)


def test_shim_writable_close_ends_only_the_writable(env400):
    env = env400.open()
    r = js(env, """async () => {
      const port = await navigator.serial.requestPort();
      await port.open({baudRate: 9600});
      const w = port.writable.getWriter();
      await w.close();
      w.releaseLock();
      const out = [port.writable, port.readable instanceof ReadableStream];
      await port.readable.cancel().catch(() => {});
      await port.close();
      return out;
    }""")
    assert r == [None, True]
