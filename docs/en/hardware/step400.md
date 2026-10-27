---
title: STEP400
---

# STEP400

The hardware of the STEP400: the board, its main components, the pin assignment, and the connectors that are not described elsewhere.

## Hardware overview {#overview}

### PCB size {#size}

120 x 84 mm, thickness 1.6 mm.

There are five M3 mounting holes: one at each corner and one near the middle.

![](https://ponoor.com/cms/wp-content/uploads/2020/08/step400-dimension-800x661.png)  
The long parts at the top and the bottom of this picture are waste boards, and are removed after the production.

Actual size PDF: [step400_r1_dimension.pdf](https://github.com/ponoor/STEP400/blob/master/hardware/step400_r1_dimension.pdf)

### System {#system}

![diagram](https://ponoor.com/cms/wp-content/uploads/2020/08/image-1648386258465.png)

Schematics: [step400_r1_schematics.pdf](https://github.com/ponoor/STEP400/blob/master/hardware/step400_r1_schematics.pdf)

The main components are as follows.

| Components | Manufacturer | Model number |
| --- | --- | --- |
| MCU | Microchip | [ATSAMD21G18A](https://www.microchip.com/wwwproducts/en/ATsamd21g18) |
| Ethernet Controller | Wiznet | [W5500](https://www.wiznet.io/product-item/w5500/) |
| Stepper Driver | STMicroelectronics | [PowerSTEP01](https://www.st.com/en/motor-drivers/powerstep01.html) |
| DC-DC Converter | ROHM | [BD9G341AEFJ](https://www.rohm.com/products/power-management/switching-regulators/integrated-fet/buck-converters-nonsynchronous/bd9g341aefj-product) |

### Pin assignments {#pins}

| pin | function | etc |
| --- | --- | --- |
| D0 | DIPSW8 |  |
| D1 | Brake4 |  |
| D2 | DIPSW5 |  |
| D3 | DIPSW7 |  |
| D4 | SD_CS |  |
| D5 | Brake3 |  |
| D6 | PowerSTEP01_MISO |  |
| D7 | DIPSW1 |  |
| D8 | Brake2 |  |
| D9 | DIPSW6 |  |
| D10 | W5500_CS |  |
| D11 | PowerSTEP01_MOSI |  |
| D12 | PowerSTEP01_SCK |  |
| D13 | L |  |
| D20/SDA | NC | Pad on the rear side |
| D21/SCL | NC | Pad on the rear side |
| D22/MISO | W5500_MISO |  |
| D23/MOSI | W5500_MOSI |  |
| D24/SCK | W5500_SCK |  |
| D30 | DIPSW2 |  |
| D31 | DIPSW4 |  |
| D38 | NC | Pad on the rear side |
| A0 | PowerSTEP01_CS |  |
| A1 | Brake1 |  |
| A2 | PowerSTEP01_RESET |  |
| A3 | W5500_RESET |  |
| A4 | SD_DETECT |  |
| A5 | DIPSW3 |  |
| D22/MISO | MISO | - | SERCOM4.0 |
| D23/MOSI | MOSI | - | SERCOM4.2 |
| D24/SCK | SCK | - | SERCOM4.3 |
| D6 | MISO | - | SERCOM3.2 |
| D11 | MOSI | - | SERCOM3.0 |
| D12 | SCK | - | SERCOM3.3 |

PowerSTEP01_RESET and W5500_RESET are connected to the reset pins of the PowerSTEP01 and the W5500 separately. Set the pin mode to OUTPUT and then set the state to HIGH.

### Pads on the rear side {#rear-pads}

There are pads for unassigned pins and for the power on the rear side of the board. The pitch is 2.54 mm, so you can attach surface-mount pin headers or sockets. R35 and R36 on the rear side can be used as pull-up resistors for the I2C pins (SDA, SCL). The size of the chips is 1608 (0603).

The firmware does nothing with these pins. To use them, you need to add to or change the firmware.

![](https://ponoor.com/cms/wp-content/uploads/2020/08/step400-pads-800x533.jpg)

The six pads form the connector J8 of the schematics. With the Ethernet connector at the bottom, the signals from the top are:

| Position from the top | Signal |
| --- | --- |
| 1 | GND |
| 2 | 3.3V |
| 3 | SDA (D20) |
| 4 | SCL (D21) |
| 5 | D38 |
| 6 | 5V |

## Brake output (J7) {#brake-output}

The output for the electromagnetic brakes is the connector J7, a 6-pin (2 x 3) header. The pin numbers are printed on the board. With the board turned so that the printed text can be read, the upper row is 5, 3, 1 from the left, and the lower row is 6, 4, 2 from the left.

| Pin | Signal |
| --- | --- |
| 1 | EM_1 (the brake of motor 1) |
| 2 | EM_2 (motor 2) |
| 3 | EM_3 (motor 3) |
| 4 | EM_4 (motor 4) |
| 5 | 3.3V |
| 6 | GND |

The outputs are pins of the MCU (A1, D8, D5 and D1 for the motors 1 to 4), a 3.3 V logic signal. **HIGH releases the brake and LOW engages it.** Until the firmware has initialized the pins, they are in a high impedance state. For the wiring and for what to do at power-on, see [Electromagnetic brake wiring](../connections/electromagnetic-brake-wiring.md).

## SPI assignment {#spi}

The STEP400 uses different SPI ports for the PowerSTEP01 and the W5500 to make the firmware simple. Here is a very informative guide to the SPI allocation in the ATSAMD21: <https://learn.adafruit.com/using-atsamd21-sercom-to-add-more-spi-i2c-serial-ports>

### W5500 {#spi-w5500}

| Pin | Function | SERCOM | SERCOM Alt |
| --- | --- | --- | --- |
| D22/MISO | MISO | - | SERCOM4.0 |
| D23/MOSI | MOSI | - | SERCOM4.2 |
| D24/SCK | SCK | - | SERCOM4.3 |

### PowerSTEP01 {#spi-powerstep01}

| Pin | Function | SERCOM | SERCOM Alt |
| --- | --- | --- | --- |
| D6 | MISO | - | SERCOM3.2 |
| D11 | MOSI | - | SERCOM3.0 |
| D12 | SCK | - | SERCOM3.3 |

## PowerSTEP01 {#powerstep01}

### Clock {#clock}

A 16 MHz crystal oscillator is connected to OSCIN of the PowerSTEP01 of motor ID 1. From there, OSCOUT and OSCIN are daisy-chained in the order of the IDs, so set each PowerSTEP01 to "external 16 MHz input, inverted output" (`EXT_16MHZ_OSCOUT_INVERT`). The firmware does this. If the internal clock is used, the movement can shift gradually, for example during a constant speed operation.

### Features that the hardware does not support {#unavailable}

#### STCK {#stck}

STCK is not wired, so the step clock operation is not possible.

#### ADCIN {#adcin}

ADCIN is used for the LIMIT inputs, so it cannot be used for its original function, the compensation of the supply voltage. Keep the alarm UVLO_ADC, which is raised from the value of the ADC input, disabled. The firmware does so.

## Known issue: unplugging USB {#usb-unplug}

When the USB cable is pulled out while the Ethernet cable is connected, the STEP400 (R1 board) can restart. This is a hardware problem, and it is the same with firmware v2.1.0. The brakes are engaged before the restart. Pull out the cable only while the motors are stopped. The STEP800 (R1) does not restart. See also [Troubleshooting](../maintenance/troubleshooting.md#usb-unplug).
