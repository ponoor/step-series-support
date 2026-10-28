"""Checklist sections 0, 1, 2, 10 and 11.3: opening, connecting, reading, status, reboot."""
import asyncio
import json
import time

import pytest
from playwright.sync_api import expect

from testlib import make_card, card_cfg, Card, poll_until, wait_boot

pytestmark = []


# ------------------------------------------------------------------ 0
@pytest.mark.checklist('0.3')
def test_open_disconnected(env400):
    env400.open()
    assert env400.status().startswith('Disconnected')
    p = env400.page
    assert p.locator('#btn-connect').is_enabled()
    for b in ('btn-read', 'btn-save', 'btn-reboot', 'btn-poll'):
        assert p.locator('#' + b).is_disabled(), b
    assert p.locator('#no-serial').is_hidden()       # the shim provides navigator.serial
    assert p.locator('#dc-banner').is_hidden()


# ------------------------------------------------------------------ 1
@pytest.mark.checklist('1.1')
@pytest.mark.parametrize('product', ['STEP400', 'STEP800'])
def test_connect_loads_config(make_env, product):
    env = make_env(product, card=make_card(product)).open()
    env.connect()
    assert env.status() == 'Config loaded from board'
    assert env.page.locator('#btn-connect').inner_text() == '✕ Disconnect'
    for b in ('btn-read', 'btn-save', 'btn-reboot', 'btn-poll'):
        assert env.page.locator('#' + b).is_enabled(), b


@pytest.mark.checklist('1.2')
@pytest.mark.parametrize('product,axes', [('STEP400', 4), ('STEP800', 8)])
def test_board_info_with_card(make_env, product, axes):
    env = make_env(product, card=make_card(product)).open().connect()
    t = lambda i: env.page.locator(i).inner_text()
    assert t('#bi-product') == product
    assert t('#bi-fw') == '2.2.0'
    assert t('#bi-cfgver') == '1.2'
    assert t('#bi-target') == product
    assert env.page.locator('#bi-axes-fixed').inner_text() == f'{axes} (from board)'
    assert env.page.locator('#bi-axes-sel').is_hidden()


@pytest.mark.checklist('1.2')
def test_board_info_without_card(make_env):
    env = make_env('STEP400', card=Card('none')).open().connect()
    assert env.page.locator('#bi-cfgver').inner_text() == '-1.0'      # loadedConfigVersion {-1, 0}
    assert env.page.locator('#bi-target').inner_text() == '---'


@pytest.mark.checklist('1.3')
def test_config_name_from_card(make_env):
    env = make_env('STEP400', card=make_card('STEP400', name='my card name')).open().connect()
    assert env.val('#bi-cfgname') == 'my card name'


@pytest.mark.checklist('1.4')
def test_save_filename_is_the_file_read_at_startup(make_env):
    files = {'/zzz.json': json.loads(card_cfg('STEP400', 'z'))}
    env = make_env('STEP400', card=make_card(files=files)).open().connect()
    assert env.board.config_filename == '/zzz.json'
    assert env.val('#sd-filename') == '/zzz.json'
    # no card: the default /config.txt
    env2 = make_env('STEP400', card=Card('none')).open().connect()
    assert env2.val('#sd-filename') == '/config.txt'


@pytest.mark.checklist('1.5')
@pytest.mark.parametrize('product,axes', [('STEP400', 4), ('STEP800', 8)])
def test_column_count_matches_axes(make_env, product, axes):
    env = make_env(product).open().connect()
    for t in ('alarm', 'driver', 'speed', 'voltage', 'servo'):
        assert len(env.header_cells(f'#{t}-tbl')) == axes + 1, t
    if product == 'STEP400':
        assert len(env.header_cells('#current-tbl')) == axes + 1


@pytest.mark.checklist('1.6')
def test_read_again_restores_board_values(env400):
    env = env400.open().connect()
    first = env.page.evaluate("Array.from(document.querySelectorAll('input,select')).map(e => [e.id, e.type === 'checkbox' ? e.checked : e.value])")
    env.set('#f-voltage-KVAL_RUN-0', 99)
    env.set('#net-inPort', 1234)
    env.set('#bi-cfgname', 'changed')
    env.page.click('#btn-read')
    env.wait_status('Config loaded from board')
    time.sleep(0.2)
    second = env.page.evaluate("Array.from(document.querySelectorAll('input,select')).map(e => [e.id, e.type === 'checkbox' ? e.checked : e.value])")
    first = [x for x in first if x[0] not in ('file-input',)]
    second = [x for x in second if x[0] not in ('file-input',)]
    assert first == second


