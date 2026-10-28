"""A fake STEP400 / STEP800 board for the USB serial commands of firmware v2.2.0.

It imitates the behaviour of `G`, `T`, `{`, `F` and `R` (and the start-up configuration
loading) from the firmware source at tag v2.2.0 (step-series-unified-firmware):

    src/diagnosis.cpp   diagnosisCommand(), printConfigAsJson(), serializeConfigSectionsTo(),
                        printStatusAsJson(), receiveConfigJson(), receiveFilename(),
                        sdSaveConfig(), saveCurrentConfigAsJson(), rebootBoard()
    src/loadConfig.cpp  loadConfig(), findFirstValidJson()
    src/boardsDef.h     PRODUCT_NAME, NUM_OF_MOTOR, HAVE_BRAKE / HAVE_LIMIT_ADC / DRIVER_*
    src/globals.cpp     default values, loadedConfigVersion = {-1, 0}
    src/globals.h       MAX_CONFIG_FILENAME = 64
    src/idOffset.cpp    addIdToIpLastByte(), addIdToPort()
    src/main.cpp        setup(): the "myId:" and "eth ok" lines

It is a stand-in for tests of the browser tool. A pass against it says nothing about the
firmware: the places where it guesses are listed in `GUESSES` at the end of this file.

The board runs as a coroutine on the backend's event loop. Like the firmware main loop it reads
the commands from a byte buffer, one at a time; while it sleeps (a save, a reboot) the bytes
the host sends pile up in the buffer.
"""
import asyncio
import copy
import json
import os
import random

FIRMWARE_DEFAULT = (2, 2, 0)
MAX_CONFIG_FILENAME = 64          # globals.h
BUF_SIZE = 4096                   # receiveConfigJson()
HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.normpath(os.path.join(HERE, '..', '..', 'configGenerator'))

# Section / key order of serializeConfigSectionsTo().
NETWORK_KEYS = ['myIp', 'destIp', 'dns', 'gateway', 'subnet', 'isMyIpAddId', 'inPort', 'outPort',
                'isOutPortAddId', 'mac', 'isMacAddId', 'bootedMsgEnable', 'canSendMsgBeforeDestIp',
                'reportError']
ALARM_KEYS = ['reportBUSY', 'reportHiZ', 'reportHomeSwStatus', 'reportDir', 'reportMotorStatus',
              'reportSwEvn', 'reportUVLO', 'reportThermalStatus', 'reportOCD', 'reportStall',
              'reportLimitSwStatus', 'OCThreshold', 'reportPositionInterval',
              'reportPositionListInterval']
DRIVER_KEYS = ['homingAtStartup', 'homingDirection', 'homingSpeed', 'homeSwMode',
               'prohibitMotionOnHomeSw', 'limitSwMode', 'prohibitMotionOnLimitSw',
               'goUntilTimeout', 'releaseSwTimeout', 'stepMode', 'isCurrentMode', 'slewRate',
               'electromagnetBrakeEnable', 'brakeTransitionDuration']
SPEED_KEYS = ['acc', 'dec', 'maxSpeed', 'fullStepSpeed', 'minSpeed']
VOLTAGE_KEYS = ['KVAL_HOLD', 'KVAL_RUN', 'KVAL_ACC', 'KVAL_DEC', 'INT_SPEED', 'ST_SLP',
                'FN_SLP_ACC', 'FN_SLP_DEC', 'STALL_TH', 'lowSpeedOptimizeEnable',
                'lowSpeedOptimize']
CURRENT_KEYS = ['TVAL_HOLD', 'TVAL_RUN', 'TVAL_ACC', 'TVAL_DEC', 'T_FAST', 'TON_MIN', 'TOFF_MIN']
SERVO_KEYS = ['kP', 'kI', 'kD']

# Keys whose array elements are bool in the firmware (globals.h: declared in the bool group).
BOOL_KEYS = {'reportBUSY', 'reportHiZ', 'reportHomeSwStatus', 'reportDir', 'reportMotorStatus',
             'reportSwEvn', 'reportUVLO', 'reportThermalStatus', 'reportOCD', 'reportStall',
             'reportLimitSwStatus', 'homingAtStartup', 'homingDirection', 'homeSwMode',
             'prohibitMotionOnHomeSw', 'limitSwMode', 'prohibitMotionOnLimitSw', 'isCurrentMode',
             'electromagnetBrakeEnable', 'lowSpeedOptimizeEnable'}

