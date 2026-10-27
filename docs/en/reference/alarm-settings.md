---
title: Alarm settings
---

# Alarm settings

For how the alarms and the protection work, see [Alarms and protection](../guides/alarms-and-protection.md).

## Motor driver

<!-- osc: /enableUvloReport -->
<!-- generated:begin osc /enableUvloReport -->
### `/enableUvloReport` (int)motorID (bool)enable {#enableuvloreport}

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

Set the notification message when UVLO (Undervoltage Lockout) occurs in the specified motor driver.  
UVLO occurs when the supplied voltage to the motor driver falls below the UVLO turn-off threshold voltage, with or without notification. In this state, the motor cannot be operated. It will be reset when the supply voltage is above the UVLO turn-on threshold.

These thresholds are different between STEP400(PowerSTEP01) and STEP800(L6470). For details, please refer to the corresponding datasheets.

#### Response

[`/uvlo`](automatically-sent-messages.md#uvlo)

```
/uvlo (int)motorID (int)state
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| state | int |  |  |

`state`

| Value | Meaning |
| --- | --- |
| 1 | UVLO detected |
| 0 | No UVLO condition |

#### Initial value

- `enable`: true (Enable) ([alarmAndReport.reportUVLO](../connections/configuration-items.md#alarmandreport-reportuvlo))

#### See also

[`/getUvlo`](alarm-settings.md#getuvlo)
<!-- generated:end osc /enableUvloReport -->

<!-- osc: /getUvlo -->
<!-- generated:begin osc /getUvlo -->
### `/getUvlo` (int)motorID {#getuvlo}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Gets the current state of UVLO

#### Response

[`/uvlo`](automatically-sent-messages.md#uvlo)

```
/uvlo (int)motorID (int)state
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| state | int |  |  |

`state`

| Value | Meaning |
| --- | --- |
| 1 | UVLO detected |
| 0 | No UVLO condition |
<!-- generated:end osc /getUvlo -->

<!-- osc: /enableThermalStatusReport -->
<!-- generated:begin osc /enableThermalStatusReport -->
### `/enableThermalStatusReport` (int)motorID (bool)enable {#enablethermalstatusreport}

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

Sends a notification message when a change in the temperature status (thermalStatus) of the specified motor driver is detected. On bridge shutdown or device shutdown, the motor state will automatically enter High Z state with or without notification.

#### Response

[`/thermalStatus`](automatically-sent-messages.md#thermalstatus)

```
/thermalStatus (int)motorID (int)thermalStatus
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| thermalStatus | int | 0-3 | Thermal status |

#### Initial value

- `enable`: true (Enable) ([alarmAndReport.reportThermalStatus](../connections/configuration-items.md#alarmandreport-reportthermalstatus))

#### See also

[`/getThermalStatus`](alarm-settings.md#getthermalstatus)
<!-- generated:end osc /enableThermalStatusReport -->

<!-- osc: /getThermalStatus -->
<!-- generated:begin osc /getThermalStatus -->
### `/getThermalStatus` (int)motorID {#getthermalstatus}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Gets the current condition of the ThermalStatus. Thermal status thresholds are different between STEP400(PowerSTEP01) and STEP800(L6470).

In the bridge shutdown and device shutdown states, the motor goes into the High Z state with or without notification.

#### Response

[`/thermalStatus`](automatically-sent-messages.md#thermalstatus)

```
/thermalStatus (int)motorID (int)thermalStatus
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| thermalStatus | int | 0-3 | Thermal status |
<!-- generated:end osc /getThermalStatus -->

<!-- osc: /enableOverCurrentReport -->
<!-- generated:begin osc /enableOverCurrentReport -->
### `/enableOverCurrentReport` (int)motorID (bool)enable {#enableovercurrentreport}

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

Set to send a notification when the specified motor driver goes into an overcurrent state (OCD, Over Current Detection).  
When overcurrent is detected, the device automatically enters High Z state regardless of whether a notification being sent. The threshold can be set with [`/setOverCurrentThreshold`](alarm-settings.md#setovercurrentthreshold).

#### Response

[`/overCurrent`](automatically-sent-messages.md#overcurrent)

```
/overCurrent (int)motorID
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |

#### Initial value

- `enable`: true (Enable) ([alarmAndReport.reportOCD](../connections/configuration-items.md#alarmandreport-reportocd))
<!-- generated:end osc /enableOverCurrentReport -->

<!-- osc: /setOverCurrentThreshold -->
<!-- generated:begin osc /setOverCurrentThreshold -->
### `/setOverCurrentThreshold` (int)motorID (int)OCD_TH {#setovercurrentthreshold}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| OCD_TH | int | 0-31 (STEP400), 0-15 (STEP800) | Overcurrent detection threshold |

#### Executable timing

Always

#### Description

Sets the overcurrent threshold. The setting value range and corresponding currents are different between STEP400(PowerSTEP01) and STEP800(L6470).

A value above the range is not rejected; it wraps around: the value after the maximum is 0 (on STEP800, 16 becomes 0 and 17 becomes 1).

#### Response

```
/overCurrentThreshold (int)motorID (float)overCurrentThreshold
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| overCurrentThreshold | float | 312.5-10000 (STEP400), 375-6000 (STEP800) mA | thresholds in [mA]. |

#### Initial value

- `OCD_TH`: STEP400: 15; STEP800: 7 (firmware) / 15 (template) ([alarmAndReport.OCThreshold](../connections/configuration-items.md#alarmandreport-octhreshold))

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

#### See also

[`/getOverCurrentThreshold`](alarm-settings.md#getovercurrentthreshold), [`/enableOverCurrentReport`](alarm-settings.md#enableovercurrentreport)
<!-- generated:end osc /setOverCurrentThreshold -->

<!-- osc: /getOverCurrentThreshold -->
<!-- generated:begin osc /getOverCurrentThreshold -->
### `/getOverCurrentThreshold` (int)motorID {#getovercurrentthreshold}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Get the threshold of overcurrent.

#### Response

```
/overCurrentThreshold (int)motorID (float)overCurrentThreshold
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| overCurrentThreshold | float | 312.5-10000 (STEP400), 375-6000 (STEP800) mA | thresholds in [mA]. |
<!-- generated:end osc /getOverCurrentThreshold -->

<!-- osc: /enableStallReport -->
<!-- generated:begin osc /enableStallReport -->
### `/enableStallReport` (int)motorID (bool)enable {#enablestallreport}

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

The threshold can be set by [`/setStallThreshold`](alarm-settings.md#setstallthreshold).  
When the stall is detected by the specified motor driver, the following message is sent automatically.

#### Response

[`/stall`](automatically-sent-messages.md#stall)

```
/stall (int)motorID
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |

#### Initial value

- `enable`: false (Disable) ([alarmAndReport.reportStall](../connections/configuration-items.md#alarmandreport-reportstall))
<!-- generated:end osc /enableStallReport -->

<!-- osc: /setStallThreshold -->
<!-- generated:begin osc /setStallThreshold -->
### `/setStallThreshold` (int)motorID (int)STALL_TH {#setstallthreshold}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| STALL_TH | int | 0-31 (STEP400), 0-127 (STEP800) | Stall detection threshold |

#### Executable timing

Always

#### Description

Sets the threshold for stall detection. The setting value range and corresponding currents are different between STEP400(PowerSTEP01) and STEP800(L6470).

Stall detection lets the driver detect, from the motor current, that the motor can no longer turn against the load. Find a threshold (`/setStallThreshold`) as close as possible to, and slightly above, the current actually flowing. A small loss of steps cannot be detected, but a large position error may be.

A value above the range is not rejected; it wraps around: the value after the maximum is 0 (on STEP800, 128 becomes 0 and 129 becomes 1).

#### Changes

- **v2.2.0**: Also changes the saved STALL_TH (`/saveConfig`, `/resetMotorDriver`). Before, it changed the register only.

#### Response

```
/stallThreshold (int)motorID (float)stallThreshold
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| stallThreshold | float | 312.5-10000 (STEP400), 31.25-4000 (STEP800) mA | thresholds in [mA] |

#### Initial value

- `STALL_TH`: STEP400: 31; STEP800: 127 ([voltageMode.STALL_TH](../connections/configuration-items.md#voltagemode-stall_th))

##### Stall detection threshold - STEP400

| STALL_TH | Stall detection threshold |
| --- | --- |
| 0 | 312.5mA |
| 1 | 625mA |
| ... | ... |
| 30 | 9.6875A |
| 31 | 10A |

##### Stall detection threshold - STEP800

| STALL_TH | Stall detection threshold |
| --- | --- |
| 0 | 31.25mA |
| 1 | 62.5mA |
| ... | ... |
| 126 | 3.969A |
| 127 | 4A |

#### See also

[`/getStallThreshold`](alarm-settings.md#getstallthreshold), [`/enableStallReport`](alarm-settings.md#enablestallreport)
<!-- generated:end osc /setStallThreshold -->

<!-- osc: /getStallThreshold -->
<!-- generated:begin osc /getStallThreshold -->
### `/getStallThreshold` (int)motorID {#getstallthreshold}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Gets the stall detection threshold.

#### Response

```
/stallThreshold (int)motorID (float)stallThreshold
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| stallThreshold | float | 312.5-10000 (STEP400), 31.25-4000 (STEP800) mA | thresholds in [mA] |
<!-- generated:end osc /getStallThreshold -->

## Sensor

<!-- osc: /setProhibitMotionOnHomeSw -->
<!-- generated:begin osc /setProhibitMotionOnHomeSw -->
### `/setProhibitMotionOnHomeSw` (int)motorID (bool)enable {#setprohibitmotiononhomesw}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| enable | bool |  |  |

`enable`

| Value | Meaning |
| --- | --- |
| 1 | Prohibit |
| 0 | Allow |

#### Executable timing

Always

#### Description

Prohibits any motion commands towards the origin point when the HOME switch is activated. The direction to the origin point can be configured through the configuration tool or by the `/setHomingDirection` command.

#### Changes

- **v2.2.0**: The automatic hard stop at the home switch is not sent to a motor whose driver is HiZ, also with the brake disabled (a hard stop energizes a HiZ driver).

#### Initial value

- `enable`: false (Allow) ([driverSettings.prohibitMotionOnHomeSw](../connections/configuration-items.md#driversettings-prohibitmotiononhomesw))

#### See also

[`/getProhibitMotionOnHomeSw`](alarm-settings.md#getprohibitmotiononhomesw), [`/setHomingDirection`](homing.md#sethomingdirection)
<!-- generated:end osc /setProhibitMotionOnHomeSw -->

<!-- osc: /getProhibitMotionOnHomeSw -->
<!-- generated:begin osc /getProhibitMotionOnHomeSw -->
### `/getProhibitMotionOnHomeSw` (int)motorID {#getprohibitmotiononhomesw}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Returns whether the motion command towards the origin point is prohibited when the HOME switch is activated.

#### Response

```
/prohibitMotionOnHomeSw (int)motorID (int)enable
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| enable | int |  |  |

`enable`

| Value | Meaning |
| --- | --- |
| 1 | Prohibited |
| 0 | Allowed |
<!-- generated:end osc /getProhibitMotionOnHomeSw -->

<!-- osc: /setProhibitMotionOnLimitSw -->
<!-- generated:begin osc /setProhibitMotionOnLimitSw -->
### `/setProhibitMotionOnLimitSw` (int)motorID (bool)enable {#setprohibitmotiononlimitsw}

Available on STEP400 only.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| enable | bool |  |  |

`enable`

| Value | Meaning |
| --- | --- |
| 1 | Prohibit |
| 0 | Allow |

#### Executable timing

Always

#### Description

Prohibits any motion commands towards the leaving direction from origin point, when the LIMIT switch is activated. The direction to the origin point can be configured through the configuration tool or by the `/setHomingDirection` command.

#### Initial value

- `enable`: false (Allow) ([driverSettings.prohibitMotionOnLimitSw](../connections/configuration-items.md#driversettings-prohibitmotiononlimitsw))

#### See also

[`/getProhibitMotionOnLimitSw`](alarm-settings.md#getprohibitmotiononlimitsw), [`/setHomingDirection`](homing.md#sethomingdirection)
<!-- generated:end osc /setProhibitMotionOnLimitSw -->

<!-- osc: /getProhibitMotionOnLimitSw -->
<!-- generated:begin osc /getProhibitMotionOnLimitSw -->
### `/getProhibitMotionOnLimitSw` (int)motorID {#getprohibitmotiononlimitsw}

Available on STEP400 only.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Returns whether the motion command towards reverse direction to the origin point is prohibited when the LIMIT switch is activated.

#### Response

Available on STEP400 only.

```
/prohibitMotionOnLimitSw (int)motorID (int)enable
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| enable | int |  |  |

`enable`

| Value | Meaning |
| --- | --- |
| 1 | Prohibited |
| 0 | Allowed |
<!-- generated:end osc /getProhibitMotionOnLimitSw -->
