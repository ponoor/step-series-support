## Overview

This is a reference for Open Sound Control commands. Commands are common between STEP400 and STEP800 but some commands are only available in STEP400 (Noted as `STEP400 Only`). And there are some other commands which have different setting values. Please check "[Differences between STEP400 and STEP800](https://ponoor.com/en/docs/step-series/osc-command-reference/differences-between-step400-and-step800/)" for details.

You must send a single OSC message, not as an OSC bundle, which is combined multiple OSC messages.

## Motor ID

The Motor ID for OSC commands corresponds with the number printed on the circuit board. Depending on the command, you can send the same instruction to all motors at once. To do this, the ID must be specified as 255.

Because of this, the ID numbers that can be used for a command are any of the following;

| Product | motor ID range |
| --- | --- |
| STEP400 | 1-4, 255 |
| STEP800 | 1-8, 255 |

## Notation

### Argument Types

| Item | Description |
|--------|--------|
| (int) | Value of an integer. <br />Depending on the command, the acceptable range of the value may vary. |
| (float) | Value of floating-point numbers. <br />Range of the value may also vary depending on the command. |
| (bool) | Logical value. Either 1 or 0 as integer.|
| (Symbol) | String (OSC-string). |

#### Messages from the controller

The [OSC specification](https://opensoundcontrol.stanford.edu/spec-1_0.html) defines the types of arguments as integer (int32), floating-point number (float32), string (OSC-string) and more, as well as non-standard types such as logical value True/False. But STEP series always sends logical values as integer. This is valid the Universal firmware v1.1.0 or later.

No OSC message will be sent before the controller receives `/setDestIp` message.

#### Messages to the controller
All arguments are converted if necessary when they are received. For example, a logical value can be sent as integer or float. A string will cause an error.

| Type | Judged as 1 | Judged as 0 |
| --- | --- | --- |
| int32 | 1 or more | 0 or less |
| float32 | 1.0 or more | less than 1.0 |
| logical value | True | False |
| OSC-string | Error | Error |

In the same way, integers and floating point numbers are converted to each other. In this case, logical values and strings are in error.

### Command Executable Timing

Some commands have limited executable timing. It is described in "Timing" in each command reference information.


| Item | Description |
|--------|--------|
| Always | Always executable |
| Not in Busy State | Executable when the controller is not in a busy state.
| Motor stopped | Executable when the motor is stopped  |
| HiZ State | Executable when the driver output is in HiZ (high-impedance) state |
| In motion start condition | Executable when all conditions for motions are cleared |

#### Motion start condition
Following conditions should be cleared:
- The electromagnetic brake is released.
- Not in a servo mode.

In addition, the set value of the command you are trying to send must meet the following conditions:
- Not trying to move toward `homingDirection` when `/setProhibitMotionOnHomeSw` set and the HOME switch activated.
- Not trying to move toward counter `homingDirection` when `/setProhibitMotionOnLimitSw` set and the LIMIT switch activated.


## Points to Keep in Mind

The board may exhibit an unexpected behavior if it sends out a large of OSC messages that are not delivered to the destination. Therefore no OSC message will be sent before the controller receives `/setDestIp` message.