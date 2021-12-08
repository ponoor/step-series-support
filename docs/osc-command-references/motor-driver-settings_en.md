## Motor Driver Settings
### `/setMicrostepMode (int)motorID (int)STEP_SEL`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |
| STEP_SEL| 0-7 | Microstepping mode |

#### Executable timing
High Z state

#### Description
Switches the micro stepping mode.

| STEP_SEL | Micro stepping mode |
| --- | --- |
| 0 | Full-step |
| 1 | Half-step |
| 2 | 1/4 microstep |
| 3 | 1/8 microstep |
| 4 | 1/16 microstep |
| 5 | 1/32 microstep |
| 6 | 1/64 microstep |
| 7 | 1/128 microstep |

Initially, the microstep mode is set to 1/128.
In the constant-current control mode (current mode), only full-step to 1/16 microstep is available.

#### Initial value
7 (1/128 microstep)

### `/getMicrostepMode (int)motorID`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |

#### Executable timing
Always

#### Description
Gets the mode of microstepping. See [`/setMicrostepMode`](https://ponoor.com/en/docs/step-series/osc-command-reference/motordriver-settings/#setmicrostepmode_intmotorid_intstep_sel) for STEP_SEL.

#### Response
```
/microstepMode (int)motorID (int)STEP_SEL
```

### `/enableLowSpeedOptimize (int)motorID (bool)enable`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |
| enable | 0-1 | 1:Enable, 0:Disable |

#### Executable timing
When the motor is stopped.

#### Description
Enable/disable low speed optimization feature which compensate phase current distortion at a very low speed using a small driving voltage. When this optimization is enabled, speed profile minimum speed (`Min speed`) is force to zero. Only work with voltage mode. See data sheets for details. 

#### Initial value
0 (Disabled)

### `/setLowSpeedOptimizeThreshold (int)motorID (float)lowSpeedOptimizationThreshold`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |
| lowSpeedOptimizationThreshold| 0.0 - 976.3 [step/s] | Low speed optimization threshold |

#### Executable timing
When the motor is stopped.

#### Description
Set the threshold for phase current distortion compensation at very low speed. For details, refer to "Low speed optimization" section in the corresponding datasheet.

The response is same as the following [`getLowSpeedOptimizeThreshold`](https://ponoor.com/en/docs/step-series/osc-command-reference/motordriver-settings/#getlowspeedoptimizethreshold_intmotorid).

### `/getLowSpeedOptimizeThreshold (int)motorID`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |

#### Executable timing
Always

#### Description
Gets the current value of the low speed optimization threshold.

#### Response
```
/lowSpeedOptimizeThreshold (int)motorID (float)lowSpeedOptimizeThreshold
```

## Getting the status
### `/enableBusyReport (int)motorID (bool)enable`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |
| enable | 0-1 | 1:Enable, 0:Disable |

#### Executable timing
Always

#### Description
Automatically sends out notification if the BUSY status of the specified motor has changed. The notification message is same as the response from [`/getBusy`](https://ponoor.com/en/docs/step-series/osc-command-reference/motordriver-settings/#getbusy_intmotorid) command.

#### Initial value
0 (Disabled)

### `/getBusy (int)motorID`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |

#### Executable timing
Always

#### Description
Returns the BUSY state of the specified motor.

#### Response
```
/busy (int)motorID
```
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |
| state | 0-1 |  1: BUSY, 0: Not BUSY |

### `/enableHizReport (int)motorID (bool)enable`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |
| enable | 0-1 | 1:Enable, 0:Disable |

#### Executable timing
Always

#### Description
Following message is sent automatically when there is a change in the High Z (high impedance) state of the specified motor.

#### Initial value
0 (Disabled)

### `/getHiZ (int)motorID`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |

#### Executable timing
Always

#### Description
Requests the High Z (high impedance) state of the specified motor.

#### Response
```
/HiZ (int)motorID (bool)state
```
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |
| state | 0-1 | 1 if High Z state, 0 if not High Z state. |

### `/enableDirReport (int)motorID (bool)enable`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |
| enable | 0-1 | 1:Enable, 0:Disable |

#### Executable timing
Always

#### Description
Following message is sent automatically when there is a change in the direction of the specified motor.

#### Initial value
0 (Disabled)

### `/getDir (int)motorID`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |

#### Executable timing
Always

#### Description
Requests the direction of the specified motor.

#### Response
```
/dir (int)motorID (bool)direction
```
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |
| direction | 0-1 | 1: Forward, 0:Reverse |

### `/enableMotorStatusReport (int)motorID (bool)enable`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |
| enable | 0-1 | 1:Enable, 0:Disable |

#### Executable timing
Always

#### Description
Following message will be sent automatically when there is conditional change in the operating status (MOT_STATUS) of the specified motor. The response message is same as the reply from the [`/getMotorStatus`](https://ponoor.com/en/docs/step-series/osc-command-reference/motordriver-settings/#getmotorstatus_intmotorid) command.

#### Initial value
0 (Disabled)

### `/getMotorStatus (int)motorID`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |

#### Executable timing
Always

#### Description
Gets the operating status (MOT_STATUS) of the specified motor.

#### Response
```
/motorStatus (int)motorID (int)MOT_STATUS
```
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  Motor ID |
| MOT_STATUS | 0-3 | Motor status |

##### Motor status
| MOT_STATUS | Motor status |
| --- | --- |
| 0 | Stopped |
| 1 | Acceleration |
| 2 | Deceleration |
| 3 | Constant speed |

## Debug

### `/getAdcVal (int)motorID`
**STEP400 only**
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |

#### Executable timing
Always

#### Description
Acquires ADC_OUT register values from the PowerSTEP01 chip. This register stores 5-bit AD-converted voltage reading from ADC pin. This pin is pull-upped with 10kOhm resistor and wired to LIMITSW connector.

#### Response
```
/adcVal (int)motorID (int)ADC_OUT
```
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4, 255 | Motor ID |
| ADC_OUT | 0-31 | 5bit reading of ADC_OUT register |

### `/getStatus (int)motorID`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |

#### Executable timing
Always

#### Description
Gets the STATUS of the motor driver (PowerSTEP01 for STEP400/L6470 for STEP800). The STATUS includes the status of the motor, alarms and switches.

#### Response
```
/status (int)motorID (int)status
```
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |
| status | 0-65535(0xFFFF) | 16-bit STATUS register |

Refer to "STATUS" in the data sheet for the information contained in the registers. Some of bits are latched and reset when STATUS registers are read out. Because the device firmware constantly obtains the STATUS values, these values are immediately reset. It is possible to set up these events to be reported separately, so please use those commands.

| Name of bits in STATUS (STEP400) | Name of bits in STATUS (STEP800) | The corresponding configuration commands |
| --- | --- | --- |
| UVLO | UVLO | [`/enableUvloReport`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#enableuvloreport_intmotorid_boolenable) |
| UVLO_ADC | - | This feature is not available in STEP 400 and is always disabled. |
| OCD | OCD | [`/enableOverCurrentReport`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#enableovercurrentreport_intmotorid_boolenable) |
| STALL_A, STALL_B | STEP_LOSS_A, STEP_LOSS_B | [`/enableStallReport`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#enablestallreport_intmotorid_boolenable)  |
| CMD_ERROR | WRONG_CMD, NOTPREF_CMD | [`/enableCommandErrorReport`](https://ponoor.com/docs/step-series/osc-command-reference/system-settings/#reporterror_boolenable) |
| TH_STATUS | TH_WRN, TH_SD | [`/enableThermalStatusReport`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#enablethermalstatusreport_intmotorid_boolenable) |
| SW_EVN | SW_EVN | [`/enableHomeSwReport`](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#enablesweventreport_intmotorid_boolenable) |
| MOT_STATUS | MOT_STATUS | [`/enableMotorStatusReport`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#enablemotorstatusreport_intmotorid_boolenable) |
| SW_F | SW_F | [`/enableHomeSwReport`](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#enablehomeswreport_intmotorid_boolenable) |
| BUSY | BUSY | [`/enableBusyReport`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#enablebusyreport_intmotorid_boolenable) |
| HiZ | HiZ | [`/enableHizReport`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#enablehizreport_intmotorid_boolenable) |

### `/getConfigRegister (int)motorID`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |

#### Executable timing
Always

#### Description
Acquires the CONFIG register value from the motor driver (PowerSTEP01 or L6470). The information stored in CONFIG register includes motor, alarm and switch status.

#### Responses

```
/configRegister (int)motorID (int)CONFIG
```
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8 | Motor ID |
| CONFIG | 0-65535(0xFFFF) | 16bit CONFIG register content |

The CONFIG register stores various settings for the motor driver. Please refer the datasheet of the PowerSTEP01/L6470 for detail.

### `/resetMotorDriver (int)motorID`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |

#### Executable timing
Always

#### Description
Resets the motor driver (PowerSTEP01/L6470) and rewrites the setting.

### `/resetDevice`
#### Argument
None

#### Executable timing
Always

#### Description
Resets the entire device. A programmatic version of physically pressing the RESET button.