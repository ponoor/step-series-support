## Position

### `/setPosition (int)motorID (int)newPosition`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|newPosition|-2,097,152 - 2,097,151|specified coordinates|

#### Executable timing
When the motor is stopped

#### Description
Rewrites ABS_POS register to the specified coordinates. The current motor position is set to the specified coordinates.

### `/getPosition (int)motorID`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|

#### Executable timing
Always

#### Description
Returns the contents of the ABS_POS register (current position).

[`/setPositionReportInterval`](https://ponoor.com/en/docs/step-series/osc-command-reference/motor-driver-settings/#setpositionreportinterval_intmotorid_intinterval) can make the controller to send this message with a specified interval.
#### Response
```
/position (int)motorID (int)ABS_POS
```

|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8|motor ID|
|ABS_POS|-2,097,152 - 2,097,151|current position|

### `/getPositionList`
#### Argument
None

#### Executable timing
Always

#### Description
Returns the current position of all motors at once. `/getPosition 255` returns individual messages for each motors but this command returns single message with a position list.

[`/setPositionListReportInterval`](https://ponoor.com/en/docs/step-series/osc-command-reference/motor-driver-settings/#setpositionlistreportinterval_intinterval) can make the controller to send this list with a specified interval.

#### Response
```
/positionList (int)position#1 ... (int)position#n ... (int)position#4
```

|Argument|Range|Description|
|---|---|---|
|position#n|-2,097,152 - 2,097,151|current position of the motor #n|

The number of the arguments are 4 in STEP400, 8 in STEP800.

### `/resetPos (int)motorID`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|

#### Executable timing
Always

#### Description
Reset ABS_POS register to 0.

### `/setElPos (int)motorID (int)newFullstep (int)newMicrostep`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|newFullstep|0-3|Fullstep position|
|newMicrostep|0-127|Microstep position|

#### Executable timing
When the motor is stopped

#### Description
Set the electrical position of the motor. The microstep is expressed in step/128, and the value has to be matched with the current microstep mode.

### `/getElPos (int)motorID`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|

#### Executable timing
Always

#### Description
Returns the current electrical position of the motor.

#### Response
```
/elPos (int)motorID (int)fullstep (int)microstep
```

|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8|motor ID|
|fullstep|0-3|Fullstep position|
|microstep|0-127|Microstep position|


## HOME/MARK
### `/setMark (int)motorID (int)MARK`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|MARK||Coordination to be set|

#### Executable timing
Always

#### Description
Set the MARK register to arbitrary position.

### `/getMark (int)motorID`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|

#### Executable timing
Always

#### Description
Get the MARK position.

#### Response
```
/mark (int)motorID (int)MARK
```

|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|MARK|| Position of the MARK |

### `/goHome (int)motorID`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|

#### Executable timing
In motion start condition

#### Description
Move the motor to the HOME position (zero position) according to the speed profile.

#### Response
None

### `/goMark (int)motorID`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|

#### Executable timing
In motion start condition

#### Description
Move the motor to the MARK position according to the speed profile.

#### Response
None