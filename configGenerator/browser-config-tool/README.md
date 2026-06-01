# STEP Series Browser Configuration Tool

A single-file browser-based configuration tool for STEP100/200/400/800 stepper motor driver boards.

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

Limit switch fields (Alarm & Report, Driver Settings) are shown only when `limitSwMode` is present in the config (STEP400). Brake fields are shown only when `electromagnetBrakeEnable` is present.

## Board variants

| Board | Axes | Current Mode | Limit SW | Brake |
|-------|------|--------------|----------|-------|
| STEP100 | 1 | Yes | No | No |
| STEP200 | 2 | No | No | No |
| STEP400 | 4 | Yes | Yes | Yes |
| STEP800 | 8 | No | No | No |

When loading from a file, axis count is detected from the length of per-axis arrays. When reading from a board, axis count comes from `board.numMotors` in the 'G' response.

## Serial protocol

| Send | Receive | Purpose |
|------|---------|---------|
| `G` | JSON config + newline | Read full config |
| `T` | JSON status + newline | Read real-time status |
| `{...}` | `{"result":"ok/error",...}` | Write config to SD |
| `R` | `{"result":"ok",...}` | Reboot |

Baud rate is specified as 9600 for Web Serial API compliance. The SAMD21 native USB CDC ignores this value.

## Notes

- **goUntilTimeout**: older config files may contain the misspelling `goUnitlTimeout`. The tool reads both; the firmware uses `goUntilTimeout`.
- **MAC addresses**: stored as decimal integers in JSON. Use the "Show Hex" toggle for hex display.
- **slewRate**: the stored value is an index (0–5) mapping to actual slew rates (114–980 V/µs), not the raw V/µs value.
- Config changes require a reboot to take effect.
