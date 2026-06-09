---
title: Get the materials
wp_id: 2289
slug: get-the-materials
lang: en
link: "https://ponoor.com/en/docs/step100-200/get-the-materials/"
date: "2022-02-02T21:41:09"
modified: "2022-03-29T10:50:10"
parent: 2284
menu_order: 5
---

# Get the materials

## Arduino Zero or M0

![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342497869.png)![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342518306.png)

Currently, STEP100/200 firmware is compatible with:

- Arduino Zero.
- Arduino M0
- [Adafruit METRO M0 Express](https://www.adafruit.com/product/3505)

Arduino Zero/M0 are out of stock at the [official site](https://store-usa.arduino.cc/collections/boards/products/arduino-zero) but you can find [compatible products](https://www.aliexpress.com/item/4000544537659.html) at online shops like Ali Express.

### Arduino Zero or M0?

These two models have been separated into different models due to the time when Arduino was divided into two, but they are almost identical and can be used with either. However, there are some differences, so you need to select the corresponding model name when compiling and uploading the sketch.

In terms of hardware, the D2 and D4 pins are swapped between the two models. Confusingly, some compatible products may have the Arduino Zero bootloader written into the Arduino M0 equivalent hardware. Even if the board is recognized as an Arduino Zero, it is safer to actually upload a sketch to blink D2 to see if D2 or D4 flashes.

If you met these kind of boards, delete the comment out `//` in the following line near line 32 of `boardsDef.h` and compile it when you upload the firmware.

```
// #define MZERO_WITH_ZERO_BOOTLOADER
```

### Another Arduino models

The SPI pins of the X-Nucleo series used in STEP100/200 don't communicate with SPI connectors, but D11, D12, and D13. In Arduino Zero/M0, SPI functions are assigned to these pins. These pins are also used as SPI pins in the Arduino UNO, so it can control X-Nucleos, but UNO cannot run the STEP series firmware because of its small RAM and Flash size.

In Leonardo and MEGA, SPI functions are not assigned to D11-D13, so they cannot be used.

## Ethernet Shield

![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342683554.png)![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643702336632.png)

The firmware has been tested with [Arduino Ethernet Shield2](https://docs.arduino.cc/hardware/ethernet-shield-rev2) based on Wiznet W5500. This one is also out of stock at the official store, but is available at major distributors ([Mouser](https://www.mouser.jp/ProductDetail/Arduino/A000024?qs=sGAEpiMZZMvfWfew95%2FxXPtlEf46RordNAHqnNtyb4k%3D), [Digikey](https://www.digikey.jp/ja/products/detail/arduino/A000024/3476356), [RS](https://jp.rs-online.com/web/p/shields-for-arduino/8732285?sra=pmpn) etc.). There are also many compatible products of older Ethernet shield based on W5100 in Ali Express, but they didn't work for STEP100(X-NUCLEO-IHM03A1). Worked for STEP200(X-NUCLEO-IHM02A1).

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643702118944.png)

These types won't work because you cannot put more shields on top of them.  
Arduino and Ethernet shield are communicate via the 6 pins SPI connector, but it doesn't exist on X-Nucleos. Therefore, you should always put the Ethernet shield on top of the Arduino, and then put the X-Nucleo series on top of them.

## X-NUCLEO Series

![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342852324.png)![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342863866.png)

These are evaluation boards released form STMicroelectronics. Available from major distributors as well.

| Model | X-Nucleo | Driver | Mouser | Digikey | RS | Chip1stop |
| --- | --- | --- | --- | --- | --- | --- |
| STEP100 | [X-NUCLEO-IHM03A1](https://www.st.com/en/ecosystems/x-nucleo-ihm03a1.html) | PowerSTEP01 | [link](https://www.mouser.jp/ProductDetail/STMicroelectronics/X-NUCLEO-IHM03A1?qs=ILgNtqsyH21VjhjjaAqaGQ%3D%3D) | [link](https://www.digikey.jp/ja/products/detail/stmicroelectronics/X-NUCLEO-IHM03A1/5325495?s=N4IgTCBcDaIJYAsC2AGAzAQwIwgLoF8g) | [link](https://jp.rs-online.com/web/p/power-motor-robotics-development-tools/9064656) | [link](https://www.chip1stop.com/view/dispDetail/DispDetail?lang=en&cont=USA&partId=STMI-0106873&mpn=X-NUCLEO-IHM03A1&keyword=X-NUCLEO-IHM03A1) |
| STEP200 | [X-NUCLEO-IHM02A1](https://www.st.com/en/ecosystems/x-nucleo-ihm02a1.html) | L6470 | [link](https://www.mouser.jp/ProductDetail/STMicroelectronics/X-NUCLEO-IHM02A1?qs=468p3M0KQ1q0beHvLX%2FUnA%3D%3D) | [link](https://www.digikey.jp/ja/products/detail/stmicroelectronics/X-NUCLEO-IHM02A1/5768392?s=N4IgTCBcDaIJYAsC2AGMBDAjCAugXyA) | [link](https://jp.rs-online.com/web/p/power-motor-robotics-development-tools/1646982?sra=pmpn) | [link](https://www.chip1stop.com/view/dispDetail/DispDetail?lang=en&cont=USA&partId=STMI-0102961&mpn=X-NUCLEO-IHM02A1&keyword=ihm02a1) |

## Power Supply

According datasheets of the X-Nucleo, the voltages of motor power supply are;

- IHM03A1(PowerSTEP01): 10.5V-50V
- IHM02A1(L6470): 8V-45V

In the meantime, it would be a good idea to prepare a power supply of about 24V 4-5A for both and start experimenting. Please refer to the selection of [power supply and motor](https://ponoor.com/en/docs/step-series/settings/power-supply-and-motor/).

The X-Nucleo has a screw terminal, so a DC jack cable is useful if you want to supply the power with an AC adapter.  
![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643347656810.png)

The motor power supply does not supply power to the Arduino, so you need a power supply for the Arduino as well, which can be supplied from a PC or USB charger via USB.
