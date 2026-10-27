---
title: Firmware update
---

# Firmware update

The firmware is updated to fix bugs and to add features. Check the version of the firmware on the board first. If it is older than the [latest release on GitHub](https://github.com/ponoor/step-series-universal-firmware/releases), update it.

The changes of each version are in the [Changelog](changelog.md). Before you update a system that is running, read the notes for the new version in the [Migration guide](migration-guide.md): some versions change the behavior of OSC commands or add error replies.

## Checking the version of the firmware on the board {#checking}

There are two ways:

- Send the OSC (Open Sound Control) command `/getVersion`.
- Connect a USB cable to the board and send `s` from a serial monitor.

### With an OSC command {#osc}

Send [`/getVersion`](../reference/system-settings.md#getversion) to the board. The reply has the name, the version and the build date of the firmware. For example:

```
/version "STEP800_R1_UNIVERSAL 2.2.0 Oct 20 2026 10:00:00"
```

### Over USB {#usb}

Connect the board to the computer with a USB-C cable, open a serial monitor, and send `s`. The firmware is shown in the first part of the status. For example:

```
-------------- Firmware --------------
Firmware name : STEP800_R1_UNIVERSAL
Firmware version : 2.2.0
Compile date : Oct 20 2026, 10:00:00
```

See [Diagnosis via USB serial port](usb-serial-diagnosis.md#status) for the rest.

## Checking the latest version {#latest}

The latest version is on the [Releases](https://github.com/ponoor/step-series-universal-firmware/releases) page of the repository of the firmware.

Until March 2022, the firmware of the STEP400 and the STEP800 was managed in separate repositories. They moved to one "STEP-series Universal Firmware", and the version numbers were reset. To check whether the firmware on the board is the latest:

1. Check whether the name of the firmware that you got from the board has `UNIVERSAL` in it.
2. If not, the firmware is old and needs an update.
3. If it has, compare its version with the version on the [Releases](https://github.com/ponoor/step-series-universal-firmware/releases) page.

The earlier firmware is still in the following places, but it is not maintained.

| Board | Old repository |
| --- | --- |
| STEP400 | <https://github.com/ponoor/STEP400/releases> |
| STEP800 | <https://github.com/ponoor/STEP800/releases> |

## Updating {#updating}

If the firmware on the board is old, update it by building the latest firmware and uploading it through the USB bootloader. The releases have no ready-made binary files. See [Compiling the firmware](compile-the-arduino-sketch.md).

Before you update, save the settings that you changed with OSC commands: the configuration file on the card stays, but a value that you changed and did not save is lost. See [How the settings work](../connections/how-settings-work.md#saved-values).
