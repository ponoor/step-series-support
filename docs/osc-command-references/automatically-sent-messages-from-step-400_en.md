## Summary

Most of messages sent from the device are responses regarding enquiry messages. For example, when sending the message `/getPosition` to the device in order to acquire one's current position, the response message sent from the device will be `/position`. However, some messages are, as opposed to the responses to the specific messages, automatic messages which correspond to the state changes of the board. This chapter explains this sort of automatic messages.

## Startup Notification

### `/booted`

#### Explanation
 This message is automatically sent out when the device has (re)started. By watching the message, you can detect reset event of the device triggered by some reason.

The message will be sent out one second after the firmware is started up and the ethernet link is established. The message will be sent to `255.255.255.255`, means broadcasting to all nodes within the subnet.

This message can be disabled from the Config Tool.

#### Sent Message

```
/booted (int)deviceID
```

| Argument | Range | Description |
|----------|-------|-------------|
| deviceID | 0-255 | The device ID set by the DIP Switch |

## Error

### `/error/osc`

#### Explanation

Sent if any error is detected in the received OSC message.

#### Sent Message

```
/error/osc (symbol)errorText
```

| Argument | Description |
|----------|-------------|
| errorText | A character string that indicates the details of an error. |

##### Error Text

| errorText | Description |
|-----------|-------------|
| `messageNotMatch` | There is no corresponding command |
| `oscSyntaxError` | The OSC format is out of standard |
| `WrongDataType` | Wrong datatype of in argument(s) |

### `/error/command`

#### Explanation

This message will be sent if an error is detected while executing a command.

The message can be enabled or disabled with [`/reportError`](https://ponoor.com/en/docs/step-series/osc-command-reference/system-settings/#reporterror_boolenable) command.

#### Sent Message

```
/error/command (Symbol)ErrorText (int)motorID
```

| Argument | Range | Description |
|----------|-------|-------------|
| ErrorText | | A character string that indicates the details of an error. |
| motorID | 1-4/1-8 | The motor's ID |

##### Error Text
| ErrorText  | Explanation |
| --- | --- |
| `CommandIgnored` | The command is currently not executable. Also refer [Timing](https://ponoor.com/en/docs/step-series/osc-command-reference/#i-4) section. |
| `MotorIdNotMatch` | Motor ID is not appropriate. |
| `BrakeEngaging` | A motion command was sent while the electromagnet brake was active. |
| `HomeSwActivating` | Movement from home sensor position towards the origin point. |
| `LimitSwActivating` | Movement from limit sensor position towards the opposite direction from origin. |
| `GoUntilTimeout` | Timeout while executing `/goUntil` command. |
| `ReleaseSwTimeout` | Timeout while executing `/releaseSw` command. |
| `InServoMode` | Received a command which can not be executed while servo mode. |

## Notification of State

### `/busy`

Please see [`/enableBusyReport`](https://ponoor.com/en/docs/step-series/osc-command-reference/system-settings/#enablebusyreport_intmotorid_boolenable)

### `/HiZ`

 Please see [`/enableHizReport`](https://ponoor.com/en/docs/step-series/osc-command-reference/system-settings/#enablehizreport_intmotorid_boolenable)

### `/dir`
Please see [`/enableDirReport`](https://ponoor.com/en/docs/step-series/osc-command-reference/motordriver-settings/#enabledirreport_intmotorid_boolenable)

### `/motorStatus`

 Please see [`/enableMotorStatusReport`](https://ponoor.com/en/docs/step-series/osc-command-reference/system-settings/#enablemotorstatusreport_intmotorid_boolenable)

### `/homingStatus`
Please see [`/homing`](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#homing_intmotorid)

### `/position`
Please see [`/setPositionReportInterval`](https://ponoor.com/en/docs/step-series/osc-command-reference/motordriver-settings/#setpositionreportinterval_intmotorid_intinterval)

### `/positionList`
Please see [`/setPositionListReportInterval`](https://ponoor.com/en/docs/step-series/osc-command-reference/motordriver-settings/#setpositionlistreportinterval_intinterval)

## Alarm Notifications

### `/uvlo`

Please see [`/enableUvloReport`](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#enableuvloreport_intmotorid_boolenable)

### `/thermalStatus`

Please see [`/enableThermalStatusReport`](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#enablethermalstatusreport_intmotorid_boolenable)

### `/overCurrent`

Please see [`/enableOverCurrentReport`](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#enableovercurrentreport_intmotorid_boolenable)

### `/stall`

Please see [`/enableStallReport`](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#enablestallreport_intmotorid_boolenable)