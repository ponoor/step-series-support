---
title: Servo mode
---

# Servo mode

The servo mode lets the motor follow a target position that changes in real time. This page explains what the mode is, how to start it and how to give the target, and how to tune the PID gains.

## What the servo mode is {#what}

The servo mode is not a function of the motor driver chip. Positioning commands of the driver need the target position to be set before the motion starts, and a new target is not accepted until the motion has finished. In the servo mode, you can define a new target position *while the motor is moving*, like a radio-controlled servo motor. While the mode is active, the other motion commands cannot be sent: they are rejected with `InServoMode`.

![The control of the servo mode](https://python-step-series.readthedocs.io/en/documentation/_images/pid-control.jpg)

The firmware updates the speed of the motor every 5 ms. At each update it compares the current position with the target, calculates the speed with the PID control described below, and sends it to the driver as a constant speed command. (Until v2.1.0 the period was 10 ms.) The integral and derivative terms are scaled by the period, so the same gains were designed to give about the same response as before; the response can still differ a little, and you may need to tune the gains again.

## Starting the servo mode {#starting}

### Toggling the mode {#toggling}

[`/enableServoMode`](../reference/servo-mode_reference.md#enableservomode) starts and stops the servo mode. When the mode starts, the board stops the motor with a hard stop, makes the current position the target position, and clears the integral and the previous error of the PID control. For a motor with an electromagnetic brake, `/enableServoMode 1` is a motion command: while the brake is engaged, the board replies `BrakeEngaged` and does not start the mode (see the [motion start condition](../reference/index.md#motion-start-condition)).

When the mode stops, the board stops the motor with a soft stop and keeps it energized. For a motor with an electromagnetic brake, what `/enableServoMode 0` does depends on the state of the brake; see [Electromagnetic brake](electromagnetic-brake.md#commands).

**Notifications are turned off.** When the servo mode starts, the notifications of [`/busy`](../reference/automatically-sent-messages.md#busy), [`/motorStatus`](../reference/automatically-sent-messages.md#motorstatus) and [`/dir`](../reference/automatically-sent-messages.md#dir) are disabled (the settings that [`/enableBusyReport`](../reference/motor-driver-settings.md#enablebusyreport), [`/enableMotorStatusReport`](../reference/motor-driver-settings.md#enablemotorstatusreport) and [`/enableDirReport`](../reference/motor-driver-settings.md#enabledirreport) make). They are not enabled again when the mode stops. Enable them again if you need them.

### Updating the target position {#target}

[`/setTargetPosition`](../reference/servo-mode_reference.md#settargetposition) updates the target position. When the firmware receives a new target, it compares it with the current position and changes the speed of the motor. [`/setTargetPositionList`](../reference/servo-mode_reference.md#settargetpositionlist) sends the targets of all the motors at once.

### Cases where the servo mode stops or is not available {#limits}

- [`/goUntil`](../reference/homing.md#gountil), [`/goUntilRaw`](../reference/motor-control.md#gountilraw) and [`/releaseSw`](../reference/homing.md#releasesw) reply `InServoMode` and do nothing while the motor is in the servo mode, as the other motion commands and [`/homing`](../reference/homing.md#homing) do.
- **Do not send [`/setPosition`](../reference/position-management.md#setposition) or [`/resetPos`](../reference/position-management.md#resetpos) while the motor is in the servo mode.** The board does not guard against this.
- When the driver makes the motor HiZ by itself (overcurrent, overtemperature or UVLO), the servo mode is cancelled and `ServoModeCancelledOnHiZ` is sent. The commands that make the motor HiZ cancel the servo mode first. To resume, send `/enableServoMode 1` again; the current position becomes the target. See [Alarms and protection](alarms-and-protection.md#hiz-by-itself).
- **In the servo mode, the firmware watches the switches itself** (in addition to the driver). At every update, it sets the speed to 0 if the motor would move in a prohibited direction: toward `homingDirection` while the HOME switch is on, and (STEP400 only) away from `homingDirection` while the LIMIT switch is on. This applies to a switch whose motion is prohibited ([`/setProhibitMotionOnHomeSw`](../reference/alarm-settings.md#setprohibitmotiononhomesw), [`/setProhibitMotionOnLimitSw`](../reference/alarm-settings.md#setprohibitmotiononlimitsw)) or whose mode is the hard stop mode. The two switches are judged separately, so a pressed HOME switch does not hide the LIMIT switch. Motion in the other direction is not blocked, so the motor can move away from a switch. The STEP800 has the HOME switch only. When the HOME switch turns on in the hard stop mode, the motor also makes a hard stop at once, whichever direction it moves (see [Hard stop mode](homing-and-position.md#sw-mode)).

## Control parameters {#parameters}

The speed of the motor is calculated with a technique called PID control. [`/setServoParam`](../reference/servo-mode_reference.md#setservoparam) sets the three gains of it.

### Proportional gain (kP) {#kp}

PID control uses the difference between the current position and the target position (the deviation). The motor turns faster when the deviation is large and slower when it is small, so it approaches the target. The proportional gain sets how much the deviation influences the speed. If it is too small, the approach takes a long time; if it is too large, the motor overshoots the target.

### Integral gain (kI) {#ki}

With the proportional control only, the motor gets slower as it approaches the target, and it takes a very long time to remove the last small deviation. Adding the time integral of the deviation to the control value removes it. A large integral gain removes the deviation quickly, but it can cause overshoot, and the motion that compensates for the overshoot can cause continuous oscillation.

### Derivative gain (kD) {#kd}

When the motor overshoots or oscillates, this gain works against the steep changes of the deviation. It acts like a damper that reduces each oscillation.

## Determining the PID parameters {#tuning}

### Step by step {#steps}

The PID gains depend on the acceleration, the deceleration and the maximum speed that the motor can actually use (the speed profile). Determine them in this order:

1. Decide the KVAL (the TVAL in current mode) that suits the rating of the motor and the load. See [Voltage mode and current mode](voltage-and-current-mode.md).
2. Decide the acceleration, the deceleration and the maximum speed that the motor can use. See [Speed profile and types of motor motion](speed-profile-and-motions.md).
3. Adjust the PID gains.

### Deciding the gains {#deciding}

There are many methods to decide the best gains. They depend on the purpose of the motion and on how often the target changes. We recommend this approach, with trial and error on the real setup.

#### 1. kP {#tune-kp}

Set kP, kI and kD to 0.0, and raise kP gradually until the motor starts to oscillate around its target. When the target changes only from time to time, we often set only kP and keep kI and kD at 0.0.

#### 2. kI {#tune-ki}

When the target changes only once every few seconds, a higher kI makes the motion more agile. When the target is sent at 60 fps, however, the acceleration toward each new target can cause vibration and spoil the smoothness. The value depends on whether a quick response to the target or a smooth overall motion is more important.

#### 3. kD {#tune-kd}

Raise kD gradually if you see oscillation or overshoot when the motor approaches the target.

## Related commands and settings {#related}

<!-- osc-related: servo -->
<!-- generated:begin osc-related servo -->
**Related commands**

| Command | Arguments | Description |
| --- | --- | --- |
| [`/enableServoMode`](../reference/servo-mode_reference.md#enableservomode) | (int)motorID (bool)enable | Turns on/off the servo mode (position tracking mode). |
| [`/setServoParam`](../reference/servo-mode_reference.md#setservoparam) | (int)motorID (float)kP (float)kI (float)kD | Adjusts the PID control gain. |
| [`/getServoParam`](../reference/servo-mode_reference.md#getservoparam) | (int)motorID | Gets the PID gains (kP, kI, kD) of the servo mode. |
| [`/setTargetPosition`](../reference/servo-mode_reference.md#settargetposition) | (int)motorID (int)position | Sets the target position in servo mode. |
| [`/setTargetPositionList`](../reference/servo-mode_reference.md#settargetpositionlist) | (int)position1 ... (int)positionN | Sets the target positions of the servo mode for all axes at once. |
<!-- generated:end osc-related servo -->

<!-- osc-settings: servoMode -->
<!-- generated:begin osc-settings servoMode -->
**Related configuration items**

| Key | Name | Commands |
| --- | --- | --- |
| [`servoMode.kP`](../connections/configuration-items.md#servomode-kp) | kP | `/setServoParam` |
| [`servoMode.kI`](../connections/configuration-items.md#servomode-ki) | kI | `/setServoParam` |
| [`servoMode.kD`](../connections/configuration-items.md#servomode-kd) | kD | `/setServoParam` |
<!-- generated:end osc-settings servoMode -->
