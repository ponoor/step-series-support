"""Checklist sections 9 and 11: Load / Download JSON (offline), other browsers, dark mode."""
import json
import re

import pytest
from playwright.sync_api import expect

from testlib import TEMPLATES, tmpl, make_card, Card, poll_until, wait_boot


def luminance(rgb):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


@pytest.fixture
def offline(make_env):
    """No board: the shim is loaded but never connected."""
    return make_env('STEP400').open()


def write_json(tmp_path, name, data):
    p = tmp_path / name
    p.write_text(json.dumps(data))
    return p


# ------------------------------------------------------------------ 9
@pytest.mark.checklist('9.1')
def test_load_step800_template(offline):
    env = offline
    env.load_file(TEMPLATES / 'configTemplate_step800.json')
    env.wait_status('Loaded from file: configTemplate_step800.json')
    assert env.val('#bi-axes-sel') == '8'
    assert env.page.locator('#bi-axes-sel').is_visible()
    assert len(env.header_cells('#alarm-tbl')) == 9
    o = env.options('#f-alarm-OCThreshold-0')
    assert len(o) == 16 and o[1][1] == '750 mA (1)'                  # 375 mA steps: targetProduct STEP800
    assert not any('Slew rate' in r for r in env.visible_rows('#driver-tbl'))   # no slewRate key in the template
    assert env.page.locator('#bi-product').inner_text() == '—'
    assert env.page.locator('#bi-target').inner_text() == 'STEP800'


@pytest.mark.checklist('9.2')
def test_load_step400_template_with_old_spelling(offline, tmp_path):
    d = tmpl('STEP400')
    d['driverSettings']['goUnitlTimeout'] = d['driverSettings'].pop('goUntilTimeout')   # an old file
    d['driverSettings']['goUnitlTimeout'] = [11111, 22222, 33333, 44444]
    p = write_json(tmp_path, 'typo.json', d)
    env = offline
    env.load_file(p)
    env.wait_status('Loaded from file: typo.json')
    assert env.val('#bi-axes-sel') == '4'
    assert len(env.header_cells('#driver-tbl')) == 5
    assert [env.val(f'#f-driver-goUntilTimeout-{i}') for i in range(4)] == ['11111', '22222', '33333', '44444']
    assert env.options('#f-alarm-OCThreshold-0')[1][1] == '625 mA (1)'       # 312.5 mA steps


@pytest.mark.checklist('9.2')
def test_load_step400_template_new_spelling(offline):
    env = offline
    env.load_file(TEMPLATES / 'configTemplate_step400.json')
    env.wait_status('Loaded from file: configTemplate_step400.json')
    assert len(env.header_cells('#driver-tbl')) == 5
    assert [env.val(f'#f-driver-goUntilTimeout-{i}') for i in range(4)] == ['10000'] * 4


@pytest.mark.checklist('9.3')
def test_download_content(offline, tmp_path):
    env = offline
    env.load_file(TEMPLATES / 'configTemplate_step400.json')
    env.wait_status('Loaded from file')
    env.set('#f-speed-acc-0', 1234.5)
    env.set('#bi-cfgname', 'dl test')
    name, d = env.download()
    assert name == 'configTemplate_step400.json'
    ds = d['driverSettings']
    assert 'goUntilTimeout' in ds and 'goUnitlTimeout' not in ds
    assert d['information']['configVersion'] == [1, 2]
    assert d['information']['targetProduct'] == 'STEP400'
    assert d['information']['configName'] == 'dl test'
    assert ds['homingDirection'] == [False] * 4
    assert all(isinstance(v, bool) for v in ds['homingDirection'])
    assert d['speedProfile']['acc'][0] == 1234.5
    assert 'currentMode' in d and 'servoMode' in d