@pytest.mark.checklist('1.7')
def test_unplug_banner_and_reconnect(env400):
    env = env400.open().connect()
    env.expect_unplug()
    env.backend.disconnect(stay_unplugged=False)
    expect(env.page.locator('#dc-banner')).to_be_visible()
    assert 'Serial connection lost' in env.page.locator('#dc-banner').inner_text()
    assert env.page.locator('#btn-connect').inner_text() == '⬡ Connect'
    for b in ('btn-read', 'btn-save', 'btn-reboot', 'btn-poll'):
        assert env.page.locator('#' + b).is_disabled(), b
    env.page.click('#dc-banner button.primary')           # Reconnect
    env.wait_status('Config loaded from board')
    assert env.page.locator('#dc-banner').is_hidden()
    assert env.page.locator('#btn-connect').inner_text() == '✕ Disconnect'


@pytest.mark.checklist('1.7')
def test_reconnect_while_still_unplugged_then_plug(env400):
    env = env400.open().connect()
    env.expect_unplug()
    env.backend.disconnect(stay_unplugged=True)
    expect(env.page.locator('#dc-banner')).to_be_visible()
    env.page.click('#dc-banner button.primary')
    env.wait_status('Reconnect failed')
    assert env.page.locator('#btn-connect').is_enabled()
    env.backend.plug()
    env.page.click('#btn-connect')                         # asks for the port again
    env.wait_status('Config loaded from board')


@pytest.mark.checklist('1.7')
def test_dismiss_banner(env400):
    env = env400.open().connect()
    env.expect_unplug()
    env.backend.disconnect(stay_unplugged=False)
    expect(env.page.locator('#dc-banner')).to_be_visible()
    env.page.click('#dc-banner button:not(.primary)')
    expect(env.page.locator('#dc-banner')).to_be_hidden()


def test_connect_cancelled_in_port_dialog(make_env):
    env = make_env('STEP400').open()
    env.page.evaluate('window.__SERIAL_REQUEST_FAIL__ = true')
    env.page.click('#btn-connect')
    env.wait_status('Connection failed')
    assert env.page.locator('#btn-connect').inner_text() == '⬡ Connect'


def test_unplug_during_polling_stops_polling(env400):
    env = env400.open().connect()
    env.expect_unplug()
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text('STEP400')
    env.backend.disconnect(stay_unplugged=False)
    expect(env.page.locator('#dc-banner')).to_be_visible()
    assert env.page.locator('#btn-poll').inner_text() == '▶ Start Status'
    assert env.page.evaluate('pollTimer') is None


@pytest.mark.checklist('11.3')
def test_unplug_leaves_no_page_error(env400):
    env = env400.open().connect()
    env.expect_unplug()
    env.backend.disconnect(stay_unplugged=False)
    expect(env.page.locator('#dc-banner')).to_be_visible()
    time.sleep(0.3)
    assert [e for e in env.console_errors if e.startswith('pageerror')] == []


@pytest.mark.checklist('1.7')
def test_unplug_during_save_status_recovers(make_env):
    env = make_env('STEP400', delay_save=0.7).open().connect()
    env.expect_unplug()
    env.dialogs.answers = [False]
    m = env.backend.mark()
    env.page.click('#btn-save')
    poll_until(lambda: '{' in env.backend.sent(m))
    env.backend.disconnect(stay_unplugged=False)
    expect(env.page.locator('#dc-banner')).to_be_visible()
    env.wait_err('The connection was lost during the save: the board may or may not have saved the configuration, so reconnect and read it back to check.')
    assert env.status() == 'Save failed'
    assert env.page.evaluate('isSaving') is False
    env.page.click('#dc-banner button.primary')
    env.wait_status('Config loaded from board')
    env.page.click('#btn-poll')
    # a working status panel fills in within a few seconds
    expect(env.page.locator('#rt-board')).to_contain_text('STEP400', timeout=3000)


# ------------------------------------------------------------------ 2
@pytest.mark.checklist('2.1')
def test_status_panel_values_and_updates(make_env):
    env = make_env('STEP400', card=make_card('STEP400')).open().connect()
    env.page.click('#btn-poll')
    rb = env.page.locator('#rt-board')
    expect(rb).to_contain_text('STEP400')
    txt = rb.inner_text()
    assert '10.0.0.100' in txt and 'Link ON' in txt
    assert env.page.locator('#rt-board .badge').nth(1).inner_text() == 'OK'          # SD
    assert env.page.locator('#rt-board .badge').nth(2).inner_text() == 'Loaded'      # Config
    assert env.page.locator('#btn-poll').inner_text() == '■ Stop Status'
    assert len(env.header_cells('#rt-motors table')) == 5
    env.board.motors[0]['position'] = 12345
    env.board.motors[1]['speed'] = 321.5
    expect(env.page.locator('#rt-motors')).to_contain_text('12345', timeout=3000)
    assert '321.5' in env.page.locator('#rt-motors').inner_text()
    # once per second
    m = env.backend.mark()
    time.sleep(3.3)
    n = env.backend.sent(m).count('T')
    assert 2 <= n <= 5, n


