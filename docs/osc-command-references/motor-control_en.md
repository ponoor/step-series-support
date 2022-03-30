 ## Motor movement
### `/run (int)motorID (float)speed`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|speed|-15625 - 15625 [step/s]|Rotation speed|

#### Executable timing
In motion start condition

#### Description
Rotates the motor at specified speed. The acceleration is controlled with the pre-set speed profile. The speed is limited by maxSpeed. It remains in the BUSY state until the motor reached to the specified speed.

### `/move (int)motorID (int)step`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|step||Moving step counts|

#### Executable timing
When the motor is stopped, and In motion start condition.

#### Description
Moves specified number of steps according to the pre-set speed profile. It remains in the BUSY state until reaches to the specified step counts. This command can only execute when the motor is stopped.

### `/goTo (int)motorID (int)position`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|position|-2,097,152 - 2,097,151|Destination|

#### Executable timing
In motion start condition

#### Description
Moves to the specified position in the shortest route according to the pre-set speed profile. Remains in the BUSY state until it finishes moving to the specified position.

Inside the driver, -2,097,152 and 2,097,151 are located next to each other in a loop.

### `/goToDir (int)motorID (bool)DIR (int)position`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|DIR|0-1||
|position|-2,097,152 - 2,097,151|Destination|

#### Executable timing
In motion start condition

#### Description
Moves to the specified position in the specified direction according to the pre-set speed profile. Remains in the BUSY state until it finishes moving to the specified position.

## Stops
### `/softStop (int)motorID`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|

#### Executable timing
Always

#### Description
After decelerating according to the speed profile, the motor stops while it is kept excited. Remains in the BUSY state until the motor stops. If it was originally in the High Z state, the motor will be excited while it keeps its position.

If it was in the servo mode, the mode will be released.

### `/hardStop (int)motorID`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|

#### Executable timing
Always

#### Description
Immediately stops the motor and leaves it excited. Remains in the BUSY state until the motor stops. If it was originally in the High Z state, the motor is excited while it keeps its position.

If it was in the servo mode, the mode will be released.

### `/softHiZ (int)motorID`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|

#### Executable timing
Always

#### Description
Decelerate according to the speed profile, then stop the motor and release excitation. When the excitation is released, it goes into the High Z state. It remains in the BUSY state until the motor is stopped.
If it was in the servo mode, it will be released.
if electromagnetic brake mode is enabled, the controller puts the brake into hold state, and then transits to High Z state.

### `/hardHiZ (int)motorID`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|

#### Executable timing
Always

#### Description
Immediately stops the motor and releases the stepper excitation. When the motor excitation is released, it goes into the High Z state. Remains in the BUSY state until the motor is stopped.
If it was in the servo mode, it will be released.
if electromagnetic brake mode is enabled, the controller puts the brake into hold state, and then transits to High Z state.