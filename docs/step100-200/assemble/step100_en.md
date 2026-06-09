---
title: Prepare X-Nucleo – STEP100
wp_id: 2295
slug: step100
lang: en
link: "https://ponoor.com/en/docs/step100-200/assemble/step100/"
date: "2022-01-28T13:54:28"
modified: "2022-02-03T12:49:47"
parent: 2293
menu_order: 13
---

# Prepare X-Nucleo &#8211; STEP100

## STEP100 (X-NUCLEO-IHM03A1)

Since some pins used by IHM03A1 and Ethernet Shield are overlapped so we need modify the IHM03A1 pin assignments.

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

### 1: SD CS and PowerSTEP01 BUSY

The D4 pin is used as the CS pin when reading the SD card on the Ethernet Shield, but it is also used as the BUSY pin on the IHM03A1. Unfortunately, the pins on both cannot be easily changed, so we are going to cut the legs on the IHM03A1.  
This pin indicates that the PowerSTEP01 is in BUSY state, but since the same information can be obtained via SPI, so there is no particular need to connect it to the Arduino. You can just cut it.

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643345614045.png)

### 2: W5500 CS and PowerSTEP01 CS

The CS pin of the W5500 (or W5100) on the Ethernet Shield and the CS pin of the PowerSTEP01 on the IHM03A1 are both wired to D10, so change the IHM03A1 side. Remove the 0Ω resistor at `R10` on the IHM03A1, then solder it to `R9` pad. Now, the CS pin of PowerSTEP01 is changed from D10 to A2 pin.

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643345121196.png)

When removing the resistor, you need to heat the pads on both sides at the same time. Using two soldering irons is the easiest way to do this.
