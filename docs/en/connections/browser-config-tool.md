---
title: Browser configuration tool
---

# Browser configuration tool

The browser configuration tool reads the settings of the board over USB, lets you edit them, and saves them to the microSD card of the board, without removing the card. It runs in a web browser and needs no installation.

The tool is at: <https://ponoor.com/tools/step-config/>

It works with firmware v2.1.0 or later. The tool was checked with firmware v2.2.0. The version of the tool is separate from the version of the firmware: the tool shows `v2.1.0 · checked with firmware v2.2.0` beside its name.

For what the settings mean and when they take effect, see [How the settings work](how-settings-work.md).

## What you need {#requirements}

- Google Chrome or Microsoft Edge (the Web Serial API is required). Firefox 151 or later has the Web Serial API and should work, but this has not been checked with a board. Safari has no Web Serial API: the tool shows a banner, and only **Load JSON** and **Download JSON** work.
- A USB cable (a cable for data, not only for charging) between the computer and the board.
- Firmware v2.1.0 or later on the board.
- To save to the card, a microSD card in the board; see [Configuration with a microSD card](microsd-card.md).

## Connecting to the board {#connecting}

1. Turn on the power of the board and connect the USB cable to the computer. (USB alone powers only the control circuits.)
2. Open the tool in Chrome or Edge.
3. Click **Connect**.
4. Choose the serial port of the board in the dialog of the browser.
5. The tool reads the settings of the board and shows them. You can read them again with **Read from Board**.

The board does not need a card for the connection. It needs one to save.

### When the USB cable is pulled out {#disconnected}

The tool shows the banner "Serial connection lost". Plug in the USB cable again, and then click **Reconnect**. The tool waits up to 3 s for the board to come back ("Waiting for the board to come back…"), reads the settings again, and shows them. If it does not connect, click **Connect**. If the tool connects to a different board from before, it tells you so.

If you pull the cable out while the tool is saving, the tool cannot know whether the board saved the settings. Connect again and check the settings with **Read from Board**.

**Disconnect** does not show this banner.

## Reading and editing the settings {#editing}

The settings are in panels that you can open and close: **Board Info**, **Network**, **Alarm & Report**, **Driver Settings**, **Speed Profile**, **Voltage Mode**, **Current Mode (PowerSTEP01)** and **Servo Mode**. The settings of each motor are shown in columns, one column for each motor. **Copy Motor 1 → All** copies the values of motor 1 to the other motors in the panel.

