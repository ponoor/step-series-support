---
title: Overview
---

# Overview

This page introduces the products of the STEP Series, what you can do with them, the software that sends OSC messages, and how this documentation is organized.

## Products {#products}

All the products run the same firmware. They differ in the driver IC, the number of motors and the inputs and outputs of the board.

| Product | Driver IC | Motors | Drive mode | Switch inputs | Electromagnetic brake output | Form |
| --- | --- | --- | --- | --- | --- | --- |
| [STEP400](../hardware/step400.md) | PowerSTEP01 | 4 | Voltage mode and current mode | HOME and LIMIT | With the [EMB-STEP400](../hardware/emb-step400.md) board | Finished board |
| [STEP800](../hardware/step800.md) | L6470 | 8 | Voltage mode | HOME | On the board | Finished board |
| STEP100 | PowerSTEP01 | 1 | Voltage mode and current mode | HOME | None | Do-it-yourself |
| STEP200 | L6470 | 2 | Voltage mode | HOME | None | Do-it-yourself |

The commands are common to the products, but a command that needs a function that the board does not have is not available on it. The commands that differ between the STEP400 and the STEP800 are listed in [Differences between STEP400 and STEP800](../reference/differences-step400-step800.md). For the voltage mode and the current mode, see [Voltage mode and current mode](../guides/voltage-and-current-mode.md).

The STEP100 and the STEP200 are built from an Arduino Zero, an Ethernet shield and an X-NUCLEO board. The firmware can be built for them, but it has not been tested on real hardware since v2.1.0. See [STEP100 / STEP200](../step100-200/index.md).

## What you can do {#features}

- **Turn a motor at a speed, and move it to a position:** [Speed profile and types of motor motion](../guides/speed-profile-and-motions.md).
- **Find the reference position:** [Homing and position management](../guides/homing-and-position.md), with the HOME and LIMIT switches.
- **Make the motor follow a target that changes in real time:** [Servo mode](../guides/servo-mode.md).
- **Choose how the motor is driven:** [Voltage mode and current mode](../guides/voltage-and-current-mode.md), and how to decide KVAL and TVAL.
- **Hold a load when the motor is not powered:** [Electromagnetic brake](../guides/electromagnetic-brake.md).
- **Know how the board protects itself and what it reports:** [Alarms and protection](../guides/alarms-and-protection.md), and [Communication and messages](../guides/communication-and-messages.md) for the replies and the messages that the board sends by itself.
- **Keep the settings:** [How the settings work](../connections/how-settings-work.md). The board reads its settings from a microSD card at the start, and you can edit them with the [browser configuration tool](../connections/browser-config-tool.md).

## Software to send OSC {#software}

The STEP Series communicate with the Open Sound Control (OSC) protocol, so you need an application or a program that sends and receives OSC. Many environments can do it. These example files are provided:

- [Max](https://github.com/ponoor/step-series-example-Max) (recommended: its example covers the functions most completely. [Download Max](https://cycling74.com/downloads))
- [Processing](https://github.com/yuskegoto/STEP400_Processing) (thanks [@yuskegoto](https://github.com/yuskegoto))
- [openFrameworks](https://github.com/ponoor/step-series-example-openFrameworks) (thanks [@niimi](https://github.com/niimi))
- [Unity](https://github.com/ponoor/step-series-example-Unity) (thanks [@niimi](https://github.com/niimi))
- [TouchDesigner](https://github.com/ponoor/step-series-example-TouchDesigner) (thanks [@loveandsheep](https://github.com/loveandsheep), [@yuskegoto](https://github.com/yuskegoto))
- [Node-RED](https://github.com/yuskegoto/STEP400_Node-RED) (thanks [@yuskegoto](https://github.com/yuskegoto))
- [Python library](https://github.com/ponoor/python-step-series) (thanks [@JulianOrteil](https://github.com/JulianOrteil))

## How this documentation is organized {#organization}

The pages are of four kinds, by what you come to do. Each kind has the information for that purpose and leaves the rest to the others, and the pages link to each other.

- **Getting started** (this section): the steps for the first time. One path with the minimum of explanation: [Quick start](quickstart.md).
- **[Connections and settings](../connections/index.md)**: the procedures. Wiring, the network, and how to set up the board.
- **[Functional guides](../guides/index.md)**: the explanations. How a function works, which commands to use in which order, and what to be careful about.
- **[OSC reference](../reference/index.md)**: the reference. The exact specification of each command: the arguments, the ranges, the initial values and the replies. Look here to check a value; the values are written only in the reference.

Besides them, [Hardware](../hardware/step400.md) has the data of the boards, [Maintenance](../maintenance/index.md) has the firmware update, the build, the diagnosis and the troubleshooting, and [STEP100 / STEP200](../step100-200/index.md) is the section for the do-it-yourself versions.
