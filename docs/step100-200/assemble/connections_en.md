---
title: Connections
wp_id: 2304
slug: connections
lang: en
link: "https://ponoor.com/en/docs/step100-200/assemble/connections/"
date: "2022-02-02T21:48:15"
modified: "2022-02-03T14:01:24"
parent: 2293
menu_order: 43
---

# Connections

## Stacking order

Arduino and Ethernet shield are communicate via the 6 pins SPI connector, but it doesn't exist on X-Nucleos. Also, the D4 leg of X-Nuleco was cutted when preparing it and that pin is required for the Ethernet shield.

Therefore, the stacking order should always be as follows;

1. the Ethernet Shield on the Arduino
2. X-Nucleo on top of them

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643346463746.png)  
The photo shows STEP200. The Ethernet Shield is on top of the Arduino M0, and the X-NUCLEO-IHM02A1 is on top of them.

## Connections

### Power supply

Connect the power supply to the X-Nucleo. A positive and negative terminals are indicated as follows.

NOTE: Do not turn on the power until you have finished writing the firmware.

| Polarity | IHM03A1 (STEP100) | IHM02A1 (STEP200) |
| --- | --- | --- |
| Positive | `Vin` | `VS+` |
| Negative | `GND` | `-` |

![](https://ponoor.com/cms/wp-content/uploads/2022/01/IMG_4315.jpg)![](https://ponoor.com/cms/wp-content/uploads/2022/01/IMG_4314.jpg)

### Motor

Connect a bipolar stepping motor. This type of motor contains two pairs of coils, and these pairs should be connected to correspond with the paired outputs on the driver side. The pair can be checked with the motor datasheet or by measuring the resistance between 4 wires with a tester.

The indication of the pair on the board are as follows, but it is confusing especially for IHM02A1 (L6470).

| Motor coil | IHM03A1 | IHM02A1 |
| --- | --- | --- |
| Coil 1 | A+, A- | 1A, 2A |
| Coil 2 | B+, B- | 1B, 2B |

[![](https://ponoor.com/cms/wp-content/uploads/2022/02/step200_wiring-700x510.png)](https://ponoor.com/cms/wp-content/uploads/2022/02/step200_wiring.png)
