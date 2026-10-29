---
title: Get the materials
---

# Get the materials

The STEP100 and the STEP200 are made of an Arduino Zero (or a compatible board), an Ethernet shield and an X-NUCLEO board. This page lists what to get.

## Arduino Zero or M0 {#arduino}

![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342497869.png)![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342518306.png)

The firmware is compatible with:

- Arduino Zero
- Arduino M0
- [Adafruit METRO M0 Express](https://www.adafruit.com/product/3505)

The Arduino Zero and the Arduino M0 are out of stock at the [official site](https://store-usa.arduino.cc/collections/boards/products/arduino-zero), but you can find the [M0 at Akizuki Denshi](https://akizukidenshi.com/catalog/g/gM-09079/) and [compatible products](https://www.aliexpress.com/item/4000544537659.html) at online shops like AliExpress.

### Arduino Zero or M0? {#zero-or-m0}

These two models were separated when Arduino was divided into two companies, but they are almost identical and either can be used. There are some differences, however, and you must take them into account when you build and upload the firmware (see [Upload the Arduino sketch](upload-the-sketch.md#m0)).

In terms of hardware, the D2 and D4 pins are swapped between the two models. Confusingly, some compatible products have the Arduino Zero bootloader written on Arduino M0 equivalent hardware. Even if the board is recognized as an Arduino Zero, it is safer to upload a sketch that blinks D2 and see whether D2 or D4 blinks.

If D2 and D4 are swapped on a board that is recognized as an Arduino Zero, define `MZERO_WITH_ZERO_BOOTLOADER` when you build the firmware. It is in `boardsDef.h`:

```
// #define MZERO_WITH_ZERO_BOOTLOADER
```

### Other Arduino models {#other-arduinos}

The SPI pins of the X-NUCLEO boards are not on the SPI connector, but on D11, D12 and D13. The Arduino Zero and M0 have the SPI function on these pins. The Arduino UNO also uses them as the SPI pins, so it could control the X-NUCLEO boards, but it cannot run the firmware of the STEP Series because its RAM and flash memory are small.

The Leonardo and the MEGA do not have the SPI function on D11-D13, so they cannot be used.

## Ethernet shield {#ethernet-shield}

![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342683554.png)![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643702336632.png)

The firmware has been tested with the [Arduino Ethernet Shield 2](https://docs.arduino.cc/hardware/ethernet-shield-rev2), which is based on the Wiznet W5500. It is also out of stock at the official store, but major distributors carry it ([Mouser](https://www.mouser.jp/ProductDetail/Arduino/A000024?qs=sGAEpiMZZMvfWfew95%2FxXPtlEf46RordNAHqnNtyb4k%3D), [Digikey](https://www.digikey.jp/ja/products/detail/arduino/A000024/3476356), [RS](https://jp.rs-online.com/web/p/shields-for-arduino/8732285?sra=pmpn) and others).

There are also many compatible products of the older shield based on the W5100 at AliExpress. In our test they did not work for the STEP100 (X-NUCLEO-IHM03A1). They worked for the STEP200 (X-NUCLEO-IHM02A1).

The [Ethernet Shield for Arduino v2.2](https://akizukidenshi.com/catalog/g/gM-13165/) of Akizuki Denshi should work if you change the pin assignment in `boardsDef.h`, but we have not checked it on real hardware.

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643702118944.png)

A shield of this type cannot be used because you cannot put more shields on top of it. The Arduino and the Ethernet shield communicate through the 6-pin SPI connector, which the X-NUCLEO boards do not have. So you must always put the Ethernet shield on the Arduino, and then put the X-NUCLEO board on top of them.

## X-NUCLEO board {#x-nucleo}

![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342852324.png)![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342863866.png)

These are evaluation boards of STMicroelectronics. Major distributors carry them too.

| Model | X-NUCLEO | Driver IC | Mouser | Digikey | RS | Chip1stop |
| --- | --- | --- | --- | --- | --- | --- |
| STEP100 | [X-NUCLEO-IHM03A1](https://www.st.com/en/ecosystems/x-nucleo-ihm03a1.html) | PowerSTEP01 | [link](https://www.mouser.jp/ProductDetail/STMicroelectronics/X-NUCLEO-IHM03A1?qs=ILgNtqsyH21VjhjjaAqaGQ%3D%3D) | [link](https://www.digikey.jp/ja/products/detail/stmicroelectronics/X-NUCLEO-IHM03A1/5325495?s=N4IgTCBcDaIJYAsC2AGAzAQwIwgLoF8g) | [link](https://jp.rs-online.com/web/p/power-motor-robotics-development-tools/9064656) | [link](https://www.chip1stop.com/view/dispDetail/DispDetail?lang=en&cont=USA&partId=STMI-0106873&mpn=X-NUCLEO-IHM03A1&keyword=X-NUCLEO-IHM03A1) |
| STEP200 | [X-NUCLEO-IHM02A1](https://www.st.com/en/ecosystems/x-nucleo-ihm02a1.html) | L6470 | [link](https://www.mouser.jp/ProductDetail/STMicroelectronics/X-NUCLEO-IHM02A1?qs=468p3M0KQ1q0beHvLX%2FUnA%3D%3D) | [link](https://www.digikey.jp/ja/products/detail/stmicroelectronics/X-NUCLEO-IHM02A1/5768392?s=N4IgTCBcDaIJYAsC2AGMBDAjCAugXyA) | [link](https://jp.rs-online.com/web/p/power-motor-robotics-development-tools/1646982?sra=pmpn) | [link](https://www.chip1stop.com/view/dispDetail/DispDetail?lang=en&cont=USA&partId=STMI-0102961&mpn=X-NUCLEO-IHM02A1&keyword=ihm02a1) |

## Power supply {#power-supply}

According to the datasheets of the X-NUCLEO boards, the voltage of the motor power supply is:

- IHM03A1 (PowerSTEP01): 10.5 V to 50 V
- IHM02A1 (L6470): 8 V to 45 V

To start experimenting, prepare a power supply of about 24 V and 4 to 5 A for both. For how to choose a power supply and a motor, see [Power supply and motor](../connections/power-supply-and-motor.md#ratings).

The X-NUCLEO board has a screw terminal, so a cable with a DC jack is useful when you supply the power with an AC adapter.

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643347656810.png)

The motor power supply does not power the Arduino, so the Arduino needs its own power. You can supply it from a PC or a USB charger through USB.
