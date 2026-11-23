---
title: Firmware changelog
---

# Firmware changelog

This page summarizes what changed in each version of the firmware, from the point of view of the people who write OSC clients, make configuration files, use the board, or build the firmware. The full text is in the [CHANGELOG](https://github.com/ponoor/step-series-universal-firmware/blob/main/CHANGELOG.md) of the repository, and each version has a [Release](https://github.com/ponoor/step-series-universal-firmware/releases) on GitHub. The releases carry the source of the Arduino sketch only; there are no ready-made binary files, so you build the firmware yourself ([Compiling the firmware](compile-the-arduino-sketch.md)).

## v2.2.0 {#v2-2-0}

Released 2026-10-20. The OSC addresses are compatible with v2.1.0, but the behavior of many commands changed and some commands now reply with an error. **If you update from v2.1.0, read the [Migration guide](migration-guide.md) first.** The firmware needs the driver libraries v1.2.0 (see [Build and libraries](#v2-2-0-build)).

### Behavior changes {#v2-2-0-behavior}

#### Argument checks and errors {#v2-2-0-arguments}

- **Arguments are checked before a command is applied** (all commands). Too few arguments reply `/error/osc MissingArgument`, and an argument of the wrong type (a string for a number, NaN or infinity, `/setConfigName` with a non-string) replies `/error/osc WrongDataType`; nothing is applied either way. Before, the missing or wrong arguments were applied as 0 (`/setKval 1` set every KVAL of the motor to 0). Extra arguments are still ignored. A motor ID outside 0-255 replies `MotorIdNotMatch` with the value sent. See [Errors](../guides/communication-and-messages.md#errors) and [`/error/osc`](../reference/automatically-sent-messages.md#error-osc).
- **A value outside the range of a command is rejected** with `/error/command CommandIgnored`, and nothing is applied: [`/setPositionReportInterval`](../reference/motor-driver-settings.md#setpositionreportinterval) and [`/setPositionListReportInterval`](../reference/motor-driver-settings.md#setpositionlistreportinterval) above 65535 (32768 and above were read as negative and disabled the report), [`/setGoUntilTimeout`](../reference/homing.md#setgountiltimeout) and [`/setReleaseSwTimeout`](../reference/homing.md#setreleaseswtimeout) below 0 (they became about 49 days), [`/setElPos`](../reference/position-management.md#setelpos) with a full step outside 0-3 or a microstep outside 0-127, [`/setServoParam`](../reference/servo-mode_reference.md#setservoparam) with a negative gain, [`/setBrakeTransitionDuration`](../reference/brake.md#setbraketransitionduration) outside 0-65535, and TON_MIN or TOFF_MIN above 127 in [`/setDecayModeParam`](../reference/voltage-and-current-mode-settings.md#setdecaymodeparam) (STEP400).
- **Packets larger than 512 bytes and messages with more than 16 arguments** are answered with `/error/osc OscSyntaxError`.
- **Registers that the driver accepts only in some states.** A command that writes such a register replies `/error/command MotorNotHiZ` or `MotorNotStopped` and applies nothing to a motor that is not in the state; for example, [`/setMicrostepMode`](../reference/motor-driver-settings.md#setmicrostepmode) needs the outputs HiZ, and [`/setAcc`](../reference/speed-profile.md#setacc) needs a stopped motor. Before, the driver ignored the write while the firmware and the saved configuration took the value, so the register and the saved value differed. [`/setVoltageMode`](../reference/voltage-and-current-mode-settings.md#setvoltagemode) and [`/setCurrentMode`](../reference/voltage-and-current-mode-settings.md#setcurrentmode) change the mode only if the driver took it. `/setMicrostepMode` on a STEP400 motor in current mode replies `CommandIgnored` for a step mode finer than 1/16. With 255, each motor is judged alone.
- **`HomeSwActivating`.** [`/goUntil`](../reference/homing.md#gountil) and [`/goUntilRaw`](../reference/motor-control.md#gountilraw) send the error as `HomeSwActivating`, the text in the error list (it was `HomeSwActivated`), and it follows `/reportError`. For a motor in the servo mode, `/goUntil`, `/goUntilRaw` and [`/releaseSw`](../reference/homing.md#releasesw) reply `InServoMode` and do nothing.
- New command errors: `BrakeReleaseFailed`, `BrakeEngagedOnHiZ`, `ServoModeCancelledOnHiZ`, `MotorNotHiZ`, `MotorNotStopped`. See [`/error/command`](../reference/automatically-sent-messages.md#error-command).

#### Messages that the board sends {#v2-2-0-messages}

- **`/booted` has a second argument**, `resetCause`: `/booted myId resetCause`. Clients that check the exact number of arguments must be updated. The numbers: 0 unknown, 1 power-on, 2 brown-out, 3 reset pin, 4 watchdog, 5 software reset, 6 CPU fault. Treat 1 and 2 both as a reset by the power supply (on the SAMD21 a normal power-up is often reported as 2), and an unknown number as "other". See [`/booted`](../reference/automatically-sent-messages.md#booted).
- **Boolean arguments sent as `T` / `F` are now integers 0 / 1** (type tag `i`): the `/uvlo` notification ([`/uvlo`](../reference/automatically-sent-messages.md#uvlo)) and the third argument of `/lowSpeedOptimizeThreshold` ([`/getLowSpeedOptimizeThreshold`](../reference/motor-driver-settings.md#getlowspeedoptimizethreshold)).
- **[`/overCurrent`](../reference/automatically-sent-messages.md#overcurrent) and [`/stall`](../reference/automatically-sent-messages.md#stall)** are sent at once when the condition starts and, while it lasts, at most every 200 ms per motor and kind. Before, they were sent at every status read.
- **The status of the drivers is read every 5 ms** (it was 10 ms). The status notifications (`/busy`, `/HiZ`, `/homeSw`, `/dir`, `/motorStatus`, `/swEvent`, `/uvlo`, `/thermalStatus`, `/limitSw`) arrive up to 5 ms earlier and are still sent only on a change. Position reports and the other 10 ms tasks are unchanged. See [Timing of the notifications](../guides/alarms-and-protection.md#timing).
- **[`/getStatus`](../reference/motor-driver-settings.md#getstatus) and [`/getStatusList`](../reference/motor-driver-settings.md#getstatuslist) no longer clear the latched flags** of the driver, so a report can no longer be lost because a `/getStatus` cleared its flag. Only the status poll clears them, so a second `/getStatus` right after the first can still show a flag.
- When a driver goes HiZ by itself in the servo mode (overcurrent, overtemperature, UVLO), the servo mode is cancelled and `/error/command ServoModeCancelledOnHiZ` is sent, with or without the brake. See [When the driver goes HiZ by itself](../guides/alarms-and-protection.md#hiz-by-itself).
- The received address patterns are matched by the firmware's own parser; in some corner cases (for example characters following a `{...}` list) the result can differ from before.

#### Settings and values {#v2-2-0-settings}

- **Settings made with a Raw command are kept**: `/setSpeedProfileRaw`, `/setMaxSpeedRaw`, `/setMinSpeedRaw`, `/setFullstepSpeedRaw`, `/setAccRaw` and `/setDecRaw` also set the settings that `/saveConfig` saves and `/resetMotorDriver` applies again. They changed the register only. `/setMinSpeedRaw` ignores bit 12. See [`/setAccRaw`](../reference/speed-profile.md#setaccraw).
- [`/setStallThreshold`](../reference/alarm-settings.md#setstallthreshold) also changes the saved value (it changed the register only). [`/setPositionReportInterval`](../reference/motor-driver-settings.md#setpositionreportinterval) for one motor also clears the saved position list report interval.
- [`/getKval`](../reference/voltage-and-current-mode-settings.md#getkval), [`/getTval`](../reference/voltage-and-current-mode-settings.md#gettval) and [`/getTval_mA`](../reference/voltage-and-current-mode-settings.md#gettval_ma) (STEP400) return the settings instead of the registers, including the KVAL_HOLD that is raised for a motor with the brake.
- **[`/getSpeedProfile`](../reference/speed-profile.md#getspeedprofile) reports an acceleration and deceleration about 4.9% smaller**, which now matches the datasheet (driver libraries v1.2.0). [`/setAcc`](../reference/speed-profile.md#setacc), `/setDec` and `/setSpeedProfile` round to the nearest register value, so the value written can differ by 1 LSB.
- [`/getMinSpeed`](../reference/speed-profile.md#getminspeed) returns 0.0 for a motor with the low speed optimization enabled, for one motor and for 255. `/setMinSpeed 255` checks the optimization of each motor. [`/getDir`](../reference/motor-driver-settings.md#getdir)` 255` returns the direction (it returned the HiZ state).
- STEP400: the slew rate value 5 (980 V/µs, the initial value) is now written as the datasheet says, so the default setting switches faster than before ([`driverSettings.slewRate`](../connections/configuration-items.md#driversettings-slewrate)). A maximum speed of 0 is written as 1 by `/setMaxSpeed`, `/setSpeedProfile` and the `maxSpeed` setting. `/setFullstepSpeed` keeps the BOOST_MODE bit.
- `/setMinSpeedRaw` only changes the saved value while the low speed optimization is on. `/activate 1` no longer toggles the LED (debug code). [`/goUntilRaw`](../reference/motor-control.md#gountilraw) limits the speed to 20 bits, and `/goUntilRaw 255` reads the speed as a raw register value. [`/releaseSw`](../reference/homing.md#releasesw) reads its action argument like the other boolean arguments (0.5 was 0).
- **Homing at startup** (`homingAtStartup`) with the brake enabled first releases the brake, then starts the homing ([`driverSettings.homingAtStartup`](../connections/configuration-items.md#driversettings-homingatstartup)).

#### Motion, switches and homing {#v2-2-0-motion}

- **[`/goTo`](../reference/motor-control.md#goto), [`/goHome`](../reference/position-management.md#gohome), [`/goMark`](../reference/position-management.md#gomark) and `/combine/goTo` judge their direction correctly** when the HOME switch or the LIMIT switch prohibits a motion ([`/setProhibitMotionOnHomeSw`](../reference/alarm-settings.md#setprohibitmotiononhomesw), [`/setProhibitMotionOnLimitSw`](../reference/alarm-settings.md#setprohibitmotiononlimitsw)). The direction was reversed for a target less than 2048 steps away, and wrong again beyond 2^21 steps. It is now the shortest way, the way the driver goes. Motion near a switch can differ from v2.1.0.
- **[`/hardHiZ`](../reference/motor-control.md#hardhiz) for one motor no longer sends a soft stop first.** All the forms now behave the same.
- **Stop and HiZ commands cancel pending motion, also for motors with the brake disabled**: `/softStop`, `/hardStop`, `/softHiZ`, `/hardHiZ`, `/enableServoMode` and `/resetMotorDriver` cancel a `/goTo` (etc.) that waits for the BUSY flag, the homing and the servo mode. Before, a stopped motor could start again, or the timeout of a cancelled homing sent a hard stop to a motor made HiZ. A motion command that is accepted cancels a waiting `/goTo`.
- The automatic hard stops are not sent to a motor whose driver is HiZ, also with the brake disabled (home switch with `/setProhibitMotionOnHomeSw`, LIMIT switch, switch event in the servo mode, and the timeouts of `/goUntil` and `/releaseSw`). A hard stop energizes a HiZ driver. A motion command that clears the homing state now also clears the state of a `/goUntil` sent directly.

#### Servo mode {#v2-2-0-servo}

- **The update period is 5 ms** (it was 10 ms, and varied between about 7 and 13 ms when position reports were enabled). The integral and derivative terms are scaled by the period, so the same `kP`, `kI` and `kD` were designed to give about the same response, but the response can differ, so retune the gains if needed. See [Servo mode](../guides/servo-mode.md).
- Enabling the servo mode resets the integral and the previous error of the PID controller. The position error is wrapped correctly around the ends of the ABS_POS range. STEP400: the HOME switch and the LIMIT switch are judged separately.

#### Electromagnetic brake {#v2-2-0-brake}

- **On the STEP800, the brake outputs change as soon as the brake state changes** (0.2-0.3 ms), not 10-20 ms later.
- **The brake follows a state machine with six states**, readable with [`/getBrakeStatus`](../reference/brake.md#getbrakestatus). The commands changed for a motor with the brake enabled; the details are in the table of [Commands and the brake](../guides/electromagnetic-brake.md#commands). The main points:
  - `/activate 1` while the brake is released does nothing (it sent a hard stop). It releases the brake only if the driver is energized after the command; otherwise the brake stays engaged and `BrakeReleaseFailed` is sent.
  - `/activate 0` on a turning motor decelerates it and engages the brake when it has stopped, like `/softHiZ`.
  - After `/free`, a motion command or `/activate 1` returns the motor to the released state, and a stop of the motor no longer engages the brake.
  - `/softStop`, `/hardStop` and `/enableServoMode 0` while the brake is engaged or after `/free` do nothing. `/enableServoMode 1` and `/homing` while the brake is not released reply `BrakeEngaged`.
  - `/resetMotorDriver` and `/enableElectromagnetBrake` are accepted only in the states in which they are safe; otherwise `CommandIgnored` (the same rule applies to a configuration loaded over USB serial, with a warning).
  - `/activate 1` or a motion command during the deceleration for `/softHiZ` or `/activate 0` cancels the engaging and keeps the brake released (before, `/activate 1` sent a hard stop, and the brake engaged when the motor stopped later). On a stopped motor, `/softHiZ` and `/activate 0` engage the brake at the next status read (up to 5 ms); after `/free`, `/activate 0`, `/softHiZ` and `/hardHiZ` engage it at once. `/hardHiZ` on a released motor first stops it with a hard stop.
  - When the driver goes HiZ by itself, the brake engages and `BrakeEngagedOnHiZ` is sent.
  - A stop command received while the motor is decelerating for `/softHiZ` or `/activate 0` (state Stopping) cancels the plan to engage the brake, and the state returns to Released. This is the intended behavior, and the last command wins ([Stopping a motor that is going to engage the brake](../guides/electromagnetic-brake.md#stopping)).
- **Holding current**: KVAL_HOLD (TVAL_HOLD) is raised to at least half of KVAL_RUN (TVAL_RUN) whenever a motor with the brake enabled is energized again, now also after `/free` ([Holding current](../guides/electromagnetic-brake.md#hold-current)).
- **Restart, watchdog and CPU fault**: [`/resetDevice`](../reference/system-settings.md#resetdevice) and the USB serial command `R` first stop the turning motors, engage their brakes and wait for the longest transition duration (at most 1 s). **The watchdog detects a hang about 250 ms after the last watchdog reset**, with or without the brake (v2.1.0: about 62.5 ms); a command or load that blocks the board longer would restart it, and none is known. With the brake, every brake is engaged first and the board restarts up to 1 s later (`resetCause` 4). A CPU fault now engages every brake and restarts with `resetCause` 6 ([Restart, watchdog and CPU fault](../guides/electromagnetic-brake.md#restart)).
- **Times in which the load is not held** remain. On the STEP800, the brake outputs are engaged in `setup()` before the drivers are reset; at power-up they are still released for about 250 ms (mostly the bootloader), and longer with some power supplies (about 2 s was measured with 24 V). After a reset or a drop of the supply voltage, they are released for about 0.5 s. See [When the load is not held](../guides/electromagnetic-brake.md#unsupported).

#### Network {#v2-2-0-network}

- **`/destIp` can come later.** When [`/setDestIp`](../reference/system-settings.md#setdestip) starts the resolution of the MAC address of the destination, the reply is sent once the address is resolved: a few ms on a wired network, up to a few seconds on Wi-Fi. If it does not come, send `/setDestIp` again. Messages to the destination are dropped during the resolution (up to a few seconds), except the broadcast `/booted`. Use a command with a reply, such as `/getVersion`, to check that the board is alive. See [The destination and `/setDestIp`](../guides/communication-and-messages.md#setdestip).
- **A client replaced by another device with the same IP address** (another PC or network adapter) is now served after `/setDestIp` from the new device, sent 1.5 s or more after the last packet from the old one. Before, the board kept sending to the old MAC address until it was restarted.
- A send to a destination that never answers ARP no longer stops the processing for every message: the sends are paused for 1 s and then retried (the messages in between are dropped). The retransmission time of the W5500 is 20 ms with 2 retries.
- The MAC address is also resolved at start-up, after a change of the ID and when the Ethernet link comes up again (once `destIp` is set); the board sends one byte of UDP to port 9 of the broadcast address and of `destIp`, and the messages to `destIp` are dropped meanwhile. When a send to `destIp` fails, the sends are paused for 1 s and a packet from `destIp` resumes them.
- With `isMyIpAddId` or `isOutPortAddId`, an address beyond .254 or a port beyond 65535 is no longer used: the ID is not added and a warning is printed on the USB serial port ([Network and the DIP switch](../connections/network-and-dip-switch.md)).

#### microSD card {#v2-2-0-sd}

- Files whose name starts with `.` (for example the `._name.json` files that macOS writes) are no longer candidates for the configuration file.
- The values of a configuration file that is not accepted are no longer applied: the defaults are used. A first `.json` file that is invalid ends the search. The priority is unchanged: `config.txt`, then the first valid `.json`.
- An exFAT card is reported as `No SD card` and is not touched, with the PlatformIO build and the Arduino IDE build alike. Format the card as FAT16 or FAT32.
- Saving writes a hidden temporary file `.<name>.tmp` in the same folder and replaces the saved file only after it is written, so a failed save leaves the old file. See [Saving to the card](../connections/microsd-card.md#saving).
- Config received from the browser configuration tool no longer has the DIP switch ID added twice after an ID change. The received IP address, port and MAC address are applied by a reboot.

### Added {#v2-2-0-added}

- [`/getBrakeStatus`](../reference/brake.md#getbrakestatus): replies `/brakeStatus motorID state` (-1 for a motor with the brake disabled, otherwise 0-5). The numbers are part of the specification.
- USB serial: the destination MAC address (`s`, and `destMac` and `arpPending` in `T`), the brake states with names, `mcu`, `resetCause` and `resetCauseRaw` in `T`, and the command `p` (timing statistics). Test builds (`HIL_PROBE`) have more commands. See [Diagnosis via USB serial port](usb-serial-diagnosis.md).
- The hardware-in-the-loop test bench `tools/hil/` and timing probes (STEP800, `HIL_PROBE` builds) are for the developers of the firmware.

### Changed (internal) {#v2-2-0-changed}

These changes are not visible to OSC clients, or only in timing.

- The watchdog is driven by the firmware instead of the Adafruit SleepyDog library; the main loop runs in 5 ms slots; the OSC messages are received, dispatched and sent with static buffers (the CNMAT OSC library is not used any more); the drivers are read with one packed daisy-chain transfer.
- The USB serial `R` waits at least 50 ms after its reply before it restarts, so the reply arrives.
- The USB serial `b` (brake output test) is available only in test builds; it is gone from the normal builds.

### Fixed {#v2-2-0-fixed}

- A timeout (`goUntilTimeout`, `releaseSwTimeout`) of 2^31 ms or more no longer fires; before, it fired after 24.8 days or more.
- **CPU fault (HardFault).** The firmware engages every brake at once and restarts after the transition duration, with `resetCause` 6. On the STEP400 (R1 board), unplugging the USB cable while the Ethernet cable is connected can cause a CPU fault; this is a hardware issue of the board and also happens with v2.1.0, so the fault itself is not fixed. What changed is how the firmware handles it: the brakes are engaged first, and the restart is reported. See [The STEP400 restarts when USB is unplugged](troubleshooting.md#usb-unplug).
- `/setStallThreshold` was not saved, the position report interval of 32768 and above disabled the report, and `/setConfigName` accepted a non-string (it now replies `WrongDataType`). See [Settings and values](#v2-2-0-settings) and [Argument checks and errors](#v2-2-0-arguments).
- Servo mode: the update period varied between about 7 and 13 ms with position reports; with the brake disabled, a driver that went HiZ by itself was energized again by the next update.
- The transmit LED (TX) of the board blinks again for the position reports (it was turned off at once). This is only how it looks.
- USB serial: `F<filename>` typed by hand restarted the board; `R` replies are no longer lost; several fields of the diagnosis output were shown wrong.
- `/resetDevice` caused a HardFault, and the board was restarted by the watchdog. It now resets by software and `/booted` reports 5.
- A `/goTo`, `/goToDir`, `/goHome` or `/goMark` on a busy motor, and the USB serial `s`, cleared the latched flags of the driver, so a report could be lost.
- Arduino IDE build: saving to an exFAT card deleted the file on the card.
- A save to the card that failed after the old file was deleted left no configuration file (see [microSD card](#v2-2-0-sd)).
- With the DIP switch ID added to the IP address, an address beyond .254 became the broadcast address or wrapped around.

### Build and libraries {#v2-2-0-build}

- **Driver libraries v1.2.0 are required**: Ponoor PowerSTEP01 Library (STEP400, STEP100) and Ponoor L6470 Library (STEP800, STEP200). Firmware v2.1.0 and earlier use v1.1.x.
- With PlatformIO, the board is selected by the environment in `platformio.ini` (`step400`, `step800`, `step100`, `step200`), no longer by uncommenting a line in `src/boardsDef.h`. The Arduino IDE still uses `boardsDef.h`.
- The CNMAT OSC library and the Adafruit SleepyDog library are not needed any more. SdFat 2.2.3 or later, Ethernet 2.0.2 or later and ArduinoJson 7.4.1 or later (7.x) are needed; the version of SdFat is the same as for v2.1.0.
- See [Compiling the firmware](compile-the-arduino-sketch.md).

### Known issues in v2.2.0 {#v2-2-0-known-issues}

- **`canSendMsgBeforeDestIp` shares its value with "`/setDestIp` has been received".** After `/setDestIp` was received, saving the configuration (`/saveConfig`, or with the browser configuration tool) writes `true` to the card, and when the browser configuration tool writes `false`, the board sends no reply until `/setDestIp` is sent again. Send `/setDestIp` again after saving, and check the value in the saved file. See [`network.canSendMsgBeforeDestIp`](../connections/configuration-items.md#network-cansendmsgbeforedestip) and [A known issue with `canSendMsgBeforeDestIp`](../connections/browser-config-tool.md#known-issue).
- **Saving without a configuration file.** If the board started without a configuration file (no card, or no valid file) and you save, the file is written with `information.configVersion` `[-1, 0]` and `information.targetProduct` `"---"`, because the board has no version and product to write. The values are saved. To get a file with the right version and product, make it with the browser configuration tool (**Download JSON**). See [Where it is saved](../connections/microsd-card.md#save-target).
- **The STEP400 (R1 board) can restart when the USB cable is unplugged while the Ethernet cable is connected.** It is a hardware issue, the same as with v2.1.0. See [STEP400](../hardware/step400.md#usb-unplug).

## v2.1.0 {#v2-1-0}

Released in June 2026 ([GitHub Release](https://github.com/ponoor/step-series-universal-firmware/releases/tag/v2.1.0)).

### New features {#v2-1-0-new}

- **Browser configuration tool support.** The serial commands `G`, `T`, `{...}`, `R` and `F` let the [browser configuration tool](../connections/browser-config-tool.md) read and write the settings over USB (Web Serial API).
- **[`/saveConfig`](../reference/system-settings.md#saveconfig)** saves the running configuration to the microSD card without removing the card.
- **[`/setConfigName`](../reference/system-settings.md#setconfigname)** sets the name of the configuration, and the reply of [`/getConfigName`](../reference/system-settings.md#getconfigname) has a fifth argument, `configFilename`, the file name on the card.
- **Long file names.** The configuration file is no longer limited to the 8.3 file name. The firmware reads `config.txt` first, and then the alphabetically first `.json` file ([The file that the board reads](../connections/microsd-card.md#files)).

### Changes {#v2-1-0-changes}

- The SD library was changed from `arduino-libraries/SD` to `greiman/SdFat` v2 (long file names). The Arduino IDE sketch folder was removed from the repository; the sketch for the Arduino IDE is `step-series-universal-firmware.zip` in the assets of each release.
- The STEP400 configuration key `goUnitlTimeout` (a typo of the template) is accepted. The firmware reads `goUntilTimeout`, and if it is missing, `goUnitlTimeout`. Before (v2.0.0), only `goUntilTimeout` was read, so the value under the misspelled key was silently ignored and the default (10000 ms) was used.

### Migration notes {#v2-1-0-migration}

- Configuration files from v2.0.0 are compatible (the configuration version is the same). A STEP400 configuration file made from the old template can contain `goUnitlTimeout`. Its value was ignored by v2.0.0 and is used from v2.1.0; check that it is the value you want. Renaming the key to `goUntilTimeout` is recommended but not required.
- Long file names are supported, but `config.txt` is still read first.

## v2.0.0 {#v2-0-0}

Released in October 2025 ([GitHub Release](https://github.com/ponoor/step-series-universal-firmware/releases/tag/v2.0.0)). **The physical motion changes for the same commands.**

- **The speed calculations were corrected** to match the real motion. Acceleration and deceleration take twice as long as in v1.x, and the speed is slightly slower. Details: [issue of the PowerSTEP01 library](https://github.com/ponoor/Ponoor_PowerSTEP01_Library/issues/4).
- **The status poll period was changed from 1 ms to 10 ms, and the servo update period to 10 ms**, based on measured processing speeds, to reduce the interference of the OSC communication. The servo mode can track the target position differently from v1.x. (v2.2.0 changes the status read and the servo update to 5 ms.)
- If you update from v1.x, check the motion, adjust the speed profiles, the timing of the commands and your control logic.

## Earlier versions {#earlier}

The firmware of the STEP Series (STEP400, STEP800, and the STEP100 / STEP200 variants) was developed in the repository [step-series-universal-firmware](https://github.com/ponoor/step-series-universal-firmware) as v0.x and v1.x before v2.0.0. Detailed changelogs of these versions were not kept; see the [Releases](https://github.com/ponoor/step-series-universal-firmware/releases) and the tags on GitHub. The older STEP400 and STEP800 firmware is in the repositories [ponoor/STEP400](https://github.com/ponoor/STEP400) and [ponoor/STEP800](https://github.com/ponoor/STEP800).
