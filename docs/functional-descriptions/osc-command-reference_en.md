## Overview

This is a reference for Open Sound Control commands.

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
| (int) | Value of an integer. Depending on the command, the acceptable range of the value may vary. |
| (float) | Value of floating-point numbers. Range of the value may also vary depending on the command. |
| (bool) | Logical value. Either 1 or 0. |

### Command Executable Timing

Some commands have limited executable timing. It is described in "Timing" in each command reference information.


| Item | Description |
|--------|--------|
| Always | The command can be sent at any moment of operation. |
| Not in Busy State | The command can be sent when the device is not in a busy state.
| Motor stopped | The command can be sent when the motor is stopped  |
| HiZ State | The command can be sent when the driver output is in HiZ (high-impedance) state |

## Points to Keep in Mind

The board may exhibit an unexpected behavior if it sends out a large of OSC messages that are not delivered to the destination. Therefore no OSC message will be sent before the board receives `/setDestIp` message.