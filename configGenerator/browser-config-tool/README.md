# STEP Series Browser Configuration Tool

A single-file browser-based configuration tool for STEP100/200/400/800 stepper motor driver boards.

## Where this tool lives

- **This folder is the source of truth** (`index.html`). Edit it here.
- The published tool is at **<https://ponoor.com/tools/step-config/>**. It is uploaded by hand: after a change here, upload `index.html` to that address.
- Firmware: works with **v2.1.0 or later**. Checked against the source of **v2.2.0** (USB serial commands `G`, `T`, `{`, `F`, `R`, the configuration keys and their ranges).
- The copy of `index.html` in the firmware repository (`step-series-universal-firmware`) will be removed in the next firmware release, and the firmware README will link to the URL above.

## Requirements

- **Chrome or Edge** (required for Web Serial API)
- Firefox and Safari: offline file workflow only (serial features disabled)

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
