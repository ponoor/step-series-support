---
title: "OSC command reference: common rules"
---

# OSC command reference: common rules

## Overview

For a quick reference table of all commands, see the [Command list](command-list.md).

This is a reference for the Open Sound Control (OSC) commands. The commands are common to STEP400 and STEP800, but some commands are available only on STEP400 (marked "Available on STEP400 only."), and some have different values on each board. See [Differences between STEP400 and STEP800](differences-step400-step800.md) for details.

Send each command as a single OSC message, not as an OSC bundle (several OSC messages combined). Bundles are not supported.

## Motor ID

The motor ID of an OSC command corresponds to the number printed on the circuit board. Some commands can send the same instruction to all motors at once; specify 255 as the motor ID for this.

The motor IDs that can be used in a command are:

| Product | Motor ID range |
| --- | --- |
| STEP400 | 1-4, 255 |
| STEP800 | 1-8, 255 |

## Notation

### Argument types

| Item | Description |
| --- | --- |
| (int) | An integer. The range that can actually be sent depends on the command. |
| (float) | A floating-point number. The range that can actually be sent depends on the command. |
| (bool) | A logical value, sent as the integer 1 or 0. It is written as bool to show that the range is 0 and 1. |
| (string) | A string (OSC-string). |

### Messages from the board

The [OSC specification](https://opensoundcontrol.stanford.edu/spec-1_0.html) defines the argument types integer (int32), floating-point number (float32), string (OSC-string) and others, as well as non-standard types such as the logical values True / False. The STEP series always sends a logical value as the integer 0 or 1 (type tag `i`), never as True / False. Before v2.2.0, a few messages still used True / False (see the [Migration guide](../maintenance/migration-guide.md)).

### Messages to the board

The board checks the arguments of a command before it applies the command. When a check fails, nothing is applied.

| Case | Reply |
| --- | --- |
| Fewer arguments than the command needs | `/error/osc MissingArgument` |
| An argument of the wrong type: a string for a number, NaN or infinity, or a non-string for `/setConfigName` | `/error/osc WrongDataType` |
| A motor ID outside the range of the board | `/error/command MotorIdNotMatch` with the motor ID sent |
| A value outside the range of the command | `/error/command CommandIgnored` |
| More than 16 arguments, or a packet larger than 512 bytes | `/error/osc OscSyntaxError` |

Arguments beyond the ones a command needs are ignored. The errors are not sent while the error report is disabled ([`/reportError`](system-settings.md#reporterror)). See [Automatically sent messages](automatically-sent-messages.md) for the error messages.

An integer and a floating-point number are converted into each other when they are received. A logical value is accepted as an integer, a float, or the OSC logical value True / False:

| Type | Judged as 1 | Judged as 0 |
| --- | --- | --- |
| int32 | greater than 0 | 0 or less |
| float32 | 1.0 or more | less than 1.0 |
| Logical value | True | False |

### Command executable timing

Some commands can be executed only in a certain state. It is shown as "Executable timing" in the reference of each command.

| Item | Description |
| --- | --- |
| Always | The command can always be executed. |
| When the motor is stopped | The command can be executed while the motor is stopped (a motor that is HiZ also counts). While the motor is turning, `/error/command MotorNotStopped` is replied and nothing is applied. |
| High Z state | The command can be executed while the driver output is HiZ. A motor holding its position is not HiZ: send [`/softHiZ`](motor-control.md#softhiz) or [`/hardHiZ`](motor-control.md#hardhiz) first. Otherwise `/error/command MotorNotHiZ` is replied and nothing is applied. |
| In motion start condition | The command can be executed when the conditions for motions are met (see below). |

HiZ is the state in which the outputs of the motor driver are high-impedance and no current flows in the motor, so the motor is not energized.

#### Motion start condition

Both of the following must be true:

- The electromagnetic brake is released.
- The board is not in the servo mode.

In addition, the values of the command you send must meet the following conditions:

- The command does not move toward `homingDirection` while [`/setProhibitMotionOnHomeSw`](alarm-settings.md#setprohibitmotiononhomesw) is set and the HOME switch is on.
- The command does not move against `homingDirection` while [`/setProhibitMotionOnLimitSw`](alarm-settings.md#setprohibitmotiononlimitsw) is set and the LIMIT switch is on.

A motion command that does not meet the conditions is rejected with an error such as `BrakeEngaged`, `InServoMode`, `HomeSwActivating` or `LimitSwActivating`. The errors of each command are listed in its reference.

## Points to keep in mind

- The board sends no OSC message, except the broadcast [`/booted`](automatically-sent-messages.md#booted), until it receives [`/setDestIp`](system-settings.md#setdestip). The board can behave unexpectedly if it sends a large number of messages that do not reach the destination. (With the configuration tool you can make the board send without waiting for `/setDestIp`.)
- The messages to the destination are also dropped while the board resolves the MAC address of the destination (up to a few seconds after `/setDestIp`). For details, see [Communication and messages](../guides/communication-and-messages.md).
