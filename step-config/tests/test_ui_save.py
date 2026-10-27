"""Checklist sections 3, 4 and 5: saving, file names, errors of the card."""
import json
import time

import pytest
from playwright.sync_api import expect

from testlib import (make_card, card_cfg, tmpl, sent_json, Card, RED, ORANGE, NORMAL,
                     poll_until, wait_boot)

LONG_OK = '/' + 'x' * 57 + '.json'          # 63 bytes
assert len(LONG_OK.encode()) == 63


def fn_color(env):
    return env.page.eval_on_selector('#sd-filename', 'e => getComputedStyle(e).borderColor')


def save_expect_nothing_sent(env):
    m = env.backend.mark()
    env.page.click('#btn-save')
    time.sleep(0.4)
    return env.backend.sent(m)


# ------------------------------------------------------------------ 3
@pytest.mark.checklist('3.1', '3.2')
def test_change_values_and_save(make_env):
    env = make_env('STEP400', card=make_card('STEP400')).open().connect()
    env.set('#net-myIp-3', 110)
    env.set('#bi-cfgname', 'tooltest')
    env.page.check('#f-alarm-reportBUSY-0')
    env.dialogs.answers = [False]
    m = env.backend.mark()
    env.page.click('#btn-save')
    env.wait_status("✓ Saved to SD. Reboot (send 'R') to apply.")
    assert env.dialogs.messages == ['Config saved.\n\nReboot now to apply changes?']
    sent = env.backend.sent(m)
    assert sent.startswith('F/config.txt\n{')
    cfg = sent_json(env.backend, m)
    assert cfg['network']['myIp'] == [10, 0, 0, 110]
    assert cfg['information']['configName'] == 'tooltest'
    assert cfg['alarmAndReport']['reportBUSY'] == [True, False, False, False]
    # the file on the card: one line, compact, the saved values
    data = env.board.card.read('/config.txt').decode()
    assert data.count('\n') == 1 and data.endswith('}\n')
    assert json.loads(data)['information']['configName'] == 'tooltest'
    assert json.loads(data)['network']['myIp'] == [10, 0, 0, 110]


@pytest.mark.checklist('3.3', '3.4')
def test_cancel_reboot_ip_unchanged_read_shows_saved(make_env):
    env = make_env('STEP400', card=make_card('STEP400')).open().connect()
    env.set('#net-myIp-3', 110)
    env.set('#bi-cfgname', 'tooltest')
    env.dialogs.answers = [False]
    env.page.click('#btn-save')
    env.wait_status('Saved to SD')
    assert env.board.boot_count == 1
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text('10.0.0.100')      # running IP unchanged
    env.page.click('#btn-poll')
    env.set('#net-myIp-3', 5)
    env.set('#bi-cfgname', 'x')
    env.page.click('#btn-read')
    env.wait_status('Config loaded from board')
    time.sleep(0.2)
    assert env.val('#net-myIp-3') == '110'
    assert env.val('#bi-cfgname') == 'tooltest'


@pytest.mark.checklist('3.5', '3.6', '10.1', '10.2')
def test_save_reboot_connect_shows_saved_values_and_new_ip(make_env):
    env = make_env('STEP400', card=make_card('STEP400'), boot_time=0.4).open().connect()
    env.expect_unplug()
    env.set('#net-myIp-3', 110)
    env.set('#bi-cfgname', 'tooltest')
    env.dialogs.answers = [True]             # reboot now
    env.page.click('#btn-save')
    env.wait_status('Board rebooted — click Connect to reconnect.')
    assert env.page.locator('#btn-connect').inner_text() == '⬡ Connect'
    wait_boot(env, 2)
    env.page.click('#btn-connect')
    env.wait_status('Config loaded from board')
    assert env.val('#net-myIp-3') == '110'
    assert env.val('#bi-cfgname') == 'tooltest'
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text('10.0.0.110')       # the running IP changed
    assert env.board.config_filename == '/config.txt'


# ------------------------------------------------------------------ 4
@pytest.mark.checklist('4.1')
@pytest.mark.parametrize('name', [LONG_OK, '/STEP400_test_with_a_long_file_name_0123456789.json'])
def test_long_name_up_to_63_bytes(make_env, name):
    assert len(name.encode()) <= 63
    card = make_card('STEP400')
    before = card.read('/config.txt')
    env = make_env('STEP400', card=card).open().connect()
    env.fn(name)
    assert fn_color(env) == NORMAL
    env.dialogs.answers = [False]
    m = env.backend.mark()
    env.page.click('#btn-save')
    env.wait_status('Saved to SD')
    assert env.backend.sent(m).startswith('F' + name + '\n')
    assert env.board.card.read(name) is not None
    assert env.board.card.read('/config.txt') == before


@pytest.mark.checklist('4.2')
@pytest.mark.parametrize('name', ['/' + 'x' * 58 + '.json', '/' + 'x' * 60 + '.json'])
def test_name_64_bytes_or_more_is_red_and_nothing_is_sent(make_env, name):
    env = make_env('STEP400').open().connect()
    env.fn(name)
    assert fn_color(env) == RED
    n = len(name.encode())
    assert n >= 64
    assert save_expect_nothing_sent(env) == ''
    assert f'File name is {n} bytes long' in env.err() or f'is {n} bytes long' in env.err()
    assert env.status() == 'Save failed'


