---
title: Homing
---

# Homing

For how homing and the position work, see [Homing and position](../guides/homing-and-position.md).

<!-- osc: /homing -->
<!-- generated:begin osc /homing -->
### `/homing` (int)motorID {#homing}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Start the homing movement. Move towards origin direction, stop when the HOME switch is activated. Then the motor reverses the direction and move slowly, halts when the HOME switch is not active anymore, then reset location to zero at the current point.

This is equivalent to the following actions of executing [`/goUntil`](homing.md#gountil) command, and after the motor stops on HOME switch activation, execute [`/releaseSw`](homing.md#releasesw) command.

The `homingDirection` and the `homingSpeed` can be set by [`/setHomingDirection`](homing.md#sethomingdirection) and [`/setHomingSpeed`](homing.md#sethomingspeed) commands, as well as configuring from the configuration tool.

Time-out can be set for each of the `/goUntil` and `/releaseSw` commands. The controller halts the motor movement if the sensor state has not changed during this time frame. The time-out values can be set from [`/setGoUntilTimeout`](homing.md#setgountiltimeout) and from the [`/setReleaseSwTimeout`](homing.md#setreleaseswtimeout) command.

Depending on the state change on the homing movement, following response will be sent.

#### Changes

- **v2.2.0**: While the brake is engaged, releasing or engaging (not while stopping or after `/free`), replies `/error/command BrakeEngaged` and does nothing. Before, it set the homing state although it did not start.
- **v2.2.0**: The homing no longer often ends with `/homingStatus` 4 and `ReleaseSwTimeout` about 1 ms after the switch was found, instead of 3 (a timing error of the timeout check; it happened in almost every homing or almost never, depending on the start-up).

#### Response

[`/homingStatus`](automatically-sent-messages.md#homingstatus)

```
/homingStatus (int)motorID (int)homingStatus
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| homingStatus | int | 0-4 | Homing status |

#### Errors

- `CommandIgnored`: The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`).
- `BrakeEngaged`: A motion command was sent while the electromagnetic brake was active. Also sent for `/enableServoMode 1` and `/homing` while the brake is engaged, releasing or engaging (not while stopping or after `/free`).
- `GoUntilTimeout`: Timeout while executing `/goUntil` command.
- `ReleaseSwTimeout`: Timeout while executing `/releaseSw` command.
- `InServoMode`: Received a command which can not be executed while servo mode. **v2.2.0**: Also sent for `/goUntil`, `/goUntilRaw` and `/releaseSw`.

#### See also

[`/getHomingStatus`](homing.md#gethomingstatus)
<!-- generated:end osc /homing -->

<!-- osc: /getHomingStatus -->
<!-- generated:begin osc /getHomingStatus -->
### `/getHomingStatus` (int)motorID {#gethomingstatus}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Returns current state of homing movement.

#### Response

[`/homingStatus`](automatically-sent-messages.md#homingstatus)

```
/homingStatus (int)motorID (int)homingStatus
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| homingStatus | int | 0-4 | Homing status |
<!-- generated:end osc /getHomingStatus -->

<!-- osc: /setHomingDirection -->
<!-- generated:begin osc /setHomingDirection -->
### `/setHomingDirection` (int)motorID (bool)direction {#sethomingdirection}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| direction | bool |  |  |

`direction`

| Value | Meaning |
| --- | --- |
| 1 | Forward |
| 0 | Reverse |

#### Executable timing

Always

#### Description

Sets the `homingDirection` for the [`/homing`](homing.md#homing) command. It can be also configured from the configuration tool.

#### Initial value

- `direction`: 0 (Reverse) ([driverSettings.homingDirection](../connections/configuration-items.md#driversettings-homingdirection))

#### See also

[`/getHomingDirection`](homing.md#gethomingdirection)
<!-- generated:end osc /setHomingDirection -->

<!-- osc: /getHomingDirection -->
<!-- generated:begin osc /getHomingDirection -->
### `/getHomingDirection` (int)motorID {#gethomingdirection}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Returns `homingDirection` parameter.

#### Response

```
/homingDirection (int)motorID (int)homingDirection
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| homingDirection | int |  |  |

`homingDirection`

| Value | Meaning |
| --- | --- |
| 1 | Forward |
| 0 | Reverse |
<!-- generated:end osc /getHomingDirection -->

<!-- osc: /setHomingSpeed -->
<!-- generated:begin osc /setHomingSpeed -->
### `/setHomingSpeed` (int)motorID (float)speed {#sethomingspeed}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| speed | float | 0-15610 step/s | homing speed |

#### Executable timing

Always

#### Description

Sets the `homingSpeed` when executing the command [`/homing`](homing.md#homing). It can be configured from the configuration tool.

A value outside the range is not rejected: it is limited to 0-15610.

#### Initial value

- `speed`: 50 ([driverSettings.homingSpeed](../connections/configuration-items.md#driversettings-homingspeed))

#### See also

[`/getHomingSpeed`](homing.md#gethomingspeed)
<!-- generated:end osc /setHomingSpeed -->

<!-- osc: /getHomingSpeed -->
<!-- generated:begin osc /getHomingSpeed -->
### `/getHomingSpeed` (int)motorID {#gethomingspeed}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Returns `homingSpeed` parameter.

#### Response

```
/homingSpeed (int)motorID (float)homingSpeed
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| homingSpeed | float | 0-15610 step/s | homing speed |
<!-- generated:end osc /getHomingSpeed -->

<!-- osc: /goUntil -->
<!-- generated:begin osc /goUntil -->
### `/goUntil` (int)motorID (bool)ACT (float)speed {#gountil}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| ACT | bool |  |  |
| speed | float | -15625-15625 step/s |  |

`ACT`

| Value | Meaning |
| --- | --- |
| 0 | Reset the ABS_POS register |
| 1 | Copy the value of the ABS_POS register to the MARK register |

#### Executable timing

Always

#### Description

Move the motor at specified speed and direction. When the HOME switch turns on (the HOME switch terminal is closed), process ABS_POS register according to the ACT value.  
The motor will softStop afterwards, but if the SW_MODE is set to 0 in the [`/setHomeSwMode`](home-and-limit-sensors.md#sethomeswmode) command, it will be a hardStop instead. This command will keep the motor to the BUSY state until it stops.

The sign of the speed is the direction. A speed whose absolute value is above the range is limited to the largest register value (0xFFFFF, about 15625 step/s) by the driver library.

#### Changes

- **v2.2.0**: An activated home switch is reported as `/error/command HomeSwActivating`, the text in the error list. It was sent as `HomeSwActivated`. It now follows [`/reportError`](system-settings.md#reporterror) like the other command errors.
- **v2.2.0**: For a motor in the servo mode, replies `/error/command InServoMode` and does nothing. Before, the command was sent to the driver. With 255, only the motors in the servo mode reply the error; the others execute the command.

#### Errors

- `BrakeEngaged`: A motion command was sent while the electromagnetic brake was active. Also sent for `/enableServoMode 1` and `/homing` while the brake is engaged, releasing or engaging (not while stopping or after `/free`).
- `GoUntilTimeout`: Timeout while executing `/goUntil` command.
- `HomeSwActivating`: Movement from home switch position towards the origin point. Also sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. **v2.2.0**: Sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. It was sent as `HomeSwActivated` before.
- `InServoMode`: Received a command which can not be executed while servo mode. **v2.2.0**: Also sent for `/goUntil`, `/goUntilRaw` and `/releaseSw`.

#### See also

[`/setGoUntilTimeout`](homing.md#setgountiltimeout), [`/releaseSw`](homing.md#releasesw), [`/goUntilRaw`](motor-control.md#gountilraw)
<!-- generated:end osc /goUntil -->

<!-- osc: /setGoUntilTimeout -->
<!-- generated:begin osc /setGoUntilTimeout -->
### `/setGoUntilTimeout` (int)motorID (int)timeOut {#setgountiltimeout}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| timeOut | int | 0-2147483647 ms | Time-out duration |

#### Executable timing

Always

#### Description

Sets the time-out duration when executing [`/goUntil`](homing.md#gountil) command. If the sensor did not detect during this time frame, the controller will regard time-out and halts the movement. Specify 0 to disable the timeout. It can also be configured from the configuration tool.

A negative value replies `CommandIgnored` and nothing is applied. The maximum is 2147483647. The automatic hard stop at the timeout is not sent to a motor whose driver is HiZ (the timeout error is still sent).

#### Changes

- **v2.2.0**: A negative value replies `/error/command CommandIgnored` and nothing is applied. Before, it became about 49 days.
- **v2.2.0**: The hard stop at the timeout is not sent to a motor whose driver is HiZ, also with the brake disabled (a hard stop energizes a HiZ driver). The timeout error is still sent.

#### Errors

- `CommandIgnored`: The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`).

#### Initial value

- `timeOut`: 10000 ([driverSettings.goUntilTimeout](../connections/configuration-items.md#driversettings-gountiltimeout))

#### See also

[`/getGoUntilTimeout`](homing.md#getgountiltimeout)
<!-- generated:end osc /setGoUntilTimeout -->

<!-- osc: /getGoUntilTimeout -->
<!-- generated:begin osc /getGoUntilTimeout -->
### `/getGoUntilTimeout` (int)motorID {#getgountiltimeout}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Returns the time-out duration when executing [`/goUntil`](homing.md#gountil) command.

#### Response

```
/goUntilTimeout (int)motorID (int)timeout
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| timeout | int | 0-2147483647 ms | Time-out duration |
<!-- generated:end osc /getGoUntilTimeout -->

<!-- osc: /releaseSw -->
<!-- generated:begin osc /releaseSw -->
### `/releaseSw` (int)motorID (bool)ACT (bool)DIR {#releasesw}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| ACT | bool |  |  |
| DIR | bool |  |  |

`ACT`

| Value | Meaning |
| --- | --- |
| 0 | Reset the ABS_POS register |
| 1 | Copy the value of the ABS_POS register to the MARK register |

`DIR`

| Value | Meaning |
| --- | --- |
| 1 | Forward |
| 0 | Reverse |

#### Executable timing

Always

#### Description

Move at minimum speed (5[step/s] by default) in the specified direction until the HOME switch pin becomes open. Then it will process the ABS_POS register according to the value of ACT. The process of the ACT is same as the [`/goUntil`](homing.md#gountil) command. Then halt the motor with hardStop.

#### Changes

- **v2.2.0**: `ACT` is read like the other boolean arguments (a number of 1.0 or more, or a positive integer, is true). It was read as an integer, so 0.5 was 0.
- **v2.2.0**: For a motor in the servo mode, replies `/error/command InServoMode` and does nothing. Before, the command was sent to the driver. With 255, only the motors in the servo mode reply the error; the others execute the command.

#### Errors

- `BrakeEngaged`: A motion command was sent while the electromagnetic brake was active. Also sent for `/enableServoMode 1` and `/homing` while the brake is engaged, releasing or engaging (not while stopping or after `/free`).
- `ReleaseSwTimeout`: Timeout while executing `/releaseSw` command.
- `InServoMode`: Received a command which can not be executed while servo mode. **v2.2.0**: Also sent for `/goUntil`, `/goUntilRaw` and `/releaseSw`.

#### See also

[`/setReleaseSwTimeout`](homing.md#setreleaseswtimeout), [`/setMinSpeed`](speed-profile.md#setminspeed)
<!-- generated:end osc /releaseSw -->

<!-- osc: /setReleaseSwTimeout -->
<!-- generated:begin osc /setReleaseSwTimeout -->
### `/setReleaseSwTimeout` (int)motorID (int)timeOut {#setreleaseswtimeout}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| timeOut | int | 0-2147483647 ms | Time-out duration |

#### Executable timing

Always

#### Description

Sets the time-out duration when executing [`/releaseSw`](homing.md#releasesw) command. If the sensor cannot be released during this time frame, halt the movement as time-out. Specify 0 to disable the timeout. It can be configured from the configuration tool.

A negative value replies `CommandIgnored` and nothing is applied. The maximum is 2147483647. The automatic hard stop at the timeout is not sent to a motor whose driver is HiZ (the timeout error is still sent).

#### Changes

- **v2.2.0**: A negative value replies `/error/command CommandIgnored` and nothing is applied. Before, it became about 49 days.
- **v2.2.0**: The hard stop at the timeout is not sent to a motor whose driver is HiZ, also with the brake disabled (a hard stop energizes a HiZ driver). The timeout error is still sent.

#### Errors

- `CommandIgnored`: The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`).

#### Initial value

- `timeOut`: 10000 ([driverSettings.releaseSwTimeout](../connections/configuration-items.md#driversettings-releaseswtimeout))

#### See also

[`/getReleaseSwTimeout`](homing.md#getreleaseswtimeout)
<!-- generated:end osc /setReleaseSwTimeout -->

<!-- osc: /getReleaseSwTimeout -->
<!-- generated:begin osc /getReleaseSwTimeout -->
### `/getReleaseSwTimeout` (int)motorID {#getreleaseswtimeout}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Returns the time-out duration when executing [`/releaseSw`](homing.md#releasesw) command.

#### Response

```
/releaseSwTimeout (int)motorID (int)timeout
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| timeout | int | 0-2147483647 ms | Time-out duration |
<!-- generated:end osc /getReleaseSwTimeout -->
