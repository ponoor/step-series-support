## Status Report
### `/enableHomeSwReport (int)motorID (bool)enable`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 |  motor ID |
| enable | 0-1 | 1:Enable, 0:Disable |

#### Executable timing
Always

#### Description
Sets the following message to be sent automatically when conditional change of the HOME switch of the specified motor is detected. The response message is same as [`/getHomeSw`](https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#gethomesw_intmotorid) command.

#### Initial value
0 (Disabled)

### `/enableSwEventReport (int)motorID (bool)enable`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|Motor ID|
|enable|0-1|1: Enable, 0: Disable|

#### Executable timing
Always

#### Description
Sets the following message to be sent automatically when the specified motor's HOME switch terminal state drops from HIGH level to LOW (Falling Edge).
While the[`/enableHomeSwReport`](https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#enablehomeswreport_intmotorid_boolenable)command observes the status by polling the STATUS register of motor driver IC from microcomputer's firmware, this`/enableSwEventReport`detects the event by driver IC's hardware, able to pick up the sensor detection shorter than 1ms.
Following message will be sent.
```
/swEvent (int)motorID
```
|Argument|Range|Description|
|---|---|---|
|motorID|1-4|Motor ID|

#### Initial value
0 (Disabled)

```
/homeSw (int)motorID (bool)swState (bool)direction
```

|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|swState|0-1|State|

| swState | State |
| --- | --- |
| 0 | Open, Undetected state |
| 1 | Closed, Detected state |

| direction | Motor direction |
| --- | --- |
| 1 | Forward |
| 0 | Reverse |

#### Initial value
0 (Disabled)

### `/getHomeSw (int)motorID`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|

#### Executable timing
Always

#### Description
Gets the status of the HOME switch, closed or opened.

#### Response
```
/homeSw (int)motorID (bool)swState (bool)direction
```

|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|swState|0-1|State|
|direction|0-1|direction|

| swState | State |
| --- | --- |
| 0 | Open, Undetected state |
| 1 | Closed, Detected state |

| direction | Motor direction |
| --- | --- |
| 1 | Forward |
| 0 | Reverse |

### `/enableLimitSwReport (int)motorID (bool)enable`
**STEP400 only**
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4, 255|Motor ID|
|enable|0-1|1:Enable, 0:Disable|

#### Executable timing
Always

#### Description
Sets automatic response when conditional change on the specified motor's LIMIT switch terminal is detected. The sent message is as same as the response from[`/getLimitSw`](https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#getlimitsw_intmotorid)command.

#### Initial value
0 (Disable)

### `/getLimitSw (int)motorID`
**STEP400 only**
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4, 255|Motor ID|

#### Executable timing
Always

#### Description
Returns the status of LIMIT switch.

#### Response
```
/limitSw (int)motorID (bool)swState (bool)direction
```

|Argument|Range|Description|
|---|---|---|
|motorID|1-4, 255|Motor ID|
|swState|0-1|Status|
|direction|0-1|Direction|

| swState | Status |
| --- | --- |
| 0 | Open, Undetected state |
| 1 | Closed, Detected state |

| direction | Motor direction |
| --- | --- |
| 1 | Forward |
| 0 | Reverse |

## Response settings
### `/setHomeSwMode (int)motorID (bool)SW_MODE`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|SW_MODE|0-1|Switch mode|

| SW_MODE | Switch mode |
| --- | --- |
| 0 | HardStop interrupt (stop immediately) |
| 1 | User disposal (not stop) |

#### Executable timing
HiZ state

#### Description
Sets switch mode whether to stop immediately when the HOME switch terminal state changes (falling edge).

#### Initial value
1 (User disposal)

### `/getHomeSwMode (int)motorID`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|

#### Executable timing
Always

#### Description
Get the Switch mode described above.

#### Response
``` 
/homeSwMode (int)motorID (bool)swMode
```

|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|swMode|0-1||

### `/setLimitSwMode (int)motorID (bool)SW_MODE`
**STEP400 only**
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4, 255|Motor ID|
|SW_MODE|0-1|Switch mode|

| SW_MODE | Switch mode |
| --- | --- |
| 0 | HardStop interrupt  (Immediate stop)|
| 1 | User disposal (Does not stop)|

#### Executable timing
Always

#### Description
Sets the Switch mode whether to stop the motor immediately when the LIMIT switch terminal condition is changed.

#### Initial value
1 (User disposal)

### `/getLimitSwMode (int)motorID`
**STEP400 only**
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4, 255|Motor ID|

#### Executable timing
Always

#### Description
Get the Switch mode described above.

#### Response
```
/limitSwMode (int)motorID (bool)swMode
```

|Argument|Range|Description|
|---|---|---|
|motorID|1-4, 255|Motor ID|
|swMode|0-1||