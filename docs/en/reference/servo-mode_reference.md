---
title: Servo mode
---

# Servo mode

For how the servo mode works, see [Servo mode](../guides/servo-mode.md).

<!-- osc: /enableServoMode -->
<!-- generated:begin osc /enableServoMode -->
### `/enableServoMode` (int)motorID (bool)enable {#enableservomode}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| enable | bool |  |  |

`enable`

| Value | Meaning |
| --- | --- |
| 1 | Enable |
| 0 | Disable |

#### Executable timing

Always

#### Description

Turns on/off the servo mode (position tracking mode). To avoid sudden movement, the current position at the moment of activation is set to the target position.  
It is not possible to send other motor control commands such as `/run` or `/goTo` while operating in this mode.

Enabling the servo mode turns off the BUSY, motor status and direction reports ([`/enableBusyReport`](motor-driver-settings.md#enablebusyreport), [`/enableMotorStatusReport`](motor-driver-settings.md#enablemotorstatusreport), [`/enableDirReport`](motor-driver-settings.md#enabledirreport)) of the motor. Disabling the servo mode does not turn them on again; send the enable commands again if needed. It also resets the integral term and the previous error of the PID controller. While in the servo mode, [`/goUntil`](homing.md#gountil), [`/goUntilRaw`](motor-control.md#gountilraw), [`/releaseSw`](homing.md#releasesw) and [`/homing`](homing.md#homing) reply `InServoMode`.

With the electromagnetic brake enabled, `/enableServoMode 1` replies `BrakeEngaged` and does nothing while the brake is engaged, releasing or engaging (while stopping or after `/free` the command is executed); `/enableServoMode 0` does nothing while the brake is engaged or after [`/free`](brake.md#free).

When the driver goes HiZ by itself (overcurrent shutdown, thermal shutdown, UVLO) in the servo mode, the servo mode is cancelled and `ServoModeCancelledOnHiZ` is sent (`BrakeEngagedOnHiZ` too, with the brake enabled). Enable the servo mode again with `/enableServoMode 1`; the current position becomes the target.

#### Changes

- **v2.2.0**: With the brake enabled, `/enableServoMode 1` while the brake is engaged, releasing or engaging (not while stopping or after `/free`) replies `/error/command BrakeEngaged` and does nothing. Before, it energized and moved the motor with the brake engaged.
- **v2.2.0**: With the brake enabled, `/enableServoMode 0` while the brake is engaged or after `/free` (motor HiZ) does nothing. Before, it energized the motor.
- **v2.2.0**: When a driver goes HiZ by itself (overcurrent shutdown, thermal shutdown, UVLO) in the servo mode, the servo mode is cancelled and `/error/command ServoModeCancelledOnHiZ` is sent (follows [`/reportError`](system-settings.md#reporterror)), with or without the brake. With the brake enabled, `BrakeEngagedOnHiZ` is also sent. Before, with the brake disabled the next servo update energized the driver again. The commands that make the driver HiZ cancel the servo mode first and do not send this error.
- **v2.2.0**: Enabling the servo mode resets the integral and the previous error of the PID controller. The previous values were kept from the last time the servo mode was used.
- **v2.2.0**: The update period is 5 ms instead of 10 ms (and no longer varies between 7 and 13 ms when position reports are enabled; an OSC message that sends several replies can still delay one update, up to 7.75 ms measured). The integral and derivative terms are scaled by the period, so the same `kP`, `kI` and `kD` were designed to give about the same response; retune the gains if needed.
- **v2.2.0**: STEP400: the home switch and the limit switch are judged separately. A pressed home switch stops the motion towards `homingDirection` (with `/setProhibitMotionOnHomeSw` or the home switch in the hard stop mode), and a pressed limit switch stops the motion away from it (with `/setProhibitMotionOnLimitSw` or the limit switch in the hard stop mode), as before. While the home switch was pressed, the limit switch was not checked. Only a motor with both switches pressed behaves differently.
- **v2.2.0**: The automatic hard stop at a switch event in the servo mode is not sent to a motor whose driver is HiZ.
- **v2.2.0**: Cancels pending motion, also for a motor with the brake disabled: a `/goTo`, `/goToDir`, `/goHome` or `/goMark` waiting for the BUSY flag to clear (it was sent when the motor became not busy, so a stopped motor started again), the homing (its timeout sent a hard stop, which energized a motor made HiZ in the meantime) and the servo mode.

#### Response

When: While homing is in progress

[`/homingStatus`](automatically-sent-messages.md#homingstatus)

```
/homingStatus (int)motorID (int)homingStatus
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| homingStatus | int | 0-4 | Homing status |

#### Errors

- `BrakeEngaged`: A motion command was sent while the electromagnetic brake was active. Also sent for `/enableServoMode 1` and `/homing` while the brake is engaged, releasing or engaging (not while stopping or after `/free`).

#### See also

[`/setTargetPosition`](servo-mode_reference.md#settargetposition), [`/setServoParam`](servo-mode_reference.md#setservoparam)
<!-- generated:end osc /enableServoMode -->

<!-- osc: /setServoParam -->
<!-- generated:begin osc /setServoParam -->
### `/setServoParam` (int)motorID (float)kP (float)kI (float)kD {#setservoparam}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| kP | float |  | Proportional control gain |
| kI | float |  | Integral control gain |
| kD | float |  | Differential control gain |

#### Executable timing

Always

#### Description

Adjusts the PID control gain.

A negative gain replies `CommandIgnored` and nothing is applied. The update period of the servo mode is 5 ms; the integral and derivative terms are scaled by the period.

#### Changes

- **v2.2.0**: A negative gain replies `/error/command CommandIgnored` and nothing is applied. Before, it was set to 0.
- **v2.2.0**: The servo update period is 5 ms instead of 10 ms. The same gains were designed to give about the same response, but retune them if needed.

#### Errors

- `CommandIgnored`: The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`).

#### Initial value

- `kP`: 0.06 ([servoMode.kP](../connections/configuration-items.md#servomode-kp))
- `kI`: 0 ([servoMode.kI](../connections/configuration-items.md#servomode-ki))
- `kD`: 0 ([servoMode.kD](../connections/configuration-items.md#servomode-kd))

#### See also

[`/getServoParam`](servo-mode_reference.md#getservoparam)
<!-- generated:end osc /setServoParam -->

<!-- osc: /getServoParam -->
<!-- generated:begin osc /getServoParam -->
### `/getServoParam` (int)motorID {#getservoparam}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Gets the PID gains (kP, kI, kD) of the servo mode.

#### Response

```
/servoParam (int)motorID (float)kP (float)kI (float)kD
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| kP | float |  | Proportional control gain |
| kI | float |  | Integral control gain |
| kD | float |  | Differential control gain |
<!-- generated:end osc /getServoParam -->

<!-- osc: /setTargetPosition -->
<!-- generated:begin osc /setTargetPosition -->
### `/setTargetPosition` (int)motorID (int)position {#settargetposition}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| position | int | -2097152-2097151 | target position |

#### Executable timing

Always

#### Description

Sets the target position in servo mode.

#### See also

[`/enableServoMode`](servo-mode_reference.md#enableservomode), [`/setTargetPositionList`](servo-mode_reference.md#settargetpositionlist)
<!-- generated:end osc /setTargetPosition -->

<!-- osc: /setTargetPositionList -->
<!-- generated:begin osc /setTargetPositionList -->
### `/setTargetPositionList` (int)position1 ... (int)positionN {#settargetpositionlist}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| position1 ... positionN | int | -2097152-2097151 | target position |

#### Executable timing

Always

#### Description

Sets the target positions of the servo mode for all axes at once.

#### Changes

- **v2.2.0**: A message with fewer positions than the number of motors replies `/error/osc MissingArgument` and nothing is applied. Before, the missing positions became 0 and a servo-mode motor ran to 0.

#### See also

[`/setTargetPosition`](servo-mode_reference.md#settargetposition)
<!-- generated:end osc /setTargetPositionList -->
