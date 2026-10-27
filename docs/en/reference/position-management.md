---
title: Position management
---

# Position management

For how the position is managed, see [Homing and position](../guides/homing-and-position.md).

## Position

<!-- osc: /setPosition -->
<!-- generated:begin osc /setPosition -->
### `/setPosition` (int)motorID (int)newPosition {#setposition}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| newPosition | int | -2097152-2097151 | specified coordinates |

#### Executable timing

When the motor is stopped

#### Description

Rewrites ABS_POS register to the specified coordinates. The current motor position is set to the specified coordinates.

Do not use it while the motor is running or in the servo mode. There is no guard: if the driver refuses the write, `CommandIgnored` is sent.

A value outside the range is not rejected: the driver truncates it to 22 bits.

#### Errors

- `CommandIgnored`: The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`).

#### See also

[`/getPosition`](position-management.md#getposition), [`/resetPos`](position-management.md#resetpos)
<!-- generated:end osc /setPosition -->

<!-- osc: /getPosition -->
<!-- generated:begin osc /getPosition -->
### `/getPosition` (int)motorID {#getposition}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Returns the contents of the ABS_POS register (current position).  
[`/setPositionReportInterval`](motor-driver-settings.md#setpositionreportinterval) can make the controller to send this message with a specified interval.

#### Response

[`/position`](automatically-sent-messages.md#position)

```
/position (int)motorID (int)ABS_POS
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| ABS_POS | int | -2097152-2097151 | current position |
<!-- generated:end osc /getPosition -->

<!-- osc: /getPositionList -->
<!-- generated:begin osc /getPositionList -->
### `/getPositionList` {#getpositionlist}

#### Argument

None

#### Executable timing

Always

#### Description

