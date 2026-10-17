---
title: Command list
slug: command-list
lang: en
parent: 886
menu_order: 21
---

# Command list

<!-- This page is generated from spec/osc-commands.yaml by tools/generate.py. Do not edit it directly. -->

All OSC commands in the order of the reference pages. Click a command to go to its reference.

## System settings

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/setDestIp`](system-settings_en.md#setdestip) | - | ✓ | ✓ |  |
| [`/getVersion`](system-settings_en.md#getversion) | - | ✓ | ✓ |  |
| [`/getConfigName`](system-settings_en.md#getconfigname) | - | ✓ | ✓ |  |
| [`/reportError`](system-settings_en.md#reporterror) | (bool)enable | ✓ | ✓ |  |
| [`/setConfigName`](system-settings_en.md#setconfigname) | (string)configName | ✓ | ✓ | 2.1.0 |
| [`/saveConfig`](system-settings_en.md#saveconfig) | - | ✓ | ✓ | 2.1.0 |
| [`/resetDevice`](system-settings_en.md#resetdevice) | - | ✓ | ✓ |  |

## Motor driver settings

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/setMicrostepMode`](motor-driver-settings_en.md#setmicrostepmode) | (int)motorID (int)STEP_SEL | ✓ | ✓ |  |
| [`/getMicrostepMode`](motor-driver-settings_en.md#getmicrostepmode) | (int)motorID | ✓ | ✓ |  |
| [`/enableLowSpeedOptimize`](motor-driver-settings_en.md#enablelowspeedoptimize) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/setLowSpeedOptimizeThreshold`](motor-driver-settings_en.md#setlowspeedoptimizethreshold) | (int)motorID (float)lowSpeedOptimizationThreshold | ✓ | ✓ |  |
| [`/getLowSpeedOptimizeThreshold`](motor-driver-settings_en.md#getlowspeedoptimizethreshold) | (int)motorID | ✓ | ✓ |  |
| [`/enableBusyReport`](motor-driver-settings_en.md#enablebusyreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getBusy`](motor-driver-settings_en.md#getbusy) | (int)motorID | ✓ | ✓ |  |
| [`/enableHizReport`](motor-driver-settings_en.md#enablehizreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getHiZ`](motor-driver-settings_en.md#gethiz) | (int)motorID | ✓ | ✓ |  |
| [`/enableDirReport`](motor-driver-settings_en.md#enabledirreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getDir`](motor-driver-settings_en.md#getdir) | (int)motorID | ✓ | ✓ |  |
| [`/enableMotorStatusReport`](motor-driver-settings_en.md#enablemotorstatusreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getMotorStatus`](motor-driver-settings_en.md#getmotorstatus) | (int)motorID | ✓ | ✓ |  |
| [`/setPositionReportInterval`](motor-driver-settings_en.md#setpositionreportinterval) | (int)motorID (int)interval | ✓ | ✓ |  |
| [`/setPositionListReportInterval`](motor-driver-settings_en.md#setpositionlistreportinterval) | (int)interval | ✓ | ✓ |  |
| [`/getAdcVal`](motor-driver-settings_en.md#getadcval) | (int)motorID | ✓ |  |  |
| [`/getStatus`](motor-driver-settings_en.md#getstatus) | (int)motorID | ✓ | ✓ |  |
| [`/getConfigRegister`](motor-driver-settings_en.md#getconfigregister) | (int)motorID | ✓ | ✓ |  |
| [`/resetMotorDriver`](motor-driver-settings_en.md#resetmotordriver) | (int)motorID | ✓ | ✓ |  |
| [`/getStatusList`](motor-driver-settings_en.md#getstatuslist) | - | ✓ | ✓ |  |

## Alarm settings

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/enableUvloReport`](alarm-settings_en.md#enableuvloreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getUvlo`](alarm-settings_en.md#getuvlo) | (int)motorID | ✓ | ✓ |  |
| [`/enableThermalStatusReport`](alarm-settings_en.md#enablethermalstatusreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getThermalStatus`](alarm-settings_en.md#getthermalstatus) | (int)motorID | ✓ | ✓ |  |
| [`/enableOverCurrentReport`](alarm-settings_en.md#enableovercurrentreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/setOverCurrentThreshold`](alarm-settings_en.md#setovercurrentthreshold) | (int)motorID (int)OCD_TH | ✓ | ✓ |  |
| [`/getOverCurrentThreshold`](alarm-settings_en.md#getovercurrentthreshold) | (int)motorID | ✓ | ✓ |  |
| [`/enableStallReport`](alarm-settings_en.md#enablestallreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/setStallThreshold`](alarm-settings_en.md#setstallthreshold) | (int)motorID (int)STALL_TH | ✓ | ✓ |  |
| [`/getStallThreshold`](alarm-settings_en.md#getstallthreshold) | (int)motorID | ✓ | ✓ |  |
| [`/setProhibitMotionOnHomeSw`](alarm-settings_en.md#setprohibitmotiononhomesw) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getProhibitMotionOnHomeSw`](alarm-settings_en.md#getprohibitmotiononhomesw) | (int)motorID | ✓ | ✓ |  |
| [`/setProhibitMotionOnLimitSw`](alarm-settings_en.md#setprohibitmotiononlimitsw) | (int)motorID (bool)enable | ✓ |  |  |
| [`/getProhibitMotionOnLimitSw`](alarm-settings_en.md#getprohibitmotiononlimitsw) | (int)motorID | ✓ |  |  |

## Voltage and current mode settings

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/setVoltageMode`](voltage-and-current-mode-settings_en.md#setvoltagemode) | (int)motorID | ✓ |  |  |
| [`/setKval`](voltage-and-current-mode-settings_en.md#setkval) | (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)decKVAL | ✓ | ✓ |  |
| [`/getKval`](voltage-and-current-mode-settings_en.md#getkval) | (int)motorID | ✓ | ✓ |  |
| [`/setBemfParam`](voltage-and-current-mode-settings_en.md#setbemfparam) | (int)motorID (int)INT_SPEED (int)ST_SLP (int)FN_SLP_ACC (int)FN_SLP_DEC | ✓ | ✓ |  |
| [`/getBemfParam`](voltage-and-current-mode-settings_en.md#getbemfparam) | (int)motorID | ✓ | ✓ |  |
| [`/setHoldKval`](voltage-and-current-mode-settings_en.md#setholdkval) | (int)motorID (int)holdKVAL | ✓ | ✓ |  |
| [`/setRunKval`](voltage-and-current-mode-settings_en.md#setrunkval) | (int)motorID (int)runKVAL | ✓ | ✓ |  |
| [`/setAccKval`](voltage-and-current-mode-settings_en.md#setacckval) | (int)motorID (int)accKVAL | ✓ | ✓ |  |
| [`/setDecKval`](voltage-and-current-mode-settings_en.md#setdeckval) | (int)motorID (int)decKVAL | ✓ | ✓ |  |
| [`/setCurrentMode`](voltage-and-current-mode-settings_en.md#setcurrentmode) | (int)motorID | ✓ |  |  |
| [`/setTval`](voltage-and-current-mode-settings_en.md#settval) | (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL | ✓ |  |  |
| [`/getTval`](voltage-and-current-mode-settings_en.md#gettval) | (int)motorID | ✓ |  |  |
| [`/getTval_mA`](voltage-and-current-mode-settings_en.md#gettval_ma) | (int)motorID | ✓ |  |  |
| [`/setDecayModeParam`](voltage-and-current-mode-settings_en.md#setdecaymodeparam) | (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN | ✓ |  |  |
| [`/getDecayModeParam`](voltage-and-current-mode-settings_en.md#getdecaymodeparam) | (int)motorID | ✓ |  |  |
| [`/setHoldTval`](voltage-and-current-mode-settings_en.md#setholdtval) | (int)motorID (int)holdTVAL | ✓ |  |  |
| [`/setRunTval`](voltage-and-current-mode-settings_en.md#setruntval) | (int)motorID (int)runTVAL | ✓ |  |  |
| [`/setAccTval`](voltage-and-current-mode-settings_en.md#setacctval) | (int)motorID (int)accTVAL | ✓ |  |  |
| [`/setDecTval`](voltage-and-current-mode-settings_en.md#setdectval) | (int)motorID (int)decTVAL | ✓ |  |  |

## Speed profile

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/setSpeedProfile`](speed-profile_en.md#setspeedprofile) | (int)motorID (float)acc (float)dec (float)maxSpeed | ✓ | ✓ |  |
| [`/getSpeedProfile`](speed-profile_en.md#getspeedprofile) | (int)motorID | ✓ | ✓ |  |
| [`/setFullstepSpeed`](speed-profile_en.md#setfullstepspeed) | (int)motorID (float)fullstepSpeed | ✓ | ✓ |  |
| [`/getFullstepSpeed`](speed-profile_en.md#getfullstepspeed) | (int)motorID | ✓ | ✓ |  |
| [`/setMaxSpeed`](speed-profile_en.md#setmaxspeed) | (int)motorID (float)maxSpeed | ✓ | ✓ |  |
| [`/setAcc`](speed-profile_en.md#setacc) | (int)motorID (float)acc | ✓ | ✓ |  |
| [`/setDec`](speed-profile_en.md#setdec) | (int)motorID (float)dec | ✓ | ✓ |  |
| [`/setMinSpeed`](speed-profile_en.md#setminspeed) | (int)motorID (float)minSpeed | ✓ | ✓ |  |
| [`/getMinSpeed`](speed-profile_en.md#getminspeed) | (int)motorID | ✓ | ✓ |  |
| [`/getSpeed`](speed-profile_en.md#getspeed) | (int)motorID | ✓ | ✓ |  |
| [`/setSpeedProfileRaw`](speed-profile_en.md#setspeedprofileraw) | (int)motorID (int)acc (int)dec (int)maxSpeed | ✓ | ✓ |  |
| [`/getSpeedProfileRaw`](speed-profile_en.md#getspeedprofileraw) | (int)motorID | ✓ | ✓ |  |
| [`/setMaxSpeedRaw`](speed-profile_en.md#setmaxspeedraw) | (int)motorID (int)maxSpeed | ✓ | ✓ |  |
| [`/setMinSpeedRaw`](speed-profile_en.md#setminspeedraw) | (int)motorID (int)minSpeed | ✓ | ✓ |  |
| [`/setFullstepSpeedRaw`](speed-profile_en.md#setfullstepspeedraw) | (int)motorID (int)fullstepSpeed | ✓ | ✓ |  |
| [`/setAccRaw`](speed-profile_en.md#setaccraw) | (int)motorID (int)acc | ✓ | ✓ |  |
| [`/setDecRaw`](speed-profile_en.md#setdecraw) | (int)motorID (int)dec | ✓ | ✓ |  |

## Homing

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/homing`](homing_en.md#homing) | (int)motorID | ✓ | ✓ |  |
| [`/getHomingStatus`](homing_en.md#gethomingstatus) | (int)motorID | ✓ | ✓ |  |
| [`/setHomingDirection`](homing_en.md#sethomingdirection) | (int)motorID (bool)direction | ✓ | ✓ |  |
| [`/getHomingDirection`](homing_en.md#gethomingdirection) | (int)motorID | ✓ | ✓ |  |
| [`/setHomingSpeed`](homing_en.md#sethomingspeed) | (int)motorID (float)speed | ✓ | ✓ |  |
| [`/getHomingSpeed`](homing_en.md#gethomingspeed) | (int)motorID | ✓ | ✓ |  |
| [`/goUntil`](homing_en.md#gountil) | (int)motorID (bool)ACT (float)speed | ✓ | ✓ |  |
| [`/setGoUntilTimeout`](homing_en.md#setgountiltimeout) | (int)motorID (int)timeOut | ✓ | ✓ |  |
| [`/getGoUntilTimeout`](homing_en.md#getgountiltimeout) | (int)motorID | ✓ | ✓ |  |
| [`/releaseSw`](homing_en.md#releasesw) | (int)motorID (bool)ACT (bool)DIR | ✓ | ✓ |  |
| [`/setReleaseSwTimeout`](homing_en.md#setreleaseswtimeout) | (int)motorID (int)timeOut | ✓ | ✓ |  |
| [`/getReleaseSwTimeout`](homing_en.md#getreleaseswtimeout) | (int)motorID | ✓ | ✓ |  |

## HOME and LIMIT sensors

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/enableHomeSwReport`](home-and-limit-sensors_en.md#enablehomeswreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/enableSwEventReport`](home-and-limit-sensors_en.md#enablesweventreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getHomeSw`](home-and-limit-sensors_en.md#gethomesw) | (int)motorID | ✓ | ✓ |  |
| [`/enableLimitSwReport`](home-and-limit-sensors_en.md#enablelimitswreport) | (int)motorID (bool)enable | ✓ |  |  |
| [`/getLimitSw`](home-and-limit-sensors_en.md#getlimitsw) | (int)motorID | ✓ |  |  |
| [`/setHomeSwMode`](home-and-limit-sensors_en.md#sethomeswmode) | (int)motorID (bool)SW_MODE | ✓ | ✓ |  |
| [`/getHomeSwMode`](home-and-limit-sensors_en.md#gethomeswmode) | (int)motorID | ✓ | ✓ |  |
| [`/setLimitSwMode`](home-and-limit-sensors_en.md#setlimitswmode) | (int)motorID (bool)SW_MODE | ✓ |  |  |
| [`/getLimitSwMode`](home-and-limit-sensors_en.md#getlimitswmode) | (int)motorID | ✓ |  |  |

## Position management

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/setPosition`](position-management_en.md#setposition) | (int)motorID (int)newPosition | ✓ | ✓ |  |
| [`/getPosition`](position-management_en.md#getposition) | (int)motorID | ✓ | ✓ |  |
| [`/getPositionList`](position-management_en.md#getpositionlist) | - | ✓ | ✓ |  |
| [`/resetPos`](position-management_en.md#resetpos) | (int)motorID | ✓ | ✓ |  |
| [`/setElPos`](position-management_en.md#setelpos) | (int)motorID (int)newFullstep (int)newMicrostep | ✓ | ✓ |  |
| [`/getElPos`](position-management_en.md#getelpos) | (int)motorID | ✓ | ✓ |  |
| [`/setMark`](position-management_en.md#setmark) | (int)motorID (int)MARK | ✓ | ✓ |  |
| [`/getMark`](position-management_en.md#getmark) | (int)motorID | ✓ | ✓ |  |
| [`/goHome`](position-management_en.md#gohome) | (int)motorID | ✓ | ✓ |  |
| [`/goMark`](position-management_en.md#gomark) | (int)motorID | ✓ | ✓ |  |

## Motor control

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/run`](motor-control_en.md#run) | (int)motorID (float)speed | ✓ | ✓ |  |
| [`/move`](motor-control_en.md#move) | (int)motorID (int)step | ✓ | ✓ |  |
| [`/goTo`](motor-control_en.md#goto) | (int)motorID (int)position | ✓ | ✓ |  |
| [`/goToDir`](motor-control_en.md#gotodir) | (int)motorID (bool)DIR (int)position | ✓ | ✓ |  |
| [`/softStop`](motor-control_en.md#softstop) | (int)motorID | ✓ | ✓ |  |
| [`/hardStop`](motor-control_en.md#hardstop) | (int)motorID | ✓ | ✓ |  |
| [`/softHiZ`](motor-control_en.md#softhiz) | (int)motorID | ✓ | ✓ |  |
| [`/hardHiZ`](motor-control_en.md#hardhiz) | (int)motorID | ✓ | ✓ |  |
| [`/combine/run`](motor-control_en.md#combine-run) | (int)motorID1 (int)motorID2 (float)speed | ✓ | ✓ |  |
| [`/combine/move`](motor-control_en.md#combine-move) | (int)motorID1 (int)motorID2 (int)step | ✓ | ✓ |  |
| [`/combine/goTo`](motor-control_en.md#combine-goto) | (int)motorID1 (int)motorID2 (int)position | ✓ | ✓ |  |
| [`/combine/goToDir`](motor-control_en.md#combine-gotodir) | (int)motorID1 (int)motorID2 (bool)DIR (int)position | ✓ | ✓ |  |
| [`/combine/softStop`](motor-control_en.md#combine-softstop) | (int)motorID1 (int)motorID2 | ✓ | ✓ |  |
| [`/combine/hardStop`](motor-control_en.md#combine-hardstop) | (int)motorID1 (int)motorID2 | ✓ | ✓ |  |
| [`/combine/softHiZ`](motor-control_en.md#combine-softhiz) | (int)motorID1 (int)motorID2 | ✓ | ✓ |  |
| [`/combine/hardHiZ`](motor-control_en.md#combine-hardhiz) | (int)motorID1 (int)motorID2 | ✓ | ✓ |  |
| [`/runRaw`](motor-control_en.md#runraw) | (int)motorID (int)speed | ✓ | ✓ |  |
| [`/goUntilRaw`](motor-control_en.md#gountilraw) | (int)motorID (bool)ACT (int)speed | ✓ | ✓ |  |
| [`/combine/runRaw`](motor-control_en.md#combine-runraw) | (int)motorID1 (int)motorID2 (int)speed | ✓ | ✓ |  |

## Electromagnetic brake

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/enableElectromagnetBrake`](brake_en.md#enableelectromagnetbrake) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/activate`](brake_en.md#activate) | (int)motorID (bool)state | ✓ | ✓ |  |
| [`/free`](brake_en.md#free) | (int)motorID | ✓ | ✓ |  |
| [`/setBrakeTransitionDuration`](brake_en.md#setbraketransitionduration) | (int)motorID (int)duration | ✓ | ✓ |  |
| [`/getBrakeTransitionDuration`](brake_en.md#getbraketransitionduration) | (int)motorID | ✓ | ✓ |  |
| [`/getBrakeStatus`](brake_en.md#getbrakestatus) | (int)motorID | ✓ | ✓ | 2.2.0 |

## Servo mode

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/enableServoMode`](servo-mode_reference_en.md#enableservomode) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/setServoParam`](servo-mode_reference_en.md#setservoparam) | (int)motorID (float)kP (float)kI (float)kD | ✓ | ✓ |  |
| [`/getServoParam`](servo-mode_reference_en.md#getservoparam) | (int)motorID | ✓ | ✓ |  |
| [`/setTargetPosition`](servo-mode_reference_en.md#settargetposition) | (int)motorID (int)position | ✓ | ✓ |  |
| [`/setTargetPositionList`](servo-mode_reference_en.md#settargetpositionlist) | (int)position1 ... (int)positionN | ✓ | ✓ |  |
