"""Tools to talk to real STEP400 / STEP800 boards (firmware v2.2.0) over USB serial and OSC.

Used by the board-only tests (test_hw_board.py), the tool + board tests (test_e2e_hw.py) and
guided.py. Command line:

    python hw_protocol.py ports                  # list the USB serial ports and tell the boards apart
    python hw_protocol.py backup                 # save G of every board to out/backup_<product>_<time>.json
    python hw_protocol.py --restore <backup>     # put a board back as in the backup, and check it
    python hw_protocol.py fixtures               # save G, T and the start-up lines to fixtures/real/

Safety: the only serial commands sent are G T F { R (never t, Z, W, ...). The OSC addresses that may
be sent are in OSC_ALLOWED; anything else raises OscNotAllowed *before* anything is sent. The list
holds the commands that only read (/get...) and the settings used in these tests. No command that
moves a motor, changes the brake or excitation, or resets the driver is in it.

Where the board sends its OSC replies (src/oscListeners.cpp, src/utils.cpp at v2.2.0):
  to destIp : outPort, never to the sender's address. destIp is the `network.destIp` of the
  configuration at start-up; `/setDestIp` (no argument) sets it to the sender's address and also
  sets isDestIpSet. Until then (and canSendMsgBeforeDestIp is false) most replies are not sent.
  outPort = network.outPort (+ myId when isOutPortAddId). inPort (receiving) is not changed by ID.
  myIp = network.myIp with the last byte + myId when isMyIpAddId (not above 254).
"""
import argparse
import datetime
import json
import os
import re
import select
import socket
import subprocess
import sys
import time

import serial
import serial.tools.list_ports
from pythonosc import osc_message_builder
from pythonosc.osc_message import OscMessage

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
FIXTURES = os.path.join(HERE, 'fixtures', 'real')
ARDUINO_VID = 0x2341

# ---------------------------------------------------------------- OSC allow-list
# Names checked in src/oscRoutes.h at v2.2.0.
OSC_ALLOWED_SET = {
    '/setDestIp',                  # no argument: destIp := sender
    '/setOverCurrentThreshold',    # motorId, value
    '/setStallThreshold',          # motorId, value
}
OSC_GET = re.compile(r'^/get[A-Za-z0-9_]*$')   # every /get... of the route table only reads
OSC_FORBIDDEN_HINT = ('run', 'move', 'goTo', 'goUntil', 'homing', 'releaseSw', 'Hiz', 'HiZ', 'Stop',
                      'activate', 'free', 'Brake', 'resetDevice', 'resetMotorDriver', 'saveConfig',
                      'setPosition', 'resetPos', 'Servo', 'goHome', 'goMark')


class allowed:
    """`with allowed('/run', ...):` adds addresses to the allow-list for the block only (guided.py,
    step 10.3, after the person confirmed that a motor is connected and powered)."""

    def __init__(self, *addresses):
        self.addresses = set(addresses)
        self.added = set()

    def __enter__(self):
        self.added = self.addresses - OSC_ALLOWED_SET
        OSC_ALLOWED_SET.update(self.added)
        return self

    def __exit__(self, *a):
        OSC_ALLOWED_SET.difference_update(self.added)


class OscNotAllowed(Exception):
    pass


class HwError(Exception):
    pass


def osc_allowed(address):
    return address in OSC_ALLOWED_SET or bool(OSC_GET.match(address))


def check_osc(address):
    if not osc_allowed(address):
        raise OscNotAllowed(f'OSC address not in the allow-list: {address}')


# ---------------------------------------------------------------- ports
def usb_ports():
    out = []
    for p in serial.tools.list_ports.comports():
        if p.vid == ARDUINO_VID:
            out.append(dict(device=p.device, vid=p.vid, pid=p.pid, serial_number=p.serial_number,
                            location=p.location, description=p.description))
    return out


def port_holders(device):
    """PIDs that have the device open (lsof), this process included."""
    r = subprocess.run(['lsof', '-t', device], capture_output=True, text=True)
    return [int(x) for x in r.stdout.split()]


