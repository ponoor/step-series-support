# Tests of the browser configuration tool (no hardware)

Playwright tests that open the real `step-config/index.html` and talk to a **fake board**
through a **Web Serial shim**. `index.html` is not modified.

What they check: the UI behaviour of the checklist `CHECKLIST_config_tool_v220.md` that needs no
board (rows are tagged with `@pytest.mark.checklist("4.2")` = section 4, 2nd `[ ]`).

## Set up

```bash
python3 -m venv ~/.venvs/step-config-test          # keep it outside Dropbox
~/.venvs/step-config-test/bin/pip install -r step-config/tests/requirements.txt
~/.venvs/step-config-test/bin/python -m playwright install chromium firefox webkit
```

## Run (from the repository root)

```bash
~/.venvs/step-config-test/bin/pytest step-config/tests
```

`-m "not hw"` is the default; tests marked `hw` need a real board (stage 2). Output goes to
`step-config/tests/out/` (ignored by git): `logs/*.jsonl` (every byte between page and board),
`screens/*.png`, `downloads/`, `checklist_results.json`.

## How it works

```
index.html ── serial_shim.js ──WebSocket── serial_backend.py ─┬─ fake_board.py   (these tests)
                                                              └─ SerialBridge → pyserial → real board
```

- `serial_shim.js` replaces `navigator.serial` (init script). Bytes are passed on in the pieces
  they arrive in. Like Chrome it throws on a second `open()` and on `close()` with a locked
  stream, and errors a pending `read()` with `NetworkError` when the device is lost.
- `serial_backend.py` records everything; tests use it to check, e.g., that no `{` or `F` was sent.
- `fake_board.py` imitates `G`, `T`, `{`, `F`, `R` and the start-up file choice of firmware v2.2.0
  (each function names its source in the firmware). It cuts lines at random places, can delay
  answers, and can change the firmware version, card state and contents.

## Limits

A pass against the fake board says nothing about the firmware. Its guesses are listed in
`GUESSES` at the end of `fake_board.py`. The shim differs from real Web Serial in buffer sizes,
event targets (`disconnect` is dispatched on the port and on `navigator.serial` separately) and
timing. Real Chrome, a real USB unplug, Safari and Firefox are checked by hand in stage 3.
