"""Checklist sections 6, 7 and 8: fields per board, current / threshold display, range checks."""
import json
import time

import pytest
from playwright.sync_api import expect

from testlib import make_card, sent_json, tmpl


def labels(env, table):
    return env.visible_rows(table)


def option_texts(env, sel):
    return [t for _, t in env.options(sel)]


def default_option(env, sel):
    """The option that is `selected` in the HTML the tool builds (the tool's default)."""
    return env.page.eval_on_selector(sel, 'e => { const o = e.querySelector("option[selected]"); return o ? [o.value, o.textContent] : null; }')


# ------------------------------------------------------------------ 6: STEP800
@pytest.fixture
def e800(make_env):
    return make_env('STEP800').open().connect()


@pytest.fixture
def e400(make_env):
    return make_env('STEP400').open().connect()


@pytest.mark.checklist('6.1')
def test_step800_has_brake_fields(e800):
    rows = labels(e800, '#driver-tbl')
    assert 'Electromagnetic brake enable' in rows
    assert 'Brake transition duration (ms)' in rows


@pytest.mark.checklist('6.2')
def test_step800_has_no_current_mode_and_no_limit(e800):
    assert e800.page.locator('#current-panel').is_hidden()
    drv = labels(e800, '#driver-tbl')
    assert not any('Current mode enable' in r for r in drv)
    assert not any('LIMIT' in r for r in drv)
    assert not any('LIMIT' in r for r in labels(e800, '#alarm-tbl'))


@pytest.mark.checklist('6.3')
def test_step800_slew_rate(e800):
    sel = '#f-driver-slewRate-0'
    assert option_texts(e800, sel) == ['0 – 180 V/µs', '1 – 290 V/µs', '2 – 530 V/µs']
    assert default_option(e800, sel)[0] == '2'
    assert e800.val(sel) == '2'                               # the board's value


@pytest.mark.checklist('6.4')
def test_step800_overcurrent_options(e800):
    sel = '#f-alarm-OCThreshold-0'
    o = option_texts(e800, sel)
    assert len(o) == 16
    assert o[0] == '375 mA (0)' and o[1] == '750 mA (1)' and o[-1] == '6000 mA (15)'
    assert default_option(e800, sel) == ['7', '3000 mA (7)']


@pytest.mark.checklist('6.5')
def test_step800_stall_threshold_options(e800):
    sel = '#f-voltage-STALL_TH-0'
    o = option_texts(e800, sel)
    assert len(o) == 128
    assert o[0] == '31.25 mA (0)' and o[1] == '62.5 mA (1)' and o[-1] == '4000 mA (127)'
    assert default_option(e800, sel) == ['127', '4000 mA (127)']


# ------------------------------------------------------------------ 6: STEP400
@pytest.mark.checklist('6.6')
def test_step400_has_limit_fields(e400):
    assert 'Report LIMIT switch status' in labels(e400, '#alarm-tbl')
    drv = labels(e400, '#driver-tbl')
    assert 'LIMIT switch mode' in drv
    assert 'Prohibit motion when LIMIT SW active' in drv


@pytest.mark.checklist('6.7')
def test_step400_has_current_mode(e400):
    assert e400.page.locator('#current-panel').is_visible()
    assert 'Current mode enable (PowerSTEP01)' in labels(e400, '#driver-tbl')


@pytest.mark.checklist('6.8')
def test_step400_has_brake_fields(e400):
    drv = labels(e400, '#driver-tbl')
    assert 'Electromagnetic brake enable' in drv and 'Brake transition duration (ms)' in drv


@pytest.mark.checklist('6.9')
def test_step400_slew_rate(e400):
    sel = '#f-driver-slewRate-0'
    o = option_texts(e400, sel)
    assert o == ['0 – 114 V/µs', '1 – 220 V/µs', '2 – 400 V/µs', '3 – 520 V/µs', '4 – 790 V/µs', '5 – 980 V/µs']
    assert default_option(e400, sel)[0] == '5'