PRODUCTS = {
    # boardsDef.h: STEP400_R1 / STEP800_R1
    'STEP400': dict(n=4, brake=True, limit=True, current=True, driver='POWERSTEP01',
                    slew_default=5, template='configTemplate_step400.json'),
    'STEP800': dict(n=8, brake=True, limit=False, current=False, driver='L6470',
                    slew_default=2, template='configTemplate_step800.json'),
}


def default_config(product):
    """Default configuration: the template of configGenerator/, adjusted to what the board
    reports in `G` (correct spelling of goUntilTimeout, slewRate present, key set of the product)."""
    p = PRODUCTS[product]
    with open(os.path.join(TEMPLATE_DIR, p['template'])) as f:
        t = json.load(f)
    d = t['driverSettings']
    if 'goUnitlTimeout' in d:
        d['goUntilTimeout'] = d.pop('goUnitlTimeout')
    d.setdefault('slewRate', [p['slew_default']] * p['n'])
    if not p['limit']:
        for k in ('limitSwMode', 'prohibitMotionOnLimitSw'):
            d.pop(k, None)
        t['alarmAndReport'].pop('reportLimitSwStatus', None)
    if not p['current']:
        d.pop('isCurrentMode', None)
        t.pop('currentMode', None)
    if not p['brake']:
        d.pop('electromagnetBrakeEnable', None)
        d.pop('brakeTransitionDuration', None)
    # bool-typed keys are sent as true / false
    for sec in t.values():
        if isinstance(sec, dict):
            for k, v in sec.items():
                if k in BOOL_KEYS and isinstance(v, list):
                    sec[k] = [bool(x) for x in v]
    return t


class Card:
    """The microSD card. state: 'fat32' | 'none' | 'exfat'. `generation` changes whenever the
    card is taken out or put in, so a board that started with another generation cannot use it
    (the firmware reads the card only at start-up)."""

    def __init__(self, state='fat32', files=None):
        self.state = state
        self.files = dict(files or {})     # '/name' or '/dir/name' -> bytes
        self.dirs = set()                  # '/dir'
        self.generation = 0
        self.full = False

    def remove(self):
        self.state = 'none'
        self.generation += 1

    def insert(self, state='fat32'):
        self.state = state
        self.generation += 1

    def _find(self, name):
        low = name.lower()
        for k in self.files:
            if k.lower() == low:
                return k
        return None

    def read(self, name):
        k = self._find(name)
        return self.files[k] if k is not None else None

    def write(self, name, data):
        k = self._find(name)
        if k is not None:
            del self.files[k]
        self.files[name] = data

    def delete(self, name):
        k = self._find(name)
        if k is not None:
            del self.files[k]

    def has_dir(self, d):
        return d == '' or d.lower() in {x.lower() for x in self.dirs}

    def root_files(self):
        return [k for k in self.files if k.count('/') == 1]