@pytest.mark.checklist('2.1')
def test_status_panel_8_axes(make_env):
    env = make_env('STEP800', card=make_card('STEP800')).open().connect()
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text('STEP800')
    assert len(env.header_cells('#rt-motors table')) == 9


@pytest.mark.checklist('2.2')
def test_status_link_off_on(env400):
    env = env400.open().connect()
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text('Link ON')
    env.board.link_status = 2
    expect(env.page.locator('#rt-board')).to_contain_text('Link OFF', timeout=3000)
    assert env.page.locator('#rt-board .badge.b-err').count() >= 1
    env.board.link_status = 1
    expect(env.page.locator('#rt-board')).to_contain_text('Link ON', timeout=3000)


@pytest.mark.checklist('2.3')
@pytest.mark.parametrize('state', ['none', 'exfat'])
def test_status_sd_err_and_config_not_loaded(make_env, state):
    env = make_env('STEP400', card=Card(state)).open().connect()
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text('STEP400')
    badges = env.page.locator('#rt-board .badge')
    assert badges.nth(1).inner_text() == 'ERR'
    assert 'b-err' in badges.nth(1).get_attribute('class')
    assert badges.nth(2).inner_text() == 'Not loaded'


@pytest.mark.checklist('2.4', '3.8')
def test_save_while_status_is_polling_with_a_slow_response(make_env):
    """A status request still waiting for its answer when Save is pressed. The board answers in
    order (T, then F), so a tool that takes the late T answer for the F answer fails."""
    env = make_env('STEP400', card=make_card('STEP400'), delay_T=0.5).open().connect()
    env.dialogs.answers = [False]
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text('STEP400')
    m = env.backend.mark()
    # wait for the next T to be on its way, then press Save
    poll_until(lambda: env.backend.sent(m).count('T') >= 1, timeout=3)
    env.page.click('#btn-save')
    env.wait_status('Saved to SD', timeout=6000)
    assert 'Filename rejected' not in env.err()
    assert env.status().startswith('✓ Saved to SD')


@pytest.mark.checklist('2.4', '3.8')
def test_save_while_status_is_polling_normal_speed(make_env):
    env = make_env('STEP400', card=make_card('STEP400'), delay_T=0.02).open().connect()
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text('STEP400')
    for _ in range(3):
        env.dialogs.answers = [False]
        env.page.click('#btn-save')
        env.wait_status('Saved to SD')
        assert env.err() == ''
        time.sleep(1.1)
    # polling continues after the saves
    env.board.motors[2]['position'] = 777
    expect(env.page.locator('#rt-motors')).to_contain_text('777', timeout=3000)


@pytest.mark.checklist('2.4')
def test_status_polling_pauses_during_save(make_env):
    """Between the F and the { the tool sends no T (isSaving), so the board is not asked for
    anything while it saves."""
    env = make_env('STEP400', card=make_card('STEP400'), delay_save=0.7).open().connect()
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text('STEP400')
    env.dialogs.answers = [False]
    m = env.backend.mark()
    env.page.click('#btn-save')
    env.wait_status('Saved to SD', timeout=6000)
    texts = [e.text for e in env.backend.since(m, 'tx')]
    i = next(k for k, t in enumerate(texts) if t.startswith('F'))
    assert not any(t == 'T' for t in texts[i:]), texts[i:]


@pytest.mark.checklist('2.5')
def test_stop_status(env400):
    env = env400.open().connect()
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text('STEP400')
    env.page.click('#btn-poll')
    assert env.page.locator('#btn-poll').inner_text() == '▶ Start Status'
    m = env.backend.mark()
    time.sleep(2.3)
    assert env.backend.sent(m) == ''


