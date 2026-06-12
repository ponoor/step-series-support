---
title: Firmware Update
wp_id: 1624
slug: firmware-update
lang: en
link: "https://ponoor.com/en/docs/step-series/technical-information/firmware-update/"
date: "2021-04-03T22:16:40"
modified: "2022-08-05T21:37:27"
parent: 888
menu_order: 50
---

# Firmware Update

## Updating the firmware

The firmware may be updated for bugfixes and adding features.

Please check the current firmware version on the controller first, then if it is older than [the version published on GitHub](https://github.com/ponoor/step-series-universal-firmware/releases), please update the firmware.

> **Note:** The latest firmware version is v2.1.0. See the [Firmware Changelog](firmware-changelog_en.md) for details on what has changed.

## Checking firmware version burned on to the controller

Two methods exist to check the current version of the firmware:

- Using the OSC (Open Sound Control) command `/getVersion`
- Connecting a USB cable to the board and typing `s` in the Serial Monitor

### Method 1: OSC Command

This method only requires you to send the [`/getVersion`](https://ponoor.com/en/docs/step-series/osc-command-reference/system-settings/#getversion) command to the board. The resulting response will tell you the current version of the firmware.

For example:

```
/version "STEP800_R1_UNIVERSAL 1.0.1 Mar 24 2022 11:17:29"
```

### Method 2: Over USB

Connect the USB-C cable to the board and to your PC. Then open Serial Monitor in the IDE you're using. Send the command `s` and you should receive a response containing the version.

For example:

```
-------------- Firmware --------------
Firmware name : STEP800_R1_UNIVERSAL
Firmware version : 1.0.1
Compile date : Mar 24 2022, 11:17:29
```

## To check the latest firmware version

Check the latest firmware version from the "[Releases](https://github.com/ponoor/step-series-universal-firmware/releases)" of the Github repository of STEP-Series.

Previously, STEP400 and STEP800 firmware was managed in separate repositories, but as of March 2022, we have moved to a unified "STEP-series Universal Firmware". The version numbers have been reset accordingly, so please follow the procedure below to make sure you have the latest version.

1. Check if `UNIVERSAL` is in the name of the firmware obtained from the controller.
2. If no, the firmware in the controller is old and needs to be updated
3. If yes, compare with the version number of "[Releases](https://github.com/ponoor/step-series-universal-firmware/releases)".

## Updating firmware

If the firmware on the controller is old, please update it. The update can be done by compiling and uploading the latest firmware. Refer to [Compiling the Firmware](compile-the-arduino-sketch_en.md) for details.
