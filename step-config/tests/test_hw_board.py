"""B: the boards alone (USB serial + OSC), no browser. Needs both boards: pytest -m hw.

The motors are NOT driven: the motor power must be off. Only G T F { R are sent over USB and only
the OSC addresses of hw_protocol.OSC_ALLOWED. Every test that changes a setting puts the board
back (Hw.restore) and the session restores both boards from the backup taken at the start.
"""
import copy
import json
import threading
import time

import pytest

import hw_protocol as hp

pytestmark = pytest.mark.hw


def osc_ok(board, timeout=4.0):
    """True when the board answers an OSC query within `timeout` (asked every 0.3 s)."""
    t0 = time.monotonic()
    while time.monotonic() - t0 < timeout:
        if board.osc_query('/getVersion', timeout=0.3):
            return True
    return False


def restore_after(hw, board):
    d = hw.restore(board)
    assert not d, d


# ------------------------------------------------------------------ 3.9 OSC during a save
class Stream:
    """Sends /getPosition every 20 ms and records when the replies arrive."""

    def __init__(self, board, interval=0.02):
        self.b = board
        self.interval = interval
        self.sent = []
        self.got = []
        self._stop = threading.Event()
        self.sock = board.osc()
        self.sock.flush()

    def _tx(self):
        nxt = time.monotonic()
        while not self._stop.is_set():
            self.b.osc_send('/getPosition', 1)
            self.sent.append(time.monotonic())
            nxt += self.interval
            time.sleep(max(0, nxt - time.monotonic()))

    def _rx(self):
        while not self._stop.is_set():
            r = self.sock.recv(0.01)
            if r and r[2] == self.b.my_ip and r[0] == '/position':
                self.got.append(r[3])

    def __enter__(self):
        self.th = [threading.Thread(target=self._tx), threading.Thread(target=self._rx)]
        for t in self.th:
            t.start()
        time.sleep(0.3)
        return self

    def __exit__(self, *a):
        time.sleep(0.3)
        self._stop.set()
        for t in self.th:
            t.join()

    def max_gap(self, t0, t1):
        ts = [t for t in self.got if t0 - 0.1 <= t <= t1 + 0.4]
        return max((b - a for a, b in zip(ts, ts[1:])), default=None)


def save_with_stream(board, cfg):
    with board.line() as ln, Stream(board) as st:
        ln.drain(0.05)
        t0 = time.monotonic()
        r = ln.send_config(cfg)
        t1 = time.monotonic()
        assert r and r['result'] == 'ok', r
        time.sleep(0.2)
    return dict(save_s=t1 - t0, max_gap_s=st.max_gap(t0, t1), n_replies=len(st.got), n_sent=len(st.sent))


@pytest.mark.checklist('3.9')
def test_osc_gap_during_a_save(hw, board):
    cfg = json.loads(json.dumps(board.refresh().G))
    runs = []
    # the first save after a start-up
    hp.reboot_and_wait(board)
    board.refresh()
    board.osc_set_dest()
    runs.append(dict(first_after_boot=True, **save_with_stream(board, cfg)))
    for _ in range(9):
        runs.append(dict(first_after_boot=False, **save_with_stream(board, cfg)))
    hw.rec(f'3.9 {board.product}', runs)
    gaps = [r['max_gap_s'] for r in runs]
    assert all(g is not None for g in gaps)
    assert max(gaps) < 1.5      # NOTES_v2.2.0 3: 0.1-0.7 s (this only guards against a stall)
    restore_after(hw, board)


# ------------------------------------------------------------------ IP: saved now, applied by a reboot
@pytest.mark.checklist('3.4', '3.6')
def test_ip_change_applies_only_after_a_reboot(hw, board):
    old_ip = board.refresh().my_ip
    cfg = copy.deepcopy(board.G)
    cfg['network']['myIp'][3] = 120
    new_ip = f'10.0.0.{120 + board.my_id}'
    with board.line() as ln:
        assert ln.send_config(cfg)['result'] == 'ok'
    G2 = None
    with board.line() as ln:
        G2, T2 = ln.get_config(), ln.get_status()
    assert G2['network']['myIp'][3] == 120                   # G: the saved value
    assert T2['board']['myIp'] == list(map(int, old_ip.split('.')))   # T: the running value
    # replies keep coming from the old IP (the time to the first one is recorded: after a `{`
    # the board was sometimes silent for a moment)
    t0 = time.monotonic()
    answered = None
    while time.monotonic() - t0 < 6:
        if board.osc_query('/getVersion', timeout=0.3):
            answered = time.monotonic() - t0
            break
    hw.rec(f'3.4 first OSC reply after the save {board.product}', answered)
    assert answered is not None, 'no OSC reply from the old IP'
    # the new address does not answer yet
    sock = board.osc()
    sock.flush()
    hp.OscPort.send_to(new_ip, board.in_port, '/getVersion')
    assert not sock.collect(new_ip, 0.7)
    hp.reboot_and_wait(board)
    board.refresh()
    assert board.my_ip == new_ip
    board.osc_set_dest()
    assert osc_ok(board), 'no OSC reply from the new IP'
    hw.rec(f'3.4 {board.product}', dict(old=old_ip, new=new_ip, G_after_save=G2['network']['myIp'],
                                        T_after_save=T2['board']['myIp']))
    restore_after(hw, board)
    assert osc_ok(board), 'no OSC reply from the old IP after the restore'
    assert board.my_ip == old_ip


