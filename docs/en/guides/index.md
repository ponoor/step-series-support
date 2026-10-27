---
title: Functional guides
---

# Functional guides

The functional guides explain how each function of the STEP Series works: the concepts, the states and how they change, and which commands to use in which order. They describe what happens and why. The arguments, the ranges and the replies of each command are in the [OSC command reference](../reference/index.md), which the guides link to.

## Guides {#guides}

- [Communication and messages](communication-and-messages.md): how the board sends and receives OSC messages, `/setDestIp`, replies and automatically sent messages, and the errors of the arguments.
- [Voltage mode and current mode](voltage-and-current-mode.md): the two ways of driving the motor, KVAL and TVAL, and how to switch between them.
- [Speed profile and types of motor motion](speed-profile-and-motions.md): acceleration, deceleration and maximum speed; constant speed, positioning and the four kinds of stop.
- [Homing and position management](homing-and-position.md): finding the reference position with the HOME and LIMIT switches, and the collision prevention settings.
- [Servo mode](servo-mode.md): following a target position that changes in real time, and how to tune the PID gains.
- [Electromagnetic brake](electromagnetic-brake.md): the states of the brake, how each command acts on it, and what to keep in mind for a hanging load.
- [Alarms and protection](alarms-and-protection.md): undervoltage lockout, overtemperature, overcurrent and stall, and how the board reports them.

For the connections and the settings, see [Connections and settings](../connections/index.md).
