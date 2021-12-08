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

#### Response
```
/position (int)motorID (int)ABS_POS
```

|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|ABS_POS|-2,097,152 - 2,097,151|current position|

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
When the motor is not in BUSY state.

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
When the motor is not in BUSY state

#### Description
Move the motor to the MARK position according to the speed profile.

#### Response
None