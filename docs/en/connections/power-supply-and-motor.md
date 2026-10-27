---
title: Power supply and motor
---

# Power supply and motor

How to connect a power supply and a motor to the STEP400 and the STEP800, and how to choose them.

## Connecting a power supply {#power-supply}

### Power supply {#power}

The two boards have different power ratings, and the power goes directly to the driver ICs. The control circuits get 5 V and 3.3 V from it through on-board converters.

When a PC is connected to the USB-C connector, only the control circuits are powered. The USB-C connector is for communication: USB supplies at most 5 V, which cannot drive the motor drivers. It is safe to connect USB while the power is supplied to one of the two power inputs below.

### Power terminals {#power-terminals}

The board has two power inputs: a DC barrel jack (4) and a screw terminal (5).

![](https://ponoor.com/cms/wp-content/uploads/2020/10/step400_connectors_numbering.jpg)

| Number | Description |
| --- | --- |
| 1 | Connector for the electromagnetic brake (STEP400) |
| 2 | Ethernet |
| 3 | USB type-C |
| 4 | DC barrel jack (power input) |
| 5 | Screw terminal (power input) |

The jack and the screw terminal are connected in parallel on the board. **Never connect a power supply to both of them. It damages the board.**

| Board | Supply voltage | DC barrel jack | Screw terminal |
| --- | --- | --- | --- |
| STEP400 | 12 V to 76 V @ 20 A | 24 V @ 5 A | 76 V @ 20 A |
| STEP800 | 9 V to 36 V @ 16 A | 24 V @ 5 A | 36 V @ 16 A |

The currents are the sum of the phase currents of all the motors, not the current capacity that the power supply needs; see [Current capacity](#current-capacity). One motor can draw at most 5 A on the STEP400 and 2 A on the STEP800. Keep these limits in mind when you choose a motor.

#### DC barrel jack {#dc-jack}

- 5.5 mm outer diameter
- 2.1 mm inner diameter
- Center positive

Use the screw terminal for a voltage or a current beyond the rating of the jack.

#### Screw terminal {#screw-terminal}

- Negative on the left, positive on the right
- M3 screws
- You can fasten the bare wire directly, but a wire terminal such as the `NICHIFU TMEX1.25-3N` is more secure.

## Connecting a motor {#motor}

### Choosing a motor {#choosing-motor}

The boards drive bipolar stepper motors. The phase current of the motor depends on the board:

| Board | Phase current |
| --- | --- |
| STEP400 | 5 A or less |
| STEP800 | 2 A or less |

How the motor current is set (KVAL and TVAL) is explained in [Voltage mode and current mode](../guides/voltage-and-current-mode.md#kval-tval), and the overcurrent threshold in [Alarms and protection](../guides/alarms-and-protection.md#thresholds).

We measured some motors and made configuration files with the register values that we calculated. See [Example parameter values for example steppers](example-parameters.md).

### Motor terminals {#motor-terminals}

![](https://ponoor.com/cms/wp-content/uploads/2020/10/image-1604122105179.png)

The motor terminal is a 3.81 mm (0.150") pitch Euro-style terminal block. Mating connectors include:

- TE Connectivity AMP Connectors 284507-4
- Ningbo Kangnex Elec WJ15EDGK-3.81-4P

A bipolar stepper motor has two coils. To connect it, find out which two of the four wires belong to the same coil. The datasheet of the motor gives the colors of the wires of each coil. With a multimeter you can also find the pairs: the resistance of a coil is very low.

Connect the wires of the two coils as follows. The wiring is the same for the STEP400 and the STEP800.

![](https://ponoor.com/cms/wp-content/uploads/2020/10/coil-wiring.png)

It does not matter which coil is A and which is B, nor in which order the two wires of a coil are connected. If you swap them, the motor works as before, but the direction of the rotation is reversed. It is convenient to use the same wiring rule for all the motors.

## Power supply and motor ratings {#ratings}

### Inductance {#inductance}

The copper winding of a stepper motor is an inductor. When a voltage is applied to it, the current does not flow at once but rises gradually. The motor is driven by switching the current on and off at every step, so the faster it turns, the shorter the cycle, and the less current can flow. The torque of a stepper motor is almost proportional to the current, so the maximum torque drops at high speed.

### Power supply voltage {#voltage}

To overcome the inductance and drive the current into the motor, use a power supply with as high a voltage as possible. The datasheet of a motor may give a very low rated voltage, but the motor cannot get the required current at that voltage when it turns. You need a voltage several times higher.

The graph below from an application note of ST shows the relation between the supply voltage and the current. The values depend on the motor, but at a low supply voltage the driver cannot supply enough current as the speed rises.

![](https://ponoor.com/cms/wp-content/uploads/2020/10/motor_current_example_graph-800x570.png)

The voltage that you need depends greatly on the rating of the motor, the speed and the torque that you need. As a rough guide:

- Up to NEMA17: 24 V
- NEMA23 or larger: 48 V, or 72 V for high speed

So the STEP800 may not be suitable for driving larger motors. Some small motors give a high torque, and some large ones cannot take much current, so **check the voltage and the current ratings of your motor**.

The STEP400 works from 12 V. That is the lower limit of its on-board DC-DC converter, so the voltage can drop in the wiring from the power supply at the inrush current when the motor starts, and the STEP400 can reset. We do not recommend 12 V except for a small motor with a low load.

![STEP400 working with the 48 V configuration, series of two 24V power supplies.](https://ponoor.com/cms/wp-content/uploads/2020/10/update-48V-configuration-800x533.jpg)

A STEP400 supplied with 48 V from two 24 V power supplies in series.

### Current capacity {#current-capacity}

The current capacity of the power supply is as important as its voltage. When a motor stalls, a large current can flow. If the capacity is not enough, the protection of the power supply works and the supply shuts down. A few amperes are enough for a small motor at a low speed, but a large motor or a high speed often needs a capacity of 10 A to 20 A. It depends on the number of motors, how you move them and the protection of the power supply, so choose one with as much margin as possible.