@pytest.mark.checklist('6.10')
def test_step400_overcurrent_options(e400):
    sel = '#f-alarm-OCThreshold-0'
    o = option_texts(e400, sel)
    assert len(o) == 32
    assert o[0] == '312.5 mA (0)' and o[-1] == '10000 mA (31)'
    assert default_option(e400, sel) == ['15', '5000 mA (15)']


@pytest.mark.checklist('6.11')
def test_step400_stall_threshold_options(e400):
    sel = '#f-voltage-STALL_TH-0'
    o = option_texts(e400, sel)
    assert len(o) == 32
    assert o[0] == '312.5 mA (0)' and o[-1] == '10000 mA (31)'
    assert default_option(e400, sel) == ['31', '10000 mA (31)']


@pytest.mark.checklist('6.12')
def test_step400_tval_options(e400):
    o = e400.options('#f-current-TVAL_RUN-0')
    assert len(o) == 65
    assert o[0] == ['0', '78.125 mA (0)']
    assert o[16] == ['16', '1328.125 mA (16)']
    assert o[64] == ['64', '5078.125 mA (64)']
    for v, t in o:                                           # (value + 1) x 78.125
        assert t == f'{(int(v) + 1) * 78.125:.10g} mA ({v})', (v, t)
    assert default_option(e400, '#f-current-TVAL_HOLD-0')[0] == '0'
    for k in ('RUN', 'ACC', 'DEC'):
        assert default_option(e400, f'#f-current-TVAL_{k}-0')[0] == '16'


@pytest.mark.checklist('6.13')
@pytest.mark.parametrize('field', ['TON_MIN', 'TOFF_MIN'])
def test_step400_ton_toff_128_is_refused(e400, field):
    e400.set(f'#f-current-{field}-0', 128)
    m = e400.backend.mark()
    e400.page.click('#btn-save')
    e400.wait_err('Check the values')
    assert f'{field} (0–127) (Motor 1): 128 is out of range' in e400.err()
    time.sleep(0.2)
    assert e400.backend.sent(m) == ''
    e400.set(f'#f-current-{field}-0', 127)
    e400.dialogs.answers = [False]
    e400.page.click('#btn-save')
    e400.wait_status('Saved to SD')


# ------------------------------------------------------------------ 7 (display of what the board reports)
@pytest.mark.checklist('7.1')
def test_overcurrent_3_and_tval_display(make_env):
    env = make_env('STEP400').open()
    env.board.cfg['alarmAndReport']['OCThreshold'][0] = 3
    env.connect()
    t = env.page.locator('#f-alarm-OCThreshold-0 option:checked').inner_text()
    assert t == '1250 mA (3)'
    assert env.page.locator('#f-current-TVAL_RUN-0 option:checked').inner_text() == '1328.125 mA (16)'


@pytest.mark.checklist('7.2')
def test_overcurrent_20_is_shown_and_saved_unchanged(make_env):
    env = make_env('STEP400').open()
    env.board.cfg['alarmAndReport']['OCThreshold'][0] = 20
    env.connect()
    assert env.page.locator('#f-alarm-OCThreshold-0 option:checked').inner_text() == '6562.5 mA (20)'
    assert env.err() == ''
    env.dialogs.answers = [False]
    m = env.backend.mark()
    env.page.click('#btn-save')
    env.wait_status('Saved to SD')
    assert sent_json(env.backend, m)['alarmAndReport']['OCThreshold'][0] == 20
    assert env.board.cfg['alarmAndReport']['OCThreshold'][0] == 20


@pytest.mark.checklist('7.3')
def test_step800_overcurrent_10(make_env):
    env = make_env('STEP800').open()
    env.board.cfg['alarmAndReport']['OCThreshold'][0] = 10
    env.connect()
    assert env.page.locator('#f-alarm-OCThreshold-0 option:checked').inner_text() == '4125 mA (10)'


