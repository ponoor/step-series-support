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
| <a id="information-configname"></a>`configName` | Configuration name | string | Default (firmware) / "" (template) |  | [`/setConfigName`](../reference/system-settings.md#setconfigname) | Configuration file name. Can be set freely. |
| <a id="information-configversion"></a>`configVersion` | Configuration version | version | 0.0 (firmware) / 1.2 (template) |  |  | Version number of the Config Tool. Unable to modify. |
| <a id="information-targetproduct"></a>`targetProduct` | Target product | string | STEP400: --- (firmware) / STEP400 (template); STEP800: --- (firmware) / STEP800 (template) |  |  | Name of the target product for the config file. Unable to modify. |

## network {#network}

| Key | Name | Type | Initial value | Range / Unit | Commands | Description |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="network-myip"></a>`myIp` | My IP address | ip | 10.0.0.100 |  |  | Set the IP address. if `ID adds to my IP` is checked, ID value added to this address becomes the actual IP address. For example if the IP address is set to `10.0.0.100` and ID switch is set to 1, `10.0.0.101` will be the actual address. Be cautious not the added value to exceed 254. |
| <a id="network-ismyipaddid"></a>`isMyIpAddId` | ID adds to my IP | bool | true |  |  | If the address with the ID added would be beyond .254 (ID 155 or more with the default 10.0.0.100), the ID is not added: the configured address is used and a warning is printed on USB serial. |
| <a id="network-destip"></a>`destIp` | Destination IP | ip | 10.0.0.10 |  | [`/setDestIp`](../reference/system-settings.md#setdestip) |  |
| <a id="network-dns"></a>`dns` | DNS | ip | 10.0.0.1 |  |  |  |
| <a id="network-gateway"></a>`gateway` | Gateway | ip | 10.0.0.1 |  |  |  |
| <a id="network-subnet"></a>`subnet` | Subnet mask | ip | 255.255.255.0 |  |  |  |
| <a id="network-inport"></a>`inPort` | Incoming port | int | 50000 |  |  | The port number that the device receives OSC messages. |
| <a id="network-outport"></a>`outPort` | Outgoing port | int | 50100 |  |  | The port number that the device send out OSC message. If `ID adds to Outgoing port` check box is checked, the ID value will be added to the port number. |
| <a id="network-isoutportaddid"></a>`isOutPortAddId` | ID adds to Outgoing port | bool | true |  |  | If the port with the ID added would be beyond 65535, the ID is not added: the configured port is used and a warning is printed on USB serial. |
| <a id="network-mac"></a>`mac` | MAC address | mac | STEP400: 60:95:CE:10:06:00 (firmware) / 60:95:CE:10:02:00 (template); STEP800: 60:95:CE:10:06:00 (firmware) / 60:95:CE:10:03:00 (template) |  |  | You can switch decimal and hexadecimal display by clicking the check box `Hex`. |
| <a id="network-ismacaddid"></a>`isMacAddId` | ID adds to MAC address | bool | true |  |  | When this check box is checked, the ID value will be added to the lowest byte of the MAC address. |
| <a id="network-bootedmsgenable"></a>`bootedMsgEnable` | Booted message enable | bool | true |  |  | Enables or disables the auto message [`/booted`](../reference/automatically-sent-messages.md#booted) on ethernet link establishment on start. |
| <a id="network-cansendmsgbeforedestip"></a>`canSendMsgBeforeDestIp` | Allow OSC reply before /setDestIp | bool | false |  |  | In initial state, the controller does not send OSC response until receiving `/setDestIp`. However if this check box is checked, the controller will sends out OSC message immediately after boot up. |
| <a id="network-reporterror"></a>`reportError` | Report errors | bool | true |  | [`/reportError`](../reference/system-settings.md#reporterror) |  |

## alarmAndReport {#alarmandreport}

| Key | Name | Type | Initial value | Range / Unit | Commands | Description |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="alarmandreport-reportbusy"></a>`reportBUSY` | Report BUSY (per motor) | bool | false |  | [`/enableBusyReport`](../reference/motor-driver-settings.md#enablebusyreport) |  |
| <a id="alarmandreport-reporthiz"></a>`reportHiZ` | Report HiZ (per motor) | bool | false |  | [`/enableHizReport`](../reference/motor-driver-settings.md#enablehizreport) |  |
| <a id="alarmandreport-reporthomeswstatus"></a>`reportHomeSwStatus` | Report HOME switch status (per motor) | bool | false |  | [`/enableHomeSwReport`](../reference/home-and-limit-sensors.md#enablehomeswreport) |  |
| <a id="alarmandreport-reportlimitswstatus"></a>`reportLimitSwStatus` | Report LIMIT switch status (per motor) (STEP400 only) | bool | false |  | [`/enableLimitSwReport`](../reference/home-and-limit-sensors.md#enablelimitswreport) |  |
| <a id="alarmandreport-reportdir"></a>`reportDir` | Report motor direction (per motor) | bool | false |  | [`/enableDirReport`](../reference/motor-driver-settings.md#enabledirreport) |  |
| <a id="alarmandreport-reportmotorstatus"></a>`reportMotorStatus` | Report Motor Status (per motor) | bool | false |  | [`/enableMotorStatusReport`](../reference/motor-driver-settings.md#enablemotorstatusreport) |  |
| <a id="alarmandreport-reportswevn"></a>`reportSwEvn` | Report HOME switch event (per motor) | bool | false |  | [`/enableSwEventReport`](../reference/home-and-limit-sensors.md#enablesweventreport) |  |
| <a id="alarmandreport-reportuvlo"></a>`reportUVLO` | Report undervoltage lockout (per motor) | bool | true |  | [`/enableUvloReport`](../reference/alarm-settings.md#enableuvloreport) |  |
| <a id="alarmandreport-reportthermalstatus"></a>`reportThermalStatus` | Report thermal status of driver chip (per motor) | bool | true |  | [`/enableThermalStatusReport`](../reference/alarm-settings.md#enablethermalstatusreport) |  |
| <a id="alarmandreport-reportocd"></a>`reportOCD` | per motor | bool | true |  | [`/enableOverCurrentReport`](../reference/alarm-settings.md#enableovercurrentreport) |  |
| <a id="alarmandreport-reportstall"></a>`reportStall` | Report motor stall detection (per motor) | bool | false |  | [`/enableStallReport`](../reference/alarm-settings.md#enablestallreport) |  |
| <a id="alarmandreport-reportpositioninterval"></a>`reportPositionInterval` | per motor | int | 0 | ms | [`/setPositionReportInterval`](../reference/motor-driver-settings.md#setpositionreportinterval) |  |
| <a id="alarmandreport-reportpositionlistinterval"></a>`reportPositionListInterval` |  | int | 0 | ms | [`/setPositionListReportInterval`](../reference/motor-driver-settings.md#setpositionlistreportinterval) |  |
| <a id="alarmandreport-octhreshold"></a>`OCThreshold` | Overcurrent threshold (per motor) | int | STEP400: 15; STEP800: 7 (firmware) / 15 (template) |  | [`/setOverCurrentThreshold`](../reference/alarm-settings.md#setovercurrentthreshold) |  |

## driverSettings {#driversettings}

| Key | Name | Type | Initial value | Range / Unit | Commands | Description |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="driversettings-homingatstartup"></a>`homingAtStartup` | Homing when the system starts (per motor) | bool | false |  |  | Proceed to homing movement soon after boot when this check box is checked.  With the electromagnetic brake enabled, the brake is released first, as [`/activate`](../reference/brake.md#activate) does, and the homing starts once the brake is released. **v2.2.0**: With the electromagnetic brake enabled, the brake is released first, as `/activate 1` does, and the homing starts once the brake is released. Before, the homing failed because the brake was engaged, and the timeout of the homing later sent a hard stop to the HiZ motor. |
| <a id="driversettings-homingdirection"></a>`homingDirection` | Homing Direction (per motor) | int | 0 (Reverse) |  | [`/setHomingDirection`](../reference/homing.md#sethomingdirection) |  |
| <a id="driversettings-homingspeed"></a>`homingSpeed` | Homing Speed (per motor) | float | 50 | step/s | [`/setHomingSpeed`](../reference/homing.md#sethomingspeed) |  |
| <a id="driversettings-homeswmode"></a>`homeSwMode` | Home switch won't cause HardStop (per motor) | bool | true |  | [`/setHomeSwMode`](../reference/home-and-limit-sensors.md#sethomeswmode) |  |
| <a id="driversettings-prohibitmotiononhomesw"></a>`prohibitMotionOnHomeSw` | Prohibit motions on HomeSw (per motor) | bool | false |  | [`/setProhibitMotionOnHomeSw`](../reference/alarm-settings.md#setprohibitmotiononhomesw) |  |
| <a id="driversettings-limitswmode"></a>`limitSwMode` | Limit switch won't cause HardStop (per motor) (STEP400 only) | bool | true |  | [`/setLimitSwMode`](../reference/home-and-limit-sensors.md#setlimitswmode) |  |
| <a id="driversettings-prohibitmotiononlimitsw"></a>`prohibitMotionOnLimitSw` | Prohibit motions on LimitSw (per motor) (STEP400 only) | bool | false |  | [`/setProhibitMotionOnLimitSw`](../reference/alarm-settings.md#setprohibitmotiononlimitsw) |  |
| <a id="driversettings-gountiltimeout"></a>`goUntilTimeout` | goUntil timeout duration (per motor) | int | 10000 | ms | [`/setGoUntilTimeout`](../reference/homing.md#setgountiltimeout) |  |
| <a id="driversettings-releaseswtimeout"></a>`releaseSwTimeout` | releaseSw timeout duration (per motor) | int | 10000 | ms | [`/setReleaseSwTimeout`](../reference/homing.md#setreleaseswtimeout) |  |
| <a id="driversettings-stepmode"></a>`stepMode` | Microstepping mode (per motor) | int | 7 |  | [`/setMicrostepMode`](../reference/motor-driver-settings.md#setmicrostepmode) |  |
| <a id="driversettings-iscurrentmode"></a>`isCurrentMode` | Current mode (per motor) (STEP400 only) | bool | false |  | [`/setVoltageMode`](../reference/voltage-and-current-mode-settings.md#setvoltagemode), [`/setCurrentMode`](../reference/voltage-and-current-mode-settings.md#setcurrentmode) |  |
| <a id="driversettings-slewrate"></a>`slewRate` | Slew rate (per motor) | int | STEP400: 5 (980V/us); STEP800: 2 (400V/us) | 0-5 (STEP400), 0-2 (STEP800) |  | Set the slew rate (steepness of rising) of motor control current from a motor driver in 6 steps for STEP400, 3 steps for STEP800. |
| <a id="driversettings-electromagnetbrakeenable"></a>`electromagnetBrakeEnable` | Electromagnetic brake enable (per motor) | bool | false |  | [`/enableElectromagnetBrake`](../reference/brake.md#enableelectromagnetbrake) |  |
| <a id="driversettings-braketransitionduration"></a>`brakeTransitionDuration` | Brake transition duration (per motor) | int | 100 | 0-65535 ms | [`/setBrakeTransitionDuration`](../reference/brake.md#setbraketransitionduration) |  |

## speedProfile {#speedprofile}

| Key | Name | Type | Initial value | Range / Unit | Commands | Description |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="speedprofile-acc"></a>`acc` | Acceleration (per motor) | float | 1000 (firmware) / 2000 (template) | step/s/s | [`/setAcc`](../reference/speed-profile.md#setacc), [`/setSpeedProfile`](../reference/speed-profile.md#setspeedprofile) |  |
| <a id="speedprofile-dec"></a>`dec` | Deceleration (per motor) | float | 1000 (firmware) / 2000 (template) | step/s/s | [`/setDec`](../reference/speed-profile.md#setdec), [`/setSpeedProfile`](../reference/speed-profile.md#setspeedprofile) |  |
| <a id="speedprofile-maxspeed"></a>`maxSpeed` | Max speed (per motor) | float | 650 (firmware) / 620 (template) | step/s | [`/setMaxSpeed`](../reference/speed-profile.md#setmaxspeed), [`/setSpeedProfile`](../reference/speed-profile.md#setspeedprofile) |  |
| <a id="speedprofile-fullstepspeed"></a>`fullStepSpeed` | Transit to fullstep threshold speed (per motor) | float | 15610 (firmware) / 15625 (template) | step/s | [`/setFullstepSpeed`](../reference/speed-profile.md#setfullstepspeed) |  |
| <a id="speedprofile-minspeed"></a>`minSpeed` | per motor | float | 0 | step/s | [`/setMinSpeed`](../reference/speed-profile.md#setminspeed) |  |

## voltageMode {#voltagemode}

| Key | Name | Type | Initial value | Range / Unit | Commands | Description |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="voltagemode-kval_hold"></a>`KVAL_HOLD` | KVAL_HOLD (per motor) | int | 0 |  | [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval), [`/setHoldKval`](../reference/voltage-and-current-mode-settings.md#setholdkval) | With the electromagnetic brake enabled, KVAL_HOLD is raised to at least half of KVAL_RUN whenever the motor is energized again; the raised value replaces the stored setting (so `/saveConfig` saves it) and is returned by [`/getKval`](../reference/voltage-and-current-mode-settings.md#getkval). |
| <a id="voltagemode-kval_run"></a>`KVAL_RUN` | KVAL_RUN (per motor) | int | 16 |  | [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval), [`/setRunKval`](../reference/voltage-and-current-mode-settings.md#setrunkval) |  |
| <a id="voltagemode-kval_acc"></a>`KVAL_ACC` | KVAL_ACC (per motor) | int | 16 |  | [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval), [`/setAccKval`](../reference/voltage-and-current-mode-settings.md#setacckval) |  |
| <a id="voltagemode-kval_dec"></a>`KVAL_DEC` | KVAL_DEC (per motor) | int | 16 |  | [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval), [`/setDecKval`](../reference/voltage-and-current-mode-settings.md#setdeckval) |  |
| <a id="voltagemode-int_speed"></a>`INT_SPEED` | INT_SPEED (per motor) | int | 1032 |  | [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) |  |
| <a id="voltagemode-st_slp"></a>`ST_SLP` | ST_SLP (per motor) | int | 25 |  | [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) |  |
| <a id="voltagemode-fn_slp_acc"></a>`FN_SLP_ACC` | FN_SLP_ACC (per motor) | int | 41 |  | [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) |  |
| <a id="voltagemode-fn_slp_dec"></a>`FN_SLP_DEC` | FN_SLP_DEC (per motor) | int | 41 |  | [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) |  |
| <a id="voltagemode-stall_th"></a>`STALL_TH` | STALL_TH (per motor) | int | STEP400: 31; STEP800: 127 |  | [`/setStallThreshold`](../reference/alarm-settings.md#setstallthreshold) |  |
| <a id="voltagemode-lowspeedoptimizeenable"></a>`lowSpeedOptimizeEnable` | per motor | bool | false |  | [`/enableLowSpeedOptimize`](../reference/motor-driver-settings.md#enablelowspeedoptimize) |  |
| <a id="voltagemode-lowspeedoptimize"></a>`lowSpeedOptimize` | lowSpeedOptimize (per motor) | float | 20 | step/s | [`/setLowSpeedOptimizeThreshold`](../reference/motor-driver-settings.md#setlowspeedoptimizethreshold) |  |

## currentMode {#currentmode}

| Key | Name | Type | Initial value | Range / Unit | Commands | Description |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="currentmode-tval_hold"></a>`TVAL_HOLD` | TVAL_HOLD (per motor) (STEP400 only) | int | 0 |  | [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval), [`/setHoldTval`](../reference/voltage-and-current-mode-settings.md#setholdtval) | With the electromagnetic brake enabled, TVAL_HOLD is raised to at least half of TVAL_RUN whenever the motor is energized again; the raised value replaces the stored setting (so `/saveConfig` saves it) and is returned by [`/getTval`](../reference/voltage-and-current-mode-settings.md#gettval). |
| <a id="currentmode-tval_run"></a>`TVAL_RUN` | TVAL_RUN (per motor) (STEP400 only) | int | 16 |  | [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval), [`/setRunTval`](../reference/voltage-and-current-mode-settings.md#setruntval) |  |
| <a id="currentmode-tval_acc"></a>`TVAL_ACC` | TVAL_ACC (per motor) (STEP400 only) | int | 16 |  | [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval), [`/setAccTval`](../reference/voltage-and-current-mode-settings.md#setacctval) |  |
| <a id="currentmode-tval_dec"></a>`TVAL_DEC` | TVAL_DEC (per motor) (STEP400 only) | int | 16 |  | [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval), [`/setDecTval`](../reference/voltage-and-current-mode-settings.md#setdectval) |  |
| <a id="currentmode-t_fast"></a>`T_FAST` | T_FAST (per motor) (STEP400 only) | int | 25 |  | [`/setDecayModeParam`](../reference/voltage-and-current-mode-settings.md#setdecaymodeparam) |  |
| <a id="currentmode-ton_min"></a>`TON_MIN` | TON_MIN (per motor) (STEP400 only) | int | 41 |  | [`/setDecayModeParam`](../reference/voltage-and-current-mode-settings.md#setdecaymodeparam) |  |
| <a id="currentmode-toff_min"></a>`TOFF_MIN` | TOFF_MIN (per motor) (STEP400 only) | int | 41 |  | [`/setDecayModeParam`](../reference/voltage-and-current-mode-settings.md#setdecaymodeparam) |  |

## servoMode {#servomode}

| Key | Name | Type | Initial value | Range / Unit | Commands | Description |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="servomode-kp"></a>`kP` | kP (per motor) | float | 0.06 |  | [`/setServoParam`](../reference/servo-mode_reference.md#setservoparam) |  |
| <a id="servomode-ki"></a>`kI` | kI (per motor) | float | 0 |  | [`/setServoParam`](../reference/servo-mode_reference.md#setservoparam) |  |
| <a id="servomode-kd"></a>`kD` | kD (per motor) | float | 0 |  | [`/setServoParam`](../reference/servo-mode_reference.md#setservoparam) |  |
