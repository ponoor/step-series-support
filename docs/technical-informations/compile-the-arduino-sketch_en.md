## Compiling Arduino sketch
To update or customize the firmware, you need to compile and upload the STEP-series firmware Arduino sketch. Roughly there are two methods.
- Compiling from PlatformIO
- Compiling from Arduino IDE

### Compiling from PlatformIO
The step-series firmware is developed with [PlatformIO](https://platformio.org/), an extension for Visual Studio Code. Each repository of STEP400/800 has a dedicated directory for a platformIO. You can open this folder from "Open Project" menu of PlatformIO. All dependencies are installed automatically when you compile the project first time.

### Compiling from ArduinoIDE
If you want to compile the project with the original Arduino IDE from [Arduino.cc](https://www.arduino.cc/), following setups are necessary.
- Install Arduino Zero board profile
- Install dependent libraries
- Download sketch

From here, we will go through this steps.

## Installing Arduino Zero profile
The step-series is compatible with [Arduino Zero](https://www.arduino.cc/en/Main/ArduinoBoardZero&). Install "Arduino SAMD Boards (32-bits ARM Cortex-M0+)" from the Arduino IDE's Board Manager. You can refer to the following page for this procedure.

[Getting started with the Arduino Zero](https://www.arduino.cc/en/Guide/ArduinoZero)

## Installing libraries
### Libraries to install
Install the following libraries from the library manager in the Arduino IDE. You can find a detailed guide to install library [here](https://www.arduino.cc/en/guide/libraries).

- [OSC Library](https://github.com/CNMAT/OSC)
- [ArduinoJSON](https://arduinojson.org/)
- [Adafruit SleepyDog Arduino Library](https://github.com/adafruit/Adafruit_SleepyDog)
- STEP400 only : [Ponoor PowerSTEP01 Library](https://github.com/ponoor/Ponoor_PowerSTEP01_Library)
- STEP800 only : [Ponoor L6470 Library](https://github.com/ponoor/Ponoor_L6470_Library)

### Note for the OSC library
There are many libraries to support OSC, but for this project, use the [OSC Library](https://github.com/CNMAT/OSC) from CNMAT.
From the Arduino IDE, goto "Manage Libraries" and install the library named "OSC". Note that the creators are listed as Adrian Freed and Yotam Mann, not as the organization name CNMAT.

![](http://ponoor.com/manage/wp-content/uploads/2020/09/OSC_library_manager.png)

## Compiling the sketch
Clone files from the repository of the corresponding model.

| Model | Arduino Sketch Directory | PlatformIO Directory |
| --- | --- | ---|
| [STEP400](https://github.com/ponoor/STEP400) | [/STEP400_firmware](https://github.com/ponoor/STEP400/tree/master/STEP400_firmware) | [/firmware-platformio/STEP400_firmware](https://github.com/ponoor/STEP400/tree/master/firmware-platformio/STEP400_firmware) |
| [STEP800](https://github.com/ponoor/STEP800) | [/STEP800_firmware](https://github.com/ponoor/STEP800/tree/main/STEP800_firmware) | [/firmware-platformIO/STEP800_firmware](https://github.com/ponoor/STEP800/tree/main/firmware-platformIO/STEP800_firmware) |

 If you are not familiar with git system, you can also download ZIP files from upper right `Code` -> `Download ZIP`.

![file](https://ponoor.com/cms/wp-content/uploads/2020/08/image-1617454087280.png)

Browse the Arduino sketch folder and open the `.ino` file from Arduino IDE. From "Tools" -> "Boards" select "Arduino Zero (Native USB port)" and compile the sketch.

## Notes for uploading the Arduino sketch
- If the electromagnet brake board is connected with STEP400, remove it before uploading the sketch. The EM brake on ch.4 is released on uploading the firmware. It may cause the load to drop. This is due to teh setting of the Arduino Zero's bootloader. In STEP800, this problem won't happen so you can leave it connected.
- If you connect only the USB cable to the board, you can upload the sketch, but the motor driver chips won't boot up. So you can't perform any operations that involve exchanging messages with the drivers.
- It seems to be a quirk of the Arduino Zero that it sometimes fails to write. In that case, try double-clicking the RESET switch and putting it in bootloader mode, and try again. In the bootloader mode, the sketch won't boot and L will fade slowly. Also, you have to re-select a different serial port than normal one.