@pytest.mark.checklist('7.4')
def test_step800_stall_64(make_env):
    env = make_env('STEP800').open()
    env.board.cfg['voltageMode']['STALL_TH'][0] = 64
    env.connect()
    assert env.page.locator('#f-voltage-STALL_TH-0 option:checked').inner_text() == '2031.25 mA (64)'


@pytest.mark.checklist('7.5')
def test_step800_slew_1(make_env):
    env = make_env('STEP800').open()
    env.board.cfg['driverSettings']['slewRate'][0] = 1
    env.connect()
    assert env.page.locator('#f-driver-slewRate-0 option:checked').inner_text() == '1 – 290 V/µs'


@pytest.mark.checklist('7.2')
def test_value_outside_the_options_is_moved_with_a_notice(make_env):
    env = make_env('STEP800').open()
    env.board.cfg['alarmAndReport']['OCThreshold'][0] = 40        # the L6470 has 16 steps
    env.connect()
    assert env.page.locator('#f-alarm-OCThreshold-0 option:checked').inner_text() == '6000 mA (15)'
    assert 'moved to the nearest option' in env.err()


# ------------------------------------------------------------------ 8: ranges
def blocked(env, expect_text):
    m = env.backend.mark()
    env.page.click('#btn-save')
    env.wait_err(expect_text)
    time.sleep(0.2)
    assert env.backend.sent(m) == '', env.backend.sent(m)[:60]
    return env.err()


def download_blocked(env):
    with pytest.raises(Exception):
        with env.page.expect_download(timeout=1200):
            env.page.click('#btn-download')


@pytest.mark.checklist('8.1')
def test_kval_run_256(e400):
    e400.set('#f-voltage-KVAL_RUN-0', 256)
    err = blocked(e400, 'Check the values')
    assert 'KVAL_RUN (0–255) (Motor 1): 256 is out of range' in err
    download_blocked(e400)


@pytest.mark.checklist('8.2')
@pytest.mark.parametrize('sel', ['#f-rpl-interval', '#f-alarm-reportPositionInterval-0'])
@pytest.mark.parametrize('value,text', [('70000', 'out of range'), ('-1', 'out of range'), ('', 'not a number')])
def test_position_interval_range(e400, sel, value, text):
    e400.set(sel, value)
    blocked(e400, text)


@pytest.mark.checklist('8.3')
def test_go_until_timeout_range(e400):
    sel = '#f-driver-goUntilTimeout-0'
    e400.set(sel, -1)
    blocked(e400, 'out of range')
    e400.set(sel, 2147483648)
    blocked(e400, 'out of range')
    e400.set(sel, 2147483647)
    e400.dialogs.answers = [False]
    m = e400.backend.mark()
    e400.page.click('#btn-save')
    e400.wait_status('Saved to SD')
    assert sent_json(e400.backend, m)['driverSettings']['goUntilTimeout'][0] == 2147483647


@pytest.mark.checklist('8.4')
@pytest.mark.parametrize('product', ['STEP400', 'STEP800'])
def test_brake_transition_duration_65536(make_env, product):
    env = make_env(product).open().connect()
    env.set('#f-driver-brakeTransitionDuration-0', 65536)
    blocked(env, 'out of range')
    env.set('#f-driver-brakeTransitionDuration-0', 65535)
    env.dialogs.answers = [False]
    env.page.click('#btn-save')
    env.wait_status('Saved to SD')