@pytest.mark.checklist('9.3')
def test_download_is_tab_indented_and_uses_the_save_name(offline):
    env = offline
    env.load_file(TEMPLATES / 'configTemplate_step800.json')
    env.wait_status('Loaded from file')
    env.fn('/My Config.json')
    name, d = env.download()
    assert name == 'My Config.json'
    with env.page.expect_download() as dl:
        env.page.click('#btn-download')
    text = open(dl.value.path()).read()
    assert text.startswith('{\n\t"information"')


@pytest.mark.checklist('9.4')
@pytest.mark.parametrize('product', ['STEP400', 'STEP800'])
def test_file_without_information_gets_version_and_target(offline, tmp_path, product):
    d = tmpl(product)
    del d['information']
    env = offline
    env.load_file(write_json(tmp_path, 'noinfo.json', d))
    env.wait_status('Loaded from file: noinfo.json')
    _, out = env.download()
    assert out['information']['configVersion'] == [1, 2]
    assert out['information']['targetProduct'] == product              # guessed from the number of axes
    assert out['information']['configName'] == ''


@pytest.mark.checklist('9.7')
def test_axes_reselect_keeps_values_of_existing_columns(offline, tmp_path):
    d = tmpl('STEP400')
    d['speedProfile']['acc'] = [101, 102, 103, 104]
    env = offline
    env.load_file(write_json(tmp_path, 'four.json', d))
    env.wait_status('Loaded from file')
    env.page.select_option('#bi-axes-sel', '8')
    assert len(env.header_cells('#speed-tbl')) == 9
    assert [env.val(f'#f-speed-acc-{i}') for i in range(4)] == ['101', '102', '103', '104']
    assert env.val('#f-speed-acc-4') == '0'                              # new columns are empty
    env.page.select_option('#bi-axes-sel', '2')
    assert len(env.header_cells('#speed-tbl')) == 3
    assert [env.val(f'#f-speed-acc-{i}') for i in range(2)] == ['101', '102']
    env.page.select_option('#bi-axes-sel', '4')
    assert [env.val(f'#f-speed-acc-{i}') for i in range(4)] == ['101', '102', '103', '104']


@pytest.mark.checklist('9.7')
def test_axes_reselect_discards_unsaved_edits(offline, tmp_path):
    """Observation: the tables are rebuilt from the loaded file, so an edit is lost when the
    number of axes is changed. (The checklist asks only that the file's values stay.)"""
    env = offline
    env.load_file(TEMPLATES / 'configTemplate_step400.json')
    env.wait_status('Loaded from file')
    env.set('#f-speed-acc-0', 4242)
    env.page.select_option('#bi-axes-sel', '8')
    assert env.val('#f-speed-acc-0') == '2000'


@pytest.mark.checklist('9.8')
def test_download_without_a_config_says_load_first(offline):
    env = offline
    with pytest.raises(Exception):
        with env.page.expect_download(timeout=1200):
            env.page.click('#btn-download')
    assert 'Load a config first.' in env.err()


@pytest.mark.checklist('9.8')
def test_save_with_no_config_loaded_is_not_possible_offline(offline):
    assert offline.page.locator('#btn-save').is_disabled()


def test_bad_json_file_is_reported(offline, tmp_path):
    p = tmp_path / 'bad.json'
    p.write_text('{ not json')
    offline.load_file(p)
    offline.wait_err('JSON parse failed')


def test_downloaded_file_is_accepted_by_the_start_up_rules(make_env, tmp_path):
    """Extra (fake board): a downloaded file put on the card as /test_offline.json (and with
    config.txt gone) is the file read at the next start-up. The real check is stage 3 (D)."""
    env = make_env('STEP400').open()
    env.load_file(TEMPLATES / 'configTemplate_step400.json')
    env.wait_status('Loaded from file')
    env.set('#f-speed-acc-0', 1357)
    env.set('#bi-cfgname', 'offline name')
    _, d = env.download()
    card = Card('fat32', {'/test_offline.json': json.dumps(d, indent='\t').encode()})
    brd = env.board
    brd.card = card
    brd._boot()
    assert brd.config_filename == '/test_offline.json' and brd.config_file_parse
    assert brd.config_name == 'offline name'
    assert brd.cfg['speedProfile']['acc'][0] == 1357


