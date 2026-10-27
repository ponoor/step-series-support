---
title: Motor driver settings
---

# Motor driver settings

## Motor driver settings

<!-- osc: /setMicrostepMode -->
<!-- generated:begin osc /setMicrostepMode -->
### `/setMicrostepMode` (int)motorID (int)STEP_SEL {#setmicrostepmode}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| STEP_SEL | int | 0-7 | Microstepping mode |

`STEP_SEL`

| Value | Meaning |
| --- | --- |
| 0 | Full-step |
| 1 | Half-step |
| 2 | 1/4 microstep |
| 3 | 1/8 microstep |
| 4 | 1/16 microstep |
| 5 | 1/32 microstep |
| 6 | 1/64 microstep |
| 7 | 1/128 microstep |

#### Executable timing

High Z state

#### Description

Sets the microstepping mode.  
In the constant-current control mode (current mode), only full-step to 1/16 microstep is available.

The motor must be HiZ. A motor holding its position is not HiZ: send [`/softHiZ`](motor-control.md#softhiz) or [`/hardHiZ`](motor-control.md#hardhiz) first, otherwise `MotorNotHiZ` is replied and nothing is applied. On STEP400 in the current mode, a step mode finer than 1/16 replies `CommandIgnored`.

A value outside 0-7 is not rejected: it is converted to 8 bits and then limited to 0-7 (-1 becomes 7, 256 becomes 0).

#### Changes

- **v2.2.0**: The motor must be HiZ; otherwise `/error/command MotorNotHiZ` is replied and nothing is applied. Before, the driver ignored the write while the firmware variable and the saved configuration took the new value.
- **v2.2.0**: STEP400 in the current mode: a step mode finer than 1/16 replies `CommandIgnored` (the PowerSTEP01 current mode goes up to 1/16).

#### Errors

- `MotorNotHiZ`: The command writes a driver register that can be written only while the outputs are HiZ, and the motor is not HiZ. A motor holding its position is not HiZ: send `/softHiZ` or `/hardHiZ` first. Nothing is applied. Added in v2.2.0.
- `CommandIgnored`: The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`).

#### Initial value

- `STEP_SEL`: 7 (1/128 microstep) ([driverSettings.stepMode](../connections/configuration-items.md#driversettings-stepmode))

#### See also

[`/getMicrostepMode`](motor-driver-settings.md#getmicrostepmode), [`/setCurrentMode`](voltage-and-current-mode-settings.md#setcurrentmode)
<!-- generated:end osc /setMicrostepMode -->

<!-- osc: /getMicrostepMode -->
<!-- generated:begin osc /getMicrostepMode -->
### `/getMicrostepMode` (int)motorID {#getmicrostepmode}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Gets the mode of microstepping. See [`/setMicrostepMode`](motor-driver-settings.md#setmicrostepmode) for STEP_SEL.

#### Response

```
/microstepMode (int)motorID (int)STEP_SEL
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| STEP_SEL | int | 0-7 | Microstepping mode |

`STEP_SEL`

| Value | Meaning |
| --- | --- |
| 0 | Full-step |
| 1 | Half-step |
| 2 | 1/4 microstep |
| 3 | 1/8 microstep |
| 4 | 1/16 microstep |
| 5 | 1/32 microstep |
| 6 | 1/64 microstep |
| 7 | 1/128 microstep |
<!-- generated:end osc /getMicrostepMode -->

<!-- osc: /enableLowSpeedOptimize -->
<!-- generated:begin osc /enableLowSpeedOptimize -->
### `/enableLowSpeedOptimize` (int)motorID (bool)enable {#enablelowspeedoptimize}

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

When the motor is stopped

#### Description

Enable/disable low speed optimization feature which compensate phase current distortion at a very low speed using a small driving voltage. When this optimization is enabled, speed profile minimum speed (`Min speed`) is force to zero. Only work with voltage mode. See data sheets for details.

#### Changes

- **v2.2.0**: The motor must be stopped or HiZ; a turning motor replies `/error/command MotorNotStopped` and nothing is applied.

#### Errors

- `MotorNotStopped`: The command writes a driver register that can be written only while the motor is stopped or HiZ, and the motor is turning. Nothing is applied. Added in v2.2.0.

#### Initial value

- `enable`: false (Disable) ([voltageMode.lowSpeedOptimizeEnable](../connections/configuration-items.md#voltagemode-lowspeedoptimizeenable))

#### See also

[`/setLowSpeedOptimizeThreshold`](motor-driver-settings.md#setlowspeedoptimizethreshold), [`/setMinSpeed`](speed-profile.md#setminspeed)
<!-- generated:end osc /enableLowSpeedOptimize -->

<!-- osc: /setLowSpeedOptimizeThreshold -->
<!-- generated:begin osc /setLowSpeedOptimizeThreshold -->
### `/setLowSpeedOptimizeThreshold` (int)motorID (float)lowSpeedOptimizationThreshold {#setlowspeedoptimizethreshold}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| lowSpeedOptimizationThreshold | float | 0-976.3 step/s | Low speed optimization threshold |

#### Executable timing

Always

#### Description

Set the threshold for phase current distortion compensation at very low speed. For details, refer to "Low speed optimization" section in the corresponding datasheet.

No reply is sent. Read the value back with [`/getLowSpeedOptimizeThreshold`](motor-driver-settings.md#getlowspeedoptimizethreshold).

While the low speed optimization is enabled, the motor must be stopped or HiZ; a turning motor replies `MotorNotStopped` and nothing is applied.

#### Changes

- **v2.2.0**: While the low speed optimization is enabled, a turning motor replies `/error/command MotorNotStopped` and nothing is applied.

#### Errors

- `MotorNotStopped`: The command writes a driver register that can be written only while the motor is stopped or HiZ, and the motor is turning. Nothing is applied. Added in v2.2.0.

#### Initial value

- `lowSpeedOptimizationThreshold`: 20 ([voltageMode.lowSpeedOptimize](../connections/configuration-items.md#voltagemode-lowspeedoptimize))

#### See also

[`/getLowSpeedOptimizeThreshold`](motor-driver-settings.md#getlowspeedoptimizethreshold), [`/enableLowSpeedOptimize`](motor-driver-settings.md#enablelowspeedoptimize)
<!-- generated:end osc /setLowSpeedOptimizeThreshold -->

<!-- osc: /getLowSpeedOptimizeThreshold -->
<!-- generated:begin osc /getLowSpeedOptimizeThreshold -->
### `/getLowSpeedOptimizeThreshold` (int)motorID {#getlowspeedoptimizethreshold}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Gets the current value of the low speed optimization threshold.

#### Response

```
/lowSpeedOptimizeThreshold (int)motorID (float)lowSpeedOptimizeThreshold (int)optimizationEnabled
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| lowSpeedOptimizeThreshold | float | 0-976.3 step/s | Low speed optimization threshold |
| optimizationEnabled | int |  |  |

`optimizationEnabled`

| Value | Meaning |
| --- | --- |
| 1 | Low speed optimization enabled |
| 0 | Low speed optimization disabled |

##### Changes

- **v2.2.0**: The third argument `optimizationEnabled` is sent with the integer type tag `i` (0 / 1). Before, it used `T` / `F`. Clients that expect `T` / `F` must be updated.
<!-- generated:end osc /getLowSpeedOptimizeThreshold -->

## Getting the status

<!-- osc: /enableBusyReport -->
<!-- generated:begin osc /enableBusyReport -->
### `/enableBusyReport` (int)motorID (bool)enable {#enablebusyreport}

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

Automatically sends out notification if the BUSY status of the specified motor has changed. The notification message is same as the response from [`/getBusy`](motor-driver-settings.md#getbusy) command.

#### Response

[`/busy`](automatically-sent-messages.md#busy)

```
/busy (int)motorID (int)state
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| state | int |  |  |

`state`

| Value | Meaning |
| --- | --- |
| 1 | BUSY |
| 0 | Not BUSY |

#### Initial value

- `enable`: false (Disable) ([alarmAndReport.reportBUSY](../connections/configuration-items.md#alarmandreport-reportbusy))
<!-- generated:end osc /enableBusyReport -->

<!-- osc: /getBusy -->
<!-- generated:begin osc /getBusy -->
### `/getBusy` (int)motorID {#getbusy}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Returns the BUSY state of the specified motor.

#### Response

[`/busy`](automatically-sent-messages.md#busy)

```
/busy (int)motorID (int)state
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| state | int |  |  |

`state`

| Value | Meaning |
| --- | --- |
| 1 | BUSY |
| 0 | Not BUSY |
<!-- generated:end osc /getBusy -->

<!-- osc: /enableHizReport -->
<!-- generated:begin osc /enableHizReport -->
### `/enableHizReport` (int)motorID (bool)enable {#enablehizreport}

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

Following message is sent automatically when there is a change in the High Z (high impedance) state of the specified motor.

#### Response

[`/HiZ`](automatically-sent-messages.md#hiz)

```
/HiZ (int)motorID (int)state
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| state | int | 0-1 | 1 if High Z state, 0 if not High Z state. |

#### Initial value

- `enable`: false (Disable) ([alarmAndReport.reportHiZ](../connections/configuration-items.md#alarmandreport-reporthiz))
<!-- generated:end osc /enableHizReport -->

<!-- osc: /getHiZ -->
<!-- generated:begin osc /getHiZ -->
### `/getHiZ` (int)motorID {#gethiz}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Requests the High Z (high impedance) state of the specified motor.

#### Response

[`/HiZ`](automatically-sent-messages.md#hiz)

```
/HiZ (int)motorID (int)state
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| state | int | 0-1 | 1 if High Z state, 0 if not High Z state. |
<!-- generated:end osc /getHiZ -->

<!-- osc: /enableDirReport -->
<!-- generated:begin osc /enableDirReport -->
### `/enableDirReport` (int)motorID (bool)enable {#enabledirreport}

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

Following message is sent automatically when there is a change in the direction of the specified motor.

#### Response

[`/dir`](automatically-sent-messages.md#dir)

```
/dir (int)motorID (int)direction
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| direction | int |  |  |

`direction`

| Value | Meaning |
| --- | --- |
| 1 | Forward |
| 0 | Reverse |

#### Initial value

- `enable`: false (Disable) ([alarmAndReport.reportDir](../connections/configuration-items.md#alarmandreport-reportdir))
<!-- generated:end osc /enableDirReport -->

<!-- osc: /getDir -->
<!-- generated:begin osc /getDir -->
### `/getDir` (int)motorID {#getdir}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Requests the direction of the specified motor.

#### Changes

- **v2.2.0**: `/getDir 255` (all motors) returns the direction. It returned the HiZ state.

#### Response

[`/dir`](automatically-sent-messages.md#dir)

```
/dir (int)motorID (int)direction
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| direction | int |  |  |

`direction`

| Value | Meaning |
| --- | --- |
| 1 | Forward |
| 0 | Reverse |
<!-- generated:end osc /getDir -->

<!-- osc: /enableMotorStatusReport -->
<!-- generated:begin osc /enableMotorStatusReport -->
### `/enableMotorStatusReport` (int)motorID (bool)enable {#enablemotorstatusreport}

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

Following message will be sent automatically when there is conditional change in the operating status (MOT_STATUS) of the specified motor. The response message is same as the reply from the [`/getMotorStatus`](motor-driver-settings.md#getmotorstatus) command.

#### Response

[`/motorStatus`](automatically-sent-messages.md#motorstatus)

```
/motorStatus (int)motorID (int)MOT_STATUS
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| MOT_STATUS | int | 0-3 | Motor status |

`MOT_STATUS`

| Value | Meaning |
| --- | --- |
| 0 | Stopped |
| 1 | Acceleration |
| 2 | Deceleration |
| 3 | Constant speed |

#### Initial value

- `enable`: false (Disable) ([alarmAndReport.reportMotorStatus](../connections/configuration-items.md#alarmandreport-reportmotorstatus))
<!-- generated:end osc /enableMotorStatusReport -->

<!-- osc: /getMotorStatus -->
<!-- generated:begin osc /getMotorStatus -->
### `/getMotorStatus` (int)motorID {#getmotorstatus}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Gets the operating status (MOT_STATUS) of the specified motor.

#### Response

[`/motorStatus`](automatically-sent-messages.md#motorstatus)

```
/motorStatus (int)motorID (int)MOT_STATUS
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| MOT_STATUS | int | 0-3 | Motor status |

`MOT_STATUS`

| Value | Meaning |
| --- | --- |
| 0 | Stopped |
| 1 | Acceleration |
| 2 | Deceleration |
| 3 | Constant speed |
<!-- generated:end osc /getMotorStatus -->

<!-- osc: /setPositionReportInterval -->
<!-- generated:begin osc /setPositionReportInterval -->
### `/setPositionReportInterval` (int)motorID (int)interval {#setpositionreportinterval}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| interval | int | 0-65535 ms | transmit interval |

#### Executable timing

Always

#### Description

Send the current position (`ABS_POS`) of the specified motor with the specified interval. Disabled with the interval 0.

When this function enabled, `/setPositionListReportInterval` will be automatically disabled and stop the transmitting.

An interval above 65535 replies `CommandIgnored` and nothing is applied. A negative interval disables the report, as 0.

#### Changes

- **v2.2.0**: A value above 65535 replies `/error/command CommandIgnored` and nothing is applied. Before, 32768 and above were read as negative and disabled the report. A negative interval still disables it.
- **v2.2.0**: When the report is enabled (interval above 0) for one motor, the saved position list report interval is cleared too, as it was for 255. Before, a configuration saved after switching from the list report to one motor's report started the list report again at the next start and cleared the motor's report.

#### Response

[`/position`](automatically-sent-messages.md#position)

```
/position (int)motorID (int)ABS_POS
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| ABS_POS | int | -2097152-2097151 | current position |

#### Errors

- `CommandIgnored`: The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`).

#### Initial value

- `interval`: 0 ([alarmAndReport.reportPositionInterval](../connections/configuration-items.md#alarmandreport-reportpositioninterval))

#### See also

[`/getPosition`](position-management.md#getposition), [`/setPositionListReportInterval`](motor-driver-settings.md#setpositionlistreportinterval)
<!-- generated:end osc /setPositionReportInterval -->

<!-- osc: /setPositionListReportInterval -->
<!-- generated:begin osc /setPositionListReportInterval -->
### `/setPositionListReportInterval` (int)interval {#setpositionlistreportinterval}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| interval | int | 0-65535 ms | transmit interval |

#### Executable timing

Always

#### Description

Send a single message with a list of the current position (`ABS_POS`) of all motors with the specified interval. Disabled with the interval 0.

When this function enabled, `/setPositionReportInterval` will be disabled automatically for all motors and stop the transmitting.

An interval above 65535 replies `CommandIgnored` with the motor ID 255 and nothing is applied. A negative interval disables the report, as 0.

#### Changes

- **v2.2.0**: A value above 65535 replies `/error/command CommandIgnored 255` and nothing is applied. Before, 32768 and above were read as negative and disabled the report. A negative interval still disables it.

#### Response

[`/positionList`](automatically-sent-messages.md#positionlist)

```
/positionList (int)position1 ... (int)positionN
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| position1 ... positionN | int | -2097152-2097151 | current position of the motor #n |

#### Errors

- `CommandIgnored`: The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`).

#### Initial value

- `interval`: 0 ([alarmAndReport.reportPositionListInterval](../connections/configuration-items.md#alarmandreport-reportpositionlistinterval))

#### See also

[`/getPositionList`](position-management.md#getpositionlist), [`/setPositionReportInterval`](motor-driver-settings.md#setpositionreportinterval)
<!-- generated:end osc /setPositionListReportInterval -->

## Debug

<!-- osc: /getAdcVal -->
<!-- generated:begin osc /getAdcVal -->
### `/getAdcVal` (int)motorID {#getadcval}

Available on STEP400 only.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Acquires ADC_OUT register values from the PowerSTEP01 chip. This register stores 5-bit AD-converted voltage reading from ADC pin. This pin is pull-upped with 10kOhm resistor and wired to LIMITSW connector.

STEP400 only. The firmware also accepts the command on STEP800, but it is not meaningful there.

#### Response

```
/adcVal (int)motorID (int)ADC_OUT
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| ADC_OUT | int | 0-31 | 5bit reading of ADC_OUT register |
<!-- generated:end osc /getAdcVal -->

<!-- osc: /getStatus -->
<!-- generated:begin osc /getStatus -->
### `/getStatus` (int)motorID {#getstatus}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Gets the STATUS of the motor driver (PowerSTEP01 for STEP400/L6470 for STEP800). The STATUS includes the status of the motor, alarms and switches.

Refer to "STATUS" in the data sheet for the information contained in the registers. Some of bits are latched and reset when STATUS registers are read out. Because the device firmware constantly obtains the STATUS values, these values are immediately reset. It is possible to set up these events to be reported separately, so please use those commands.

This command does not clear the latched flags; only the status poll of the firmware (every 5 ms) does.

#### Changes

- **v2.2.0**: Reads the STATUS register with GetParam instead of GetStatus, so it no longer clears the latched driver flags (e.g. OCD, stall flags, UVLO, SW_EVN). The register values are the same. Only the status poll of the firmware (every 5 ms) clears them now, so a `/getStatus` sent right after another can show a flag the earlier reply showed (until the next poll, up to 5 ms).

#### Response

```
/status (int)motorID (int)status
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| status | int | 0-65535 | 16-bit STATUS register |

| Name of bits in STATUS (STEP400) | Name of bits in STATUS (STEP800) | The corresponding configuration commands |
| --- | --- | --- |
| UVLO | UVLO | [`/enableUvloReport`](alarm-settings.md#enableuvloreport) |
| UVLO_ADC | - | This feature is not available in STEP400 and is always disabled. |
| OCD | OCD | [`/enableOverCurrentReport`](alarm-settings.md#enableovercurrentreport) |
| STALL_A, STALL_B | STEP_LOSS_A, STEP_LOSS_B | [`/enableStallReport`](alarm-settings.md#enablestallreport) |
| CMD_ERROR | WRONG_CMD, NOTPREF_CMD | [`/reportError`](system-settings.md#reporterror) |
| TH_STATUS | TH_WRN, TH_SD | [`/enableThermalStatusReport`](alarm-settings.md#enablethermalstatusreport) |
| SW_EVN | SW_EVN | [`/enableSwEventReport`](home-and-limit-sensors.md#enablesweventreport) |
| MOT_STATUS | MOT_STATUS | [`/enableMotorStatusReport`](motor-driver-settings.md#enablemotorstatusreport) |
| SW_F | SW_F | [`/enableHomeSwReport`](home-and-limit-sensors.md#enablehomeswreport) |
| BUSY | BUSY | [`/enableBusyReport`](motor-driver-settings.md#enablebusyreport) |
| HiZ | HiZ | [`/enableHizReport`](motor-driver-settings.md#enablehizreport) |

#### See also

[`/getStatusList`](motor-driver-settings.md#getstatuslist)
<!-- generated:end osc /getStatus -->

<!-- osc: /getConfigRegister -->
<!-- generated:begin osc /getConfigRegister -->
### `/getConfigRegister` (int)motorID {#getconfigregister}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Acquires the CONFIG register value from the motor driver (PowerSTEP01 or L6470). The information stored in CONFIG register includes motor, alarm and switch status.

The CONFIG register stores various settings for the motor driver. Please refer the datasheet of the PowerSTEP01/L6470 for detail.

#### Response

```
/configRegister (int)motorID (int)CONFIG
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| CONFIG | int | 0-65535 | 16bit CONFIG register content |
<!-- generated:end osc /getConfigRegister -->

<!-- osc: /resetMotorDriver -->
<!-- generated:begin osc /resetMotorDriver -->
### `/resetMotorDriver` (int)motorID {#resetmotordriver}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Resets the motor driver (PowerSTEP01/L6470) and rewrites the setting.

With the electromagnetic brake enabled, the command is accepted only while the brake is engaged or after [`/free`](brake.md#free) (the motor is HiZ); otherwise it replies `CommandIgnored`. When it is accepted (also with the brake disabled), it cancels pending motion and the servo mode. A command that is refused (`CommandIgnored`) cancels nothing.

#### Changes

- **v2.2.0**: With the electromagnetic brake enabled, accepted only while the brake is engaged or after `/free`; otherwise `/error/command CommandIgnored`. Before, it made the driver HiZ with the brake released.
- **v2.2.0**: Cancels pending motion (a `/goTo` etc. waiting for the BUSY flag, the homing, the servo mode) when it is accepted, also with the brake disabled. A refused command (`CommandIgnored`) cancels nothing.
- **v2.2.0**: The settings applied again after the reset include those made with the Raw commands (see [`/setAccRaw`](speed-profile.md#setaccraw)).

#### Errors

- `CommandIgnored`: The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`).
<!-- generated:end osc /resetMotorDriver -->

<!-- osc: /getStatusList -->
<!-- generated:begin osc /getStatusList -->
### `/getStatusList` {#getstatuslist}

#### Argument

None

#### Executable timing

Always

#### Description

Gets the STATUS registers of all motors at once. See [`/getStatus`](motor-driver-settings.md#getstatus) for the contents of the register.

#### Changes

- **v2.2.0**: Reads the STATUS registers with GetParam instead of GetStatus, so it no longer clears the latched driver flags. See [`/getStatus`](motor-driver-settings.md#getstatus).

#### Response

```
/statusList (int)status1 ... (int)statusN
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| status1 ... statusN | int | 0-65535 |  |

#### See also

[`/getStatus`](motor-driver-settings.md#getstatus)
<!-- generated:end osc /getStatusList -->