# ------------------------------------------------------------------ 10
@pytest.mark.checklist('10.1', '10.2', '3.5')
def test_reboot_closes_after_reply_then_reconnect(make_env):
    env = make_env('STEP400', card=make_card('STEP400'), boot_time=0.5).open().connect()
    env.dialogs.answers = [True]
    m = env.backend.mark()
    env.page.click('#btn-reboot')
    env.wait_status('Board rebooted — click Connect to reconnect.')
    assert env.dialogs.messages[0].startswith('Reboot the board now?')
    assert env.page.locator('#dc-banner').is_hidden()                 # not shown for an intended close
    assert env.page.locator('#btn-connect').inner_text() == '⬡ Connect'
    # order in the record: R sent, the reply received, then the page closed the port
    time.sleep(0.3)
    ev = [(e['dir'], e.text) for e in env.backend.since(m)]
    assert ev[0] == ('tx', 'R')
    rx_so_far, r = '', None
    for i, (d, t) in enumerate(ev):
        if d == 'rx':
            rx_so_far += t
            if r is None and 'Rebooting...' in rx_so_far:
                r = i
    c = next(i for i, (d, t) in enumerate(ev) if d == 'ev' and t in ('close', 'device-drop'))
    assert r is not None and r < c
    assert env.err() == ''
    # reconnect after the board is up again
    wait_boot(env, 2)
    env.page.click('#btn-connect')
    env.wait_status('Config loaded from board')
    assert env.board.boot_count == 2


@pytest.mark.checklist('10.1')
def test_reboot_cancelled(env400):
    env = env400.open().connect()
    env.dialogs.answers = [False]
    m = env.backend.mark()
    env.page.click('#btn-reboot')
    time.sleep(0.3)
    assert env.backend.sent(m) == ''
    assert env.page.locator('#btn-connect').inner_text() == '✕ Disconnect'


@pytest.mark.checklist('10.3')
def test_reboot_with_brake_wait_has_no_timeout_error(make_env):
    """The firmware replies first and waits for the brakes (up to 1 s) before it resets."""
    env = make_env('STEP400', boot_time=0.3, reboot_brake_wait=1.0).open().connect()
    env.expect_unplug()
    env.dialogs.answers = [True]
    env.page.click('#btn-reboot')
    env.wait_status('Board rebooted')
    time.sleep(1.6)
    assert 'timeout' not in env.err().lower()
    assert env.page.locator('#dc-banner').is_hidden()


@pytest.mark.checklist('10.1')
def test_reboot_while_polling(make_env):
    env = make_env('STEP400', boot_time=0.3).open().connect()
    env.expect_unplug()
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text('STEP400')
    env.dialogs.answers = [True]
    env.page.click('#btn-reboot')
    env.wait_status('Board rebooted')
    time.sleep(1.5)
    assert 'timeout' not in env.err().lower()
    assert env.page.locator('#dc-banner').is_hidden()
    assert env.page.evaluate('pollTimer') is None


def test_reboot_reply_never_comes(make_env):
    """If the reply to R is lost the tool waits 3 s and closes anyway."""
    env = make_env('STEP400').open().connect()
    env.allow_console_error('WebSocket connection')

    async def silent(text):
        return None
    env.board._out = silent
    env.dialogs.answers = [True]
    env.page.click('#btn-reboot')
    env.wait_status('Board rebooted', timeout=6000)


# ------------------------------------------------------------------ 11.3
@pytest.mark.checklist('11.3')
def test_no_console_errors_in_a_normal_session(make_env):
    env = make_env('STEP400', card=make_card('STEP400'), boot_time=0.4).open().connect()
    env.expect_unplug()
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text('STEP400')
    env.page.click('#btn-poll')
    env.dialogs.answers = [False]
    env.page.click('#btn-save')
    env.wait_status('Saved to SD')
    env.dialogs.answers = [True]
    env.page.click('#btn-reboot')
    env.wait_status('Board rebooted')
    wait_boot(env, 2)
    env.page.click('#btn-connect')
    env.wait_status('Config loaded from board')
    assert env.unexpected_console_errors() == []
    # board noise lines are logged, not errors
    assert any(t == 'log' and '[serial]' in x for t, x in env.console_log)


# ------------------------------------------------------------------ Disconnect -> Connect
def open_connections(env):
    return [e for e in env.backend.entries if e['dir'] == 'ev' and e.text == 'open'].__len__() - \
           [e for e in env.backend.entries if e['dir'] == 'ev' and e.text == 'close'].__len__()


@pytest.mark.checklist('1.1', '1.6')
def test_disconnect_then_connect_three_times(make_env):
    env = make_env('STEP400', card=make_card('STEP400')).open().connect()
    for i in range(3):
        env.page.click('#btn-connect')                       # Disconnect
        env.wait_status('Disconnected')
        assert env.page.locator('#btn-connect').inner_text() == '⬡ Connect'
        assert poll_until(lambda: open_connections(env) == 0), 'the connection stayed open'
        env.page.click('#btn-connect')                       # Connect
        env.wait_status('Config loaded from board')
        assert poll_until(lambda: open_connections(env) == 1)
        env.page.click('#btn-read')
        env.wait_status('Config loaded from board')
    assert env.backend.connections == 4


