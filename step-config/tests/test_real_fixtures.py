"""The fake board against the answers of the real boards (fixtures/real/, taken at stage 2 from
STEP400 and STEP800 with firmware v2.2.0): same keys, same order, same value types, same number
format. Needs no hardware."""
import json
from collections import OrderedDict

import pytest

from fake_board import FakeBoard, Card, REAL_DIR


def shape(o, path=''):
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            out += shape(v, path + '/' + k)
    elif isinstance(o, list):
        out.append((path, 'list', tuple(sorted({type(x).__name__ for x in o})), len(o)))
    else:
        out.append((path, type(o).__name__))
    return out


def load(text):
    return json.loads(text, object_pairs_hook=OrderedDict)


@pytest.fixture(params=['STEP400', 'STEP800'])
def pair(request):
    real = json.loads((REAL_DIR / f'{request.param}_sd_ok.json').read_text())
    fake = FakeBoard(request.param, card=Card('fat32', {'/config.txt': b'{"information":{"configVersion":[-1,0]}}'}))
    return real, fake


def test_g_has_the_keys_order_and_types_of_the_real_board(pair):
    real, fake = pair
    assert shape(load(real['G_raw'])) == shape(load(fake.config_json()))


def test_t_has_the_keys_order_and_types_of_the_real_board(pair):
    real, fake = pair
    assert shape(load(real['T_raw'])) == shape(load(fake.status_json()))


def test_g_text_format_is_compact_like_the_firmware(pair):
    real, fake = pair
    assert real['G_raw'].strip() == json.dumps(json.loads(real['G_raw']), separators=(',', ':'))
    assert fake.config_json() == json.dumps(json.loads(fake.config_json()), separators=(',', ':'))


def test_default_values_are_those_of_the_firmware(pair):
    real, fake = pair
    backup = json.loads((REAL_DIR / f'{fake.product}_no_config_file_backup.json').read_text())['G']
    g = json.loads(fake.config_json())
    for sec in backup:
        if sec in ('board', 'information'):
            continue
        assert g[sec] == backup[sec], sec


def test_t_board_values_of_the_real_board_are_as_the_fake_guessed(pair):
    real, fake = pair
    rb, fb = real['T']['board'], json.loads(fake.status_json())['board']
    assert rb['mcu'] == fb['mcu'] == 'SAMD21'
    assert rb['destMac'] == fb['destMac'] == [255] * 6
    assert rb['arpPending'] is fb['arpPending'] is False
    # after R the real board reports a software reset
    assert real['T_after_reboot']['board']['resetCause'] == 5
    assert real['T_after_reboot']['board']['resetCauseRaw'] == 64