class Line:
    """A serial connection to a board: lines in, a few fixed commands out."""

    def __init__(self, device, log=None):
        holders = port_holders(device)
        if holders:
            raise HwError(f'{device} is open in another process: {holders}')
        self.device = device
        self.ser = serial.Serial(device, 115200, timeout=0.02)
        self.buf = b''
        self.log = log if log is not None else []
        self.t0 = time.monotonic()

    def close(self):
        try:
            self.ser.close()
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()

    def _now(self):
        return time.monotonic()

    def pump(self):
        data = self.ser.read(max(self.ser.in_waiting, 1))
        if data:
            self.buf += data
            self.log.append((self._now(), 'rx', data))
        return data

    def drain(self, quiet=0.15):
        """Read and return everything that arrives until `quiet` seconds of silence."""
        got = b''
        last = self._now()
        while self._now() - last < quiet:
            d = self.pump()
            if d:
                last = self._now()
        got, self.buf = self.buf, b''
        return got

    def send(self, data):
        self.log.append((self._now(), 'tx', data))
        self.ser.write(data)
        self.ser.flush()

    def next_line(self, timeout, until=None):
        """Next complete line (bytes, no EOL) or None."""
        end = self._now() + timeout
        while True:
            i = self.buf.find(b'\n')
            if i >= 0:
                line, self.buf = self.buf[:i], self.buf[i + 1:]
                return line.rstrip(b'\r')
            if self._now() >= end:
                return None
            self.pump()

    def json_line(self, timeout, want=None):
        """Next line that parses as a JSON object (and satisfies `want`); other lines are
        returned in the second item."""
        end = self._now() + timeout
        others = []
        while True:
            line = self.next_line(max(0.0, end - self._now()))
            if line is None:
                return None, others
            if line.startswith(b'{'):
                try:
                    obj = json.loads(line)
                    if want is None or want(obj):
                        return obj, others
                except ValueError:
                    pass
            others.append(line)

    # ---- the commands. Only these bytes are ever sent to the board.
    def get_config(self, timeout=3):
        self.drain(0.05)
        self.send(b'G')
        obj, _ = self.json_line(timeout, want=lambda o: 'board' in o and 'information' in o)
        if obj is None:
            raise HwError('no answer to G')
        return obj

    def get_status(self, timeout=3):
        self.drain(0.05)
        self.send(b'T')
        obj, _ = self.json_line(timeout, want=lambda o: 'board' in o and 'motors' in o)
        if obj is None:
            raise HwError('no answer to T')
        return obj

    def send_filename(self, name, timeout=3, raw=None):
        self.drain(0.05)
        self.send(b'F' + (raw if raw is not None else name.encode()) + b'\n')
        obj, _ = self.json_line(timeout, want=lambda o: 'result' in o)
        return obj

    def send_config(self, cfg, timeout=5, raw=None):
        """`{` + the rest. `cfg` is a dict (compact JSON) or `raw` bytes starting with `{`."""
        self.drain(0.05)
        data = raw if raw is not None else json.dumps(cfg, separators=(',', ':')).encode()
        assert data.startswith(b'{')
        self.send(data)
        obj, _ = self.json_line(timeout, want=lambda o: 'result' in o)
        return obj

    def reboot(self, timeout=3):
        """R. Returns the time (s since sending) of the 'Rebooting...' reply or None."""
        self.drain(0.05)
        t = self._now()
        self.send(b'R')
        obj, _ = self.json_line(timeout, want=lambda o: 'result' in o)
        return (self._now() - t) if obj else None, obj


def identify(device):
    """Open a port, send G and T, and return what the board is."""
    with Line(device) as ln:
        time.sleep(0.2)
        g = ln.get_config()
        t = ln.get_status()
    return dict(device=device, product=g['board']['product'], G=g, T=t)


def find_boards(expect=('STEP400', 'STEP800')):
    """Return {product: Board}. Raises when there is not exactly one of each."""
    found = {}
    for p in usb_ports():
        info = identify(p['device'])
        b = Board(info['product'], p, info['G'], info['T'])
        if b.product in found:
            raise HwError(f'two boards of the same product: {b.product}')
        found[b.product] = b
    if sorted(found) != sorted(expect):
        raise HwError(f'expected {expect}, found {sorted(found)}')
    return found


