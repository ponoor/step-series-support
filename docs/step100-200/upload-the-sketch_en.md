---
title: Upload the Arduino sketch
wp_id: 2307
slug: upload-the-sketch
lang: en
link: "https://ponoor.com/en/docs/step100-200/upload-the-sketch/"
date: "2022-01-28T16:18:29"
modified: "2022-03-29T10:46:29"
parent: 2284
menu_order: 25
---

# Upload the Arduino sketch

## Upload with PlatformIO

### Get the firmware

<https://github.com/ponoor/step-series-universal-firmware>

Since this firmware is developed with PlatformIO, you can clone the above repository and open it with PlatformIO to download the necessary libraries, compile, and upload the firmware.  
This firmware is compatible with all STEP series, but you need to specify the target model before compiling. Please refer to "[Set the compile target](https://ponoor.com/en/docs/step100-200/upload-the-sketch/#set_the_compile_target)" below.

### Select env

`platformio.ini` contains settings for two environments, Arudino Zero (`zeroUSB`) and Arduino M0 (`mzeroUSB`). You can leave out whichever one you need and comment out the one you don't need with `;`.

```
[env:zeroUSB]
platform = atmelsam
board = zeroUSB
framework = arduino
lib_deps = 
    arduino-libraries/Ethernet@^2.0.0
    arduino-libraries/SD@^1.2.4
    cnmat/OSC@0.0.0-alpha+sha.41b44981e3
    adafruit/Adafruit SleepyDog Library@^1.4.0
    bblanchon/ArduinoJson@^6.18.4
    https://github.com/ponoor/Ponoor_L6470_Library/archive/refs/tags/v1.0.3.zip
    ponoor/Ponoor PowerSTEP01 Library@^1.0.2

[env:mzeroUSB]
platform = atmelsam
board = mzeroUSB
framework = arduino
lib_deps = 
    arduino-libraries/Ethernet@^2.0.0
    arduino-libraries/SD@^1.2.4
    cnmat/OSC@0.0.0-alpha+sha.41b44981e3
    adafruit/Adafruit SleepyDog Library@^1.4.0
    bblanchon/ArduinoJson@^6.18.4
    https://github.com/ponoor/Ponoor_L6470_Library/archive/refs/tags/v1.0.3.zip
    ponoor/Ponoor PowerSTEP01 Library@^1.0.2
```

#### In case of Adaruit METRO M0 Express

Please compile and upload the code as Arduino Zero (`[env:zeroUSB]`) . There is a dedicated board definition but it won't work well for the USB diagnosis tool, since the behavior of the USB serial is different.

## Upload with Arduino IDE

If you want to compile and upload with Arduino IDE instead of PlatformIO, the following steps are required

1. Install the SAMD core to compile for Arduino Zero/M0
2. Install the necessary libraries
3. Get and open the sketch

### Install the SAMD core

Install "Arduino SAMD Boards (32-bits ARM Cortex-M0+)" from Boards Manager of Arduino IDE. You can find the explanation of this procedure at the "Quick Start" of [the Arduino Zero documentation](https://docs.arduino.cc/hardware/zero).

### Install the necessary libraries

Install the following libraries from the library manager in the Arduino IDE. You can find a detailed guide to install library [here](https://www.arduino.cc/en/guide/libraries).

- [OSC Library](https://github.com/CNMAT/OSC)
- [ArduinoJSON](https://arduinojson.org/)
- [Adafruit SleepyDog Arduino Library](https://github.com/adafruit/Adafruit_SleepyDog)
- STEP100 Only: [Ponoor PowerSTEP01 Library](https://github.com/ponoor/Ponoor_PowerSTEP01_Library)
- STEP200 Only: [Ponoor L6470 Library](https://github.com/ponoor/Ponoor_L6470_Library)

### Get the Arduino sketch

You can find the Arduino sketch here.

<https://github.com/ponoor/step-series-universal-firmware/releases>

Find a latest release and click the "Asset" of it. Then download and unzip `step-series-universal-firmware.zip`.

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643348613641.png)

Open the `.ino` file from Arduino IDE.

### Set the compile target

There is a list of boards at the beginning of `boardsDef.h`. Remove the comment `//` for the target you want to compile for.  
For example, a code for STEP100 will look like this;

```
// Products
// #define STEP400_R1
// #define STEP800_R1

// Prototypes
// #define STEP400_PROTO_R4
// #define STEP800_PROTO_R3
// #define STEP800_PROTO_R1

// X-Nucleos
#define STEP100_R1 // X-NUCLEO-IHM03A1, PowerSTEP01 x1
// #define STEP200_R1 // X-NUCLEO-IHM02A1, L6470 x2
```

If you are using an Arduino M0 board with Arduino Zero bootloader, delete the first comment out of this line.

```
// #define MZERO_WITH_ZERO_BOOTLOADER
```

### Compile and Upload

From "Tools" -> "Boards" select "Arduino Zero (Native USB port)" and compile the sketch.

If the process is completed without errors, proceed to uploading. Connect your PC and the Arduino with an USB, then select the serial port from "Tools" -> "Port" then upload it.

Please refer to [Compiling the Arduino sketch](https://ponoor.com/en/docs/step-series/technical-information/compile-the-arduino-sketch/) in STEP400/800 documentation for this process.