# ------------------------------------------------------------------ F
NAME63 = '/' + 'a' * 57 + '.json'
assert len(NAME63) == 63


@pytest.mark.checklist('4.1', '4.2', '4.3')
def test_filename_rules(hw, board):
    cur = board.refresh().G['board']['configFilename']
    out = {}
    with board.line() as ln:
        out['63 bytes'] = ln.send_filename(NAME63)
        out['63 bytes, G'] = ln.get_config()['board']['configFilename']
        long_ = NAME63 + 'zzz'                                  # 66 bytes; cut to 63 = a valid name
        out['66 bytes (cut to 63)'] = ln.send_filename(long_)
        out['66 bytes (cut to 63), G'] = ln.get_config()['board']['configFilename']
        out['64 bytes ending .json'] = ln.send_filename('/' + 'b' * 58 + '.json')     # cut to .jso
        out['no leading /'] = ln.send_filename('config.txt')
        out['.csv'] = ln.send_filename('/a.csv')
        out['.JSON'] = ln.send_filename('/ABC.JSON')
        out['.txt'] = ln.send_filename('/foo.txt')
        out['empty'] = ln.send_filename('')
        out['G after the errors'] = ln.get_config()['board']['configFilename']
        ln.send_filename(cur)
    hw.rec(f'4.x F {board.product}', out)
    assert out['63 bytes'] == {'result': 'ok', 'configFilename': NAME63}
    assert out['63 bytes, G'] == NAME63
    assert out['66 bytes (cut to 63)']['configFilename'] == NAME63
    assert out['64 bytes ending .json']['result'] == 'error'
    assert out['no leading /']['message'] == 'Filename must start with /'
    assert out['.csv']['message'] == 'Filename must end with .json or .txt'
    assert out['.JSON']['result'] == 'ok'
    assert out['.txt']['result'] == 'ok'
    assert out['empty']['result'] == 'error'
    # an error does not change the name (the last valid one stays)
    assert out['G after the errors'] == '/foo.txt'
    assert board.refresh().G['board']['configFilename'] == cur


def test_save_63_byte_name_and_truncated_name_make_one_file(hw):
    """STEP400 only (the card is handled the same by both): saving to a 66-byte name saves under the
    63-byte prefix. Leaves NAME63 on the card."""
    b = hw.boards['STEP400']
    cfg = copy.deepcopy(b.refresh().G)
    with b.line() as ln:
        assert ln.send_filename(NAME63 + 'zzz')['configFilename'] == NAME63
        r = ln.send_config(cfg)
        name = ln.get_config()['board']['configFilename']
    hw.rec('4.1 truncated-name save', dict(result=r, configFilename=name))
    assert r['result'] == 'ok' and name == NAME63
    restore_after(hw, b)


# ------------------------------------------------------------------ { errors
@pytest.mark.checklist('8.7', '3.1')
def test_brace_errors_save_nothing(hw, board):
    G0 = board.refresh().G
    out = {}
    with board.line() as ln:
        # more than 4095 bytes before the closing brace (digits: the bytes the board drops or
        # reads afterwards are not commands)
        big = b'{"x":"' + b'0' * 5000 + b'"}'
        ln.drain(0.05)
        ln.send(big)
        o, _ = ln.json_line(5, want=lambda o: 'result' in o)
        out['too big'] = o
        time.sleep(0.5)
        ln.drain(0.3)
        # an unfinished one: the board times out after 10 s
        ln.send(b'{"network":{"myIp":[10,0,0,')
        t = time.monotonic()
        o, _ = ln.json_line(14, want=lambda o: 'result' in o)
        out['unfinished'] = o
        out['unfinished after s'] = time.monotonic() - t
        ln.drain(0.3)
        # balanced braces but not JSON
        o = ln.send_config(None, raw=b'{"network":{"myIp":[10,0,0,}}')
        out['broken'] = o
        o2 = ln.send_config(None, raw=b'{"network":{"myIp":"x","inPort":}}')
        out['broken 2'] = o2
        G1 = ln.get_config()
        out['T still answers'] = bool(ln.get_status())
    hw.rec(f'8.7 { {} } {board.product}'.replace(' {} ', ' '), out)
    assert out['too big']['message'] == 'Buffer overflow'
    assert out['unfinished']['message'] == 'Timeout'
    assert 9.5 < out['unfinished after s'] < 11.5
    assert out['broken'] == {'result': 'error', 'message': 'JSON parse failed'}, out['broken']
    assert G1 == G0
    assert board.refresh().G == G0


