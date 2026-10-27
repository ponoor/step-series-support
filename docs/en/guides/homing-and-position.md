---
title: Homing and position management
---

# Homing and position management

A stepper motor does not know where it is when the board starts. This page explains why you need homing, how the HOME and LIMIT switches are used, what the homing commands do, and what to keep in mind when you manage the position.

## Stepper motor and homing {#why-homing}

When the system powers up, it does not know where the motor is. It could be pointing in any direction, depending on where it stopped when the system was last shut down.

If the stepper motor receives an external force that exceeds its limit, the steps slip out of alignment (**stall**). The motor then keeps working with an unknown offset between the position in the program and the physical position.

Applications that have a position or an orientation must therefore use a sensor to detect a reference position on startup, or periodically while they are running. This action is called **homing**.

After the board restarts, and after the motor has been HiZ, do homing again: the position is not reliable any more. This is especially important for a motor with an electromagnetic brake; see [Electromagnetic brake](electromagnetic-brake.md#usage).

## Switches and sensors {#switches}

![Two configurations of homing sensors](http://ponoor.com/manage/wp-content/uploads/2020/10/two-homing-sensors.png)

Photointerrupters are often used as home sensors. On the left, a piece of white plastic attached to the slider blocks the light between the emitter and the receiver of the photointerrupter. The right side is an example of a rotary table where the photointerrupter responds to the black screw. Microswitches and photoelectric sensors are also used.

## The HOME and LIMIT switches {#home-limit}

Each axis of the STEP400 and the STEP800 has a HOME terminal where a sensor or a switch can be connected, with a 5 V power supply for the sensor. The STEP400 has a LIMIT terminal as well. A sensor on a terminal is called the HOME switch or the LIMIT switch. For the pin assignment and how to connect a switch or a sensor, see [Sensors and switches](../connections/sensors-and-switches.md#terminals).

### HOME {#home}

The HOME terminal is connected directly to the motor driver and works with the homing function of the driver. It is normally used for the home sensor.

### LIMIT (STEP400 only) {#limit}

Some applications need two sensors. A slider, for example, has a limited range of motion, and if it stalls while it is moving, it can collide with one of the ends. Sensors at both ends prevent this.

The motor can be set to stop forcibly when a switch is on. The switches can also be used as simple inputs, separate from the motor operation: for example, you can connect a push button and have the board send an OSC message when it is pressed.

A switch is on when its input is LOW. The combination of the mechanism and the sensor must make the signal of the sensor go from HIGH to LOW at the home position (see [Sensors and switches](../connections/sensors-and-switches.md#wiring) for the sensors and the wiring). The commands [`/setHomeSwMode`](../reference/home-and-limit-sensors.md#sethomeswmode) and [`/setLimitSwMode`](../reference/home-and-limit-sensors.md#setlimitswmode) set what the board does when the switch turns on.

### Hard stop mode and `SW_USER` {#sw-mode}

The setting of the HOME switch (and the LIMIT switch on the STEP400) is either `SW_HARD_STOP` or `SW_USER`; see [`/setHomeSwMode`](../reference/home-and-limit-sensors.md#sethomeswmode) and [`/setLimitSwMode`](../reference/home-and-limit-sensors.md#setlimitswmode). With `SW_HARD_STOP` the motor makes a hard stop at the moment the switch turns on. It does not look at the direction of the motion: a motor that moves away from the switch is stopped as well. Use the collision prevention settings below to restrict the direction. In the servo mode the firmware also judges the direction itself; see [Servo mode](servo-mode.md#limits).

### Collision prevention settings {#collision-prevention}

You can limit the direction in which the motor can turn while the HOME or LIMIT switch is on. With [`/setProhibitMotionOnHomeSw`](../reference/alarm-settings.md#setprohibitmotiononhomesw) and [`/setProhibitMotionOnLimitSw`](../reference/alarm-settings.md#setprohibitmotiononlimitsw), you can prohibit the motion toward `homingDirection` while the HOME switch is on, and the motion in the opposite direction while the LIMIT switch is on. This prevents the mechanism from running into its ends with a wrong command. A motion command that does not meet the condition is rejected with `HomeSwActivating` or `LimitSwActivating`; see the [motion start condition](../reference/index.md#motion-start-condition).

For [`/goTo`](../reference/motor-control.md#goto), [`/goHome`](../reference/position-management.md#gohome), [`/goMark`](../reference/position-management.md#gomark) and [`/goToDir`](../reference/motor-control.md#gotodir) the direction of the motion is the direction of the way to the target that the driver takes (the shortest way, with wrap-around). Before v2.2.0 the board judged this direction wrongly for a target that was close, so a short move away from the switch was refused.

`homingDirection` is set with [`/setHomingDirection`](../reference/homing.md#sethomingdirection) or with the [browser configuration tool](../connections/browser-config-tool.md). It is also used for [`/homing`](../reference/homing.md#homing).

![Homing direction](https://ponoor.com/cms/wp-content/uploads/2020/08/homingDirection-800x533.jpg)

## Homing commands {#homing-commands}

The homing command is [`/homing`](../reference/homing.md#homing). It combines two commands that the motor driver provides, [`/goUntil`](../reference/homing.md#gountil) and [`/releaseSw`](../reference/homing.md#releasesw). This section explains them first.

### `/goUntil` {#gountil}

First the motor moves toward the home sensor with [`/goUntil`](../reference/homing.md#gountil). When the sensor turns on, the motor decelerates and stops (if the setting makes it do so).

### `/releaseSw` {#releasesw}

[`/releaseSw`](../reference/homing.md#releasesw) moves the motor slowly in the opposite direction from the current position, and stops it immediately when the sensor turns off. The position where the motor stops is the home position. Strictly speaking, `/goUntil` does not stop at the moment the sensor turns on; the motor decelerates first, so it stops a little away from the point where the sensor responded. The firmware does not correct this, because every environment is different.

Both commands can be set to reset the current position to 0 at the moment the sensor turns on, with [`/setHomeSwMode`](../reference/home-and-limit-sensors.md#sethomeswmode).

A demonstration video of `/goUntil` and `/releaseSw`: [Homing demo (Vimeo)](https://vimeo.com/1239729741)

### `/homing` {#homing}

You can send the two commands one after the other over OSC, but [`/homing`](../reference/homing.md#homing) runs the whole sequence as one command. It completes the home sequence automatically in the homing direction and at the homing speed that you set beforehand with the [browser configuration tool](../connections/browser-config-tool.md) or with [`/setHomingDirection`](../reference/homing.md#sethomingdirection) and [`/setHomingSpeed`](../reference/homing.md#sethomingspeed).

The progress is reported with [`/homingStatus`](../reference/automatically-sent-messages.md#homingstatus) (and [`/getHomingStatus`](../reference/homing.md#gethomingstatus) asks for it). The homing ends with `HOMING_COMPLETED` when `/releaseSw` has finished, or with `HOMING_TIMEOUT` when a timeout elapsed (below). The values are listed at [`/homingStatus`](../reference/automatically-sent-messages.md#homingstatus). A motion command that you send during the homing clears the homing state.

[`/goUntil`](../reference/homing.md#gountil), [`/goUntilRaw`](../reference/motor-control.md#gountilraw) and [`/releaseSw`](../reference/homing.md#releasesw) are rejected with `InServoMode` while the motor is in the servo mode, and [`/homing`](../reference/homing.md#homing) is rejected with `BrakeEngaged` while the brake of the motor is not released.

### Homing timeouts {#timeouts}

Both `/goUntil` and `/releaseSw` have timeouts, set with [`/setGoUntilTimeout`](../reference/homing.md#setgountiltimeout) and [`/setReleaseSwTimeout`](../reference/homing.md#setreleaseswtimeout). When the state of the sensor has not changed within the time, the board stops the motor with a hard stop and sends `/error/command GoUntilTimeout` or `ReleaseSwTimeout`. This prevents the moving part from being pushed against a mechanical end forever when the sensor does not respond.

### Homing at startup {#homing-at-startup}

When [`driverSettings.homingAtStartup`](../connections/configuration-items.md#driversettings-homingatstartup) is set, the board starts the homing after it starts. For a motor with an electromagnetic brake, the board releases the brake first and starts the homing when the brake is released.

## Rotary tables {#rotary-tables}

When the home sensor responds to a hole or to a part that has a width, the position at which the sensor responds differs between clockwise and counterclockwise rotation by that width. The board can notify both the change from HIGH to LOW and the change from LOW to HIGH of the home sensor with an OSC message. The message also contains the direction of the rotation, so you can align the home position if you write a sequence for each direction. Enable this notification with [`/enableHomeSwReport`](../reference/home-and-limit-sensors.md#enablehomeswreport).

## Position management {#position}

- [`/setPosition`](../reference/position-management.md#setposition) and [`/resetPos`](../reference/position-management.md#resetpos) change the position that the board holds. **Do not send them while the motor is in the servo mode or moving.** The board does not guard against this; the motor can behave unexpectedly.
- [`/setMark`](../reference/position-management.md#setmark) stores a position that [`/goMark`](../reference/position-management.md#gomark) goes to.
- When the microstep setting changes, the coordinate system changes too; see [Voltage mode and current mode](voltage-and-current-mode.md#switching).

## Related commands and settings {#related}

<!-- osc-related: homing, sensors, position, /setProhibitMotionOnHomeSw, /setProhibitMotionOnLimitSw -->
<!-- generated:begin osc-related homing, sensors, position, /setProhibitMotionOnHomeSw, /setProhibitMotionOnLimitSw -->
**Related commands**

| Command | Arguments | Description |
| --- | --- | --- |
| [`/homing`](../reference/homing.md#homing) | (int)motorID | Start the homing movement. |
| [`/getHomingStatus`](../reference/homing.md#gethomingstatus) | (int)motorID | Returns current state of homing movement. |
| [`/setHomingDirection`](../reference/homing.md#sethomingdirection) | (int)motorID (bool)direction | Sets the `homingDirection` for the `/homing` command. |
| [`/getHomingDirection`](../reference/homing.md#gethomingdirection) | (int)motorID | Returns `homingDirection` parameter. |
| [`/setHomingSpeed`](../reference/homing.md#sethomingspeed) | (int)motorID (float)speed | Sets the `homingSpeed` when executing the command `/homing`. |
| [`/getHomingSpeed`](../reference/homing.md#gethomingspeed) | (int)motorID | Returns `homingSpeed` parameter. |
| [`/goUntil`](../reference/homing.md#gountil) | (int)motorID (bool)ACT (float)speed | Move the motor at specified speed and direction. |
| [`/setGoUntilTimeout`](../reference/homing.md#setgountiltimeout) | (int)motorID (int)timeOut | Sets the time-out duration when executing `/goUntil` command. |
| [`/getGoUntilTimeout`](../reference/homing.md#getgountiltimeout) | (int)motorID | Returns the time-out duration when executing `/goUntil` command. |
| [`/releaseSw`](../reference/homing.md#releasesw) | (int)motorID (bool)ACT (bool)DIR | Move at minimum speed (5[step/s] by default) in the specified direction until the HOME switch pin becomes open. |
| [`/setReleaseSwTimeout`](../reference/homing.md#setreleaseswtimeout) | (int)motorID (int)timeOut | Sets the time-out duration when executing `/releaseSw` command. |
| [`/getReleaseSwTimeout`](../reference/homing.md#getreleaseswtimeout) | (int)motorID | Returns the time-out duration when executing `/releaseSw` command. |
| [`/enableHomeSwReport`](../reference/home-and-limit-sensors.md#enablehomeswreport) | (int)motorID (bool)enable | Sets the following message to be sent automatically when conditional change of the HOME switch of the specified motor is detected. |
| [`/enableSwEventReport`](../reference/home-and-limit-sensors.md#enablesweventreport) | (int)motorID (bool)enable | Sets the following message to be sent automatically when the specified motor's HOME switch terminal state drops from HIGH level to LOW (Falling Edge). |
| [`/getHomeSw`](../reference/home-and-limit-sensors.md#gethomesw) | (int)motorID | Gets the status of the HOME switch, closed or opened. |
| [`/enableLimitSwReport`](../reference/home-and-limit-sensors.md#enablelimitswreport) | (int)motorID (bool)enable | Sets automatic response when conditional change on the specified motor's LIMIT switch terminal is detected. |
| [`/getLimitSw`](../reference/home-and-limit-sensors.md#getlimitsw) | (int)motorID | Returns the status of LIMIT switch. |
| [`/setHomeSwMode`](../reference/home-and-limit-sensors.md#sethomeswmode) | (int)motorID (bool)SW_MODE | Sets switch mode whether to stop immediately when the HOME switch terminal state changes (falling edge). |
| [`/getHomeSwMode`](../reference/home-and-limit-sensors.md#gethomeswmode) | (int)motorID | Get the Switch mode described above. |
| [`/setLimitSwMode`](../reference/home-and-limit-sensors.md#setlimitswmode) | (int)motorID (bool)SW_MODE | Sets the Switch mode whether to stop the motor immediately when the LIMIT switch terminal condition is changed. |
| [`/getLimitSwMode`](../reference/home-and-limit-sensors.md#getlimitswmode) | (int)motorID | Get the Switch mode described above. |
| [`/setPosition`](../reference/position-management.md#setposition) | (int)motorID (int)newPosition | Rewrites ABS_POS register to the specified coordinates. |
| [`/getPosition`](../reference/position-management.md#getposition) | (int)motorID | Returns the contents of the ABS_POS register (current position). |
| [`/getPositionList`](../reference/position-management.md#getpositionlist) | - | Returns the current position of all motors at once. |
| [`/resetPos`](../reference/position-management.md#resetpos) | (int)motorID | Reset ABS_POS register to 0. |
| [`/setElPos`](../reference/position-management.md#setelpos) | (int)motorID (int)newFullstep (int)newMicrostep | Set the electrical position of the motor. |
| [`/getElPos`](../reference/position-management.md#getelpos) | (int)motorID | Returns the current electrical position of the motor. |
| [`/setMark`](../reference/position-management.md#setmark) | (int)motorID (int)MARK | Set the MARK register to arbitrary position. |
| [`/getMark`](../reference/position-management.md#getmark) | (int)motorID | Get the MARK position. |
| [`/goHome`](../reference/position-management.md#gohome) | (int)motorID | Move the motor to the HOME position (zero position) according to the speed profile. |
| [`/goMark`](../reference/position-management.md#gomark) | (int)motorID | Move the motor to the MARK position according to the speed profile. |
| [`/setProhibitMotionOnHomeSw`](../reference/alarm-settings.md#setprohibitmotiononhomesw) | (int)motorID (bool)enable | Prohibits any motion commands towards the origin point when the HOME switch is activated. |
| [`/setProhibitMotionOnLimitSw`](../reference/alarm-settings.md#setprohibitmotiononlimitsw) | (int)motorID (bool)enable | Prohibits any motion commands towards the leaving direction from origin point, when the LIMIT switch is activated. |
<!-- generated:end osc-related homing, sensors, position, /setProhibitMotionOnHomeSw, /setProhibitMotionOnLimitSw -->

<!-- osc-settings: driverSettings.homingAtStartup, driverSettings.homingDirection, driverSettings.homingSpeed, driverSettings.homeSwMode, driverSettings.prohibitMotionOnHomeSw, driverSettings.limitSwMode, driverSettings.prohibitMotionOnLimitSw, driverSettings.goUntilTimeout, driverSettings.releaseSwTimeout, alarmAndReport.reportHomeSwStatus, alarmAndReport.reportLimitSwStatus, alarmAndReport.reportSwEvn -->
<!-- generated:begin osc-settings driverSettings.homingAtStartup, driverSettings.homingDirection, driverSettings.homingSpeed, driverSettings.homeSwMode, driverSettings.prohibitMotionOnHomeSw, driverSettings.limitSwMode, driverSettings.prohibitMotionOnLimitSw, driverSettings.goUntilTimeout, driverSettings.releaseSwTimeout, alarmAndReport.reportHomeSwStatus, alarmAndReport.reportLimitSwStatus, alarmAndReport.reportSwEvn -->
**Related configuration items**

| Key | Name | Commands |
| --- | --- | --- |
| [`driverSettings.homingAtStartup`](../connections/configuration-items.md#driversettings-homingatstartup) | Homing when the system starts |  |
| [`driverSettings.homingDirection`](../connections/configuration-items.md#driversettings-homingdirection) | Homing Direction | `/setHomingDirection` |
| [`driverSettings.homingSpeed`](../connections/configuration-items.md#driversettings-homingspeed) | Homing Speed | `/setHomingSpeed` |
| [`driverSettings.homeSwMode`](../connections/configuration-items.md#driversettings-homeswmode) | Home switch won't cause HardStop | `/setHomeSwMode` |
| [`driverSettings.prohibitMotionOnHomeSw`](../connections/configuration-items.md#driversettings-prohibitmotiononhomesw) | Prohibit motions on HomeSw | `/setProhibitMotionOnHomeSw` |
| [`driverSettings.limitSwMode`](../connections/configuration-items.md#driversettings-limitswmode) | Limit switch won't cause HardStop | `/setLimitSwMode` |
| [`driverSettings.prohibitMotionOnLimitSw`](../connections/configuration-items.md#driversettings-prohibitmotiononlimitsw) | Prohibit motions on LimitSw | `/setProhibitMotionOnLimitSw` |
| [`driverSettings.goUntilTimeout`](../connections/configuration-items.md#driversettings-gountiltimeout) | goUntil timeout duration | `/setGoUntilTimeout` |
| [`driverSettings.releaseSwTimeout`](../connections/configuration-items.md#driversettings-releaseswtimeout) | releaseSw timeout duration | `/setReleaseSwTimeout` |
| [`alarmAndReport.reportHomeSwStatus`](../connections/configuration-items.md#alarmandreport-reporthomeswstatus) | Report HOME switch status | `/enableHomeSwReport` |
| [`alarmAndReport.reportLimitSwStatus`](../connections/configuration-items.md#alarmandreport-reportlimitswstatus) | Report LIMIT switch status | `/enableLimitSwReport` |
| [`alarmAndReport.reportSwEvn`](../connections/configuration-items.md#alarmandreport-reportswevn) | Report HOME switch event | `/enableSwEventReport` |
<!-- generated:end osc-settings driverSettings.homingAtStartup, driverSettings.homingDirection, driverSettings.homingSpeed, driverSettings.homeSwMode, driverSettings.prohibitMotionOnHomeSw, driverSettings.limitSwMode, driverSettings.prohibitMotionOnLimitSw, driverSettings.goUntilTimeout, driverSettings.releaseSwTimeout, alarmAndReport.reportHomeSwStatus, alarmAndReport.reportLimitSwStatus, alarmAndReport.reportSwEvn -->
