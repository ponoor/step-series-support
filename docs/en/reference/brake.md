---
title: Electromagnetic brake
---

# Electromagnetic brake

For how the electromagnetic brake works, see [Electromagnetic brake](../guides/electromagnetic-brake.md).

<!-- osc: /enableElectromagnetBrake -->
<!-- generated:begin osc /enableElectromagnetBrake -->
### `/enableElectromagnetBrake` (int)motorID (bool)enable {#enableelectromagnetbrake}

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

Enables / disables electromagnetic brake mode.  
While in the mode, the controller replies the `BrakeEngaged` ([`/error/command`](automatically-sent-messages.md#error-command)) if motor movement command is sent without releasing the electromagnetic brake.

The setting is changed only while the driver is HiZ, and the brake is disabled only while it is engaged or after [`/free`](brake.md#free); otherwise the command replies `CommandIgnored`. Sending the current value does nothing. After a change, the brake output is engaged and the brake state is engaged. The same rule applies to a configuration loaded over USB serial (a warning is printed for a motor that is not changed).

#### Changes

- **v2.2.0**: Changes the setting only while the driver is HiZ, and disables the brake only while it is engaged or after `/free`; otherwise `/error/command CommandIgnored`. Sending the current value does nothing. After a change the brake output is engaged and the state is engaged. Before, disabling a released brake engaged it on a turning motor, and enabling it on an energized motor left a state where `/activate 0` and `/hardHiZ` did nothing.

#### Errors

- `CommandIgnored`: The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`).

#### Initial value

- `enable`: false (Disable) ([driverSettings.electromagnetBrakeEnable](../connections/configuration-items.md#driversettings-electromagnetbrakeenable))

#### See also

[`/activate`](brake.md#activate), [`/free`](brake.md#free), [`/setBrakeTransitionDuration`](brake.md#setbraketransitionduration), [`/getBrakeStatus`](brake.md#getbrakestatus)
<!-- generated:end osc /enableElectromagnetBrake -->

<!-- osc: /activate -->
<!-- generated:begin osc /activate -->
### `/activate` (int)motorID (bool)state {#activate}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| state | bool |  |  |

`state`

| Value | Meaning |
| --- | --- |
| 1 | Motor excited, EM brake released |
| 0 | Motor not excited, EM brake engaged |

#### Executable timing

Always

#### Description

Switches motor excitation / release when electromagnetic brake mode is enabled. The electromagnetic brake (EM) also works conjunction with the motor. You cannot send motor movement command when the motor is not excited by this command.  
If the EM mode is disabled, this command is ignored: only `CommandIgnored` is sent, and pending motion is not cancelled.

`/activate 1` while the brake is released does nothing. From the engaged state it energizes the driver and releases the brake after `brakeTransitionDuration`, but only if a status read after the command shows the driver energized (during the engaging it goes back to the release sequence (the transition time starts again), during the stopping it only cancels the engaging, after [`/free`](brake.md#free) it releases at once). If the driver stays HiZ (for example without motor power), the brake stays engaged and `BrakeReleaseFailed` is sent.

`/activate 0` on a turning motor decelerates it and engages the brake when it has stopped, like [`/softHiZ`](motor-control.md#softhiz); on a stopped motor the brake is engaged at the next status read (up to 5 ms later). The driver goes HiZ after `brakeTransitionDuration`. The brake state can be read with [`/getBrakeStatus`](brake.md#getbrakestatus).

#### Changes

- **v2.2.0**: `/activate 1` while the brake is released does nothing. Before, it sent a hard stop, which stopped a turning motor abruptly.
- **v2.2.0**: `/activate 1` releases the brake only if a status read after the command shows the driver energized. If the driver stays HiZ (e.g. no motor power), the brake stays engaged and `/error/command BrakeReleaseFailed motorID` is sent. Before, the brake was released after `brakeTransitionDuration` in any case.
- **v2.2.0**: `/activate 1` during the deceleration of `/softHiZ` (or `/activate 0`) cancels the engaging and keeps the brake released; the deceleration goes on. Before, it stopped the motor with a hard stop, and the brake still engaged when the motor stopped.
- **v2.2.0**: `/activate 0` on a turning motor decelerates it and engages the brake when it has stopped, like `/softHiZ`. Before, it engaged the brake without stopping the motor.
- **v2.2.0**: `/activate 0` on a stopped motor engages the brake at the next status read (up to 5 ms later). The stop is now judged on a status read after the command.
- **v2.2.0**: After `/free`: `/activate 1` returns the motor to the released (energized) state, and `/activate 0` engages the brake at once (the motor is already HiZ).
- **v2.2.0**: KVAL_HOLD (TVAL_HOLD in the current mode) is raised to at least half of KVAL_RUN (TVAL_RUN) whenever the motor is energized again: from engaged or engaging (as before), and now also after `/free`.
- **v2.2.0**: `/activate 0` cancels pending motion of a motor with the brake enabled (with the brake disabled it replies `CommandIgnored` and cancels nothing): a `/goTo`, `/goToDir`, `/goHome` or `/goMark` waiting for the BUSY flag to clear (it was sent when the motor became not busy, so a stopped motor started again), the homing (its timeout sent a hard stop, which energized a motor made HiZ in the meantime) and the servo mode.

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

- `CommandIgnored`: The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`).
- `BrakeReleaseFailed`: `/activate 1` was sent but the driver stayed HiZ (for example without motor power), so the brake stays engaged. Added in v2.2.0.

#### See also

[`/enableElectromagnetBrake`](brake.md#enableelectromagnetbrake), [`/free`](brake.md#free), [`/getBrakeStatus`](brake.md#getbrakestatus)
<!-- generated:end osc /activate -->

<!-- osc: /free -->
<!-- generated:begin osc /free -->
### `/free` (int)motorID {#free}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Releases motor axis when the electromagnetic brake mode is active. It releases motor excitation and keep EM brake in release state.  
Be cautious when sending this command. If some load is hanged to the motor, it will loose the hold and the load may fall down.  
If the EM mode is disabled, this command is ignored: only `CommandIgnored` is sent, and pending motion is not cancelled.

After `/free`, a stop of the motor no longer engages the brake (when `/free` was sent during the deceleration of [`/softHiZ`](motor-control.md#softhiz)). A motion command (`/run`, `/move`, `/goTo`, ...) or `/activate 1` energizes the motor again and returns it to the released state. `/activate 0`, `/softHiZ` and `/hardHiZ` engage the brake at once.

#### Changes

- **v2.2.0**: After `/free`, a stop of the motor no longer engages the brake (when `/free` was sent during the deceleration of `/softHiZ`).
- **v2.2.0**: After `/free`, a motion command (`/run`, `/move`, `/goTo`, ...) is executed and the motor returns to the released (energized) state. `/activate 1` does the same. `/activate 0`, `/softHiZ` and `/hardHiZ` engage the brake at once (the motor is already HiZ).
- **v2.2.0**: KVAL_HOLD (TVAL_HOLD in the current mode) is raised to at least half of KVAL_RUN (TVAL_RUN) when the motor is energized again after `/free`. Before, the motor was energized with the configured holding value.
- **v2.2.0**: `/free` cancels pending motion of a motor with the brake enabled (with the brake disabled it replies `CommandIgnored`): a `/goTo`, `/goToDir`, `/goHome` or `/goMark` waiting for the BUSY flag to clear (it was sent when the motor became not busy, so a stopped motor started again), the homing (its timeout sent a hard stop, which energized a motor made HiZ in the meantime) and the servo mode.

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

- `CommandIgnored`: The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`).

#### See also

[`/enableElectromagnetBrake`](brake.md#enableelectromagnetbrake), [`/activate`](brake.md#activate), [`/getBrakeStatus`](brake.md#getbrakestatus)
<!-- generated:end osc /free -->

<!-- osc: /setBrakeTransitionDuration -->
<!-- generated:begin osc /setBrakeTransitionDuration -->
### `/setBrakeTransitionDuration` (int)motorID (int)duration {#setbraketransitionduration}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| duration | int | 0-65535 ms | Transition duration |

#### Executable timing

Always

#### Description

Sets the transitional duration to keep the motor excited when the electromagnetic brake is activated or released. This is to keep holding the motor axis until the brake movement is completed, due to the physical transition time for the brake mechanism.

A value outside 0-65535 replies `CommandIgnored` and the setting is kept. The release after [`/activate`](brake.md#activate) comes 0-5 ms after the set time, because the brake is handled every 5 ms.

#### Changes

- **v2.2.0**: A value outside 0-65535 replies `/error/command CommandIgnored` and keeps the setting. Before, the value was taken as a 16-bit unsigned integer, so only its lower 16 bits were used (65536 became 0, -1 became 65535).
- **v2.2.0**: The brake times are in 5 ms steps: the release after `/activate 1` comes 0-5 ms after `brakeTransitionDuration` (measured 99.8-105.4 ms for 100 ms; before 99.8-107.6 ms), and the engage after a stop or a HiZ is judged at the next status read.

#### Errors

- `CommandIgnored`: The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`).

#### Initial value

- `duration`: 100 ([driverSettings.brakeTransitionDuration](../connections/configuration-items.md#driversettings-braketransitionduration))

#### See also

[`/getBrakeTransitionDuration`](brake.md#getbraketransitionduration)
<!-- generated:end osc /setBrakeTransitionDuration -->

<!-- osc: /getBrakeTransitionDuration -->
<!-- generated:begin osc /getBrakeTransitionDuration -->
### `/getBrakeTransitionDuration` (int)motorID {#getbraketransitionduration}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Returns the transitional duration to keep holding the motor axis when the electromagnetic brake is activated or released.

#### Response

```
/brakeTransitionDuration (int)motorID (int)duration
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| duration | int | 0-65535 ms | Transitional duration |
<!-- generated:end osc /getBrakeTransitionDuration -->

<!-- osc: /getBrakeStatus -->
<!-- generated:begin osc /getBrakeStatus -->
### `/getBrakeStatus` (int)motorID {#getbrakestatus}

Added in v2.2.0.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Returns the state of the electromagnetic brake of the specified motor. The state is -1 for a motor with the brake disabled.

#### Response

Added in v2.2.0.

```
/brakeStatus (int)motorID (int)state
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| state | int |  | State of the brake |

`state`

| Value | Meaning |
| --- | --- |
| -1 | The electromagnetic brake is disabled for the motor |
| 0 | Engaged. Brake output: engaged. Driver: HiZ |
| 1 | Releasing (`/activate 1`, waiting `brakeTransitionDuration`). Brake output: engaged. Driver: energized |
| 2 | Released. Brake output: released. Driver: energized |
| 3 | Stopping (`/softHiZ`, `/activate 0`: decelerating, engages when stopped). Brake output: released. Driver: energized |
| 4 | Engaging (waiting `brakeTransitionDuration`, then HiZ). Brake output: engaged. Driver: energized |
| 5 | Free (`/free`). Brake output: released. Driver: HiZ |

##### Description

Reply to `/getBrakeStatus`. The state numbers are part of the specification; new states will only be added as 6, 7, ....

#### See also

[`/activate`](brake.md#activate), [`/free`](brake.md#free), [`/enableElectromagnetBrake`](brake.md#enableelectromagnetbrake)
<!-- generated:end osc /getBrakeStatus -->
