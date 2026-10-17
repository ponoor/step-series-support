---
title: 設定項目一覧
lang: ja
---

# 設定項目一覧

<!-- This page is generated from spec/osc-commands.yaml by tools/generate.py. Do not edit it directly. (自動生成・直接編集しない) -->

設定ファイル（microSD カードの JSON）の項目です。初期値は、設定ファイルまたはそのキーがないときの値です。

## information {#information}

| キー | 名称 | 型 | 初期値 | 範囲 / 単位 | コマンド | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="information-configname"></a>`configName` | Configuration name | string | Default (ファームウェア) / "" (テンプレート) |  | [`/setConfigName`](../reference/system-settings.md#setconfigname) | 設定ファイルの名称で、自由に設定できます。 |
| <a id="information-configversion"></a>`configVersion` | Configuration version | version | 0.0 (ファームウェア) / 1.2 (テンプレート) |  |  | Config Toolsのバージョン番号で、変更できません。 |
| <a id="information-targetproduct"></a>`targetProduct` | Target product | string | STEP400: --- (ファームウェア) / STEP400 (テンプレート); STEP800: --- (ファームウェア) / STEP800 (テンプレート) |  |  | 設定ファイルの対象機種名で、変更できません。 |

## network {#network}

| キー | 名称 | 型 | 初期値 | 範囲 / 単位 | コマンド | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="network-myip"></a>`myIp` | My IP address | ip | 10.0.0.100 |  |  | IPアドレスを設定します。`ID adds to my IP`にチェックが入っている場合は、この数値にIDが加算されたものが実際のIPアドレスになります。例えば`10.0.0.100`に設定してIDスイッチが1になっている場合は、`10.0.0.101`が実際のアドレスになります。加算した数値が254を超えないようにしてください。 |
| <a id="network-ismyipaddid"></a>`isMyIpAddId` | ID adds to my IP | bool | true |  |  | If the address with the ID added would be beyond .254 (ID 155 or more with the default 10.0.0.100), the ID is not added: the configured address is used and a warning is printed on USB serial. |
| <a id="network-destip"></a>`destIp` | Destination IP | ip | 10.0.0.10 |  | [`/setDestIp`](../reference/system-settings.md#setdestip) |  |
| <a id="network-dns"></a>`dns` | DNS | ip | 10.0.0.1 |  |  |  |
| <a id="network-gateway"></a>`gateway` | Gateway | ip | 10.0.0.1 |  |  |  |
| <a id="network-subnet"></a>`subnet` | Subnet mask | ip | 255.255.255.0 |  |  |  |
| <a id="network-inport"></a>`inPort` | Incoming port | int | 50000 |  |  | 本デバイスがOSCを受信するポート番号です。 |
| <a id="network-outport"></a>`outPort` | Outgoing port | int | 50100 |  |  | 本デバイスがOSCを送信するポート番号です。`ID adds to Outgoing port`にチェックが入っていると、この数値にIDが加算されます。 |
| <a id="network-isoutportaddid"></a>`isOutPortAddId` | ID adds to Outgoing port | bool | true |  |  | If the port with the ID added would be beyond 65535, the ID is not added: the configured port is used and a warning is printed on USB serial. |
| <a id="network-mac"></a>`mac` | MAC address | mac | STEP400: 60:95:CE:10:06:00 (ファームウェア) / 60:95:CE:10:02:00 (テンプレート); STEP800: 60:95:CE:10:06:00 (ファームウェア) / 60:95:CE:10:03:00 (テンプレート) |  |  | `Hex`チェックボックスで、16進数表示と10進数表示を切替できます。 |
| <a id="network-ismacaddid"></a>`isMacAddId` | ID adds to MAC address | bool | true |  |  | このチェックボックスが入っていると、MACアドレスの最終バイトにIDが加算されます。 |
| <a id="network-bootedmsgenable"></a>`bootedMsgEnable` | Booted message enable | bool | true |  |  | 起動時にイーサネットがリンクすると自動で送られる[`/booted`](../reference/automatically-sent-messages.md#booted)メッセージの有効無効を切り替えます。 |
| <a id="network-cansendmsgbeforedestip"></a>`canSendMsgBeforeDestIp` | Allow OSC reply before /setDestIp | bool | false |  |  | 初期状態では`/setDestIp`を受信するまではOSCの返送を行わないようになっていますが、このチェックボックスが入っていると、起動してすぐからOSC返送するようにします。 |
| <a id="network-reporterror"></a>`reportError` | Report errors | bool | true |  | [`/reportError`](../reference/system-settings.md#reporterror) |  |

## alarmAndReport {#alarmandreport}

| キー | 名称 | 型 | 初期値 | 範囲 / 単位 | コマンド | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="alarmandreport-reportbusy"></a>`reportBUSY` | Report BUSY (モータごと) | bool | false |  | [`/enableBusyReport`](../reference/motor-driver-settings.md#enablebusyreport) |  |
| <a id="alarmandreport-reporthiz"></a>`reportHiZ` | Report HiZ (モータごと) | bool | false |  | [`/enableHizReport`](../reference/motor-driver-settings.md#enablehizreport) |  |
| <a id="alarmandreport-reporthomeswstatus"></a>`reportHomeSwStatus` | Report HOME switch status (モータごと) | bool | false |  | [`/enableHomeSwReport`](../reference/home-and-limit-sensors.md#enablehomeswreport) |  |
| <a id="alarmandreport-reportlimitswstatus"></a>`reportLimitSwStatus` | Report LIMIT switch status (モータごと) (STEP400 のみ) | bool | false |  | [`/enableLimitSwReport`](../reference/home-and-limit-sensors.md#enablelimitswreport) |  |
| <a id="alarmandreport-reportdir"></a>`reportDir` | Report motor direction (モータごと) | bool | false |  | [`/enableDirReport`](../reference/motor-driver-settings.md#enabledirreport) |  |
| <a id="alarmandreport-reportmotorstatus"></a>`reportMotorStatus` | Report Motor Status (モータごと) | bool | false |  | [`/enableMotorStatusReport`](../reference/motor-driver-settings.md#enablemotorstatusreport) |  |
| <a id="alarmandreport-reportswevn"></a>`reportSwEvn` | Report HOME switch event (モータごと) | bool | false |  | [`/enableSwEventReport`](../reference/home-and-limit-sensors.md#enablesweventreport) |  |
| <a id="alarmandreport-reportuvlo"></a>`reportUVLO` | Report undervoltage lockout (モータごと) | bool | true |  | [`/enableUvloReport`](../reference/alarm-settings.md#enableuvloreport) |  |
| <a id="alarmandreport-reportthermalstatus"></a>`reportThermalStatus` | Report thermal status of driver chip (モータごと) | bool | true |  | [`/enableThermalStatusReport`](../reference/alarm-settings.md#enablethermalstatusreport) |  |
| <a id="alarmandreport-reportocd"></a>`reportOCD` | モータごと | bool | true |  | [`/enableOverCurrentReport`](../reference/alarm-settings.md#enableovercurrentreport) |  |
| <a id="alarmandreport-reportstall"></a>`reportStall` | Report motor stall detection (モータごと) | bool | false |  | [`/enableStallReport`](../reference/alarm-settings.md#enablestallreport) |  |
| <a id="alarmandreport-reportpositioninterval"></a>`reportPositionInterval` | モータごと | int | 0 | ms | [`/setPositionReportInterval`](../reference/motor-driver-settings.md#setpositionreportinterval) |  |
| <a id="alarmandreport-reportpositionlistinterval"></a>`reportPositionListInterval` |  | int | 0 | ms | [`/setPositionListReportInterval`](../reference/motor-driver-settings.md#setpositionlistreportinterval) |  |
| <a id="alarmandreport-octhreshold"></a>`OCThreshold` | Overcurrent threshold (モータごと) | int | STEP400: 15; STEP800: 7 (ファームウェア) / 15 (テンプレート) |  | [`/setOverCurrentThreshold`](../reference/alarm-settings.md#setovercurrentthreshold) |  |

## driverSettings {#driversettings}

| キー | 名称 | 型 | 初期値 | 範囲 / 単位 | コマンド | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="driversettings-homingatstartup"></a>`homingAtStartup` | Homing when the system starts (モータごと) | bool | false |  |  | このチェックボックスが入っていると、起動すると直ちに原点復帰動作を行います。 |
| <a id="driversettings-homingdirection"></a>`homingDirection` | Homing Direction (モータごと) | int | 0 (Reverse) |  | [`/setHomingDirection`](../reference/homing.md#sethomingdirection) |  |
| <a id="driversettings-homingspeed"></a>`homingSpeed` | Homing Speed (モータごと) | float | 50 | step/s | [`/setHomingSpeed`](../reference/homing.md#sethomingspeed) |  |
| <a id="driversettings-homeswmode"></a>`homeSwMode` | Home switch won't cause HardStop (モータごと) | bool | true |  | [`/setHomeSwMode`](../reference/home-and-limit-sensors.md#sethomeswmode) |  |
| <a id="driversettings-prohibitmotiononhomesw"></a>`prohibitMotionOnHomeSw` | Prohibit motions on HomeSw (モータごと) | bool | false |  | [`/setProhibitMotionOnHomeSw`](../reference/alarm-settings.md#setprohibitmotiononhomesw) |  |
| <a id="driversettings-limitswmode"></a>`limitSwMode` | Limit switch won't cause HardStop (モータごと) (STEP400 のみ) | bool | true |  | [`/setLimitSwMode`](../reference/home-and-limit-sensors.md#setlimitswmode) |  |
| <a id="driversettings-prohibitmotiononlimitsw"></a>`prohibitMotionOnLimitSw` | Prohibit motions on LimitSw (モータごと) (STEP400 のみ) | bool | false |  | [`/setProhibitMotionOnLimitSw`](../reference/alarm-settings.md#setprohibitmotiononlimitsw) |  |
| <a id="driversettings-gountiltimeout"></a>`goUntilTimeout` | goUntil timeout duration (モータごと) | int | 10000 | ms | [`/setGoUntilTimeout`](../reference/homing.md#setgountiltimeout) |  |
| <a id="driversettings-releaseswtimeout"></a>`releaseSwTimeout` | releaseSw timeout duration (モータごと) | int | 10000 | ms | [`/setReleaseSwTimeout`](../reference/homing.md#setreleaseswtimeout) |  |
| <a id="driversettings-stepmode"></a>`stepMode` | Microstepping mode (モータごと) | int | 7 |  | [`/setMicrostepMode`](../reference/motor-driver-settings.md#setmicrostepmode) |  |
| <a id="driversettings-iscurrentmode"></a>`isCurrentMode` | Current mode (モータごと) (STEP400 のみ) | bool | false |  | [`/setVoltageMode`](../reference/voltage-and-current-mode-settings.md#setvoltagemode), [`/setCurrentMode`](../reference/voltage-and-current-mode-settings.md#setcurrentmode) |  |
| <a id="driversettings-slewrate"></a>`slewRate` | Slew rate (モータごと) | int | STEP400: 5 (980V/us); STEP800: 2 (400V/us) | 0-5 (STEP400), 0-2 (STEP800) |  | モータドライバから出力されるモータ制御電流のスリューレート（立ち上がりの鋭さ）をSTEP400では6段階、STEP800では3段階で指定します。 |
| <a id="driversettings-electromagnetbrakeenable"></a>`electromagnetBrakeEnable` | Electromagnetic brake enable (モータごと) | bool | false |  | [`/enableElectromagnetBrake`](../reference/brake.md#enableelectromagnetbrake) |  |
| <a id="driversettings-braketransitionduration"></a>`brakeTransitionDuration` | Brake transition duration (モータごと) | int | 100 | 0-65535 ms | [`/setBrakeTransitionDuration`](../reference/brake.md#setbraketransitionduration) |  |

## speedProfile {#speedprofile}

| キー | 名称 | 型 | 初期値 | 範囲 / 単位 | コマンド | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="speedprofile-acc"></a>`acc` | Acceleration (モータごと) | float | 1000 (ファームウェア) / 2000 (テンプレート) | step/s/s | [`/setAcc`](../reference/speed-profile.md#setacc), [`/setSpeedProfile`](../reference/speed-profile.md#setspeedprofile) |  |
| <a id="speedprofile-dec"></a>`dec` | Deceleration (モータごと) | float | 1000 (ファームウェア) / 2000 (テンプレート) | step/s/s | [`/setDec`](../reference/speed-profile.md#setdec), [`/setSpeedProfile`](../reference/speed-profile.md#setspeedprofile) |  |
| <a id="speedprofile-maxspeed"></a>`maxSpeed` | Max speed (モータごと) | float | 650 (ファームウェア) / 620 (テンプレート) | step/s | [`/setMaxSpeed`](../reference/speed-profile.md#setmaxspeed), [`/setSpeedProfile`](../reference/speed-profile.md#setspeedprofile) |  |
| <a id="speedprofile-fullstepspeed"></a>`fullStepSpeed` | Transit to fullstep threshold speed (モータごと) | float | 15610 (ファームウェア) / 15625 (テンプレート) | step/s | [`/setFullstepSpeed`](../reference/speed-profile.md#setfullstepspeed) |  |
| <a id="speedprofile-minspeed"></a>`minSpeed` | モータごと | float | 0 | step/s | [`/setMinSpeed`](../reference/speed-profile.md#setminspeed) |  |

## voltageMode {#voltagemode}

| キー | 名称 | 型 | 初期値 | 範囲 / 単位 | コマンド | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="voltagemode-kval_hold"></a>`KVAL_HOLD` | KVAL_HOLD (モータごと) | int | 0 |  | [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval), [`/setHoldKval`](../reference/voltage-and-current-mode-settings.md#setholdkval) | With the electromagnetic brake enabled, KVAL_HOLD is raised to at least half of KVAL_RUN whenever the motor is energized again; the raised value replaces the stored setting (so `/saveConfig` saves it) and is returned by [`/getKval`](../reference/voltage-and-current-mode-settings.md#getkval). |
| <a id="voltagemode-kval_run"></a>`KVAL_RUN` | KVAL_RUN (モータごと) | int | 16 |  | [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval), [`/setRunKval`](../reference/voltage-and-current-mode-settings.md#setrunkval) |  |
| <a id="voltagemode-kval_acc"></a>`KVAL_ACC` | KVAL_ACC (モータごと) | int | 16 |  | [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval), [`/setAccKval`](../reference/voltage-and-current-mode-settings.md#setacckval) |  |
| <a id="voltagemode-kval_dec"></a>`KVAL_DEC` | KVAL_DEC (モータごと) | int | 16 |  | [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval), [`/setDecKval`](../reference/voltage-and-current-mode-settings.md#setdeckval) |  |
| <a id="voltagemode-int_speed"></a>`INT_SPEED` | INT_SPEED (モータごと) | int | 1032 |  | [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) |  |
| <a id="voltagemode-st_slp"></a>`ST_SLP` | ST_SLP (モータごと) | int | 25 |  | [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) |  |
| <a id="voltagemode-fn_slp_acc"></a>`FN_SLP_ACC` | FN_SLP_ACC (モータごと) | int | 41 |  | [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) |  |
| <a id="voltagemode-fn_slp_dec"></a>`FN_SLP_DEC` | FN_SLP_DEC (モータごと) | int | 41 |  | [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) |  |
| <a id="voltagemode-stall_th"></a>`STALL_TH` | STALL_TH (モータごと) | int | STEP400: 31; STEP800: 127 |  | [`/setStallThreshold`](../reference/alarm-settings.md#setstallthreshold) |  |
| <a id="voltagemode-lowspeedoptimizeenable"></a>`lowSpeedOptimizeEnable` | モータごと | bool | false |  | [`/enableLowSpeedOptimize`](../reference/motor-driver-settings.md#enablelowspeedoptimize) |  |
| <a id="voltagemode-lowspeedoptimize"></a>`lowSpeedOptimize` | lowSpeedOptimize (モータごと) | float | 20 | step/s | [`/setLowSpeedOptimizeThreshold`](../reference/motor-driver-settings.md#setlowspeedoptimizethreshold) |  |

## currentMode {#currentmode}

| キー | 名称 | 型 | 初期値 | 範囲 / 単位 | コマンド | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="currentmode-tval_hold"></a>`TVAL_HOLD` | TVAL_HOLD (モータごと) (STEP400 のみ) | int | 0 |  | [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval), [`/setHoldTval`](../reference/voltage-and-current-mode-settings.md#setholdtval) | With the electromagnetic brake enabled, TVAL_HOLD is raised to at least half of TVAL_RUN whenever the motor is energized again; the raised value replaces the stored setting (so `/saveConfig` saves it) and is returned by [`/getTval`](../reference/voltage-and-current-mode-settings.md#gettval). |
| <a id="currentmode-tval_run"></a>`TVAL_RUN` | TVAL_RUN (モータごと) (STEP400 のみ) | int | 16 |  | [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval), [`/setRunTval`](../reference/voltage-and-current-mode-settings.md#setruntval) |  |
| <a id="currentmode-tval_acc"></a>`TVAL_ACC` | TVAL_ACC (モータごと) (STEP400 のみ) | int | 16 |  | [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval), [`/setAccTval`](../reference/voltage-and-current-mode-settings.md#setacctval) |  |
| <a id="currentmode-tval_dec"></a>`TVAL_DEC` | TVAL_DEC (モータごと) (STEP400 のみ) | int | 16 |  | [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval), [`/setDecTval`](../reference/voltage-and-current-mode-settings.md#setdectval) |  |
| <a id="currentmode-t_fast"></a>`T_FAST` | T_FAST (モータごと) (STEP400 のみ) | int | 25 |  | [`/setDecayModeParam`](../reference/voltage-and-current-mode-settings.md#setdecaymodeparam) |  |
| <a id="currentmode-ton_min"></a>`TON_MIN` | TON_MIN (モータごと) (STEP400 のみ) | int | 41 |  | [`/setDecayModeParam`](../reference/voltage-and-current-mode-settings.md#setdecaymodeparam) |  |
| <a id="currentmode-toff_min"></a>`TOFF_MIN` | TOFF_MIN (モータごと) (STEP400 のみ) | int | 41 |  | [`/setDecayModeParam`](../reference/voltage-and-current-mode-settings.md#setdecaymodeparam) |  |

## servoMode {#servomode}

| キー | 名称 | 型 | 初期値 | 範囲 / 単位 | コマンド | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="servomode-kp"></a>`kP` | kP (モータごと) | float | 0.06 |  | [`/setServoParam`](../reference/servo-mode_reference.md#setservoparam) |  |
| <a id="servomode-ki"></a>`kI` | kI (モータごと) | float | 0 |  | [`/setServoParam`](../reference/servo-mode_reference.md#setservoparam) |  |
| <a id="servomode-kd"></a>`kD` | kD (モータごと) | float | 0 |  | [`/setServoParam`](../reference/servo-mode_reference.md#setservoparam) |  |
