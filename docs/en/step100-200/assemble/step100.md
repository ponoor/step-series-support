---
title: Prepare X-Nucleo - STEP100
---

# Prepare X-Nucleo - STEP100

How to modify the X-NUCLEO-IHM03A1 so that it can be stacked on the Ethernet shield.

## STEP100 (X-NUCLEO-IHM03A1) {#step100}

The table is for the default build; with `MZERO_WITH_ZERO_BOOTLOADER` the SD CS pin is D2 ([Upload the Arduino sketch](../upload-the-sketch.md#m0)). Some pins that the IHM03A1 uses overlap with the pins of the Ethernet shield, so the pin assignment of the IHM03A1 must be modified.

| Arduino | (Ethernet) | Default | Modified | Firmware | Note |
| --- | --- | --- | --- | --- | --- |
| D0 |  |  |  |  |  |
| D1 |  |  |  |  |  |
| D2 |  | FLAG | FLAG |  | Not in use |
| D3 |  |  |  | LED | Optional |
| D4 | SD CS | BUSY |  | SD CS | #1 |
| D5 |  |  |  |  |  |
| D6 |  |  |  |  |  |
| D7 |  |  |  |  |  |
| D8 |  | RST | RST | RST - PowerSTEP01 |  |
| D9 |  | STCK | STCK |  | Not in use |
| D10 | CS | CS |  | CS - W5500 | #2 |
| D11 |  | MOSI | MOSI | MOSI - PowerSTEP01 |  |
| D12 |  | MISO | MISO | MISO - PowerSTEP01 |  |
| D13 |  | SCK | SCK | SCK - PowerSTEP01 |  |
| A0 |  | ID | ID |  | Not in use |
| A1 |  |  |  |  |  |
| A2 |  |  | CS | CS - PowerSTEP01 | #2 |
| A3 |  |  |  |  |  |
| A4 |  |  |  |  |  |
| A5 |  |  |  |  |  |
| MOSI | MOSI |  |  | MOSI - W5500 | SPI pin header |
| MISO | MISO |  |  | MISO - W5500 | SPI pin header |
| SCK | SCK |  |  | SCK - W5500 | SPI pin header |

### 1: SD CS and PowerSTEP01 BUSY {#sd-cs}

The D4 pin is the CS pin when the Ethernet shield reads the microSD card, but it is also the BUSY pin of the IHM03A1. Unfortunately neither can be changed easily, so cut the leg of that pin on the IHM03A1. The pin tells that the PowerSTEP01 is in the BUSY state, but the same information is available through SPI, so there is no need to connect it to the Arduino. You can cut it.

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643345614045.png)

### 2: W5500 CS and PowerSTEP01 CS {#cs}

The CS pin of the W5500 (or W5100) on the Ethernet shield and the CS pin of the PowerSTEP01 on the IHM03A1 are both wired to D10, so change the IHM03A1 side. Remove the 0 Ω resistor at `R10` of the IHM03A1, and solder it to the `R9` pad. The CS pin of the PowerSTEP01 is now A2, not D10.

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643345121196.png)

When you remove the resistor, you need to heat the pads on both sides at the same time. Two soldering irons make it easiest.
