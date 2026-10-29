---
title: Troubleshooting
---

# Troubleshooting

Symptoms, their causes, and what to do. Each item links to the page that explains the matter. If your symptom is not here, connect a USB cable and look at the [status of the board](usb-serial-diagnosis.md#status).

## Communication {#communication}

### Replies and position reports do not arrive {#no-reply}

The commands may work, but nothing comes back. Check these points:

- **`/setDestIp` was not sent.** The board does not send anything to the PC before it gets [`/setDestIp`](../reference/system-settings.md#setdestip) (unless the setting `canSendMsgBeforeDestIp` is on). See [The destination and `/setDestIp`](../guides/communication-and-messages.md#setdestip).
- **`/destIp` did not come back.** The board resolves the MAC address of the destination before it replies, and can fail. Send `/setDestIp` again. See [Resolving the MAC address](../guides/communication-and-messages.md#arp).
- **The IP address, the subnet or the port is wrong.** The board and the PC must be in the same network. The ID of the DIP switch is added to the IP address and to the sending port, so the PC must receive on the port with the ID added. If the result is out of range, the board does not add the ID and prints a warning on USB serial. See [Network and the DIP switch](../connections/network-and-dip-switch.md#adding-id).
- **A firewall of the PC blocks the messages.**
- Over USB, send `s` and check `Ethernet link status`, `isDestIpSet` and `Destination Ip` ([Ethernet](usb-serial-diagnosis.md#status-ethernet)).
- **The board has just restarted** (observed). A `/setDestIp` sent about 0.1 s after the restart can be ignored: wait a little and send it again. The first OSC command after the restart may get no reply while the board resolves the MAC address (see [Resolving the MAC address](../guides/communication-and-messages.md#arp)). Send it again.
- **The board is saving the configuration.** The OSC messages that arrive while the board saves (about 0.1 s to 0.7 s) are lost. See [While the board saves](../connections/how-settings-work.md#saving).
- **The configuration was saved.** See the next item.

### Replies stopped after the PC was replaced (firmware up to v2.1.0) {#pc-replaced}

With firmware up to v2.1.0, when another PC (or another network adapter) with the same IP address replaces the PC, the board keeps sending to the MAC address of the old one. The commands work, but no reply and no report arrives, and `/setDestIp` does not repair it. Restart the board, or send `/setDestIp` from another IP address first and then send again from the original IP address.

With v2.2.0, send `/setDestIp` from the new PC. Wait at least 1.5 s after the last packet of the old one. See [When to send `/setDestIp`](../guides/communication-and-messages.md#when).

### Replies stopped after saving the configuration, or come from the start {#after-save}

In v2.2.0, the setting `canSendMsgBeforeDestIp` has the same value as "`/setDestIp` has been received":

- After you save the configuration (`/saveConfig`, or **Save to SD** of the browser configuration tool) when `/setDestIp` has been received, the saved file has `true`. From the next start, the board sends messages before it receives `/setDestIp`.
- When the tool writes `false`, the running value also becomes `false`, and the board sends no reply until you send `/setDestIp` again.

Send `/setDestIp` again after you save, and check the value in the saved file. See [`network.canSendMsgBeforeDestIp`](../connections/configuration-items.md#network-cansendmsgbeforedestip) and [Running values and saved values](../connections/how-settings-work.md#saved-values).

## Settings and the card {#settings}

### The configuration file is not read {#config-not-read}

The board uses the default values when it does not accept a file. Check these points:

- **The card is exFAT.** Only FAT16 and FAT32 can be used. See [Preparing the card](../connections/microsd-card.md#card).
- **The card was inserted after the start.** The board reads the card only when it starts. Restart the board.
- **The name or the place of the file.** The board reads only `config.txt` and the first `*.json` (in the alphabetical order) in the root folder. Files that start with `.` and subfolders are ignored, and the path can have at most 63 characters. See [The file that the board reads](../connections/microsd-card.md#files).
- **The file was saved with a name that the board does not read**, with `F<path>`. See [The name set by `F<path>`](../connections/microsd-card.md#f-path).
- **The file is not valid.** A `.json` file without `information.configVersion`, or a file that is not JSON, is not applied.

To see what the board read, send [`/getConfigName`](../reference/system-settings.md#getconfigname), or see [microSD](usb-serial-diagnosis.md#status-microsd) of the USB serial status.

### Saving the configuration fails {#save-fails}

The messages are `No SD card` and `SD open failed`. See [Errors](../connections/microsd-card.md#errors) for the causes.

### The browser configuration tool cannot connect {#tool-no-connect}

Use Chrome or Edge, a USB cable for data, and check the list of the serial ports. See [Troubleshooting](../connections/browser-config-tool.md#troubleshooting) of the tool.

## Motion {#motion}

### The motor does not move {#motor-not-moving}

- **Only USB is connected.** USB does not power the driver ICs. Turn on the motor power. See [Connection](usb-serial-diagnosis.md#connection).
- **The command is answered with `/error/command`.** The error tells the reason: for example `BrakeEngaged` (the brake is not released), `MotorNotHiZ`, `MotorNotStopped` or `InServoMode`. See [`/error/command`](../reference/automatically-sent-messages.md#error-command) and [Errors](../guides/communication-and-messages.md#errors). The conditions for the start of a motion are in [the motion start condition](../reference/index.md#motion-start-condition), and for the brake in [Electromagnetic brake](../guides/electromagnetic-brake.md#commands). If you do not get the error, check that error reports are not switched off ([`/reportError`](../reference/system-settings.md#reporterror)).
- **A switch prohibits the motion.** See [Switches that prohibit a motion](../guides/alarms-and-protection.md#switches).
- **The driver went HiZ by itself** (overcurrent, overtemperature, undervoltage). See [When the driver goes HiZ by itself](../guides/alarms-and-protection.md#hiz-by-itself).

### Homing ends at once with `ReleaseSwTimeout` {#release-sw-timeout}

With firmware up to v2.1.0, the homing sometimes ended at once with the status `ReleaseSwTimeout` (`/homingStatus` 4), at almost every start or almost never. This was fixed in v2.2.0. Update the firmware: [Firmware update](firmware-update.md).

## The board and the firmware {#board}

### The STEP400 restarts when USB is unplugged {#usb-unplug}

With an Ethernet cable connected, the STEP400 (R1 board) can restart when the USB cable is pulled out. This is a hardware problem. The brakes are engaged first. Stop the motors before you pull out the cable. See [STEP400](../hardware/step400.md#usb-unplug).

### The firmware cannot be written {#cannot-write}

Double-click the RESET switch to put the board in the bootloader mode, select the serial port again, and try again. See [Notes for uploading the firmware](compile-the-arduino-sketch.md#uploading).

### The board restarts for no reason {#unexpected-restart}

Look at the reset cause, the second argument of [`/booted`](../reference/automatically-sent-messages.md#booted) (or `resetCause` of the `T` command of USB serial). A restart by the watchdog or by a CPU fault is explained in [Restart, watchdog and CPU fault](../guides/electromagnetic-brake.md#restart). The STEP400 can also reset when the voltage of the power supply drops at the inrush current of a motor (see [Power supply voltage](../connections/power-supply-and-motor.md#voltage)).
