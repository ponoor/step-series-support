"""Section 1.7, the part that stage 3 (the real Chrome) showed: what the tool does when Web Serial
leaves a promise pending after the device is lost, and how it finds the port again.

Behaviour of the shim: see the top of serial_shim.js. On the tool before `closeConn()` had time limits
and `reconnect()` looked for a new Port, tests 'hang' and 'reconnect' fail (the page stays on
'Reconnecting…' / on '✕ Disconnect').
"""
import time

import pytest
from playwright.sync_api import expect

from testlib import poll_until

HANG_ALL = "window.__SERIAL_HANG__ = {open: true, close: true, write: true, writerClose: true}"


def banner(env):
    return env.page.locator('#dc-banner')


def connect_label(env):
    return env.page.locator('#btn-connect').inner_text()


@pytest.mark.checklist('1.7')
def test_reconnect_opens_the_new_port_object(env400):
    env = env400.open().connect()
    env.expect_unplug()
    env.page.evaluate('window.__old = port')
    env.backend.disconnect(stay_unplugged=False)      # replugged 50 ms later: a new Port object + 'connect'
    expect(banner(env)).to_be_visible()
    env.page.click('#dc-banner button.primary')
    env.wait_status('Config loaded from board')
    assert env.page.evaluate('port !== window.__old && lastPort === port') is True
    assert env.page.evaluate('window.__old.connected') is False
    assert connect_label(env) == '✕ Disconnect'


@pytest.mark.checklist('1.7')
def test_reconnect_when_open_of_the_lost_port_never_ends(env400):
    env = env400.open().connect()
    env.expect_unplug()
    env.page.evaluate(HANG_ALL)
    env.backend.disconnect(stay_unplugged=False)
    expect(banner(env)).to_be_visible(timeout=8000)
    env.page.click('#dc-banner button.primary')
    env.wait_status('Config loaded from board', timeout=8000)
    assert connect_label(env) == '✕ Disconnect'


@pytest.mark.checklist('1.7')
def test_unplug_during_save_with_pending_close_returns_to_connect(make_env):
    env = make_env('STEP400', delay_save=0.7).open().connect()
    env.expect_unplug()
    env.page.evaluate(HANG_ALL)
    env.dialogs.answers = [False]
    m = env.backend.mark()
    env.page.click('#btn-save')
    poll_until(lambda: '{' in env.backend.sent(m))
    env.backend.disconnect(stay_unplugged=True)
    t = time.monotonic()
    expect(banner(env)).to_be_visible(timeout=10000)
    assert time.monotonic() - t < 7                       # five steps, 1 s each at most
    env.wait_err('The connection was lost during the save: the board may or may not have saved the configuration, so reconnect and read it back to check.')
    assert connect_label(env) == '⬡ Connect'
    assert env.page.evaluate('[closing, isSaving, port]') == [False, False, None]
    for b in ('btn-read', 'btn-save', 'btn-reboot', 'btn-poll'):
        assert env.page.locator('#' + b).is_disabled(), b
    # the cable comes back: Connect (asks for the port) works, and so does Disconnect afterwards
    env.backend.plug()
    env.page.evaluate('window.__SERIAL_HANG__ = {}')
    env.page.click('#btn-connect')
    env.wait_status('Config loaded from board')
    env.page.click('#btn-connect')
    env.wait_status('Disconnected')
    assert env.page.evaluate('closing') is False


@pytest.mark.checklist('1.7')
def test_disconnect_button_after_a_stuck_close_still_works(env400):
    """The 'closing' mark must not stay set when a step times out."""
    env = env400.open().connect()
    env.expect_unplug()
    env.page.evaluate(HANG_ALL)
    env.backend.disconnect(stay_unplugged=True)
    expect(banner(env)).to_be_visible(timeout=10000)
    assert env.page.evaluate('closing') is False
    env.page.evaluate('closeConn()')                       # a second call returns at once and changes nothing
    assert connect_label(env) == '⬡ Connect'


@pytest.mark.checklist('1.7')
def test_write_that_never_ends_counts_as_a_lost_connection(env400):
    env = env400.open().connect()
    env.expect_unplug()
    env.page.evaluate("window.__SERIAL_HANG__ = {stall: true, writerClose: true, close: true, open: true}")
    # the first write is accepted by the stream's queue, the second one waits behind the stuck sink
    env.page.evaluate("void (window.__sent = send('G').then(() => send('G')).then(() => 'sent', e => e.closed ? 'closed' : e.message))")
    expect(banner(env)).to_be_visible(timeout=10000)
    assert env.page.evaluate('window.__sent') == 'closed'
    assert connect_label(env) == '⬡ Connect'
    assert env.page.evaluate('closing') is False


