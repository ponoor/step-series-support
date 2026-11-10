---
title: Upload the Arduino sketch
---

# Upload the Arduino sketch

How to build the firmware for the STEP100 or the STEP200 and write it to the Arduino. The steps that are common to all the products are in [Compiling the firmware](../maintenance/compile-the-arduino-sketch.md); this page has what is specific to the STEP100 and the STEP200.

!!! warning "Not tested on real hardware since v2.1.0"
    The firmware v2.2.0 can be built for the STEP100 and the STEP200, but they have not been tested on real hardware since v2.1.0. The procedures in this section follow the source code of the firmware and the earlier documents.

## Upload with PlatformIO {#platformio}

Get the firmware from <https://github.com/ponoor/step-series-universal-firmware> and open it with PlatformIO, as described in [Compiling with PlatformIO](../maintenance/compile-the-arduino-sketch.md#platformio). The libraries are installed automatically.

### Select the environment {#select-env}

Select the environment `step100` for the STEP100 or `step200` for the STEP200, as described in [Selecting the board](../maintenance/compile-the-arduino-sketch.md#select-board). Leave every board line in `boardsDef.h` commented out.

The environments build for the board `zeroUSB` (Arduino Zero). They need the Ethernet shield and the driver library of the model: the Ponoor PowerSTEP01 Library for the STEP100 and the Ponoor L6470 Library for the STEP200, which `platformio.ini` takes from the tag ZIPs on GitHub.

### Arduino M0 and METRO M0 Express {#m0}

`platformio.ini` of v2.2.0 has no environment for the board definition of the Arduino M0 (`mzeroUSB`) or the METRO M0 Express: they remain in it only as commented-out examples of the earlier versions, which do not work with v2.2.0. Use the environment `step100` or `step200`, that is, build as an Arduino Zero. For the METRO M0 Express this is also what the comment in `platformio.ini` tells, because the USB serial of its own board definition behaves differently and the [USB serial diagnosis](../maintenance/usb-serial-diagnosis.md) does not work well with it.

For the board with the hardware of the Arduino M0 (D2 and D4 are swapped), define `MZERO_WITH_ZERO_BOOTLOADER` ([Arduino Zero or M0?](get-the-materials.md#zero-or-m0)). With it, the CS pin of the microSD card is D2 in the numbering of the Arduino Zero, which is D4 on the M0. In PlatformIO, add it to the build flags of the environment:

```ini
[env:step100]
extends = samd_base
build_flags =
	${samd_base.build_flags}
	-D STEP100_R1
	-D MZERO_WITH_ZERO_BOOTLOADER
```

We built v2.2.0 with this setting for both the `step100` and the `step200`, and confirmed that the CS pin of the microSD card changes (the build succeeds, and `PIN_SD_CS` becomes 2 instead of 4). We have not tried it on real hardware.

## Upload with the Arduino IDE {#arduino-ide}

The steps are in [Compiling with the Arduino IDE](../maintenance/compile-the-arduino-sketch.md#arduino-ide): install the SAMD core, install the libraries, and open the sketch of the latest release (`step-series-universal-firmware.zip`, in the "Assets"). For the STEP100 and the STEP200, note these points.

- **Libraries:** install the [Ponoor PowerSTEP01 Library](https://github.com/ponoor/Ponoor_PowerSTEP01_Library) for the STEP100, and the [Ponoor L6470 Library](https://github.com/ponoor/Ponoor_L6470_Library) for the STEP200, in addition to the common ones. The versions are in [Libraries](../maintenance/compile-the-arduino-sketch.md#libraries).
- **Select the board in `boardsDef.h`:** remove the comment `//` of the model at the beginning of the file. For the STEP100 it looks like this:

  ```
  // Products
  // Arduino IDE: uncomment ONE line to select the board.
  // PlatformIO: pass the board as a build flag instead (e.g. -D STEP800_R1).
  // #define STEP400_R1
  // #define STEP800_R1

  // X-Nucleos
  #define STEP100_R1 // X-NUCLEO-IHM03A1, PowerSTEP01 x1
  // #define STEP200_R1 // X-NUCLEO-IHM02A1, L6470 x2
  ```

- **Arduino M0 hardware:** if D2 and D4 are swapped on your board, remove the comment of this line, too:

  ```
  // #define MZERO_WITH_ZERO_BOOTLOADER
  ```

- **The board:** from "Tools" -> "Board", select "Arduino Zero (Native USB Port)" and compile.

## Uploading {#uploading}

Connect the PC and the Arduino with USB, select the serial port from "Tools" -> "Port", and upload. Read [Notes for uploading the firmware](../maintenance/compile-the-arduino-sketch.md#uploading) first.
