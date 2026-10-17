---
title: コマンド一覧
lang: ja
---

# コマンド一覧

<!-- This page is generated from spec/osc-commands.yaml by tools/generate.py. Do not edit it directly. (自動生成・直接編集しない) -->

すべての OSC コマンドを、リファレンスのページの順に並べています。コマンド名から詳細へ移動できます。

## 基板全体の設定

| コマンド | アーギュメント | STEP400 | STEP800 | 追加 |
| --- | --- | --- | --- | --- |
| [`/setDestIp`](system-settings_jp.md#setdestip) | - | ✓ | ✓ |  |
| [`/getVersion`](system-settings_jp.md#getversion) | - | ✓ | ✓ |  |
| [`/getConfigName`](system-settings_jp.md#getconfigname) | - | ✓ | ✓ |  |
| [`/reportError`](system-settings_jp.md#reporterror) | (bool)enable | ✓ | ✓ |  |
| [`/setConfigName`](system-settings_jp.md#setconfigname) | (string)configName | ✓ | ✓ | 2.1.0 |
| [`/saveConfig`](system-settings_jp.md#saveconfig) | - | ✓ | ✓ | 2.1.0 |
| [`/resetDevice`](system-settings_jp.md#resetdevice) | - | ✓ | ✓ |  |

## モータドライバの設定

| コマンド | アーギュメント | STEP400 | STEP800 | 追加 |
| --- | --- | --- | --- | --- |
| [`/setMicrostepMode`](motor-driver-settings_jp.md#setmicrostepmode) | (int)motorID (int)STEP_SEL | ✓ | ✓ |  |
| [`/getMicrostepMode`](motor-driver-settings_jp.md#getmicrostepmode) | (int)motorID | ✓ | ✓ |  |
| [`/enableLowSpeedOptimize`](motor-driver-settings_jp.md#enablelowspeedoptimize) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/setLowSpeedOptimizeThreshold`](motor-driver-settings_jp.md#setlowspeedoptimizethreshold) | (int)motorID (float)lowSpeedOptimizationThreshold | ✓ | ✓ |  |
| [`/getLowSpeedOptimizeThreshold`](motor-driver-settings_jp.md#getlowspeedoptimizethreshold) | (int)motorID | ✓ | ✓ |  |
| [`/enableBusyReport`](motor-driver-settings_jp.md#enablebusyreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getBusy`](motor-driver-settings_jp.md#getbusy) | (int)motorID | ✓ | ✓ |  |
| [`/enableHizReport`](motor-driver-settings_jp.md#enablehizreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getHiZ`](motor-driver-settings_jp.md#gethiz) | (int)motorID | ✓ | ✓ |  |
| [`/enableDirReport`](motor-driver-settings_jp.md#enabledirreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getDir`](motor-driver-settings_jp.md#getdir) | (int)motorID | ✓ | ✓ |  |
| [`/enableMotorStatusReport`](motor-driver-settings_jp.md#enablemotorstatusreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getMotorStatus`](motor-driver-settings_jp.md#getmotorstatus) | (int)motorID | ✓ | ✓ |  |
| [`/setPositionReportInterval`](motor-driver-settings_jp.md#setpositionreportinterval) | (int)motorID (int)interval | ✓ | ✓ |  |
| [`/setPositionListReportInterval`](motor-driver-settings_jp.md#setpositionlistreportinterval) | (int)interval | ✓ | ✓ |  |
| [`/getAdcVal`](motor-driver-settings_jp.md#getadcval) | (int)motorID | ✓ |  |  |
| [`/getStatus`](motor-driver-settings_jp.md#getstatus) | (int)motorID | ✓ | ✓ |  |
| [`/getConfigRegister`](motor-driver-settings_jp.md#getconfigregister) | (int)motorID | ✓ | ✓ |  |
| [`/resetMotorDriver`](motor-driver-settings_jp.md#resetmotordriver) | (int)motorID | ✓ | ✓ |  |
| [`/getStatusList`](motor-driver-settings_jp.md#getstatuslist) | - | ✓ | ✓ |  |

## アラーム

| コマンド | アーギュメント | STEP400 | STEP800 | 追加 |
| --- | --- | --- | --- | --- |
| [`/enableUvloReport`](alarm-settings_jp.md#enableuvloreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getUvlo`](alarm-settings_jp.md#getuvlo) | (int)motorID | ✓ | ✓ |  |
| [`/enableThermalStatusReport`](alarm-settings_jp.md#enablethermalstatusreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getThermalStatus`](alarm-settings_jp.md#getthermalstatus) | (int)motorID | ✓ | ✓ |  |
| [`/enableOverCurrentReport`](alarm-settings_jp.md#enableovercurrentreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/setOverCurrentThreshold`](alarm-settings_jp.md#setovercurrentthreshold) | (int)motorID (int)OCD_TH | ✓ | ✓ |  |
| [`/getOverCurrentThreshold`](alarm-settings_jp.md#getovercurrentthreshold) | (int)motorID | ✓ | ✓ |  |
| [`/enableStallReport`](alarm-settings_jp.md#enablestallreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/setStallThreshold`](alarm-settings_jp.md#setstallthreshold) | (int)motorID (int)STALL_TH | ✓ | ✓ |  |
| [`/getStallThreshold`](alarm-settings_jp.md#getstallthreshold) | (int)motorID | ✓ | ✓ |  |
| [`/setProhibitMotionOnHomeSw`](alarm-settings_jp.md#setprohibitmotiononhomesw) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getProhibitMotionOnHomeSw`](alarm-settings_jp.md#getprohibitmotiononhomesw) | (int)motorID | ✓ | ✓ |  |
| [`/setProhibitMotionOnLimitSw`](alarm-settings_jp.md#setprohibitmotiononlimitsw) | (int)motorID (bool)enable | ✓ |  |  |
| [`/getProhibitMotionOnLimitSw`](alarm-settings_jp.md#getprohibitmotiononlimitsw) | (int)motorID | ✓ |  |  |

## 電圧モードと電流モード

| コマンド | アーギュメント | STEP400 | STEP800 | 追加 |
| --- | --- | --- | --- | --- |
| [`/setVoltageMode`](voltage-and-current-mode-settings_jp.md#setvoltagemode) | (int)motorID | ✓ |  |  |
| [`/setKval`](voltage-and-current-mode-settings_jp.md#setkval) | (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)decKVAL | ✓ | ✓ |  |
| [`/getKval`](voltage-and-current-mode-settings_jp.md#getkval) | (int)motorID | ✓ | ✓ |  |
| [`/setBemfParam`](voltage-and-current-mode-settings_jp.md#setbemfparam) | (int)motorID (int)INT_SPEED (int)ST_SLP (int)FN_SLP_ACC (int)FN_SLP_DEC | ✓ | ✓ |  |
| [`/getBemfParam`](voltage-and-current-mode-settings_jp.md#getbemfparam) | (int)motorID | ✓ | ✓ |  |
| [`/setHoldKval`](voltage-and-current-mode-settings_jp.md#setholdkval) | (int)motorID (int)holdKVAL | ✓ | ✓ |  |
| [`/setRunKval`](voltage-and-current-mode-settings_jp.md#setrunkval) | (int)motorID (int)runKVAL | ✓ | ✓ |  |
| [`/setAccKval`](voltage-and-current-mode-settings_jp.md#setacckval) | (int)motorID (int)accKVAL | ✓ | ✓ |  |
| [`/setDecKval`](voltage-and-current-mode-settings_jp.md#setdeckval) | (int)motorID (int)decKVAL | ✓ | ✓ |  |
| [`/setCurrentMode`](voltage-and-current-mode-settings_jp.md#setcurrentmode) | (int)motorID | ✓ |  |  |
| [`/setTval`](voltage-and-current-mode-settings_jp.md#settval) | (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL | ✓ |  |  |
| [`/getTval`](voltage-and-current-mode-settings_jp.md#gettval) | (int)motorID | ✓ |  |  |
| [`/getTval_mA`](voltage-and-current-mode-settings_jp.md#gettval_ma) | (int)motorID | ✓ |  |  |
| [`/setDecayModeParam`](voltage-and-current-mode-settings_jp.md#setdecaymodeparam) | (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN | ✓ |  |  |
| [`/getDecayModeParam`](voltage-and-current-mode-settings_jp.md#getdecaymodeparam) | (int)motorID | ✓ |  |  |
| [`/setHoldTval`](voltage-and-current-mode-settings_jp.md#setholdtval) | (int)motorID (int)holdTVAL | ✓ |  |  |
| [`/setRunTval`](voltage-and-current-mode-settings_jp.md#setruntval) | (int)motorID (int)runTVAL | ✓ |  |  |
| [`/setAccTval`](voltage-and-current-mode-settings_jp.md#setacctval) | (int)motorID (int)accTVAL | ✓ |  |  |
| [`/setDecTval`](voltage-and-current-mode-settings_jp.md#setdectval) | (int)motorID (int)decTVAL | ✓ |  |  |

## スピードプロファイル

| コマンド | アーギュメント | STEP400 | STEP800 | 追加 |
| --- | --- | --- | --- | --- |
| [`/setSpeedProfile`](speed-profile_jp.md#setspeedprofile) | (int)motorID (float)acc (float)dec (float)maxSpeed | ✓ | ✓ |  |
| [`/getSpeedProfile`](speed-profile_jp.md#getspeedprofile) | (int)motorID | ✓ | ✓ |  |
| [`/setFullstepSpeed`](speed-profile_jp.md#setfullstepspeed) | (int)motorID (float)fullstepSpeed | ✓ | ✓ |  |
| [`/getFullstepSpeed`](speed-profile_jp.md#getfullstepspeed) | (int)motorID | ✓ | ✓ |  |
| [`/setMaxSpeed`](speed-profile_jp.md#setmaxspeed) | (int)motorID (float)maxSpeed | ✓ | ✓ |  |
| [`/setAcc`](speed-profile_jp.md#setacc) | (int)motorID (float)acc | ✓ | ✓ |  |
| [`/setDec`](speed-profile_jp.md#setdec) | (int)motorID (float)dec | ✓ | ✓ |  |
| [`/setMinSpeed`](speed-profile_jp.md#setminspeed) | (int)motorID (float)minSpeed | ✓ | ✓ |  |
| [`/getMinSpeed`](speed-profile_jp.md#getminspeed) | (int)motorID | ✓ | ✓ |  |
| [`/getSpeed`](speed-profile_jp.md#getspeed) | (int)motorID | ✓ | ✓ |  |
| [`/setSpeedProfileRaw`](speed-profile_jp.md#setspeedprofileraw) | (int)motorID (int)acc (int)dec (int)maxSpeed | ✓ | ✓ |  |
| [`/getSpeedProfileRaw`](speed-profile_jp.md#getspeedprofileraw) | (int)motorID | ✓ | ✓ |  |
| [`/setMaxSpeedRaw`](speed-profile_jp.md#setmaxspeedraw) | (int)motorID (int)maxSpeed | ✓ | ✓ |  |
| [`/setMinSpeedRaw`](speed-profile_jp.md#setminspeedraw) | (int)motorID (int)minSpeed | ✓ | ✓ |  |
| [`/setFullstepSpeedRaw`](speed-profile_jp.md#setfullstepspeedraw) | (int)motorID (int)fullstepSpeed | ✓ | ✓ |  |
| [`/setAccRaw`](speed-profile_jp.md#setaccraw) | (int)motorID (int)acc | ✓ | ✓ |  |
| [`/setDecRaw`](speed-profile_jp.md#setdecraw) | (int)motorID (int)dec | ✓ | ✓ |  |

## 原点復帰

| コマンド | アーギュメント | STEP400 | STEP800 | 追加 |
| --- | --- | --- | --- | --- |
| [`/homing`](homing_jp.md#homing) | (int)motorID | ✓ | ✓ |  |
| [`/getHomingStatus`](homing_jp.md#gethomingstatus) | (int)motorID | ✓ | ✓ |  |
| [`/setHomingDirection`](homing_jp.md#sethomingdirection) | (int)motorID (bool)direction | ✓ | ✓ |  |
| [`/getHomingDirection`](homing_jp.md#gethomingdirection) | (int)motorID | ✓ | ✓ |  |
| [`/setHomingSpeed`](homing_jp.md#sethomingspeed) | (int)motorID (float)speed | ✓ | ✓ |  |
| [`/getHomingSpeed`](homing_jp.md#gethomingspeed) | (int)motorID | ✓ | ✓ |  |
| [`/goUntil`](homing_jp.md#gountil) | (int)motorID (bool)ACT (float)speed | ✓ | ✓ |  |
| [`/setGoUntilTimeout`](homing_jp.md#setgountiltimeout) | (int)motorID (int)timeOut | ✓ | ✓ |  |
| [`/getGoUntilTimeout`](homing_jp.md#getgountiltimeout) | (int)motorID | ✓ | ✓ |  |
| [`/releaseSw`](homing_jp.md#releasesw) | (int)motorID (bool)ACT (bool)DIR | ✓ | ✓ |  |
| [`/setReleaseSwTimeout`](homing_jp.md#setreleaseswtimeout) | (int)motorID (int)timeOut | ✓ | ✓ |  |
| [`/getReleaseSwTimeout`](homing_jp.md#getreleaseswtimeout) | (int)motorID | ✓ | ✓ |  |

## HOME/LIMITセンサ

| コマンド | アーギュメント | STEP400 | STEP800 | 追加 |
| --- | --- | --- | --- | --- |
| [`/enableHomeSwReport`](home-and-limit-sensers_jp.md#enablehomeswreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/enableSwEventReport`](home-and-limit-sensers_jp.md#enablesweventreport) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/getHomeSw`](home-and-limit-sensers_jp.md#gethomesw) | (int)motorID | ✓ | ✓ |  |
| [`/enableLimitSwReport`](home-and-limit-sensers_jp.md#enablelimitswreport) | (int)motorID (bool)enable | ✓ |  |  |
| [`/getLimitSw`](home-and-limit-sensers_jp.md#getlimitsw) | (int)motorID | ✓ |  |  |
| [`/setHomeSwMode`](home-and-limit-sensers_jp.md#sethomeswmode) | (int)motorID (bool)SW_MODE | ✓ | ✓ |  |
| [`/getHomeSwMode`](home-and-limit-sensers_jp.md#gethomeswmode) | (int)motorID | ✓ | ✓ |  |
| [`/setLimitSwMode`](home-and-limit-sensers_jp.md#setlimitswmode) | (int)motorID (bool)SW_MODE | ✓ |  |  |
| [`/getLimitSwMode`](home-and-limit-sensers_jp.md#getlimitswmode) | (int)motorID | ✓ |  |  |

## 座標

| コマンド | アーギュメント | STEP400 | STEP800 | 追加 |
| --- | --- | --- | --- | --- |
| [`/setPosition`](position-management_jp.md#setposition) | (int)motorID (int)newPosition | ✓ | ✓ |  |
| [`/getPosition`](position-management_jp.md#getposition) | (int)motorID | ✓ | ✓ |  |
| [`/getPositionList`](position-management_jp.md#getpositionlist) | - | ✓ | ✓ |  |
| [`/resetPos`](position-management_jp.md#resetpos) | (int)motorID | ✓ | ✓ |  |
| [`/setElPos`](position-management_jp.md#setelpos) | (int)motorID (int)newFullstep (int)newMicrostep | ✓ | ✓ |  |
| [`/getElPos`](position-management_jp.md#getelpos) | (int)motorID | ✓ | ✓ |  |
| [`/setMark`](position-management_jp.md#setmark) | (int)motorID (int)MARK | ✓ | ✓ |  |
| [`/getMark`](position-management_jp.md#getmark) | (int)motorID | ✓ | ✓ |  |
| [`/goHome`](position-management_jp.md#gohome) | (int)motorID | ✓ | ✓ |  |
| [`/goMark`](position-management_jp.md#gomark) | (int)motorID | ✓ | ✓ |  |

## モータの回転・停止

| コマンド | アーギュメント | STEP400 | STEP800 | 追加 |
| --- | --- | --- | --- | --- |
| [`/run`](motor-control_jp.md#run) | (int)motorID (float)speed | ✓ | ✓ |  |
| [`/move`](motor-control_jp.md#move) | (int)motorID (int)step | ✓ | ✓ |  |
| [`/goTo`](motor-control_jp.md#goto) | (int)motorID (int)position | ✓ | ✓ |  |
| [`/goToDir`](motor-control_jp.md#gotodir) | (int)motorID (bool)DIR (int)position | ✓ | ✓ |  |
| [`/softStop`](motor-control_jp.md#softstop) | (int)motorID | ✓ | ✓ |  |
| [`/hardStop`](motor-control_jp.md#hardstop) | (int)motorID | ✓ | ✓ |  |
| [`/softHiZ`](motor-control_jp.md#softhiz) | (int)motorID | ✓ | ✓ |  |
| [`/hardHiZ`](motor-control_jp.md#hardhiz) | (int)motorID | ✓ | ✓ |  |
| [`/combine/run`](motor-control_jp.md#combine-run) | (int)motorID1 (int)motorID2 (float)speed | ✓ | ✓ |  |
| [`/combine/move`](motor-control_jp.md#combine-move) | (int)motorID1 (int)motorID2 (int)step | ✓ | ✓ |  |
| [`/combine/goTo`](motor-control_jp.md#combine-goto) | (int)motorID1 (int)motorID2 (int)position | ✓ | ✓ |  |
| [`/combine/goToDir`](motor-control_jp.md#combine-gotodir) | (int)motorID1 (int)motorID2 (bool)DIR (int)position | ✓ | ✓ |  |
| [`/combine/softStop`](motor-control_jp.md#combine-softstop) | (int)motorID1 (int)motorID2 | ✓ | ✓ |  |
| [`/combine/hardStop`](motor-control_jp.md#combine-hardstop) | (int)motorID1 (int)motorID2 | ✓ | ✓ |  |
| [`/combine/softHiZ`](motor-control_jp.md#combine-softhiz) | (int)motorID1 (int)motorID2 | ✓ | ✓ |  |
| [`/combine/hardHiZ`](motor-control_jp.md#combine-hardhiz) | (int)motorID1 (int)motorID2 | ✓ | ✓ |  |
| [`/runRaw`](motor-control_jp.md#runraw) | (int)motorID (int)speed | ✓ | ✓ |  |
| [`/goUntilRaw`](motor-control_jp.md#gountilraw) | (int)motorID (bool)ACT (int)speed | ✓ | ✓ |  |
| [`/combine/runRaw`](motor-control_jp.md#combine-runraw) | (int)motorID1 (int)motorID2 (int)speed | ✓ | ✓ |  |

## 電磁ブレーキ

| コマンド | アーギュメント | STEP400 | STEP800 | 追加 |
| --- | --- | --- | --- | --- |
| [`/enableElectromagnetBrake`](brake_jp.md#enableelectromagnetbrake) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/activate`](brake_jp.md#activate) | (int)motorID (bool)state | ✓ | ✓ |  |
| [`/free`](brake_jp.md#free) | (int)motorID | ✓ | ✓ |  |
| [`/setBrakeTransitionDuration`](brake_jp.md#setbraketransitionduration) | (int)motorID (int)duration | ✓ | ✓ |  |
| [`/getBrakeTransitionDuration`](brake_jp.md#getbraketransitionduration) | (int)motorID | ✓ | ✓ |  |
| [`/getBrakeStatus`](brake_jp.md#getbrakestatus) | (int)motorID | ✓ | ✓ | 2.2.0 |

## サーボモード

| コマンド | アーギュメント | STEP400 | STEP800 | 追加 |
| --- | --- | --- | --- | --- |
| [`/enableServoMode`](servo-mode_reference_jp.md#enableservomode) | (int)motorID (bool)enable | ✓ | ✓ |  |
| [`/setServoParam`](servo-mode_reference_jp.md#setservoparam) | (int)motorID (float)kP (float)kI (float)kD | ✓ | ✓ |  |
| [`/getServoParam`](servo-mode_reference_jp.md#getservoparam) | (int)motorID | ✓ | ✓ |  |
| [`/setTargetPosition`](servo-mode_reference_jp.md#settargetposition) | (int)motorID (int)position | ✓ | ✓ |  |
| [`/setTargetPositionList`](servo-mode_reference_jp.md#settargetpositionlist) | (int)position1 ... (int)positionN | ✓ | ✓ |  |
