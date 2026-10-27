---
title: HOME and LIMIT switches
---

# HOME and LIMIT switches

For how the HOME and LIMIT switches are used in homing, see [Homing and position](../guides/homing-and-position.md).

## Status report

<!-- osc: /enableHomeSwReport -->
<!-- generated:begin osc /enableHomeSwReport -->
### `/enableHomeSwReport` (int)motorID (bool)enable {#enablehomeswreport}

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

Sets the following message to be sent automatically when conditional change of the HOME switch of the specified motor is detected. The response message is same as [`/getHomeSw`](home-and-limit-sensors.md#gethomesw) command.

#### Response

[`/homeSw`](automatically-sent-messages.md#homesw)

```
/homeSw (int)motorID (int)swState (int)direction
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| swState | int |  | State |
| direction | int |  | direction |

`swState`

| Value | Meaning |
| --- | --- |
| 0 | Open, Undetected state |
| 1 | Closed, Detected state |

`direction`

| Value | Meaning |
| --- | --- |
| 1 | Forward |
| 0 | Reverse |

#### Initial value

- `enable`: false (Disable) ([alarmAndReport.reportHomeSwStatus](../connections/configuration-items.md#alarmandreport-reporthomeswstatus))
<!-- generated:end osc /enableHomeSwReport -->

<!-- osc: /enableSwEventReport -->
<!-- generated:begin osc /enableSwEventReport -->
### `/enableSwEventReport` (int)motorID (bool)enable {#enablesweventreport}

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

Sets the following message to be sent automatically when the specified motor's HOME switch terminal state drops from HIGH level to LOW (Falling Edge).  
While the [`/enableHomeSwReport`](home-and-limit-sensors.md#enablehomeswreport) command observes the status by polling the STATUS register of motor driver IC from microcomputer's firmware, this `/enableSwEventReport` detects the event by driver IC's hardware, able to pick up the sensor detection shorter than 1ms.

#### Response

[`/swEvent`](automatically-sent-messages.md#swevent)

```
/swEvent (int)motorID
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |

#### Initial value

- `enable`: false (Disable) ([alarmAndReport.reportSwEvn](../connections/configuration-items.md#alarmandreport-reportswevn))
<!-- generated:end osc /enableSwEventReport -->

<!-- osc: /getHomeSw -->
<!-- generated:begin osc /getHomeSw -->
### `/getHomeSw` (int)motorID {#gethomesw}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Gets the status of the HOME switch, closed or opened.

#### Response

[`/homeSw`](automatically-sent-messages.md#homesw)

```
/homeSw (int)motorID (int)swState (int)direction
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| swState | int |  | State |
| direction | int |  | direction |

`swState`

| Value | Meaning |
| --- | --- |
| 0 | Open, Undetected state |
| 1 | Closed, Detected state |

`direction`

| Value | Meaning |
| --- | --- |
| 1 | Forward |
| 0 | Reverse |
<!-- generated:end osc /getHomeSw -->

<!-- osc: /enableLimitSwReport -->
<!-- generated:begin osc /enableLimitSwReport -->
### `/enableLimitSwReport` (int)motorID (bool)enable {#enablelimitswreport}

Available on STEP400 only.

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

Sets automatic response when conditional change on the specified motor's LIMIT switch terminal is detected. The sent message is as same as the response from [`/getLimitSw`](home-and-limit-sensors.md#getlimitsw) command.

#### Response

[`/limitSw`](automatically-sent-messages.md#limitsw)

Available on STEP400 only.

```
/limitSw (int)motorID (int)swState (int)direction
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| swState | int |  | Status |
| direction | int |  | Direction |

`swState`

| Value | Meaning |
| --- | --- |
| 0 | Open, Undetected state |
| 1 | Closed, Detected state |

`direction`

| Value | Meaning |
| --- | --- |
| 1 | Forward |
| 0 | Reverse |

#### Initial value

- `enable`: false (Disable) ([alarmAndReport.reportLimitSwStatus](../connections/configuration-items.md#alarmandreport-reportlimitswstatus))
<!-- generated:end osc /enableLimitSwReport -->

<!-- osc: /getLimitSw -->
<!-- generated:begin osc /getLimitSw -->
### `/getLimitSw` (int)motorID {#getlimitsw}

Available on STEP400 only.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Returns the status of LIMIT switch.

#### Response

[`/limitSw`](automatically-sent-messages.md#limitsw)

Available on STEP400 only.

```
/limitSw (int)motorID (int)swState (int)direction
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| swState | int |  | Status |
| direction | int |  | Direction |

`swState`

| Value | Meaning |
| --- | --- |
| 0 | Open, Undetected state |
| 1 | Closed, Detected state |

`direction`

| Value | Meaning |
| --- | --- |
| 1 | Forward |
| 0 | Reverse |
<!-- generated:end osc /getLimitSw -->

## Response settings

<!-- osc: /setHomeSwMode -->
<!-- generated:begin osc /setHomeSwMode -->
### `/setHomeSwMode` (int)motorID (bool)SW_MODE {#sethomeswmode}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| SW_MODE | bool |  | Switch mode |

`SW_MODE`

| Value | Meaning |
| --- | --- |
| 0 | HardStop interrupt (stop immediately) |
| 1 | User disposal (not stop) |

#### Executable timing

High Z state

#### Description

Sets switch mode whether to stop immediately when the HOME switch terminal state changes (falling edge).

The outputs must be HiZ; otherwise `MotorNotHiZ` is replied and nothing is applied.

#### Changes

- **v2.2.0**: The outputs must be HiZ (SW_MODE of the CONFIG register is writable only in HiZ); otherwise `/error/command MotorNotHiZ` and nothing is applied.

#### Errors

- `MotorNotHiZ`: The command writes a driver register that can be written only while the outputs are HiZ, and the motor is not HiZ. A motor holding its position is not HiZ: send `/softHiZ` or `/hardHiZ` first. Nothing is applied. Added in v2.2.0.

#### Initial value

- `SW_MODE`: true (User disposal (not stop)) ([driverSettings.homeSwMode](../connections/configuration-items.md#driversettings-homeswmode))

#### See also

[`/getHomeSwMode`](home-and-limit-sensors.md#gethomeswmode)
<!-- generated:end osc /setHomeSwMode -->

<!-- osc: /getHomeSwMode -->
<!-- generated:begin osc /getHomeSwMode -->
### `/getHomeSwMode` (int)motorID {#gethomeswmode}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Get the Switch mode described above.

#### Response

```
/homeSwMode (int)motorID (int)swMode
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| swMode | int | 0-1 |  |

#### See also

[`/setHomeSwMode`](home-and-limit-sensors.md#sethomeswmode)
<!-- generated:end osc /getHomeSwMode -->

<!-- osc: /setLimitSwMode -->
<!-- generated:begin osc /setLimitSwMode -->
### `/setLimitSwMode` (int)motorID (bool)SW_MODE {#setlimitswmode}

Available on STEP400 only.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| SW_MODE | bool |  | Switch mode |

`SW_MODE`

| Value | Meaning |
| --- | --- |
| 0 | HardStop interrupt (Immediate stop) |
| 1 | User disposal (Does not stop) |

#### Executable timing

Always

#### Description

Sets the Switch mode whether to stop the motor immediately when the LIMIT switch terminal condition is changed.

#### Changes

- **v2.2.0**: The automatic hard stop at the limit switch (`SW_HARD_STOP`) is not sent to a motor whose driver is HiZ, also with the brake disabled (a hard stop energizes a HiZ driver).

#### Initial value

- `SW_MODE`: true (User disposal (Does not stop)) ([driverSettings.limitSwMode](../connections/configuration-items.md#driversettings-limitswmode))

#### See also

[`/getLimitSwMode`](home-and-limit-sensors.md#getlimitswmode)
<!-- generated:end osc /setLimitSwMode -->

<!-- osc: /getLimitSwMode -->
<!-- generated:begin osc /getLimitSwMode -->
### `/getLimitSwMode` (int)motorID {#getlimitswmode}

Available on STEP400 only.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Get the Switch mode described above.

#### Response

Available on STEP400 only.

```
/limitSwMode (int)motorID (int)swMode
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| swMode | int | 0-1 |  |

#### See also

[`/setLimitSwMode`](home-and-limit-sensors.md#setlimitswmode)
<!-- generated:end osc /getLimitSwMode -->
