#!/usr/bin/env python3
"""Guided checks for the hand-made parts of CHECKLIST_config_tool_v220.md (stage 3).

Run it in a terminal by a person:

    ~/.venvs/step-config-test/bin/python step-config/tests/guided.py            # from the start
    ~/.venvs/step-config-test/bin/python step-config/tests/guided.py --resume step-config/tests/out/guided_<time>.json
    ~/.venvs/step-config-test/bin/python step-config/tests/guided.py --list      # the steps
    ~/.venvs/step-config-test/bin/python step-config/tests/guided.py --only card # one step (or several, comma separated)
    ~/.venvs/step-config-test/bin/python step-config/tests/guided.py --check     # only find the boards and back them up

One step at a time: it says what to do, you press Enter, it checks what it can by itself (serial,
OSC, ping, which program has a port open) and asks y / n only for what has to be seen with the eyes.
The result of every step is written to out/guided_<time>.json as soon as it is known, so after an
interruption (Ctrl-C, closing the window) `--resume` starts again at the first step without a result.

Before the first step it finds the two boards (by `G`, not by the name of the port), saves their
settings (out/backup_*.json) and checks that they are as in the golden backup (out/golden_*.json);
at the end of every step that changes a setting it puts the settings back.

The motors stay still, except in step `brake` (10.3) and only after you confirm that a motor is connected
and its power is on: the one OSC command that makes it turn is allowed for that step only.

Real Chrome (or Safari) may hold a serial port: this program cannot open that port then. Where it needs
the port it asks you to press Disconnect in the tool first; otherwise it uses OSC only.
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import time

import hw_protocol as hp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
TOOL = os.path.normpath(os.path.join(HERE, '..', 'index.html'))
TEMPLATES = os.path.normpath(os.path.join(HERE, '..', '..', 'configGenerator'))

# files the automatic tests left on the card (stage 2); this program deletes only these names
LEFTOVERS = ['/config.txt', '/zzz.json', '/ABC.JSON', '/My Config.json',
             '/STEP400_test_with_a_long_file_name_0123456789.json',
             '/' + 'a' * 57 + '.json', '/test_offline.json']

STEPS = []        # (id, title, function), in order


def step(sid, title):
    def deco(fn):
        STEPS.append((sid, title, fn))
        return fn
    return deco


class Stop(Exception):
    pass


class Guide:
    def __init__(self, path, results):
        self.path = path
        self.results = results
        self.boards = None
        self.golden = {}

    # ---- talking
    def say(self, *a):
        print(*a, flush=True)

    def head(self, sid, title):
        self.say('\n' + '=' * 72 + f'\n[{sid}] {title}\n' + '=' * 72)

    def enter(self, msg):
        self.say('\n' + msg)
        try:
            a = input('   -> press Enter when done (q + Enter: stop here) ')
        except EOFError:
            raise Stop()
        if a.strip().lower() == 'q':
            raise Stop('stopped by the person')

    def yn(self, msg):
        while True:
            try:
                a = input(f'\n{msg} [y/n/s=skip] ').strip().lower()
            except EOFError:
                raise Stop()
            if a in ('y', 'n', 's'):
                return {'y': True, 'n': False, 's': None}[a]

    def choose(self, msg, options):
        for i, o in enumerate(options, 1):
            self.say(f'  {i}. {o}')
        while True:
            a = input(f'{msg} (number) ').strip()
            if a.isdigit() and 1 <= int(a) <= len(options):
                return options[int(a) - 1]

    # ---- results
    def record(self, rid, ok, detail='', rows=()):
        """ok: True / False / None (skipped). Written at once."""
        self.results['results'][rid] = dict(ok=ok, detail=detail, rows=list(rows),
                                            time=datetime.datetime.now().isoformat(timespec='seconds'))
        self.save()
        mark = {True: 'PASS', False: 'FAIL', None: 'SKIP'}[ok]
        self.say(f'   [{mark}] {rid}  {detail}')

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.results, f, indent=1, default=str)

    # ---- boards
    def find(self):
        self.boards = hp.find_boards()
        return self.boards

    def show_ports(self):
        self.say('\nWhich port is which board (found by sending G, not by the port name):')
        for prod, b in sorted(self.boards.items()):
            self.say(f'  {b.device:28s} {prod}  USB serial {b.serial_number}  location {b.port["location"]}'
                     f'  IP {b.my_ip}  ID {b.my_id}')
        names = {b.port['description'] for b in self.boards.values()}
        if len(names) == 1:
            self.say('  The two boards have the same name in a port list (e.g. "Arduino Zero"). In the port\n'
                     '  list of Chrome the order is not reliable: after you choose one, this program checks\n'
                     '  which board it is. If you are not sure, unplug the USB of the other board.')

    def holders(self, b):
        return hp.port_holders(b.device)

    def wait_port(self, b, present, timeout=60):
        t0 = time.time()
        while time.time() - t0 < timeout:
            here = any(p['serial_number'] == b.serial_number for p in hp.usb_ports())
            if here == present:
                if present:
                    b.find_again(5)
                return True
            time.sleep(0.2)
        return False

    def wait_held(self, b, held, timeout=60):
        t0 = time.time()
        while time.time() - t0 < timeout:
            if bool(self.holders(b)) == held:
                return True
            time.sleep(0.2)
        return False

    def wait_booted(self, b, timeout=40):
        """The board (same USB serial number) is back and its main loop answers T."""
        if not self.wait_port(b, True, timeout):
            return False
        for _ in range(int(timeout * 2)):
            try:
                with b.line() as ln:
                    b.T = ln.get_status(timeout=1)
                    b.G = ln.get_config(timeout=2)
                return True
            except Exception:
                time.sleep(0.5)
        return False

    def need_free(self, b):
        """Make sure no other program has the serial port; ask for Disconnect in the browser."""
        while self.holders(b):
            self.enter(f'The serial port of {b.product} is open in another program (the browser?). '
                       'Press Disconnect in the tool.')

    def restore(self, prod):
        self.need_free(self.boards[prod])
        d = hp.restore(self.golden[prod])
        b = self.boards[prod] = hp.find_boards()[prod]
        b.osc_set_dest()
        return d

    def restore_all(self):
        out = {}
        for prod in self.boards:
            try:
                out[prod] = self.restore(prod)
            except Exception as e:      # noqa: BLE001
                out[prod] = [f'restore failed: {e!r}']
        return out


# ====================================================================== steps
@step('chrome', 'Real Chrome: open the tool, Connect (port choice), Disconnect, Connect x3, dark and light')
def s_chrome(g):
    b4 = g.boards['STEP400']
    g.show_ports()
    g.enter('Open the tool in Chrome: a window opens now. (Quit the Arduino serial monitor, if any.)')
    subprocess.run(['open', '-a', 'Google Chrome', TOOL])
    g.enter('In Chrome press Connect and choose the port of the STEP400 (see the list above).')
    held = [p for p, b in g.boards.items() if g.holders(b)]
    ok = held == ['STEP400']
    g.record('1.1 chrome port choice', ok, f'Chrome holds: {held}')
    if held == ['STEP800']:
        g.say('   You chose the STEP800. Press Disconnect and choose the other one (STEP400) for the next steps.')
        g.wait_held(g.boards['STEP800'], False)
        g.enter('Connect again, STEP400 this time.')
    r = g.yn('Does the tool say "Config loaded from board" and show Product STEP400, Firmware Version 2.2.0, Axes 4 (from board)?')
    g.record('1.1/1.2 chrome shows the board', r)
    # Disconnect -> Connect three times: the program sees the port being opened and closed
    cycles = 0
    g.say('\nNow press Disconnect, then Connect, three times (Disconnect, Connect, Disconnect, Connect, ...).')
    g.say('This program counts how often the port is opened (up to 3 Connects, 90 s).')
    prev = bool(g.holders(b4))
    t0 = time.time()
    opens = 0
    while time.time() - t0 < 90 and opens < 3:
        now = bool(g.holders(b4))
        if now and not prev:
            opens += 1
            g.say(f'   port opened (Connect #{opens})')
        prev = now
        time.sleep(0.15)
    r = g.yn('No "Serial connection lost" banner after any Disconnect, and every Connect read the config?')
    g.record('1.6 disconnect/connect x3 in Chrome', bool(opens >= 3 and r), f'ports opened after the start: {opens}; answer {r}')
    for scheme in ('dark', 'light'):
        g.enter(f'Switch macOS to {scheme.upper()} appearance (System Settings > Appearance); reload the tool, Connect if needed.')
        r = g.yn(f'{scheme}: are the labels of Connect / Disconnect / Reboot readable, also while the mouse is over them (hover)?')
        g.record(f'11.2 {scheme} mode buttons and hover', r)
    g.say('\nIn Chrome, press Disconnect now (the port must be free for the next steps).')
    g.wait_held(b4, False)


@step('unplug', 'USB unplug: banner, Reconnect, unplug during a save, Reboot -> Connect')
def s_unplug(g):
    b = g.boards['STEP400']
    g.need_free(b)
    g.enter('In Chrome press Connect (STEP400), wait for "Config loaded".')
    g.wait_held(b, True)
    g.enter('Now UNPLUG the USB cable of the STEP400 (Ethernet stays).')
    gone = g.wait_port(b, False, 30)
    g.record('1.7 unplug seen', gone, 'port vanished' if gone else 'port still there')
    r = g.yn('Chrome tool shows the banner "Serial connection lost" and Connect is back to "Connect"? (no red error in the console)')
    g.record('1.7 banner after unplug', r)
    g.enter('Plug the USB cable in again, wait 3 s, then press Reconnect in the banner.')
    back = g.wait_port(b, True, 30)
    g.wait_held(b, True, 30)
    r = g.yn('The tool reads the config again ("Config loaded from board")?')
    g.record('1.7 reconnect', bool(back and r))
    # unplug during a save
    g.enter('Change Config Name to "unplugtest" in the tool. Be ready to press "Save to SD" and unplug the USB\n'
            '   cable THE MOMENT you click it (the save takes about 0.3 s). Then press Enter here after you did it.')
    g.wait_port(b, True, 30)
    r = g.yn('The tool showed a message about the lost connection during the save (it may or may not have saved)?')
    g.record('3.x unplug during save: message', r)
    g.enter('Plug the USB in again, press Reconnect, then press Disconnect in the tool (so this program can read the board).')
    g.wait_held(b, False, 120)
    g.wait_booted(b)
    name = b.G['information']['configName']
    g.record('3.x unplug during save: result on the board', None,
             f'G configName after the unplug = {name!r} (the save {"was" if name == "unplugtest" else "was NOT"} applied); '
             f'resetCause {b.T["board"]["resetCause"]}')
    d = g.restore('STEP400')
    g.record('unplug: settings back', not d, '; '.join(d))
    # Reboot -> Connect
    g.enter('Press Connect in the tool again. Then press Reboot and OK. Wait for "Board rebooted — click Connect to reconnect." and press Connect.')
    g.wait_held(b, True, 120)
    r = g.yn('After Reboot the tool disconnected by itself without a "lost" banner or a timeout error, and Connect read the config?')
    g.record('10.1/10.2 reboot -> connect in Chrome', r)
    g.say('Press Disconnect in the tool.')
    g.wait_held(b, False)


@step('ethernet', 'Ethernet cable: Status Link OFF / ON')
def s_ethernet(g):
    b = g.boards['STEP400']
    g.need_free(b)
    g.enter('In Chrome: Connect, press Start Status. Link should be ON.')
    r = g.yn('Link shows ON (green)?')
    g.enter('UNPLUG the Ethernet cable of the STEP400.')
    time.sleep(2)
    ping = subprocess.run(['ping', '-c', '1', '-t', '2', b.my_ip], capture_output=True).returncode
    r2 = g.yn('Link shows OFF (red) within 1-2 s?')
    g.enter('Plug the Ethernet cable in again.')
    time.sleep(3)
    ping2 = subprocess.run(['ping', '-c', '1', '-t', '2', b.my_ip], capture_output=True).returncode
    r3 = g.yn('Link shows ON again?')
    g.record('2.2 link off/on', bool(r and r2 and r3 and ping != 0 and ping2 == 0),
             f'ping with cable out rc={ping} (want not 0), back rc={ping2}')
    g.say('Press Stop Status and Disconnect.')
    g.wait_held(b, False)


@step('safari', 'Safari: banner, Connect disabled, Load / Download')
def s_safari(g):
    g.enter('Open the tool in Safari (a window opens now).')
    subprocess.run(['open', '-a', 'Safari', TOOL])
    r1 = g.yn('The banner says Web Serial is not available, names Chrome or Edge and says Firefox 151 or later should work (not tested)?')
    r2 = g.yn('The Connect button cannot be pressed (greyed)?')
    g.say(f'   Use Load JSON with {TEMPLATES}/configTemplate_step400.json')
    r3 = g.yn('The 4-column tables are filled, and Download JSON saves a file?')
    g.record('11.1 safari', bool(r1 and r2 and r3), f'banner={r1} connect-disabled={r2} load/download={r3}')


# ---------------------------------------------------------------- card steps
def volumes():
    return sorted(os.listdir('/Volumes'))


def first_json(card):
    """loadConfig.cpp findFirstValidJson(): the alphabetically first *.json of the root (strcasecmp),
    names starting with '.' skipped; if it is not valid there is no next try. Returns the name or None."""
    names = [n for n in os.listdir(card) if not n.startswith('.') and n.lower().endswith('.json')
             and os.path.isfile(os.path.join(card, n))]
    names.sort(key=str.lower)
    if not names:
        return None
    try:
        d = json.load(open(os.path.join(card, names[0])))
        return '/' + names[0] if d['information']['configVersion'] is not None else None
    except Exception:
        return None


def expected_boot_file(card):
    cfg = os.path.join(card, 'config.txt')
    if os.path.exists(cfg):
        try:
            json.load(open(cfg))
            return '/config.txt'
        except Exception:
            pass
    return first_json(card)


def pick_card(g, why):
    before = set(volumes())
    g.enter(f'{why}\n   Take the microSD card out of the STEP400 (power the board off first), put it in the Mac.')
    time.sleep(3)
    new = sorted(set(volumes()) - before)
    opts = new + [v for v in volumes() if v not in new]
    g.say('Volumes now: ' + ', '.join(volumes()))
    vol = g.choose('Which one is the card from the STEP400?', opts)
    path = os.path.join('/Volumes', vol)
    info = subprocess.run(['diskutil', 'info', path], capture_output=True, text=True).stdout
    fs = next((l.split(':', 1)[1].strip() for l in info.splitlines() if 'File System Personality' in l), '?')
    g.say(f'   {path}: {fs}')
    if 'FAT' not in fs.upper():
        raise Stop(f'{path} is {fs}, not FAT: stopping so nothing is written to it')
    ok = g.yn(f'Write to {path} (only the files named in LEFTOVERS and the scene files)?')
    if not ok:
        raise Stop('card not confirmed')
    return path


def eject(g, path):
    subprocess.run(['sync'])
    subprocess.run(['diskutil', 'eject', path], capture_output=True)
    g.say('   ejected: take the card out and put it into the STEP400.')


def board_booted_with_card(g, b):
    g.enter('Put the card in the STEP400 and power the board on (USB + Ethernet).')
    ok = g.wait_booted(b, 60)
    if ok:
        b.osc_set_dest()
    return ok


def scene(g, card, name, setup, expect_name, why):
    """Prepare the card (setup(card)), put it in the board, boot, ask /getConfigName by OSC."""
    b = g.boards['STEP400']
    setup(card)
    exp_file = expected_boot_file(card)
    eject(g, card)
    if not board_booted_with_card(g, b):
        g.record(name, False, 'the board did not come back')
        return False
    r = b.osc_query('/getConfigName', timeout=1.5)
    got = r[0][1] if r else None
    ok = bool(got) and got[4] == exp_file and got[0] == expect_name and tuple(got[1:4]) == (1, 1, 1)
    g.record(name, ok, f'{why}: /configName = {got}; expected file {exp_file}, name {expect_name!r}')
    return ok


def write_cfg(card, fname, cfg_name, g):
    base = json.loads(json.dumps(g.golden_G['STEP400']))
    base.pop('board')
    base['information'] = dict(configName=cfg_name, configVersion=[1, 2], targetProduct='STEP400')
    with open(os.path.join(card, fname.lstrip('/')), 'w') as f:
        f.write(json.dumps(base, separators=(',', ':')) + '\n')


@step('card', 'Card in the Mac (STEP400): what the tests left, start-up order scenes (3.7, 4.8, 9.5, 9.6, 4.9)')
def s_card(g):
    b = g.boards['STEP400']
    g.need_free(b)
    card = pick_card(g, 'Card step: this program saves the whole card first, then changes it, and puts everything back at the end.')
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    bk = os.path.join(OUT, f'card_backup_{stamp}')
    shutil.copytree(card, bk, ignore=shutil.ignore_patterns('.Spotlight*', '.fseventsd', '.Trashes'))
    g.results['card_backup'] = bk
    g.results['card_volume'] = card
    g.save()
    g.say(f'   whole card saved in {bk}')
    files = sorted(n for n in os.listdir(card) if not n.startswith('.'))
    g.say('   on the card: ' + ', '.join(files))
    # 3.7: the files the automatic tests wrote are one-line JSON
    bad = []
    for n in files:
        if n.lower().endswith(('.json', '.txt')):
            raw = open(os.path.join(card, n), 'rb').read()
            try:
                d = json.loads(raw)
                if raw.count(b'\n') != 1 or not raw.endswith(b'}\n'):
                    bad.append(f'{n}: {raw.count(10)} newlines')
                if 'information' not in d:
                    bad.append(f'{n}: no information')
            except Exception as e:      # noqa: BLE001
                bad.append(f'{n}: not JSON ({e})')
    tmp = [n for n in os.listdir(card) if n.startswith('.') and n.endswith('.tmp')]
    g.record('3.7 files on the card are one-line JSON', not bad and not tmp, '; '.join(bad + [f'left over: {tmp}'] if tmp else bad))
    cfgtxt = os.path.join(card, 'config.txt')
    if os.path.exists(cfgtxt):
        d = json.load(open(cfgtxt))
        g.record('3.7 config.txt information.configName', d['information']['configName'] == b.G['information']['configName'],
                 f'{d["information"]["configName"]!r}')
    # long name file left by 4.1 is there, and config.txt was not changed by it
    g.record('4.1 long-name file exists', os.path.exists(os.path.join(card, LEFTOVERS[4].lstrip('/'))))
    # scenes (the card stays mounted between scenes; for each one it goes into the board and back)
    held = os.path.join(bk, '_held')
    os.makedirs(held, exist_ok=True)

    def only(*keep):
        def f(card):
            for n in os.listdir(card):
                if n.startswith('.'):
                    continue
                p = os.path.join(card, n)
                if os.path.isfile(p) and n not in keep and ('/' + n) in LEFTOVERS:
                    shutil.move(p, os.path.join(held, n))
        return f

    # (a) 4.8 second half: no config.txt, several .json -> the alphabetically first valid one
    def a(card):
        only('ABC.JSON', 'My Config.json', 'zzz.json', LEFTOVERS[5].lstrip('/'), LEFTOVERS[4].lstrip('/'))(card)
    ok = scene(g, card, '4.8 no config.txt, several .json -> first in alphabetical order', a, 'Default',
               'config.txt removed')
    card = pick_card(g, 'Take the card out of the STEP400 again.')
    # (b) 9.5: only /test_offline.json (made like a downloaded file)
    def bscene(card):
        only()(card)
        write_cfg(card, '/test_offline.json', 'offline-b', g)
    ok = scene(g, card, '9.5 downloaded file as /test_offline.json (config.txt moved away)', bscene, 'offline-b',
               'only test_offline.json')
    card = pick_card(g, 'Take the card out of the STEP400 again.')
    # (c) 9.6: the downloaded file as config.txt
    def cscene(card):
        only()(card)
        write_cfg(card, '/config.txt', 'offline-c', g)
    scene(g, card, '9.6 downloaded file as config.txt', cscene, 'offline-c', 'config.txt')
    card = pick_card(g, 'Take the card out of the STEP400 again.')
    # (d) 4.9 start-up: only "My Config.json"
    def dscene(card):
        only()(card)
        write_cfg(card, '/My Config.json', 'spaced-boot', g)
    scene(g, card, '4.9 only "My Config.json" is read at start-up', dscene, 'spaced-boot', 'spaced name')
    # check the board with the tool's Read through OSC only (the port is free): nothing else to do
    g.say('\nScenes done. The card is in the board with the last scene; step `card-restore` puts the card back.')


@step('card-errors', 'Card errors: no card at start, card removed after start, put back, reboot (2.3, 5, 13.7-13.9)')
def s_card_errors(g):
    b = g.boards['STEP400']
    g.need_free(b)
    cfg = json.loads(json.dumps(b.G))
    # no card at boot
    g.enter('Power the STEP400 off, TAKE THE CARD OUT (leave it out), power on (USB + Ethernet).')
    g.wait_booted(b, 60)
    sd = b.T['board']['sdInitialized']
    with b.line() as ln:
        r = ln.send_config(cfg)
    g.record('5.1 no card at start: board side', sd is False and r == {'result': 'error', 'message': 'No SD card'},
             f'sdInitialized={sd}, save answer {r}')
    g.enter('In Chrome: Connect, Start Status, press Save to SD. Then Disconnect.')
    r1 = g.yn('Read worked; Status shows SD ERR (red) and Config "Not loaded"?')
    r2 = g.yn('Save showed "Save failed: No SD card — Is a card inserted, and formatted as FAT16 or FAT32 (exFAT cannot be used)?..." and the tool still works (Read)?')
    g.record('5.1/2.3/13.7 tool, no card', bool(r1 and r2))
    # exFAT (optional)
    if g.yn('Do you have an exFAT card to try? (s/n = skip)'):
        g.enter('Power off, insert the exFAT card, power on.')
        g.wait_booted(b, 60)
        with b.line() as ln:
            r = ln.send_config(cfg)
        g.record('5.2 exFAT: board side', b.T['board']['sdInitialized'] is False and r.get('message') == 'No SD card', f'{r}')
        r1 = g.yn('In Chrome: Save to SD shows "No SD card" with the exFAT hint, Status SD ERR?')
        g.record('5.2/13.9 tool, exFAT', r1)
    else:
        g.record('5.2/13.9 exFAT', None, 'no exFAT card')
    # removed after start
    g.enter('Power off, put the normal FAT32 card in, power on. Wait 5 s. Then TAKE THE CARD OUT while the board runs.')
    g.wait_booted(b, 60)
    before = b.T['board']['resetCauseRaw'], b.T['board']['sdInitialized']
    with b.line() as ln:
        r = ln.send_config(cfg)
        t = ln.get_status()
    g.record('5.3 card removed after start: board side', before[1] and r == {'result': 'error', 'message': 'SD open failed'}
             and t['board']['resetCause'] == b.T['board']['resetCause'], f'save answer {r}; the board did not restart')
    r1 = g.yn('In Chrome: Connect, Save to SD shows "Save failed: SD open failed — The card was removed after start-up, the card is full..."; Read still works?')
    g.record('5.3/13.8 tool, card removed', r1)
    # put back, still fails
    g.enter('Put the card back in the running board. Wait 3 s.')
    with b.line() as ln:
        r = ln.send_config(cfg)
    g.record('5.4 card put back: save still fails until a restart', r.get('message') == 'SD open failed', f'{r}')
    g.enter('In Chrome press Reboot (OK) and then Connect; press Save to SD again.')
    ok = g.yn('The save now works ("Saved to SD")?')
    g.record('5.4 after the restart the save works', ok)
    g.say('Press Disconnect in the tool.')
    g.wait_held(b, False)
    d = g.restore('STEP400')
    g.record('card-errors: settings back', not d, '; '.join(d))


@step('brake', '10.3 Reboot while a motor turns slowly (motor connected and powered)')
def s_brake(g):
    b = g.boards['STEP400']
    g.need_free(b)
    g.say('\nThis is the only step where a motor turns. Slowly (400 microsteps/s = about 3 full steps/s).')
    ok = g.yn('A motor is connected to the STEP400, its power is ON, it can turn freely and nothing is in its way? (n = skip)')
    if not ok:
        g.record('10.3 reboot while turning', None, 'skipped: no motor')
        return
    m = int(g.choose('Which output is the motor on?', ['1', '2', '3', '4']))
    brake = g.yn('Does that motor have an electromagnetic brake (EMB-STEP400, 24 V on)?')
    if brake:
        cfg = json.loads(json.dumps(b.G))
        cfg['driverSettings']['electromagnetBrakeEnable'][m - 1] = True
        with b.line() as ln:
            ln.send_config(cfg)
            ln.send(b'R')
        g.wait_booted(b, 40)
        b.osc_set_dest()
        g.say('   brake enable is on for this motor (it is put back at the end).')
    with hp.allowed('/run', '/softStop'):
        g.enter('In Chrome: Connect. Then press Enter: the motor will start to turn slowly.')
        b.osc_set_dest()
        b.osc_send('/run', m, 400)
        time.sleep(1.0)
        r = g.yn('The motor is turning slowly?')
        if not r:
            b.osc_send('/softStop', m)
            g.record('10.3 reboot while turning', None, 'motor did not turn; stopped')
            return
        g.say('   Now press Reboot in the tool and OK. WATCH the motor / brake.')
        g.enter('Press Enter after the tool says "Board rebooted…".')
        b.osc_send('/softStop', m)        # harmless if the board is already restarting
    r1 = g.yn('The motor stopped and (with a brake) the brake held it before the board restarted?')
    r2 = g.yn('The tool showed no "Serial response timeout"?')
    g.record('10.3 reboot while turning', bool(r1 and r2), f'brake={brake} motor={m}')
    g.say('Press Disconnect in the tool.')
    g.wait_held(b, False)
    d = g.restore('STEP400')
    g.record('brake: settings back', not d, '; '.join(d))


@step('card-restore', 'Put the card back as it was; delete the files made for these checks')
def s_card_restore(g):
    b = g.boards['STEP400']
    g.need_free(b)
    card = pick_card(g, 'Card restore: take the card out of the STEP400 and put it in the Mac.')
    bk = g.results.get('card_backup')
    present = [n for n in LEFTOVERS if os.path.exists(os.path.join(card, n.lstrip('/')))]
    g.say('Files that will be deleted from the card (only these names): ' + (', '.join(present) or '(none)'))
    others = sorted(n for n in os.listdir(card) if not n.startswith('.') and ('/' + n) not in LEFTOVERS)
    if others:
        g.say('   Other files on the card (left alone): ' + ', '.join(others))
    if g.yn('Delete the files listed above?'):
        for n in present:
            os.remove(os.path.join(card, n.lstrip('/')))
        left = [n for n in os.listdir(card) if n.endswith('.tmp')]
        for n in left:
            os.remove(os.path.join(card, n))
        g.record('card restored (test files deleted)', True, f'deleted {present} {left}; whole-card backup in {bk}')
    eject(g, card)
    g.enter('Put the card into the STEP400, power on (USB + Ethernet).')
    g.wait_booted(b, 60)
    d = g.restore('STEP400')
    g.record('card-restore: settings back', not d, '; '.join(d))


@step('final', 'Put both boards back and compare')
def s_final(g):
    out = g.restore_all()
    ok = all(not v for v in out.values())
    g.record('settings of both boards are as before', ok, json.dumps(out))
    for p, b in g.boards.items():
        g.record(f'OSC answers at the original IP {p}', bool(b.osc_query('/getVersion', timeout=1.5)), b.my_ip)


# ====================================================================== main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--resume', metavar='FILE')
    ap.add_argument('--only', help='comma separated step ids')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--check', action='store_true', help='find the boards and back them up, then stop')
    a = ap.parse_args()
    if a.list:
        for sid, title, _ in STEPS:
            print(f'{sid:12s} {title}')
        return 0
    os.makedirs(OUT, exist_ok=True)
    if a.resume:
        path = a.resume
        results = json.load(open(path))
    else:
        path = os.path.join(OUT, f'guided_{hp.stamp()}.json')
        results = dict(started=datetime.datetime.now().isoformat(timespec='seconds'), results={}, steps_done=[])
    g = Guide(path, results)
    g.say('Finding the boards (sending G to every USB serial port) ...')
    holders = {p['device']: hp.port_holders(p['device']) for p in hp.usb_ports()}
    if any(holders.values()):
        g.say(f'A serial port is open in another program: {holders}. Close it (Disconnect in the tool) and run again.')
        return 2
    g.find()
    g.show_ports()
    for p, b in g.boards.items():
        golden = os.path.join(OUT, f'golden_{p}.json')
        if not os.path.exists(golden):
            shutil.copy(hp.backup(b), golden)
        else:
            hp.backup(b)
        g.golden[p] = golden
        g.say(f'   backup of {p} saved; reference: {golden}')
    g.golden_G = {p: json.load(open(path_))['G'] for p, path_ in g.golden.items()}
    results['ports'] = {p: dict(device=b.device, serial=b.serial_number, ip=b.my_ip, id=b.my_id) for p, b in g.boards.items()}
    for p, b in g.boards.items():
        want = g.golden_G[p]
        dd = hp.diff(hp._strip_volatile(want), hp._strip_volatile(b.G))
        dd = [x for x in dd if 'canSendMsgBeforeDestIp' not in x]
        if dd:
            g.say(f'   {p} differs from the reference: {dd[:3]} ... putting it back first')
            g.restore(p)
        b.osc_set_dest()
    g.save()
    if a.check:
        g.say('Boards found, backed up and reachable by OSC. Nothing else done.')
        return 0
    only = set(a.only.split(',')) if a.only else None
    try:
        for sid, title, fn in STEPS:
            if only and sid not in only:
                continue
            if sid in results['steps_done'] and not only:
                continue
            g.head(sid, title)
            if input('   Enter = start this step, s = skip it, q = stop here: ').strip().lower() == 's':
                g.record(f'step {sid}', None, 'skipped by the person')
            else:
                try:
                    fn(g)
                except Stop as e:
                    g.say(f'\nStopped: {e}')
                    raise
            results['steps_done'].append(sid)
            g.save()
    except (KeyboardInterrupt, Stop):
        g.save()
        g.say(f'\nInterrupted. Resume with:\n  {sys.executable} {os.path.abspath(__file__)} --resume {path}')
        g.say('(If a step had changed a board setting, the `final` step puts everything back.)')
        return 1
    n = results['results']
    g.say(f'\nDone: {sum(1 for v in n.values() if v["ok"] is True)} passed, {sum(1 for v in n.values() if v["ok"] is False)} failed, '
          f'{sum(1 for v in n.values() if v["ok"] is None)} skipped. Result file: {path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
