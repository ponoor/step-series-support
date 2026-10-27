---
title: System settings
---

# System settings

For how the board communicates and how the messages work, see [Communication and messages](../guides/communication-and-messages.md).

<!-- osc: /setDestIp -->
<!-- generated:begin osc /setDestIp -->
### `/setDestIp` {#setdestip}

#### Argument

None

#### Executable timing

Always

#### Description

Sets the destination IP address (`destIp`) to where the device should send messages to, when it replies to a query or report internal state changes, etc.  
The board sets the `destIp` to the sender of this message.

Until the board receives `/setDestIp`, it sends nothing to the destination (except the broadcast [`/booted`](automatically-sent-messages.md#booted)), so send this command first. When [`network.canSendMsgBeforeDestIp`](../connections/configuration-items.md#network-cansendmsgbeforedestip) is enabled in the configuration, it sends to [`network.destIp`](../connections/configuration-items.md#network-destip) from the start.

To resolve the MAC address, the board sends one byte of UDP to port 9 (discard) of the destination; a Mac answers with ICMP port unreachable, which has no effect on the board. To check that the board is alive, use a command with a reply such as [`/getVersion`](system-settings.md#getversion), not `/setDestIp`.

#### Changes

- **v2.2.0**: When this `/setDestIp` starts the resolution of the MAC address of the destination, the reply `/destIp` is sent once it has been resolved, so it can come later than before (a few ms on a wired network, up to a few seconds on Wi-Fi). If it does not come, send `/setDestIp` again. A `/setDestIp` that starts no resolution (for example one sent every second as a heartbeat) is answered at once.
- **v2.2.0**: Messages to the destination (replies, reports, errors) are dropped while the MAC address is being resolved (up to a few seconds). The broadcast `/booted` is still sent.
- **v2.2.0**: A `/setDestIp` from a different device with the same IP address (another PC or network adapter), sent 1.5 s or more after the last packet from the old one, now makes the board send to the new device. Before, the board kept sending to the old MAC address until it was restarted.
- **v2.2.0**: A send to a destination that has never answered ARP (for example a wrong destination address) blocks the processing for about 41 ms (1.6 s or more before). It no longer happens for every message: the sends to that destination are paused for 1 s: the messages in that time are dropped, not sent later. A packet received from that destination resumes the sends at once. The broadcast `/booted` is not affected.

#### Response

```
/destIp (int)destIp[0] (int)destIp[1] (int)destIp[2] (int)destIp[3] (int)isNewDestIp
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| destIp[0] | int | 0-255 | Each byte of destIp |
| destIp[1] | int | 0-255 | Each byte of destIp |
| destIp[2] | int | 0-255 | Each byte of destIp |
| destIp[3] | int | 0-255 | Each byte of destIp |
| isNewDestIp | int | 0-1 | Indicates if destIp has been changed. 1 if it has been changed, or 0 if the same address has already been set. |

##### Changes

- **v2.2.0**: When the `/setDestIp` starts the resolution of the MAC address (the first one, one from another address, or one 1.5 s or more after the last packet from the destination), the message is sent once it has been resolved, so it can come up to about 2 s later; otherwise it is sent at once. If it does not come, send `/setDestIp` again.
<!-- generated:end osc /setDestIp -->

<!-- osc: /getVersion -->
<!-- generated:begin osc /getVersion -->
### `/getVersion` {#getversion}

#### Argument

None

#### Executable timing

Always

#### Description

Returns the firmware version burnt on the chip.

#### Response

```
/version (string)version
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| version | string |  |  |
<!-- generated:end osc /getVersion -->

<!-- osc: /getConfigName -->
<!-- generated:begin osc /getConfigName -->
### `/getConfigName` {#getconfigname}

#### Argument

None

#### Executable timing

Always

#### Description

Returns `/configName`: the configuration name, whether the microSD card could be used, whether a configuration file was opened and parsed, and the path of the file.

#### Response

```
/configName (string)configName (int)sdInitializeSucceeded (int)configFileOpenSucceeded (int)configFileParseSucceeded (string)configFilename
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| configName | string |  | The configuration name (`information.configName` of the configuration file that was read). It is `Default` when no file was read or the file has no name. [`/setConfigName`](system-settings.md#setconfigname) changes it. |
| sdInitializeSucceeded | int | 0-1 | 1 if the microSD card could be used at start-up. 0 if there was no card, the card is not FAT16 or FAT32 (for example exFAT). The card is checked only at start-up. |
| configFileOpenSucceeded | int | 0-1 | 1 if `config.txt` could be opened or a valid `.json` file was read. 0 if neither (including a first `.json` file that is invalid). See the table below. |
| configFileParseSucceeded | int | 0-1 | 1 if a configuration file was read and its values were applied (a `config.txt` that could be parsed as JSON, or a valid `.json` file, which has `information.configVersion`). 0 if the defaults are used. |
| configFilename | string |  | The path of the configuration file that was read, with a leading `/` (e.g., `/config.txt` or `/STEP400_venue-A.json`). When no file was read, it is `/config.txt`, where [`/saveConfig`](system-settings.md#saveconfig) saves. `F<path>` over USB serial changes it. The path is at most 63 characters. This is the on-disk path, distinct from `configName` which is the user-editable label. (Added in v2.1.0.) |

##### Combinations of configFileOpenSucceeded and configFileParseSucceeded

| configFileOpenSucceeded | configFileParseSucceeded | Meaning |
| --- | --- | --- |
| 1 | 1 | A configuration file was read and its values were applied (`config.txt`, or else the first valid `.json` file). |
| 1 | 0 | `config.txt` could be opened but not parsed, and there was no valid `.json` file. The defaults are used. |
| 0 | 0 | There was no `config.txt`, and there was no `.json` file or the first one is invalid (or the card could not be used). The defaults are used. |

##### Changes

- **v2.2.0**: A file whose name starts with `.` (for example `._name.json`, which macOS writes next to each file it copies to the card) is no longer a candidate for the configuration file. Before, such a file could come first among the `.json` files and, being invalid, hid every valid `.json` file after it.
- **v2.2.0**: The values of a configuration file that was not accepted are no longer applied: a first `.json` file that cannot be parsed or has no `information.configVersion` (it ends the search), and a `config.txt` that failed to parse in the middle. Now the defaults are used, as with no card. Before, the values of such a file were still used, even when it was reported as not loaded (`configName` showed its name).

#### See also

[`/setConfigName`](system-settings.md#setconfigname)
<!-- generated:end osc /getConfigName -->

<!-- osc: /reportError -->
<!-- generated:begin osc /reportError -->
### `/reportError` (bool)enable {#reporterror}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| enable | bool |  |  |

`enable`

| Value | Meaning |
| --- | --- |
| 1 | Enable |
| 0 | Disable |

#### Executable timing

Always

#### Description

Enables or disables the automatic message notification for [`/error/command`](automatically-sent-messages.md#error-command) and [`/error/osc`](automatically-sent-messages.md#error-osc).

#### Response

[`/error/command`](automatically-sent-messages.md#error-command)

```
/error/command (string)errorText (int)motorID
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| errorText | string |  | A character string that indicates the details of an error. |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | The motor's ID |

`errorText`

| Value | Meaning |
| --- | --- |
| CommandIgnored | The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`). |
| MotorIdNotMatch | Motor ID is not appropriate. A motor ID outside 0-255 is replied with the value sent. **v2.2.0**: A motor ID outside 0-255 is replied with the value sent. Before, 257 and 511 were read as 1 and 255. |
| BrakeEngaged | A motion command was sent while the electromagnetic brake was active. Also sent for `/enableServoMode 1` and `/homing` while the brake is engaged, releasing or engaging (not while stopping or after `/free`). |
| HomeSwActivating | Movement from home switch position towards the origin point. Also sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. **v2.2.0**: Sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. It was sent as `HomeSwActivated` before. |
| LimitSwActivating | Movement from limit switch position towards the opposite direction from origin. (STEP400 only) |
| GoUntilTimeout | Timeout while executing `/goUntil` command. |
| ReleaseSwTimeout | Timeout while executing `/releaseSw` command. |
| InServoMode | Received a command which can not be executed while servo mode. **v2.2.0**: Also sent for `/goUntil`, `/goUntilRaw` and `/releaseSw`. |
| BrakeReleaseFailed | `/activate 1` was sent but the driver stayed HiZ (for example without motor power), so the brake stays engaged. Added in v2.2.0. |
| BrakeEngagedOnHiZ | The driver went HiZ by itself (overcurrent shutdown, thermal shutdown, UVLO) while the brake was released, so the brake was engaged. Added in v2.2.0. |
| ServoModeCancelledOnHiZ | The driver went HiZ by itself (overcurrent shutdown, thermal shutdown, UVLO) in the servo mode, so the servo mode was cancelled. Enable it again with `/enableServoMode 1`. Added in v2.2.0. |
| MotorNotHiZ | The command writes a driver register that can be written only while the outputs are HiZ, and the motor is not HiZ. A motor holding its position is not HiZ: send `/softHiZ` or `/hardHiZ` first. Nothing is applied. Added in v2.2.0. |
| MotorNotStopped | The command writes a driver register that can be written only while the motor is stopped or HiZ, and the motor is turning. Nothing is applied. Added in v2.2.0. |

[`/error/osc`](automatically-sent-messages.md#error-osc)

```
/error/osc (string)errorText
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| errorText | string |  | A character string that indicates the details of an error. |

`errorText`

| Value | Meaning |
| --- | --- |
| MessageNotMatch | There is no corresponding command |
| OscSyntaxError | The OSC format is out of standard. Also sent for a packet larger than 512 bytes and for a message with more than 16 arguments. **v2.2.0**: Also sent for a packet larger than 512 bytes and for a message with more than 16 arguments. |
| WrongDataType | Wrong datatype of in argument(s): a string for a number, NaN or infinity, or a non-string for `/setConfigName`. Nothing is applied. **v2.2.0**: Nothing is applied. Before, such an argument was applied as 0. |
| MissingArgument | The message has fewer arguments than the command needs. Nothing is applied. Added in v2.2.0. |

#### Initial value

- `enable`: true (Enable) ([network.reportError](../connections/configuration-items.md#network-reporterror))
<!-- generated:end osc /reportError -->

<!-- osc: /setConfigName -->
<!-- generated:begin osc /setConfigName -->
### `/setConfigName` (string)configName {#setconfigname}

Added in v2.1.0.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| configName | string |  | Configuration name string |

#### Executable timing

Always

#### Description

Sets the configuration name stored in the device. This is a user-editable label for identifying configurations and is distinct from the on-disk filename.

The name changes only in the board until it is saved with [`/saveConfig`](system-settings.md#saveconfig): [`/getConfigName`](system-settings.md#getconfigname) returns the new name at once, but a restart before the save brings back the name in the configuration file.

#### Initial value

- `configName`: Default (firmware) / "" (template) ([information.configName](../connections/configuration-items.md#information-configname))

#### See also

[`/getConfigName`](system-settings.md#getconfigname), [`/saveConfig`](system-settings.md#saveconfig)
<!-- generated:end osc /setConfigName -->

<!-- osc: /saveConfig -->
<!-- generated:begin osc /saveConfig -->
### `/saveConfig` {#saveconfig}

Added in v2.1.0.

#### Argument

None

#### Executable timing

Always

#### Description

Saves the current running configuration to the microSD card as a JSON file. The file is the one read at start-up, or `/config.txt` if no file was read. The path can be changed with `F<path>` over USB serial.

The configuration is written to a hidden temporary file `.<name>.tmp` in the same folder first, and the saved file is replaced only after that has been written. A save that fails while the temporary file is being written leaves the saved file as it was.

The card is checked only at start-up. With no usable card at start-up (a card inserted afterwards, or an exFAT card) the reply is `No SD card`; with a card removed after start-up, a full card or a missing folder it is `SD open failed`. The saved configuration is applied at the next start-up.

#### Changes

- **v2.2.0**: The configuration is written to a hidden temporary file `.<name>.tmp` in the same folder, and the saved file is replaced only after the temporary file has been written and closed. A save that fails (the card or the folder is full, the folder does not exist, a write error) leaves the saved file as it was and replies `SD open failed`. Before, the old file was deleted first, so a failed save left no configuration file on the card. If the power is cut after the old file is deleted and before the new one is renamed, or if the rename fails (`SD open failed`), only the temporary file remains (there is no recovery at start-up). Its name starts with `.`, so it is not read as a configuration file (see [`/configName`](system-settings.md#getconfigname)).
- **v2.2.0**: Arduino IDE build: saving to an exFAT card (SDXC, 64 GB or more by default) deleted the file on the card and replied `SD open failed`. Now the Arduino IDE build is the same as the PlatformIO build: an exFAT card is not used (`No SD card`) and nothing on it is touched. Format the card as FAT16 or FAT32.

#### Response

When: Saved

Added in v2.1.0.

```
/saveConfig (string)message
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| message | string |  | `Saved to SD. Reboot to apply.` |

When: Failed

Added in v2.1.0.

```
/error/saveConfig (string)errorText
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| errorText | string |  |  |

`errorText`

| Value | Meaning |
| --- | --- |
| SD open failed | The card was usable at start-up, but the file could not be written: the card was removed after start-up, the card or the folder is full, the folder does not exist, or a write error. If the temporary file could not be written, the saved file stays as it was. |
| No SD card | There was no usable card at start-up: no card, or a card that is not FAT16 or FAT32 (for example exFAT). A card inserted after start-up is not used until the board restarts. |

#### See also

[`/configName`](system-settings.md#getconfigname), [`/setConfigName`](system-settings.md#setconfigname)
<!-- generated:end osc /saveConfig -->

<!-- osc: /resetDevice -->
<!-- generated:begin osc /resetDevice -->
### `/resetDevice` {#resetdevice}

#### Argument

None

#### Executable timing

Always

#### Description

Resets the entire device. A programmatic version of physically pressing the RESET button.

After the restart, [`/booted`](automatically-sent-messages.md#booted) is sent with `resetCause` 5 (software reset).

#### Changes

- **v2.2.0**: First stops the turning motors that have the electromagnetic brake enabled and not engaged with a hard stop, engages their brakes and waits for the longest `brakeTransitionDuration` of them (at most 1 s), then restarts. Motors without the brake are not stopped by the firmware. Before, the board restarted at once.
- **v2.2.0**: Resets with a software reset: `/booted` reports `resetCause` 5.
<!-- generated:end osc /resetDevice -->
