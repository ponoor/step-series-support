"""A smoke test in Firefox: the tool's JavaScript runs in Gecko, with the Web Serial shim and the
fake board.

This does not check a real Firefox: the serial port is the shim's, not Firefox's own Web Serial
(available from Firefox 151). It only shows that the tool's code (connect, read, save, reboot,
download) works in the Gecko engine. A real Firefox with a board has not been tried.
"""
import pytest
from playwright.sync_api import expect

from testlib import make_card, wait_boot


@pytest.fixture
def fx(make_env, firefox):
    return make_env('STEP400', browser=firefox, card=make_card('STEP400', name='fromcard'), boot_time=0.4)


def test_firefox_has_web_serial_so_no_banner(make_env, firefox):
    env = make_env('STEP400', browser=firefox, shim=False).open()
    assert env.page.evaluate("'serial' in navigator") is True
    expect(env.page.locator('#no-serial')).to_be_hidden()
    assert env.page.locator('#btn-connect').is_enabled()


def test_firefox_connect_reads_the_config(fx):
    env = fx.open().connect()
    assert env.val('#bi-cfgname') == 'fromcard'
    assert env.page.locator('#dc-banner').is_hidden()


def test_firefox_disconnect_shows_no_banner(fx):
    env = fx.open().connect()
    env.page.click('#btn-connect')
    env.wait_status('Disconnected')
    assert env.page.locator('#dc-banner').is_hidden()


def test_firefox_save_and_reboot(fx):
    env = fx.open().connect()
    env.set('#bi-cfgname', 'ff-saved')
    env.expect_unplug()
    env.dialogs.answers = [True]
    env.page.click('#btn-save')
    env.wait_status('Board rebooted')
    assert b'ff-saved' in env.board.card.read('/config.txt')
    wait_boot(env, 2)
    env.page.click('#btn-connect')
    env.wait_status('Config loaded from board')
    assert env.val('#bi-cfgname') == 'ff-saved'


def test_firefox_status_polling(fx):
    env = fx.open().connect()
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text('STEP400')


def test_firefox_download(fx):
    env = fx.open().connect()
    name, d = env.download()
    assert d['information']['targetProduct'] == 'STEP400'
