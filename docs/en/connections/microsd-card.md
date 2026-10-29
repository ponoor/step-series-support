---
title: Configuration with a microSD card
---

# Configuration with a microSD card

If you insert a microSD card with a configuration file and start the board, the board is set up with the settings in the file. This page explains how to prepare the card, which file the board reads, and how the board saves the settings to the card. For the big picture of the settings, see [How the settings work](how-settings-work.md).

If the board starts without a card or without a valid file, it uses the default values of the firmware.

## Preparing the card {#card}

Use a microSD card that is formatted as **FAT16 or FAT32**. **exFAT cannot be used.**

- SDXC cards of 64 GB or more are exFAT by default. Format them as FAT32 again (in the Disk Utility of macOS, choose "MS-DOS (FAT)").
- The board treats an exFAT card as if there were no card, and does not touch anything on it. Reading fails, and saving fails with `No SD card`.
- The root folder of a FAT16 card holds at most 512 entries, and a long file name uses several of them. Use FAT32 if you put many files on the card.

> **From v2.2.0:** the Arduino IDE build also treats an exFAT card as no card. In the earlier Arduino IDE builds, saving the configuration to an exFAT card deleted the file on the card.

## The file that the board reads {#files}

### Order {#order}

The board looks for the file in this order:

1. `config.txt` in the root folder of the card.
2. If there is no `config.txt`, or it cannot be parsed: the first `*.json` file in the alphabetical order in the root folder. The extension is not case-sensitive.
3. If there is no valid file: the default values.

If the first `.json` file is not valid (it is not JSON, or it has no `information.configVersion`), the board does not go on to the next `.json` file. It uses the default values. **From v2.2.0, the values of a file that is not accepted are not applied at all.**

This means that old `config.txt` files work as before, and that a new card can have a file with any name, for example `STEP800_ST-42BYH1684_24V.json`.

### File names {#names}

- Long file names can be used. The path, including the leading `/`, can have **at most 63 characters**.
- Files and folders whose name starts with `.` are ignored. macOS writes `._*` files and `.Trashes` to a FAT card when it copies files, and they would hide the real files.
- The board does not look into subfolders. Put the file in the root folder.

## When the card is read {#when-read}

**The board reads the card only when it starts.** If you insert a card after the start, restart the board. If you remove the card after the start, the settings stay as they were at the start, and saving fails with `SD open failed`.

To see what the board read, use [`/getConfigName`](../reference/system-settings.md#getconfigname) or the USB serial output; see [How the settings work](how-settings-work.md#at-start).

## Saving to the card {#saving}

### Where it is saved {#save-target}

[`/saveConfig`](../reference/system-settings.md#saveconfig), the **Save to SD** button of the [browser configuration tool](browser-config-tool.md) and the USB serial command `{` save the settings to the file that the board read at the start, or to `/config.txt` when it read no file. The file name can be changed until the next restart; see below.

The board writes the settings to a hidden temporary file `.<name>.tmp` in the same folder, and replaces the saved file with it only after it has been written and closed. If the writing fails, the saved file stays as it was.

**Known issue in v2.2.0:** if the board started without a configuration file (no card, or no valid file) and you save, the board has no version and product to write. The file gets `information.configVersion` `[-1, 0]` and `information.targetProduct` `"---"`. The values are saved, and the board reads the file at the next start, but the diagnosis shows the configuration version -1.0 and "Config and product match" as false. To get a file with the right version and product, make it with the [browser configuration tool](browser-config-tool.md) (**Download JSON**). The saving also writes `canSendMsgBeforeDestIp` wrongly in some cases; see [`network.canSendMsgBeforeDestIp`](configuration-items.md#network-cansendmsgbeforedestip).

The saving stops the processing of the board for a short time. Stop the motors before you save; see [While the board saves](how-settings-work.md#saving).

### Errors {#errors}

| Message | Meaning and causes |
| --- | --- |
| `No SD card` | The board has no card to write to: no card was inserted at the start, the card is exFAT, or the card could not be initialized |
| `SD open failed` | The card could not be written: the card was removed after the start, the card or the root folder is full, the folder of the file name does not exist, or a write error. The saved file stays as it was |

The OSC command `/saveConfig` replies `/error/saveConfig` with the same texts. If the power is cut while the board replaces the file, only the temporary file may remain, and the board does not recover it at the next start.

### The name set by `F<path>` {#f-path}

With the USB serial command `F<path>` you can change the file that the board saves to, until the next restart. The board accepts any name that starts with `/`, ends with `.json` or `.txt`, and has at most 63 characters.

The board does not refuse a longer name: **a name of 64 bytes or more is cut to 63 bytes without an error** (v2.2.0), and the file is saved under the cut name.

**At the start the board reads only `config.txt` and the `*.json` files in the root folder.** A configuration that you save as `/foo.txt` or in a subfolder is not read at the next start. The browser configuration tool warns you in this case.

## Making a configuration file {#making}

!!! warning "The firmware does not check the range of some values of a file"
    The range check is made when you send an OSC command, and by the [browser configuration tool](browser-config-tool.md). **When the board reads a configuration file, it does not check the range of some values.** The most important is **TVAL**: the OSC commands limit it to 64 (about 5 A), but in a file it is not limited. A value up to 127 is written to the driver as it is, and a large current (about 10 A for 127 on the STEP400) can flow in the motor and the driver. The overcurrent threshold and the stall threshold are not checked either, so a value out of the range gives a different threshold from what you intend. Keep every value in the range of [Configuration items](configuration-items.md). The same applies to the settings sent with the USB serial command `{`.

- With the [browser configuration tool](browser-config-tool.md): read the settings from the board over USB, or start from a file, edit the values, and save to the card or download the file.
- From the examples: configuration files for some motors are in the [configGenerator folder](https://github.com/ponoor/step-series-support/tree/main/configGenerator) of the repository; see [Example parameter values for example steppers](example-parameters.md).
- With OSC commands: send the commands, and then [`/saveConfig`](../reference/system-settings.md#saveconfig) (firmware v2.1.0 or later). You do not need to remove the card.

The items of the file are in [Configuration items](configuration-items.md).

## Older firmware (before v2.1.0) {#legacy}

Firmware before v2.1.0 reads only a file named `config.txt` in the root folder; the old SD library accepted only short file names, so the JSON file has the extension `.txt`. For this firmware use the configuration tools of the products. Click the "Export" button at the bottom of the page to download `config.txt`, copy it to the root folder of the card, and start or reset the board. The settings are read only at the start.

| Model | URL | Source (GitHub) |
| --- | --- | --- |
| STEP400 | <http://ponoor.com/tools/step400-config/> | [/configTool](https://github.com/ponoor/STEP400/tree/master/configTool) |
| STEP800 | <http://ponoor.com/tools/step800-config/> | [/configTool](https://github.com/ponoor/STEP800/tree/master/configTool) |

## Configuration items {#items}

The items of the configuration file, with their initial values, ranges and the commands that change them, are in [Configuration items](configuration-items.md).

## Related commands {#related}

<!-- osc-related: /getConfigName, /saveConfig -->
<!-- generated:begin osc-related /getConfigName, /saveConfig -->
**Related commands**

| Command | Arguments | Description |
| --- | --- | --- |
| [`/getConfigName`](../reference/system-settings.md#getconfigname) | - | Returns `/configName`: the configuration name, whether the microSD card could be used, whether a configuration file was opened and parsed, and the path of the file. |
| [`/saveConfig`](../reference/system-settings.md#saveconfig) | - | Saves the current running configuration to the microSD card as a JSON file. |
<!-- generated:end osc-related /getConfigName, /saveConfig -->