def test_disconnect_then_connect_while_status_is_shown(make_env):
    env = make_env('STEP400', card=make_card('STEP400')).open().connect()
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text('STEP400')
    env.page.click('#btn-connect')
    env.wait_status('Disconnected')
    assert env.page.locator('#btn-poll').inner_text() == '▶ Start Status'
    assert poll_until(lambda: open_connections(env) == 0)
    env.page.click('#btn-connect')
    env.wait_status('Config loaded from board')
    env.page.click('#btn-poll')
    env.board.motors[1]['position'] = 4321
    expect(env.page.locator('#rt-motors')).to_contain_text('4321', timeout=3000)


@pytest.mark.checklist('1.7')
@pytest.mark.xfail(strict=True, reason='(a) tool, not in the 1b list: closeConn() cancels the reader, the read '
                   'loop sees done and calls handleDisconnect() while port is still set, so the "Serial '
                   'connection lost" banner appears after the user clicks Disconnect')
def test_disconnect_button_shows_no_lost_banner(env400):
    env = env400.open().connect()
    env.page.click('#btn-connect')
    env.wait_status('Disconnected')
    time.sleep(0.3)
    assert env.page.locator('#dc-banner').is_hidden()


@pytest.mark.checklist('1.7')
def test_unplug_before_the_json_is_sent_says_nothing_was_saved(make_env):
    env = make_env('STEP400', delay_F=0.6).open().connect()
    env.expect_unplug()
    env.dialogs.answers = [False]
    m = env.backend.mark()
    env.page.click('#btn-save')
    poll_until(lambda: env.backend.sent(m).startswith('F'))
    env.backend.disconnect(stay_unplugged=False)
    env.wait_err('The connection was lost before the configuration was sent: nothing was saved.')
    assert '{' not in env.backend.sent(m)
    assert env.page.evaluate('isSaving') is False


@pytest.mark.parametrize('cmd', ['read', 'status', 'reboot'])
def test_unplug_ends_a_waiting_read_status_or_reboot_at_once(make_env, cmd):
    """G, T and R waits end with the unplug (not after their own timeouts of 8 / 3 / 3 s)."""
    env = make_env('STEP400', delay_G=3.0, delay_T=3.0, reboot_min_wait=3.0).open()
    env.expect_unplug()
    env.board.delay_G = 0.02
    env.connect()
    if cmd == 'read':
        env.board.delay_G = 3.0
        env.page.click('#btn-read')
    elif cmd == 'status':
        env.page.click('#btn-poll')
    else:
        env.board._out = lambda text: asyncio.sleep(0)     # no reply to R
        env.dialogs.answers = [True]
        env.page.click('#btn-reboot')
    time.sleep(0.4)
    t0 = time.time()
    env.backend.disconnect(stay_unplugged=False)
    if cmd == 'reboot':
        env.wait_status('Board rebooted', timeout=2000)
    else:
        expect(env.page.locator('#dc-banner')).to_be_visible()
        if cmd == 'read':
            env.wait_err('Read failed', timeout=1500)
    assert time.time() - t0 < 2.0
    assert env.page.evaluate('lineWaiters.length') == 0


@pytest.mark.checklist('11.3')
@pytest.mark.parametrize('how', ['unplug', 'disconnect', 'reboot', 'unplug_polling', 'reboot_reply_lost'])
def test_no_page_error_on_unplug_disconnect_or_reboot(make_env, how):
    env = make_env('STEP400', boot_time=0.3).open().connect()
    if how == 'unplug':
        env.backend.disconnect(stay_unplugged=False)
        expect(env.page.locator('#dc-banner')).to_be_visible()
    elif how == 'unplug_polling':
        env.page.click('#btn-poll')
        expect(env.page.locator('#rt-board')).to_contain_text('STEP400')
        env.backend.disconnect(stay_unplugged=False)
        expect(env.page.locator('#dc-banner')).to_be_visible()
    elif how == 'disconnect':
        env.page.click('#btn-connect')
        env.wait_status('Disconnected')
    else:
        if how == 'reboot_reply_lost':
            env.board._out = lambda text: asyncio.sleep(0)
        env.dialogs.answers = [True]
        env.page.click('#btn-reboot')
        env.wait_status('Board rebooted', timeout=6000)
    time.sleep(0.8)
    assert env.console_errors == []