# ------------------------------------------------------------------ missing folder
@pytest.mark.checklist('4.4')
def test_missing_folder_says_sd_open_failed(hw, board):
    cur = board.refresh().G['board']['configFilename']
    with board.line() as ln:
        assert ln.send_filename('/sub/test.json')['result'] == 'ok'
        r = ln.send_config(copy.deepcopy(board.G))
        ln.send_filename(cur)
    hw.rec(f'4.4 {board.product}', r)
    assert r == {'result': 'error', 'message': 'SD open failed'}
    assert board.refresh().G['board']['configFilename'] == cur


# ------------------------------------------------------------------ 4.8 start-up order
@pytest.mark.checklist('4.8')
def test_config_txt_is_read_before_zzz_json(hw, board):
    cfg = copy.deepcopy(board.refresh().G)
    cfg['information']['configName'] = 'zzz'
    with board.line() as ln:
        assert ln.send_filename('/zzz.json')['result'] == 'ok'
        assert ln.send_config(cfg)['result'] == 'ok'
        assert ln.send_filename('/config.txt')['result'] == 'ok'
    hp.reboot_and_wait(board)
    board.refresh()
    board.osc_set_dest()
    r = board.osc_query('/getConfigName', timeout=1.0)
    hw.rec(f'4.8 {board.product}', dict(reply=r, G_name=board.G['information']['configName'],
                                        filename=board.G['board']['configFilename']))
    assert r and r[0][0] == '/configName'
    name, sd, opened, parsed, filename = r[0][1]
    assert (sd, opened, parsed) == (1, 1, 1)
    assert filename == '/config.txt' and name != 'zzz'
    restore_after(hw, board)


# ------------------------------------------------------------------ brake enable
@pytest.mark.checklist('3.1')
def test_brake_enable_change_is_saved_and_reflected(hw, board):
    """Motors off. enableElectromagnetBrake() (oscListeners.cpp) changes only while the driver is
    HiZ (and, to disable, while the brake is engaged or free). Expected: motor 1 goes
    false -> true, G shows it, no warning on USB. Result only."""
    cfg = copy.deepcopy(board.refresh().G)
    cfg['driverSettings']['electromagnetBrakeEnable'][0] = True
    with board.line() as ln:
        ln.drain(0.05)
        ln.send(json.dumps(cfg, separators=(',', ':')).encode())
        o, others = ln.json_line(5, want=lambda o: 'result' in o)
        time.sleep(0.3)
        extra = ln.drain(0.3).decode('utf-8', 'replace')
        g = ln.get_config()
        t = ln.get_status()
    hw.rec(f'3.1 brake {board.product}', dict(
        result=o, usb_other_lines=[x.decode('utf-8', 'replace') for x in others] + [extra],
        G=g['driverSettings']['electromagnetBrakeEnable'], T_motor1=t['motors'][0]))
    assert o['result'] == 'ok'
    # whatever happened is recorded; the expectation from the source is that it is applied
    assert g['driverSettings']['electromagnetBrakeEnable'][0] is True
    restore_after(hw, board)
    assert board.G['driverSettings']['electromagnetBrakeEnable'][0] is False


# ------------------------------------------------------------------ 10.1 R
@pytest.mark.checklist('10.1')
def test_reboot_timing(hw, board):
    runs = []
    for _ in range(3):
        r = hp.reboot_and_wait(board)
        board.osc_set_dest()
        runs.append({k: r.get(k) for k in ('reply', 'gone', 'back', 'opened', 't_answers',
                                            'name_before', 'name_after', 'startup_lines')})
        assert r['reply_json'] == {'result': 'ok', 'message': 'Rebooting...'}
        assert r['T']['board']['resetCause'] == 5
    hw.rec(f'10.1 {board.product}', runs)
    assert all(x['name_before'] == x['name_after'] for x in runs)
    assert all(x['gone'] is not None for x in runs)
    assert all(x['reply'] < 0.5 for x in runs)
