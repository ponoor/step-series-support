---
title: Motor control
wp_id: 1002
slug: motor-control
lang: en
link: "https://ponoor.com/en/docs/step-series/osc-command-reference/motor-control/"
date: "2020-11-05T12:34:07"
modified: "2022-03-30T12:18:09"
parent: 886
menu_order: 78
---

# Motor control

## Motor movement

### `/run (int)motorID (float)speed`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | motor ID |
| speed | -15625 - 15625 [step/s] | Rotation speed |

#### Executable timing

In motion start condition

#### Description

Rotates the motor at specified speed. The acceleration is controlled with the pre-set speed profile. The speed is limited by maxSpeed. It remains in the BUSY state until the motor reaches the specified speed.

### `/move (int)motorID (int)step`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | motor ID |
| step | Moving step counts |

#### Executable timing

When the motor is stopped, and In motion start condition.

#### Description

Moves specified number of steps according to the pre-set speed profile. It remains in the BUSY state until it reaches the specified step count. This command can only execute when the motor is stopped.

### `/goTo (int)motorID (int)position`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | motor ID |
| position | -2,097,152 - 2,097,151 | Destination |

#### Executable timing

In motion start condition

#### Description

Moves to the specified position in the shortest route according to the pre-set speed profile. Remains in the BUSY state until it finishes moving to the specified position.

Inside the driver, -2,097,152 and 2,097,151 are located next to each other in a loop.

### `/goToDir (int)motorID (bool)DIR (int)position`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | motor ID |
| DIR | 0-1 |
| position | -2,097,152 - 2,097,151 | Destination |

#### Executable timing

In motion start condition

#### Description

Moves to the specified position in the specified direction according to the pre-set speed profile. Remains in the BUSY state until it finishes moving to the specified position.

## Stops

### `/softStop (int)motorID`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | motor ID |

#### Executable timing

Always

#### Description

After decelerating according to the speed profile, the motor stops while it is kept excited. Remains in the BUSY state until the motor stops. If it was originally in the High Z state, the motor will be excited while it keeps its position.

If it was in the servo mode, the mode will be released.

### `/hardStop (int)motorID`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | motor ID |

#### Executable timing

Always

#### Description

Immediately stops the motor and leaves it excited. Remains in the BUSY state until the motor stops. If it was originally in the High Z state, the motor is excited while it keeps its position.

If it was in the servo mode, the mode will be released.

### `/softHiZ (int)motorID`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | motor ID |

#### Executable timing

Always

#### Description

Decelerate according to the speed profile, then stop the motor and release excitation. When the excitation is released, it goes into the High Z state. It remains in the BUSY state until the motor is stopped.  
If it was in the servo mode, it will be released.  
if electromagnetic brake mode is enabled, the controller puts the brake into hold state, and then transits to High Z state.

### `/hardHiZ (int)motorID`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | motor ID |

#### Executable timing

Always

#### Description

Immediately stops the motor and releases the stepper excitation. When the motor excitation is released, it goes into the High Z state. Remains in the BUSY state until the motor is stopped.  
If it was in the servo mode, it will be released.  
if electromagnetic brake mode is enabled, the controller puts the brake into hold state, and then transits to High Z state.

## Combined commands

### `/combinedRun (float)speed1 ... (float)speedN`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| speed1 ... speedN | -15625 - 15625 [step/s] | Rotation speed for each motor |

#### Executable timing

In motion start condition

#### Description

Runs all motors at the specified speeds. The number of arguments matches the number of motors (4 for STEP400, 8 for STEP800).

### `/combinedMove (int)step1 ... (int)stepN`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| step1 ... stepN | | Moving step counts for each motor |

#### Executable timing

When the motor is stopped, and In motion start condition.

#### Description

Moves all motors the specified number of steps. The number of arguments matches the number of motors (4 for STEP400, 8 for STEP800).

### `/combinedGoTo (int)position1 ... (int)positionN`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| position1 ... positionN | -2,097,152 - 2,097,151 | Destination for each motor |

#### Executable timing

In motion start condition

#### Description

Moves all motors to the specified positions in the shortest route.

### `/combinedGoToDir (bool)DIR1 (int)position1 ... (bool)DIRN (int)positionN`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| DIR | 0-1 | Direction for each motor |
| position | -2,097,152 - 2,097,151 | Destination for each motor |

#### Executable timing

In motion start condition

#### Description

Moves all motors to the specified positions in the specified directions.

### `/combinedSoftStop`

#### Argument

None

#### Executable timing

Always

#### Description

Decelerates and stops all motors while keeping them excited.

### `/combinedHardStop`

#### Argument

None

#### Executable timing

Always

#### Description

Immediately stops all motors while keeping them excited.

### `/combinedSoftHiZ`

#### Argument

None

#### Executable timing

Always

#### Description

Decelerates and stops all motors, then releases excitation (High Z state).

### `/combinedHardHiZ`

#### Argument

None

#### Executable timing

Always

#### Description

Immediately stops all motors and releases excitation (High Z state).

## Raw register value commands

The following commands use raw driver IC register values for speed without unit conversion.

### `/runRaw (int)motorID (int)speed`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | motor ID |
| speed | | Rotation speed (raw register value, signed) |

#### Executable timing

In motion start condition

#### Description

Rotates the motor at the specified speed using a raw register value. The sign of the speed value determines the direction.

### `/goUntilRaw (int)motorID (bool)ACT (int)speed`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | motor ID |
| ACT | 0-1 | Same as `/goUntil` |
| speed | | Speed (raw register value, signed) |

#### Executable timing

Always

#### Description

Same as `/goUntil` but uses a raw register value for speed. The sign of the speed value determines the direction.

### `/combinedRunRaw (int)speed1 ... (int)speedN`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| speed1 ... speedN | | Rotation speed for each motor (raw register value, signed) |

#### Executable timing

In motion start condition

#### Description

Runs all motors at the specified speeds using raw register values. The number of arguments matches the number of motors (4 for STEP400, 8 for STEP800).
