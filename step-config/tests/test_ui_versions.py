"""Checklist section 13: versions, firmware notices, the save note, OCD / Stall."""
import pytest
from playwright.sync_api import expect

from testlib import make_card


NOTICE_OLD = 'This tool requires firmware v2.1.0 or later (this board: v{v}).'
NOTICE_NEW = 'This tool was checked with firmware v2.2.0. Some settings of firmware v{v} may not be shown.'


@pytest.mark.checklist('13.1')
def test_version_text_in_the_heading(env400):
    env400.open()
    assert env400.page.locator('#tool-ver').inner_text() == 'v2.1.0 · checked with firmware v2.2.0'
    assert env400.page.locator('h1').inner_text().startswith('STEP Series Config Tool')


@pytest.mark.checklist('13.2')
@pytest.mark.parametrize('product', ['STEP400', 'STEP800'])
def test_no_notice_for_v220(make_env, product):
    env = make_env(product).open().connect()
    assert env.err() == ''


@pytest.mark.checklist('13.3')
def test_no_notice_for_v210(make_env):
    env = make_env('STEP400', fw=(2, 1, 0)).open().connect()
    assert env.err() == ''
    assert env.page.locator('#bi-fw').inner_text() == '2.1.0'


@pytest.mark.checklist('13.3')
@pytest.mark.parametrize('fw', [(2, 0, 0), (1, 9, 9), (2, 0, 7)])
def test_notice_for_older_firmware(make_env, fw):
    env = make_env('STEP400', fw=fw).open().connect()
    env.wait_err('This tool requires firmware v2.1.0 or later')
    assert NOTICE_OLD.format(v='.'.join(map(str, fw))) in env.err()


@pytest.mark.checklist('13.3', '13.4')
@pytest.mark.parametrize('fw', [(2, 3, 0), (3, 0, 0)])
def test_notice_for_newer_firmware_from_a_board(make_env, fw):
    env = make_env('STEP800', fw=fw).open().connect()
    env.wait_err('This tool was checked with firmware v2.2.0')
    assert NOTICE_NEW.format(v='.'.join(map(str, fw))) in env.err()


@pytest.mark.checklist('13.4')
def test_firmware_notice_function(env400):
    env = env400.open()
    f = lambda fw: env.page.evaluate('fw => firmwareNotice(fw)', fw)
    assert f([2, 3, 0]) == NOTICE_NEW.format(v='2.3.0')
    assert f([2, 2, 5]) == ''
    assert f([2, 2, 0]) == ''
    assert f([2, 1, 0]) == ''
    assert f([2, 1, 9]) == ''
    assert f([2, 0, 9]) == NOTICE_OLD.format(v='2.0.9')
    assert f([3, 0, 0]) == NOTICE_NEW.format(v='3.0.0')
    assert f([1, 9, 0]) == NOTICE_OLD.format(v='1.9.0')
    # input that is not a version: no notice
    for bad in (None, [], [2], ['2', '3'], [2.5, 1], 'x'):
        assert f(bad) == '', bad


@pytest.mark.checklist('13.4')
def test_firmware_notice_called_in_the_page_console_way(env400):
    """The checklist calls firmwareNotice() from the developer console."""
    env = env400.open()
    assert 'v2.3.0 may not be shown' in env.page.evaluate('firmwareNotice([2,3,0])')
    assert env.page.evaluate('firmwareNotice([2,2,5])') == ''


@pytest.mark.checklist('13.5')
def test_save_note(env400):
    env = env400.open()
    t = env.page.locator('#save-note').inner_text()
    assert t == 'Save to SD: the board stops processing for about 0.1–0.7 s while it saves. Stop the motors first.'
    assert env.page.locator('#save-note').is_visible()


@pytest.mark.checklist('13.6')
@pytest.mark.parametrize('product,axes', [('STEP400', 4), ('STEP800', 8)])
def test_ocd_and_stall_are_not_reported(make_env, product, axes):
    env = make_env(product, card=make_card(product)).open().connect()
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text(product)
    for label in ('OCD', 'Stall'):
        cells = env.page.locator(f'#rt-motors tbody tr:has(td:text-is("{label}")) td')
        assert cells.count() == axes + 1
        for i in range(1, axes + 1):
            b = cells.nth(i).locator('.badge')
            assert b.inner_text() == 'not reported'
            assert 'b-off' in b.get_attribute('class')
            assert 'b-ok' not in b.get_attribute('class')
    # the other rows are shown as before
    assert env.page.locator('#rt-motors tbody tr:has(td:text-is("Busy")) .badge.b-ok').count() == axes
    assert env.page.locator('#rt-motors tbody tr:has(td:text-is("UVLO")) .badge.b-ok').count() == axes
    rows = env.page.eval_on_selector_all('#rt-motors tbody tr', 'rs => rs.map(r => r.cells[0].innerText)')
    assert rows == ['Position', 'Speed (step/s)', 'Busy', 'HiZ', 'Direction', 'Motor Status', 'Thermal',
                    'UVLO', 'OCD', 'Stall', 'Home SW', 'Homing Status', 'Servo Mode']


@pytest.mark.checklist('13.6')
def test_ocd_stall_stay_not_reported_even_if_a_board_sent_true(make_env):
    env = make_env('STEP400').open().connect()
    orig = env.board.status_json
    import json as _j
    def patched():
        d = _j.loads(orig())
        for m in d['motors']:
            m['ocd'] = True
            m['stall'] = True
        return _j.dumps(d)
    env.board.status_json = patched
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text('STEP400')
    assert env.page.locator('#rt-motors .badge.b-err').count() == 0
    assert env.page.locator('#rt-motors tbody tr:has(td:text-is("OCD")) .badge').first.inner_text() == 'not reported'


@pytest.mark.checklist('13.7', '13.8', '13.9')
def test_save_error_hint_texts_exist_in_the_tool(env400):
    h = env400.open().page.evaluate('SAVE_ERROR_HINTS')
    assert h['No SD card'].startswith('Is a card inserted, and formatted as FAT16 or FAT32 (exFAT cannot be used)?')
    assert 'restart it after inserting a card' in h['No SD card']
    assert h['SD open failed'].startswith('The card was removed after start-up, the card is full, or the folder')
    assert 'does not exist' in h['SD open failed']


@pytest.mark.checklist('13.2')
def test_v220_board_connect_shows_no_firmware_text_in_status(env400):
    env = env400.open().connect()
    assert 'firmware' not in env.status().lower()
