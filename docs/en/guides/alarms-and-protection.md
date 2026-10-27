---
title: Alarms and protection
---

# Alarms and protection

The motor driver chips detect four kinds of alarms: a drop of the supply voltage (UVLO), overtemperature, overcurrent and stall. This page explains what each alarm means, what the driver does, and what the board sends to you.

## Overview {#overview}

Each alarm has a flag in the status of the driver. The board reads the status of every driver every 5 ms, and sends a message when the status changes (see [Timing of the notifications](#timing)). Whether a message is sent is set for each alarm with an `/enable...Report` command. The alarms differ in what the driver does:

| Alarm | What the driver does | Message |
| --- | --- | --- |
| Undervoltage lockout (UVLO) | turns off the outputs: the motor is HiZ | [`/uvlo`](../reference/automatically-sent-messages.md#uvlo) |
| Overtemperature | warning: nothing. Bridge shutdown or device shutdown: the motor is HiZ | [`/thermalStatus`](../reference/automatically-sent-messages.md#thermalstatus) |
| Overcurrent | turns off the outputs: the motor is HiZ | [`/overCurrent`](../reference/automatically-sent-messages.md#overcurrent) |
| Stall | nothing (only a flag) | [`/stall`](../reference/automatically-sent-messages.md#stall) |

The PowerSTEP01 of the STEP400 and the L6470 of the STEP800 differ in the details. This page notes where they do.

## The alarms {#alarms}

### UVLO: undervoltage lockout {#uvlo}

UVLO happens when the supply voltage of the driver falls below the turn-off threshold. The driver turns off all the outputs at once, so the motor is HiZ and cannot be operated while the condition lasts. The condition ends when the voltage is above the turn-on threshold; then see [Resuming](#resuming). The thresholds are different on the STEP400 and on the STEP800; see the datasheets of the driver chips.

[`/enableUvloReport`](../reference/alarm-settings.md#enableuvloreport) turns the notification on (the message [`/uvlo`](../reference/automatically-sent-messages.md#uvlo) is sent when the state changes). [`/getUvlo`](../reference/alarm-settings.md#getuvlo) reads the state.

### Overtemperature {#thermal}

The driver monitors its temperature. At the warning level, only a flag is set and the operation is not limited. At the shutdown level the outputs are turned off, so the motor is HiZ. The STEP400 has two shutdown levels (bridge shutdown and device shutdown); the STEP800 has one. The temperatures are listed at [`/thermalStatus`](../reference/automatically-sent-messages.md#thermalstatus).

[`/enableThermalStatusReport`](../reference/alarm-settings.md#enablethermalstatusreport) turns the notification on, and [`/getThermalStatus`](../reference/alarm-settings.md#getthermalstatus) reads the state. The motor is HiZ with or without the notification. After a shutdown, see [Resuming](#resuming).

### Overcurrent {#overcurrent}

The driver measures the current of the power transistors. When the current exceeds the threshold, the driver turns off the outputs (the firmware keeps this protection on), so the motor is HiZ. The protection is a critical one; it is not meant to be turned off.

[`/setOverCurrentThreshold`](../reference/alarm-settings.md#setovercurrentthreshold) sets the threshold, [`/enableOverCurrentReport`](../reference/alarm-settings.md#enableovercurrentreport) turns the notification on, and [`/overCurrent`](../reference/automatically-sent-messages.md#overcurrent) is sent. To start the motor again after the cause has gone, see [Resuming](#resuming) (a motor with the electromagnetic brake needs `/activate 1` first).

### Stall {#stall}

The stall detection lets the driver find out, from the current of the motor, that the motor can no longer turn against the load. The driver only sets a flag; it does not stop the motor. The detection works only in voltage mode on the STEP400: it is not available in current mode.

[`/setStallThreshold`](../reference/alarm-settings.md#setstallthreshold) sets the threshold and [`/enableStallReport`](../reference/alarm-settings.md#enablestallreport) turns the notification on. See [Using the stall detection](#using-stall).

## Timing of the notifications {#timing}

- The board reads the state of the drivers every 5 ms. The messages [`/busy`](../reference/automatically-sent-messages.md#busy), [`/HiZ`](../reference/automatically-sent-messages.md#hiz), [`/uvlo`](../reference/automatically-sent-messages.md#uvlo), [`/thermalStatus`](../reference/automatically-sent-messages.md#thermalstatus) and so on are sent when the state changes, not at every read.
- [`/overCurrent`](../reference/automatically-sent-messages.md#overcurrent) and [`/stall`](../reference/automatically-sent-messages.md#stall) are sent at once when the condition starts. While it lasts, they are sent at most every 200 ms for each motor and each kind. A detection within the 200 ms is not lost; it gives one message at the end of the interval. A detection while the notification is disabled is not sent later.
- [`/getStatus`](../reference/motor-driver-settings.md#getstatus) and [`/getStatusList`](../reference/motor-driver-settings.md#getstatuslist) read the status of the driver without clearing the latched flags (OCD, stall, UVLO, SW_EVN and so on). Only the poll of the board every 5 ms clears them, so a `/getStatus` or `/getStatusList` sent right after another one can show a flag that the earlier reply showed (until the next poll, up to 5 ms).

## When the driver goes HiZ by itself {#hiz-by-itself}

When the driver makes the motor HiZ because of an overcurrent shutdown, an overtemperature shutdown or UVLO, the board does the following, in this order (each message follows its own setting):

1. [`/HiZ`](../reference/automatically-sent-messages.md#hiz) (when [`/enableHizReport`](../reference/motor-driver-settings.md#enablehizreport) is on).
2. If the motor is in the servo mode: the servo mode is cancelled and `/error/command ServoModeCancelledOnHiZ` is sent. Nothing is sent to the driver.
3. If the motor has an electromagnetic brake that is released: the brake is engaged at the next status read (up to 5 ms later) and `/error/command BrakeEngagedOnHiZ` is sent. See [Electromagnetic brake](electromagnetic-brake.md#transitions).

The errors follow [`/reportError`](../reference/system-settings.md#reporterror). The commands that make a motor HiZ (`/softHiZ`, `/hardHiZ`, `/activate 0`, `/free`, `/resetMotorDriver`) cancel the servo mode first and do not send `ServoModeCancelledOnHiZ`.

### Resuming {#resuming}

After the cause (the overcurrent, the temperature or the supply voltage) is gone, the motor is still HiZ. Start it again with a motion command. A motor with the electromagnetic brake enabled needs `/activate 1` first, because the board has engaged its brake (a motion command is rejected with `BrakeEngaged` while the brake is engaged). To resume the servo mode, send `/enableServoMode 1` (after `/activate 1` for a motor with the brake); the current position becomes the target. If the cause remains, the driver shuts down again.

## Thresholds and currents {#thresholds}

The thresholds of the overcurrent and of the stall are set with a number, and the current of a number is

> current = (value + 1) × step

The step depends on the driver:

| | Overcurrent | Stall |
| --- | --- | --- |
| STEP400 (PowerSTEP01) | 312.5 mA | 312.5 mA |
| STEP800 (L6470) | 375 mA | 31.25 mA |

The value 0 is one step, not 0 A. The datasheet of the PowerSTEP01 gives these thresholds as voltages (31.25 mV steps for the stall); the conversion to the current is the one of the sensing circuit of the STEP400. The same kind of conversion applies to TVAL in current mode, with a step of 78.125 mA ([Voltage mode and current mode](voltage-and-current-mode.md#current-mode-setting)). The ranges and the initial values depend on the board, so they are written only in [`/setOverCurrentThreshold`](../reference/alarm-settings.md#setovercurrentthreshold) and [`/setStallThreshold`](../reference/alarm-settings.md#setstallthreshold).

## Using the stall detection {#using-stall}

The stall detection compares the current of the motor with a threshold. Find the threshold by trial: it should be as close as possible to the current that actually flows, and a little above it. A small loss of steps cannot be detected, but a large position error may be detected.

The current depends on KVAL and on the back-EMF compensation, so adjust them to the motor and to the supply voltage first: see [Voltage mode and current mode](voltage-and-current-mode.md#voltage-mode-setting).

## Switches that prohibit a motion {#switches}

The motion that the HOME and LIMIT switches prohibit ([`/setProhibitMotionOnHomeSw`](../reference/alarm-settings.md#setprohibitmotiononhomesw), [`/setProhibitMotionOnLimitSw`](../reference/alarm-settings.md#setprohibitmotiononlimitsw)) is described in [Homing and position management](homing-and-position.md#collision-prevention).

## Related commands and settings {#related}

<!-- osc-related: alarm, /getStatus, /getStatusList -->
<!-- generated:begin osc-related alarm, /getStatus, /getStatusList -->
**Related commands**

| Command | Arguments | Description |
| --- | --- | --- |
| [`/enableUvloReport`](../reference/alarm-settings.md#enableuvloreport) | (int)motorID (bool)enable | Set the notification message when UVLO (Undervoltage Lockout) occurs in the specified motor driver. |
| [`/getUvlo`](../reference/alarm-settings.md#getuvlo) | (int)motorID | Gets the current state of UVLO |
| [`/enableThermalStatusReport`](../reference/alarm-settings.md#enablethermalstatusreport) | (int)motorID (bool)enable | Sends a notification message when a change in the temperature status (thermalStatus) of the specified motor driver is detected. |
| [`/getThermalStatus`](../reference/alarm-settings.md#getthermalstatus) | (int)motorID | Gets the current condition of the ThermalStatus. |
| [`/enableOverCurrentReport`](../reference/alarm-settings.md#enableovercurrentreport) | (int)motorID (bool)enable | Set to send a notification when the specified motor driver goes into an overcurrent state (OCD, Over Current Detection). |
| [`/setOverCurrentThreshold`](../reference/alarm-settings.md#setovercurrentthreshold) | (int)motorID (int)OCD_TH | Sets the overcurrent threshold. |
| [`/getOverCurrentThreshold`](../reference/alarm-settings.md#getovercurrentthreshold) | (int)motorID | Get the threshold of overcurrent. |
| [`/enableStallReport`](../reference/alarm-settings.md#enablestallreport) | (int)motorID (bool)enable | The threshold can be set by `/setStallThreshold`. |
| [`/setStallThreshold`](../reference/alarm-settings.md#setstallthreshold) | (int)motorID (int)STALL_TH | Sets the threshold for stall detection. |
| [`/getStallThreshold`](../reference/alarm-settings.md#getstallthreshold) | (int)motorID | Gets the stall detection threshold. |
| [`/setProhibitMotionOnHomeSw`](../reference/alarm-settings.md#setprohibitmotiononhomesw) | (int)motorID (bool)enable | Prohibits any motion commands towards the origin point when the HOME switch is activated. |
| [`/getProhibitMotionOnHomeSw`](../reference/alarm-settings.md#getprohibitmotiononhomesw) | (int)motorID | Returns whether the motion command towards the origin point is prohibited when the HOME switch is activated. |
| [`/setProhibitMotionOnLimitSw`](../reference/alarm-settings.md#setprohibitmotiononlimitsw) | (int)motorID (bool)enable | Prohibits any motion commands towards the leaving direction from origin point, when the LIMIT switch is activated. |
| [`/getProhibitMotionOnLimitSw`](../reference/alarm-settings.md#getprohibitmotiononlimitsw) | (int)motorID | Returns whether the motion command towards reverse direction to the origin point is prohibited when the LIMIT switch is activated. |
| [`/getStatus`](../reference/motor-driver-settings.md#getstatus) | (int)motorID | Gets the STATUS of the motor driver (PowerSTEP01 for STEP400/L6470 for STEP800). |
| [`/getStatusList`](../reference/motor-driver-settings.md#getstatuslist) | - | Gets the STATUS registers of all motors at once. |
<!-- generated:end osc-related alarm, /getStatus, /getStatusList -->

<!-- osc-settings: alarmAndReport.reportUVLO, alarmAndReport.reportThermalStatus, alarmAndReport.reportOCD, alarmAndReport.reportStall, alarmAndReport.OCThreshold, voltageMode.STALL_TH -->
<!-- generated:begin osc-settings alarmAndReport.reportUVLO, alarmAndReport.reportThermalStatus, alarmAndReport.reportOCD, alarmAndReport.reportStall, alarmAndReport.OCThreshold, voltageMode.STALL_TH -->
**Related configuration items**

| Key | Name | Commands |
| --- | --- | --- |
| [`alarmAndReport.reportUVLO`](../connections/configuration-items.md#alarmandreport-reportuvlo) | Report undervoltage lockout | `/enableUvloReport` |
| [`alarmAndReport.reportThermalStatus`](../connections/configuration-items.md#alarmandreport-reportthermalstatus) | Report thermal status of driver chip | `/enableThermalStatusReport` |
| [`alarmAndReport.reportOCD`](../connections/configuration-items.md#alarmandreport-reportocd) | Report overcurrent detection | `/enableOverCurrentReport` |
| [`alarmAndReport.reportStall`](../connections/configuration-items.md#alarmandreport-reportstall) | Report motor stall detection | `/enableStallReport` |
| [`alarmAndReport.OCThreshold`](../connections/configuration-items.md#alarmandreport-octhreshold) | Overcurrent threshold | `/setOverCurrentThreshold` |
| [`voltageMode.STALL_TH`](../connections/configuration-items.md#voltagemode-stall_th) | STALL_TH | `/setStallThreshold` |
<!-- generated:end osc-settings alarmAndReport.reportUVLO, alarmAndReport.reportThermalStatus, alarmAndReport.reportOCD, alarmAndReport.reportStall, alarmAndReport.OCThreshold, voltageMode.STALL_TH -->
