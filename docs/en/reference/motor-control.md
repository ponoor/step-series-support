---
title: Motor control
---

# Motor control

For how the motions work, see [Speed profile and motions](../guides/speed-profile-and-motions.md).

## Motor movement

<!-- osc: /run -->
<!-- generated:begin osc /run -->
### `/run` (int)motorID (float)speed {#run}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| speed | float | -15625-15625 step/s | Rotation speed |

#### Executable timing

In motion start condition

#### Description

Rotates the motor at specified speed. The acceleration is controlled with the pre-set speed profile. The speed is limited by maxSpeed. It remains in the BUSY state until the motor reaches the specified speed.

The sign of the speed is the direction. A speed whose absolute value is above the range is limited to the largest register value (0xFFFFF, about 15625 step/s) by the driver library.

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
- `HomeSwActivating`: Movement from home switch position towards the origin point. Also sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. **v2.2.0**: Sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. It was sent as `HomeSwActivated` before.
- `LimitSwActivating`: Movement from limit switch position towards the opposite direction from origin.
- `InServoMode`: Received a command which can not be executed while servo mode. **v2.2.0**: Also sent for `/goUntil`, `/goUntilRaw` and `/releaseSw`.

#### See also

[`/runRaw`](motor-control.md#runraw), [`/combine/run`](motor-control.md#combine-run)
<!-- generated:end osc /run -->

<!-- osc: /move -->
<!-- generated:begin osc /move -->
### `/move` (int)motorID (int)step {#move}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| step | int |  | Moving step counts |

#### Executable timing

When the motor is stopped, In motion start condition

#### Description

Moves specified number of steps according to the pre-set speed profile. It remains in the BUSY state until it reaches the specified step count. This command can only execute when the motor is stopped.

A step count whose absolute value is above 4,194,303 (22 bits) is not rejected: it is limited to 4,194,303 by the driver library.

#### Errors

- `BrakeEngaged`: A motion command was sent while the electromagnetic brake was active. Also sent for `/enableServoMode 1` and `/homing` while the brake is engaged, releasing or engaging (not while stopping or after `/free`).
- `HomeSwActivating`: Movement from home switch position towards the origin point. Also sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. **v2.2.0**: Sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. It was sent as `HomeSwActivated` before.
- `LimitSwActivating`: Movement from limit switch position towards the opposite direction from origin.
- `InServoMode`: Received a command which can not be executed while servo mode. **v2.2.0**: Also sent for `/goUntil`, `/goUntilRaw` and `/releaseSw`.

#### See also

[`/combine/move`](motor-control.md#combine-move)
<!-- generated:end osc /move -->

<!-- osc: /goTo -->
<!-- generated:begin osc /goTo -->
### `/goTo` (int)motorID (int)position {#goto}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| position | int | -2097152-2097151 | Destination |

#### Executable timing

In motion start condition

#### Description

Moves to the specified position in the shortest route according to the pre-set speed profile. Remains in the BUSY state until it finishes moving to the specified position.  
Inside the driver, -2,097,152 and 2,097,151 are located next to each other in a loop.

A position outside the range is not rejected. A position above 4,194,303 is limited to 4,194,303 by the driver library, which the driver reads as -1. Any other position is cut to its lower 22 bits and read as a signed number: 2,097,152 becomes -2,097,152 and -2,097,153 becomes 2,097,151.

#### Changes

- **v2.2.0**: Judges its direction correctly when the home switch or the limit switch prohibits a motion ([`/setProhibitMotionOnHomeSw`](alarm-settings.md#setprohibitmotiononhomesw), [`/setProhibitMotionOnLimitSw`](alarm-settings.md#setprohibitmotiononlimitsw)): it is the sign of the 22-bit difference to the target, the way the driver goes (the shortest way). The direction was reversed for a target less than 2048 steps away (so a short move away from the switch was refused with `HomeSwActivating` / `LimitSwActivating` and a short move towards it was started), and wrong again beyond 2^21 steps.
- **v2.2.0**: On a busy motor, the STATUS register is read with GetParam, which does not clear the latched flags. Before, it was read with GetStatus, so the status poll could miss a flag and the report (`/overCurrent`, `/stall`, `/swEvent`, `/uvlo`, ...) was lost.

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
- `HomeSwActivating`: Movement from home switch position towards the origin point. Also sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. **v2.2.0**: Sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. It was sent as `HomeSwActivated` before.
- `LimitSwActivating`: Movement from limit switch position towards the opposite direction from origin.
- `InServoMode`: Received a command which can not be executed while servo mode. **v2.2.0**: Also sent for `/goUntil`, `/goUntilRaw` and `/releaseSw`.

#### See also

[`/goToDir`](motor-control.md#gotodir), [`/combine/goTo`](motor-control.md#combine-goto)
<!-- generated:end osc /goTo -->

<!-- osc: /goToDir -->
<!-- generated:begin osc /goToDir -->
### `/goToDir` (int)motorID (bool)DIR (int)position {#gotodir}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| DIR | bool |  | Rotation direction |
| position | int | -2097152-2097151 | Destination |

#### Executable timing

In motion start condition

#### Description

Moves to the specified position in the specified direction according to the pre-set speed profile. Remains in the BUSY state until it finishes moving to the specified position.

A position outside the range is not rejected. A position above 4,194,303 is limited to 4,194,303 by the driver library, which the driver reads as -1. Any other position is cut to its lower 22 bits and read as a signed number: 2,097,152 becomes -2,097,152 and -2,097,153 becomes 2,097,151.

#### Changes

- **v2.2.0**: On a busy motor, the STATUS register is read with GetParam, which does not clear the latched flags. Before, it was read with GetStatus, so the status poll could miss a flag and the report (`/overCurrent`, `/stall`, `/swEvent`, `/uvlo`, ...) was lost.

#### Errors

- `BrakeEngaged`: A motion command was sent while the electromagnetic brake was active. Also sent for `/enableServoMode 1` and `/homing` while the brake is engaged, releasing or engaging (not while stopping or after `/free`).
- `HomeSwActivating`: Movement from home switch position towards the origin point. Also sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. **v2.2.0**: Sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. It was sent as `HomeSwActivated` before.
- `LimitSwActivating`: Movement from limit switch position towards the opposite direction from origin.
- `InServoMode`: Received a command which can not be executed while servo mode. **v2.2.0**: Also sent for `/goUntil`, `/goUntilRaw` and `/releaseSw`.

#### See also

[`/goTo`](motor-control.md#goto), [`/combine/goToDir`](motor-control.md#combine-gotodir)
<!-- generated:end osc /goToDir -->

## Stops

<!-- osc: /softStop -->
<!-- generated:begin osc /softStop -->
### `/softStop` (int)motorID {#softstop}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

After decelerating according to the speed profile, the motor stops while it is kept excited. Remains in the BUSY state until the motor stops. If it was originally in the High Z state, the motor will be excited while it keeps its position.  
If it was in the servo mode, the mode will be released.

With the electromagnetic brake enabled, the command does nothing while the brake is engaged or after [`/free`](brake.md#free) (the motor is HiZ). During the deceleration of [`/softHiZ`](motor-control.md#softhiz) or `/activate 0` (brake state 3), the command is executed and cancels the engaging: the brake stays released (state 2).

#### Changes

- **v2.2.0**: With the brake enabled, does nothing while the brake is engaged or after `/free` (motor HiZ). Before, it energized the motor and left the brake state engaged, so `/activate 0` and `/hardHiZ` could not make the motor HiZ again.
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

#### See also

[`/combine/softStop`](motor-control.md#combine-softstop)
<!-- generated:end osc /softStop -->

<!-- osc: /hardStop -->
<!-- generated:begin osc /hardStop -->
### `/hardStop` (int)motorID {#hardstop}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Immediately stops the motor and leaves it excited. Remains in the BUSY state until the motor stops. If it was originally in the High Z state, the motor is excited while it keeps its position.  
If it was in the servo mode, the mode will be released.

With the electromagnetic brake enabled, the command does nothing while the brake is engaged or after [`/free`](brake.md#free) (the motor is HiZ). During the deceleration of [`/softHiZ`](motor-control.md#softhiz) or `/activate 0` (brake state 3), the command is executed and cancels the engaging: the brake stays released (state 2).

#### Changes

- **v2.2.0**: With the brake enabled, does nothing while the brake is engaged or after `/free` (motor HiZ). Before, it energized the motor and left the brake state engaged, so `/activate 0` and `/hardHiZ` could not make the motor HiZ again.
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

#### See also

[`/combine/hardStop`](motor-control.md#combine-hardstop)
<!-- generated:end osc /hardStop -->

<!-- osc: /softHiZ -->
<!-- generated:begin osc /softHiZ -->
### `/softHiZ` (int)motorID {#softhiz}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Decelerate according to the speed profile, then stop the motor and release excitation. When the excitation is released, it goes into the High Z state. It remains in the BUSY state until the motor is stopped.  
If it was in the servo mode, it will be released.  
if electromagnetic brake mode is enabled, the controller puts the brake into hold state, and then transits to High Z state.

#### Changes

- **v2.2.0**: With the brake enabled, on a stopped motor the brake is engaged at the next status read (up to 5 ms later). The stop is judged on a status read after the command.
- **v2.2.0**: A motion command (`/run`, `/move`, `/goTo`, ...) or `/activate 1` during the deceleration cancels the engaging; the brake stays released. Before, the brake engaged when the motor stopped later.
- **v2.2.0**: After `/free`, the brake is engaged at once (the motor is already HiZ).
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

#### See also

[`/combine/softHiZ`](motor-control.md#combine-softhiz), [`/enableElectromagnetBrake`](brake.md#enableelectromagnetbrake)
<!-- generated:end osc /softHiZ -->

<!-- osc: /hardHiZ -->
<!-- generated:begin osc /hardHiZ -->
### `/hardHiZ` (int)motorID {#hardhiz}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Immediately stops the motor and releases the stepper excitation. When the motor excitation is released, it goes into the High Z state. Remains in the BUSY state until the motor is stopped.  
If it was in the servo mode, it will be released.  
if electromagnetic brake mode is enabled, the controller puts the brake into hold state, and then transits to High Z state.

#### Changes

- **v2.2.0**: A single motor no longer sends a soft stop before the hard HiZ; a single motor, all motors (255) and `/combine/hardHiZ` behave the same. With the brake enabled and released (after `/activate 1`), the motor is stopped with a hard stop (still energized) before the brake is engaged, so it does not keep running during the brake transition time. While the brake is engaged or engaging, the command does nothing as before.
- **v2.2.0**: After `/free`, the brake is engaged at once (the motor is already HiZ).
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

#### See also

[`/combine/hardHiZ`](motor-control.md#combine-hardhiz), [`/enableElectromagnetBrake`](brake.md#enableelectromagnetbrake)
<!-- generated:end osc /hardHiZ -->

## Combined commands

<!-- osc: /combine/run -->
<!-- generated:begin osc /combine/run -->
### `/combine/run` (int)motorID1 (int)motorID2 (float)speed {#combine-run}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID1 | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| motorID2 | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| speed | float | -15625-15625 step/s | Rotation speed |

#### Executable timing

In motion start condition

#### Description

Same as [`/run`](motor-control.md#run) for two motors. The sign of the speed is the direction. A speed whose absolute value is above the range is limited to the largest register value (0xFFFFF, about 15625 step/s) by the driver library.

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
- `HomeSwActivating`: Movement from home switch position towards the origin point. Also sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. **v2.2.0**: Sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. It was sent as `HomeSwActivated` before.
- `LimitSwActivating`: Movement from limit switch position towards the opposite direction from origin.
- `InServoMode`: Received a command which can not be executed while servo mode. **v2.2.0**: Also sent for `/goUntil`, `/goUntilRaw` and `/releaseSw`.

#### See also

[`/run`](motor-control.md#run)
<!-- generated:end osc /combine/run -->

<!-- osc: /combine/move -->
<!-- generated:begin osc /combine/move -->
### `/combine/move` (int)motorID1 (int)motorID2 (int)step {#combine-move}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID1 | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| motorID2 | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| step | int |  | Moving step counts |

#### Executable timing

When the motor is stopped, In motion start condition

#### Description

Same as [`/move`](motor-control.md#move) for two motors. A step count whose absolute value is above 4,194,303 (22 bits) is not rejected: it is limited to 4,194,303 by the driver library.

#### Errors

- `BrakeEngaged`: A motion command was sent while the electromagnetic brake was active. Also sent for `/enableServoMode 1` and `/homing` while the brake is engaged, releasing or engaging (not while stopping or after `/free`).
- `HomeSwActivating`: Movement from home switch position towards the origin point. Also sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. **v2.2.0**: Sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. It was sent as `HomeSwActivated` before.
- `LimitSwActivating`: Movement from limit switch position towards the opposite direction from origin.
- `InServoMode`: Received a command which can not be executed while servo mode. **v2.2.0**: Also sent for `/goUntil`, `/goUntilRaw` and `/releaseSw`.

#### See also

[`/move`](motor-control.md#move)
<!-- generated:end osc /combine/move -->

<!-- osc: /combine/goTo -->
<!-- generated:begin osc /combine/goTo -->
### `/combine/goTo` (int)motorID1 (int)motorID2 (int)position {#combine-goto}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID1 | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| motorID2 | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| position | int | -2097152-2097151 | Destination |

#### Executable timing

In motion start condition

#### Description

Same as [`/goTo`](motor-control.md#goto) for two motors. A position outside the range is not rejected. A position above 4,194,303 is limited to 4,194,303 by the driver library, which the driver reads as -1. Any other position is cut to its lower 22 bits and read as a signed number: 2,097,152 becomes -2,097,152 and -2,097,153 becomes 2,097,151.

#### Changes

- **v2.2.0**: Judges its direction correctly when the home switch or the limit switch prohibits a motion ([`/setProhibitMotionOnHomeSw`](alarm-settings.md#setprohibitmotiononhomesw), [`/setProhibitMotionOnLimitSw`](alarm-settings.md#setprohibitmotiononlimitsw)): it is the sign of the 22-bit difference to the target, the way the driver goes (the shortest way). The direction was reversed for a target less than 2048 steps away (so a short move away from the switch was refused with `HomeSwActivating` / `LimitSwActivating` and a short move towards it was started), and wrong again beyond 2^21 steps.

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
- `HomeSwActivating`: Movement from home switch position towards the origin point. Also sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. **v2.2.0**: Sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. It was sent as `HomeSwActivated` before.
- `LimitSwActivating`: Movement from limit switch position towards the opposite direction from origin.
- `InServoMode`: Received a command which can not be executed while servo mode. **v2.2.0**: Also sent for `/goUntil`, `/goUntilRaw` and `/releaseSw`.

#### See also

[`/goTo`](motor-control.md#goto)
<!-- generated:end osc /combine/goTo -->

<!-- osc: /combine/goToDir -->
<!-- generated:begin osc /combine/goToDir -->
### `/combine/goToDir` (int)motorID1 (int)motorID2 (bool)DIR (int)position {#combine-gotodir}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID1 | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| motorID2 | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| DIR | bool |  | Rotation direction |
| position | int | -2097152-2097151 | Destination |

#### Executable timing

In motion start condition

#### Description

Same as [`/goToDir`](motor-control.md#gotodir) for two motors. A position outside the range is not rejected. A position above 4,194,303 is limited to 4,194,303 by the driver library, which the driver reads as -1. Any other position is cut to its lower 22 bits and read as a signed number: 2,097,152 becomes -2,097,152 and -2,097,153 becomes 2,097,151.

#### Errors

- `BrakeEngaged`: A motion command was sent while the electromagnetic brake was active. Also sent for `/enableServoMode 1` and `/homing` while the brake is engaged, releasing or engaging (not while stopping or after `/free`).
- `HomeSwActivating`: Movement from home switch position towards the origin point. Also sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. **v2.2.0**: Sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. It was sent as `HomeSwActivated` before.
- `LimitSwActivating`: Movement from limit switch position towards the opposite direction from origin.
- `InServoMode`: Received a command which can not be executed while servo mode. **v2.2.0**: Also sent for `/goUntil`, `/goUntilRaw` and `/releaseSw`.

#### See also

[`/goToDir`](motor-control.md#gotodir)
<!-- generated:end osc /combine/goToDir -->

<!-- osc: /combine/softStop -->
<!-- generated:begin osc /combine/softStop -->
### `/combine/softStop` (int)motorID1 (int)motorID2 {#combine-softstop}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID1 | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| motorID2 | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Same as [`/softStop`](motor-control.md#softstop) for two motors: it is handled as [`/softStop`](motor-control.md#softstop) for motorID1 and then for motorID2.

#### Changes

- **v2.2.0**: Cancels pending motion like [`/softStop`](motor-control.md#softstop) (each of the two motors is handled as a separate [`/softStop`](motor-control.md#softstop)), also for a motor with the brake disabled.

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

#### See also

[`/softStop`](motor-control.md#softstop)
<!-- generated:end osc /combine/softStop -->

<!-- osc: /combine/hardStop -->
<!-- generated:begin osc /combine/hardStop -->
### `/combine/hardStop` (int)motorID1 (int)motorID2 {#combine-hardstop}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID1 | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| motorID2 | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Same as [`/hardStop`](motor-control.md#hardstop) for two motors: it is handled as [`/hardStop`](motor-control.md#hardstop) for motorID1 and then for motorID2.

#### Changes

- **v2.2.0**: Cancels pending motion like [`/hardStop`](motor-control.md#hardstop) (each of the two motors is handled as a separate [`/hardStop`](motor-control.md#hardstop)), also for a motor with the brake disabled.

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

#### See also

[`/hardStop`](motor-control.md#hardstop)
<!-- generated:end osc /combine/hardStop -->

<!-- osc: /combine/softHiZ -->
<!-- generated:begin osc /combine/softHiZ -->
### `/combine/softHiZ` (int)motorID1 (int)motorID2 {#combine-softhiz}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID1 | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| motorID2 | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Same as [`/softHiZ`](motor-control.md#softhiz) for two motors: it is handled as [`/softHiZ`](motor-control.md#softhiz) for motorID1 and then for motorID2.

#### Changes

- **v2.2.0**: Cancels pending motion like [`/softHiZ`](motor-control.md#softhiz) (each of the two motors is handled as a separate [`/softHiZ`](motor-control.md#softhiz)), also for a motor with the brake disabled.

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

#### See also

[`/softHiZ`](motor-control.md#softhiz)
<!-- generated:end osc /combine/softHiZ -->

<!-- osc: /combine/hardHiZ -->
<!-- generated:begin osc /combine/hardHiZ -->
### `/combine/hardHiZ` (int)motorID1 (int)motorID2 {#combine-hardhiz}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID1 | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| motorID2 | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Same as [`/hardHiZ`](motor-control.md#hardhiz) for two motors: it is handled as [`/hardHiZ`](motor-control.md#hardhiz) for motorID1 and then for motorID2.

#### Changes

- **v2.2.0**: Cancels pending motion like [`/hardHiZ`](motor-control.md#hardhiz) (each of the two motors is handled as a separate [`/hardHiZ`](motor-control.md#hardhiz)), also for a motor with the brake disabled.

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

#### See also

[`/hardHiZ`](motor-control.md#hardhiz)
<!-- generated:end osc /combine/hardHiZ -->

## Raw register value commands

The following commands specify the speed with the register value of the driver IC, without unit conversion.

<!-- osc: /runRaw -->
<!-- generated:begin osc /runRaw -->
### `/runRaw` (int)motorID (int)speed {#runraw}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| speed | int |  | Rotation speed (raw register value, signed) |

#### Executable timing

In motion start condition

#### Description

Rotates the motor at the specified speed using a raw register value. The sign of the speed value determines the direction.

A speed outside the 20-bit range is limited to 20 bits by the driver.

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
- `HomeSwActivating`: Movement from home switch position towards the origin point. Also sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. **v2.2.0**: Sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. It was sent as `HomeSwActivated` before.
- `LimitSwActivating`: Movement from limit switch position towards the opposite direction from origin.
- `InServoMode`: Received a command which can not be executed while servo mode. **v2.2.0**: Also sent for `/goUntil`, `/goUntilRaw` and `/releaseSw`.

#### See also

[`/run`](motor-control.md#run), [`/combine/runRaw`](motor-control.md#combine-runraw)
<!-- generated:end osc /runRaw -->

<!-- osc: /goUntilRaw -->
<!-- generated:begin osc /goUntilRaw -->
### `/goUntilRaw` (int)motorID (bool)ACT (int)speed {#gountilraw}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| ACT | bool |  | Same as `/goUntil` |
| speed | int |  | Speed (raw register value, signed) |

#### Executable timing

Always

#### Description

Same as `/goUntil` but uses a raw register value for speed. The sign of the speed value determines the direction.

The speed is limited to 20 bits (0xFFFFF) by the firmware and the driver libraries. `/goUntilRaw 255` (all motors) interprets the speed as a raw register value, like for a single motor.

#### Changes

- **v2.2.0**: Limits the speed to 20 bits (`0xFFFFF`), like [`/runRaw`](motor-control.md#runraw). Larger values were sent as is, and the driver ignored the upper bits.
- **v2.2.0**: `/goUntilRaw 255` (all motors) interprets the speed as a raw register value, like for a single motor. It was treated as steps/s.
- **v2.2.0**: An activated home switch is reported as `/error/command HomeSwActivating`, the text in the error list. It was sent as `HomeSwActivated`. It now follows [`/reportError`](system-settings.md#reporterror) like the other command errors.
- **v2.2.0**: For a motor in the servo mode, replies `/error/command InServoMode` and does nothing. Before, the command was sent to the driver. With 255, only the motors in the servo mode reply the error; the others execute the command.

#### Errors

- `BrakeEngaged`: A motion command was sent while the electromagnetic brake was active. Also sent for `/enableServoMode 1` and `/homing` while the brake is engaged, releasing or engaging (not while stopping or after `/free`).
- `GoUntilTimeout`: Timeout while executing `/goUntil` command.
- `HomeSwActivating`: Movement from home switch position towards the origin point. Also sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. **v2.2.0**: Sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. It was sent as `HomeSwActivated` before.
- `InServoMode`: Received a command which can not be executed while servo mode. **v2.2.0**: Also sent for `/goUntil`, `/goUntilRaw` and `/releaseSw`.

#### See also

[`/goUntil`](homing.md#gountil)
<!-- generated:end osc /goUntilRaw -->

<!-- osc: /combine/runRaw -->
<!-- generated:begin osc /combine/runRaw -->
### `/combine/runRaw` (int)motorID1 (int)motorID2 (int)speed {#combine-runraw}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID1 | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| motorID2 | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| speed | int |  | Rotation speed (raw register value, signed) |

#### Executable timing

In motion start condition

#### Description

A speed outside the 20-bit range is limited to 20 bits by the driver.

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
- `HomeSwActivating`: Movement from home switch position towards the origin point. Also sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. **v2.2.0**: Sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. It was sent as `HomeSwActivated` before.
- `LimitSwActivating`: Movement from limit switch position towards the opposite direction from origin.
- `InServoMode`: Received a command which can not be executed while servo mode. **v2.2.0**: Also sent for `/goUntil`, `/goUntilRaw` and `/releaseSw`.

#### See also

[`/runRaw`](motor-control.md#runraw)
<!-- generated:end osc /combine/runRaw -->
