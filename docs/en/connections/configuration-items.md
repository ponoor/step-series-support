---
title: Configuration items
lang: en
---

# Configuration items

<!-- This page is generated from spec/osc-commands.yaml by tools/generate.py. Do not edit it directly. -->

Items of the configuration file (JSON on the microSD card). The initial value is the one used when the file or the key is missing.

## information {#information}

| Key / Name | Type / Initial value | Description |
| --- | --- | --- |
| <a id="information-configname"></a>`configName`<br>Configuration name | string<br>Default (firmware) / "" (template) | Configuration file name. Can be set freely. Commands: [`/setConfigName`](../reference/system-settings.md#setconfigname) |
| <a id="information-configversion"></a>`configVersion`<br>Configuration version | version<br>0.0 (firmware) / 1.2 (template) | Version of the configuration file format. A `.json` file without it is not accepted (`config.txt` is accepted without it). Unable to modify. |
| <a id="information-targetproduct"></a>`targetProduct`<br>Target product | string<br>STEP400: --- (firmware) / STEP400 (template)<br>STEP800: --- (firmware) / STEP800 (template) | Name of the target product for the config file. Unable to modify. |

## network {#network}

| Key / Name | Type / Initial value | Description |
| --- | --- | --- |
| <a id="network-myip"></a>`myIp`<br>My IP address | ip<br>10.0.0.100 | Set the IP address. if `ID adds to my IP` is checked, ID value added to this address becomes the actual IP address. For example if the IP address is set to `10.0.0.100` and ID switch is set to 1, `10.0.0.101` will be the actual address. Be cautious not the added value to exceed 254. |
| <a id="network-ismyipaddid"></a>`isMyIpAddId`<br>ID adds to my IP | bool<br>true | If the address with the ID added would be beyond .254 (ID 155 or more with the default 10.0.0.100), the ID is not added: the configured address is used and a warning is printed on USB serial. |
| <a id="network-destip"></a>`destIp`<br>Destination IP | ip<br>10.0.0.10 | Commands: [`/setDestIp`](../reference/system-settings.md#setdestip) |
| <a id="network-dns"></a>`dns`<br>DNS | ip<br>10.0.0.1 |  |
| <a id="network-gateway"></a>`gateway`<br>Gateway | ip<br>10.0.0.1 |  |
| <a id="network-subnet"></a>`subnet`<br>Subnet mask | ip<br>255.255.255.0 |  |
| <a id="network-inport"></a>`inPort`<br>Incoming port | int<br>50000 | The port number that the device receives OSC messages. |
| <a id="network-outport"></a>`outPort`<br>Outgoing port | int<br>50100 | The port number that the device send out OSC message. If `ID adds to Outgoing port` check box is checked, the ID value will be added to the port number. |
| <a id="network-isoutportaddid"></a>`isOutPortAddId`<br>ID adds to Outgoing port | bool<br>true | If the port with the ID added would be beyond 65535, the ID is not added: the configured port is used and a warning is printed on USB serial. |
| <a id="network-mac"></a>`mac`<br>MAC address | mac<br>STEP400: 60:95:CE:10:06:00 (firmware) / 60:95:CE:10:02:00 (template)<br>STEP800: 60:95:CE:10:06:00 (firmware) / 60:95:CE:10:03:00 (template) | You can switch decimal and hexadecimal display by clicking the check box `Hex`. |
| <a id="network-ismacaddid"></a>`isMacAddId`<br>ID adds to MAC address | bool<br>true | When this check box is checked, the ID value will be added to the lowest byte of the MAC address. |
| <a id="network-bootedmsgenable"></a>`bootedMsgEnable`<br>Booted message enable | bool<br>true | Enables or disables the auto message [`/booted`](../reference/automatically-sent-messages.md#booted) on ethernet link establishment on start. |
| <a id="network-cansendmsgbeforedestip"></a>`canSendMsgBeforeDestIp`<br>Allow OSC reply before /setDestIp | bool<br>false | In initial state, the controller does not send OSC response until receiving `/setDestIp`. However if this check box is checked, the controller will sends out OSC message immediately after boot up.  Known issue in v2.2.0: the running board keeps "`/setDestIp` has been received" in the same value as this setting. After `/setDestIp` was received, saving the configuration ([`/saveConfig`](../reference/system-settings.md#saveconfig), or saving with the browser configuration tool) writes `true` to the card. When the browser configuration tool writes `false`, the running value also becomes `false`, and the board sends no reply until `/setDestIp` is sent again. Workaround: send `/setDestIp` again after saving, and check the value in the saved file. |
| <a id="network-reporterror"></a>`reportError`<br>Report errors | bool<br>true | Commands: [`/reportError`](../reference/system-settings.md#reporterror) |

## alarmAndReport {#alarmandreport}

| Key / Name | Type / Initial value | Description |
| --- | --- | --- |
| <a id="alarmandreport-reportbusy"></a>`reportBUSY`<br>Report BUSY (per motor) | bool<br>false | Commands: [`/enableBusyReport`](../reference/motor-driver-settings.md#enablebusyreport) |
| <a id="alarmandreport-reporthiz"></a>`reportHiZ`<br>Report HiZ (per motor) | bool<br>false | Commands: [`/enableHizReport`](../reference/motor-driver-settings.md#enablehizreport) |
| <a id="alarmandreport-reporthomeswstatus"></a>`reportHomeSwStatus`<br>Report HOME switch status (per motor) | bool<br>false | Commands: [`/enableHomeSwReport`](../reference/home-and-limit-sensors.md#enablehomeswreport) |
| <a id="alarmandreport-reportlimitswstatus"></a>`reportLimitSwStatus`<br>Report LIMIT switch status (per motor) (STEP400 only) | bool<br>false | Commands: [`/enableLimitSwReport`](../reference/home-and-limit-sensors.md#enablelimitswreport) |
| <a id="alarmandreport-reportdir"></a>`reportDir`<br>Report motor direction (per motor) | bool<br>false | Commands: [`/enableDirReport`](../reference/motor-driver-settings.md#enabledirreport) |
| <a id="alarmandreport-reportmotorstatus"></a>`reportMotorStatus`<br>Report Motor Status (per motor) | bool<br>false | Commands: [`/enableMotorStatusReport`](../reference/motor-driver-settings.md#enablemotorstatusreport) |
| <a id="alarmandreport-reportswevn"></a>`reportSwEvn`<br>Report HOME switch event (per motor) | bool<br>false | Commands: [`/enableSwEventReport`](../reference/home-and-limit-sensors.md#enablesweventreport) |
| <a id="alarmandreport-reportuvlo"></a>`reportUVLO`<br>Report undervoltage lockout (per motor) | bool<br>true | Commands: [`/enableUvloReport`](../reference/alarm-settings.md#enableuvloreport) |
| <a id="alarmandreport-reportthermalstatus"></a>`reportThermalStatus`<br>Report thermal status of driver chip (per motor) | bool<br>true | Commands: [`/enableThermalStatusReport`](../reference/alarm-settings.md#enablethermalstatusreport) |
| <a id="alarmandreport-reportocd"></a>`reportOCD`<br>Report overcurrent detection (per motor) | bool<br>true | Commands: [`/enableOverCurrentReport`](../reference/alarm-settings.md#enableovercurrentreport) |
| <a id="alarmandreport-reportstall"></a>`reportStall`<br>Report motor stall detection (per motor) | bool<br>false | Stall detection lets the driver detect, from the motor current, that the motor can no longer turn against the load. Find a threshold ([`/setStallThreshold`](../reference/alarm-settings.md#setstallthreshold)) as close as possible to, and slightly above, the current actually flowing. A small loss of steps cannot be detected, but a large position error may be. Commands: [`/enableStallReport`](../reference/alarm-settings.md#enablestallreport) |
| <a id="alarmandreport-reportpositioninterval"></a>`reportPositionInterval`<br>Report position interval (per motor) | int<br>0 | Range: 0-65535 ms. The interval of the position report ([`/position`](../reference/automatically-sent-messages.md#position)) of each motor. 0 turns the report off.  The value is not range-checked when the configuration file is read (or written over USB serial). An out-of-range value wraps around: the value after the maximum is 0 (65536 becomes 0, which turns the report off; 65537 becomes 1; -1 becomes 65535). [`/setPositionReportInterval`](../reference/motor-driver-settings.md#setpositionreportinterval) rejects a value above 65535 with `CommandIgnored`, and a negative value turns the report off. Commands: [`/setPositionReportInterval`](../reference/motor-driver-settings.md#setpositionreportinterval) |
| <a id="alarmandreport-reportpositionlistinterval"></a>`reportPositionListInterval`<br>Report position list interval | int<br>0 | Range: 0-65535 ms. The interval of the position list report ([`/positionList`](../reference/automatically-sent-messages.md#positionlist)). 0 turns the report off. When it is greater than 0, the position report of each motor ([`/position`](../reference/automatically-sent-messages.md#position)) is turned off.  The value is not range-checked when the configuration file is read (or written over USB serial). An out-of-range value wraps around: the value after the maximum is 0 (65536 becomes 0, 65537 becomes 1, and -1 becomes 65535). [`/setPositionListReportInterval`](../reference/motor-driver-settings.md#setpositionlistreportinterval) rejects a value above 65535 with `CommandIgnored`. Commands: [`/setPositionListReportInterval`](../reference/motor-driver-settings.md#setpositionlistreportinterval) |
| <a id="alarmandreport-octhreshold"></a>`OCThreshold`<br>Overcurrent threshold (per motor) | int<br>STEP400: 15 (5A)<br>STEP800: 7 (3A) | Commands: [`/setOverCurrentThreshold`](../reference/alarm-settings.md#setovercurrentthreshold) |

## driverSettings {#driversettings}

| Key / Name | Type / Initial value | Description |
| --- | --- | --- |
| <a id="driversettings-homingatstartup"></a>`homingAtStartup`<br>Homing when the system starts (per motor) | bool<br>false | Proceed to homing movement soon after boot when this check box is checked.  With the electromagnetic brake enabled, the brake is released first, as [`/activate`](../reference/brake.md#activate) does, and the homing starts once the brake is released. **v2.2.0**: With the electromagnetic brake enabled, the brake is released first, as `/activate 1` does, and the homing starts once the brake is released. Before, the homing failed because the brake was engaged, and the timeout of the homing later sent a hard stop to the HiZ motor. |
| <a id="driversettings-homingdirection"></a>`homingDirection`<br>Homing Direction (per motor) | int<br>0 (Reverse) | Values: 1: Forward, 0: Reverse. Commands: [`/setHomingDirection`](../reference/homing.md#sethomingdirection) |
| <a id="driversettings-homingspeed"></a>`homingSpeed`<br>Homing Speed (per motor) | float<br>50 | Unit: step/s. Commands: [`/setHomingSpeed`](../reference/homing.md#sethomingspeed) |
| <a id="driversettings-homeswmode"></a>`homeSwMode`<br>Home switch won't cause HardStop (per motor) | bool<br>true | Commands: [`/setHomeSwMode`](../reference/home-and-limit-sensors.md#sethomeswmode) |
| <a id="driversettings-prohibitmotiononhomesw"></a>`prohibitMotionOnHomeSw`<br>Prohibit motions on HomeSw (per motor) | bool<br>false | Commands: [`/setProhibitMotionOnHomeSw`](../reference/alarm-settings.md#setprohibitmotiononhomesw) |
| <a id="driversettings-limitswmode"></a>`limitSwMode`<br>Limit switch won't cause HardStop (per motor) (STEP400 only) | bool<br>true | Commands: [`/setLimitSwMode`](../reference/home-and-limit-sensors.md#setlimitswmode) |
| <a id="driversettings-prohibitmotiononlimitsw"></a>`prohibitMotionOnLimitSw`<br>Prohibit motions on LimitSw (per motor) (STEP400 only) | bool<br>false | Commands: [`/setProhibitMotionOnLimitSw`](../reference/alarm-settings.md#setprohibitmotiononlimitsw) |
| <a id="driversettings-gountiltimeout"></a>`goUntilTimeout`<br>goUntil timeout duration (per motor) | int<br>10000 | Unit: ms. Commands: [`/setGoUntilTimeout`](../reference/homing.md#setgountiltimeout) |
| <a id="driversettings-releaseswtimeout"></a>`releaseSwTimeout`<br>releaseSw timeout duration (per motor) | int<br>10000 | Unit: ms. Commands: [`/setReleaseSwTimeout`](../reference/homing.md#setreleaseswtimeout) |
| <a id="driversettings-stepmode"></a>`stepMode`<br>Microstepping mode (per motor) | int<br>7 | Commands: [`/setMicrostepMode`](../reference/motor-driver-settings.md#setmicrostepmode) |
| <a id="driversettings-iscurrentmode"></a>`isCurrentMode`<br>Current mode (per motor) (STEP400 only) | bool<br>false | Commands: [`/setVoltageMode`](../reference/voltage-and-current-mode-settings.md#setvoltagemode), [`/setCurrentMode`](../reference/voltage-and-current-mode-settings.md#setcurrentmode) |
| <a id="driversettings-slewrate"></a>`slewRate`<br>Slew rate (per motor) | int<br>STEP400: 5 (980V/us)<br>STEP800: 2 (530V/us) | Range: 0-5 (STEP400), 0-2 (STEP800)<br>STEP400: 0: 114V/us, 1: 220V/us, 2: 400V/us, 3: 520V/us, 4: 790V/us, 5: 980V/us<br>STEP800: 0: 180V/us, 1: 290V/us, 2: 530V/us. Set the slew rate (steepness of rising) of motor control current from a motor driver in 6 steps for STEP400, 3 steps for STEP800.  A value outside the range in the configuration file is not rejected: it is limited to the range (a negative value becomes 0, a larger one the highest value). |
| <a id="driversettings-electromagnetbrakeenable"></a>`electromagnetBrakeEnable`<br>Electromagnetic brake enable (per motor) | bool<br>false | Commands: [`/enableElectromagnetBrake`](../reference/brake.md#enableelectromagnetbrake) |
| <a id="driversettings-braketransitionduration"></a>`brakeTransitionDuration`<br>Brake transition duration (per motor) | int<br>100 | Range: 0-65535 ms. The time to wait for the brake to release or to engage. See [`/setBrakeTransitionDuration`](../reference/brake.md#setbraketransitionduration).  The value is not range-checked when the configuration file is read (or written over USB serial). An out-of-range value wraps around: the value after the maximum is 0 (65536 becomes 0, 65537 becomes 1, and -1 becomes 65535). [`/setBrakeTransitionDuration`](../reference/brake.md#setbraketransitionduration) rejects such a value with `CommandIgnored`. Commands: [`/setBrakeTransitionDuration`](../reference/brake.md#setbraketransitionduration) |

## speedProfile {#speedprofile}

| Key / Name | Type / Initial value | Description |
| --- | --- | --- |
| <a id="speedprofile-acc"></a>`acc`<br>Acceleration (per motor) | float<br>1000 (firmware) / 2000 (template) | Unit: step/s/s. Commands: [`/setAcc`](../reference/speed-profile.md#setacc), [`/setSpeedProfile`](../reference/speed-profile.md#setspeedprofile) |
| <a id="speedprofile-dec"></a>`dec`<br>Deceleration (per motor) | float<br>1000 (firmware) / 2000 (template) | Unit: step/s/s. Commands: [`/setDec`](../reference/speed-profile.md#setdec), [`/setSpeedProfile`](../reference/speed-profile.md#setspeedprofile) |
| <a id="speedprofile-maxspeed"></a>`maxSpeed`<br>Max speed (per motor) | float<br>650 (firmware) / 620 (template) | Unit: step/s. Commands: [`/setMaxSpeed`](../reference/speed-profile.md#setmaxspeed), [`/setSpeedProfile`](../reference/speed-profile.md#setspeedprofile) |
| <a id="speedprofile-fullstepspeed"></a>`fullStepSpeed`<br>Transit to fullstep threshold speed (per motor) | float<br>15610 (firmware) / 15625 (template) | Unit: step/s. Commands: [`/setFullstepSpeed`](../reference/speed-profile.md#setfullstepspeed) |
| <a id="speedprofile-minspeed"></a>`minSpeed`<br>Minimum speed (per motor) | float<br>0 | Unit: step/s. Commands: [`/setMinSpeed`](../reference/speed-profile.md#setminspeed) |

## voltageMode {#voltagemode}

| Key / Name | Type / Initial value | Description |
| --- | --- | --- |
| <a id="voltagemode-kval_hold"></a>`KVAL_HOLD`<br>KVAL_HOLD (per motor) | int<br>0 | With the electromagnetic brake enabled, KVAL_HOLD is raised to at least half of KVAL_RUN whenever the motor is energized again; the raised value replaces the stored setting (so `/saveConfig` saves it) and is returned by [`/getKval`](../reference/voltage-and-current-mode-settings.md#getkval). Commands: [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval), [`/setHoldKval`](../reference/voltage-and-current-mode-settings.md#setholdkval) |
| <a id="voltagemode-kval_run"></a>`KVAL_RUN`<br>KVAL_RUN (per motor) | int<br>16 | Commands: [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval), [`/setRunKval`](../reference/voltage-and-current-mode-settings.md#setrunkval) |
| <a id="voltagemode-kval_acc"></a>`KVAL_ACC`<br>KVAL_ACC (per motor) | int<br>16 | Commands: [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval), [`/setAccKval`](../reference/voltage-and-current-mode-settings.md#setacckval) |
| <a id="voltagemode-kval_dec"></a>`KVAL_DEC`<br>KVAL_DEC (per motor) | int<br>16 | Commands: [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval), [`/setDecKval`](../reference/voltage-and-current-mode-settings.md#setdeckval) |
| <a id="voltagemode-int_speed"></a>`INT_SPEED`<br>INT_SPEED (per motor) | int<br>1032 | Commands: [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) |
| <a id="voltagemode-st_slp"></a>`ST_SLP`<br>ST_SLP (per motor) | int<br>25 | Commands: [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) |
| <a id="voltagemode-fn_slp_acc"></a>`FN_SLP_ACC`<br>FN_SLP_ACC (per motor) | int<br>41 | Commands: [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) |
| <a id="voltagemode-fn_slp_dec"></a>`FN_SLP_DEC`<br>FN_SLP_DEC (per motor) | int<br>41 | Commands: [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) |
| <a id="voltagemode-stall_th"></a>`STALL_TH`<br>STALL_TH (per motor) | int<br>STEP400: 31 (10A)<br>STEP800: 127 (4A) | Commands: [`/setStallThreshold`](../reference/alarm-settings.md#setstallthreshold) |
| <a id="voltagemode-lowspeedoptimizeenable"></a>`lowSpeedOptimizeEnable`<br>Low speed optimize enable (per motor) | bool<br>false | Commands: [`/enableLowSpeedOptimize`](../reference/motor-driver-settings.md#enablelowspeedoptimize) |
| <a id="voltagemode-lowspeedoptimize"></a>`lowSpeedOptimize`<br>lowSpeedOptimize (per motor) | float<br>20 | Unit: step/s. Commands: [`/setLowSpeedOptimizeThreshold`](../reference/motor-driver-settings.md#setlowspeedoptimizethreshold) |

## currentMode {#currentmode}

| Key / Name | Type / Initial value | Description |
| --- | --- | --- |
| <a id="currentmode-tval_hold"></a>`TVAL_HOLD`<br>TVAL_HOLD (per motor) (STEP400 only) | int<br>0 (78.125mA) | With the electromagnetic brake enabled, TVAL_HOLD is raised to at least half of TVAL_RUN whenever the motor is energized again; the raised value replaces the stored setting (so `/saveConfig` saves it) and is returned by [`/getTval`](../reference/voltage-and-current-mode-settings.md#gettval). Commands: [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval), [`/setHoldTval`](../reference/voltage-and-current-mode-settings.md#setholdtval) |
| <a id="currentmode-tval_run"></a>`TVAL_RUN`<br>TVAL_RUN (per motor) (STEP400 only) | int<br>16 (1.328A) | Commands: [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval), [`/setRunTval`](../reference/voltage-and-current-mode-settings.md#setruntval) |
| <a id="currentmode-tval_acc"></a>`TVAL_ACC`<br>TVAL_ACC (per motor) (STEP400 only) | int<br>16 (1.328A) | Commands: [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval), [`/setAccTval`](../reference/voltage-and-current-mode-settings.md#setacctval) |
| <a id="currentmode-tval_dec"></a>`TVAL_DEC`<br>TVAL_DEC (per motor) (STEP400 only) | int<br>16 (1.328A) | Commands: [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval), [`/setDecTval`](../reference/voltage-and-current-mode-settings.md#setdectval) |
| <a id="currentmode-t_fast"></a>`T_FAST`<br>T_FAST (per motor) (STEP400 only) | int<br>25 | Commands: [`/setDecayModeParam`](../reference/voltage-and-current-mode-settings.md#setdecaymodeparam) |
| <a id="currentmode-ton_min"></a>`TON_MIN`<br>TON_MIN (per motor) (STEP400 only) | int<br>41 | Commands: [`/setDecayModeParam`](../reference/voltage-and-current-mode-settings.md#setdecaymodeparam) |
| <a id="currentmode-toff_min"></a>`TOFF_MIN`<br>TOFF_MIN (per motor) (STEP400 only) | int<br>41 | Commands: [`/setDecayModeParam`](../reference/voltage-and-current-mode-settings.md#setdecaymodeparam) |

## servoMode {#servomode}

| Key / Name | Type / Initial value | Description |
| --- | --- | --- |
| <a id="servomode-kp"></a>`kP`<br>kP (per motor) | float<br>0.06 | Commands: [`/setServoParam`](../reference/servo-mode_reference.md#setservoparam) |
| <a id="servomode-ki"></a>`kI`<br>kI (per motor) | float<br>0 | Commands: [`/setServoParam`](../reference/servo-mode_reference.md#setservoparam) |
| <a id="servomode-kd"></a>`kD`<br>kD (per motor) | float<br>0 | Commands: [`/setServoParam`](../reference/servo-mode_reference.md#setservoparam) |