# ---------------------------------------------------------------- the board
class Board:
    def __init__(self, product, port, G, T):
        self.product = product
        self.port = port
        self.serial_number = port['serial_number']
        self.device = port['device']
        self.G = G
        self.T = T
        self.osc_socks = {}

    @property
    def my_ip(self):
        return '.'.join(map(str, self.T['board']['myIp']))

    @property
    def my_id(self):
        return self.T['board']['myId']

    @property
    def out_port(self):
        n = self.G['network']
        return n['outPort'] + (self.my_id if n['isOutPortAddId'] else 0)

    @property
    def in_port(self):
        return self.G['network']['inPort']

    def line(self):
        return Line(self.device)

    def refresh(self, timeout=3):
        with self.line() as ln:
            self.G = ln.get_config()
            self.T = ln.get_status()
        return self

    def find_again(self, timeout=20):
        """After a reboot / unplug: find the same board again by serial number (never take the
        other board). Updates `device`."""
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            for p in usb_ports():
                if p['serial_number'] == self.serial_number:
                    self.device = p['device']
                    self.port = p
                    return p
            time.sleep(0.02)
        raise HwError(f'{self.product} did not come back within {timeout}s')

    # ---- OSC
    def osc(self):
        return OscPort.get(self.out_port)

    def osc_send(self, address, *args):
        OscPort.send_to(self.my_ip, self.in_port, address, *args)

    def osc_query(self, address, *args, timeout=1.0, setdest=True):
        """Send `address` and return the messages that came from this board within `timeout`."""
        sock = OscPort.get(self.out_port)
        sock.flush()
        self.osc_send(address, *args)
        return sock.collect(self.my_ip, timeout)

    def osc_set_dest(self, timeout=8.0):
        """Make the board send replies to this Mac and wait until it does (destIp is 10.0.0.10 in
        the config already). Just after a start the replies are held back while the board resolves
        the MAC address of destIp (src/arpResolve.h: up to 2 s, 1 s after the link came up), so
        ask until one comes. Returns the seconds it took."""
        t0 = time.monotonic()
        last = 0.0
        while time.monotonic() - t0 < timeout:
            if time.monotonic() - last > 0.6:      # one right after a start can be lost: ask again
                self.osc_send('/setDestIp')
                last = time.monotonic()
            if self.osc_query('/getVersion', timeout=0.2):
                return time.monotonic() - t0
        raise HwError(f'{self.product}: no OSC reply after /setDestIp')


class OscPort:
    """UDP socket bound to a board's outPort on this Mac."""
    _ports = {}
    _tx = None

    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('0.0.0.0', port))
        self.port = port

    @classmethod
    def get(cls, port):
        if port not in cls._ports:
            cls._ports[port] = cls(port)
        return cls._ports[port]

    @classmethod
    def send_to(cls, ip, port, address, *args):
        check_osc(address)
        b = osc_message_builder.OscMessageBuilder(address=address)
        for a in args:
            b.add_arg(a)
        if cls._tx is None:
            cls._tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cls._tx.sendto(b.build().dgram, (ip, port))

    def flush(self):
        while select.select([self.sock], [], [], 0)[0]:
            self.sock.recvfrom(4096)

    def recv(self, timeout):
        """(address, params, source ip, time) or None."""
        if not select.select([self.sock], [], [], timeout)[0]:
            return None
        data, src = self.sock.recvfrom(4096)
        t = time.monotonic()
        try:
            m = OscMessage(data)
            return m.address, list(m.params), src[0], t
        except Exception:
            return None

    def collect(self, ip, timeout):
        end = time.monotonic() + timeout
        out = []
        while True:
            left = end - time.monotonic()
            if left <= 0:
                break
            r = self.recv(left)
            if r and r[2] == ip:
                out.append(r)
        return out


# ---------------------------------------------------------------- reboot with timing
def reboot_and_wait(board, timeout=25):
    """R, then wait for the port to vanish and come back and for T to answer. Returns timings
    (seconds since R was sent) and the lines received after the port came back."""
    res = {}
    name_before = board.device
    ln = board.line()
    t0 = time.monotonic()
    dt, reply = ln.reboot()
    res['reply'] = dt
    res['reply_json'] = reply
    # keep the port open until it errors out, to see when it goes away
    gone = None
    try:
        while time.monotonic() - t0 < 10:
            ln.ser.read(max(ln.ser.in_waiting, 1))
            if not os.path.exists(name_before) or not any(
                    p['serial_number'] == board.serial_number for p in usb_ports()):
                gone = time.monotonic() - t0
                break
    except Exception:
        gone = time.monotonic() - t0
    ln.close()
    res['gone'] = gone
    deadline = t0 + timeout
    back = None
    while time.monotonic() < deadline:
        for p in usb_ports():
            if p['serial_number'] == board.serial_number:
                back = time.monotonic() - t0
                board.device, board.port = p['device'], p
                break
        if back is not None:
            break
        time.sleep(0.005)
    res['back'] = back
    res['name_before'] = name_before
    res['name_after'] = board.device
    if back is None:
        raise HwError(f'{board.product} did not come back after R')
    # open as soon as possible and collect the start-up lines
    lines = []
    ln = None
    for _ in range(400):
        try:
            ln = Line(board.device)
            break
        except Exception:
            time.sleep(0.01)
    if ln is None:
        raise HwError('could not open the port after R')
    res['opened'] = time.monotonic() - t0
    # T answers only when the main loop runs
    ok = None
    while time.monotonic() - t0 < timeout:
        ln.pump()
        ln.send(b'T')
        obj, others = ln.json_line(0.5, want=lambda o: 'motors' in o)
        lines += others
        if obj:
            ok = time.monotonic() - t0
            res['T'] = obj
            break
    res['t_answers'] = ok
    res['startup_lines'] = [l.decode('utf-8', 'replace') for l in lines]
    res['pre'] = ln.buf.decode('utf-8', 'replace')
    ln.close()
    if ok is None:
        raise HwError('T did not answer after R')
    board.refresh()
    return res


