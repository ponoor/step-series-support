---
title: Electromagnetic brake
---

# Electromagnetic brake

An electromagnetic brake locks the shaft of the motor when it is not powered. This page explains how the board controls the brake together with the motor: the states of the brake, what each command does to it, and what you must know before you hang a load on the motor.

## What an electromagnetic brake is {#what}

Some stepper motors have an electromagnetic brake built in. A stepper motor keeps a holding torque while it is stopped and energized. If the power is lost, the torque is lost, and a suspended load moves or falls. The brake locks the shaft when its power is off (or when you command it) and releases the shaft when it is powered. It is needed especially when a load is moved up and down.

The board controls the brake output of each motor on its own. It supports the STEP400 with the EMB-STEP400 brake board and the brake outputs of the STEP800. For the wiring, see [Electromagnetic brake connection](../connections/electromagnetic-brake-wiring.md#overview). For the specifications of the brake board, see [EMB-STEP400](../hardware/emb-step400.md#specifications).

## Enabling the brake {#enable}

Enable the brake of a motor with [`/enableElectromagnetBrake`](../reference/brake.md#enableelectromagnetbrake) or with [`driverSettings.electromagnetBrakeEnable`](../connections/configuration-items.md#driversettings-electromagnetbrakeenable) in the configuration. While the brake is enabled, the board releases the brake when the motor is energized and engages it when the motor is not energized, by itself. A motor whose brake is not enabled is not affected by anything on this page.

The setting can be changed only while the driver is HiZ and, to disable the brake, only while it is engaged or after `/free`; otherwise the board replies `CommandIgnored`.

## States of the brake {#states}

The brake of each motor is in one of six states. [`/getBrakeStatus`](../reference/brake.md#getbrakestatus) returns the number. The numbers are part of the specification; new states will only be added as 6, 7, ...  A motor whose brake is disabled has the state -1.

| State | Name | Brake output | Driver | Meaning |
| --- | --- | --- | --- | --- |
| 0 | Engaged | engaged | HiZ | The brake holds the shaft. The motor is not energized. |
| 1 | Releasing | engaged | energized | `/activate 1` was sent. The board waits for the transition duration, then releases the brake. |
| 2 | Released | released | energized | The motor is energized and the shaft is free. Motion commands are accepted. |
| 3 | Stopping | released | energized | `/softHiZ` or `/activate 0` is decelerating the motor. When the motor has stopped, the brake is engaged. |
| 4 | Engaging | engaged | energized | The brake is engaged and the motor is still energized. After the transition duration the driver goes HiZ. |
| 5 | Free | released | HiZ | `/free` was sent. The brake is released and the motor is not energized. |

### How the state changes {#transitions}

Besides the commands (see below), the board changes the state by itself. It reads the state of the driver every 5 ms and decides at that moment:

| From | When | To |
| --- | --- | --- |
| Releasing | the driver is energized and the transition duration has passed | Released (the brake output is released) |
| Releasing | the driver is HiZ (for example the motor has no power) | Engaged, and `/error/command BrakeReleaseFailed` |
| Stopping | the motor has stopped | Engaging |
| Engaging | the transition duration has passed, or the driver is found HiZ | Engaged (the driver is made HiZ in the first case) |
| Released, Stopping | the driver went HiZ by itself (overcurrent, overtemperature, UVLO) | Engaged at once, and `/error/command BrakeEngagedOnHiZ`. Pending motions are cancelled. |

Because the state is read every 5 ms, a transition happens up to 5 ms after the command.

## Commands and the brake {#commands}

This is what each command does to a motor with the brake enabled. "Nothing" means that the command is not executed and no error is sent.

| Command | Engaged (0) | Releasing (1) | Released (2) | Stopping (3) | Engaging (4) | Free (5) |
| --- | --- | --- | --- | --- | --- | --- |
| `/activate 1` | energizes the driver, then Releasing | nothing | nothing | cancels the engaging, Released; the deceleration goes on | back to Releasing (the wait starts again) | energizes the driver, Released |
| `/activate 0`, `/softHiZ` | nothing | Engaging | decelerates the motor, Stopping | nothing | nothing | Engaged |
| `/hardHiZ` | nothing | Engaging | stops the motor at once, Engaging | stops the motor at once, Engaging | nothing | Engaged |
| `/free` | HiZ with the brake released, Free | same | same | same | same | nothing |
| Motion commands (`/run`, `/move`, `/goTo`, ..., `/homing`, `/enableServoMode 1`) | `BrakeEngaged` | `BrakeEngaged` | executed | executed, Released (the engaging is cancelled) | `BrakeEngaged` | executed, the motor is energized, Released |
| `/softStop`, `/hardStop`, `/enableServoMode 0` | nothing | executed | executed | executed, Released (the engaging is cancelled) | executed | nothing |
| `/resetMotorDriver` | executed | `CommandIgnored` | `CommandIgnored` | `CommandIgnored` | `CommandIgnored` | executed |

A motion command while the brake is engaged is rejected with `BrakeEngaged`; this is part of the [motion start condition](../reference/index.md#motion-start-condition).

The commands for all motors (255) and the combined commands (`/combine/...`) act on each motor like this.

### Stopping a motor that is going to engage the brake {#stopping}

While the motor decelerates after `/softHiZ` or `/activate 0` (state Stopping), **the command that arrived last wins**:

- `/softStop`, `/hardStop` and `/enableServoMode 0` cancel the plan to engage the brake. The state returns to Released and the motor stops and stays energized. These commands mean "stop and hold", so they override the earlier "stop and engage the brake". If you want the brake after that, send `/softHiZ`, `/activate 0` or `/hardHiZ` again.
- `/hardHiZ` does not cancel the plan: it stops the motor at once and engages the brake.
- `/softHiZ` and `/activate 0` do nothing: the deceleration and the plan go on.
- A motion command and `/activate 1` also cancel the plan; the brake stays released.

The same happens for a motor whose brake is not enabled: a `/softStop` sent during the deceleration of a `/softHiZ` leaves the motor energized.

## Transition duration {#transition-duration}

The brake needs a short time to work mechanically, so the motor and the brake must hold the shaft together for a while. The **transition duration** ([`/setBrakeTransitionDuration`](../reference/brake.md#setbraketransitionduration), [`driverSettings.brakeTransitionDuration`](../connections/configuration-items.md#driversettings-braketransitionduration)) is this overlap:

- To release: the board energizes the motor, waits for the transition duration, then releases the brake.
- To engage: the board engages the brake, waits for the transition duration, then makes the motor HiZ.

[![Brake transition duration](https://ponoor.com/cms/wp-content/uploads/2021/03/brakeTransition.png)](https://ponoor.com/cms/wp-content/uploads/2021/03/brakeTransition.png)

The duration does not change how long the brake takes to lock; it changes how long the board waits before it makes the motor HiZ or releases the brake. The wait is counted in 5 ms steps, so the actual time is 0 to 5 ms longer than the setting.

We do not give a recommended value: it depends on the response time of your brake, on the load and on the device. Set a value that is the release and engage time in the specification of the brake plus a margin. See [`/setBrakeTransitionDuration`](../reference/brake.md#setbraketransitionduration) for the initial value and the range.

## Holding current {#hold-current}

When a motor with the brake enabled is energized again (`/activate 1`, and a motion command after `/free`), KVAL_HOLD (TVAL_HOLD in current mode) is raised to at least half of KVAL_RUN (TVAL_RUN), so that the motor holds the load while the brake is released. [`/getKval`](../reference/voltage-and-current-mode-settings.md#getkval) returns the raised value. See [Voltage mode and current mode](voltage-and-current-mode.md#kval-tval).

## Restart, watchdog and CPU fault {#restart}

The board engages the brakes before it restarts, whatever the reason:

- **[`/resetDevice`](../reference/system-settings.md#resetdevice) and the `R` command of the USB serial port**: the board stops the motors that are turning with a hard stop, engages their brakes, waits for the longest transition duration of them (at most 1 s), and then restarts.
- **Watchdog**: when the processing stops for about 250 ms, the board engages every brake, waits for the longest transition duration (at most 1 s), and then the watchdog restarts the board. Nothing is sent to the drivers; a turning motor is stopped by the brake. `/booted` reports the reset cause 4.
- **CPU fault** (an exception of the CPU): the board engages every brake at once, waits in the same way, and restarts. `/booted` reports the reset cause 6.

The reset cause is the second argument of [`/booted`](../reference/automatically-sent-messages.md#booted); see there for the numbers.

When the USB cable is pulled out while the Ethernet cable is connected, the STEP400 (R1 board) can restart (a hardware problem). The brakes are engaged first, but pull the cable out only while the motors are stopped.

## When the load is not held {#unsupported}

The firmware cannot prevent these times in which the load is not held:

- **Power-on of the STEP800**: all the brakes stay released for about 250 ms after the power is applied, mostly the time of the bootloader. **Depending on the power supply and the conditions, it can be longer: with 24 V, the brakes stayed released for about 2 s in a measurement.** This depends on the hardware, not on the firmware.
- **The reset button and a drop of the supply voltage**: the drivers are in standby and the brakes (STEP800) stay released for about 0.5 s, until the firmware starts.
- On the STEP400 with the EMB-STEP400, the brakes engage at once also at a reset (the brake board pulls them down).
- Even when the brake is engaged electrically first, the shaft is held only after the brake has locked mechanically, which takes tens of ms.

If you hang a load on the motor, take these times into account.

## Usage notes {#usage}

- **Take the power of the brake from the same power supply as the motor, or from a supply that is cut together with the power of the motor.** Do not let only the power of the motor be cut first: the holding force is then lost before the undervoltage lockout acts, and the load falls. The brake and the motor can use different voltages (for example, a 48 V motor and a 24 V brake); in that case, make the brake supply follow the motor supply.
- **Do homing again after a restart, and after the motor has been HiZ.** The position is not reliable: after the motor is energized again, the first release of the brake can shift the shaft. See [Homing and position management](homing-and-position.md).
- **`/free` is for maintenance.** It releases the motor and keeps the brake released, so a load that hangs on the motor falls. Be very careful with this command; make the load safe before you send it.
- The motor turns only when the brake is released: see the motion start condition above.
- For the driver that goes HiZ by itself, the board engages the brake (`BrakeEngagedOnHiZ`); see [Alarms and protection](alarms-and-protection.md#hiz-by-itself).

## Examples of motors with an electromagnetic brake {#examples}

[![Stepper motor with brake](https://ponoor.com/cms/wp-content/uploads/2021/03/nema-23-stepper-19nm269ozin-w-brake-friction-torque-20nm283ozin-52372-1000x1000-1.jpg)](https://ponoor.com/cms/wp-content/uploads/2021/03/nema-23-stepper-19nm269ozin-w-brake-friction-torque-20nm283ozin-52372-1000x1000-1.jpg)

[STEPPER ONLINE](https://www.omc-stepperonline.com/stepper-motor-brake/nema-23-stepper-19nm269ozin-w-brake-friction-torque-20nm283ozin-23hs30-2804d-b200.html)

[![PKP243D23M2](https://ponoor.com/cms/wp-content/uploads/2021/03/pkp243d-700x525.jpg)](https://ponoor.com/cms/wp-content/uploads/2021/03/pkp243d.jpg)

[Orientalmotor](https://www.orientalmotor.co.jp/) PKP243D23M2

## Related commands and settings {#related}

<!-- osc-related: brake -->
<!-- generated:begin osc-related brake -->
**Related commands**

| Command | Arguments | Description |
| --- | --- | --- |
| [`/enableElectromagnetBrake`](../reference/brake.md#enableelectromagnetbrake) | (int)motorID (bool)enable | Enables / disables electromagnetic brake mode. |
| [`/activate`](../reference/brake.md#activate) | (int)motorID (bool)state | Switches motor excitation / release when electromagnetic brake mode is enabled. |
| [`/free`](../reference/brake.md#free) | (int)motorID | Releases motor axis when the electromagnetic brake mode is active. |
| [`/setBrakeTransitionDuration`](../reference/brake.md#setbraketransitionduration) | (int)motorID (int)duration | Sets the transitional duration to keep the motor excited when the electromagnetic brake is activated or released. |
| [`/getBrakeTransitionDuration`](../reference/brake.md#getbraketransitionduration) | (int)motorID | Returns the transitional duration to keep holding the motor axis when the electromagnetic brake is activated or released. |
| [`/getBrakeStatus`](../reference/brake.md#getbrakestatus) | (int)motorID | Returns the state of the electromagnetic brake of the specified motor. |
<!-- generated:end osc-related brake -->

<!-- osc-settings: driverSettings.electromagnetBrakeEnable, driverSettings.brakeTransitionDuration -->
<!-- generated:begin osc-settings driverSettings.electromagnetBrakeEnable, driverSettings.brakeTransitionDuration -->
**Related configuration items**

| Key | Name | Commands |
| --- | --- | --- |
| [`driverSettings.electromagnetBrakeEnable`](../connections/configuration-items.md#driversettings-electromagnetbrakeenable) | Electromagnetic brake enable | `/enableElectromagnetBrake` |
| [`driverSettings.brakeTransitionDuration`](../connections/configuration-items.md#driversettings-braketransitionduration) | Brake transition duration | `/setBrakeTransitionDuration` |
<!-- generated:end osc-settings driverSettings.electromagnetBrakeEnable, driverSettings.brakeTransitionDuration -->
