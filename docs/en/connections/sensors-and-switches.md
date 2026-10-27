---
title: Sensors and switches
---

# Sensors and switches

The terminals for the switches and the sensors, their pin assignment, and how to wire a switch or a sensor. What the board does with the signal, such as homing and the hard stop, is explained in [Homing and position management](../guides/homing-and-position.md).

## HOME and LIMIT terminals {#terminals}

Each axis of the STEP400 and the STEP800 has a HOME terminal for a switch or a sensor. The STEP400 has a LIMIT terminal for each axis in addition. A sensor on a terminal is also called the HOME switch or the LIMIT switch.

### HOME {#home}

A stepper motor cannot detect its own position, so a sensor is needed to find the home position at the start. The HOME terminal is connected directly to the driver IC and can be used for the position management of the driver. The input is pulled up to 3.3 V. What it is used for is explained in [Homing and position management](../guides/homing-and-position.md#home).

### LIMIT (STEP400 only) {#limit}

The LIMIT terminal can be used to limit the range of the motion of each motor, or as an input for another purpose. The input is pulled up to 3.3 V like the HOME input. On the STEP400 (R1) it is connected to the ADC input (ADCIN) of the driver IC, and the firmware reads it from there. The STEP800 has no LIMIT terminal. See [Homing and position management](../guides/homing-and-position.md#limit).

### Connector {#connector}

The terminals are XA series connectors from JST (J.S.T.MFG.CO., LTD.). Compatible parts:

| Product name | Model number | Remarks |
| --- | --- | --- |
| (Reference) PCB post | B03B-XASK-1 (LF)(SN) | Header mounted on the board |
| Housing | XAP-03V-1 | Plastic housing |
| Contact | BXA-001T-P0.6 | Crimp contact inserted into the housing |

### Pin assignment {#pins}

The pin assignment is the same for HOME and LIMIT. The pin number is printed on the housing.

| Pin number | Function |
| --- | --- |
| 1 | GND |
| 2 | Switch or sensor input |
| 3 | 5 V output |

## Wiring a switch or a sensor {#wiring}

### Electrical connection {#electrical}

The input (pin 2) is pulled up to 3.3 V. To connect a switch, connect it between GND (pin 1) and the input (pin 2). When the switch closes, the input is connected to GND and its voltage falls from 3.3 V (HIGH) to 0 V (LOW). **A switch is on when its input is LOW.**

The firmware and the driver respond when the switch turns on, that is, when the input falls from HIGH to LOW (a falling edge). So that the board finds the home position, the mechanism and the switch must be combined so that the input goes from HIGH to LOW at the home position. What the board does when the switch turns on is set with [`/setHomeSwMode`](../reference/home-and-limit-sensors.md#sethomeswmode) and [`/setLimitSwMode`](../reference/home-and-limit-sensors.md#setlimitswmode); see [Hard stop mode and `SW_USER`](../guides/homing-and-position.md#sw-mode).

### Which switch to use {#switches}

- **A switch with a normally open (NO) contact** is the simplest. Connect the NO contact between pin 1 and pin 2. The input is HIGH normally and goes LOW when the switch is operated.
- **A switch with a normally closed (NC) contact** has the opposite behavior. The input is LOW normally, so the board sees the switch as on while the mechanism is away from the switch, and the input goes HIGH when the switch is operated. Do not use the NC contact. If the switch has a changeover contact, use the NO terminal and the common terminal.
- **A sensor** needs an output that goes to 0 V when the sensor is on. Connect the output to pin 2, the ground of the sensor to pin 1, and the power of the sensor to pin 3 (5 V).

The settings `/setHomeSwMode` and `/setLimitSwMode` do not invert the signal; they only choose what the board does when the switch is on.

### Example: the photo interrupter EE-SX671A {#ee-sx671a}

The connection of the photo interrupter [EE-SX671A](http://www.ia.omron.com/product/item/2219/) of Omron is as follows.

![EE-SX671A Diagram](http://ponoor.com/manage/wp-content/uploads/2020/10/ee-sx67.jpeg)

| Pin number | Function | Sensor pin |
| --- | --- | --- |
| 1 | GND | - |
| 2 | Switch or sensor input | OUT |
| 3 | 5 V output | + |

### Light-on and dark-on sensors {#light-dark}

Think about this carefully before you buy a sensor.

![Dark on or Light on](http://ponoor.com/manage/wp-content/uploads/2020/10/sensor_dark_light.png)

In the left picture, the light enters the sensor at the home position. In the right picture, the light is blocked at the home position.

Some sensors turn on when the light enters (light-on), and some turn on when the light is blocked (dark-on). Some sensors can be switched. With the Omron sensor above, the operation changes when you connect the "L" terminal to the "+" terminal.

Combine the mechanism and the sensor so that the input goes from HIGH to LOW at the home position.

## Related commands and settings {#related}

<!-- osc-related: /setHomeSwMode, /setLimitSwMode, /getHomeSw, /getLimitSw -->
<!-- generated:begin osc-related /setHomeSwMode, /setLimitSwMode, /getHomeSw, /getLimitSw -->
**Related commands**

| Command | Arguments | Description |
| --- | --- | --- |
| [`/setHomeSwMode`](../reference/home-and-limit-sensors.md#sethomeswmode) | (int)motorID (bool)SW_MODE | Sets switch mode whether to stop immediately when the HOME switch terminal state changes (falling edge). |
| [`/setLimitSwMode`](../reference/home-and-limit-sensors.md#setlimitswmode) | (int)motorID (bool)SW_MODE | Sets the Switch mode whether to stop the motor immediately when the LIMIT switch terminal condition is changed. |
| [`/getHomeSw`](../reference/home-and-limit-sensors.md#gethomesw) | (int)motorID | Gets the status of the HOME switch, closed or opened. |
| [`/getLimitSw`](../reference/home-and-limit-sensors.md#getlimitsw) | (int)motorID | Returns the status of LIMIT switch. |
<!-- generated:end osc-related /setHomeSwMode, /setLimitSwMode, /getHomeSw, /getLimitSw -->

<!-- osc-settings: driverSettings.homeSwMode, driverSettings.limitSwMode, alarmAndReport.reportHomeSwStatus, alarmAndReport.reportLimitSwStatus -->
<!-- generated:begin osc-settings driverSettings.homeSwMode, driverSettings.limitSwMode, alarmAndReport.reportHomeSwStatus, alarmAndReport.reportLimitSwStatus -->
**Related configuration items**

| Key | Name | Commands |
| --- | --- | --- |
| [`driverSettings.homeSwMode`](configuration-items.md#driversettings-homeswmode) | Home switch won't cause HardStop | `/setHomeSwMode` |
| [`driverSettings.limitSwMode`](configuration-items.md#driversettings-limitswmode) | Limit switch won't cause HardStop | `/setLimitSwMode` |
| [`alarmAndReport.reportHomeSwStatus`](configuration-items.md#alarmandreport-reporthomeswstatus) | Report HOME switch status | `/enableHomeSwReport` |
| [`alarmAndReport.reportLimitSwStatus`](configuration-items.md#alarmandreport-reportlimitswstatus) | Report LIMIT switch status | `/enableLimitSwReport` |
<!-- generated:end osc-settings driverSettings.homeSwMode, driverSettings.limitSwMode, alarmAndReport.reportHomeSwStatus, alarmAndReport.reportLimitSwStatus -->
