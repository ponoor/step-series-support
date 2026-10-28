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
(() => {
  'use strict';
  const WS_URL = window.__SERIAL_WS_URL__;
  if (!WS_URL) return;

  const dom = (name, msg) => new DOMException(msg, name);

  class FakeSerialPort extends EventTarget {
    constructor() {
      super();
      this._ws = null;
      this._readable = null;
      this._writable = null;
      this._rctl = null;
      this._opening = false;
      this._open = false;       // the port is open, whatever state its streams are in
      this.onconnect = null;
      this.ondisconnect = null;
    }
    get readable() { return this._readable; }
    get writable() { return this._writable; }
    getInfo() { return { usbVendorId: 0x2341, usbProductId: 0x804d }; }

    async open(options) {
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
            if (!this._ws || this._ws.readyState !== WebSocket.OPEN)
              throw dom('NetworkError', 'The device has been lost.');
            this._ws.send(chunk);
          },
          close: () => { this._writable = null; },
          abort: () => { this._writable = null; },
        });
        ws.onmessage = (ev) => {
          if (typeof ev.data === 'string') { this._control(JSON.parse(ev.data)); return; }
          try { this._rctl && this._rctl.enqueue(new Uint8Array(ev.data)); } catch (_) {}
        };
        ws.onclose = () => { if (this._ws === ws) this._lost(); };
        window.__serialShim.log.push({ ev: 'open' });
      } finally {
        this._opening = false;
      }
    }

    async close() {
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
      if (msg.type === 'disconnect') this._lost();
    }

    // Device lost (cable pulled, board reset). Called from the WebSocket or from the backend.
    _lost() {
      const ws = this._ws;
      const wasOpen = this._open;
      this._ws = null;
      this._open = false;
      if (this._rctl) { try { this._rctl.error(dom('NetworkError', 'The device has been lost.')); } catch (_) {} }
      this._readable = null;
      this._writable = null;
      this._rctl = null;
      if (ws) { try { ws.close(); } catch (_) {} }
      if (wasOpen) {
        window.__serialShim.log.push({ ev: 'disconnect' });
        this.dispatchEvent(new Event('disconnect'));
        serial.dispatchEvent(new Event('disconnect'));   // (Chrome: bubbles from the port; target differs)
      }
    }
  }

  class FakeSerial extends EventTarget {
    constructor() { super(); this._port = new FakeSerialPort(); this._granted = false; }
    async requestPort() {
      if (window.__SERIAL_REQUEST_FAIL__)
        throw dom('NotFoundError', 'Failed to execute \'requestPort\' on \'Serial\': No port selected by the user.');
      this._granted = true;
      window.__serialShim.log.push({ ev: 'requestPort' });
      return this._port;
    }
    async getPorts() { return this._granted ? [this._port] : []; }
  }

  const serial = new FakeSerial();
  Object.defineProperty(navigator, 'serial', { value: serial, configurable: true });
  window.__serialShim = { log: [], port: serial._port };
})();
