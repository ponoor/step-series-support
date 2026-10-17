---
title: Configuration items
lang: en
---

# Configuration items

<!-- This page is generated from spec/osc-commands.yaml by tools/generate.py. Do not edit it directly. -->

Items of the configuration file (JSON on the microSD card). The initial value is the one used when the file or the key is missing.

## information {#information}

| Key | Name | Type | Initial value | Range / Unit | Commands | Description |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="information-configname"></a>`configName` | Configuration name | string | Default (firmware) / "" (template) |  | [`/setConfigName`](../osc-command-references/system-settings_en.md#setconfigname) | Configuration file name. Can be set freely. |
| <a id="information-configversion"></a>`configVersion` | Configuration version | version | 0.0 (firmware) / 1.2 (template) |  |  | Version number of the Config Tool. Unable to modify. |
| <a id="information-targetproduct"></a>`targetProduct` | Target product | string | STEP400: --- (firmware) / STEP400 (template); STEP800: --- (firmware) / STEP800 (template) |  |  | Name of the target product for the config file. Unable to modify. |

## network {#network}

| Key | Name | Type | Initial value | Range / Unit | Commands | Description |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="network-myip"></a>`myIp` | My IP address | ip | 10.0.0.100 |  |  | Set the IP address. if `ID adds to my IP` is checked, ID value added to this address becomes the actual IP address. For example if the IP address is set to `10.0.0.100` and ID switch is set to 1, `10.0.0.101` will be the actual address. Be cautious not the added value to exceed 254. |
| <a id="network-ismyipaddid"></a>`isMyIpAddId` | ID adds to my IP | bool | true |  |  | If the address with the ID added would be beyond .254 (ID 155 or more with the default 10.0.0.100), the ID is not added: the configured address is used and a warning is printed on USB serial. |
| <a id="network-destip"></a>`destIp` | Destination IP | ip | 10.0.0.10 |  | [`/setDestIp`](../osc-command-references/system-settings_en.md#setdestip) |  |
| <a id="network-dns"></a>`dns` | DNS | ip | 10.0.0.1 |  |  |  |
| <a id="network-gateway"></a>`gateway` | Gateway | ip | 10.0.0.1 |  |  |  |
| <a id="network-subnet"></a>`subnet` | Subnet mask | ip | 255.255.255.0 |  |  |  |
| <a id="network-inport"></a>`inPort` | Incoming port | int | 50000 |  |  | The port number that the device receives OSC messages. |
| <a id="network-outport"></a>`outPort` | Outgoing port | int | 50100 |  |  | The port number that the device send out OSC message. If `ID adds to Outgoing port` check box is checked, the ID value will be added to the port number. |
| <a id="network-isoutportaddid"></a>`isOutPortAddId` | ID adds to Outgoing port | bool | true |  |  | If the port with the ID added would be beyond 65535, the ID is not added: the configured port is used and a warning is printed on USB serial. |
| <a id="network-mac"></a>`mac` | MAC address | mac | STEP400: 60:95:CE:10:06:00 (firmware) / 60:95:CE:10:02:00 (template); STEP800: 60:95:CE:10:06:00 (firmware) / 60:95:CE:10:03:00 (template) |  |  | You can switch decimal and hexadecimal display by clicking the check box `Hex`. |
| <a id="network-ismacaddid"></a>`isMacAddId` | ID adds to MAC address | bool | true |  |  | When this check box is checked, the ID value will be added to the lowest byte of the MAC address. |
| <a id="network-bootedmsgenable"></a>`bootedMsgEnable` | Booted message enable | bool | true |  |  | Enables or disables the auto message [`/booted`](../osc-command-references/automatically-sent-messages-from-step-400_en.md#booted) on ethernet link establishment on start. |
| <a id="network-cansendmsgbeforedestip"></a>`canSendMsgBeforeDestIp` | Allow OSC reply before /setDestIp | bool | false |  |  | In initial state, the controller does not send OSC response until receiving `/setDestIp`. However if this check box is checked, the controller will sends out OSC message immediately after boot up. |
| <a id="network-reporterror"></a>`reportError` | Report errors | bool | true |  | [`/reportError`](../osc-command-references/system-settings_en.md#reporterror) |  |

## alarmAndReport {#alarmandreport}

| Key | Name | Type | Initial value | Range / Unit | Commands | Description |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="alarmandreport-reportbusy"></a>`reportBUSY` | Report BUSY (per motor) | bool | false |  | [`/enableBusyReport`](../osc-command-references/motor-driver-settings_en.md#enablebusyreport) |  |
| <a id="alarmandreport-reporthiz"></a>`reportHiZ` | Report HiZ (per motor) | bool | false |  | [`/enableHizReport`](../osc-command-references/motor-driver-settings_en.md#enablehizreport) |  |
| <a id="alarmandreport-reporthomeswstatus"></a>`reportHomeSwStatus` | Report HOME switch status (per motor) | bool | false |  | [`/enableHomeSwReport`](../osc-command-references/home-and-limit-sensors_en.md#enablehomeswreport) |  |
| <a id="alarmandreport-reportlimitswstatus"></a>`reportLimitSwStatus` | Report LIMIT switch status (per motor) (STEP400 only) | bool | false |  | [`/enableLimitSwReport`](../osc-command-references/home-and-limit-sensors_en.md#enablelimitswreport) |  |
| <a id="alarmandreport-reportdir"></a>`reportDir` | Report motor direction (per motor) | bool | false |  | [`/enableDirReport`](../osc-command-references/motor-driver-settings_en.md#enabledirreport) |  |
| <a id="alarmandreport-reportmotorstatus"></a>`reportMotorStatus` | Report Motor Status (per motor) | bool | false |  | [`/enableMotorStatusReport`](../osc-command-references/motor-driver-settings_en.md#enablemotorstatusreport) |  |
| <a id="alarmandreport-reportswevn"></a>`reportSwEvn` | Report HOME switch event (per motor) | bool | false |  | [`/enableSwEventReport`](../osc-command-references/home-and-limit-sensors_en.md#enablesweventreport) |  |
| <a id="alarmandreport-reportuvlo"></a>`reportUVLO` | Report undervoltage lockout (per motor) | bool | true |  | [`/enableUvloReport`](../osc-command-references/alarm-settings_en.md#enableuvloreport) |  |
| <a id="alarmandreport-reportthermalstatus"></a>`reportThermalStatus` | Report thermal status of driver chip (per motor) | bool | true |  | [`/enableThermalStatusReport`](../osc-command-references/alarm-settings_en.md#enablethermalstatusreport) |  |
| <a id="alarmandreport-reportocd"></a>`reportOCD` | per motor | bool | true |  | [`/enableOverCurrentReport`](../osc-command-references/alarm-settings_en.md#enableovercurrentreport) |  |
| <a id="alarmandreport-reportstall"></a>`reportStall` | Report motor stall detection (per motor) | bool | false |  | [`/enableStallReport`](../osc-command-references/alarm-settings_en.md#enablestallreport) |  |
| <a id="alarmandreport-reportpositioninterval"></a>`reportPositionInterval` | per motor | int | 0 | ms | [`/setPositionReportInterval`](../osc-command-references/motor-driver-settings_en.md#setpositionreportinterval) |  |
| <a id="alarmandreport-reportpositionlistinterval"></a>`reportPositionListInterval` |  | int | 0 | ms | [`/setPositionListReportInterval`](../osc-command-references/motor-driver-settings_en.md#setpositionlistreportinterval) |  |
| <a id="alarmandreport-octhreshold"></a>`OCThreshold` | Overcurrent threshold (per motor) | int | STEP400: 15; STEP800: 7 (firmware) / 15 (template) |  | [`/setOverCurrentThreshold`](../osc-command-references/alarm-settings_en.md#setovercurrentthreshold) |  |

## driverSettings {#driversettings}

| Key | Name | Type | Initial value | Range / Unit | Commands | Description |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="driversettings-homingatstartup"></a>`homingAtStartup` | Homing when the system starts (per motor) | bool | false |  |  | Proceed to homing movement soon after boot when this check box is checked.  With the electromagnetic brake enabled, the brake is released first, as [`/activate`](../osc-command-references/brake_en.md#activate) does, and the homing starts once the brake is released. (Before 2.2.0 the homing failed because the brake was engaged.) |
| <a id="driversettings-homingdirection"></a>`homingDirection` | Homing Direction (per motor) | int | 0 (Reverse) |  | [`/setHomingDirection`](../osc-command-references/homing_en.md#sethomingdirection) |  |
| <a id="driversettings-homingspeed"></a>`homingSpeed` | Homing Speed (per motor) | float | 50 | step/s | [`/setHomingSpeed`](../osc-command-references/homing_en.md#sethomingspeed) |  |
| <a id="driversettings-homeswmode"></a>`homeSwMode` | Home switch won't cause HardStop (per motor) | bool | true |  | [`/setHomeSwMode`](../osc-command-references/home-and-limit-sensors_en.md#sethomeswmode) |  |
| <a id="driversettings-prohibitmotiononhomesw"></a>`prohibitMotionOnHomeSw` | Prohibit motions on HomeSw (per motor) | bool | false |  | [`/setProhibitMotionOnHomeSw`](../osc-command-references/alarm-settings_en.md#setprohibitmotiononhomesw) |  |
| <a id="driversettings-limitswmode"></a>`limitSwMode` | Limit switch won't cause HardStop (per motor) (STEP400 only) | bool | true |  | [`/setLimitSwMode`](../osc-command-references/home-and-limit-sensors_en.md#setlimitswmode) |  |
| <a id="driversettings-prohibitmotiononlimitsw"></a>`prohibitMotionOnLimitSw` | Prohibit motions on LimitSw (per motor) (STEP400 only) | bool | false |  | [`/setProhibitMotionOnLimitSw`](../osc-command-references/alarm-settings_en.md#setprohibitmotiononlimitsw) |  |
| <a id="driversettings-gountiltimeout"></a>`goUntilTimeout` | goUntil timeout duration (per motor) | int | 10000 | ms | [`/setGoUntilTimeout`](../osc-command-references/homing_en.md#setgountiltimeout) |  |
| <a id="driversettings-releaseswtimeout"></a>`releaseSwTimeout` | releaseSw timeout duration (per motor) | int | 10000 | ms | [`/setReleaseSwTimeout`](../osc-command-references/homing_en.md#setreleaseswtimeout) |  |
| <a id="driversettings-stepmode"></a>`stepMode` | Microstepping mode (per motor) | int | 7 |  | [`/setMicrostepMode`](../osc-command-references/motor-driver-settings_en.md#setmicrostepmode) |  |
| <a id="driversettings-iscurrentmode"></a>`isCurrentMode` | Current mode (per motor) (STEP400 only) | bool | false |  | [`/setVoltageMode`](../osc-command-references/voltage-and-current-mode-settings_en.md#setvoltagemode), [`/setCurrentMode`](../osc-command-references/voltage-and-current-mode-settings_en.md#setcurrentmode) |  |
| <a id="driversettings-slewrate"></a>`slewRate` | Slew rate (per motor) | int | STEP400: 5 (980V/us); STEP800: 2 (400V/us) | 0-5 (STEP400), 0-2 (STEP800) |  | Set the slew rate (steepness of rising) of motor control current from a motor driver in 6 steps for STEP400, 3 steps for STEP800. |
| <a id="driversettings-electromagnetbrakeenable"></a>`electromagnetBrakeEnable` | Electromagnetic brake enable (per motor) | bool | false |  | [`/enableElectromagnetBrake`](../osc-command-references/brake_en.md#enableelectromagnetbrake) |  |
| <a id="driversettings-braketransitionduration"></a>`brakeTransitionDuration` | Brake transition duration (per motor) | int | 100 | 0-65535 ms | [`/setBrakeTransitionDuration`](../osc-command-references/brake_en.md#setbraketransitionduration) |  |

## speedProfile {#speedprofile}

| Key | Name | Type | Initial value | Range / Unit | Commands | Description |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="speedprofile-acc"></a>`acc` | Acceleration (per motor) | float | 1000 (firmware) / 2000 (template) | step/s/s | [`/setAcc`](../osc-command-references/speed-profile_en.md#setacc), [`/setSpeedProfile`](../osc-command-references/speed-profile_en.md#setspeedprofile) |  |
| <a id="speedprofile-dec"></a>`dec` | Deceleration (per motor) | float | 1000 (firmware) / 2000 (template) | step/s/s | [`/setDec`](../osc-command-references/speed-profile_en.md#setdec), [`/setSpeedProfile`](../osc-command-references/speed-profile_en.md#setspeedprofile) |  |
| <a id="speedprofile-maxspeed"></a>`maxSpeed` | Max speed (per motor) | float | 650 (firmware) / 620 (template) | step/s | [`/setMaxSpeed`](../osc-command-references/speed-profile_en.md#setmaxspeed), [`/setSpeedProfile`](../osc-command-references/speed-profile_en.md#setspeedprofile) |  |
| <a id="speedprofile-fullstepspeed"></a>`fullStepSpeed` | Transit to fullstep threshold speed (per motor) | float | 15610 (firmware) / 15625 (template) | step/s | [`/setFullstepSpeed`](../osc-command-references/speed-profile_en.md#setfullstepspeed) |  |
| <a id="speedprofile-minspeed"></a>`minSpeed` | per motor | float | 0 | step/s | [`/setMinSpeed`](../osc-command-references/speed-profile_en.md#setminspeed) |  |

## voltageMode {#voltagemode}

| Key | Name | Type | Initial value | Range / Unit | Commands | Description |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="voltagemode-kval_hold"></a>`KVAL_HOLD` | KVAL_HOLD (per motor) | int | 0 |  | [`/setKval`](../osc-command-references/voltage-and-current-mode-settings_en.md#setkval), [`/setHoldKval`](../osc-command-references/voltage-and-current-mode-settings_en.md#setholdkval) | With the electromagnetic brake enabled, KVAL_HOLD is raised to at least half of KVAL_RUN whenever the motor is energized again; the raised value is also returned by [`/getKval`](../osc-command-references/voltage-and-current-mode-settings_en.md#getkval). |
| <a id="voltagemode-kval_run"></a>`KVAL_RUN` | KVAL_RUN (per motor) | int | 16 |  | [`/setKval`](../osc-command-references/voltage-and-current-mode-settings_en.md#setkval), [`/setRunKval`](../osc-command-references/voltage-and-current-mode-settings_en.md#setrunkval) |  |
| <a id="voltagemode-kval_acc"></a>`KVAL_ACC` | KVAL_ACC (per motor) | int | 16 |  | [`/setKval`](../osc-command-references/voltage-and-current-mode-settings_en.md#setkval), [`/setAccKval`](../osc-command-references/voltage-and-current-mode-settings_en.md#setacckval) |  |
| <a id="voltagemode-kval_dec"></a>`KVAL_DEC` | KVAL_DEC (per motor) | int | 16 |  | [`/setKval`](../osc-command-references/voltage-and-current-mode-settings_en.md#setkval), [`/setDecKval`](../osc-command-references/voltage-and-current-mode-settings_en.md#setdeckval) |  |
| <a id="voltagemode-int_speed"></a>`INT_SPEED` | INT_SPEED (per motor) | int | 1032 |  | [`/setBemfParam`](../osc-command-references/voltage-and-current-mode-settings_en.md#setbemfparam) |  |
| <a id="voltagemode-st_slp"></a>`ST_SLP` | ST_SLP (per motor) | int | 25 |  | [`/setBemfParam`](../osc-command-references/voltage-and-current-mode-settings_en.md#setbemfparam) |  |
| <a id="voltagemode-fn_slp_acc"></a>`FN_SLP_ACC` | FN_SLP_ACC (per motor) | int | 41 |  | [`/setBemfParam`](../osc-command-references/voltage-and-current-mode-settings_en.md#setbemfparam) |  |
| <a id="voltagemode-fn_slp_dec"></a>`FN_SLP_DEC` | FN_SLP_DEC (per motor) | int | 41 |  | [`/setBemfParam`](../osc-command-references/voltage-and-current-mode-settings_en.md#setbemfparam) |  |
| <a id="voltagemode-stall_th"></a>`STALL_TH` | STALL_TH (per motor) | int | STEP400: 31; STEP800: 127 |  | [`/setStallThreshold`](../osc-command-references/alarm-settings_en.md#setstallthreshold) |  |
| <a id="voltagemode-lowspeedoptimizeenable"></a>`lowSpeedOptimizeEnable` | per motor | bool | false |  | [`/enableLowSpeedOptimize`](../osc-command-references/motor-driver-settings_en.md#enablelowspeedoptimize) |  |
| <a id="voltagemode-lowspeedoptimize"></a>`lowSpeedOptimize` | lowSpeedOptimize (per motor) | float | 20 | step/s | [`/setLowSpeedOptimizeThreshold`](../osc-command-references/motor-driver-settings_en.md#setlowspeedoptimizethreshold) |  |

## currentMode {#currentmode}

| Key | Name | Type | Initial value | Range / Unit | Commands | Description |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="currentmode-tval_hold"></a>`TVAL_HOLD` | TVAL_HOLD (per motor) (STEP400 only) | int | 0 |  | [`/setTval`](../osc-command-references/voltage-and-current-mode-settings_en.md#settval), [`/setHoldTval`](../osc-command-references/voltage-and-current-mode-settings_en.md#setholdtval) | With the electromagnetic brake enabled, TVAL_HOLD is raised to at least half of TVAL_RUN whenever the motor is energized again; the raised value is also returned by [`/getTval`](../osc-command-references/voltage-and-current-mode-settings_en.md#gettval). |
| <a id="currentmode-tval_run"></a>`TVAL_RUN` | TVAL_RUN (per motor) (STEP400 only) | int | 16 |  | [`/setTval`](../osc-command-references/voltage-and-current-mode-settings_en.md#settval), [`/setRunTval`](../osc-command-references/voltage-and-current-mode-settings_en.md#setruntval) |  |
| <a id="currentmode-tval_acc"></a>`TVAL_ACC` | TVAL_ACC (per motor) (STEP400 only) | int | 16 |  | [`/setTval`](../osc-command-references/voltage-and-current-mode-settings_en.md#settval), [`/setAccTval`](../osc-command-references/voltage-and-current-mode-settings_en.md#setacctval) |  |
| <a id="currentmode-tval_dec"></a>`TVAL_DEC` | TVAL_DEC (per motor) (STEP400 only) | int | 16 |  | [`/setTval`](../osc-command-references/voltage-and-current-mode-settings_en.md#settval), [`/setDecTval`](../osc-command-references/voltage-and-current-mode-settings_en.md#setdectval) |  |
| <a id="currentmode-t_fast"></a>`T_FAST` | T_FAST (per motor) (STEP400 only) | int | 25 |  | [`/setDecayModeParam`](../osc-command-references/voltage-and-current-mode-settings_en.md#setdecaymodeparam) |  |
| <a id="currentmode-ton_min"></a>`TON_MIN` | TON_MIN (per motor) (STEP400 only) | int | 41 |  | [`/setDecayModeParam`](../osc-command-references/voltage-and-current-mode-settings_en.md#setdecaymodeparam) |  |
| <a id="currentmode-toff_min"></a>`TOFF_MIN` | TOFF_MIN (per motor) (STEP400 only) | int | 41 |  | [`/setDecayModeParam`](../osc-command-references/voltage-and-current-mode-settings_en.md#setdecaymodeparam) |  |

## servoMode {#servomode}

| Key | Name | Type | Initial value | Range / Unit | Commands | Description |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="servomode-kp"></a>`kP` | kP (per motor) | float | 0.06 |  | [`/setServoParam`](../osc-command-references/servo-mode_reference_en.md#setservoparam) |  |
| <a id="servomode-ki"></a>`kI` | kI (per motor) | float | 0 |  | [`/setServoParam`](../osc-command-references/servo-mode_reference_en.md#setservoparam) |  |
| <a id="servomode-kd"></a>`kD` | kD (per motor) | float | 0 |  | [`/setServoParam`](../osc-command-references/servo-mode_reference_en.md#setservoparam) |  |
