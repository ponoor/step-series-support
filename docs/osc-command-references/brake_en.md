### `/enableElectromagnetBrake (int)motorID (bool)enable`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|Motor ID|
| enable | 0-1 | 1:Enable, 0:Disable |

#### Executable timing
Always

#### Description
Enables / disables electromagnetic brake mode.
When the mode is enabled, the controller replies error if motor movement command is sent without releasing the electromagnetic brake.

#### Response
0 (Disabled)

### `/activate (int)motorID (bool)state`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|Motor ID|
| state | 0-1 | 1:Excited 0:Not excited|

##### state
| state | Description |
| --- | --- |
| 1 | Motor excited, EM brake released |
| 0 | Motor not excited, EM brake activated |

#### Executable timing
Always

#### Description
Switches motor excitation / release when electromagnetic brake mode is enabled. The EM is also activated together. you You cannot send motor movement command when the motor is not excited by this command.

If the EM mode is disabled, this command is ignored.

### `/free (int)motorID (bool)state`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|Motor ID|

#### Executable timing
Always

#### Description
Releases motor axis when the electromagnetic brake mode is active. It releases motor excitation and keep EM brake in release state.

Be cautious when sending this command. If some load is hanged to the motor, it will loose the hold and the load may fall down.

If the EM mode is disabled, this command is ignored.

### `/setBrakeTransitionDuration (int)motorID (int)duration`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|Motor ID|
| duration | 0-10000 [ms] | Transition duration |

#### Executable timing
Always

#### Description
Sets the transitional duration to keep the motor excited when the electromagnetic brake is activated or released. This is to keep holding the motor axis until the brake movement is completed, due to the physical transition time for the brake mechanism.

#### Initial value
100[ms]

### `/getBrakeTransitionDuration (int)motorID`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|Motor ID|

#### Executable timing
Always

#### Description
Returns the transitional duration to keep holding the motor axis when the electromagnetic brake is activated or released.

#### Response
```
/brakeTransitionDuration (int)motorID (int)duration
```
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|Motor ID|
| duration | 0-10000 [ms] | Transitional duration |
