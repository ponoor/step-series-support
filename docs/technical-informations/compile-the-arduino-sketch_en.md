---
title: Compiling the Firmware
wp_id: 892
slug: compile-the-arduino-sketch
lang: en
link: "https://ponoor.com/en/docs/step-series/technical-information/compile-the-arduino-sketch/"
date: "2020-08-21T14:14:19"
modified: "2022-08-05T21:38:36"
parent: 888
menu_order: 58
---

# Compiling the Firmware

## Overview

Because the main control unit (MCU) is an [Arduino Zero](https://www.arduino.cc/en/Main/ArduinoBoardZero&), the firmware is built as an Arduino-compatible project. The recommended build method is PlatformIO; the Arduino IDE is also supported.

The latest firmware version and pre-built binaries can be found on the [GitHub Releases](https://github.com/ponoor/step-series-universal-firmware/releases) page. The source code is in the [GitHub repository](https://github.com/ponoor/step-series-universal-firmware).

## Compiling with PlatformIO (recommended)

The firmware is primarily developed using [PlatformIO](https://platformio.org/). Open the repository folder using the "Open Project" menu of PlatformIO. All dependencies are automatically installed when you compile the project for the first time.

![file](https://ponoor.com/cms/wp-content/uploads/2020/08/image-1648187813165.png)

This firmware will work for all STEP Series boards, but you need to specify the target board before you compile it. See "Set the compile target" below.

## Compiling with Arduino IDE

Using the Arduino IDE requires more manual setup than PlatformIO. To begin, the Arduino Zero board must be first installed in the IDE using the Board Manager. This [Quickstart Page](https://www.arduino.cc/en/Guide/ArduinoZero) is a great resource for how to do this procedure.

> **Changed in firmware v2.1.0:** The Arduino IDE sketch folder is no longer included in the repository. Download the pre-built `.ino` zip file from [GitHub Releases](https://github.com/ponoor/step-series-universal-firmware/releases) instead.

Next, the following libraries need to be installed. Here's a page describing how to [install libraries](https://www.arduino.cc/en/guide/libraries).

### Installing libraries

Install the following libraries from the library manager in the Arduino IDE. You can find a detailed guide to install libraries [here](https://www.arduino.cc/en/guide/libraries).

- [OSC Library](https://github.com/CNMAT/OSC)
- [ArduinoJSON](https://arduinojson.org/)
- [Adafruit SleepyDog Arduino Library](https://github.com/adafruit/Adafruit_SleepyDog)
- [SdFat](https://github.com/greiman/SdFat) v2
- In case of STEP400/STEP100: [Ponoor PowerSTEP01 Library](https://github.com/ponoor/Ponoor_PowerSTEP01_Library)
- In case of STEP800/STEP200: [Ponoor L6470 Library](https://github.com/ponoor/Ponoor_L6470_Library)

> **Changed in firmware v2.1.0:** The SD library dependency changed from `arduino-libraries/SD` to `greiman/SdFat` v2, which provides long filename support and improved performance.

### Note for the OSC library

There many OSC libraries that may be listed in the Library Manager. This project uses the library made by CNMAT and is listed as **OSC**. Note that the creators are listed as Adrian Freed and Yotam Mann, not CNMAT.

![](http://ponoor.com/manage/wp-content/uploads/2020/09/OSC_library_manager.png)

### Get the firmware

The firmware is available from here;  
<https://github.com/ponoor/step-series-universal-firmware/releases>

See the "Assets" of the latest Release and download `step-series-universal-firmware.zip`. These zip files only contain required files to compile with Arduino IDE.

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643348613641.png)

Open the `.ino` file from Arduino IDE.

### Set the compile target

There is a list of boards at the beginning of `boardsDef.h`. Remove the comment `//` for the target you want to compile for.  
For example, a code for STEP400 will look like this;

```
// Products
#define STEP400_R1
// #define STEP800_R1

// X-Nucleos
// #define STEP100_R1 // X-NUCLEO-IHM03A1, PowerSTEP01 x1
// #define STEP200_R1 // X-NUCLEO-IHM02A1, L6470 x2
```

### Compile and upload

From "Tools" -> "Boards" select "Arduino Zero (Native USB port)" and compile the sketch.

If the process is completed without errors, proceed to uploading. Connect your PC and the Arduino with an USB, then select the serial port from "Tools" -> "Port" then upload it.

## Notes for uploading the firmware

- As a safety precaution, the electromagnetic brake should be disconnected from the board. While uploading the firmware, defaults are sometimes reset which may lead to the load being held by the brake to be dropped.
- Connecting just the USB-C cable is not enough to power the motor driver chips on either board. So, while you can upload the firmware and perform some basic commands on the board, no movement will be possible unless additional power is provided.
- Occasionally, the Arduino Zero may fail to write. In case this happens, try double-clicking the RESET switch and putting the board in bootloader mode. Then try uploading again. In this mode, the sketch will not boot and the LED `L` will begin to fade. You also have to reselect a different serial port.
