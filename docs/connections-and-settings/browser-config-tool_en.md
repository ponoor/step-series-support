---
title: Configuration with Browser Tool
wp_id:
slug: browser-config-tool
lang: en
link: "https://ponoor.com/en/docs/step-series/settings/browser-config-tool/"
parent: 867
menu_order: 50
---

# Configuration with Browser Tool

> **Requires firmware v2.1.0 or later.**  
> For earlier firmware, use the [legacy per-product configuration tools](setup-with-a-microsd-card_en.md#legacy-per-product-configuration-tools).

The browser configuration tool lets you read, edit, and save the board configuration directly over USB from a web browser — without removing the microSD card from the device.

The tool is available at: <https://ponoor.com/tools/step-config/>

## Requirements

- Google Chrome or Microsoft Edge (Web Serial API required — Firefox and Safari are not supported)
- USB cable connected between your computer and the STEP400/STEP800
- Firmware v2.1.0 or later installed on the device

## Connecting to the board

1. Power on the device and connect the USB cable to your computer.
2. Open the tool in Chrome or Edge.
3. Click **Connect**.
4. Select the serial port corresponding to your device from the browser dialog.
5. The tool reads the current configuration from the device and displays it in the interface.

The device does not need a microSD card inserted for a USB connection, but saving the configuration to SD requires one.

## Reading and editing configuration

The configuration is organized into collapsible sections that mirror the JSON config file structure:

- **Information** — config name, firmware version, target product
- **Network** — IP addresses, ports, MAC address settings
- **Alarm and Report** — enable/disable various status reports
- **Driver Settings** — homing, microstepping, electromagnetic brake
- **Speed Profile** — acceleration, deceleration, max speed
- **Voltage Mode / Current Mode** — KVAL or TVAL values, BEMF parameters
- **Servo Mode** — PID gains

Per-axis parameters are displayed as columns, one column per motor axis. Changes take effect on the running firmware immediately when saved; they persist to the SD card when you use **Save to SD**.

## Saving configuration

### Save to SD card

Click **Save to SD** to write the current configuration to the microSD card. The firmware saves the file using the name shown in the **Config filename** field.

> **Note:** A microSD card must be inserted in the device for this operation.

You can change the filename before saving. The firmware will use this filename for subsequent saves during the same session. See [Configuration with microSD Card](setup-with-a-microsd-card_en.md) for file discovery priority rules.

This is equivalent to sending the [`/saveConfig`](../osc-command-references/system-settings_en.md#saveconfig) OSC command.

### Export JSON

Click **Export** to download the current configuration as a `.json` file to your computer. This is useful for backing up configurations or pre-staging them offline.

## Offline mode

The tool can be used without a serial connection to prepare configuration files in advance:

1. Open the tool in Chrome or Edge without connecting a device.
2. Click **Load JSON** to open an existing configuration file.
3. Edit the values as needed.
4. Click **Export** to save the modified file to your computer.

You can then copy the file to a microSD card and insert it into the device, or connect the device later and push the configuration over USB.

## Status monitoring

While connected, the tool displays real-time motor status including:

- Motor state (stopped, running, accelerating, decelerating)
- Current position
- Alarm flags (stall, overcurrent, thermal, UVLO)
- HOME and LIMIT switch states

Status is polled automatically while the tool is open.

## Troubleshooting

**"Connect" button is missing or grayed out**  
Your browser does not support the Web Serial API. Use Google Chrome or Microsoft Edge. Firefox and Safari are not supported.

**Device not appearing in the serial port list**  
- Check that the USB cable is data-capable (not charge-only).
- Try a different USB port.
- On Windows, verify the device appears in Device Manager.
- On macOS/Linux, the device appears as `/dev/tty.usbmodem*` or `/dev/ttyACM*`.

**Configuration loads but shows unexpected values**  
The tool reads the current running configuration, which may differ from the SD card contents if the device was reconfigured by OSC messages after boot. Use **Save to SD** to persist the current state.

**Save to SD fails**  
- Verify the microSD card is inserted.
- Ensure the card is formatted FAT16 or FAT32.
- Check that the card is not write-protected.

## Previous configuration tools

For devices running firmware earlier than v2.1.0, use the original HTML-based tools:

| Model | URL |
| --- | --- |
| STEP400 | <http://ponoor.com/tools/step400-config/> |
| STEP800 | <http://ponoor.com/tools/step800-config/> |

These tools export a `config.txt` file that you copy to the microSD card manually. See [Configuration with microSD Card](setup-with-a-microsd-card_en.md) for details.
