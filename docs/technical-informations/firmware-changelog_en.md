---
title: Firmware Changelog
wp_id:
slug: firmware-changelog
lang: en
link: "https://ponoor.com/en/docs/step-series/technical-information/firmware-changelog/"
date: "2026-06-12T00:00:00"
modified: "2026-06-12T00:00:00"
parent: 888
menu_order: 67
---

# Firmware Changelog

This page summarizes the changes in each firmware release. For full details and downloadable binaries, see the [GitHub Releases](https://github.com/ponoor/step-series-universal-firmware/releases) page.

## v2.1.0

[GitHub Release](https://github.com/ponoor/step-series-universal-firmware/releases/tag/v2.1.0)

### New features

- **Browser configuration tool support:** Added serial commands (`G`, `T`, `{...}`, `R`, `F`) to enable the new [browser configuration tool](../connections-and-settings/browser-config-tool_en.md) via Web Serial API.
- **`/saveConfig` command:** Save the running configuration to the microSD card without removing it from the board. See [System Settings](../osc-command-references/system-settings_en.md#saveconfig).
- **`/getConfigName` extended:** The response now includes a 5th argument `configFilename`, the on-disk filename of the configuration file.
- **`/setConfigName` command:** Set the user-editable configuration name label.
- **Long filename support:** Configuration files are no longer limited to 8.3 filenames. Descriptive names like `STEP400_venue-A.json` are now supported.
- **File discovery priority:** The firmware looks for `config.txt` first (backward compatibility), then falls back to the alphabetically first `.json` file on the card.
- **Individual KVAL/TVAL setters:** `/setHoldKval`, `/setRunKval`, `/setAccKval`, `/setDecKval` and their TVAL equivalents (STEP400 only for TVAL).
- **Raw register value commands:** `/setSpeedProfileRaw`, `/getSpeedProfileRaw`, `/setMaxSpeedRaw`, `/setMinSpeedRaw`, `/setFullstepSpeedRaw`, `/setAccRaw`, `/setDecRaw`, `/runRaw`, `/goUntilRaw`, `/combinedRunRaw`.

### Changes

- **SD library:** Changed from `arduino-libraries/SD` to `greiman/SdFat` v2, providing long filename support and improved performance.
- **Arduino IDE folder removed:** The Arduino IDE sketch folder is no longer included in the repository. Download pre-built `.ino` zip files from GitHub Releases.

### Bug fixes

- **`goUntilTimeout` typo fix (STEP400):** The STEP400 configuration template previously contained a typo `goUnitlTimeout` (note the swapped letters). The firmware always read the correctly spelled `goUntilTimeout`, so this value was silently ignored on STEP400 configs, always falling back to the default (10000 ms). This has been corrected.

### Migration notes

- Configuration files from v2.0.0 are compatible. If your STEP400 config contained `goUnitlTimeout`, rename it to `goUntilTimeout` to ensure your timeout value is used.
- The new SdFat library supports long filenames, but `config.txt` remains the default for backward compatibility.

## v2.0.0

[GitHub Release](https://github.com/ponoor/step-series-universal-firmware/releases/tag/v2.0.0)

This release unified the previously separate STEP400 and STEP800 firmware into a single codebase: **STEP-Series Universal Firmware**. Version numbers were reset accordingly.

### Key changes

- **Unified firmware:** A single firmware repository supports STEP100, STEP200, STEP400, and STEP800. The target board is selected at compile time via `boardsDef.h`.
- **PlatformIO support:** PlatformIO is now the primary build system, with all dependencies managed automatically.
- **Configuration versioning:** Configuration files now include a version number, and the firmware validates compatibility at boot.

## Earlier versions

Detailed changelogs were not maintained for firmware versions before v2.0.0. The STEP400 and STEP800 firmware were managed in separate repositories during this period.

For historical firmware files, check the archived repositories:
- [ponoor/STEP400](https://github.com/ponoor/STEP400) (archived)
- [ponoor/STEP800](https://github.com/ponoor/STEP800) (archived)
