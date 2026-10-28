"""C: the real tool (index.html in Chromium) with the real boards through the serial bridge.

pytest -m hw. Needs both boards (USB + Ethernet), cards in them, the motor power OFF. Nothing here
moves a motor: the tool only sends G T F { R, and the OSC addresses are those of
hw_protocol.OSC_ALLOWED. A test that changes a board sets `env.dirty`; the teardown then puts
the board back from the golden backup (after the page let go of the port).

While a page has the port the test does not open it (hw_protocol refuses: lsof). A reboot or an
unplug makes the port vanish; the bridge tells the page and, on the next open(), looks for the
same board again by its USB serial number.
"""
import copy
import json
import time

import pytest
from playwright.sync_api import expect

import hw_protocol as hp
import test_ui_fields as fields
import test_ui_versions as versions
from testlib import RED, ORANGE, NORMAL, poll_until, tmpl

pytestmark = pytest.mark.hw

AXES = {'STEP400': 4, 'STEP800': 8}
LONG_NAME = '/STEP400_test_with_a_long_file_name_0123456789.json'
assert len(LONG_NAME) <= 63


@pytest.fixture(autouse=True)
def _name(hw):
    hw.rec('_name', 'C')


@pytest.fixture(params=['STEP400', 'STEP800'])
def product(request):
    return request.param


def ready(real, product, scheme='light'):
    return real(product, scheme).open().connect()


def fn_color(env):
    return env.page.eval_on_selector('#sd-filename', 'e => getComputedStyle(e).borderColor')


def nothing_sent_on_save(env):
    m = env.backend.mark()
    env.page.click('#btn-save')
    time.sleep(0.4)
    return env.backend.sent(m)


def state(env):
    """Every input / select of the page, to compare two reads."""
    return [x for x in env.page.evaluate(
        "Array.from(document.querySelectorAll('input,select')).map(e => [e.id, e.type === 'checkbox' ? e.checked : e.value])")
        if x[0] != 'file-input']


def osc_ready(b, timeout=6):
    return b.osc_set_dest(timeout)


def osc_answers(b, timeout=3.0):
    t0 = time.monotonic()
    while time.monotonic() - t0 < timeout:
        if b.osc_query('/getVersion', timeout=0.3):
            return True
    return False


