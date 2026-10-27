---
title: EMB-STEP400
---

# EMB-STEP400

The EMB-STEP400 is a brake board for the STEP400. It drives the electromagnetic brakes of 4 motors, and the STEP400 controls it. What an electromagnetic brake is and how the board controls it are explained in [Electromagnetic brake](../guides/electromagnetic-brake.md#what). The wiring is in [Electromagnetic brake wiring](../connections/electromagnetic-brake-wiring.md).

## Specifications {#specifications}

- Input voltage: 5 V to 48 V
- Control channels: 4
- PCB size: 45 x 56 mm

When you supply less than 12 V, the indicator LED may not be visible.

### Driving current {#driving-current}

The rating of the switching MOSFET is 60 V and 28 A, according to its [datasheet](https://datasheet.lcsc.com/szlcsc/Winsok-Semicon-WSF28N06_C148431.pdf). The actual limit is the rating of the terminal block of the power input, which is 7 A. Within this range, you can also drive other loads, such as LEDs or motors.

### Behavior at power-on {#power-on}

The gate of each MOSFET is pulled down with a resistor (10 kΩ, in the circuit diagram). When the input from the STEP400 is not driven, for example until the firmware of the STEP400 starts, the brake is engaged.

## PCB drawing {#drawing}

[![](https://ponoor.com/cms/wp-content/uploads/2021/03/step400-emb-dimension.png)](https://ponoor.com/cms/wp-content/uploads/2021/03/step400-emb-dimension.png)

[step400-emb-dimension.pdf](https://ponoor.com/cms/wp-content/uploads/2021/03/step400-emb-dimension.pdf)

## Circuit diagram {#schematic}

[![](https://ponoor.com/cms/wp-content/uploads/2021/03/stem400-emb-schematic.png)](https://ponoor.com/cms/wp-content/uploads/2021/03/stem400-emb-schematic.png)

[step400-brakeBoard-schematic.pdf](https://ponoor.com/cms/wp-content/uploads/2021/03/step400-brakeBoard-schematic.pdf)

## Accessories {#accessories}

- 3.81 mm pitch, 2-pin Euro-style terminal block x 5
- 6-pin ribbon cable
