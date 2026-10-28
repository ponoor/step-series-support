"""WebSocket server between serial_shim.js (in the page) and a "device".

A device is a FakeBoard (fake_board.py) or a SerialBridge (pyserial, for a real board).
Everything that crosses the WebSocket is recorded with a time, a direction and the bytes:

    tx  page -> board      rx  board -> page      ev  an event (open, close, disconnect, ...)

so a test can check, for example, that no `{` or `F` was sent.

The server runs on its own thread and event loop; the methods called from tests are thread-safe.
"""
import asyncio
import http
import json
import threading
import time

from websockets.asyncio.server import serve


class Entry(dict):
    @property
    def text(self):
        return self['data'].decode('utf-8', errors='replace')


class _Io:
    """What a device sees of the connection."""

    def __init__(self, backend):
        self.b = backend

    async def write(self, data: bytes):
        await self.b._send_to_page(data)

    async def drop_connection(self):
        await self.b._drop()

    async def set_plugged(self, on: bool):
        self.b.plugged = on
        self.b._record('ev', f'plugged={on}')


class SerialBackend:
    def __init__(self, device=None, log_path=None):
        self.device = device
        self.log_path = log_path
        self.plugged = True
        self.entries = []
        self._t0 = time.monotonic()
        self._lock = threading.Lock()
        self._ws = None
        self._loop = None
        self._server = None
        self._thread = None
        self._ready = threading.Event()
        self.port = None
        self._logf = open(log_path, 'w') if log_path else None
        self.connections = 0

    # ------------------------------------------------------------ lifecycle
    def start(self):
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        if not self._ready.wait(10):
            raise RuntimeError('serial backend did not start')
        return self

    def _run(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._serve())

    async def _serve(self):
        async def refuse(connection, request):
            # one page at a time, and none while the board is "unplugged" / rebooting
            if not self.plugged or self._ws is not None:
                return connection.respond(http.HTTPStatus.SERVICE_UNAVAILABLE, 'unavailable\n')
            return None

        self._server = await serve(self._handler, '127.0.0.1', 0, process_request=refuse,
                                   max_size=None)
        self.port = self._server.sockets[0].getsockname()[1]
        self._stop = asyncio.Event()
        if self.device is not None and hasattr(self.device, 'start'):
            self.device.start()
        self._ready.set()
        await self._stop.wait()
        if self.device is not None and hasattr(self.device, 'stop'):
            await self.device.stop()
        self._server.close()
        await self._server.wait_closed()

    def stop(self):
        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._stop.set)
        if self._thread:
            self._thread.join(5)
        if self._logf:
            self._logf.close()

    def __enter__(self):
        return self.start()

    def __exit__(self, *a):
        self.stop()

    @property
    def url(self):
        return f'ws://127.0.0.1:{self.port}/'

    # ------------------------------------------------------------ record
    def _record(self, direction, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        e = Entry(t=round(time.monotonic() - self._t0, 4), dir=direction, data=bytes(data))
        with self._lock:
            self.entries.append(e)
            if self._logf:
                self._logf.write(json.dumps({'t': e['t'], 'dir': direction,
                                             'text': e.text, 'hex': e['data'].hex()}) + '\n')
                self._logf.flush()
        return e

    def mark(self):
        with self._lock:
            return len(self.entries)

    def since(self, mark=0, direction=None):
        with self._lock:
            es = self.entries[mark:]
        return [e for e in es if direction is None or e['dir'] == direction]

    def sent(self, mark=0):
        """Everything the page sent since `mark`, as one string."""
        return b''.join(e['data'] for e in self.since(mark, 'tx')).decode('utf-8', errors='replace')

    def received_json(self, mark=0):
        """The JSON lines the board sent since `mark`."""
        text = b''.join(e['data'] for e in self.since(mark, 'rx')).decode('utf-8', errors='replace')
        out = []
        for line in text.splitlines():
            line = line.strip()
            if line.startswith('{'):
                try:
                    out.append(json.loads(line))
                except ValueError:
                    pass
        return out

    # ------------------------------------------------------------ connection
    async def _handler(self, ws):
        self._ws = ws
        self.connections += 1
        self._record('ev', 'open')
        dev = self.device
        if dev is not None:
            dev.attach(_Io(self))
            if hasattr(dev, 'on_open'):
                dev.on_open()
        try:
            async for msg in ws:
                if isinstance(msg, str):
                    continue
                self._record('tx', msg)
                if dev is not None:
                    dev.feed(msg)
        except Exception:
            pass
        finally:
            if self._ws is ws:
                self._ws = None
            self._record('ev', 'close')
            if dev is not None:
                dev.detach()

    async def _send_to_page(self, data: bytes):
        ws = self._ws
        if ws is None:
            return
        self._record('rx', data)
        try:
            await ws.send(data)
        except Exception:
            pass

    async def _drop(self, replug=False):
        ws = self._ws
        if ws is not None:
            self._record('ev', 'device-drop')
            try:
                await ws.send(json.dumps({'type': 'disconnect', 'replug': replug}))
                await ws.close()
            except Exception:
                pass

    # ------------------------------------------------------------ test API (thread-safe)
    def call(self, coro, timeout=10):
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result(timeout)

    def call_soon(self, fn, *a):
        self._loop.call_soon_threadsafe(fn, *a)

    def disconnect(self, stay_unplugged=True):
        """Pull the cable: the page sees a lost device. New connections are refused until plug()."""
        async def go():
            if stay_unplugged:
                self.plugged = False
                self._record('ev', 'plugged=False')
            await self._drop(replug=not stay_unplugged)
        self.call(go())

    def plug(self):
        self.plugged = True
        self._record('ev', 'plugged=True')

    def reboot_board(self):
        """Start a reboot of the fake board (like a reset)."""
        self.call(self.device.reboot())


class SerialBridge:
    """Device that forwards to a real serial port with pyserial (also `loop://` for a pipe test)."""

    def __init__(self, url, baudrate=9600, resolver=None, wait=20.0, settle=0.0):
        """`resolver()` (optional) returns the device to open each time the page opens the port:
        after a reboot or an unplug the name can change, so the same board is looked for again
        (by its USB serial number, hw_protocol.Board.find_again) and never the other one. The page
        waits (up to `wait` s) while the board is away."""
        import serial
        self.serial = serial
        self.resolver = resolver
        self.wait = wait
        self.settle = settle      # s to wait after a port was found again (a person needs that long to click Connect)
        self.url = url
        self.baudrate = baudrate
        self.ser = None
        self.io = None
        self._reader = None
        self._stop = threading.Event()
        self._loop = None

    def start(self):
        self._loop = asyncio.get_running_loop()

    async def stop(self):
        self._close()

    def attach(self, io):
        self.io = io
        self._stop.clear()
        if self.resolver is not None:
            self.url = self.resolver()
            time.sleep(self.settle)
        end = time.monotonic() + self.wait
        while True:
            try:
                self.ser = self.serial.serial_for_url(self.url, baudrate=self.baudrate, timeout=0.05)
                break
            except Exception:
                if time.monotonic() > end:
                    raise
                time.sleep(0.05)
                if self.resolver is not None:
                    self.url = self.resolver()
        self._reader = threading.Thread(target=self._read_loop, daemon=True)
        self._reader.start()

    def detach(self):
        self._close()
        self.io = None

    def _close(self):
        self._stop.set()
        if self._reader:
            self._reader.join(2)
            self._reader = None
        if self.ser:
            try:
                self.ser.close()
            except Exception:
                pass
            self.ser = None

    def feed(self, data):
        if self.ser:
            self.ser.write(data)

    def _read_loop(self):
        ser = self.ser
        while not self._stop.is_set():
            try:
                data = ser.read(max(ser.in_waiting, 1))
            except Exception:
                # the port vanished (unplugged / the board rebooted): tell the page
                if not self._stop.is_set() and self.io is not None:
                    asyncio.run_coroutine_threadsafe(self.io.drop_connection(), self._loop)
                break
            if data and self.io is not None:
                asyncio.run_coroutine_threadsafe(self.io.write(data), self._loop)
