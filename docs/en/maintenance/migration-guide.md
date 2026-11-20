---
title: Migration guide
---

# Migration guide

This page is for people who update the firmware from v2.1.0 to v2.2.0. The OSC addresses are compatible, but the behavior of many commands changed, and a client or a setup that worked with v2.1.0 can behave differently. Each item below says what changed, who is affected, and what to do. The details are in the guides and the reference; this page gives the points and the actions only. For the full list of the changes, see the [Firmware changelog](changelog.md#v2-2-0).

If you update from v2.0.0, read [Updating from v2.0.0](#from-v2-0-0) first. If you want to go back to v2.1.0, see [Going back to v2.1.0](#downgrade).

## Checklist {#checklist}

Go through the list and read the items that apply to you.

**If you write OSC clients (software that sends commands to the board):**

- [ ] Your client checks the number of arguments of `/booted` → [`/booted` has a second argument](#booted)
- [ ] Your client reads `/uvlo` or `/lowSpeedOptimizeThreshold` → [Booleans are sent as integers](#boolean-args)
- [ ] Your client sends commands that can lack an argument, have a wrong type, or a value out of range → [Wrong commands are rejected](#rejected-args)
- [ ] Your client changes the microstep mode, the speed profile, the voltage or current mode, or the decay mode while the motor is moving or holding → [Settings the driver accepts only in some states](#register-states)
- [ ] Your client reads back KVAL, TVAL, the speed profile or the minimum speed → [Values returned by the get commands](#getters)
- [ ] Your client talks to the board over Wi-Fi, replaces the PC, or uses `/setDestIp` as a heartbeat → [`/setDestIp` and `/destIp`](#destip)
- [ ] Your client reads `/getStatus`, or counts `/overCurrent` and `/stall` → [Status flags and reports](#status-reports)
- [ ] You use the servo mode → [Servo mode](#servo)
- [ ] You use `/setProhibitMotionOnHomeSw` or `/setProhibitMotionOnLimitSw` with `/goTo`, `/goHome` or `/goMark` → [Direction near a switch](#switch-direction)
- [ ] You send `/hardHiZ` to one motor, or stop commands while a `/goTo` is waiting → [Stop commands](#stop-commands)
- [ ] You set the position report interval above 32767 → [Position report interval](#report-interval)
- [ ] Your client retries the homing or treats `/homingStatus` 4 as success → [Homing no longer ends at once with `ReleaseSwTimeout`](#homing-timeout)

**If you make configuration files or use the microSD card:**

- [ ] You use `/setAccRaw` and the other Raw commands, with `/saveConfig` or `/resetMotorDriver` → [Raw settings are kept](#raw-saved)
- [ ] Your card is an SDXC card of 64 GB or more, or was formatted on a Mac → [exFAT cards and hidden files](#exfat)
- [ ] Your card can hold a configuration file that is not valid → [Invalid files are not applied](#invalid-files)
- [ ] You use `myIp` or the send port with the ID added → [Address and port with the ID](#id-limits)
- [ ] You have a STEP400 configuration with `goUnitlTimeout` → [`goUnitlTimeout`](#go-until-timeout)
- [ ] You use the default slew rate of the STEP400 → [Slew rate of the STEP400](#slew-rate)
- [ ] You write the settings with the browser configuration tool → [Writing from the browser configuration tool](#config-tool)

**If you use an electromagnetic brake:**

- [ ] You send commands to a motor with the brake enabled → [Commands and states](#brake-commands)
- [ ] You use `homingAtStartup` or the servo mode with the brake → [Commands and states](#brake-commands)
- [ ] The motor holds a load → [Holding current](#brake-hold-current), [Restart, watchdog and CPU fault](#brake-restart), [Times in which the load is not held](#brake-unsupported)

**If you build the firmware yourself:**

- [ ] You build with PlatformIO → [Selecting the board](#board-select)
- [ ] You use the Arduino IDE or manage the libraries yourself → [Libraries](#libraries)

## OSC clients {#osc-clients}

### `/booted` has a second argument {#booted}

**What changed.** v2.1.0 sent `/booted myId`. v2.2.0 sends `/booted myId resetCause`, where `resetCause` is an integer (`i`).

**Who is affected.** Clients that check the exact number of arguments of `/booted`, and clients that stop at a reset cause they do not know.

**What to do.** Accept two arguments. Treat `1` (power-on) and `2` (brown-out) both as a reset by the power supply, because on the SAMD21 a normal power-up is often reported as `2`. Accept `6` (CPU fault), which is new, and treat any number you do not know as "other"; the numbers will not change, and new ones are added as 7, 8, ... Details: [`/booted`](../reference/automatically-sent-messages.md#booted).

### Booleans are sent as integers {#boolean-args}

**What changed.** The `/uvlo` notification (enabled by `/enableUvloReport`) and the third argument of `/lowSpeedOptimizeThreshold` (the reply to `/getLowSpeedOptimizeThreshold`) were sent as the OSC types `T` and `F`. They are now integers `0` and `1` (type tag `i`), as all the other booleans of the STEP Series. The reply to `/getUvlo` was already an integer.

**Who is affected.** Clients that expect `T` / `F` in these two messages.

**What to do.** Read these arguments as integers 0 / 1. When you send a boolean, send an integer 0 / 1. The board accepts a number of 1.0 or more, a positive integer, or `T`; this has not changed. Details: [`/uvlo`](../reference/automatically-sent-messages.md#uvlo).

### Wrong commands are rejected {#rejected-args}

**What changed.** v2.1.0 applied a missing or wrong argument as 0: `/setKval 1` set every KVAL of motor 1 to 0, `/setSpeedProfile 1` set the acceleration, deceleration and maximum speed to 0, and a `/setTargetPositionList` with too few positions sent the missing motors to position 0. v2.2.0 checks the command before it applies anything:

- too few arguments: `/error/osc MissingArgument`;
- an argument of the wrong type (a string for a number, NaN, infinity): `/error/osc WrongDataType`;
- a value out of the range of the command: `/error/command CommandIgnored motorID` (`255` for `/setPositionListReportInterval`);
- a motor ID outside 0-255: `/error/command MotorIdNotMatch` with the value sent (257 and 511 were read as 1 and 255);
- a packet larger than 512 bytes, or a message with more than 16 arguments: `/error/osc OscSyntaxError`;
- not a rejection, but also changed: address patterns are matched by the firmware's own parser, and in rare cases (for example characters after a `{...}` list) the result can differ from v2.1.0.

Nothing is applied when a command is rejected. Extra arguments are still ignored. In addition, `/goUntil` and `/goUntilRaw` report an activated HOME switch as `HomeSwActivating`; v2.1.0 sent the text `HomeSwActivated`.

**Who is affected.** Clients that send incomplete commands, send the wrong type, or depend on the old values; clients that wait for a specific error text; clients that count on a command having an effect when its value is out of range.

**What to do.** Send complete commands with numbers of the right type and in the range. Show or log `/error/osc` and `/error/command`, and keep error reports on (`/reportError 1`; with `/reportError 0` nothing is sent, but the command is still rejected). Match the error text `HomeSwActivating`. The ranges are in the reference of each command. Details: [Errors](../guides/communication-and-messages.md#errors), [The arguments that the board receives](../guides/communication-and-messages.md#arguments).

### Settings the driver accepts only in some states {#register-states}

**What changed.** The driver accepts some registers only in some states. In v2.1.0, a set command that did not meet the condition was ignored by the driver, but the firmware and the saved configuration took the new value, so the register and the saved value differed. In v2.2.0 the state is read when the command arrives, and a motor that is not in the state replies an error and nothing is applied:

- `/error/command MotorNotHiZ`: the outputs must be HiZ. `/setMicrostepMode`, `/setHomeSwMode`, `/setBemfParam`, `/setDecayModeParam`, and (STEP400) `/setVoltageMode` and `/setCurrentMode`. **A motor that holds its position is not HiZ.**
- `/error/command MotorNotStopped`: the motor must be stopped or HiZ. `/setAcc`, `/setDec`, `/setMinSpeed`, `/setSpeedProfile`, the Raw versions of these, `/enableLowSpeedOptimize`, and `/setLowSpeedOptimizeThreshold` while the optimization is enabled.
- `/setMicrostepMode` in the current mode of a STEP400 motor: `CommandIgnored` for a step mode finer than 1/16.
- `/setVoltageMode` and `/setCurrentMode` change the mode only if the driver took it; otherwise `CommandIgnored`.

With `255`, each motor is judged alone: the motors in the state are changed and the others reply the error.

**Who is affected.** Clients that change these settings while the motor is moving or holding its position.

**What to do.** Send `/softHiZ` or `/hardHiZ` first for the MotorNotHiZ group, and stop the motor first for the MotorNotStopped group (a motor that is stopped and holding is accepted). Handle the errors. Details: [Errors](../guides/communication-and-messages.md#errors) and the reference of each command, for example [`/setMicrostepMode`](../reference/motor-driver-settings.md#setmicrostepmode).

### Values returned by the get commands {#getters}

**What changed.**

- `/getKval`, `/getTval` and `/getTval_mA` (STEP400) return the settings (what `/setKval` and `/setTval` set, and `/saveConfig` saves), not the registers. `/setKval` changes the KVAL registers only in the voltage mode, and `/setTval` the TVAL registers only in the current mode; the registers of the mode that is not in use keep the earlier value. For a motor with the brake, the raised KVAL_HOLD (TVAL_HOLD) is returned. The STEP800 is unchanged.
- `/getSpeedProfile` reports an acceleration and deceleration about 4.9% smaller than v2.1.0 for the same motion. They now match the datasheet. `/setAcc`, `/setDec` and `/setSpeedProfile` round to the nearest register value, so the value written can differ by 1 LSB.
- `/getMinSpeed` returns `0.0` for a motor with the low speed optimization enabled, for one motor and for `255` alike.
- `/getDir 255` returns the direction (it returned the HiZ state).
- STEP400: a maximum speed of 0 is written as 1.

**Who is affected.** Clients that compare the value they read with the value they set, or that show these values.

**What to do.** Do not compare the numbers exactly; allow the rounding. Do not use the reported acceleration to check that a value was applied. The motion itself is not changed by the 4.9%: only the reported value is. Details: [`/getKval`](../reference/voltage-and-current-mode-settings.md#getkval), [`/getSpeedProfile`](../reference/speed-profile.md#getspeedprofile).

### `/setDestIp` and `/destIp` {#destip}

**What changed.** When `/setDestIp` starts the resolution of the MAC address of the destination (the first one, one from another address than the current destination, or one 1.5 s or more after the last packet from the destination), the reply `/destIp` is sent once the address is resolved. It takes a few ms on a wired network and up to a few seconds on Wi-Fi. While the address is being resolved, the messages to the destination (replies, reports, errors) are dropped, not sent later; the broadcast `/booted` is sent. In exchange, a client replaced by another device with the same IP address is now served after a `/setDestIp` from the new device. The same resolution also runs at start-up, after a change of the ID and when the link comes up again, and a destination that never answers ARP pauses the sends for 1 s; messages in that time are dropped.

**Who is affected.** Clients that wait for `/destIp` with a short time-out; clients on Wi-Fi; clients that send `/setDestIp` every second as a heartbeat; setups that change the PC or the network adapter.

**What to do.** Wait a few seconds for `/destIp`; if it does not come, send `/setDestIp` again. Send `/setDestIp` at the start of the connection and after a change of the network or the PC, at least 1.5 s after the last packet of the old one. Send it while the motors are stopped, because the resolution on Wi-Fi can stop the board's processing for up to about 41 ms at a time. To check that the board is alive, use a command with a reply, such as `/getVersion`, not `/setDestIp`. Details: [The destination and `/setDestIp`](../guides/communication-and-messages.md#setdestip), [`/setDestIp`](../reference/system-settings.md#setdestip).

### Status flags and reports {#status-reports}

**What changed.**

- `/getStatus` and `/getStatusList` no longer clear the latched flags of the driver (OCD, the stall flags, UVLO, SW_EVN). Only the status poll of the firmware (every 5 ms) clears them. A `/getStatus` sent right after another can show a flag that the earlier reply showed.
- `/setStallThreshold` also changes the saved value, so `/saveConfig` and `/resetMotorDriver` now keep it.
- `/overCurrent` and `/stall` are sent at once when the condition starts and, while it lasts, at most every 200 ms per motor and kind. Before, they were sent at every status read.
- The status is read every 5 ms instead of 10 ms, so the status notifications (`/busy`, `/HiZ`, `/homeSw`, ...) arrive up to 5 ms earlier. They are still sent only on a change.

**Who is affected.** Clients that use `/getStatus` to clear a flag, or that count `/overCurrent` or `/stall` messages as a measure of how long the condition lasted.

**What to do.** Do not depend on `/getStatus` to clear a flag. Use the time between `/overCurrent` messages (200 ms at the shortest) instead of their number. Details: [Timing of the notifications](../guides/alarms-and-protection.md#timing).

### Servo mode {#servo}

**What changed.** The update period is 5 ms instead of 10 ms (and no longer varies between about 7 and 13 ms when position reports are enabled). The integral and derivative terms are scaled by the period, so the same `kP`, `kI` and `kD` were designed to give about the same response, but the response can differ. Enabling the servo mode resets the integral and the previous error. `/goUntil`, `/goUntilRaw` and `/releaseSw` for a motor in the servo mode reply `InServoMode` and do nothing. When the driver goes HiZ by itself (overcurrent, overtemperature, UVLO), the servo mode is cancelled and `ServoModeCancelledOnHiZ` is sent. Send `/enableServoMode 1` to start again (the current position becomes the target). With the brake enabled, see also [Commands and states](#brake-commands).

**Who is affected.** Everyone who uses the servo mode; clients that expect the servo mode to go on after an overcurrent shutdown.

**What to do.** Check the response of the servo mode and tune the gains again if needed ([Determining the PID parameters](../guides/servo-mode.md#tuning)). Handle `ServoModeCancelledOnHiZ`. Details: [Servo mode](../guides/servo-mode.md), [When the driver goes HiZ by itself](../guides/alarms-and-protection.md#hiz-by-itself).

### Direction near a switch {#switch-direction}

**What changed.** `/goTo`, `/goHome`, `/goMark` and `/combine/goTo` judge their direction correctly when the HOME switch or the LIMIT switch prohibits a motion (`/setProhibitMotionOnHomeSw`, `/setProhibitMotionOnLimitSw`). In v2.1.0 the direction was reversed for a target less than 2048 steps away (a short move away from the switch was refused with `HomeSwActivating` or `LimitSwActivating`, and a short move towards it was started), and wrong again beyond 2^21 steps. It is now the shortest way, the way the driver goes.

**Who is affected.** Setups that use these settings with `/goTo` and the like near a switch. The motion can differ from v2.1.0, especially for short moves.

**What to do.** Test the motions near the switches again. A workaround that you built for the old direction is no longer needed. Details: [Switches that prohibit a motion](../guides/alarms-and-protection.md#switches).

### Stop commands {#stop-commands}

**What changed.**

- `/hardHiZ` for one motor no longer sends a soft stop before the hard HiZ. A single motor, `255` and `/combine/hardHiZ` behave the same. With the brake enabled and released, the motor is stopped with a hard stop before the brake engages.
- `/goUntilRaw 255` reads the speed as a raw register value, like `/goUntilRaw` for one motor (it was steps/s).
- `/softStop`, `/hardStop`, `/softHiZ`, `/hardHiZ`, `/enableServoMode` and `/resetMotorDriver` cancel the pending motion, also for a motor with the brake disabled: a `/goTo`, `/goToDir`, `/goHome` or `/goMark` that waits for the BUSY flag, the homing, and the servo mode. Before, a stopped motor could start again, and the timeout of a cancelled homing sent a hard stop that energized a motor made HiZ. An accepted motion command also cancels a waiting `/goTo`.
- The automatic hard stops (home switch with `/setProhibitMotionOnHomeSw`, LIMIT switch, switch event in the servo mode, and the timeouts of `/goUntil` and `/releaseSw`) are not sent to a motor whose driver is HiZ.

**Who is affected.** Clients that send a stop command and then rely on the earlier `/goTo` to start later, or that rely on a hard stop to energize a HiZ motor.

**What to do.** Send the motion command again after a stop command. To energize a motor, use a motion command, not a stop. Details: [Types of stop](../guides/speed-profile-and-motions.md#stops).

### Position report interval {#report-interval}

**What changed.** The interval of `/setPositionReportInterval` and `/setPositionListReportInterval` is 0-65535 ms. v2.1.0 read 32768 and above as negative, which disabled the report. A value above 65535 now replies `CommandIgnored`. A negative interval still disables the report. For one motor, `/setPositionReportInterval` also clears the saved position list report interval.

**Who is affected.** Clients that set an interval of 32768 ms or more.

**What to do.** Use values up to 65535 (0 or a negative value disables the report, as before). Details: [`/setPositionReportInterval`](../reference/motor-driver-settings.md#setpositionreportinterval).

### Homing no longer ends at once with `ReleaseSwTimeout` {#homing-timeout}

**What changed.** In v2.1.0 and earlier, `/homing` often ended with `/homingStatus` 4 and `ReleaseSwTimeout` about 1 ms after the switch was found, instead of 3. It happened in almost every homing or almost never, depending on the start-up. It was an error in the calculation of the elapsed time of the timeout, and v2.2.0 fixes it.

**Who is affected.** Clients that retried the homing, or treated `/homingStatus` 4 as success, to get around the error.

**What to do.** Remove the retry. Treat 3 as the end of the homing, and 4 as a real timeout of `/releaseSw`. Details: [Homing ends at once with `ReleaseSwTimeout`](troubleshooting.md#release-sw-timeout), [Fixed](changelog.md#v2-2-0-fixed).

## Configuration files and the microSD card {#config-files}

### Raw settings are kept {#raw-saved}

**What changed.** `/setSpeedProfileRaw`, `/setMaxSpeedRaw`, `/setMinSpeedRaw`, `/setFullstepSpeedRaw`, `/setAccRaw` and `/setDecRaw` now also set the settings that `/saveConfig` saves and `/resetMotorDriver` applies again (also the reset after a fault). In v2.1.0 they changed the register only, so a reset or a saved configuration brought back the value from before. The value kept is the one that converts back to the same Raw value, so it can differ from `/getMinSpeed` and `/getFullstepSpeed` by half a register step. `/setMinSpeedRaw` ignores bit 12 (it switched the low speed optimization on).

**Who is affected.** Clients and setups that use the Raw commands together with `/saveConfig`, or that expected a reset to bring back the earlier value.

**What to do.** Nothing in most cases: the Raw settings now survive a reset and are saved. If you relied on the reset to undo a Raw setting, send the earlier value again. Details: [`/setAccRaw`](../reference/speed-profile.md#setaccraw), [What is saved](../connections/how-settings-work.md#what-is-saved).

### Invalid files are not applied {#invalid-files}

**What changed.** The values of a configuration file that is not accepted are no longer applied. In v2.1.0, a first `.json` file without `information.configVersion`, or a `config.txt` that failed to parse in the middle, was reported as not loaded, but its values (or the values before the failure) were still used. Now the defaults are used, as with no card. The priority is unchanged: `config.txt`, then the alphabetically first `.json` file; if that file is invalid, the search ends and the defaults are used.

**Who is affected.** Cards with an invalid file; cards that were copied on a Mac (see the next item).

**What to do.** After starting, check `/getConfigName` (the open and parse arguments) or the USB serial `s`. Make the configuration file valid, or remove the invalid one. Details: [The file that the board reads](../connections/microsd-card.md#files).

### exFAT cards and hidden files {#exfat}

**What changed.**

- Files whose name starts with `.` are no longer candidates for the configuration file. A Mac writes a hidden `._name.json` next to each file it copies to a FAT card; in v2.1.0 these sorted first, were not JSON, and hid every valid `.json` file after them.
- An exFAT card (SDXC, 64 GB or more by default) is treated as "No SD card" and nothing on it is touched. In v2.1.0, the Arduino IDE build deleted the configuration file on an exFAT card when it saved.

**Who is affected.** Users of SDXC cards, and of cards copied on a Mac.

**What to do.** Format the card as FAT16 or FAT32 (FAT32 for 64 GB or more; "MS-DOS (FAT)" in the Disk Utility of macOS). Details: [Preparing the card](../connections/microsd-card.md#card).

### Saving and the temporary file {#saving}

**What changed.** A save writes the configuration to a hidden temporary file `.<name>.tmp` in the same folder, and replaces the saved file only after it is written and closed. A save that fails (the card or the root folder is full, a write error) leaves the old file and replies `SD open failed`. The target of a save is the file read at start (`/config.txt` if none was read). A power cut between deleting the old file and renaming the new one leaves only the temporary file, and nothing recovers it at start-up.

**Who is affected.** Everyone who saves. The `.tmp` file can be seen on the card after a failure; it is not read.

**What to do.** Do not cut the power during a save. If only a `.tmp` file is left, rename it to the name of the configuration file. Details: [Saving to the card](../connections/microsd-card.md#saving).

### Address and port with the ID {#id-limits}

**What changed.** With `isMyIpAddId`, the last number of `myIp` plus the ID can be up to 254 (up to ID 154 with the default 10.0.0.100); beyond that, the ID is not added, the configured address is used, and a warning is printed on the USB serial port. v2.1.0 produced the broadcast address (.255) or wrapped around (.0 to .99). The same applies to the send port with `isOutPortAddId`, beyond 65535.

**Who is affected.** Setups with many boards whose IDs reach the limit.

**What to do.** Choose `myIp` and the IDs so that the sum stays within the limit. Details: [Network and DIP switch](../connections/network-and-dip-switch.md).

### `goUnitlTimeout` {#go-until-timeout}

**What changed.** The STEP400 template of the configuration file once had the key `goUnitlTimeout` (a typo). v2.0.0 reads only `goUntilTimeout`, so the value under the typo was ignored and the default (10000 ms) was used. v2.1.0 and v2.2.0 read `goUntilTimeout`, and if it is missing, `goUnitlTimeout`, when the file is loaded at start-up (the write of the browser configuration tool reads only `goUntilTimeout`). So nothing changes between v2.1.0 and v2.2.0.

**Who is affected.** A file with `goUnitlTimeout` and a value other than 10000 that you move from v2.0.0 to a newer firmware: the value starts to work.

**What to do.** Check the value, and rename the key to `goUntilTimeout`. Details: [`driverSettings.goUntilTimeout`](../connections/configuration-items.md#driversettings-gountiltimeout).

### Slew rate of the STEP400 {#slew-rate}

**What changed.** The slew rate value 5 (980 V/µs), the initial value, was written to the driver with the wrong values in v2.1.0 (64 mA and 2375 ns), so the switching was slower than 980 V/µs. v2.2.0 writes what the datasheet says (96 mA, 375 ns). A board with the default setting switches faster than before. The values 0-4 are unchanged. The STEP800 is not affected.

**Who is affected.** STEP400 boards that use the default slew rate.

**What to do.** Check the temperature of the drivers and the EMI on the real hardware. If needed, choose a lower value of `driverSettings.slewRate`. Details: [`driverSettings.slewRate`](../connections/configuration-items.md#driversettings-slewrate).

### Writing from the browser configuration tool {#config-tool}

**What changed.** Writing the settings from the browser configuration tool (the `{` command of the USB serial port) stops the processing of the board for a short time, as before (about 0.1-0.3 s, and up to about 0.7 s for the first save after a card is inserted; measured). A change of the brake setting is judged by the rule of `/enableElectromagnetBrake` (see [Commands and states](#brake-commands)): for a motor that is energized, it is not applied and a warning is printed. The received IP address, port and MAC address are stored without the ID added, so they no longer get the ID twice after an ID change, and they take effect at the next reboot.

**Who is affected.** Anyone who writes the settings while the motors are moving.

**What to do.** Stop the motors before you write. Also note the [known issue with `canSendMsgBeforeDestIp`](../connections/browser-config-tool.md#known-issue). Details: [Browser configuration tool](../connections/browser-config-tool.md#saving).

## Electromagnetic brake {#brake}

This section is for a motor with the brake enabled (`/enableElectromagnetBrake`). A motor whose brake is disabled is not affected, except by [Stop commands](#stop-commands).

### Commands and states {#brake-commands}

**What changed.** The brake follows a new state machine with six states, which `/getBrakeStatus` returns. In short:

- On the STEP800, the brake outputs change as soon as the brake state changes (within 0.3 ms of the command), not 10-20 ms later.
- `/activate 1` while the brake is released does nothing (it sent a hard stop). It releases the brake only if a status read after the command shows the driver energized; otherwise the brake stays engaged and `BrakeReleaseFailed` is sent. Before, the brake was released after `brakeTransitionDuration` in any case.
- `/activate 0` on a turning motor decelerates it and engages the brake when it has stopped, like `/softHiZ`. It engaged the brake without stopping the motor.
- `/softStop`, `/hardStop` and `/enableServoMode 0` while the brake is engaged or after `/free` do nothing. `/enableServoMode 1` and `/homing` while the brake is not released reply `BrakeEngaged` and do nothing.
- A stop command received during the deceleration for `/softHiZ` or `/activate 0` (state Stopping) cancels the plan to engage the brake and returns the state to Released; the motor stays energized. The last command wins. Send `/softHiZ`, `/activate 0` or `/hardHiZ` again if you want the brake.
- After `/free`, a motion command or `/activate 1` energizes the motor and returns it to Released.
- `/resetMotorDriver` is accepted only while the brake is engaged or after `/free`; `/enableElectromagnetBrake` changes the setting only while the driver is HiZ. Otherwise `CommandIgnored`.
- When the driver goes HiZ by itself, the brake engages at the next status read and `BrakeEngagedOnHiZ` is sent.
- `/activate 1` or a motion command during the deceleration for `/softHiZ` or `/activate 0` cancels the engaging (it sent a hard stop before).
- Homing at startup (`homingAtStartup`) releases the brake first and starts the homing when the brake is released.
- The brake times are counted in 5 ms steps: the release comes 0-5 ms after `brakeTransitionDuration`.

**Who is affected.** Clients that control a motor with the brake enabled.

**What to do.** Use `/activate 1` to start (check with `/getBrakeStatus` that the state is 2, Released, before you send motions), `/softHiZ` or `/activate 0` to stop, and handle `BrakeEngaged`, `BrakeReleaseFailed` and `BrakeEngagedOnHiZ`. Do not rely on the old behavior of `/activate`. Details: the table in [Commands and the brake](../guides/electromagnetic-brake.md#commands), [States of the brake](../guides/electromagnetic-brake.md#states) and [Stopping a motor that is going to engage the brake](../guides/electromagnetic-brake.md#stopping).

### Holding current {#brake-hold-current}

**What changed.** KVAL_HOLD (TVAL_HOLD in the current mode) is raised to at least half of KVAL_RUN (TVAL_RUN) whenever a motor with the brake is energized again: `/activate 1` (as before), and now also after `/free`. The raised value is what `/getKval` returns.

**Who is affected.** Motors that hold a load with the brake released.

**What to do.** Check that the holding current is suitable for the motor and the load. Details: [Holding current](../guides/electromagnetic-brake.md#hold-current).

### Restart, watchdog and CPU fault {#brake-restart}

**What changed.** The board engages the brakes before it restarts. `/resetDevice` and the USB serial `R` stop the turning motors with a hard stop, engage their brakes and wait for the longest `brakeTransitionDuration` (at most 1 s). When the watchdog detects a hang (about 250 ms after the last watchdog reset), every brake is engaged first, and the board restarts after the longest `brakeTransitionDuration` (at most 1 s), with `resetCause` 4; v2.1.0 restarted about 62.5 ms after a hang. A CPU fault engages every brake at once and restarts with `resetCause` 6.

**Who is affected.** Setups in which a restart must be quick, or that watch for the restart.

**What to do.** Expect a restart to take up to 1 s longer. The watchdog itself now fires about 250 ms after a hang with or without the brake (v2.1.0: about 62.5 ms); a command that blocks the board longer would restart it, and none is known. Details: [Restart, watchdog and CPU fault](../guides/electromagnetic-brake.md#restart).

### Times in which the load is not held {#brake-unsupported}

**What changed.** The firmware cannot remove these times, but v2.2.0 engages the brake outputs earlier in `setup()`. On the STEP800, all the brakes stay released for about 250 ms after the power is applied (mostly the bootloader); depending on the power supply it can be longer, and about 2 s was measured with 24 V. After a reset or a drop of the supply voltage, they are released for about 0.5 s. The STEP400 with the EMB-STEP400 engages the brakes at once at a reset. Even then, the shaft is held only after the brake has locked mechanically, which takes tens of ms.

**Who is affected.** Setups that hang a load on the motor, especially with the STEP800.

**What to do.** Take the power of the brake from the same power supply as the motor, or from a supply that is cut together with the power of the motor. Do not let only the power of the motor be cut first. Do homing again after a restart and after the motor has been HiZ. Details: [When the load is not held](../guides/electromagnetic-brake.md#unsupported), [Usage notes](../guides/electromagnetic-brake.md#usage).

## Building the firmware yourself {#building}

### Selecting the board {#board-select}

**What changed.** Until v2.1.0, you selected the board by uncommenting one line in `src/boardsDef.h`. With PlatformIO, v2.2.0 selects it by the environment in `platformio.ini`: `step400`, `step800`, `step100` or `step200`. The Arduino IDE still uses `boardsDef.h`.

**Who is affected.** Everyone who builds with PlatformIO.

**What to do.** Leave every board line in `boardsDef.h` commented out; do not select the board in both places. Select the environment: `pio run -e step800 -t upload`, or `default_envs` in `platformio.ini`. The old environment `zeroUSB` is kept and builds the STEP400. Details: [Selecting the board](compile-the-arduino-sketch.md#select-board).

### Libraries {#libraries}

**What changed.** The firmware needs the driver libraries **1.2.0 or later** (Ponoor PowerSTEP01 Library, Ponoor L6470 Library); v2.1.0 and earlier use 1.1.x. Ethernet 2.0.2 or later, SdFat 2.2.3 or later (the same as v2.1.0) and ArduinoJson 7.4.1 or later (7.x) are needed. The CNMAT OSC library and the Adafruit SleepyDog library are not needed any more. The L6470 Library of the PlatformIO Registry is still 1.0.0; do not install the driver libraries from the Registry.

**Who is affected.** Everyone who builds the firmware, mainly with the Arduino IDE.

**What to do.** Update the driver libraries in the Library Manager (PlatformIO takes them from the v1.2.0 tags on GitHub), and remove the two libraries that are not used. Details: [Libraries](compile-the-arduino-sketch.md#libraries).

## Updating from v2.0.0 {#from-v2-0-0}

v2.1.0 added the following. Read them, and then go through the items of this page.

- **Configuration files** from v2.0.0 are compatible. A STEP400 file made from the old template can contain the misspelled key `goUnitlTimeout`, whose value v2.0.0 ignored and v2.1.0 and later use. See [`goUnitlTimeout`](#go-until-timeout).
- **The microSD card.** The firmware reads `config.txt` first and then the alphabetically first `.json` file, and long file names can be used. `/saveConfig` and the browser configuration tool save the running configuration to the card. See [Configuration with a microSD card](../connections/microsd-card.md).
- **New messages.** `/setConfigName`, `/saveConfig`, and a fifth argument `configFilename` in the reply of `/getConfigName`. A client that checks the exact number of arguments of `/configName` must accept five.
- **The build.** The SD library is SdFat; the Arduino IDE sketch folder was removed from the repository, and `step-series-universal-firmware.zip` in the assets of each release is the sketch for the Arduino IDE. See [Building the firmware yourself](#building).

## Going back to v2.1.0 {#downgrade}

To go back from v2.2.0 to v2.1.0, build and upload v2.1.0 with the driver libraries **1.1.x**. The libraries 1.2.0 are for v2.2.0. Make sure that PlatformIO or the Library Manager installs 1.1.x. The entry `^1.1.0` of the `platformio.ini` of v2.1.0 can resolve to a later version (see [Libraries](#libraries)).

- **Configuration files.** The configuration saved by v2.2.0 has the same keys and the same applicable configuration version as v2.1.0, so v2.1.0 can read it. The Raw settings are saved as the same keys as the normal settings.
- **The `.tmp` file** that a failed save leaves is not a candidate for the configuration file in v2.1.0 either.
- **The hidden files** (`._name.json`) on a card copied on a Mac are candidates in v2.1.0 again, and can hide the valid `.json` files. Delete them or use `config.txt`. Also remember that the invalid-file behavior of v2.1.0 returns ([Invalid files are not applied](#invalid-files)), and that an exFAT card must not be used with the Arduino IDE build of v2.1.0 (it can delete the file).
- **Clients** written for v2.2.0 should be checked against the [Firmware changelog](changelog.md#v2-2-0): v2.1.0 sends `/booted` without `resetCause`, sends `T` / `F` for `/uvlo` and `/lowSpeedOptimizeThreshold`, and applies missing arguments as 0.
- **Electromagnetic brake.** With v2.1.0, the commands and the restart behave as before v2.2.0. See [Commands and states](#brake-commands) and [Restart, watchdog and CPU fault](#brake-restart).
