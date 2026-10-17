---
title: Command list
lang: en
---

# Command list

<!-- This page is generated from spec/osc-commands.yaml by tools/generate.py. Do not edit it directly. -->

All OSC commands in the order of the reference pages. Click a command to go to its reference.

## System settings

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/setDestIp`](system-settings.md#setdestip) | - | ✓ | ✓ |  |
| [`/getVersion`](system-settings.md#getversion) | - | ✓ | ✓ |  |
| [`/getConfigName`](system-settings.md#getconfigname) | - | ✓ | ✓ |  |
| [`/reportError`](system-settings.md#reporterror) | (bool)enable | ✓ | ✓ |  |
| [`/setConfigName`](system-settings.md#setconfigname) | (string)configName | ✓ | ✓ | 2.1.0 |
| [`/saveConfig`](system-settings.md#saveconfig) | - | ✓ | ✓ | 2.1.0 |
| [`/resetDevice`](system-settings.md#resetdevice) | - | ✓ | ✓ |  |

## Motor driver settings

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/setMicrostepMode`](motor-driver-settings.md#setmicrostepmode) | (int)motorID (int)STEP_SEL | ✓ | ✓ |  |
| [`/getMicrostepMode`](motor-driver-settings.md#getmicrostepmode) | (int)motorID | ✓ | ✓ |  |
| [`/enableLowSpeedOptimize`](motor-driver-settings.md#enablelowspeedoptimize) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/setLowSpeedOptimizeThreshold`](motor-driver-settings.md#setlowspeedoptimizethreshold) | (int)motorID (float)lowSpeedOptimizationThreshold | ✓ | ✓ |  |
| [`/getLowSpeedOptimizeThreshold`](motor-driver-settings.md#getlowspeedoptimizethreshold) | (int)motorID | ✓ | ✓ |  |
| [`/enableBusyReport`](motor-driver-settings.md#enablebusyreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getBusy`](motor-driver-settings.md#getbusy) | (int)motorID | ✓ | ✓ |  |
| [`/enableHizReport`](motor-driver-settings.md#enablehizreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getHiZ`](motor-driver-settings.md#gethiz) | (int)motorID | ✓ | ✓ |  |
| [`/enableDirReport`](motor-driver-settings.md#enabledirreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getDir`](motor-driver-settings.md#getdir) | (int)motorID | ✓ | ✓ |  |
| [`/enableMotorStatusReport`](motor-driver-settings.md#enablemotorstatusreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getMotorStatus`](motor-driver-settings.md#getmotorstatus) | (int)motorID | ✓ | ✓ |  |
| [`/setPositionReportInterval`](motor-driver-settings.md#setpositionreportinterval) | (int)motorID (int)interval | ✓ | ✓ |  |
| [`/setPositionListReportInterval`](motor-driver-settings.md#setpositionlistreportinterval) | (int)interval | ✓ | ✓ |  |
| [`/getAdcVal`](motor-driver-settings.md#getadcval) | (int)motorID | ✓ |  |  |
| [`/getStatus`](motor-driver-settings.md#getstatus) | (int)motorID | ✓ | ✓ |  |
| [`/getConfigRegister`](motor-driver-settings.md#getconfigregister) | (int)motorID | ✓ | ✓ |  |
| [`/resetMotorDriver`](motor-driver-settings.md#resetmotordriver) | (int)motorID | ✓ | ✓ |  |
| [`/getStatusList`](motor-driver-settings.md#getstatuslist) | - | ✓ | ✓ |  |

## Alarm settings

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/enableUvloReport`](alarm-settings.md#enableuvloreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getUvlo`](alarm-settings.md#getuvlo) | (int)motorID | ✓ | ✓ |  |
| [`/enableThermalStatusReport`](alarm-settings.md#enablethermalstatusreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getThermalStatus`](alarm-settings.md#getthermalstatus) | (int)motorID | ✓ | ✓ |  |
| [`/enableOverCurrentReport`](alarm-settings.md#enableovercurrentreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/setOverCurrentThreshold`](alarm-settings.md#setovercurrentthreshold) | (int)motorID (int)OCD_TH | ✓ | ✓ |  |
| [`/getOverCurrentThreshold`](alarm-settings.md#getovercurrentthreshold) | (int)motorID | ✓ | ✓ |  |
| [`/enableStallReport`](alarm-settings.md#enablestallreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/setStallThreshold`](alarm-settings.md#setstallthreshold) | (int)motorID (int)STALL_TH | ✓ | ✓ |  |
| [`/getStallThreshold`](alarm-settings.md#getstallthreshold) | (int)motorID | ✓ | ✓ |  |
| [`/setProhibitMotionOnHomeSw`](alarm-settings.md#setprohibitmotiononhomesw) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getProhibitMotionOnHomeSw`](alarm-settings.md#getprohibitmotiononhomesw) | (int)motorID | ✓ | ✓ |  |
| [`/setProhibitMotionOnLimitSw`](alarm-settings.md#setprohibitmotiononlimitsw) | (int)motorID (bool)enable | ✓ |  |  |
| [`/getProhibitMotionOnLimitSw`](alarm-settings.md#getprohibitmotiononlimitsw) | (int)motorID | ✓ |  |  |

## Voltage and current mode settings

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/setVoltageMode`](voltage-and-current-mode-settings.md#setvoltagemode) | (int)motorID | ✓ |  |  |
| [`/setKval`](voltage-and-current-mode-settings.md#setkval) | (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)decKVAL | ✓ | ✓ |  |
| [`/getKval`](voltage-and-current-mode-settings.md#getkval) | (int)motorID | ✓ | ✓ |  |
| [`/setBemfParam`](voltage-and-current-mode-settings.md#setbemfparam) | (int)motorID (int)INT_SPEED (int)ST_SLP (int)FN_SLP_ACC (int)FN_SLP_DEC | ✓ | ✓ |  |
| [`/getBemfParam`](voltage-and-current-mode-settings.md#getbemfparam) | (int)motorID | ✓ | ✓ |  |
| [`/setHoldKval`](voltage-and-current-mode-settings.md#setholdkval) | (int)motorID (int)holdKVAL | ✓ | ✓ |  |
| [`/setRunKval`](voltage-and-current-mode-settings.md#setrunkval) | (int)motorID (int)runKVAL | ✓ | ✓ |  |
| [`/setAccKval`](voltage-and-current-mode-settings.md#setacckval) | (int)motorID (int)accKVAL | ✓ | ✓ |  |
| [`/setDecKval`](voltage-and-current-mode-settings.md#setdeckval) | (int)motorID (int)decKVAL | ✓ | ✓ |  |
| [`/setCurrentMode`](voltage-and-current-mode-settings.md#setcurrentmode) | (int)motorID | ✓ |  |  |
| [`/setTval`](voltage-and-current-mode-settings.md#settval) | (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL | ✓ |  |  |
| [`/getTval`](voltage-and-current-mode-settings.md#gettval) | (int)motorID | ✓ |  |  |
| [`/getTval_mA`](voltage-and-current-mode-settings.md#gettval_ma) | (int)motorID | ✓ |  |  |
| [`/setDecayModeParam`](voltage-and-current-mode-settings.md#setdecaymodeparam) | (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN | ✓ |  |  |
| [`/getDecayModeParam`](voltage-and-current-mode-settings.md#getdecaymodeparam) | (int)motorID | ✓ |  |  |
| [`/setHoldTval`](voltage-and-current-mode-settings.md#setholdtval) | (int)motorID (int)holdTVAL | ✓ |  |  |
| [`/setRunTval`](voltage-and-current-mode-settings.md#setruntval) | (int)motorID (int)runTVAL | ✓ |  |  |
| [`/setAccTval`](voltage-and-current-mode-settings.md#setacctval) | (int)motorID (int)accTVAL | ✓ |  |  |
| [`/setDecTval`](voltage-and-current-mode-settings.md#setdectval) | (int)motorID (int)decTVAL | ✓ |  |  |

## Speed profile

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/setSpeedProfile`](speed-profile.md#setspeedprofile) | (int)motorID (float)acc (float)dec (float)maxSpeed | ✓ | ✓ |  |
| [`/getSpeedProfile`](speed-profile.md#getspeedprofile) | (int)motorID | ✓ | ✓ |  |
| [`/setFullstepSpeed`](speed-profile.md#setfullstepspeed) | (int)motorID (float)fullstepSpeed | ✓ | ✓ |  |
| [`/getFullstepSpeed`](speed-profile.md#getfullstepspeed) | (int)motorID | ✓ | ✓ |  |
| [`/setMaxSpeed`](speed-profile.md#setmaxspeed) | (int)motorID (float)maxSpeed | ✓ | ✓ |  |
| [`/setAcc`](speed-profile.md#setacc) | (int)motorID (float)acc | ✓ | ✓ |  |
| [`/setDec`](speed-profile.md#setdec) | (int)motorID (float)dec | ✓ | ✓ |  |
| [`/setMinSpeed`](speed-profile.md#setminspeed) | (int)motorID (float)minSpeed | ✓ | ✓ |  |
| [`/getMinSpeed`](speed-profile.md#getminspeed) | (int)motorID | ✓ | ✓ |  |
| [`/getSpeed`](speed-profile.md#getspeed) | (int)motorID | ✓ | ✓ |  |
| [`/setSpeedProfileRaw`](speed-profile.md#setspeedprofileraw) | (int)motorID (int)acc (int)dec (int)maxSpeed | ✓ | ✓ |  |
| [`/getSpeedProfileRaw`](speed-profile.md#getspeedprofileraw) | (int)motorID | ✓ | ✓ |  |
| [`/setMaxSpeedRaw`](speed-profile.md#setmaxspeedraw) | (int)motorID (int)maxSpeed | ✓ | ✓ |  |
| [`/setMinSpeedRaw`](speed-profile.md#setminspeedraw) | (int)motorID (int)minSpeed | ✓ | ✓ |  |
| [`/setFullstepSpeedRaw`](speed-profile.md#setfullstepspeedraw) | (int)motorID (int)fullstepSpeed | ✓ | ✓ |  |
| [`/setAccRaw`](speed-profile.md#setaccraw) | (int)motorID (int)acc | ✓ | ✓ |  |
| [`/setDecRaw`](speed-profile.md#setdecraw) | (int)motorID (int)dec | ✓ | ✓ |  |

## Homing

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/homing`](homing.md#homing) | (int)motorID | ✓ | ✓ |  |
| [`/getHomingStatus`](homing.md#gethomingstatus) | (int)motorID | ✓ | ✓ |  |
| [`/setHomingDirection`](homing.md#sethomingdirection) | (int)motorID (bool)direction | ✓ | ✓ |  |
| [`/getHomingDirection`](homing.md#gethomingdirection) | (int)motorID | ✓ | ✓ |  |
| [`/setHomingSpeed`](homing.md#sethomingspeed) | (int)motorID (float)speed | ✓ | ✓ |  |
| [`/getHomingSpeed`](homing.md#gethomingspeed) | (int)motorID | ✓ | ✓ |  |
| [`/goUntil`](homing.md#gountil) | (int)motorID (bool)ACT (float)speed | ✓ | ✓ |  |
| [`/setGoUntilTimeout`](homing.md#setgountiltimeout) | (int)motorID (int)timeOut | ✓ | ✓ |  |
| [`/getGoUntilTimeout`](homing.md#getgountiltimeout) | (int)motorID | ✓ | ✓ |  |
| [`/releaseSw`](homing.md#releasesw) | (int)motorID (bool)ACT (bool)DIR | ✓ | ✓ |  |
| [`/setReleaseSwTimeout`](homing.md#setreleaseswtimeout) | (int)motorID (int)timeOut | ✓ | ✓ |  |
| [`/getReleaseSwTimeout`](homing.md#getreleaseswtimeout) | (int)motorID | ✓ | ✓ |  |

## HOME and LIMIT sensors

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/enableHomeSwReport`](home-and-limit-sensors.md#enablehomeswreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/enableSwEventReport`](home-and-limit-sensors.md#enablesweventreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getHomeSw`](home-and-limit-sensors.md#gethomesw) | (int)motorID | ✓ | ✓ |  |
| [`/enableLimitSwReport`](home-and-limit-sensors.md#enablelimitswreport) | (int)motorID (bool)enable | ✓ |  |  |
| [`/getLimitSw`](home-and-limit-sensors.md#getlimitsw) | (int)motorID | ✓ |  |  |
| [`/setHomeSwMode`](home-and-limit-sensors.md#sethomeswmode) | (int)motorID (bool)SW_MODE | ✓ | ✓ |  |
| [`/getHomeSwMode`](home-and-limit-sensors.md#gethomeswmode) | (int)motorID | ✓ | ✓ |  |
| [`/setLimitSwMode`](home-and-limit-sensors.md#setlimitswmode) | (int)motorID (bool)SW_MODE | ✓ |  |  |
| [`/getLimitSwMode`](home-and-limit-sensors.md#getlimitswmode) | (int)motorID | ✓ |  |  |

## Position management

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/setPosition`](position-management.md#setposition) | (int)motorID (int)newPosition | ✓ | ✓ |  |
| [`/getPosition`](position-management.md#getposition) | (int)motorID | ✓ | ✓ |  |
| [`/getPositionList`](position-management.md#getpositionlist) | - | ✓ | ✓ |  |
| [`/resetPos`](position-management.md#resetpos) | (int)motorID | ✓ | ✓ |  |
| [`/setElPos`](position-management.md#setelpos) | (int)motorID (int)newFullstep (int)newMicrostep | ✓ | ✓ |  |
| [`/getElPos`](position-management.md#getelpos) | (int)motorID | ✓ | ✓ |  |
| [`/setMark`](position-management.md#setmark) | (int)motorID (int)MARK | ✓ | ✓ |  |
| [`/getMark`](position-management.md#getmark) | (int)motorID | ✓ | ✓ |  |
| [`/goHome`](position-management.md#gohome) | (int)motorID | ✓ | ✓ |  |
| [`/goMark`](position-management.md#gomark) | (int)motorID | ✓ | ✓ |  |

## Motor control

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/run`](motor-control.md#run) | (int)motorID (float)speed | ✓ | ✓ |  |
| [`/move`](motor-control.md#move) | (int)motorID (int)step | ✓ | ✓ |  |
| [`/goTo`](motor-control.md#goto) | (int)motorID (int)position | ✓ | ✓ |  |
| [`/goToDir`](motor-control.md#gotodir) | (int)motorID (bool)DIR (int)position | ✓ | ✓ |  |
| [`/softStop`](motor-control.md#softstop) | (int)motorID | ✓ | ✓ |  |
| [`/hardStop`](motor-control.md#hardstop) | (int)motorID | ✓ | ✓ |  |
| [`/softHiZ`](motor-control.md#softhiz) | (int)motorID | ✓ | ✓ |  |
| [`/hardHiZ`](motor-control.md#hardhiz) | (int)motorID | ✓ | ✓ |  |
| [`/combine/run`](motor-control.md#combine-run) | (int)motorID1 (int)motorID2 (float)speed | ✓ | ✓ |  |
| [`/combine/move`](motor-control.md#combine-move) | (int)motorID1 (int)motorID2 (int)step | ✓ | ✓ |  |
| [`/combine/goTo`](motor-control.md#combine-goto) | (int)motorID1 (int)motorID2 (int)position | ✓ | ✓ |  |
| [`/combine/goToDir`](motor-control.md#combine-gotodir) | (int)motorID1 (int)motorID2 (bool)DIR (int)position | ✓ | ✓ |  |
| [`/combine/softStop`](motor-control.md#combine-softstop) | (int)motorID1 (int)motorID2 | ✓ | ✓ |  |
| [`/combine/hardStop`](motor-control.md#combine-hardstop) | (int)motorID1 (int)motorID2 | ✓ | ✓ |  |
| [`/combine/softHiZ`](motor-control.md#combine-softhiz) | (int)motorID1 (int)motorID2 | ✓ | ✓ |  |
| [`/combine/hardHiZ`](motor-control.md#combine-hardhiz) | (int)motorID1 (int)motorID2 | ✓ | ✓ |  |
| [`/runRaw`](motor-control.md#runraw) | (int)motorID (int)speed | ✓ | ✓ |  |
| [`/goUntilRaw`](motor-control.md#gountilraw) | (int)motorID (bool)ACT (int)speed | ✓ | ✓ |  |
| [`/combine/runRaw`](motor-control.md#combine-runraw) | (int)motorID1 (int)motorID2 (int)speed | ✓ | ✓ |  |

## Electromagnetic brake

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/enableElectromagnetBrake`](brake.md#enableelectromagnetbrake) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/activate`](brake.md#activate) | (int)motorID (bool)state | ✓ | ✓ |  |
| [`/free`](brake.md#free) | (int)motorID | ✓ | ✓ |  |
| [`/setBrakeTransitionDuration`](brake.md#setbraketransitionduration) | (int)motorID (int)duration | ✓ | ✓ |  |
| [`/getBrakeTransitionDuration`](brake.md#getbraketransitionduration) | (int)motorID | ✓ | ✓ |  |
| [`/getBrakeStatus`](brake.md#getbrakestatus) | (int)motorID | ✓ | ✓ | 2.2.0 |

## Servo mode

| Command | Arguments | STEP400 | STEP800 | Since |
| --- | --- | --- | --- | --- |
| [`/enableServoMode`](servo-mode_reference.md#enableservomode) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/setServoParam`](servo-mode_reference.md#setservoparam) | (int)motorID (float)kP (float)kI (float)kD | ✓ | ✓ |  |
| [`/getServoParam`](servo-mode_reference.md#getservoparam) | (int)motorID | ✓ | ✓ |  |
| [`/setTargetPosition`](servo-mode_reference.md#settargetposition) | (int)motorID (int)position | ✓ | ✓ |  |
| [`/setTargetPositionList`](servo-mode_reference.md#settargetpositionlist) | (int)position1 ... (int)positionN | ✓ | ✓ |  |
