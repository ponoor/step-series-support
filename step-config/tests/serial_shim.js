// Replacement for navigator.serial, loaded with Playwright's add_init_script.
//
// The page talks to a fake SerialPort whose bytes go over a WebSocket to serial_backend.py
// (window.__SERIAL_WS_URL__, set by the test before this script runs). index.html is not
// changed; it sees the same surface as Chrome's Web Serial API in the part it uses:
//   navigator.serial.requestPort() / getPorts()
//   port.open({baudRate}), port.close(), port.readable, port.writable
//   'disconnect' events on navigator.serial and on the port
//
// Strictness copied from Chrome (so that bugs in the tool's close / reopen order show up):
//   - open() on an open port: InvalidStateError
//   - close() while readable or writable is locked: TypeError (Chrome rejects)
//   - on a lost device, a pending read() rejects with NetworkError and readable / writable
//     become null; open() then fails with NetworkError until the backend "plugs in" again
//   - bytes are enqueued exactly as they arrive from the WebSocket (one chunk per message)
//
// A lost device (the part of Chrome's behaviour that the stage 3 test with the real Chrome showed
// the tool had to survive; see claude_docs/REPORT_cfgtest_3b_fixes.md):
//   - the lost SerialPort object is dead for good: connected is false, open() fails with
//     NetworkError, close() with InvalidStateError ("already closed");
//   - when the device comes back, the browser makes a NEW SerialPort object, fires 'connect' at
//     navigator.serial (event.target is the new port) and lists it in getPorts();
//     __serialShim.plugIn() does this, and the backend's disconnect(stay_unplugged=False) does it
//     50 ms after the loss; after a board reboot or disconnect(stay_unplugged=True) the device is
//     "away" (getPorts() is empty) until plugIn(), or until requestPort() (the user picks it);
//   - window.__SERIAL_HANG__ = {open, close, write, writerClose}: the named operation on the lost
//     device never settles (a pending promise that Chrome may leave pending; not known which);
//     'stall': write() never settles even though the device is there.
(() => {
  'use strict';
  const WS_URL = window.__SERIAL_WS_URL__;
  if (!WS_URL) return;

  const dom = (name, msg) => new DOMException(msg, name);
  const hang = (what) => !!(window.__SERIAL_HANG__ && window.__SERIAL_HANG__[what]);
  // 'connect' / 'disconnect' fire at the port and bubble to navigator.serial with the port as target
  const fire = (port, type) => {
    port.dispatchEvent(new Event(type));
    const ev = new Event(type, { bubbles: true });
    Object.defineProperty(ev, 'target', { value: port });
    serial.dispatchEvent(ev);
    window.__serialShim.log.push({ ev: type });
  };

  class FakeSerialPort extends EventTarget {
    constructor() {
      super();
      this._ws = null;
      this._readable = null;
      this._writable = null;
      this._rctl = null;
      this._opening = false;
      this._open = false;       // the port is open, whatever state its streams are in
      this._gone = false;       // the device was lost: this object is dead
      this.onconnect = null;
      this.ondisconnect = null;
    }
    get readable() { return this._readable; }
    get writable() { return this._writable; }
    get connected() { return !this._gone; }
    getInfo() { return { usbVendorId: 0x2341, usbProductId: 0x804d }; }

    async open(options) {
      if (this._gone) {
        if (hang('open')) return new Promise(() => {});
        throw dom('NetworkError', 'Failed to open serial port.');
      }
      if (!options || typeof options.baudRate !== 'number')
        throw new TypeError("Failed to execute 'open' on 'SerialPort': required member baudRate is undefined.");
      if (this._opening || this._open)
        throw dom('InvalidStateError', "Failed to execute 'open' on 'SerialPort': The port is already open.");
      this._opening = true;
      try {
        const ws = new WebSocket(WS_URL);
        ws.binaryType = 'arraybuffer';
        await new Promise((resolve, reject) => {
          ws.onopen = () => resolve();
          ws.onerror = () => reject(dom('NetworkError', "Failed to open serial port."));
        });
        this._ws = ws;
        this._open = true;
        this._readable = new ReadableStream({
          start: (ctl) => { this._rctl = ctl; },
          // cancel / close / error end the readable only; the writable and the port stay
          cancel: () => { this._readable = null; this._rctl = null; },
        });
        this._writable = new WritableStream({
          write: (chunk) => {
            if ((this._gone && hang('write')) || hang('stall')) return new Promise(() => {});
            if (!this._ws || this._ws.readyState !== WebSocket.OPEN)
              throw dom('NetworkError', 'The device has been lost.');
            this._ws.send(chunk);
          },
          close: () => {
            if (this._gone && hang('writerClose')) return new Promise(() => {});
            this._writable = null;
          },
          abort: () => { this._writable = null; },
        });
        ws.onmessage = (ev) => {
          if (typeof ev.data === 'string') { this._control(JSON.parse(ev.data)); return; }
          try { this._rctl && this._rctl.enqueue(new Uint8Array(ev.data)); } catch (_) {}
        };
        ws.onclose = () => { if (this._ws === ws) this._lost(false); };
        window.__serialShim.log.push({ ev: 'open' });
      } finally {
        this._opening = false;
      }
    }

    async close() {
      if (this._gone) {
        if (hang('close')) return new Promise(() => {});
        throw dom('InvalidStateError', "Failed to execute 'close' on 'SerialPort': The port is already closed.");
      }
      if (!this._open) return;
      if (this._readable && this._readable.locked)
        throw new TypeError("Failed to execute 'close' on 'SerialPort': Cannot cancel a locked stream.");
      if (this._writable && this._writable.locked)
        throw new TypeError("Failed to execute 'close' on 'SerialPort': Cannot abort a locked stream.");
      const ws = this._ws;
      this._ws = null;
      this._readable = null;
      this._writable = null;
      this._rctl = null;
      this._open = false;
      if (ws) { try { ws.close(); } catch (_) {} }
      window.__serialShim.log.push({ ev: 'close' });
    }

    // Backend commands (text frames).
    _control(msg) {
      if (msg.type === 'disconnect') this._lost(!!msg.replug);
    }

    // Device lost (cable pulled, board reset). Called from the WebSocket or from the backend.
    _lost(replug) {
      const ws = this._ws;
      const wasOpen = this._open;
      if (wasOpen) this._gone = true;
      this._ws = null;
      this._open = false;
      if (this._rctl) { try { this._rctl.error(dom('NetworkError', 'The device has been lost.')); } catch (_) {} }
      this._readable = null;
      this._writable = null;
      this._rctl = null;
      if (ws) { try { ws.close(); } catch (_) {} }
      if (wasOpen) {
        window.__serialShim.log.push({ ev: 'disconnect' });
        fire(this, 'disconnect');
        serial._plugged = false;
        if (replug) setTimeout(() => serial.plugIn(), 50);
      }
    }
  }

  class FakeSerial extends EventTarget {
    constructor() { super(); this._port = new FakeSerialPort(); this._granted = false; this._plugged = true; }
    async requestPort() {
      if (window.__SERIAL_REQUEST_FAIL__)
        throw dom('NotFoundError', 'Failed to execute \'requestPort\' on \'Serial\': No port selected by the user.');
      this._granted = true;
      // the user picks the device that is there now: after a loss that is a new Port object
      if (this._port._gone) { this._port = new FakeSerialPort(); window.__serialShim.port = this._port; }
      this._plugged = true;
      window.__serialShim.log.push({ ev: 'requestPort' });
      return this._port;
    }
    async getPorts() { return this._granted && this._plugged ? [this._port] : []; }
    // The device is back: a new Port object, and a 'connect' event
    plugIn() {
      if (this._plugged) return;
      this._port = new FakeSerialPort();
      window.__serialShim.port = this._port;
      this._plugged = true;
      if (this._granted) fire(this._port, 'connect');
    }
  }

  const serial = new FakeSerial();
  Object.defineProperty(navigator, 'serial', { value: serial, configurable: true });
  window.__serialShim = { log: [], port: serial._port, plugIn: () => serial.plugIn() };
})();