@pytest.mark.checklist('4.2')
def test_name_with_multibyte_characters_counted_in_bytes(make_env):
    env = make_env('STEP400').open().connect()
    name = '/' + 'あ' * 20 + '.json'            # 20 characters, 66 bytes
    assert len(name) < 64 < len(name.encode())
    env.fn(name)
    assert fn_color(env) == RED
    assert save_expect_nothing_sent(env) == ''
    assert 'bytes long' in env.err()


@pytest.mark.checklist('4.3')
@pytest.mark.parametrize('name,msg', [
    ('config.txt', 'must start with "/"'),
    ('/a.csv', 'must end with .json or .txt'),
    ('/', 'must start with "/"'),
])
def test_bad_names_are_red_and_nothing_is_sent(make_env, name, msg):
    env = make_env('STEP400').open().connect()
    env.fn(name)
    assert fn_color(env) == RED
    assert save_expect_nothing_sent(env) == ''
    assert msg in env.err()


@pytest.mark.checklist('4.4')
def test_subfolder_orange_cancel_then_ok(make_env):
    env = make_env('STEP400', card=make_card('STEP400')).open().connect()
    env.fn('/sub/test.json')
    assert fn_color(env) == ORANGE
    env.dialogs.answers = [False]
    assert save_expect_nothing_sent(env) == ''
    assert env.dialogs.messages[-1].startswith('"/sub/test.json" is in a subfolder')
    assert 'Save anyway?' in env.dialogs.messages[-1]
    assert env.status() == 'Save cancelled'
    # OK: sent; the folder does not exist -> SD open failed (with the hint)
    env.dialogs.answers = [True]
    m = env.backend.mark()
    env.page.click('#btn-save')
    env.wait_err('Save failed: SD open failed')
    assert env.backend.sent(m).startswith('F/sub/test.json\n{')
    assert 'folder of the file name does not exist' in env.err()
    assert env.board.boot_count == 1


@pytest.mark.checklist('4.4')
def test_subfolder_that_exists_saves(make_env):
    card = make_card('STEP400')
    card.dirs.add('/sub')
    env = make_env('STEP400', card=card).open().connect()
    env.fn('/sub/test.json')
    env.dialogs.answers = [True, False]
    env.page.click('#btn-save')
    env.wait_status('Saved to SD')
    assert card.read('/sub/test.json') is not None


@pytest.mark.checklist('4.5')
def test_txt_other_than_config_is_orange_with_confirm(make_env):
    env = make_env('STEP400', card=make_card('STEP400')).open().connect()
    env.fn('/foo.txt')
    assert fn_color(env) == ORANGE
    env.dialogs.answers = [False]
    assert save_expect_nothing_sent(env) == ''
    assert '.txt file other than /config.txt' in env.dialogs.messages[-1]
    env.dialogs.answers = [True, False]
    env.page.click('#btn-save')
    env.wait_status('Saved to SD')
    assert env.board.card.read('/foo.txt') is not None


@pytest.mark.checklist('4.6')
def test_hidden_name_is_orange_with_confirm(make_env):
    env = make_env('STEP400', card=make_card('STEP400')).open().connect()
    env.fn('/.hidden.json')
    assert fn_color(env) == ORANGE
    env.dialogs.answers = [False]
    assert save_expect_nothing_sent(env) == ''
    assert 'starts with "."' in env.dialogs.messages[-1]


@pytest.mark.checklist('4.7')
def test_config_txt_and_uppercase_extension_have_no_warning(make_env):
    env = make_env('STEP400', card=make_card('STEP400')).open().connect()
    for name in ('/config.txt', '/ABC.JSON', '/Config.TXT'.replace('Config', 'config'), '/abc.Json'):
        env.fn(name)
        assert fn_color(env) == NORMAL, name
    env.fn('/ABC.JSON')
    env.dialogs.answers = [False]                  # only the "reboot now?" question
    env.page.click('#btn-save')
    env.wait_status('Saved to SD')
    assert env.dialogs.messages == ['Config saved.\n\nReboot now to apply changes?']
    assert env.board.card.read('/ABC.JSON') is not None


@pytest.mark.checklist('4.9')
def test_load_json_with_spaces_in_name_saves_under_that_name(make_env, tmp_path):
    f = tmp_path / 'My Config.json'
    d = tmpl('STEP400')
    d['information']['configName'] = 'spaced'
    f.write_text(json.dumps(d))
    env = make_env('STEP400', card=make_card('STEP400'), boot_time=0.3).open().connect()
    env.expect_unplug()
    env.load_file(f)
    env.wait_status('Loaded from file: My Config.json')
    assert env.val('#sd-filename') == '/My Config.json'
    assert fn_color(env) == NORMAL
    env.dialogs.answers = [True]
    m = env.backend.mark()
    env.page.click('#btn-save')
    env.wait_status('Board rebooted')
    assert env.backend.sent(m).startswith('F/My Config.json\n')
    assert env.board.card.read('/My Config.json') is not None
    # config.txt is read first at the next start-up, so the spaced name is only a file on the card
    wait_boot(env, 2)
    assert env.board.config_filename == '/config.txt'


