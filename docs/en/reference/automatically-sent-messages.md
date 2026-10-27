---
title: Automatically sent messages
---

# Automatically sent messages

## Summary

Most messages the board sends are replies to commands. For example, when you send [`/getPosition`](position-management.md#getposition) to get the current position of a motor, the board replies with [`/position`](#position). Some messages, however, are not replies to a specific command: the board sends them automatically, for example when its state changes. This page describes these automatically sent messages. A message that is only a reply is shown in the "Response" field of each command.

## Startup notification

<!-- osc-message: /booted -->
<!-- generated:begin osc-message /booted -->
### `/booted` (int)deviceID (int)resetCause {#booted}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| deviceID | int | 0-255 | The device ID set by the DIP Switch |
| resetCause | int |  | The cause of the reset, as reported by the MCU. (Added in v2.2.0.) |

`resetCause`

| Value | Meaning |
| --- | --- |
| 0 | Unknown |
| 1 | Power-on. Treat 1 and 2 both as a reset by the power supply |
| 2 | Brown-out (supply voltage drop). On the SAMD21 a normal power-up is often reported as 2 |
| 3 | Reset pin |
| 4 | Watchdog |
| 5 | Software reset (for example after [`/resetDevice`](system-settings.md#resetdevice) or a firmware upload over USB) |
| 6 | CPU fault: the reset after a CPU exception (HardFault on the SAMD21) |

#### Description

This message is automatically sent out when the device has (re)started. By watching the message, you can detect reset event of the device triggered by some reason.

The message will be sent out one second after the firmware is started up and the ethernet link is established. The message will be sent to `255.255.255.255`, means broadcasting to all nodes within the subnet.

This message can be disabled from the configuration tool.

`resetCause`: the numbers are part of the specification; new causes will only be added as 7, 8, .... A client should treat a number it does not know as "other", and accept 6. If several causes are flagged, the first of CPU fault, brown-out, power-on, watchdog, reset pin, software is reported. After a power-on or a brown-out the CPU fault is never reported, so a fault followed by a power cycle reports 1 or 2. The numbers are those reported by the MCU as they are; with another MCU in the future the same operation may report a different number (the meaning of each number does not change).

#### Changes

- **v2.2.0**: A second argument, `resetCause` (`i`), is added: `/booted myId resetCause`. Clients that check the exact number of arguments are affected.
- **v2.2.0**: After a watchdog detects a hang (about 250 ms after the last watchdog reset), every brake output is engaged first and the firmware waits for the longest `brakeTransitionDuration` of the motors with the brake enabled and not engaged (at most 1 s) before the board is reset, so the reset comes up to 1 s later than before; `resetCause` is still 4. v2.1.0 reset the board about 62.5 ms after a hang.
- **v2.2.0**: A CPU fault (HardFault) now engages every brake output at once, waits as above (at most 1 s), and restarts with `resetCause` 6.
- **v2.2.0**: The reset by [`/resetDevice`](system-settings.md#resetdevice) now reports `resetCause` 5 (software).
<!-- generated:end osc-message /booted -->

## Error

<!-- osc-message: /error/osc -->
<!-- generated:begin osc-message /error/osc -->
### `/error/osc` (string)errorText {#error-osc}

#### Argument

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

#### Description

Sent if any error is detected in the received OSC (Open Sound Control) message.

The arguments of every command are checked before the command is applied. Arguments beyond the ones a command needs are ignored. The message is not sent while error reports are disabled ([`/reportError`](system-settings.md#reporterror)).

#### Changes

- **v2.2.0**: `MissingArgument` is new: a command with too few arguments replies it and applies nothing. Before, missing arguments were applied as 0 (`/setKval 1` set every KVAL of motor 1 to 0, `/setSpeedProfile 1` set acc, dec and max speed to 0, and the positions missing in `/setTargetPositionList` became 0).
- **v2.2.0**: `WrongDataType` is replied for an argument of the wrong type (a string for a number, NaN or infinity, `/setConfigName` with a non-string) and applies nothing. Before, the argument was applied as 0.
- **v2.2.0**: A packet larger than 512 bytes and a message with more than 16 arguments are answered with `OscSyntaxError`.
- **v2.2.0**: In some corner cases where the former OSC library read past the end of the address pattern (for example characters following a `{...}` list), the match result can differ from before.
<!-- generated:end osc-message /error/osc -->

<!-- osc-message: /error/command -->
<!-- generated:begin osc-message /error/command -->
### `/error/command` (string)errorText (int)motorID {#error-command}

#### Argument

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

#### Description

This message will be sent if an error is detected while executing a command.  
The message can be enabled or disabled with [`/reportError`](system-settings.md#reporterror) command.

With 255 (all motors), each motor is judged alone for the errors that depend on the state of a motor (`MotorNotHiZ`, `MotorNotStopped`): the motors in the required state are changed and the others reply the error.

#### Changes

- **v2.2.0**: New errors: `BrakeReleaseFailed`, `BrakeEngagedOnHiZ`, `ServoModeCancelledOnHiZ` (electromagnetic brake and servo mode), `MotorNotHiZ` and `MotorNotStopped` (registers that can be written only in some states). All follow [`/reportError`](system-settings.md#reporterror).
- **v2.2.0**: `CommandIgnored` is also replied when a value is outside the range of the command, and nothing is applied: [`/setPositionReportInterval`](motor-driver-settings.md#setpositionreportinterval) and [`/setPositionListReportInterval`](motor-driver-settings.md#setpositionlistreportinterval) above 65535 (255 for the list), [`/setGoUntilTimeout`](homing.md#setgountiltimeout) and [`/setReleaseSwTimeout`](homing.md#setreleaseswtimeout) below 0, [`/setElPos`](position-management.md#setelpos) with a full step outside 0-3 or a microstep outside 0-127, [`/setServoParam`](servo-mode_reference.md#setservoparam) with a negative gain, [`/setBrakeTransitionDuration`](brake.md#setbraketransitionduration) outside 0-65535, [`/setDecayModeParam`](voltage-and-current-mode-settings.md#setdecaymodeparam) with TON_MIN or TOFF_MIN above 127.
- **v2.2.0**: `MotorIdNotMatch` is replied for a motor ID outside 0-255, with the value sent. Before, 257 and 511 were read as 1 and 255.
- **v2.2.0**: `HomeSwActivating` is replied by `/goUntil` and `/goUntilRaw` for an activated home switch. It was sent as `HomeSwActivated`, and it now follows `/reportError` like the other command errors.
<!-- generated:end osc-message /error/command -->

## Notification of state

<!-- osc-message: /busy -->
<!-- generated:begin osc-message /busy -->
### `/busy` (int)motorID (int)state {#busy}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| state | int |  |  |

`state`

| Value | Meaning |
| --- | --- |
| 1 | BUSY |
| 0 | Not BUSY |
<!-- generated:end osc-message /busy -->

<!-- osc-message: /HiZ -->
<!-- generated:begin osc-message /HiZ -->
### `/HiZ` (int)motorID (int)state {#hiz}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| state | int | 0-1 | 1 if High Z state, 0 if not High Z state. |
<!-- generated:end osc-message /HiZ -->

<!-- osc-message: /dir -->
<!-- generated:begin osc-message /dir -->
### `/dir` (int)motorID (int)direction {#dir}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| direction | int |  |  |

`direction`

| Value | Meaning |
| --- | --- |
| 1 | Forward |
| 0 | Reverse |
<!-- generated:end osc-message /dir -->

<!-- osc-message: /motorStatus -->
<!-- generated:begin osc-message /motorStatus -->
### `/motorStatus` (int)motorID (int)MOT_STATUS {#motorstatus}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| MOT_STATUS | int | 0-3 | Motor status |

`MOT_STATUS`

| Value | Meaning |
| --- | --- |
| 0 | Stopped |
| 1 | Acceleration |
| 2 | Deceleration |
| 3 | Constant speed |
<!-- generated:end osc-message /motorStatus -->

<!-- osc-message: /homingStatus -->
<!-- generated:begin osc-message /homingStatus -->
### `/homingStatus` (int)motorID (int)homingStatus {#homingstatus}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| homingStatus | int | 0-4 | Homing status |

##### Homing status

| homingStatus | Homing status | Description |
| --- | --- | --- |
| 0 | HOMING_UNDEFINED | Not yet executing homing movement |
| 1 | HOMING_GOUNTIL | Executing `/goUntil` |
| 2 | HOMING_RELEASESW | Executing `/releaseSw` |
| 3 | HOMING_COMPLETED | Homing done |
| 4 | HOMING_TIMEOUT | The movement did not complete during specified time frame. |
<!-- generated:end osc-message /homingStatus -->

<!-- osc-message: /position -->
<!-- generated:begin osc-message /position -->
### `/position` (int)motorID (int)ABS_POS {#position}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| ABS_POS | int | -2097152-2097151 | current position |
<!-- generated:end osc-message /position -->

<!-- osc-message: /positionList -->
<!-- generated:begin osc-message /positionList -->
### `/positionList` (int)position1 ... (int)positionN {#positionlist}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| position1 ... positionN | int | -2097152-2097151 | current position of the motor #n |
<!-- generated:end osc-message /positionList -->

<!-- osc-message: /homeSw -->
<!-- generated:begin osc-message /homeSw -->
### `/homeSw` (int)motorID (int)swState (int)direction {#homesw}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| swState | int |  | State |
| direction | int |  | direction |

`swState`

| Value | Meaning |
| --- | --- |
| 0 | Open, Undetected state |
| 1 | Closed, Detected state |

`direction`

| Value | Meaning |
| --- | --- |
| 1 | Forward |
| 0 | Reverse |
<!-- generated:end osc-message /homeSw -->

<!-- osc-message: /swEvent -->
<!-- generated:begin osc-message /swEvent -->
### `/swEvent` (int)motorID {#swevent}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
<!-- generated:end osc-message /swEvent -->

<!-- osc-message: /limitSw -->
<!-- generated:begin osc-message /limitSw -->
### `/limitSw` (int)motorID (int)swState (int)direction {#limitsw}

Available on STEP400 only.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| swState | int |  | Status |
| direction | int |  | Direction |

`swState`

| Value | Meaning |
| --- | --- |
| 0 | Open, Undetected state |
| 1 | Closed, Detected state |

`direction`

| Value | Meaning |
| --- | --- |
| 1 | Forward |
| 0 | Reverse |
<!-- generated:end osc-message /limitSw -->

## Alarm notifications

<!-- osc-message: /uvlo -->
<!-- generated:begin osc-message /uvlo -->
### `/uvlo` (int)motorID (int)state {#uvlo}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| state | int |  |  |

`state`

| Value | Meaning |
| --- | --- |
| 1 | UVLO detected |
| 0 | No UVLO condition |

#### Changes

- **v2.2.0**: The report sent when the UVLO state changes (enabled by [`/enableUvloReport`](alarm-settings.md#enableuvloreport)) is sent with the integer type tag `i` (0 / 1), as the reply to [`/getUvlo`](alarm-settings.md#getuvlo) always was. Before, the report used `T` / `F`. Clients that expect `T` / `F` must be updated.
<!-- generated:end osc-message /uvlo -->

<!-- osc-message: /thermalStatus -->
<!-- generated:begin osc-message /thermalStatus -->
### `/thermalStatus` (int)motorID (int)thermalStatus {#thermalstatus}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| thermalStatus | int | 0-3 | Thermal status |

##### Thermal status - STEP400

| thermalStatus | Thermal status | Set condition | Release condition | Description |
| --- | --- | --- | --- | --- |
| 0 | Normal | - | - | Normal operation |
| 1 | Warning | 135℃ | 125℃ | Thermal warning. Operation is not limited. |
| 2 | Bridge shutdown | 155℃ | 145℃ | Thermal shutdown. The bridges are turned off. |
| 3 | Device shutdown | 170℃ | 130℃ | Thermal shutdown. The internal regulators are also turned off. |

##### Thermal status - STEP800

| thermalStatus | Thermal status | Set condition | Release condition | Description |
| --- | --- | --- | --- | --- |
| 0 | Normal | - | - | Normal operation |
| 1 | Warning | 130℃ | 130℃ | Thermal warning. Operation is not limited. |
| 2 | Bridge shutdown | 160℃ | 130℃ | Thermal shutdown. The bridges are turned off. |
<!-- generated:end osc-message /thermalStatus -->

<!-- osc-message: /overCurrent -->
<!-- generated:begin osc-message /overCurrent -->
### `/overCurrent` (int)motorID {#overcurrent}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |

#### Description

Sent at once when the overcurrent condition starts (if no such report of the motor went out in the last 200 ms) and then, while it lasts, at most every 200 ms per motor. Detections within the 200 ms are not lost: they give one message at the end of the interval. Detections while the report is disabled ([`/enableOverCurrentReport`](alarm-settings.md#enableovercurrentreport)) are not sent later.

#### Changes

- **v2.2.0**: Sent at once when the condition starts (if no such report of the motor went out in the last 200 ms) and then, while it lasts, at most every 200 ms per motor. Before, it was sent at every status read while the condition lasted (every 10 ms). The message is unchanged.
<!-- generated:end osc-message /overCurrent -->

<!-- osc-message: /stall -->
<!-- generated:begin osc-message /stall -->
### `/stall` (int)motorID {#stall}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |

#### Description

Sent at once when the stall condition starts (if no such report of the motor went out in the last 200 ms) and then, while it lasts, at most every 200 ms per motor. Detections within the 200 ms are not lost: they give one message at the end of the interval. Detections while the report is disabled ([`/enableStallReport`](alarm-settings.md#enablestallreport)) are not sent later.

Stall detection lets the driver detect, from the motor current, that the motor can no longer turn against the load. Find a threshold ([`/setStallThreshold`](alarm-settings.md#setstallthreshold)) as close as possible to, and slightly above, the current actually flowing. A small loss of steps cannot be detected, but a large position error may be.

#### Changes

- **v2.2.0**: Sent at once when the condition starts (if no such report of the motor went out in the last 200 ms) and then, while it lasts, at most every 200 ms per motor. Before, it was sent at every status read while the condition lasted (every 10 ms). The message is unchanged.
<!-- generated:end osc-message /stall -->
