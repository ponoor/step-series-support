---
title: Servo mode
wp_id: 1008
slug: servo-mode
lang: en
link: "https://ponoor.com/en/docs/step-series/osc-command-reference/servo-mode/"
date: "2020-11-05T12:35:59"
modified: "2021-08-28T15:36:05"
parent: 886
menu_order: 87
---

# Servo mode

### `/enableServoMode (int)motorID (bool)enable`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | motor ID |
| enable | 0-1 | 1:Enable, 0:Disable |

#### Executable timing

Always

#### Description

Turns on/off the servo mode (position tracking mode). To avoid sudden movement, the current position at the moment of activation is set to the target position.

It is not possible to send other motor control commands such as `/run` or `/goTo` while operating in this mode.

### `/setServoParam (int)motorID (float)kP (float)kI (float)kD`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | motor ID |
| kP | 0.0- | Proportional control gain |
| kI | 0.0- | Integral control gain |
| kD | 0.0- | Differential control gain |

#### Executable timing

Always

#### Description

Adjusts the PID control gain.

#### Initial value

| Argument | Initial value |
| --- | --- |
| kP | 0.06 |
| kI | 0 |
| kD | 0 |

### `/getServoParam (int)motorID`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | motor ID |

#### Executable timing

Always

#### Response

```
/servoParam (int)motorID (float)kP (float)kI (float)kD
```

| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | motor ID |
| kP | 0.0- | Proportional control gain |
| kI | 0.0- | Integral control gain |
| kD | 0.0- | Differential control gain |

### `/setTargetPosition (int)motorID (int)position`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | motor ID |
| position | -2,097,152 - 2,097,151 | target position |

#### Executable timing

Always

#### Description

Sets the target position in servo mode.

### `/setTargetPositionList (int)position1 (int)position2 (int)position3 (int)position4`

#### Argument

| Argument | Range | Description |
| --- | --- | --- |
| position[1-4] | -2,097,152 - 2,097,151 | target position |

#### Executable timing

Always

#### Description

Sets the target positions of the servo mode for all 4 axes at once.
