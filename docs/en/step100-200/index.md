---
title: STEP100/200
---

# STEP100/200

The STEP100 and the STEP200 are do-it-yourself motor drivers: you collect the modules and assemble them yourself. This section explains how to get the materials, how to assemble them, how to write the firmware, and how they differ in use.

!!! warning "Not tested on real hardware since v2.1.0"
    The firmware v2.2.0 can be built for the STEP100 and the STEP200, but they have not been tested on real hardware since v2.1.0. The procedures in this section follow the source code of the firmware and the earlier documents.

## Overview {#overview}

| Model | Driver IC | Motors | In other words |
| --- | --- | --- | --- |
| STEP100 | PowerSTEP01 | 1 | A small STEP400 |
| STEP200 | L6470 | 2 | A small STEP800 |

The [firmware](https://github.com/ponoor/step-series-universal-firmware) is provided as an open source project, and the same source builds all the STEP Series.

This section mainly describes how to assemble and how to write the firmware. For the actual usage, read the documents of the STEP400 and the STEP800 and replace the range of the motor ID as appropriate (the table is in [Usage](usage.md#motor-id)). The other differences are explained in [Usage](usage.md).

## Pages {#pages}

1. [Get the materials](get-the-materials.md): the Arduino, the Ethernet shield, the X-NUCLEO board and the power supply.
2. [Assemble](assemble/index.md): prepare the X-NUCLEO board ([STEP100](assemble/step100.md), [STEP200](assemble/step200.md)), stack the boards and [connect](assemble/connections.md) the power supply and the motor.
3. [Upload the Arduino sketch](upload-the-sketch.md): build the firmware and write it to the Arduino.
4. [Usage](usage.md): the differences from the STEP400 and the STEP800.

## Resources {#resources}

- [Product: STEP100/200](https://ponoor.com/products/step100-200/)
- [Updates: Pros and Cons of Stepper Motors](https://ponoor.com/en/updates/2020/11/pros-and-cons-of-stepper-motors/)
- [Updates: OSC and Programming Environments](https://ponoor.com/en/updates/2020/12/video-step400-800-osc-example-files/)
- [Updates: How To Get Started With Mechanical Parts](https://ponoor.com/en/updates/2021/01/how-to-get-started-with-mechanical-parts/)

The firmware, the forum and the browser configuration tool are listed on the [top page](../index.md#resources).
