## Compiling Arduino sketch
To update or customize the firmware, you need to compile and upload the STEP-series firmware Arduino sketch. There are two methods.
- Compiling from PlatformIO
- Compiling from Arduino IDE

### Compiling from PlatformIO
The step-series firmware is developed with [PlatformIO](https://platformio.org/). 
You can clone the [repository](https://github.com/ponoor/step-series-universal-firmware), or unzip the file acquired from "Download ZIP" menu. 
You can open this folder from "Open Project" menu of PlatformIO. All dependencies are installed automatically when you compile the project first time.

![file](https://ponoor.com/cms/wp-content/uploads/2020/08/image-1648187813165.png)

This firmware will work for all step-series but you need to specify the target board before you compile it. Please refer to "Set the compile target" below. 

### Compiling from ArduinoIDE
If you want to compile the project with the official Arduino IDE from [Arduino.cc](https://www.arduino.cc/), following setups are necessary.
- Install Arduino Zero board profile
- Install dependent libraries
- Download sketch

From here, we will go through this steps.

#### Installing Arduino Zero profile
The step-series is compatible with [Arduino Zero](https://www.arduino.cc/en/Main/ArduinoBoardZero&). Install "Arduino SAMD Boards (32-bits ARM Cortex-M0+)" from the Arduino IDE's Board Manager. You can refer to the following page for this procedure.

[Getting started with the Arduino Zero](https://www.arduino.cc/en/Guide/ArduinoZero)

#### Installing libraries
Install the following libraries from the library manager in the Arduino IDE. You can find a detailed guide to install library [here](https://www.arduino.cc/en/guide/libraries).

- [OSC Library](https://github.com/CNMAT/OSC)
- [ArduinoJSON](https://arduinojson.org/)
- [Adafruit SleepyDog Arduino Library](https://github.com/adafruit/Adafruit_SleepyDog)
- In case of STEP400/STEP100: [Ponoor PowerSTEP01 Library](https://github.com/ponoor/Ponoor_PowerSTEP01_Library)
- In case of STEP800/STEP200: [Ponoor L6470 Library](https://github.com/ponoor/Ponoor_L6470_Library)

#### Note for the OSC library
There are many libraries to support OSC, but for this project, use the [OSC Library](https://github.com/CNMAT/OSC) from CNMAT.
From the Arduino IDE, goto "Manage Libraries" and install the library named "OSC". Note that the creators are listed as Adrian Freed and Yotam Mann, not as the organization name CNMAT.

![](http://ponoor.com/manage/wp-content/uploads/2020/09/OSC_library_manager.png)

#### Get the firmware
The Arduino sketch is available from here;
https://github.com/ponoor/step-series-universal-firmware/releases

See the "Assets" of the latest Release and download `step-series-universal-firmware.zip`. These zip files only contain required files to compile with Arduino IDE.

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643348613641.png)

Open the `.ino` file from Arduino IDE. 

#### Set the compile target
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

#### Compile and upload
From "Tools" -> "Boards" select "Arduino Zero (Native USB port)" and compile the sketch.

If the process is completed without errors, proceed to uploading. Connect your PC and the Arduino with an USB, then select the serial port from "Tools" -> "Port" then upload it.

## Notes for uploading the Arduino sketch
- If the electromagnet brake board is connected with STEP400, remove it before uploading the sketch. The EM brake on ch.4 is released on uploading the firmware. It may cause the load to drop. This is due to teh setting of the Arduino Zero's bootloader. In STEP800, this problem won't happen so you can leave it connected.
- If you connect only the USB cable to the board, you can upload the sketch, but the motor driver chips won't boot up. So you can't perform any operations that involve exchanging messages with the drivers.
- It seems to be a quirk of the Arduino Zero that it sometimes fails to write. In that case, try double-clicking the RESET switch and putting it in bootloader mode, and try again. In the bootloader mode, the sketch won't boot and L will fade slowly. Also, you have to re-select a different serial port than normal one.