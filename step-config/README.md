# STEP Series Browser Configuration Tool

A single-file browser-based configuration tool for STEP100/200/400/800 stepper motor driver boards.

## Where this tool lives

- **This folder is the source of truth** (`index.html`). Edit it here.
- The published tool is at **<https://ponoor.com/tools/step-config/>**. It is uploaded by hand: after a change here, upload `index.html` to that address.
- Firmware: works with **v2.1.0 or later**. Checked against the source of **v2.2.0** (USB serial commands `G`, `T`, `{`, `F`, `R`, the configuration keys and their ranges).
- The copy of `index.html` in the firmware repository (`step-series-universal-firmware`) will be removed in the next firmware release, and the firmware README will link to the URL above.

## Requirements

- **Chrome or Edge** (Web Serial API)
- Firefox 151 or later has the Web Serial API and should work, but has not been tested with a board
- Safari: no Web Serial API; offline file workflow only (Load JSON / Download JSON)

## Usage

### Offline mode (no board)

1. Open `index.html` in Chrome/Edge
2. Click **Load JSON** → select a `config.txt` from the SD card
3. Edit values in the form
4. Click **Download JSON** → saves `config.txt` for the SD card

### Connected mode

1. Connect the board via USB
2. Click **Connect** → select the COM port in the browser dialog
3. The tool auto-reads the current config from the board
4. Edit values, then click **Save to SD**
5. Reboot the board to apply changes (offered automatically after save)

### Real-time status

Click **▶ Start Status** to poll motor status at 1 Hz. Status appears in the **Real-time Status** panel.

## Sections

| Section | Conditional |
|---------|-------------|
| Board Info | Always shown |
| Network | Always shown |
| Alarm & Report | Always shown |
| Driver Settings | Always shown |
| Speed Profile | Always shown |
| Voltage Mode | Always shown |
| Current Mode | Shown only when `currentMode` key present (STEP100, STEP400) |
| Servo Mode | Always shown |

Limit switch fields (Alarm & Report, Driver Settings) are shown only when `limitSwMode` is present in the config (STEP400). Brake fields are shown only when `electromagnetBrakeEnable` is present (the board reports it when it has the brake output: STEP400 and STEP800 products; the early prototype boards do not).

## Board variants

| Board | Axes | Current Mode | Limit SW | Brake |
|-------|------|--------------|----------|-------|
| STEP100 | 1 | Yes | No | No |
| STEP200 | 2 | No | No | No |
| STEP400 | 4 | Yes | Yes | Yes |
| STEP800 | 8 | No | No | Yes |

The STEP400 / STEP800 products (R1) have the brake output. The slew rate has 6 steps on STEP100/400 (PowerSTEP01) and 3 steps on STEP200/800 (L6470). Overcurrent and stall thresholds are shown with their current, which differs between the two drivers.

When loading from a file, the board is taken from `information.targetProduct` (or the number of axes if there is none); axis count is detected from the length of per-axis arrays. When reading from a board, axis count comes from `board.numMotors` in the 'G' response.

## Serial protocol

| Send | Receive | Purpose |
|------|---------|---------|
| `G` | JSON config + newline | Read full config |
| `T` | JSON status + newline | Read real-time status |
| `F<path>\n` | `{"result":"ok","configFilename":...}` | Set the file name for the next save |
| `{...}` | `{"result":"ok/error",...}` | Apply the config and write it to SD |
| `R` | `{"result":"ok",...}` | Reboot |

- `F<path>`: the path starts with `/`, ends with `.json` or `.txt`, and is at most 63 bytes. At start-up the board reads only `/config.txt` and then the first `*.json` of the root folder, so the tool asks before saving under any other name.
- `{...}`: at most 4095 bytes. The motors should be stopped while it is written (the board does not process anything for about 0.1–0.7 s while it saves). Errors: `No SD card` (no card, or exFAT), `SD open failed` (card removed after start-up, full, or a path that cannot be created).
- The IP address, ports and MAC address take effect at the next start.
Baud rate is specified as 9600 for Web Serial API compliance. The SAMD21 native USB CDC ignores this value.

