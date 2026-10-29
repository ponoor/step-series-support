---
title: STEP800
---

# STEP800

The hardware of the STEP800: the board, its main components, the pin assignment, and the connectors that are not described elsewhere.

## Hardware overview {#overview}

### PCB size {#size}

120 x 80 mm, thickness 1.6 mm.

There are five M3 mounting holes: one at each corner and one near the middle.

![](https://ponoor.com/cms/wp-content/uploads/2021/09/step800_r1_0_0_dimension-1.png)  
The long parts at the top and the bottom of this picture are waste boards, and are removed after the production.

Actual size PDF: [step800_r1_0_0_dimension.pdf](https://github.com/ponoor/STEP800/blob/main/hardware/step800_r1_0_0_dimension.pdf)

### System {#system}

![file](https://ponoor.com/cms/wp-content/uploads/2021/09/image-1648468983329.png)

Schematics: [step800_r1_0_0_schematics.pdf](https://github.com/ponoor/STEP800/blob/main/hardware/step800_r1_0_0_schematics.pdf)

The main components are as follows.

| Components | Manufacturer | Model number |
| --- | --- | --- |
| MCU | Microchip | [ATSAMD21G18A](https://www.microchip.com/wwwproducts/en/ATsamd21g18) |
| Ethernet Controller | Wiznet | [W5500](https://www.wiznet.io/product-item/w5500/) |
| Stepper Driver | STMicroelectronics | [L6470](https://www.st.com/en/motor-drivers/L6470.html) |
| DC-DC Converter | CUI | [P78E05-1000](https://www.jp.cui.com/product/dc-dc-converters/non-isolated/p78e-1000-series) |

### Pin assignments {#pins}

| pin | function | etc |
| --- | --- | --- |
| D0 | Shift Register SCK |  |
| D1 | NC | Pad on the rear side |
| D2 | Shift Register MOSI |  |
| D3 | Shift Register MISO |  |
| D4 | SD_CS |  |
| D5 | Shift Register ENABLE |  |
| D6 | L6470 MISO |  |
| D7 | NC | Pad on the rear side |
| D8 | NC | Pad on the rear side |
| D9 | NC | Pad on the rear side |
| D10 | W5500_CS |  |
| D11 | L6470 MOSI |  |
| D12 | L6470 SCK |  |
| D13 | L |  |
| D20/SDA | NC | Pad on the rear side |
| D21/SCL | NC | Pad on the rear side |
| D22/MISO | W5500_MISO |  |
| D23/MOSI | W5500_MOSI |  |
| D24/SCK | W5500_SCK |  |
| D30 | NC |  |
| D31 | NC |  |
| D38 | NC | Pad on the rear side |
| A0 | L6470_CS |  |
| A1 | NC | Pad on the rear side |
| A2 | L6470_RESET |  |
| A3 | W5500_RESET |  |
| A4 | SD_DETECT |  |
| A5 | Shift Register CS |  |
| D22/MISO | MISO | - | SERCOM4.0 |
| D23/MOSI | MOSI | - | SERCOM4.2 |
| D24/SCK | SCK | - | SERCOM4.3 |
| D6 | MISO | - | SERCOM3.2 |
| D11 | MOSI | - | SERCOM3.0 |
| D12 | SCK | - | SERCOM3.3 |
| D3 | MISO | - | SERCOM2.1 |
| D2 | MOSI | SERCOM2.2 | - |
| D0 | SCK | - | SERCOM2.3 |

L6470_RESET and W5500_RESET are connected to the reset pins of the L6470 and the W5500 separately. Set the pin mode to OUTPUT and then set the state to HIGH.

### Pads on the rear side {#rear-pads}

There are pads for unassigned pins and for the power on the rear side of the board. The pitch is 2.54 mm, so you can attach surface-mount pin headers or sockets. R6 and R7 on the rear side can be used as pull-up resistors for the I2C pins (SDA, SCL). The size of the chips is 1608 (0603).

The firmware does nothing with these pins. To use them, you need to add to or change the firmware.

![](https://ponoor.com/cms/wp-content/uploads/2021/09/step800_reserved_pads.jpg)

## Brake output (J2) {#brake-output}

The output for the electromagnetic brakes is the connector J2, a 10-pin (2 x 5) box header. The pins are numbered as on a standard box header: seen from above with the key (the notch) at the bottom, the lower row is 1, 3, 5, 7, 9 and the upper row is 2, 4, 6, 8, 10, from the left. The outputs 1 to 8 are the outputs QA to QH of the shift register.

| Pin | Signal |
| --- | --- |
| 1 to 8 | The brake of motor 1 to motor 8 |
| 9 | 3.3V |
| 10 | GND |

The outputs are the digital outputs of a shift register (74HC595), a 3.3 V logic signal. **HIGH releases the brake and LOW engages it.** The state of the shift register is not defined at power-on, so all the outputs can be on the releasing side until the firmware starts (for the time, see [When the load is not held](../guides/electromagnetic-brake.md#unsupported)). For the wiring and for what to do at power-on, see [Electromagnetic brake wiring](../connections/electromagnetic-brake-wiring.md).

## SPI assignment {#spi}

The STEP800 uses different SPI ports for the L6470, the W5500 and the shift registers to make the firmware simple. Here is a very informative guide to the SPI allocation in the ATSAMD21: <https://learn.adafruit.com/using-atsamd21-sercom-to-add-more-spi-i2c-serial-ports>

### W5500 {#spi-w5500}

| Pin | Function | SERCOM | SERCOM Alt |
| --- | --- | --- | --- |
| D22/MISO | MISO | - | SERCOM4.0 |
| D23/MOSI | MOSI | - | SERCOM4.2 |
| D24/SCK | SCK | - | SERCOM4.3 |

### L6470 {#spi-l6470}

| Pin | Function | SERCOM | SERCOM Alt |
| --- | --- | --- | --- |
| D6 | MISO | - | SERCOM3.2 |
| D11 | MOSI | - | SERCOM3.0 |
| D12 | SCK | - | SERCOM3.3 |

### Shift registers (DIP switch, brake output) {#spi-shift-register}

| Pin | Function | SERCOM | SERCOM Alt |
| --- | --- | --- | --- |
| D3 | MISO | - | SERCOM2.1 |
| D2 | MOSI | SERCOM2.2 | - |
| D0 | SCK | - | SERCOM2.3 |

## L6470 {#l6470}

### Clock {#clock}

A 16 MHz crystal oscillator is connected to OSCIN of the L6470 of motor ID 1. From there, OSCOUT and OSCIN are daisy-chained in the order of the IDs, so set each L6470 to "external 16 MHz input, inverted output" (`EXT_16MHZ_OSCOUT_INVERT`). The firmware does this. If the internal clock is used, the movement can shift gradually, for example during a constant speed operation.

### Features that the hardware does not support {#unavailable}

#### STCK {#stck}

STCK is not wired, so the step clock operation is not possible.

#### ADCIN {#adcin}

ADCIN is wired directly to GND and cannot be used.
