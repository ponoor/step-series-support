## Motor driver

### `/enableUvloReport (int)motorID (bool)enable`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|enable|0-1|1:Enable, 0:Disable|

#### Executable timing
Always

#### Description
Set the notification message when UVLO (Undervoltage Lockout) occurs in the specified motor driver.
UVLO occurs when the supplied voltage to the motor driver falls below the UVLO turn-off threshold voltage, with or without notification. In this state, the motor cannot be operated. It will be reset when the supply voltage is above the UVLO turn-on threshold.

These thresholds are different between STEP400(PowerSTEP01) and STEP800(L6470). For details, please refer to the corresponding datasheets.

#### Response
When ULVO occurs same message as [`/getUlvo`](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#getuvlo_intmotorid) will be sent.

#### Initial value
1 (Enabled)

### `/getUvlo (int)motorID`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |

#### Executable timing
Always

#### Description
Gets the current state of UVLO

#### Response
```
/uvlo (int)motorID
```

|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
| state | 0-1 | 1:UVLO detected 0:No UVLO condition |

### `/enableThermalStatusReport (int)motorID (bool)enable`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|enable|0-1|1:Enable, 0:Disable|

#### Executable timing
Always

#### Description
Set to send the notification message on change in the temperature status (thermalStatus) of the specified motor driver is detected. On the Bridge shutdown or Device shutdown, the motor state will automatically enters High Z state with of without notification.

#### Response
When the the thermalStatus changes, the same notification as [`/getThermalStatus`](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#getthermalstatus_intmotorid) will be sent.

#### Initial value
1 (Enabled)

### `/getThermalStatus (int)motorID`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |

#### Executable timing
Always

#### Description
Gets the current condition of the ThermalStatus. Thermal status thresholds are different between STEP400(PowerSTEP01) and STEP800(L6470).

#### Response
```
/thermalStatus (int)motorID (int)thermalStatus
```

|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|thermalStatus|0-3|Thermal status|

##### Thermal status - STEP400
| TH_STATUS | Thermal status | Set condition | Release condition |
| --- | --- | --- | --- |
| 0 | Normal | - | - |
| 1 | Warning | 135℃ | 125℃ |
| 2 | Bridge shutdown | 155℃ | 145℃ |
| 3 | Device shutdown | 170℃ | 130℃ |

##### Thermal status - STEP800
| thermalStatus | Thermal status | Set condition | Release condition |
| --- | --- | --- | --- |
| 0 | Normal | - | - |
| 1 | Warning | 130℃ | 130℃ |
| 2 | Bridge shutdown | 160℃ | 130℃ |

In the Bridge shutdown and Device shutdown states, the motor goes into the High Z state with or without notification.

#### Initial value
1 (Enabled)

### `/enableOverCurrentReport (int)motorID (bool)enable`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|enable|0-1|1:Enable, 0:Disable|

#### Executable timing
Always

#### Description
Set to send a notification when the specified motor driver goes into an overcurrent state (OCD, Over Current Detection).
When overcurrent is detected, the device automatically enters High Z state regardless of whether a notification being sent. The threshold can be set with [`/setOverCurrentThreshold`](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setovercurrentthreshold_intmotorid_intocd_th).

#### Response
On the OCD state, following message will be sent.
```
/overCurrent (int)motorID
```

|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|

#### Initial value
1 (Enabled)

### `/setOverCurrentThreshold (int)motorID (int)OCD_TH`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|OCD_TH| 0-31/0-15 |Overcurrent detection threshold|

##### Overcurrent detection threshold - STEP400
| OCD_TH | Overcurrent detection threshold |
| --- | --- |
| 0 | 312.5mA |
| 1 | 625mA |
| ... | ... |
| 30 | 9.6875A |
| 31 | 10A |

##### Overcurrent detection threshold - STEP800
| OCD_TH | Overcurrent detection threshold |
| --- | --- |
| 0 | 375mA |
| 1 | 750mA |
| ... | ... |
| 14 | 5.625A |
| 15 | 6A |

#### Executable timing
Always

#### Description
Sets the overcurrent threshold. The setting value range and corresponding currents are different between STEP400(PowerSTEP01) and STEP800(L6470).

#### Response
You will get the same response as the following [`/getOverCurrentThreshold`](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#getovercurrentthreshold_intmotorid) to see the actual value.

#### Initial value
| Model | Initial value |
| --- | ---|
| STEP400 | 15 (5A) |
| STEP800 | 7 (3A) |

### `/getOverCurrentThreshold (int)motorID`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|

#### Executable timing
Always

#### Description
Get the threshold of overcurrent.

#### Response
```
/overCurrentThreshold (int)motorID (float)overCurrentThreshold
```

|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|overCurrentThreshold|312.5-10000.0/375.0-6000.0|thresholds in [mA].

#### Initial value
| Model | Initial value |
| --- | ---|
| STEP400 | 5000.0 (15) |
| STEP800 | 3000.0 (7) |

### `/enableStallReport (int)motorID (bool)enable`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|enable|0-1|1:Enable, 0:Disable|

#### Executable timing
Always

#### Description
The threshold can be set by [`/setStallThreshold`](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setstallthreshold_intmotorid_intstall_th).
When the stall is detected by the specified motor driver, the following message is sent automatically.

#### Response
```
/stall (int)motorID
```

|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|

#### Initial value
0 (Disabled)

### `/setStallThreshold (int)motorID (int)STALL_TH`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|STALL_TH| 0-31/0-127 | Stall detection threshold |

##### Stall detection threshold - STEP400
| STALL_TH | Stall detection threshold |
| --- | --- |
| 0 | 312.5mA |
| 1 | 625mA |
| ... | ... |
| 30| 9.6875A |
| 31 | 10A |

##### Stall detection threshold - STEP800
| STALL_TH | Stall detection threshold |
| --- | --- |
| 0 | 31.25mA |
| 1 | 62.5mA |
| ... | ... |
| 126| 3.969A |
| 127 | 4A |

#### Executable timing
Always

#### Description
Sets the threshold for stall detection. The setting value range and corresponding currents are different between STEP400(PowerSTEP01) and STEP800(L6470).

#### Response
You will get the same response as the following [`/getStallThreshold`](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#getstallthreshold_intmotorid) to see the actual value.

#### Initial value
| Model | Initial value |
| --- | ---|
| STEP400 | 31 (10A) |
| STEP800 | 127 (4A) |

### `/getStallThreshold (int)motorID`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|

#### Executable timing
Always

#### Description
Gets the stall detection threshold.

#### Response
```
/stallThreshold (int)motorID (float)stallThreshold
```

|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|stallThreshold|312.5-10000.0/31.25-4000.0|thresholds in [mA]

#### Initial value
| Model | Initial value |
| --- | ---|
| STEP400 | 10000.0 (31) |
| STEP800 | 4000.0 (127) |

## Sensor
### `/setProhibitMotionOnHomeSw (int)motorID (bool)enable`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |
| enable | 0-1 | 1: Prohibit, 0: Allow |

#### Executable timing
Always

#### Description
Prohibits any motion commands towards the origin point when Home sensor is detected. The direction to the origin point can be configured through the Config Tool or by the `/setHomingDirection` command.

#### Initial value
0 (Disabled)

### `/getProhibitMotionOnHomeSw (int)motorID`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |

#### Executable timing
Always

#### Description
Returns whether the motion command towards the origin point is prohibited when Home sensor is detected.

#### Response
```
/prohibitMotionOnHomeSw (int)motorID (bool)enable
```

|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8|Motor ID|
| enable | 0-1 | 1:Prohibited, 0:Allowed |

### `/setProhibitMotionOnLimitSw (int)motorID (bool)enable`
**STEP400 only**
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4, 255 | Motor ID |
| enable | 0-1 | 1: Prohibit, 0: Allow |

#### Executable timing
Always

#### Description
Prohibits any motion commands towards the leaving direction from origin point, when the Limit sensor is detected. The direction to the origin point can be configured through the Config Tool or by the `/setHomingDirection` command.

#### Initial value
0 (Disabled)

### `/getProhibitMotionOnLimitSw (int)motorID`
**STEP400 only**
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4, 255 | Motor ID |

#### Executable timing
Always

#### Description
Returns whether the motion command towards reverse direction to the origin point is prohibited when Limit sensor is detected.

#### Response
```
/prohibitMotionOnLimitSw (int)motorID (bool)enable
```

| Argument | Range | Description |
|---|---|---|
|motorID|1-4|Motor ID|
| enable | 0-1 | 1:Prohibited, 0:Allowed |

