---
title: Example parameter values for example steppers
---

# Example parameter values for example steppers

We publish the parameters that we worked out from the datasheets and our measurements for the motors that we have in our lab, as configuration files. You can copy a file to the microSD card, or open it in the [browser configuration tool](browser-config-tool.md) and adjust it.

The files are here: <https://github.com/ponoor/step-series-support/tree/main/configGenerator>

## The parameters that are set {#parameters}

### Configuration name and file name {#names}

The configuration name in a file is `<model>_<voltage>`, for example `17HS08-1004S_24V`. The file is named `<board>_<model>_<voltage>.json`, for example `STEP400_17HS08-1004S_24V.json`, so that the files can be told apart in the repository.

### Voltage mode {#voltage-mode}

- The KVAL values (KVAL_HOLD is half of KVAL_RUN).
- The BEMF compensation parameters. For how to work them out, see [Voltage mode setting](../guides/voltage-and-current-mode.md#voltage-mode-setting).

The values depend on the supply voltage of the motor. A set of values that suits one voltage can be too strong at another one; see [KVAL and TVAL](../guides/voltage-and-current-mode.md#kval-tval).

### Current mode {#current-mode}

- The TVAL values (TVAL_HOLD is half of TVAL_RUN). Only the files for the STEP400 have them.

### Speed profile {#speed-profile}

The maximum speed and the acceleration and deceleration of a motor depend greatly on the weight of the load, its shape and how it is mounted. So these values are left at the initial values. Set them with [`/setSpeedProfile`](../reference/speed-profile.md#setspeedprofile) and other commands while you move your load.

## Using the files {#using}

Copy the file as it is to the root folder of the microSD card. The board reads the first `.json` file in the root folder in alphabetical order. You do not need to rename the file, but `config.txt` or another `.json` file may be read first, so put only the file that you use on the card. (Firmware before v2.1.0 reads only a file named `config.txt`.) See [The file that the board reads](microsd-card.md#files) for the rules.
