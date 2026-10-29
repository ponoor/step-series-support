---
title: Assemble
---

# Assemble

Assemble the STEP100 or the STEP200 in this order. You need to modify the X-NUCLEO board before you stack the boards, so read the page of your model first.

1. Prepare the X-NUCLEO board: [STEP100 (X-NUCLEO-IHM03A1)](step100.md) or [STEP200 (X-NUCLEO-IHM02A1)](step200.md). Cut a pin, and move a resistor, so that the pins do not overlap with the Ethernet shield.
2. [Connections](connections.md): stack the Arduino, the Ethernet shield and the X-NUCLEO board, and connect the power supply and the motor.

Do not turn on the power until you have written the firmware ([Upload the Arduino sketch](../upload-the-sketch.md)).