@pytest.mark.checklist('1.7')
def test_serial_log_lines_show_the_steps(env400):
    env = env400.open().connect()
    env.expect_unplug()
    env.backend.disconnect(stay_unplugged=False)
    expect(banner(env)).to_be_visible()
    env.page.click('#dc-banner button.primary')
    env.wait_status('Config loaded from board')
    logs = [t for k, t in env.console_log if t.startswith('[serial] ')]
    joined = '\n'.join(logs)
    for needle in ('open: port opened', 'closeConn: start', 'close: reader.cancel()', 'closeConn: done',
                   'reconnect: start', 'reconnect: getPorts()', 'reconnect: done'):
        assert needle in joined, needle
    assert all(' ms)' in t for t in logs if t.startswith(('[serial] close', '[serial] reconnect', '[serial] open')))


@pytest.mark.checklist('1.7')
def test_reconnect_with_two_granted_ports_asks_which(env400):
    env = env400.open().connect()
    env.expect_unplug()
    env.page.evaluate("""() => {
      window.__asked = 0;
      const a = {connected: true}, b = {connected: true};
      navigator.serial.getPorts = async () => [a, b];
      navigator.serial.requestPort = async () => { window.__asked++; throw new DOMException('No port selected by the user.', 'NotFoundError'); };
    }""")
    env.backend.disconnect(stay_unplugged=True)
    expect(banner(env)).to_be_visible()
    env.page.click('#dc-banner button.primary')
    env.wait_status('Reconnect failed: No port selected by the user.')
    assert env.page.evaluate('window.__asked') == 1
    assert connect_label(env) == '⬡ Connect'


@pytest.mark.checklist('1.7')
def test_reconnect_warns_when_another_board_answers(env400):
    env = env400.open().connect()
    env.expect_unplug()
    env.page.evaluate("lastProduct = 'STEP800'")
    env.backend.disconnect(stay_unplugged=False)
    expect(banner(env)).to_be_visible()
    env.page.click('#dc-banner button.primary')
    env.wait_status('Config loaded from board')
    env.wait_err('Reconnected to a different board: STEP400 (before: STEP800)')


def request_port_calls(env):
    return sum(1 for e in env.page.evaluate('window.__serialShim.log') if e.get('ev') == 'requestPort')


@pytest.mark.checklist('1.7')
def test_reconnect_clicked_before_the_board_is_back_waits_for_it(env400):
    env = env400.open().connect()
    env.expect_unplug()
    asked = request_port_calls(env)
    env.backend.disconnect(stay_unplugged=True)
    expect(banner(env)).to_be_visible()
    env.page.click('#dc-banner button.primary')
    env.wait_status('Waiting for the board to come back…')
    time.sleep(1)
    env.backend.plug()
    env.page.evaluate('window.__serialShim.plugIn()')
    env.wait_status('Config loaded from board')
    assert connect_label(env) == '✕ Disconnect'
    assert request_port_calls(env) == asked                # the picker was not used


@pytest.mark.checklist('1.7')
def test_reconnect_gives_up_after_3_s_without_asking_for_a_port(env400):
    env = env400.open().connect()
    env.expect_unplug()
    asked = request_port_calls(env)
    env.backend.disconnect(stay_unplugged=True)
    expect(banner(env)).to_be_visible()
    t = time.monotonic()
    env.page.click('#dc-banner button.primary')
    env.wait_status('Reconnect failed: the board is not connected. Plug in the USB cable and click Connect.', timeout=8000)
    assert 2.5 < time.monotonic() - t < 6
    assert request_port_calls(env) == asked                # requestPort() needs a fresh click: not called after waiting
    assert connect_label(env) == '⬡ Connect'
    assert env.page.locator('#btn-connect').is_enabled()
    env.backend.plug()
    env.page.click('#btn-connect')
    env.wait_status('Config loaded from board')


@pytest.mark.checklist('1.7')
def test_board_text_is_marked_board_and_the_tools_own_lines_serial(env400):
    env = env400.open().connect()
    assert any(t == 'log' and x.startswith('[board]') for t, x in env.console_log)
    assert not any(t == 'log' and x.startswith('[serial] Ethernet') for t, x in env.console_log)
    assert any(t == 'log' and x.startswith('[serial] open:') for t, x in env.console_log)
