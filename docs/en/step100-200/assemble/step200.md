---
title: Prepare X-Nucleo - STEP200
---

# Prepare X-Nucleo - STEP200

How to modify the X-NUCLEO-IHM02A1 so that it can be stacked on the Ethernet shield.

## STEP200 (X-NUCLEO-IHM02A1) {#step200}

| Arduino | (Ethernet) | Default | Modified | Firmware | Note |
| --- | --- | --- | --- | --- | --- |
| D0 |  |  |  |  |  |
| D1 |  |  |  |  |  |
| D2 |  |  |  |  |  |
| D3 |  | SCK | LED | LED | #1 |
| D4 | SD CS | STBY/RST | SD CS | SD CS | #2 |
| D5 |  |  |  |  |  |
| D6 |  |  |  |  |  |
| D7 |  |  |  |  |  |
| D8 |  |  | STBY/RST | RST - L6470 | #2 |
| D9 |  |  |  |  |  |
| D10 | CS |  |  | CS - W5500 |  |
| D11 |  | MOSI | MOSI | MOSI - L6470 |  |
| D12 |  | MISO | MISO | MISO - L6470 |  |
| D13 |  |  | SCK | SCK - L6470 | #1 |
| A0 |  |  |  |  |  |
| A1 |  |  |  |  |  |
| A2 |  | CS | CS | CS - L6470 |  |
| A3 |  |  |  |  |  |
| A4 |  |  |  |  |  |
| A5 |  |  |  |  |  |
| MOSI | MOSI |  |  | MOSI - W5500 | SPI pin header |
| MISO | MISO |  |  | MISO - W5500 | SPI pin header |
| SCK | SCK |  |  | SCK - W5500 | SPI pin header |

### 1: Move L6470 SCK {#sck}

Initially the SCK pin of the L6470 on the IHM02A1 is D3, but move it to D13 to fit the SPI pin layout of the Arduino. Remove the 0 Ω resistor at `SB34` of the IHM02A1, and move it to the `SB12` pad. This is difficult without two soldering irons. Alternatively, you can crush the `SB34` resistor with cutting pliers and short the `SB12` pad with solder.

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643345862191.png)  
In this photo, I had a hard time reattaching the removed resistor to SB12, and it became dirty.

### 2: SD CS and L6470 STBY/RST {#stby-rst}

As with the STEP100, the CS pin of the microSD card and the STBY/RST pin of the L6470 are both assigned to D4, so cut the leg of that pin on the IHM02A1. The STBY/RST pin is required to start the L6470, so assign it to another pin with a jump wire. The firmware expects it on D8 (`PIN_DRIVER_RESET` in `boardsDef.h`), so use D8; another pin needs a change of `boardsDef.h`. Connect D4 and D8 with a jump wire on the pin socket of the X-NUCLEO board.

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643345928788.png)  
The X-NUCLEO board stacked on the Arduino and the Ethernet shield. D4 of the X-NUCLEO board is now reassigned to D8.
