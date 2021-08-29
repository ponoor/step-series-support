### `/setSpeedProfile (int)motorID (float)acc (float)dec (float)maxSpeed`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|acc|14.55 - 59590 [step/s/s]|acceleration|
|dec|14.55 - 59590 [step/s/s]|deceleration|
|maxSpeed|15.25 - 15610 [step/s]|maximum speed|

#### Executable timing
when the motor is stopped

#### Description
Sets the acc, dec, and maxSpeed of the speed profile together.

#### Initial value
|Argument|Initial value|Description|
|---|---|---|
|acc|2000|acceleration|
|dcc|2000|deceleration|
|maxSpeed|620|maximum speed|

### `/getSpeedProfile (int)motorID`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|

#### Executable timing
Always

#### Description
Gets the acc, dec, and maxSpeed of the speed profile together.

#### Response
`
/speedProfile (int)motorID (float)acc (float)dec (float)maxSpeed
`

|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|acc|14.55 - 59590 [step/s/s]|acceleration|
|dec|14.55 - 59590 [step/s/s]|deceleration|
|maxSpeed|15.25 - 15610 [step/s]|maximum speed|

### `/setFullstepSpeed (int)motorID (float)fullstepSpeed`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|fullstepSpeed|7.63-15625 [step/s]|threshold|

#### Executable timing
Always

#### Description
Sets the threshold at which the microstepping mode automatically switches to full-step mode.

#### Initial value
15625 [steps/s]

### `/getFullstepSpeed (int)motorID`
#### Argument

| Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|Motor ID|

#### Executable timing
Always

#### Description
Gets the threshold at which the microstepping mode automatically switches to full-step mode.

#### Response
```
/fullstepSpeed (int)motorID (float)fullstepSpeed
```

| Argument|Range|Description|
|---|---|---|
|motorID|1-4|Motor ID|
|fullstepSpeed|7.63-15625 [step/s]|Threshold|

### `/setMaxSpeed (int)motorID (float)maxSpeed`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|Motor ID|
|maxSpeed|15.25 - 15610 [step/s]|maximum speed|

#### Executable timing
Always

#### Description
Set the maximum speed of the speed profile

#### Initial value
620[step/s]

### `/setAcc (int)motorID (float)acc`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|acc|14.55 - 59590 [step/s/s]|acceleration|

#### Executable timing
When the motor is stopped

#### Description
Sets the acceleration of the speed profile.

#### Initial value
2000[steps/s/s]

### `/setDec (int)motorID (float)dec`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|dec|14.55 - 59590 [step/s/s]|deceleration|

#### Executable timing
When the motor is stopped

#### Description
Sets the deceleration of the speed profile.

#### Initial value
2000[step/s/s]

### `/getSpeed (int)motorID`
#### Argument

| Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|Motor ID|

#### Executable timing
Always

#### Description
Returns the current motor speed.

#### Response
```
/speed (int)motorID (float)speed
```

| Argument|range|Description|
|---|---|---|
|motorID|1-4/1-8|Motor ID|
|speed|-15625 - 15625 [step/s]|Current speed|