- The tool shows an item only when the settings that it reads or loads have it: the panel **Current Mode** for the STEP400 (and the STEP100), the items of the LIMIT switch for the STEP400, and the brake items for the boards that have the brake output (the STEP400 and the STEP800).
- In **Board Info**, only the name of the configuration (at most 32 characters) can be edited. The product and the version of the configuration are read-only. The firmware version is the version of the board. When the settings come from a file, the number of motors (Axes) can be chosen too; when they come from a board, it is fixed.
- The thresholds of the overcurrent and the stall, and TVAL, are shown with their current. The steps differ between the STEP400 and the STEP800 (see [Alarms and protection](../guides/alarms-and-protection.md#thresholds)). TVAL can be chosen up to 64 (about 5 A).
- The slew rate has 6 steps for the STEP400 and 3 steps for the STEP800.
- A MAC address is shown in decimal. **Show Hex** switches the display to hexadecimal.
- **Read from Board** shows the settings in the memory of the board, which are the values that **Save to SD** writes (see [Running values and saved values](how-settings-work.md#saved-values)): the saved values, and the changes made by OSC commands since the start. The IP address, the ports and the MAC address are the configured values, not the addresses that the board uses now. The running state (the position, the speed and so on) is not in them: use **Start Status** or OSC messages.
- The tool does not accept an empty or non-numeric value, or a value outside the range, and refuses to save or to download it. It also refuses `{` or `}` in the name of the configuration and a configuration that is too large to send (more than 4095 bytes); in the last case, save it with **Download JSON** and copy the file to the card.

!!! note "A configuration file written by hand"
    The tool never sends a value outside the range. A file that you write by hand is different: the firmware does not check the range of some values in a file. See [the warning](microsd-card.md#making) before you write a file by hand.

Changing a value in the tool does not change the running board. The values are applied when you save them. After they are saved, the IP address, the ports, the MAC address and the settings that the board writes to the driver need a restart to take effect; see [When a change takes effect](how-settings-work.md#when).

## Saving to the card {#saving}

### Save to SD {#save-to-sd}

**Save to SD** sends the values to the board. The board applies them to the memory and writes them to the card (the same way as [`/saveConfig`](../reference/system-settings.md#saveconfig)). **The board stops processing for about 0.1 s to 0.7 s while it saves, so stop the motors first.** The tool shows this note beside the button. The OSC messages that arrive in this time are lost.

### A known issue with `canSendMsgBeforeDestIp` {#known-issue}

In firmware v2.2.0, saving with the tool can change the setting [`network.canSendMsgBeforeDestIp`](configuration-items.md#network-cansendmsgbeforedestip). If you use OSC and have sent `/setDestIp`, the saved file gets `true`. And when the tool writes `false`, the board sends no reply until it receives `/setDestIp` again. After you save, send `/setDestIp` again. See [Configuration items](configuration-items.md#network-cansendmsgbeforedestip) for the details.

If the saving fails, the tool shows the reply of the board with the likely cause. The causes of `No SD card` and `SD open failed` are in [Errors](microsd-card.md#errors).

### The file name {#file-name}

The text field on the left of **Save to SD** is the name of the file that the board saves to. After **Read from Board**, it has the name of the file that the board reports (the file that it read at the start, or `/config.txt`). **Load JSON** sets it to the name of the loaded file.

- The name must start with `/`, end with `.json` or `.txt`, and have at most 63 bytes. The field turns red when it does not follow these rules, and the tool refuses to save.
- At the start the board reads only `/config.txt` and the first `*.json` of the root folder. If the name is in a subfolder, starts with `.`, or is a `.txt` other than `/config.txt`, the field turns yellow, and the tool asks "Save anyway?" before it saves. The file is saved, but the board does not read it at the next start. See [The name set by `F<path>`](microsd-card.md#f-path).

The name that you set is used until the board restarts. After a restart the board saves to the file that it read at the start.

### After saving {#after-saving}

After a successful save the tool asks whether to restart the board now. If you answer yes, the board restarts, the tool closes the connection, and you click **Connect** again. The board comes back on USB about 1.5 s after the restart (measured). You can also restart the board later with **Reboot**; unsaved changes are lost.

If a motor is turning, the board stops it and engages the brake before it restarts; see [Restart, watchdog and CPU fault](../guides/electromagnetic-brake.md#restart). Still, stop the motors first.

### Download JSON {#download}

**Download JSON** saves the configuration in the tool as a `.json` file on the computer. The file name is the name in the file name field, without the leading `/`. Use it to keep a backup, or to prepare a file to copy to the card.

## Working without a board {#offline}

You can prepare a configuration file without a board:

1. Open the tool in Chrome or Edge without connecting.
2. Click **Load JSON** and choose a configuration file (`config.txt` or a `.json`).
3. Edit the values.
4. Click **Download JSON**.

Copy the file to the card, or connect the board later, click **Load JSON** to load the file, and click **Save to SD**. For a file, the tool takes the product from `information.targetProduct` (or from the number of motors). The tool does not check that the file is for the same product as the connected board; check this yourself.

## Status monitoring {#status}

Click **Start Status** to show the state of the board and the motors in **Real-time Status**. The tool asks the board once every second after you click it (it does not start by itself). It shows the product, the IP address, the link of the Ethernet, the card and the configuration, and for each motor the position, the speed, whether it is busy or HiZ, the direction, the motor status, the thermal status, UVLO, the HOME switch, the homing status and the servo mode.

- **OCD** and **Stall** are shown as "not reported": in firmware v2.2.0, the status of the USB serial output always sends false for them, so the tool does not show it as a state. Use the OSC messages `/overCurrent` and `/stall` ([Alarms and protection](../guides/alarms-and-protection.md#timing)).
- The state of the LIMIT switch is not shown.

## Firmware versions {#versions}

After the tool reads a board, it shows a notice when the firmware is older than v2.1.0, or newer than the version that the tool was checked with:

- `This tool requires firmware v2.1.0 or later (this board: vX.Y.Z).`
- `This tool was checked with firmware v2.2.0. Some settings of firmware vX.Y.Z may not be shown.`

The tool compares only the major and minor numbers, so a patch version such as v2.2.1 gives no notice. The notice is shown in a banner for about 9 s. The tool is not stopped by these notices.

## Troubleshooting {#troubleshooting}

### The Connect button is disabled {#no-connect-button}

Your browser does not support the Web Serial API (Safari, for example). Use Google Chrome or Microsoft Edge.

### The board is not in the list of serial ports {#port-not-listed}

- Check that the USB cable can carry data, not only power.
- Try another USB port.
- On Windows, check that the board appears in the Device Manager.
- On macOS and Linux, the board is a device such as `/dev/tty.usbmodem*` or `/dev/ttyACM*`.

### The tool shows unexpected values {#unexpected-values}

The tool reads the settings in the memory of the board. They can differ from the file on the card if the board was changed by OSC commands after the start. Use **Save to SD** to keep these values.

### The settings do not change after saving {#not-applied}

The IP address, the ports, the MAC address and the settings that the board writes to the driver need a restart. Restart the board; see [When a change takes effect](how-settings-work.md#when).

### Saving fails {#save-fails}

- Check that a microSD card is in the board, and that it was in it when the board started.
- Check that the card is FAT16 or FAT32 (exFAT cannot be used) and not write-protected.
- See the messages `No SD card` and `SD open failed` in [Errors](microsd-card.md#errors).

### Asking about a problem {#console}

The console of the browser (the developer tools) shows what the tool does. A line that starts with `[serial]` is the log of the tool itself, with the time. A line that starts with `[board]` is a text that the board sent. When you ask about a problem, add the `[serial]` lines.

## Older firmware {#legacy}

For firmware before v2.1.0, use the configuration tools of the products; see [Older firmware](microsd-card.md#legacy).