@pytest.mark.checklist('4.9')
def test_spaced_file_is_read_at_startup_when_it_is_the_only_json(make_env, tmp_path):
    d = tmpl('STEP400')
    d['information']['configName'] = 'spaced'
    card = make_card(files={'/My Config.json': d})
    env = make_env('STEP400', card=card).open().connect()
    assert env.board.config_filename == '/My Config.json'
    assert env.val('#sd-filename') == '/My Config.json'
    assert env.val('#bi-cfgname') == 'spaced'


# ------------------------------------------------------------------ 5
@pytest.mark.checklist('5.1', '13.7', '2.3')
def test_no_card_read_works_save_says_no_sd_card(make_env):
    env = make_env('STEP400', card=Card('none')).open().connect()
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text('ERR')
    env.page.click('#btn-poll')
    env.dialogs.answers = []
    env.page.click('#btn-save')
    env.wait_err('Save failed: No SD card')
    e = env.err()
    assert 'Is a card inserted, and formatted as FAT16 or FAT32 (exFAT cannot be used)?' in e
    assert 'restart it after inserting a card' in e
    assert env.status() == 'Save failed'
    assert env.board.boot_count == 1


@pytest.mark.checklist('5.2', '13.9')
def test_exfat_card_says_no_card_with_exfat_hint(make_env):
    env = make_env('STEP400', card=Card('exfat')).open().connect()
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text('ERR')
    env.page.click('#btn-poll')
    env.page.click('#btn-save')
    env.wait_err('Save failed: No SD card')
    assert 'exFAT cannot be used' in env.err()


@pytest.mark.checklist('5.3', '13.8')
def test_card_removed_after_startup_says_sd_open_failed(make_env):
    env = make_env('STEP400', card=make_card('STEP400')).open().connect()
    env.board.card.remove()
    env.page.click('#btn-save')
    env.wait_err('Save failed: SD open failed')
    e = env.err()
    assert 'The card was removed after start-up, the card is full, or the folder' in e
    assert 'does not exist' in e
    assert env.board.boot_count == 1                 # the board does not restart


@pytest.mark.checklist('5.4')
def test_card_put_back_needs_a_restart(make_env):
    env = make_env('STEP400', card=make_card('STEP400'), boot_time=0.3).open().connect()
    env.expect_unplug()
    card = env.board.card
    card.remove()
    env.page.click('#btn-save')
    env.wait_err('SD open failed')
    card.insert()
    time.sleep(0.5)
    env.page.click('#btn-save')
    env.wait_status('Save failed')
    env.wait_err('SD open failed')
    # after a restart the card is read again and saving works
    env.dialogs.answers = [True]
    env.board.card.insert()
    env.page.click('#btn-reboot')
    env.wait_status('Board rebooted')
    wait_boot(env, 2)
    env.page.click('#btn-connect')
    env.wait_status('Config loaded from board')
    env.dialogs.answers = [False]
    env.page.click('#btn-save')
    env.wait_status('Saved to SD')


@pytest.mark.checklist('5.5')
@pytest.mark.parametrize('state', ['none', 'exfat'])
def test_tool_does_not_freeze_after_a_save_error(make_env, state):
    env = make_env('STEP400', card=Card(state)).open().connect()
    env.page.click('#btn-save')
    env.wait_err('Save failed')
    assert env.page.evaluate('isSaving') is False
    for b in ('btn-read', 'btn-save', 'btn-reboot', 'btn-poll'):
        assert env.page.locator('#' + b).is_enabled(), b
    env.page.click('#btn-read')
    env.wait_status('Config loaded from board')
    env.page.click('#btn-poll')
    expect(env.page.locator('#rt-board')).to_contain_text('STEP400')
    env.page.click('#btn-save')                     # and a second save works the same way
    env.wait_err('Save failed')


@pytest.mark.checklist('5.5')
def test_filename_rejected_by_board_is_reported(make_env):
    """The board's own check (not reachable from the UI because the tool checks first)."""
    env = make_env('STEP400').open().connect()
    env.page.evaluate("document.getElementById('sd-filename').value = '/x.json'")
    # make the board refuse: a name the tool accepts but the board does not
    orig = env.board.config_filename
    async def refuse():
        await env.board._out('{"result":"error","message":"Filename must start with /"}')
    env.board._cmd_F = refuse
    env.page.click('#btn-save')
    env.wait_err('Filename rejected: Filename must start with /')
    assert env.page.evaluate('isSaving') is False


@pytest.mark.checklist('5.5')
def test_json_parse_failed_from_board_is_reported(make_env):
    env = make_env('STEP400').open().connect()
    async def reject():
        await env.board._out('{"result":"error","message":"JSON parse failed"}')
    env.board._save = reject
    env.page.click('#btn-save')
    env.wait_err('Save failed: JSON parse failed')
    assert env.page.evaluate('isSaving') is False