Returns the current position of all motors at once. `/getPosition 255` returns individual messages for each motor but this command returns single message with a position list.  
[`/setPositionListReportInterval`](motor-driver-settings.md#setpositionlistreportinterval) can make the controller to send this list with a specified interval.

#### Response

[`/positionList`](automatically-sent-messages.md#positionlist)

```
/positionList (int)position1 ... (int)positionN
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| position1 ... positionN | int | -2097152-2097151 | current position of the motor #n |

#### See also

[`/getPosition`](position-management.md#getposition)
<!-- generated:end osc /getPositionList -->

<!-- osc: /resetPos -->
<!-- generated:begin osc /resetPos -->
### `/resetPos` (int)motorID {#resetpos}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Reset ABS_POS register to 0.

Do not use it while the motor is running or in the servo mode. There is no guard: if the driver refuses the write, `CommandIgnored` is sent.

#### Errors

- `CommandIgnored`: The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`).

#### See also

[`/setPosition`](position-management.md#setposition)
<!-- generated:end osc /resetPos -->

<!-- osc: /setElPos -->
<!-- generated:begin osc /setElPos -->
### `/setElPos` (int)motorID (int)newFullstep (int)newMicrostep {#setelpos}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| newFullstep | int | 0-3 | Fullstep position |
| newMicrostep | int | 0-127 | Microstep position |

#### Executable timing

When the motor is stopped

#### Description

Set the electrical position of the motor. The microstep is expressed in step/128, and the value has to be matched with the current microstep mode.

Use it while the motor is HiZ. There is no guard on the motor state: the L6470 also refuses the write while the motor is stopped and energized (which the datasheet allows), and then `CommandIgnored` is sent.

A full step outside 0-3 or a microstep outside 0-127 replies `CommandIgnored` and nothing is applied.

#### Changes

- **v2.2.0**: A full step outside 0-3 or a microstep outside 0-127 replies `/error/command CommandIgnored` and nothing is applied. Before, they were clamped.

#### Errors

- `CommandIgnored`: The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`).

#### See also

[`/getElPos`](position-management.md#getelpos)
<!-- generated:end osc /setElPos -->

<!-- osc: /getElPos -->
<!-- generated:begin osc /getElPos -->
### `/getElPos` (int)motorID {#getelpos}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Returns the current electrical position of the motor.

#### Response

```
/elPos (int)motorID (int)fullstep (int)microstep
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| fullstep | int | 0-3 | Fullstep position |
| microstep | int | 0-127 | Microstep position |
<!-- generated:end osc /getElPos -->

## HOME/MARK

<!-- osc: /setMark -->
<!-- generated:begin osc /setMark -->
### `/setMark` (int)motorID (int)MARK {#setmark}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| MARK | int |  | Coordination to be set |

#### Executable timing

Always

#### Description

Set the MARK register to arbitrary position.

A value outside the range is not rejected: the driver truncates it to 22 bits.

#### See also

[`/getMark`](position-management.md#getmark), [`/goMark`](position-management.md#gomark)
<!-- generated:end osc /setMark -->

<!-- osc: /getMark -->
<!-- generated:begin osc /getMark -->
### `/getMark` (int)motorID {#getmark}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Get the MARK position.

#### Response

```
/mark (int)motorID (int)MARK
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| MARK | int |  | Position of the MARK |
<!-- generated:end osc /getMark -->

<!-- osc: /goHome -->
<!-- generated:begin osc /goHome -->
### `/goHome` (int)motorID {#gohome}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

In motion start condition

#### Description

Move the motor to the HOME position (zero position) according to the speed profile.

#### Changes

- **v2.2.0**: Judges its direction correctly when the home switch or the limit switch prohibits a motion ([`/setProhibitMotionOnHomeSw`](alarm-settings.md#setprohibitmotiononhomesw), [`/setProhibitMotionOnLimitSw`](alarm-settings.md#setprohibitmotiononlimitsw)): it is the sign of the 22-bit difference to the target, the way the driver goes (the shortest way). The direction was reversed for a target less than 2048 steps away (so a short move away from the switch was refused with `HomeSwActivating` / `LimitSwActivating` and a short move towards it was started), and wrong again beyond 2^21 steps.
- **v2.2.0**: On a busy motor, the STATUS register is read with GetParam, which does not clear the latched flags. Before, it was read with GetStatus, so the status poll could miss a flag and the report (`/overCurrent`, `/stall`, `/swEvent`, `/uvlo`, ...) was lost.

#### Errors

- `BrakeEngaged`: A motion command was sent while the electromagnetic brake was active. Also sent for `/enableServoMode 1` and `/homing` while the brake is engaged, releasing or engaging (not while stopping or after `/free`).
- `HomeSwActivating`: Movement from home switch position towards the origin point. Also sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. **v2.2.0**: Sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. It was sent as `HomeSwActivated` before.
- `LimitSwActivating`: Movement from limit switch position towards the opposite direction from origin.
- `InServoMode`: Received a command which can not be executed while servo mode. **v2.2.0**: Also sent for `/goUntil`, `/goUntilRaw` and `/releaseSw`.
<!-- generated:end osc /goHome -->

<!-- osc: /goMark -->
<!-- generated:begin osc /goMark -->
### `/goMark` (int)motorID {#gomark}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

In motion start condition

#### Description

Move the motor to the MARK position according to the speed profile.

#### Changes

- **v2.2.0**: Judges its direction correctly when the home switch or the limit switch prohibits a motion ([`/setProhibitMotionOnHomeSw`](alarm-settings.md#setprohibitmotiononhomesw), [`/setProhibitMotionOnLimitSw`](alarm-settings.md#setprohibitmotiononlimitsw)): it is the sign of the 22-bit difference to the target, the way the driver goes (the shortest way). The direction was reversed for a target less than 2048 steps away (so a short move away from the switch was refused with `HomeSwActivating` / `LimitSwActivating` and a short move towards it was started), and wrong again beyond 2^21 steps.
- **v2.2.0**: On a busy motor, the STATUS register is read with GetParam, which does not clear the latched flags. Before, it was read with GetStatus, so the status poll could miss a flag and the report (`/overCurrent`, `/stall`, `/swEvent`, `/uvlo`, ...) was lost.

#### Errors

- `BrakeEngaged`: A motion command was sent while the electromagnetic brake was active. Also sent for `/enableServoMode 1` and `/homing` while the brake is engaged, releasing or engaging (not while stopping or after `/free`).
- `HomeSwActivating`: Movement from home switch position towards the origin point. Also sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. **v2.2.0**: Sent by `/goUntil` and `/goUntilRaw` when the home switch is already activated. It was sent as `HomeSwActivated` before.
- `LimitSwActivating`: Movement from limit switch position towards the opposite direction from origin.
- `InServoMode`: Received a command which can not be executed while servo mode. **v2.2.0**: Also sent for `/goUntil`, `/goUntilRaw` and `/releaseSw`.

#### See also

[`/setMark`](position-management.md#setmark)
<!-- generated:end osc /goMark -->