@pytest.mark.checklist('8.5')
def test_ip_port_and_mac_ranges(e400):
    e400.set('#net-gateway-0', 256)
    assert 'Gateway (octet 1): 256 is out of range' in blocked(e400, 'Check the values')
    e400.set('#net-gateway-0', 10)
    e400.set('#net-inPort', 70000)
    assert 'Incoming OSC port: 70000 is out of range' in blocked(e400, 'Incoming OSC port')
    e400.set('#net-inPort', 50000)
    e400.set('#net-outPort', 70000)
    assert 'Outgoing OSC port' in blocked(e400, 'Outgoing OSC port')
    e400.set('#net-outPort', 50100)
    e400.set('#net-mac-0', 'zz')
    assert 'MAC address (byte 1): "zz" is not a decimal byte' in blocked(e400, 'MAC address')
    e400.set('#net-mac-0', 96)
    e400.page.click('#mac-hex-btn')                           # Show Hex
    assert e400.val('#net-mac-0') == '60'
    e400.set('#net-mac-0', 'zz')
    assert 'is not a hexadecimal byte' in blocked(e400, 'hexadecimal')
    e400.set('#net-mac-0', 'ff')
    e400.dialogs.answers = [False]
    m = e400.backend.mark()
    e400.page.click('#btn-save')
    e400.wait_status('Saved to SD')
    assert sent_json(e400.backend, m)['network']['mac'][0] == 255          # hex is sent as a number


@pytest.mark.checklist('8.5')
def test_empty_and_decimal_octets(e400):
    e400.set('#net-myIp-2', '')
    assert 'My IP address (octet 3): not a number' in blocked(e400, 'not a number')
    e400.set('#net-myIp-2', 1.5)
    assert 'is not an integer' in blocked(e400, 'not an integer')


@pytest.mark.checklist('8.6')
def test_config_name_braces_and_special_characters(e400):
    e400.set('#bi-cfgname', 'a}b')
    assert 'Config Name: { and } cannot be used' in blocked(e400, 'Check the values')
    e400.set('#bi-cfgname', 'a{b')
    blocked(e400, 'Check the values')
    for name in ('a"b', '日本語', 'back\\slash'):
        e400.set('#bi-cfgname', name)
        e400.dialogs.answers = [False]
        m = e400.backend.mark()
        e400.page.click('#btn-save')
        e400.wait_status('Saved to SD')
        assert sent_json(e400.backend, m)['information']['configName'] == name
        assert e400.board.config_name == name
        e400.page.evaluate("setStatus('')")        # so the next wait sees a new status


@pytest.mark.checklist('8.7')
def test_eight_axes_with_long_values_are_sent(make_env):
    env = make_env('STEP800').open().connect()
    env.page.evaluate("""() => {
      for (let i = 0; i < 8; i++) {
        document.getElementById('f-speed-acc-' + i).value = '59575.123';
        document.getElementById('f-driver-goUntilTimeout-' + i).value = '2147483647';
      }
    }""")
    env.dialogs.answers = [False]
    m = env.backend.mark()
    env.page.click('#btn-save')
    env.wait_status('Saved to SD')
    sent = env.backend.sent(m)
    n = len(sent.split('\n', 1)[1].encode())
    assert 2500 < n <= 4095, n
    cfg = sent_json(env.backend, m)
    assert cfg['speedProfile']['acc'] == [59575.123] * 8
    assert env.board.cfg['driverSettings']['goUntilTimeout'] == [2147483647] * 8


@pytest.mark.checklist('8.7')
def test_configuration_over_4095_bytes_is_refused_by_the_tool(make_env):
    """With plain numbers STEP800 reaches about 3.9 KB at most (all float fields at 17 digits);
    exponent notation (accepted by the number fields) gets over the limit."""
    env = make_env('STEP800').open().connect()
    env.page.evaluate("""() => {
      document.querySelectorAll('#speed-tbl input[type=number], #voltage-tbl input[type=number], #servo-tbl input[type=number], #driver-tbl input[type=number]').forEach(e => {
        if (e.max === '' ) e.value = '1.2345678901234567e+21';   // 22 characters each
      });
    }""")
    m = env.backend.mark()
    env.page.click('#btn-save')
    env.wait_err('too large to send over USB')
    assert '(' in env.err() and 'the board accepts 4095' in env.err()
    time.sleep(0.2)
    assert env.backend.sent(m) == ''
    assert env.status() == 'Save failed'
