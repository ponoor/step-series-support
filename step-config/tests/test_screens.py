"""Screenshots for looking at (out/screens/). The assertions only check that a file was written;
the images are looked at by a person / by Claude Code."""
import pytest
from playwright.sync_api import expect

from testlib import make_card, Card, OUT


def open_all(env):
    env.page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")


@pytest.mark.checklist('11.2')
@pytest.mark.parametrize('scheme', ['light', 'dark'])
@pytest.mark.parametrize('product', ['STEP400', 'STEP800'])
def test_screenshot_connected_with_status(make_env, product, scheme):
    env = make_env(product, scheme=scheme, card=make_card(product), viewport=(1400, 1000)).open().connect()
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text(product)
    open_all(env)
    p = env.shot(f'{product}_{scheme}_connected')
    assert p.stat().st_size > 20000


@pytest.mark.parametrize('scheme', ['light', 'dark'])
def test_screenshot_filename_states_and_errors(make_env, scheme):
    env = make_env('STEP400', scheme=scheme, card=make_card('STEP400')).open().connect()
    bar = env.page.locator('#toolbar')
    for tag, name in (('ok', '/config.txt'), ('red', '/a.csv'), ('orange', '/sub/test.json')):
        env.fn(name)
        env.page.locator('#toolbar').screenshot(path=str(OUT / 'screens' / f'filename_{tag}_{scheme}.png'))
    env.fn('/config.txt')
    env.set('#f-voltage-KVAL_RUN-0', 256)
    env.page.click('#btn-save')
    env.wait_err('Check the values')
    env.shot(f'error_range_{scheme}')


@pytest.mark.parametrize('scheme', ['light', 'dark'])
def test_screenshot_save_errors_from_the_card(make_env, scheme):
    env = make_env('STEP400', scheme=scheme, card=Card('exfat')).open().connect()
    env.page.click('#btn-save')
    env.wait_err('No SD card')
    env.shot(f'error_no_sd_card_{scheme}')


@pytest.mark.parametrize('scheme', ['light', 'dark'])
def test_screenshot_firmware_notice_and_unplug_banner(make_env, scheme):
    env = make_env('STEP800', scheme=scheme, fw=(2, 3, 0)).open().connect()
    env.expect_unplug()
    env.wait_err('This tool was checked with firmware v2.2.0')
    env.shot(f'firmware_notice_{scheme}')
    env.backend.disconnect(stay_unplugged=False)
    expect(env.page.locator('#dc-banner')).to_be_visible()
    env.shot(f'unplug_banner_{scheme}')


@pytest.mark.parametrize('scheme', ['light', 'dark'])
def test_screenshot_offline_start(make_env, scheme):
    env = make_env('STEP400', scheme=scheme).open(expand=False)
    env.shot(f'start_{scheme}')
