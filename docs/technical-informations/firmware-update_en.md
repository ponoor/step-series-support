## Updating the firmware
The firmware may be updated for bugfixes and adding features.

Please check the current firmware version on the controller first, then if it's older than [the version published on Github](https://github.com/ponoor/STEP400/releases), please update the firmware.

## Checking firmware version burned on to the controller
One method is to check the over the OSC through ethernet. Another method is to check from serial monitor over USB.

### Check over OSC

With `/getVersion` message you can check the current firmware version. For detail, please command reference for [`/getVersion`](https://ponoor.com/en/docs/step-series/osc-command-reference/system-settings/#getversion).

### Check from USB
Connect STEP400 and your PC with USB cable, send `s` from serial monitor. From the response message, you can obtain the firmware version. See more detail for [Diagnosis via USB serial port](https://ponoor.com/en/docs/step-series/technical-information/diagnosis/) under [Firmware](https://ponoor.com/en/docs/step-series/technical-information/diagnosis/#firmware) section.

## To check the latest firmware version
Check the latest firmware version from the Github repository of STEP400.
[https://github.com/ponoor/STEP400/releases](https://github.com/ponoor/STEP400/releases)

## Updating firmware
If the firmware on the controller is old. Please update the firmware. The update can be done by compiling and uploading latest firmware sketch from Arduino IDE. Refer [Compiling Arduino sketch](https://ponoor.com/docs/step-series/technical-information/compile-the-arduino-sketch/) for more detail.