## Notes

- **goUntilTimeout**: older config files may contain the misspelling `goUnitlTimeout`. The tool reads both; the firmware uses `goUntilTimeout`.
- **MAC addresses**: stored as decimal integers in JSON. Use the "Show Hex" toggle for hex display.
- **slewRate**: the stored value is an index (0–5) mapping to actual slew rates (114–980 V/µs), not the raw V/µs value.
- Config changes require a reboot to take effect.

## Changelog

The version of the tool (`TOOL_VERSION` in `index.html`) is separate from the firmware version, because the tool is fixed and published at a different time. Major: the configuration file format changes. Minor: a feature is added. Patch: a fix only. The firmware it was checked with is `TESTED_FIRMWARE`; the oldest supported is `MIN_FIRMWARE`.

### v2.1.0 (checked with firmware v2.2.0)

- Show the tool version and the firmware version it was checked with; after reading a board, notice a firmware older than v2.1.0 or newer than the checked one.
- STEP800 / STEP200 slew rate has the 3 steps of the L6470 (180 / 290 / 530 V/µs); the board is detected from `information.targetProduct` or the number of axes when a file is loaded.
- STEP400 overcurrent threshold is 0–31 (it was 0–15, so 16–31 were lost on save); options show the current.
- Stall threshold: 0–31 on STEP400/100 and 0–127 on STEP800/200, shown with the current; TON_MIN / TOFF_MIN are 0–127.
- TVAL options are 0–64 with 78.125 mA steps (the firmware does not limit TVAL in a configuration file).
- Disconnect no longer shows the "Serial connection lost" banner; the "Web Serial API is not available" text names Chrome and Edge and says Firefox 151 or later should work but is untested.
- Empty, non-numeric and out-of-range values are refused before saving or downloading; `{` / `}` in the config name and configurations over 4095 bytes are refused.
- Check the save file name (`F<path>`): leading `/`, `.json` / `.txt`, at most 63 bytes; ask before saving under a name the board does not read at start-up.
- A connection lost while a save, read, status request or reboot is waiting for the board ends that wait at once with an error (a save no longer blocks Start Status for 15 s); the save error says the board may or may not have saved.
- The rejection of the serial streams after a lost connection is handled, so the console shows no `Uncaught (in promise)` error.
- Closing the connection (Disconnect, a lost device, Reboot) gives each step 1 s at most and always resets the tool, so a pending Web Serial promise after unplugging in the middle of a save can no longer leave the tool stuck on "Disconnect".
- A write to the port that does not finish within 3 s is treated as a lost connection.
- Reconnect no longer reopens the Port object that was lost (Chrome makes a new one when the device comes back): it uses the port of the `connect` event, else the only connected granted port, else asks with the port picker (several granted ports); if the board is not back on USB yet it waits up to 3 s for the `connect` event and then says `the board is not connected. Plug in the USB cable and click Connect.` (it does not call `requestPort()` after waiting: that needs a click within about 5 s); it times out and then shows `Reconnect failed: …`, and warns when a different board (another `board.product`) answers.
- The console shows `[serial] …` lines with times for opening, closing and reconnecting, to find where it stops; text the board itself sends (not JSON) is shown as `[board] …`.
- Dark mode: the Connect / Disconnect / Reboot buttons have dark text (contrast at least 4.5:1); the hover colour of the red buttons no longer hides their label.
- A downloaded file gets a valid `information.configVersion` and `targetProduct`.
- README: source of truth, published URL, supported firmware, corrected board table.
- Note beside Save to SD to stop the motors first; the `OCD` and `Stall` rows of the status are shown as "not reported" (v2.2.0 always sends false); the save errors `No SD card` and `SD open failed` explain the likely causes.

### v2.0

- First publication (firmware v2.1.0).
