## Updating the firmware
The firmware may be updated for bugfixes and adding features.

Please check the current firmware version on the controller first, then if it's older than [the version published on Github](hhttps://github.com/ponoor/step-series-universal-firmware/releases), please update the firmware.

## Checking firmware version burned on to the controller
One method is to check the over the OSC through ethernet. Another method is to check from serial monitor over USB.

### Check over OSC

With `/getVersion` message you can check the current firmware version. For detail, please command reference for [`/getVersion`](https://ponoor.com/en/docs/step-series/osc-command-reference/system-settings/#getversion).

#### Response example
```
/version "STEP800_R1_UNIVERSAL 1.0.1 Mar 24 2022 11:17:29"
```

### Check from USB
Connect STEP400 and your PC with USB cable, send `s` from serial monitor. From the response message, you can obtain the firmware version. See more detail for [Diagnosis via USB serial port](https://ponoor.com/en/docs/step-series/technical-information/diagnosis/) under [Firmware](https://ponoor.com/en/docs/step-series/technical-information/diagnosis/#firmware) section.

#### Response example
```
-------------- Firmware --------------
Firmware name : STEP800_R1_UNIVERSAL
Firmware version : 1.0.1
Compile date : Mar 24 2022, 11:17:29
```

## To check the latest firmware version
Check the latest firmware version from the "[Releases](https://github.com/ponoor/step-series-universal-firmware/releases)" of the Github repository of STEP-Series.

Previously, STEP400 and STEP800 firmware was managed in separate repositories, but as of March 2022, we have moved to a unified "STEP-series Universal Firmware". The version numbers have been reset accordingly, so please follow the procedure below to make sure you have the latest version.

1. Check if `UNIVERSAL` is in the name of the firmware obtained from the controller.
2. If no, the firmware in the controller is old and need to update
3. If yes, compare with the version number of "[Releases](https://github.com/ponoor/step-series-universal-firmware/releases)".


## Updating firmware
If the firmware on the controller is old, please update the firmware. The update can be done by compiling and uploading latest firmware sketch from Arduino IDE. Refer [Compiling Arduino sketch](https://ponoor.com/docs/step-series/technical-information/compile-the-arduino-sketch/) for more detail.