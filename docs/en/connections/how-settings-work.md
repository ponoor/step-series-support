---
title: How the settings work
---

# How the settings work

Where the settings of the board are, when a change takes effect, and where it is saved. Read this page first; the details of the card and the tool are in [Configuration with a microSD card](microsd-card.md) and [Browser configuration tool](browser-config-tool.md).

## Three ways to change the settings {#overview}

- **The configuration file on the microSD card.** The board reads it when it starts. You can make the file on a PC or with the browser configuration tool.
- **The browser configuration tool.** It reads the settings from the board over USB, and applies the settings that you edit and saves them to the card.
- **OSC commands.** They change the values of the running board at once. [`/saveConfig`](../reference/system-settings.md#saveconfig) saves the running values to the card.

All the items that the configuration file has are listed in [Configuration items](configuration-items.md), with the commands that change them.

## At start {#at-start}

The board reads the card only when it starts. It reads the file in this order, and uses the default values of the firmware when there is no file or when the file is not valid:

1. `config.txt` in the root folder of the card.
2. The first `*.json` file in the alphabetical order in the root folder.
3. The default values.

The details are in [The file that the board reads](microsd-card.md#files). From v2.2.0, a file that is not accepted is not applied at all: the board uses the default values, as when there is no card.

To know what the board read, send [`/getConfigName`](../reference/system-settings.md#getconfigname) (the reply `/configName` has the name of the configuration, whether the card and the file were read, and the file name), or look at the USB serial output ([Diagnosis via USB serial port](../maintenance/usb-serial-diagnosis.md)).

## Running values and saved values {#saved-values}

The board keeps the settings in its memory while it runs. A value that you change with an OSC command is changed in the memory, and **it is lost when the power is turned off**, unless you save it.

- [`/saveConfig`](../reference/system-settings.md#saveconfig) writes the running settings to the card.
- The file that it writes to is the file that the board read at start, or `/config.txt` when it read no file. With the USB serial command `F<path>` you can change the file until the next restart; see [The name set by `F<path>`](microsd-card.md#f-path).
- The browser configuration tool does the same when you click **Save to SD**, after it has applied the values that you edited.

The values that the board reads from the card at the next start are the values in the saved file. What you changed after the save is not in it.

## When a change takes effect {#when}

**OSC commands** take effect at once. Some commands can be used only in some states, for example only when the motor is HiZ. The condition of each command is in the [reference](../reference/index.md).

**The browser configuration tool** applies the values to the memory of the running firmware and saves them to the card. It does not make every value effective at once:

| Settings | When they take effect |
| --- | --- |
| The name of the configuration | At once |
| The IP address, subnet mask, gateway, DNS, ports, MAC address and the switches that add the ID | At the next restart. The running values do not change |
| `destIp`, `canSendMsgBeforeDestIp` and `reportError`. (The usual way to set the destination is [`/setDestIp`](../reference/system-settings.md#setdestip).) | At once |
| The report switches and the report intervals; homing (direction, speed, timeouts, prohibition of the motion); the settings of the LIMIT switch; the brake settings (see below); the servo mode (kP, kI, kD) | At once |
| `bootedMsgEnable`; homing at start | At the next start |
| The settings that the board writes to the driver: the speed profile, the voltage mode and the current mode (KVAL, TVAL, BEMF and others), the microstep mode, the slew rate, the HOME switch mode, the overcurrent and stall thresholds | At the next restart. The board writes them to the driver registers when it starts |

For the brake, the setting `electromagnetBrakeEnable` is changed only when the driver is HiZ and the brake is engaged; otherwise the board prints a warning on the USB serial port and keeps the old value (the saved value is the one that did not change). Check by reading the settings again after you save.

So after you save with the tool, **restart the board** to make all the values effective. The tool offers to restart it after the save.

## What is saved {#what-is-saved}

The values of the items of [Configuration items](configuration-items.md) are saved. From v2.2.0 this includes the values set with the Raw commands (`/setSpeedProfileRaw`, `/setMaxSpeedRaw`, `/setMinSpeedRaw`, `/setFullstepSpeedRaw`, `/setAccRaw`, `/setDecRaw`), which changed only the register before.

What is not a configuration item is not saved: for example the position, the target of the servo mode, and whether the servo mode is on.

## While the board saves {#saving}

While the board saves the configuration, it does not process anything: about 0.1 s for `/saveConfig` (measured), at most about 0.3 s for the USB serial command `{` including the transfer (measured), and at most about 0.7 s for the first save after the card was inserted (measured). The watchdog is stopped during this time. **Stop the motors before you save.**

## Which way to use {#which-method}

- Adjusting on site: change the values with OSC commands while the system runs, and send `/saveConfig` when it is good.
- Preparing on a PC: make the configuration file on the PC (with the [browser configuration tool](browser-config-tool.md) or from the [examples](example-parameters.md)) and copy it to the card.
- Reading the settings of a board, editing and saving them: use the browser configuration tool over USB.

## Related commands and settings {#related}

<!-- osc-related: /getConfigName, /setConfigName, /saveConfig, /resetDevice -->
<!-- generated:begin osc-related /getConfigName, /setConfigName, /saveConfig, /resetDevice -->
**Related commands**

| Command | Arguments | Description |
| --- | --- | --- |
| [`/getConfigName`](../reference/system-settings.md#getconfigname) | - | Returns `/configName`: the configuration name, whether the microSD card could be used, whether a configuration file was opened and parsed, and the path of the file. |
| [`/setConfigName`](../reference/system-settings.md#setconfigname) | (string)configName | Sets the configuration name stored in the device. |
| [`/saveConfig`](../reference/system-settings.md#saveconfig) | - | Saves the current running configuration to the microSD card as a JSON file. |
| [`/resetDevice`](../reference/system-settings.md#resetdevice) | - | Resets the entire device. |
<!-- generated:end osc-related /getConfigName, /setConfigName, /saveConfig, /resetDevice -->

<!-- osc-settings: information -->
<!-- generated:begin osc-settings information -->
**Related configuration items**

| Key | Name | Commands |
| --- | --- | --- |
| [`information.configName`](configuration-items.md#information-configname) | Configuration name | `/setConfigName` |
| [`information.configVersion`](configuration-items.md#information-configversion) | Configuration version |  |
| [`information.targetProduct`](configuration-items.md#information-targetproduct) | Target product |  |
<!-- generated:end osc-settings information -->
