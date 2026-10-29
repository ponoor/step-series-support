---
title: Connections
---

# Connections

How to stack the boards, and how to connect the power supply and the motor to the X-NUCLEO board.

## Stacking order {#stacking-order}

The Arduino and the Ethernet shield communicate through the 6-pin SPI connector, which the X-NUCLEO boards do not have. Also, the D4 leg of the X-NUCLEO board was cut when you prepared it, and the Ethernet shield needs that pin.

So the stacking order must always be:

1. The Ethernet shield on the Arduino
2. The X-NUCLEO board on top of them

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643346463746.png)  
The photo shows the STEP200. The Ethernet shield is on the Arduino M0, and the X-NUCLEO-IHM02A1 is on top of them.

## Connections {#connections}

### Power supply {#power-supply}

Connect the power supply to the X-NUCLEO board. The positive and negative terminals are marked as follows.

!!! warning "Do not turn on the power until the firmware is written"
    Turn on the power after you have written the firmware ([Upload the Arduino sketch](../upload-the-sketch.md)).

| Polarity | IHM03A1 (STEP100) | IHM02A1 (STEP200) |
| --- | --- | --- |
| Positive | `Vin` | `VS+` |
| Negative | `GND` | `-` |

![](https://ponoor.com/cms/wp-content/uploads/2022/01/IMG_4315.jpg)![](https://ponoor.com/cms/wp-content/uploads/2022/01/IMG_4314.jpg)

### Motor {#motor}

Connect a bipolar stepper motor. This type of motor has two coils, and you connect each coil to a pair of outputs of the driver. You can find the pairs in the datasheet of the motor, or by measuring the resistance between the 4 wires with a multimeter.

The marks of the pairs on the board are as follows, but they are confusing, especially on the IHM02A1 (L6470).

| Motor coil | IHM03A1 | IHM02A1 |
| --- | --- | --- |
| Coil 1 | A+, A- | 1A, 2A |
| Coil 2 | B+, B- | 1B, 2B |

[![](https://ponoor.com/cms/wp-content/uploads/2022/02/step200_wiring-700x510.png)](https://ponoor.com/cms/wp-content/uploads/2022/02/step200_wiring.png)
