---
title: Compiling the firmware
---

# Compiling the firmware

To update or customize the firmware, you build it in your own environment and upload it to the board. The MCU is an [Arduino Zero](https://www.arduino.cc/en/Main/ArduinoBoardZero&) compatible one, so the firmware is built as an Arduino-compatible project. The recommended way is PlatformIO. The Arduino IDE is also supported.

The source code is in the [GitHub repository](https://github.com/ponoor/step-series-universal-firmware), and the versions are on the [Releases](https://github.com/ponoor/step-series-universal-firmware/releases) page. The releases have no ready-made binary files (`.bin`): you build the firmware and upload it through the USB bootloader. The instructions here follow the README of the repository.

## Compiling with PlatformIO (recommended) {#platformio}

The firmware is developed with [PlatformIO](https://platformio.org/) (the Arduino framework). Clone the repository, or download it as a ZIP and extract it, and open the folder in PlatformIO. The dependencies are installed automatically from `platformio.ini` when you compile for the first time.

![file](https://ponoor.com/cms/wp-content/uploads/2020/08/image-1648187813165.png)

### Selecting the board {#select-board}

With PlatformIO, you select the board by the **environment** of `platformio.ini`: `step400`, `step800`, `step100` or `step200`. (Until v2.1.0, the board was selected by uncommenting a line in `src/boardsDef.h`. This is not used with PlatformIO.)

- Set `default_envs` in `platformio.ini` to your board, and build and upload with the buttons of PlatformIO in VS Code, or with `pio run` and `pio run -t upload`.

  ```ini
  [platformio]
  default_envs = step800
  ```

- Or choose the environment each time: `pio run -e step800 -t upload`, or `env:step800` in the environment selector of the status bar of VS Code.
- Leave every board line in `boardsDef.h` commented out. A board that is defined in both places does not compile.
- The environment `zeroUSB` of the earlier versions is kept, and builds the STEP400.
- With more than one board connected, add the port to the environment, for example `upload_port = /dev/cu.usbmodem1101` under `[env:step800]`.

The libraries for the drivers are taken from the tag ZIPs on GitHub, as `platformio.ini` says. Do not install them from the registry of PlatformIO.

## Compiling with the Arduino IDE {#arduino-ide}

The Arduino IDE needs more manual work than PlatformIO.

1. Install the **Arduino SAMD Boards** core with the Boards Manager of the IDE. See the "Quick Start" of <https://docs.arduino.cc/hardware/zero>.
2. Install the libraries (see below) with the Library Manager. How to install libraries: <https://www.arduino.cc/en/guide/libraries>.
3. Download `step-series-universal-firmware.zip` from the "Assets" of the latest [release](https://github.com/ponoor/step-series-universal-firmware/releases) and extract it. The folder has the sketch; open its `.ino` file in the Arduino IDE.

   ![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643348613641.png)

4. Select the board in `boardsDef.h`: remove the comment `//` of one board at the beginning of the file. For the STEP400 it looks like this. If you do not select any board, the STEP400 (`STEP400_R1`) is used.

   ```c
   // Products
   #define STEP400_R1
   // #define STEP800_R1

   // X-Nucleos
   // #define STEP100_R1 // X-NUCLEO-IHM03A1, PowerSTEP01 x1
   // #define STEP200_R1 // X-NUCLEO-IHM02A1, L6470 x2
   ```

5. From "Tools" -> "Board", select "Arduino Zero (Native USB Port)", and compile the sketch. If there is no error, connect the board and the computer with USB, select the serial port from "Tools" -> "Port", and upload.

### Libraries {#libraries}

Install these libraries with the Library Manager.

| Library | Version | Used for |
| --- | --- | --- |
| [Ponoor PowerSTEP01 Library](https://github.com/ponoor/Ponoor_PowerSTEP01_Library) | 1.2.0 or later | STEP400, STEP100 |
| [Ponoor L6470 Library](https://github.com/ponoor/Ponoor_L6470_Library) | 1.2.0 or later | STEP800, STEP200 |
| [Ethernet](https://github.com/arduino-libraries/Ethernet) | 2.0.2 or later | |
| [SdFat](https://github.com/greiman/SdFat) (Bill Greiman) | 2.2.3 or later | |
| [ArduinoJson](https://arduinojson.org/) | 7.4.1 or later (7.x) | |

The OSC parser and the watchdog are part of the firmware, so the CNMAT OSC library and the Adafruit SleepyDog library are not needed any more.

The version of the driver library must match the version of the firmware:

| Firmware | Ponoor L6470 / PowerSTEP01 Library |
| --- | --- |
| 2.2.0 | 1.2.0 |
| 2.1.0 and earlier | 1.1.x |

## STEP100 and STEP200 {#step100-200}

The firmware can be built for the STEP100 and the STEP200 (the environments `step100` and `step200`), but they have not been tested on real hardware since v2.1.0. See [STEP100 / STEP200](../step100-200/index.md).

## Notes for uploading the firmware {#uploading}

- **Disconnect the electromagnetic brake before you upload.** While the firmware is written, the firmware does not run, and the state of the brake output is not under control; on the STEP800 the outputs can be on the releasing side. A load that the brake holds can fall. See [Electromagnetic brake wiring](../connections/electromagnetic-brake-wiring.md#power-on).
- USB alone does not power the driver ICs. You can upload the firmware and use some basic commands, but the board cannot move a motor and cannot talk to the drivers unless the motor power is on.
- The upload can fail sometimes. In that case, double-click the RESET switch to put the board in the bootloader mode, and try again. In this mode the firmware does not start, and the LED `L` fades slowly. The serial port is different from the one of the normal start, so select the port again.