# ------------------------------------------------------------------ 1
@pytest.mark.checklist('1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '13.2', '11.3')
def test_connect_and_read(real, hw, product):
    env = ready(real, product)
    b = env.hw
    assert env.status() == 'Config loaded from board'
    assert env.page.locator('#btn-connect').inner_text() == '✕ Disconnect'
    for x in ('btn-read', 'btn-save', 'btn-reboot', 'btn-poll'):
        assert env.page.locator('#' + x).is_enabled(), x
    t = lambda i: env.page.locator(i).inner_text()
    assert t('#bi-product') == product
    assert t('#bi-fw') == '2.2.0'
    assert t('#bi-axes-fixed') == f'{AXES[product]} (from board)'
    cfgver = t('#bi-cfgver')
    assert cfgver in ('1.2', '-1.0')
    hw.rec(f'1.2 {product}', dict(cfgver=cfgver, target=t('#bi-target')))
    assert env.val('#bi-cfgname') == b.G['information']['configName']
    assert env.val('#sd-filename') == b.G['board']['configFilename']
    for tb in ('alarm', 'driver', 'speed', 'voltage', 'servo'):
        assert len(env.header_cells(f'#{tb}-tbl')) == AXES[product] + 1, tb
    first = state(env)
    env.set('#f-voltage-KVAL_RUN-0', 99)
    env.set('#bi-cfgname', 'changed')
    env.page.click('#btn-read')
    env.wait_status('Config loaded from board')
    time.sleep(0.3)
    assert state(env) == first
    assert 'firmware' not in env.status().lower()                    # 13.2
    env.shot(f'hw_{product}_light_connected')


@pytest.mark.checklist('11.2')
@pytest.mark.parametrize('scheme', ['light', 'dark'])
def test_screenshots_with_status(real, product, scheme):
    env = ready(real, product, scheme)
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text(product, timeout=5000)
    time.sleep(1.2)
    env.shot(f'hw_{product}_{scheme}_status')


@pytest.mark.checklist('1.1', '1.6')
def test_disconnect_and_connect_three_times(real, product):
    env = ready(real, product)
    for i in range(3):
        env.page.click('#btn-connect')
        env.wait_status('Disconnected')
        assert env.page.locator('#dc-banner').is_hidden()
        env.page.click('#btn-connect')
        env.wait_status('Config loaded from board')
    assert env.err() == ''


# ------------------------------------------------------------------ 2
@pytest.mark.checklist('2.1', '2.4', '2.5', '13.6', '3.8')
def test_status_panel_and_save_while_polling(real, hw, product):
    env = ready(real, product)
    env.dirty = True
    env.page.click('#btn-poll')
    rb = env.page.locator('#rt-board')
    expect(rb).to_contain_text(product, timeout=5000)
    txt = rb.inner_text()
    b = env.hw
    assert b.my_ip in txt and 'Link ON' in txt, txt
    badges = env.page.locator('#rt-board .badge')
    assert badges.nth(1).inner_text() == 'OK'
    assert badges.nth(2).inner_text() == 'Loaded'
    assert len(env.header_cells('#rt-motors table')) == AXES[product] + 1
    m = env.backend.mark()
    time.sleep(3.3)
    n = env.backend.sent(m).count('T')
    assert 2 <= n <= 5, n
    hw.rec(f'2.1 {product}', dict(board_text=txt, T_in_3_3s=n))
    # 13.6 (A's check against the real board)
    for label in ('OCD', 'Stall'):
        cells = env.page.locator(f'#rt-motors tbody tr:has(td:text-is("{label}")) td')
        assert cells.count() == AXES[product] + 1
        assert cells.nth(1).locator('.badge').inner_text() == 'not reported'
    # 2.4 / 3.8: three saves while the status is shown
    for _ in range(3):
        env.dialogs.answers = [False]
        env.page.click('#btn-save')
        env.wait_status('Saved to SD')
        assert env.err() == ''
        time.sleep(1.1)
    expect(rb).to_contain_text(product)
    # 2.5
    env.page.click('#btn-poll')
    assert env.page.locator('#btn-poll').inner_text() == '▶ Start Status'
    m = env.backend.mark()
    time.sleep(2.5)
    assert 'T' not in env.backend.sent(m)


# ------------------------------------------------------------------ 3
@pytest.mark.checklist('3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '10.1', '10.2')
def test_save_cancel_reboot_read_and_new_ip(real, hw, product):
    env = ready(real, product)
    env.dirty = True
    b = env.hw
    old_ip = b.my_ip
    new_last = 120
    new_ip = f'10.0.0.{new_last + b.my_id}'
    env.set('#net-myIp-3', new_last)
    env.set('#bi-cfgname', 'tooltest')
    env.page.check('#f-alarm-reportBUSY-0')
    env.dialogs.answers = [False]
    m = env.backend.mark()
    env.page.click('#btn-save')
    env.wait_status("✓ Saved to SD. Reboot (send 'R') to apply.")
    assert env.dialogs.messages == ['Config saved.\n\nReboot now to apply changes?']
    assert env.backend.sent(m).startswith(f'F{b.G["board"]["configFilename"]}\n{{')
    env.shot(f'hw_{product}_saved')
    # 3.3: still running at the old address; the new one does not answer
    osc_ready(b)
    assert osc_answers(b)
    sock = b.osc()
    sock.flush()
    hp.OscPort.send_to(new_ip, b.in_port, '/getVersion')
    assert not sock.collect(new_ip, 0.7)
    # 3.4: Read shows the saved values
    env.set('#net-myIp-3', 5)
    env.set('#bi-cfgname', 'x')
    env.page.click('#btn-read')
    env.wait_status('Config loaded from board')
    time.sleep(0.3)
    assert env.val('#net-myIp-3') == str(new_last)
    assert env.val('#bi-cfgname') == 'tooltest'
    assert env.page.locator('#f-alarm-reportBUSY-0').is_checked()
    # 3.5 / 10.1: Reboot, the tool closes by itself after the reply
    env.dialogs.answers = [True]
    m = env.backend.mark()
    env.page.click('#btn-reboot')
    env.wait_status('Board rebooted — click Connect to reconnect.', timeout=10000)
    assert env.page.locator('#btn-connect').inner_text() == '⬡ Connect'
    ents = env.backend.since(m)
    i_reply = next(i for i, e in enumerate(ents) if e['dir'] == 'rx' and 'Rebooting...' in e.text)
    i_close = next(i for i, e in enumerate(ents) if e['dir'] == 'ev' and e.text == 'close')
    assert i_reply < i_close                                   # 10.1: the reply first, then the port closes
    hw.rec(f'10.1 {product} tool', dict(reply_t=ents[i_reply]['t'], close_t=ents[i_close]['t']))
    # 3.6 / 10.2: Connect again (the bridge waits for the board to come back)
    env.page.click('#btn-connect')
    env.wait_status('Config loaded from board', timeout=30000)
    assert env.val('#net-myIp-3') == str(new_last)
    assert env.val('#bi-cfgname') == 'tooltest'
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text(new_ip, timeout=5000)
    env.page.click('#btn-poll')
    b.T['board']['myIp'] = [10, 0, 0, new_last + b.my_id]
    osc_ready(b)
    assert osc_answers(b)
    hw.rec(f'3.6 {product}', dict(old=old_ip, new=new_ip))
    env.page.click('#btn-connect')
    env.wait_status('Disconnected')


# ------------------------------------------------------------------ 4
@pytest.mark.checklist('4.1', '4.2', '4.3', '4.4', '4.5', '4.6', '4.7')
def test_file_names(real, hw, product):
    env = ready(real, product)
    env.dirty = True
    cfgname = env.hw.G['board']['configFilename']
    # 4.1 a long name that is allowed: saved, the saved-to name is that one
    env.fn(LONG_NAME)
    assert fn_color(env) == NORMAL
    env.dialogs.answers = [False]
    m = env.backend.mark()
    env.page.click('#btn-save')
    env.wait_status('Saved to SD')
    assert env.backend.sent(m).startswith(f'F{LONG_NAME}\n{{')
    # 4.2 / 4.3: refused by the tool, nothing is sent
    for name, msg, red in [('/' + 'x' * 58 + '.json', 'bytes long', True),
                           ('/' + 'x' * 60 + '.json', 'bytes long', True),
                           ('config.txt', 'must start with "/"', True),
                           ('/a.csv', 'must end with .json or .txt', True)]:
        env.fn(name)
        assert fn_color(env) == RED, name
        assert nothing_sent_on_save(env) == '', name
        assert msg in env.err(), (name, env.err())
        assert env.status() == 'Save failed'
    # 4.5 / 4.6: orange, confirmation, cancel sends nothing
    for name, text in [('/foo.txt', '.txt file other than /config.txt'), ('/.hidden.json', 'starts with "."')]:
        env.fn(name)
        assert fn_color(env) == ORANGE, name
        env.dialogs.answers = [False]
        assert nothing_sent_on_save(env) == ''
        assert text in env.dialogs.messages[-1]
    # 4.4 subfolder: cancel -> nothing; OK -> the board says SD open failed (the folder is not there)
    env.fn('/sub/test.json')
    assert fn_color(env) == ORANGE
    env.dialogs.answers = [False]
    assert nothing_sent_on_save(env) == ''
    assert env.status() == 'Save cancelled'
    env.dialogs.answers = [True]
    m = env.backend.mark()
    env.page.click('#btn-save')
    env.wait_err('Save failed: SD open failed')
    assert env.backend.sent(m).startswith('F/sub/test.json\n{')
    assert 'folder of the file name does not exist' in env.err()
    env.shot(f'hw_{product}_sd_open_failed')
    # the tool is not stuck: Read works
    env.page.click('#btn-read')
    env.wait_status('Config loaded from board')
    # 4.7 no warning for /config.txt and /ABC.JSON; /ABC.JSON is saved
    for name in ('/config.txt', '/ABC.JSON', '/abc.Json'):
        env.fn(name)
        assert fn_color(env) == NORMAL, name
    env.fn('/ABC.JSON')
    env.dialogs.answers = [False]
    m = env.backend.mark()
    env.page.click('#btn-save')
    env.wait_status('Saved to SD')
    assert env.dialogs.messages[-1] == 'Config saved.\n\nReboot now to apply changes?'
    assert env.backend.sent(m).startswith('F/ABC.JSON\n{')


@pytest.mark.checklist('4.9')
def test_load_json_with_spaces_and_save(real, hw, product, tmp_path):
    env = ready(real, product)
    env.dirty = True
    g = copy.deepcopy(env.hw.G)
    g.pop('board')
    g['information'] = dict(configName='spaced', configVersion=[1, 2], targetProduct=product)
    f = tmp_path / 'My Config.json'
    f.write_text(json.dumps(g))
    env.load_file(f)
    env.wait_status('Loaded from file: My Config.json')
    assert env.val('#sd-filename') == '/My Config.json'
    assert fn_color(env) == NORMAL
    env.dialogs.answers = [True]
    m = env.backend.mark()
    env.page.click('#btn-save')
    env.wait_status('Board rebooted', timeout=10000)
    assert env.backend.sent(m).startswith('F/My Config.json\n')
    env.page.click('#btn-connect')
    env.wait_status('Config loaded from board', timeout=30000)
    # config.txt is read first at start-up, so the spaced file is only a file on the card
    assert env.val('#sd-filename') == '/config.txt'
    assert env.val('#bi-cfgname') != 'spaced'


# ------------------------------------------------------------------ 6
SECTION6 = {
    'STEP800': ['test_step800_has_brake_fields', 'test_step800_has_no_current_mode_and_no_limit',
                'test_step800_slew_rate', 'test_step800_overcurrent_options',
                'test_step800_stall_threshold_options'],
    'STEP400': ['test_step400_has_limit_fields', 'test_step400_has_current_mode',
                'test_step400_has_brake_fields', 'test_step400_slew_rate',
                'test_step400_overcurrent_options', 'test_step400_stall_threshold_options',
                'test_step400_tval_options'],
}


@pytest.mark.checklist('6.1', '6.2', '6.3', '6.4', '6.5', '6.6', '6.7', '6.8', '6.9', '6.10', '6.11', '6.12')
def test_fields_of_the_board(real, hw, product):
    """The assertions of test_ui_fields.py (fields, options, defaults) against the real board."""
    env = ready(real, product)
    for name in SECTION6[product]:
        getattr(fields, name)(env)
    env.shot(f'hw_{product}_fields_light')
    env.page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")


@pytest.mark.checklist('6.13')
def test_step400_ton_toff_128_refused(real, hw):
    env = ready(real, 'STEP400')
    env.dirty = True
    fields.test_step400_ton_toff_128_is_refused(env, 'TON_MIN')


# ------------------------------------------------------------------ 7
@pytest.mark.checklist('7.1')
def test_step400_overcurrent_3_and_tval(real, hw):
    b = hw.boards['STEP400']
    env = real('STEP400').open().connect()
    env.dirty = True
    env.page.select_option('#f-alarm-OCThreshold-0', '3')
    assert env.page.locator('#f-alarm-OCThreshold-0 option:checked').inner_text() == '1250 mA (3)'
    env.dialogs.answers = [True]
    env.page.click('#btn-save')
    env.wait_status('Board rebooted', timeout=10000)
    env.page.click('#btn-connect')
    env.wait_status('Config loaded from board', timeout=30000)
    shown_tval = env.page.locator('#f-current-TVAL_RUN-0 option:checked').inner_text()
    env.page.click('#btn-connect')                       # Disconnect: OSC does not need the port
    env.wait_status('Disconnected')
    osc_ready(b)
    r = b.osc_query('/getOverCurrentThreshold', 1, timeout=1.0)
    t = b.osc_query('/getTval_mA', 1, timeout=1.0)
    t_ = b.osc_query('/getTval', 1, timeout=1.0)
    ma = [x for x in t if x[0] == '/tval_mA'] or t
    hw.rec('7.1 STEP400', dict(oc=r, tval_mA=t, tval=t_, tool_shows=shown_tval))
    assert r and r[0][1][-1] == 1250.0, r              # (3 + 1) x 312.5 mA
    mA = float(ma[0][1][2])                            # [id, hold, run, acc, dec]
    tv = int(t_[0][1][2])
    assert shown_tval == f'{(tv + 1) * 78.125:.10g} mA ({tv})'
    assert abs(mA - (tv + 1) * 78.125) < 1.0, (mA, tv)


@pytest.mark.checklist('7.2', '7.3', '7.4')
def test_osc_set_then_read_shows_the_value(real, hw, product):
    b = hw.boards[product]
    env = real(product).open().connect()
    env.dirty = True
    osc_ready(b)
    if product == 'STEP400':
        b.osc_send('/setOverCurrentThreshold', 255, 20)
        want_oc, want_text = 6562.5, '6562.5 mA (20)'
        stall = None
    else:
        b.osc_send('/setOverCurrentThreshold', 255, 10)
        b.osc_send('/setStallThreshold', 255, 64)
        want_oc, want_text = 4125.0, '4125 mA (10)'
        stall = '2031.25 mA (64)'
    time.sleep(0.5)
    env.page.click('#btn-read')
    env.wait_status('Config loaded from board')
    time.sleep(0.3)
    got = env.page.locator('#f-alarm-OCThreshold-0 option:checked').inner_text()
    stall_got = env.page.locator('#f-voltage-STALL_TH-0 option:checked').inner_text()
    hw.rec(f'7.2 {product}', dict(oc=got, stall=stall_got))
    assert got == want_text
    if stall:
        assert stall_got == stall
    # 7.2: save unchanged -> still the same value
    env.dialogs.answers = [False]
    env.page.click('#btn-save')
    env.wait_status('Saved to SD')
    env.page.click('#btn-read')
    env.wait_status('Config loaded from board')
    time.sleep(0.3)
    assert env.page.locator('#f-alarm-OCThreshold-0 option:checked').inner_text() == want_text
    env.page.click('#btn-connect')
    env.wait_status('Disconnected')
    osc_ready(b)
    r = b.osc_query('/getOverCurrentThreshold', 1, timeout=1.0)
    assert r and r[0][1][-1] == want_oc, r


@pytest.mark.checklist('7.5')
def test_step800_slew_rate_1(real, hw):
    env = real('STEP800').open().connect()
    env.dirty = True
    env.page.select_option('#f-driver-slewRate-0', '1')
    env.dialogs.answers = [True]
    env.page.click('#btn-save')
    env.wait_status('Board rebooted', timeout=10000)
    env.page.click('#btn-connect')
    env.wait_status('Config loaded from board', timeout=30000)
    assert env.page.locator('#f-driver-slewRate-0 option:checked').inner_text() == '1 – 290 V/µs'


# ------------------------------------------------------------------ 10
@pytest.mark.checklist('10.1', '10.2')
def test_reboot_order_in_the_bridge_log(real, hw, product):
    env = ready(real, product)
    env.dialogs.answers = [True]
    m = env.backend.mark()
    env.page.click('#btn-reboot')
    env.wait_status('Board rebooted — click Connect to reconnect.', timeout=10000)
    ents = env.backend.since(m)
    kinds = [(e['dir'], e.text.strip()[:40]) for e in ents]
    i_tx = next(i for i, e in enumerate(ents) if e['dir'] == 'tx' and e.text == 'R')
    i_rx = next(i for i, e in enumerate(ents) if e['dir'] == 'rx' and 'Rebooting...' in e.text)
    i_close = next(i for i, e in enumerate(ents) if e['dir'] == 'ev' and e.text == 'close')
    assert i_tx < i_rx < i_close, kinds
    dt = ents[i_close]['t'] - ents[i_rx]['t']
    hw.rec(f'10.1 {product} bridge', dict(R_to_reply_s=ents[i_rx]['t'] - ents[i_tx]['t'], reply_to_close_s=dt))
    assert 'timeout' not in env.err().lower()
    env.page.click('#btn-connect')
    env.wait_status('Config loaded from board', timeout=30000)
    assert env.page.locator('#btn-connect').inner_text() == '✕ Disconnect'


# ------------------------------------------------------------------ 11.3
@pytest.mark.checklist('11.3')
def test_no_console_errors_in_a_session(real, hw, product):
    env = ready(real, product)
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text(product, timeout=5000)
    env.dialogs.answers = [False]
    env.dirty = True
    env.page.click('#btn-save')
    env.wait_status('Saved to SD')
    env.page.click('#btn-connect')
    env.wait_status('Disconnected')
    assert env.unexpected_console_errors() == []