# ---------------------------------------------------------------- backup / restore
def stamp():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


def backup(board, directory=OUT):
    os.makedirs(directory, exist_ok=True)
    b = board.refresh()
    path = os.path.join(directory, f'backup_{b.product}_{stamp()}.json')
    data = dict(product=b.product, serial_number=b.serial_number, device=b.device,
                time=datetime.datetime.now().isoformat(), G=b.G, T=b.T,
                configFilename=b.G['board']['configFilename'],
                myIp=b.my_ip, myId=b.my_id, outPort=b.out_port)
    with open(path, 'w') as f:
        json.dump(data, f, indent=1)
    return path


def _strip_volatile(G):
    """What is compared after a restore. `board` has the file name (compared separately) and
    `information.configVersion` / `targetProduct` change with the file the board loaded at
    start-up ([-1,0] / "---" when no file was loaded, the version of the file otherwise) and a
    `{` never sets them, so they are left out. Everything else is compared as is."""
    g = json.loads(json.dumps(G))
    g['information'].pop('configVersion', None)
    g['information'].pop('targetProduct', None)
    g['board'].pop('configFilename', None)
    return g


def diff(a, b, path=''):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(f'{path}/{k}: only in {"b" if k not in a else "a"}')
            else:
                out += diff(a[k], b[k], f'{path}/{k}')
    elif a != b:
        out.append(f'{path}: {a!r} != {b!r}')
    return out


def restore(backup_path, reboot=True):
    """Put the board of the backup back as it was: file name (F), configuration ({), reboot (R),
    then G must be the same (see _strip_volatile). Returns the list of differences (empty = ok)."""
    with open(backup_path) as f:
        data = json.load(f)
    boards = find_boards()
    board = boards[data['product']]
    if board.serial_number != data['serial_number']:
        raise HwError('the serial number of the board is not the one of the backup')
    want = data['G']
    with board.line() as ln:
        r = ln.send_filename(data['configFilename'])
        if not r or r.get('result') != 'ok':
            raise HwError(f'F failed: {r}')
        r = ln.send_config(want)
        if not r or r.get('result') != 'ok':
            raise HwError(f'{{ failed: {r}')
    if reboot:
        reboot_and_wait(board)
    board.refresh()
    d = diff(_strip_volatile(want), _strip_volatile(board.G))
    if board.G['board'].get('configFilename') != data['configFilename']:
        d.append(f"configFilename: {data['configFilename']!r} != {board.G['board'].get('configFilename')!r}")
    if board.my_ip != data['myIp']:
        d.append(f"myIp: {data['myIp']} != {board.my_ip}")
    return d


# ---------------------------------------------------------------- command line
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cmd', nargs='?', choices=['ports', 'backup', 'fixtures'])
    ap.add_argument('--restore', metavar='BACKUP', action='append')
    a = ap.parse_args(argv)
    if a.restore:
        rc = 0
        for p in a.restore:
            d = restore(p)
            print(p, 'restored, G equal' if not d else 'DIFFERENT:\n  ' + '\n  '.join(d))
            rc |= bool(d)
        return rc
    if a.cmd == 'ports':
        for p in usb_ports():
            print(p)
        for prod, b in sorted(find_boards().items()):
            print(prod, b.device, b.serial_number, 'myId', b.my_id, 'myIp', b.my_ip,
                  'outPort', b.out_port, 'sd', b.T['board']['sdInitialized'])
    elif a.cmd == 'backup':
        for prod, b in sorted(find_boards().items()):
            print(backup(b))
    elif a.cmd == 'fixtures':
        from capture_fixtures import capture
        capture()
    return 0


if __name__ == '__main__':
    sys.exit(main())