class FakeBoard:
    def __init__(self, product='STEP400', fw=FIRMWARE_DEFAULT, card=None, my_id=0, seed=1,
                 chunk='random', noise=False, emit_boot_lines=True, boot_time=0.8, **attrs):
        assert product in PRODUCTS
        self.product = product
        self.spec = PRODUCTS[product]
        self.n = self.spec['n']
        self.fw = tuple(fw)
        self.card = card if card is not None else Card('fat32')
        self.my_id = my_id
        self.rng = random.Random(seed)
        self.chunk = chunk              # 'random' | 'whole' | int (fixed piece size)
        self.noise = noise              # put a non-JSON line before every response
        self.emit_boot_lines = emit_boot_lines
        self.boot_time = boot_time
        # delays [s]: G / T / F responses; the save (diagnosis.cpp: about 0.1-0.7 s)
        self.delay_G = 0.02
        self.delay_T = 0.01
        self.delay_F = 0.005
        self.delay_save = 0.1
        # timeouts of the firmware loops [s]; tests may shorten them
        self.brace_timeout = 10.0       # receiveConfigJson()
        self.fname_idle_timeout = 2.0   # receiveFilename(): per character
        self.fname_total_timeout = 10.0
        self.reboot_min_wait = 0.05     # REBOOT_REPLY_MIN_WAIT_MS
        self.reboot_brake_wait = 0.0    # up to 1 s with brakes
        # live state for `T`
        self.link_status = 1            # 0 unknown, 1 ON, 2 OFF
        self.reset_cause = 1
        self.motors = [self._motor() for _ in range(self.n)]
        self.boot_count = 0
        self.up = True
        self.io = None
        self.rx = bytearray()
        self._rx_evt = None
        self._task = None
        self.history = []               # (command, detail) of what the board did
        for k, v in attrs.items():     # delay_G, delay_T, delay_F, delay_save, reboot_brake_wait, ...
            if not hasattr(self, k):
                raise TypeError(f'unknown FakeBoard attribute {k}')
            setattr(self, k, v)
        self._boot()

    # ---------------------------------------------------------------- helpers
    def _motor(self):
        m = dict(position=0, speed=0.0, busy=False, HiZ=True, dir=False, motorStatus=0,
                 homeSwState=False, uvlo=False, thermalStatus=0, homingStatus=0,
                 isServoMode=False)
        if self.spec['limit']:
            m['limitSwState'] = False
        return m

    def log(self, *a):
        self.history.append(a)

    # ---------------------------------------------------------------- start-up
    def _boot(self):
        """setup(): loadConfig() (loadConfig.cpp), then the running network values."""
        self.boot_count += 1
        card = self.card
        self.sd_initialized = card.state == 'fat32'          # sd.begin(); exFAT counts as no card
        self.boot_card_generation = card.generation
        self.config_file_open = False
        self.config_file_parse = False
        self.config_filename = '/config.txt'                 # globals.cpp
        doc = None
        if self.sd_initialized:
            data = card.read('/config.txt')                  # priority 1
            if data is not None:
                self.config_file_open = True
                try:
                    doc = json.loads(data.decode('utf-8'))
                    self.config_file_parse = True
                    self.config_filename = '/config.txt'
                except ValueError:
                    doc = None
            if not self.config_file_parse:                   # priority 2: findFirstValidJson()
                d2, name = self._first_valid_json()
                if d2 is not None:
                    doc = d2
                    self.config_file_open = self.config_file_parse = True
                    self.config_filename = name
                else:
                    doc = None
        self.cfg = default_config(self.product)
        info = (doc or {}).get('information', {}) if isinstance(doc, dict) else {}
        self.config_name = info.get('configName', 'Default') if isinstance(info.get('configName', 'Default'), str) else 'Default'
        self.loaded_config_version = [-1, 0]
        if self.config_file_open:
            v = info.get('configVersion') if isinstance(info, dict) else None
            self.loaded_config_version = [(v[i] if isinstance(v, list) and len(v) > i and isinstance(v[i], int) else 0) for i in range(2)]
        t = info.get('targetProduct', '---') if isinstance(info, dict) else '---'
        self.config_target_product = t if isinstance(t, str) else '---'
        if isinstance(doc, dict):
            self._apply_sections(doc, boot=True)
        # running values: myIp / outPort / mac are the config values plus the board ID
        net = self.cfg['network']
        ip = list(net['myIp'])
        if net['isMyIpAddId'] and ip[3] + self.my_id <= 254:     # idOffset.cpp addIdToIpLastByte()
            ip[3] += self.my_id
        self.running_my_ip = ip
        self.running_out_port = net['outPort']
        if net['isOutPortAddId'] and net['outPort'] + self.my_id <= 0xFFFF:
            self.running_out_port = net['outPort'] + self.my_id
        self.rx.clear()
        self._boot_lines_pending = self.emit_boot_lines

    def _first_valid_json(self):
        """loadConfig.cpp findFirstValidJson(): the alphabetically first *.json in the root
        folder (strcasecmp), skipping names that start with '.'. If that one is not valid
        (not JSON, or no information.configVersion) there is no fallback to the next one."""
        best = None
        for k in self.card.root_files():
            base = k[1:]
            if base.startswith('.'):
                continue
            if not base.lower().endswith('.json'):
                continue
            if best is None or k.lower() < best.lower():
                best = k
        if best is None:
            return None, None
        try:
            d = json.loads(self.card.files[best].decode('utf-8'))
        except ValueError:
            return None, None
        if not isinstance(d, dict) or not isinstance(d.get('information'), dict) \
                or d['information'].get('configVersion') is None:
            return None, None
        return d, best

    # ---------------------------------------------------------------- config model
    def _compatible(self, cur, new):
        # ArduinoJson `value | default`: the default is used when the value is not of the type
        if isinstance(cur, bool):
            return isinstance(new, bool)
        if isinstance(cur, (int, float)):
            return isinstance(new, (int, float)) and not isinstance(new, bool)
        return False

    def _apply_sections(self, doc, boot=False):
        """The `x[i] | current` pattern of loadConfig() / receiveConfigJson(): an element that
        is missing or has the wrong type keeps its current value."""
        for sec, cur_sec in self.cfg.items():
            new_sec = doc.get(sec)
            if not isinstance(new_sec, dict):
                continue
            for k, cur in cur_sec.items():
                # loadConfig.cpp reads the legacy spelling goUnitlTimeout when goUntilTimeout is
                # missing; receiveConfigJson() reads goUntilTimeout only.
                legacy = boot and k == 'goUntilTimeout' and k not in new_sec and 'goUnitlTimeout' in new_sec
                if k not in new_sec and not legacy:
                    continue
                new = new_sec['goUnitlTimeout'] if legacy else new_sec[k]
                if isinstance(cur, list):
                    if not isinstance(new, list):
                        continue
                    for i in range(len(cur)):
                        if i < len(new) and self._compatible(cur[i], new[i]):
                            cur[i] = new[i]
                else:
                    if self._compatible(cur, new):
                        cur_sec[k] = new
        if not boot:
            # receiveConfigJson(): a position list interval turns the per-motor reports off
            ar = self.cfg['alarmAndReport']
            if ar['reportPositionListInterval'] > 0:
                ar['reportPositionInterval'] = [0] * self.n

    def _section(self, name, keys):
        src = self.cfg[name]
        return {k: src[k] for k in keys if k in src}

    def config_sections(self):
        """serializeConfigSectionsTo(): all sections except `board`, in the firmware's order."""
        c = self.cfg
        out = {
            'information': {'configName': self.config_name,
                            'configVersion': list(self.loaded_config_version),
                            'targetProduct': self.config_target_product},
            'network': self._section('network', NETWORK_KEYS),
            'alarmAndReport': self._section('alarmAndReport', ALARM_KEYS),
            'driverSettings': self._section('driverSettings', DRIVER_KEYS),
            'speedProfile': self._section('speedProfile', SPEED_KEYS),
            'voltageMode': self._section('voltageMode', VOLTAGE_KEYS),
        }
        if 'currentMode' in c:
            out['currentMode'] = self._section('currentMode', CURRENT_KEYS)
        out['servoMode'] = self._section('servoMode', SERVO_KEYS)
        return copy.deepcopy(out)

    # ---------------------------------------------------------------- responses
    def config_json(self):
        """printConfigAsJson()"""
        board = {'product': self.product, 'numMotors': self.n,
                 'firmwareVersion': list(self.fw), 'configFilename': self.config_filename}
        d = {'board': board}
        d.update(self.config_sections())
        return json.dumps(d, separators=(',', ':'))

    def status_json(self):
        """printStatusAsJson(). `ocd` and `stall` are a fixed false in v2.2.0."""
        board = {'product': self.product, 'mcu': 'SAMD21G18A', 'resetCause': self.reset_cause,
                 'resetCauseRaw': 1, 'firmwareVersion': list(self.fw),
                 'myIp': list(self.running_my_ip), 'myId': self.my_id,
                 'linkStatus': self.link_status, 'destMac': [255] * 6, 'arpPending': False,
                 'sdInitialized': self.sd_initialized, 'configLoaded': self.config_file_parse,
                 'configFilename': self.config_filename}
        motors = []
        for m in self.motors:
            o = {'position': m['position'], 'speed': m['speed'], 'busy': m['busy'],
                 'HiZ': m['HiZ'], 'dir': m['dir'], 'motorStatus': m['motorStatus'],
                 'homeSwState': m['homeSwState'], 'uvlo': m['uvlo'],
                 'thermalStatus': m['thermalStatus'], 'ocd': False, 'stall': False}
            if self.spec['limit']:
                o['limitSwState'] = m.get('limitSwState', False)
            o['homingStatus'] = m['homingStatus']
            o['isServoMode'] = m['isServoMode']
            motors.append(o)
        return json.dumps({'board': board, 'motors': motors}, separators=(',', ':'))

    def write_fixtures(self, directory, prefix=None):
        """Write the `G` and `T` responses to files (to compare with the real board's)."""
        os.makedirs(directory, exist_ok=True)
        prefix = prefix or self.product
        for cmd, text in (('G', self.config_json()), ('T', self.status_json())):
            with open(os.path.join(directory, f'{prefix}_{cmd}.json'), 'w') as f:
                f.write(text + '\n')

    # ---------------------------------------------------------------- serial I/O
    def attach(self, io):
        self.io = io
        self._last_io = io
        self.rx.clear()
        if self._boot_lines_pending:
            self._boot_lines_pending = False
            asyncio.ensure_future(self._emit_boot_lines())

    async def _emit_boot_lines(self):
        # main.cpp setup(): dbgPrint("myId:%ld\n"), dbgPrint("eth ok\n")
        for line in (f'myId:{self.my_id}', 'eth ok'):
            await self._out(line)

    def detach(self):
        self.io = None

    def feed(self, data: bytes):
        self.rx.extend(data)
        if self._rx_evt is not None:
            self._rx_evt.set()

    async def _out(self, text):
        """println(): the line ends with CR LF, delivered in pieces."""
        if self.io is None:
            return
        data = (text + '\r\n').encode('utf-8')
        if self.noise and text.startswith('{'):
            data = b'Ethernet link up\r\n' + data
        if self.chunk == 'whole':
            pieces = [data]
        else:
            pieces, i = [], 0
            while i < len(data):
                size = self.chunk if isinstance(self.chunk, int) else self.rng.randint(1, 96)
                pieces.append(data[i:i + size])
                i += size
        for p in pieces:
            if self.io is None:
                return
            await self.io.write(p)
            if len(pieces) > 1:
                await asyncio.sleep(0.001)

    async def _byte(self, timeout):
        """SerialUSB.read() with a wait: None on timeout."""
        loop = asyncio.get_running_loop()
        end = None if timeout is None else loop.time() + timeout
        while not self.rx:
            self._rx_evt.clear()
            left = None if end is None else end - loop.time()
            if left is not None and left <= 0:
                return None
            try:
                await asyncio.wait_for(self._rx_evt.wait(), left)
            except asyncio.TimeoutError:
                return None
        return self.rx.pop(0)

    # ---------------------------------------------------------------- main loop
    def start(self):
        """Start the main loop on the running event loop."""
        self._rx_evt = asyncio.Event()
        self._task = asyncio.ensure_future(self._main())

    async def stop(self):
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except (asyncio.CancelledError, Exception):
                pass
            self._task = None

    async def _main(self):
        """loop(): diagnosisCommand(SerialUSB.read()) for every byte (main.cpp, diagnosis.cpp).
        Unknown bytes (and the CR / LF after a command) are ignored."""
        while True:
            b = await self._byte(None)
            if b is None:
                continue
            c = chr(b)
            if c == 'G':
                await self._cmd_G()
            elif c == 'T':
                await self._cmd_T()
            elif c == '{':
                await self._cmd_brace()
            elif c == 'F':
                await self._cmd_F()
            elif c == 'R':
                await self._cmd_R()
            # 'm' 'c' 's' 't' 'p' ...: not imitated

    async def _cmd_G(self):          # printConfigAsJson()
        self.log('G')
        await asyncio.sleep(self.delay_G)
        await self._out(self.config_json())

    async def _cmd_T(self):          # printStatusAsJson()
        self.log('T')
        await asyncio.sleep(self.delay_T)
        await self._out(self.status_json())

    async def _cmd_F(self):          # receiveFilename()
        loop = asyncio.get_running_loop()
        buf = bytearray()
        t0 = loop.time()
        while (loop.time() - t0) < self.fname_total_timeout:
            b = await self._byte(self.fname_idle_timeout)
            if b is None:
                break
            if b in (10, 13):
                break
            if len(buf) < MAX_CONFIG_FILENAME - 1:
                buf.append(b)            # longer names are read to the end and cut at 63 bytes
        name = buf.decode('utf-8', errors='replace')
        await asyncio.sleep(self.delay_F)
        self.log('F', name)
        if len(buf) < 2 or buf[0] != ord('/'):
            await self._out('{"result":"error","message":"Filename must start with /"}')
            return
        dot = name.rfind('.')
        if dot < 0 or name[dot:].lower() not in ('.json', '.txt'):
            await self._out('{"result":"error","message":"Filename must end with .json or .txt"}')
            return
        self.config_filename = name
        await self._out(json.dumps({'result': 'ok', 'configFilename': name}, separators=(',', ':')))

    async def _cmd_brace(self):      # receiveConfigJson()
        loop = asyncio.get_running_loop()
        start = loop.time()
        buf = bytearray(b'{')
        depth = 1
        while depth > 0:
            left = self.brace_timeout - (loop.time() - start)
            b = await self._byte(max(left, 0)) if left > 0 else None
            if b is None:
                self.rx.clear()          # drain
                self.log('{', 'timeout')
                await self._out('{"result":"error","message":"Timeout"}')
                return
            if len(buf) >= BUF_SIZE - 1:
                self.rx.clear()
                self.log('{', 'overflow')
                await self._out('{"result":"error","message":"Buffer overflow"}')
                return
            buf.append(b)
            if b == ord('{'):
                depth += 1
            elif b == ord('}'):
                depth -= 1
        self.log('{', bytes(buf))
        try:
            doc = json.loads(buf.decode('utf-8'))
            if not isinstance(doc, dict):
                raise ValueError
        except ValueError:
            await self._out('{"result":"error","message":"JSON parse failed"}')
            return
        # information.configName is the only part of `information` that is applied
        name = doc.get('information', {}).get('configName') if isinstance(doc.get('information'), dict) else None
        if isinstance(name, str):
            self.config_name = name
        self._apply_sections(doc)
        await self._save()

    def _sd_save(self):
        """sdSaveConfig(): temp file + rename in the folder of configFilename."""
        if not self.sd_initialized:
            return 'No SD card'
        c = self.card
        if c.state != 'fat32' or c.generation != self.boot_card_generation or c.full:
            return 'SD open failed'      # taken out after start-up, put back (not re-read), full
        name = self.config_filename
        d = name[:name.rfind('/')]
        if not c.has_dir(d):
            return 'SD open failed'      # the folder does not exist: O_CREAT does not make it
        body = '{' + ','.join(f'"{k}":{json.dumps(v, separators=(",", ":"))}'
                              for k, v in self.config_sections().items()) + '}\n'
        c.write(name, body.encode('utf-8'))
        return None

    async def _save(self):
        # the board does not read the serial port for the duration of the save
        await asyncio.sleep(self.delay_save)
        err = self._sd_save()
        self.log('save', err or 'ok', self.config_filename)
        if err is None:
            await self._out('{"result":"ok","message":"Saved to SD. Reboot (send \'R\') to apply."}')
        else:
            await self._out(json.dumps({'result': 'error', 'message': err}, separators=(',', ':')))

    async def _cmd_R(self):          # rebootBoard()
        self.log('R')
        await self._out('{"result":"ok","message":"Rebooting..."}')
        await asyncio.sleep(self.reboot_min_wait + self.reboot_brake_wait)
        await self.reboot()

    async def reboot(self):
        """The reset: USB disconnects, the board starts again (loadConfig() reads the card)."""
        io = getattr(self, '_last_io', None)
        self.up = False
        if io is not None:
            await io.set_plugged(False)
            if self.io is not None:
                await io.drop_connection()
        await asyncio.sleep(self.boot_time)
        self._boot()
        self.up = True
        if io is not None:
            await io.set_plugged(True)


# Places where this fake guesses (to be checked against a real board in stage 2):
GUESSES = [
    "`G` / `T` key set, key order and value types (bool vs int, float formatting) follow the "
    "source but have not been compared with a real response.",
    "`T`: board.mcu string, resetCause / resetCauseRaw values, destMac and arpPending values.",
    "Default values come from configGenerator/configTemplate_step*.json, not the firmware "
    "defaults (the two differ, see NOTES_v2.2.0 S1).",
    "A configuration with a section that fails ArduinoJson's filtered parse is reported only for "
    "`network` (as in the source); the fake treats any invalid JSON as 'JSON parse failed'.",
    "The write/rename of the SD save is modelled as: not initialised -> 'No SD card'; "
    "card gone / put back / full / folder missing -> 'SD open failed'.",
    "Running myIp / outPort follow idOffset.cpp; the running MAC (isMacAddId) is not modelled.",
    "Bytes the host sends while the board sleeps are buffered without limit (USB buffer sizes "
    "are not modelled).",
    "The boot lines ('myId:', 'eth ok') and 'Ethernet link up' are text only; real boards lose "
    "what they print while no host has the port open.",
]
