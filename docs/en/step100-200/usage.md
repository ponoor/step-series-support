---
title: Usage
---

# Usage

The STEP100 and the STEP200 are used in the same way as the STEP400 and the STEP800. This page explains the differences.

!!! warning "Not tested on real hardware since v2.1.0"
    The firmware v2.2.0 can be built for the STEP100 and the STEP200, but they have not been tested on real hardware since v2.1.0. The procedures in this section follow the source code of the firmware and the earlier documents.

## Usage {#usage}

Read the [Quick start](../getting-started/quickstart.md) and the [OSC reference](../reference/index.md) of the STEP400 and the STEP800. The STEP100 can use the commands of the STEP400, and the STEP200 can use the commands of the STEP800. The example files are used in the same way. The commands of a function that the board does not have are not available (see [the brake](#brake) and [the LIMIT switch](#limit) below).

### Motor ID {#motor-id}

The number of the motors is different, so the range of the motor ID changes as follows.

| Model | Corresponding model | Range of motor ID |
| --- | --- | --- |
| STEP100 | STEP400 | 1, 255 |
| STEP200 | STEP800 | 1-2, 255 |

A motor ID outside the range is answered with `MotorIdNotMatch` ([Messages to the board](../reference/index.md#messages-to-the-board)).

## Start up {#start-up}

The motor power supply of the X-NUCLEO board does not power the Arduino, so the Arduino needs its own power from the DC jack or from USB. If you turn on the motor power after the Arduino, the commands that the Arduino sends at the start do not reach the driver IC, and the initialization fails. On the other hand, if you supply the power to the driver side while the Arduino is off, the pins of the Arduino stay in an undefined state, and something unexpected may happen. The older Ethernet shields based on the W5100 also often fail to reset at the start.

So the sure way to start is:

1. Supply the power to the Arduino.
2. Supply the motor power.
3. Press the reset button of the Arduino or the Ethernet shield to restart all.

On the STEP400 and the STEP800, the Arduino part and the Ethernet part always start when the motor power is supplied.

## microSD card {#microsd}

Many Ethernet shields have a microSD card slot. You can use it for the configuration file, as described in [Configuration with a microSD card](../connections/microsd-card.md). The board reads it only at the start.

The [browser configuration tool](../connections/browser-config-tool.md) lists the STEP100 and the STEP200 as boards that it supports: it takes the product from the board, shows the panel **Current Mode** only for the STEP100, and has no items of the LIMIT switch and the brake for them (the items of the LIMIT switch appear if you enable `HAVE_LIMIT_GPIO`, see below). We have not tried it with a real STEP100 or STEP200. You can also use the configuration file of the corresponding board: the file of the STEP400 for the STEP100, and the file of the STEP800 for the STEP200. The firmware reads it even if the product in the file is different (the USB serial `s` shows that the file and the product do not match). The settings for more motors than the board has, and the settings of the LIMIT switch, are ignored.

These boards have no pin that detects the card, so the firmware always tries to initialize the card at the start. Without a card, the initialization fails and the board starts with the initial values, as the STEP400 and the STEP800 do.

## DIP switch {#dip-switch}

The firmware fixes the ID by the definition of the board in `boardsDef.h`. It is `1`. To use more than one board on a network, change the ID of each board: rewrite the number of `#define ID 1` and build the firmware. How the ID is used is in [Network and the DIP switch](../connections/network-and-dip-switch.md#adding-id).

Alternatively, you can put your own shield on top of the X-NUCLEO board and solder a DIP switch to it. In this case, you need to customize the firmware. For example, if you connect a 4-digit DIP switch to the pins A1, A3, A4 and A5, replace the commented-out line `// #define HAVE_DIP_SW` in the definition of your board in `boardsDef.h` with the following code (the ID is then read from the switch, and `ID` is not used):

```
    #define HAVE_DIP_SW
    #define DIP_SW_DIGITS   4
    const uint8_t dipSwPin[DIP_SW_DIGITS] = { A1, A3, A4, A5 };
```

## HOME switch {#home}

On the STEP400 and the STEP800, the connector of the HOME switch is wired to the SW pin of the driver IC. On the STEP100 and the STEP200, you connect the switch to the SW pin on the X-NUCLEO board in the same way. The pin is pulled up, so the switch or the sensor must connect the pin to GND when it responds. The electrical connection is explained in [Wiring a switch or a sensor](../connections/sensors-and-switches.md#wiring).

### STEP100 (X-NUCLEO-IHM03A1) {#home-step100}

The red test terminal labeled `TP1` of the X-NUCLEO-IHM03A1 is the SW pin. You have to solder the wire directly to this terminal.

![](https://ponoor.com/cms/wp-content/uploads/2022/01/IMG_4317.jpg)

It is inconvenient to attach the cable of the sensor directly here, so it is better to put a connector in between.

### STEP200 (X-NUCLEO-IHM02A1) {#home-step200}

On the IHM02A1, the `J2` connector is the SW pin. The white circle (●) on the board is pin 1 of the circuit diagram.

![](https://ponoor.com/cms/wp-content/uploads/2022/01/IMG_4312.jpg)![](https://ponoor.com/cms/wp-content/uploads/2022/02/image.png)

This is an example of the connection to the SW terminal of the first driver. A jump wire is used instead of a switch to test the function.

![](https://ponoor.com/cms/wp-content/uploads/2022/02/IMG_4321.jpg)

## LIMIT switch {#limit}

The STEP100 and the STEP200 do not define the LIMIT switch pin, but you can use a spare pin of the Arduino as the LIMIT switch. In this case, you need to customize the firmware: edit the definition of your board in `boardsDef.h` (replace the commented-out line `// #define HAVE_LIMIT_GPIO`). With it, the commands of the LIMIT switch are available on the board.

For example, if you add the following definition, the pins `D6` and `D7` work as the LIMIT switch pins. The pin is pulled up, so connect the switch between the pin and GND.

```
    #define HAVE_LIMIT_GPIO
    // In case of STEP100
    const uint8_t limitSwPin[1] = { 6 };
    // In case of STEP200
    const uint8_t limitSwPin[2] = { 6,7 };
```

## Electromagnetic brake {#brake}

The STEP100 and the STEP200 have no output for the electromagnetic brake, and the commands of the brake are not available on them.