# ------------------------------------------------------------------ 11
@pytest.mark.checklist('11.1')
def test_other_browsers_load_and_download_work(make_env, other_browser):
    env = make_env('STEP400', browser=other_browser, shim=False).open()
    env.load_file(TEMPLATES / 'configTemplate_step400.json')
    env.wait_status('Loaded from file')
    assert len(env.header_cells('#speed-tbl')) == 5
    name, d = env.download()
    assert d['information']['targetProduct'] == 'STEP400'
    env.shot(f'{other_browser.name_}_loaded_template')


@pytest.mark.checklist('11.1')
def test_other_browsers_without_web_serial_show_the_banner(make_env, other_browser, request):
    if other_browser.name_ == 'firefox':
        request.applymarker(pytest.mark.xfail(strict=True, reason=(
            '(d) checklist / (a) tool: Firefox 157 (Playwright build) has navigator.serial '
            '(getPorts, requestPort), so the tool shows no banner and Connect stays enabled. '
            'Needs a look in a real Firefox in stage 3 (what Connect does there)')))
    env = make_env('STEP400', browser=other_browser, shim=False).open()
    assert env.page.evaluate('navigator.serial') is None
    banner = env.page.locator('#no-serial')
    expect(banner).to_be_visible()
    assert 'Web Serial API is not available' in banner.inner_text()
    assert env.page.locator('#btn-connect').is_disabled()
    env.shot(f'{other_browser.name_}_no_web_serial')


@pytest.mark.checklist('11.2')
@pytest.mark.parametrize('product', ['STEP400', 'STEP800'])
def test_dark_mode_is_readable(make_env, product):
    env = make_env(product, scheme='dark', card=make_card(product)).open().connect()
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text(product)
    env.fn('/sub/x.json')
    env.page.evaluate("showErr('sample error text')")
    page = env.page
    data = page.evaluate("""() => {
      const rgb = s => s.match(/[\\d.]+/g).slice(0, 3).map(Number);
      const bg = e => { while (e) { const c = getComputedStyle(e).backgroundColor; if (!c.endsWith(', 0)') && c !== 'transparent') return c; e = e.parentElement; } return 'rgb(255,255,255)'; };
      const sel = ['body', '#toolbar h1', '#status-msg', '.ax-tbl td', '.ax-tbl thead th', 'summary',
                   '#err-banner', '#save-note', 'select', 'input[type=number]', '#sd-filename',
                   '#rt-board .badge', '.bi-grid .lbl', '.bi-grid .val', '#btn-read'];
      return sel.map(s => { const e = document.querySelector(s); const cs = getComputedStyle(e);
        return [s, rgb(cs.color), rgb(bg(e)), cs.opacity]; });
    }""")
    low = []
    for sel, fg, bg, _ in data:
        c = contrast(fg, bg)
        if c < 4.5:
            low.append((sel, fg, bg, round(c, 2)))
    assert not low, low
    assert page.evaluate("matchMedia('(prefers-color-scheme: dark)').matches")


@pytest.mark.checklist('11.2')
@pytest.mark.xfail(strict=True, reason='(a) tool, cosmetic: in dark mode the Connect button (primary) is '
                   'white on #58a6ff (2.5:1) and Disconnect (danger) white on #f85149 (3.4:1), below 4.5:1')
def test_dark_mode_connect_button_contrast(make_env):
    env = make_env('STEP400', scheme='dark').open()
    js = """() => { const e = document.querySelector('#btn-connect'); const cs = getComputedStyle(e);
        const n = s => s.match(/[\\d.]+/g).slice(0, 3).map(Number); return [n(cs.color), n(cs.backgroundColor)]; }"""
    fg, bg = env.page.evaluate(js)
    c1 = contrast(fg, bg)
    env.connect()
    fg, bg = env.page.evaluate(js)
    c2 = contrast(fg, bg)
    assert min(c1, c2) >= 4.5, (round(c1, 2), round(c2, 2))
