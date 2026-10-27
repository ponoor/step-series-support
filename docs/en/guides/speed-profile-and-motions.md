---
title: Speed profile and types of motor motion
---

# Speed profile and types of motor motion

The speed profile sets how fast the motor accelerates, decelerates and turns. This page explains the speed profile, the kinds of motion the motor can make with it, and the four kinds of stop.

## Speed profile {#speed-profile}

### Overview {#overview}

The speed profile sets the acceleration (acc), the deceleration (dec) and the maximum speed (maxSpeed) of the motor before it moves. What values the motor can take depends on:

- the specifications of the motor
- the power supply voltage
- the load
- voltage mode or current mode

The firmware has default values, but you need to set the values for your own environment, which takes some trial and error.

### Setting the profile {#setting}

Use [`/setSpeedProfile`](../reference/speed-profile.md#setspeedprofile) to set the three values. Acceleration and deceleration can be set only while the motor is stopped (or HiZ). While the motor is turning, the board replies `/error/command MotorNotStopped` and keeps the old values. The maximum speed can be set at any time.

The same applies to the other settings that are written to the driver only when the motor is stopped: [`/setAcc`](../reference/speed-profile.md#setacc), [`/setDec`](../reference/speed-profile.md#setdec), [`/setMinSpeed`](../reference/speed-profile.md#setminspeed) and [`/enableLowSpeedOptimize`](../reference/motor-driver-settings.md#enablelowspeedoptimize), and the Raw versions of them. Which commands need which state is shown in each command as the executable timing; see also [Command executable timing](../reference/index.md#command-executable-timing).

The acceleration and deceleration are rounded to the nearest value that the driver can hold, so the value that [`/getSpeedProfile`](../reference/speed-profile.md#getspeedprofile) returns can differ slightly from the one you set.

You can also set the minimum speed (minSpeed) with [`/setMinSpeed`](../reference/speed-profile.md#setminspeed). It is rarely used in an actual application, but the motor turns at this speed in [`/releaseSw`](../reference/homing.md#releasesw), the second step of the [homing](homing-and-position.md#homing-commands). The driver turns at 5 steps/s at least in `/releaseSw`, also when low speed optimization is enabled (the minimum speed is then 0).

## Types of motor motion {#motions}

### Constant speed {#constant-speed}

[`/run`](../reference/motor-control.md#run) drives the motor at a constant speed. The motor follows the acceleration and deceleration of the speed profile until it reaches the speed, and then it keeps the speed until `/run 0` or a stop command is sent. The motor does not exceed the maximum speed of the speed profile: a faster speed is limited to it. The motor is BUSY while it accelerates and decelerates.

[`/goUntil`](../reference/homing.md#gountil) and [`/releaseSw`](../reference/homing.md#releasesw) are also constant speed commands.

### Positioning {#positioning}

A positioning motion moves the motor to a target position in a trapezoidal profile. It accelerates at the configured acceleration, runs at the maximum speed once it reaches it, and decelerates at the configured deceleration, timed so that the motor stops at the target position. When the distance is short or the acceleration and deceleration are slow, the deceleration can start before the maximum speed is reached. The motor is BUSY until it stops.

[`/goTo`](../reference/motor-control.md#goto) and [`/move`](../reference/motor-control.md#move) are typical positioning commands. [`/goHome`](../reference/position-management.md#gohome), [`/goMark`](../reference/position-management.md#gomark) and [`/goToDir`](../reference/motor-control.md#gotodir) are also positioning commands.

A positioning motion in progress can be interrupted by another one, except for `/move`: [`/goTo`](../reference/motor-control.md#goto), [`/goToDir`](../reference/motor-control.md#gotodir), [`/goHome`](../reference/position-management.md#gohome) and [`/goMark`](../reference/position-management.md#gomark) are accepted while the motor is BUSY (the firmware first clears the BUSY state). `/move` is not: the driver ignores it while the motor is running, and the board then replies `/error/command CommandIgnored`.

### Servo mode {#servo-mode}

The servo mode is not a function of the motor driver but a way of driving that the firmware implements. It keeps updating a constant speed motion so that the motor follows a target position that you give in real time, like a radio-controlled servo motor. While the motor is in this mode, the other motion commands are rejected with `InServoMode`. See [Servo mode](servo-mode.md).

## Types of stop {#stops}

There are two choices, which make four commands:

- decelerate according to the speed profile, or stop instantly
- keep the motor energized, or make it HiZ (high impedance) after it stops

| State after the stop | Decelerating stop | Instant stop |
| --- | --- | --- |
| Energized | [`/softStop`](../reference/motor-control.md#softstop) | [`/hardStop`](../reference/motor-control.md#hardstop) |
| HiZ | [`/softHiZ`](../reference/motor-control.md#softhiz) | [`/hardHiZ`](../reference/motor-control.md#hardhiz) |

An energized motor keeps its position: a voltage or a current according to KVAL_HOLD or TVAL_HOLD flows in the motor. In the HiZ state the outputs of the driver are high impedance, no current flows in the motor, and the motor does not hold its position. **A load that the motor is carrying can fall or lose its position when the motor is HiZ.**

For a motor with an electromagnetic brake, the commands that make the motor HiZ also engage the brake, and the stop commands act differently depending on the state of the brake. See [Electromagnetic brake](electromagnetic-brake.md#commands).

## Related commands and settings {#related}

<!-- osc-related: speed_profile, motion -->
<!-- generated:begin osc-related speed_profile, motion -->
**Related commands**

| Command | Arguments | Description |
| --- | --- | --- |
| [`/setSpeedProfile`](../reference/speed-profile.md#setspeedprofile) | (int)motorID (float)acc (float)dec (float)maxSpeed | Sets the acc, dec, and maxSpeed of the speed profile together. |
| [`/getSpeedProfile`](../reference/speed-profile.md#getspeedprofile) | (int)motorID | Gets the acc, dec, and maxSpeed of the speed profile together. |
| [`/setFullstepSpeed`](../reference/speed-profile.md#setfullstepspeed) | (int)motorID (float)fullstepSpeed | Sets the threshold at which the microstepping mode automatically switches to full-step mode. |
| [`/getFullstepSpeed`](../reference/speed-profile.md#getfullstepspeed) | (int)motorID | Gets the threshold at which the microstepping mode automatically switches to full-step mode. |
| [`/setMaxSpeed`](../reference/speed-profile.md#setmaxspeed) | (int)motorID (float)maxSpeed | Set the maximum speed of the speed profile |
| [`/setAcc`](../reference/speed-profile.md#setacc) | (int)motorID (float)acc | Sets the acceleration of the speed profile. |
| [`/setDec`](../reference/speed-profile.md#setdec) | (int)motorID (float)dec | Sets the deceleration of the speed profile. |
| [`/setMinSpeed`](../reference/speed-profile.md#setminspeed) | (int)motorID (float)minSpeed | Set the speed profile minimum speed. |
| [`/getMinSpeed`](../reference/speed-profile.md#getminspeed) | (int)motorID | Return the speed profile minimum speed. |
| [`/getSpeed`](../reference/speed-profile.md#getspeed) | (int)motorID | Returns the current motor speed. |
| [`/setSpeedProfileRaw`](../reference/speed-profile.md#setspeedprofileraw) | (int)motorID (int)acc (int)dec (int)maxSpeed | Sets the acc, dec, and maxSpeed of the speed profile using raw driver IC register values. |
| [`/getSpeedProfileRaw`](../reference/speed-profile.md#getspeedprofileraw) | (int)motorID | Gets the acc, dec, and maxSpeed of the speed profile as raw driver IC register values. |
| [`/setMaxSpeedRaw`](../reference/speed-profile.md#setmaxspeedraw) | (int)motorID (int)maxSpeed | Sets the maximum speed of the speed profile using a raw register value. |
| [`/setMinSpeedRaw`](../reference/speed-profile.md#setminspeedraw) | (int)motorID (int)minSpeed | Sets the minimum speed of the speed profile using a raw register value. |
| [`/setFullstepSpeedRaw`](../reference/speed-profile.md#setfullstepspeedraw) | (int)motorID (int)fullstepSpeed | Sets the full-step speed threshold using a raw register value. |
| [`/setAccRaw`](../reference/speed-profile.md#setaccraw) | (int)motorID (int)acc | Sets the acceleration of the speed profile using a raw register value. |
| [`/setDecRaw`](../reference/speed-profile.md#setdecraw) | (int)motorID (int)dec | Sets the deceleration of the speed profile using a raw register value. |
| [`/run`](../reference/motor-control.md#run) | (int)motorID (float)speed | Rotates the motor at specified speed. |
| [`/move`](../reference/motor-control.md#move) | (int)motorID (int)step | Moves specified number of steps according to the pre-set speed profile. |
| [`/goTo`](../reference/motor-control.md#goto) | (int)motorID (int)position | Moves to the specified position in the shortest route according to the pre-set speed profile. |
| [`/goToDir`](../reference/motor-control.md#gotodir) | (int)motorID (bool)DIR (int)position | Moves to the specified position in the specified direction according to the pre-set speed profile. |
| [`/softStop`](../reference/motor-control.md#softstop) | (int)motorID | After decelerating according to the speed profile, the motor stops while it is kept excited. |
| [`/hardStop`](../reference/motor-control.md#hardstop) | (int)motorID | Immediately stops the motor and leaves it excited. |
| [`/softHiZ`](../reference/motor-control.md#softhiz) | (int)motorID | Decelerate according to the speed profile, then stop the motor and release excitation. |
| [`/hardHiZ`](../reference/motor-control.md#hardhiz) | (int)motorID | Immediately stops the motor and releases the stepper excitation. |
| [`/combine/run`](../reference/motor-control.md#combine-run) | (int)motorID1 (int)motorID2 (float)speed | Same as `/run` for two motors. |
| [`/combine/move`](../reference/motor-control.md#combine-move) | (int)motorID1 (int)motorID2 (int)step | Same as `/move` for two motors. |
| [`/combine/goTo`](../reference/motor-control.md#combine-goto) | (int)motorID1 (int)motorID2 (int)position | Same as `/goTo` for two motors. |
| [`/combine/goToDir`](../reference/motor-control.md#combine-gotodir) | (int)motorID1 (int)motorID2 (bool)DIR (int)position | Same as `/goToDir` for two motors. |
| [`/combine/softStop`](../reference/motor-control.md#combine-softstop) | (int)motorID1 (int)motorID2 | Same as `/softStop` for two motors: it is handled as `/softStop` for motorID1 and then for motorID2. |
| [`/combine/hardStop`](../reference/motor-control.md#combine-hardstop) | (int)motorID1 (int)motorID2 | Same as `/hardStop` for two motors: it is handled as `/hardStop` for motorID1 and then for motorID2. |
| [`/combine/softHiZ`](../reference/motor-control.md#combine-softhiz) | (int)motorID1 (int)motorID2 | Same as `/softHiZ` for two motors: it is handled as `/softHiZ` for motorID1 and then for motorID2. |
| [`/combine/hardHiZ`](../reference/motor-control.md#combine-hardhiz) | (int)motorID1 (int)motorID2 | Same as `/hardHiZ` for two motors: it is handled as `/hardHiZ` for motorID1 and then for motorID2. |
| [`/runRaw`](../reference/motor-control.md#runraw) | (int)motorID (int)speed | Rotates the motor at the specified speed using a raw register value. |
| [`/goUntilRaw`](../reference/motor-control.md#gountilraw) | (int)motorID (bool)ACT (int)speed | Same as `/goUntil` but uses a raw register value for speed. |
| [`/combine/runRaw`](../reference/motor-control.md#combine-runraw) | (int)motorID1 (int)motorID2 (int)speed | A speed outside the 20-bit range is limited to 20 bits by the driver. |
<!-- generated:end osc-related speed_profile, motion -->

<!-- osc-settings: speedProfile -->
<!-- generated:begin osc-settings speedProfile -->
**Related configuration items**

| Key | Name | Commands |
| --- | --- | --- |
| [`speedProfile.acc`](../connections/configuration-items.md#speedprofile-acc) | Acceleration | `/setAcc`, `/setSpeedProfile` |
| [`speedProfile.dec`](../connections/configuration-items.md#speedprofile-dec) | Deceleration | `/setDec`, `/setSpeedProfile` |
| [`speedProfile.maxSpeed`](../connections/configuration-items.md#speedprofile-maxspeed) | Max speed | `/setMaxSpeed`, `/setSpeedProfile` |
| [`speedProfile.fullStepSpeed`](../connections/configuration-items.md#speedprofile-fullstepspeed) | Transit to fullstep threshold speed | `/setFullstepSpeed` |
| [`speedProfile.minSpeed`](../connections/configuration-items.md#speedprofile-minspeed) | Minimum speed | `/setMinSpeed` |
<!-- generated:end osc-settings speedProfile -->
