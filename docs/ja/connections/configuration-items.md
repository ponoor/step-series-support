---
title: 設定項目一覧
lang: ja
---

# 設定項目一覧

<!-- This page is generated from spec/osc-commands.yaml by tools/generate.py. Do not edit it directly. (自動生成・直接編集しない) -->

設定ファイル（microSDカードのJSON）の項目です。初期値は、設定ファイルまたはそのキーがないときの値です。

## information {#information}

| キー / 名称 | 型 / 初期値 | 説明 |
| --- | --- | --- |
| <a id="information-configname"></a>`configName`<br>Configuration name | string<br>Default（ファームウェア）、""（テンプレート） | 設定ファイルの名称で、自由に設定できます。コマンド: [`/setConfigName`](../reference/system-settings.md#setconfigname) |
| <a id="information-configversion"></a>`configVersion`<br>Configuration version | version<br>0.0（ファームウェア）、1.2（テンプレート） | 設定ファイルの形式のバージョンです。これがない`.json`ファイルは受け付けられません（`config.txt`は、これがなくても受け付けられます）。変更できません。 |
| <a id="information-targetproduct"></a>`targetProduct`<br>Target product | string<br>STEP400: ---（ファームウェア）、STEP400（テンプレート）<br>STEP800: ---（ファームウェア）、STEP800（テンプレート） | 設定ファイルの対象機種名で、変更できません。 |

## network {#network}

| キー / 名称 | 型 / 初期値 | 説明 |
| --- | --- | --- |
| <a id="network-myip"></a>`myIp`<br>My IP address | ip<br>10.0.0.100 | IPアドレスを設定します。`ID adds to my IP`にチェックが入っている場合は、この数値にIDが加算されたものが実際のIPアドレスになります。例えば`10.0.0.100`に設定してIDスイッチが1になっている場合は、`10.0.0.101`が実際のアドレスになります。加算した数値が254を超えないようにしてください。 |
| <a id="network-ismyipaddid"></a>`isMyIpAddId`<br>ID adds to my IP | bool<br>true | IDを加算したアドレスが .254を超える場合（既定の10.0.0.100ではIDが155以上のとき）は、IDを加算せず、設定したアドレスをそのまま使い、USBシリアルにメッセージを表示します。 |
| <a id="network-destip"></a>`destIp`<br>Destination IP | ip<br>10.0.0.10 | コマンド: [`/setDestIp`](../reference/system-settings.md#setdestip) |
| <a id="network-dns"></a>`dns`<br>DNS | ip<br>10.0.0.1 |  |
| <a id="network-gateway"></a>`gateway`<br>Gateway | ip<br>10.0.0.1 |  |
| <a id="network-subnet"></a>`subnet`<br>Subnet mask | ip<br>255.255.255.0 |  |
| <a id="network-inport"></a>`inPort`<br>Incoming port | int<br>50000 | ボードがOSCを受信するポート番号です。 |
| <a id="network-outport"></a>`outPort`<br>Outgoing port | int<br>50100 | ボードがOSCを送信するポート番号です。`ID adds to Outgoing port`にチェックが入っていると、この数値にIDが加算されます。 |
| <a id="network-isoutportaddid"></a>`isOutPortAddId`<br>ID adds to Outgoing port | bool<br>true | IDを加算したポート番号が65535を超える場合は、IDを加算せず、設定したポート番号をそのまま使い、USBシリアルにメッセージを表示します。 |
| <a id="network-mac"></a>`mac`<br>MAC address | mac<br>STEP400: 60:95:CE:10:06:00（ファームウェア）、60:95:CE:10:02:00（テンプレート）<br>STEP800: 60:95:CE:10:06:00（ファームウェア）、60:95:CE:10:03:00（テンプレート） | `Hex`チェックボックスで、16進数表示と10進数表示を切替できます。 |
| <a id="network-ismacaddid"></a>`isMacAddId`<br>ID adds to MAC address | bool<br>true | このチェックボックスが入っていると、MACアドレスの最終バイトにIDが加算されます。 |
| <a id="network-bootedmsgenable"></a>`bootedMsgEnable`<br>Booted message enable | bool<br>true | 起動時にイーサネットがリンクすると自動で送られる[`/booted`](../reference/automatically-sent-messages.md#booted)メッセージの有効無効を切り替えます。 |
| <a id="network-cansendmsgbeforedestip"></a>`canSendMsgBeforeDestIp`<br>Allow OSC reply before /setDestIp | bool<br>false | 初期状態では`/setDestIp`を受信するまではOSCメッセージの送信を行わないようになっていますが、このチェックボックスが入っていると、起動してすぐからOSCメッセージを送信するようにします。v2.2.0の既知の問題: 動作中のボードは、「`/setDestIp`を受信したか」をこの設定と同じ値で持っています。`/setDestIp`を受信した後に設定を保存する（[`/saveConfig`](../reference/system-settings.md#saveconfig)、またはブラウザ設定ツールでの保存）と、カードに`true`が書かれます。ブラウザ設定ツールで`false`を書き込むと、使用中の値も`false`に戻り、`/setDestIp`を送り直すまで、ボードは返信を送りません。回避策: 保存の後に`/setDestIp`を送り直し、保存したファイルの値を確かめてください。 |
| <a id="network-reporterror"></a>`reportError`<br>Report errors | bool<br>true | コマンド: [`/reportError`](../reference/system-settings.md#reporterror) |

## alarmAndReport {#alarmandreport}

| キー / 名称 | 型 / 初期値 | 説明 |
| --- | --- | --- |
| <a id="alarmandreport-reportbusy"></a>`reportBUSY`<br>Report BUSY（モータごと） | bool<br>false | コマンド: [`/enableBusyReport`](../reference/motor-driver-settings.md#enablebusyreport) |
| <a id="alarmandreport-reporthiz"></a>`reportHiZ`<br>Report HiZ（モータごと） | bool<br>false | コマンド: [`/enableHizReport`](../reference/motor-driver-settings.md#enablehizreport) |
| <a id="alarmandreport-reporthomeswstatus"></a>`reportHomeSwStatus`<br>Report HOME switch status（モータごと） | bool<br>false | コマンド: [`/enableHomeSwReport`](../reference/home-and-limit-sensors.md#enablehomeswreport) |
| <a id="alarmandreport-reportlimitswstatus"></a>`reportLimitSwStatus`<br>Report LIMIT switch status（モータごと）（STEP400のみ） | bool<br>false | コマンド: [`/enableLimitSwReport`](../reference/home-and-limit-sensors.md#enablelimitswreport) |
| <a id="alarmandreport-reportdir"></a>`reportDir`<br>Report motor direction（モータごと） | bool<br>false | コマンド: [`/enableDirReport`](../reference/motor-driver-settings.md#enabledirreport) |
| <a id="alarmandreport-reportmotorstatus"></a>`reportMotorStatus`<br>Report Motor Status（モータごと） | bool<br>false | コマンド: [`/enableMotorStatusReport`](../reference/motor-driver-settings.md#enablemotorstatusreport) |
| <a id="alarmandreport-reportswevn"></a>`reportSwEvn`<br>Report HOME switch event（モータごと） | bool<br>false | コマンド: [`/enableSwEventReport`](../reference/home-and-limit-sensors.md#enablesweventreport) |
| <a id="alarmandreport-reportuvlo"></a>`reportUVLO`<br>Report undervoltage lockout（モータごと） | bool<br>true | コマンド: [`/enableUvloReport`](../reference/alarm-settings.md#enableuvloreport) |
| <a id="alarmandreport-reportthermalstatus"></a>`reportThermalStatus`<br>Report thermal status of driver chip（モータごと） | bool<br>true | コマンド: [`/enableThermalStatusReport`](../reference/alarm-settings.md#enablethermalstatusreport) |
| <a id="alarmandreport-reportocd"></a>`reportOCD`<br>Report overcurrent detection（モータごと） | bool<br>true | コマンド: [`/enableOverCurrentReport`](../reference/alarm-settings.md#enableovercurrentreport) |
| <a id="alarmandreport-reportstall"></a>`reportStall`<br>Report motor stall detection（モータごと） | bool<br>false | ストール検出は、モータが負荷に負けて回れなくなった状態を、ドライバが電流から検出する機能です。閾値（[`/setStallThreshold`](../reference/alarm-settings.md#setstallthreshold)）は、実際に流れている電流にできるだけ近く、少し上になるように探って決めます。脱調（ステップのずれ）程度の小さなずれは検出できませんが、位置が大きくずれたときには検出できることがあります。コマンド: [`/enableStallReport`](../reference/alarm-settings.md#enablestallreport) |
| <a id="alarmandreport-reportpositioninterval"></a>`reportPositionInterval`<br>Report position interval（モータごと） | int<br>0 | 範囲: 0-65535ms。各モータの位置を通知する間隔（[`/position`](../reference/automatically-sent-messages.md#position)）です。0にすると通知を止めます。設定ファイルの読み込み時（およびUSBシリアルからの書き込み時）には、範囲は検査されません。範囲外の値は、最大値の次を0として数え直した値になります（65536は0になって位置レポートが止まり、65537は1、-1は65535になります）。[`/setPositionReportInterval`](../reference/motor-driver-settings.md#setpositionreportinterval)は65535を超える値を`CommandIgnored`で拒否し、負の値では通知を止めます。コマンド: [`/setPositionReportInterval`](../reference/motor-driver-settings.md#setpositionreportinterval) |
| <a id="alarmandreport-reportpositionlistinterval"></a>`reportPositionListInterval`<br>Report position list interval | int<br>0 | 範囲: 0-65535ms。位置のリスト通知（[`/positionList`](../reference/automatically-sent-messages.md#positionlist)）の間隔です。0にすると通知を止めます。0より大きくすると、モータごとの位置レポート（[`/position`](../reference/automatically-sent-messages.md#position)）は止まります。設定ファイルの読み込み時（およびUSBシリアルからの書き込み時）には、範囲は検査されません。範囲外の値は、最大値の次を0として数え直した値になります（65536は0、65537は1、-1は65535になります）。[`/setPositionListReportInterval`](../reference/motor-driver-settings.md#setpositionlistreportinterval)は65535を超える値を`CommandIgnored`で拒否します。コマンド: [`/setPositionListReportInterval`](../reference/motor-driver-settings.md#setpositionlistreportinterval) |
| <a id="alarmandreport-octhreshold"></a>`OCThreshold`<br>Overcurrent threshold（モータごと） | int<br>STEP400: 15（5A）<br>STEP800: 7（3A） | コマンド: [`/setOverCurrentThreshold`](../reference/alarm-settings.md#setovercurrentthreshold) |

## driverSettings {#driversettings}

| キー / 名称 | 型 / 初期値 | 説明 |
| --- | --- | --- |
| <a id="driversettings-homingatstartup"></a>`homingAtStartup`<br>Homing when the system starts（モータごと） | bool<br>false | このチェックボックスが入っていると、起動すると直ちに原点復帰動作を行います。電磁ブレーキが有効なときは、[`/activate`](../reference/brake.md#activate)と同じようにブレーキを先に解放し、解放が終わってから原点復帰を始めます。**v2.2.0**: 電磁ブレーキが有効なときは、[`/activate`](../reference/brake.md#activate)と同じようにブレーキを先に解放し、解放が終わってから原点復帰を始めます。以前は、ブレーキが保持されたままだったため原点復帰が失敗し、原点復帰のタイムアウトで無励磁のモータに即停止が送られていました。 |
| <a id="driversettings-homingdirection"></a>`homingDirection`<br>Homing Direction（モータごと） | int<br>0（逆転方向） | 値: 1: 正転方向、0: 逆転方向。コマンド: [`/setHomingDirection`](../reference/homing.md#sethomingdirection) |
| <a id="driversettings-homingspeed"></a>`homingSpeed`<br>Homing Speed（モータごと） | float<br>50 | 単位: step/s。コマンド: [`/setHomingSpeed`](../reference/homing.md#sethomingspeed) |
| <a id="driversettings-homeswmode"></a>`homeSwMode`<br>Home switch won't cause HardStop（モータごと） | bool<br>true | コマンド: [`/setHomeSwMode`](../reference/home-and-limit-sensors.md#sethomeswmode) |
| <a id="driversettings-prohibitmotiononhomesw"></a>`prohibitMotionOnHomeSw`<br>Prohibit motions on HomeSw（モータごと） | bool<br>false | コマンド: [`/setProhibitMotionOnHomeSw`](../reference/alarm-settings.md#setprohibitmotiononhomesw) |
| <a id="driversettings-limitswmode"></a>`limitSwMode`<br>Limit switch won't cause HardStop（モータごと）（STEP400のみ） | bool<br>true | コマンド: [`/setLimitSwMode`](../reference/home-and-limit-sensors.md#setlimitswmode) |
| <a id="driversettings-prohibitmotiononlimitsw"></a>`prohibitMotionOnLimitSw`<br>Prohibit motions on LimitSw（モータごと）（STEP400のみ） | bool<br>false | コマンド: [`/setProhibitMotionOnLimitSw`](../reference/alarm-settings.md#setprohibitmotiononlimitsw) |
| <a id="driversettings-gountiltimeout"></a>`goUntilTimeout`<br>goUntil timeout duration（モータごと） | int<br>10000 | 単位: ms。コマンド: [`/setGoUntilTimeout`](../reference/homing.md#setgountiltimeout) |
| <a id="driversettings-releaseswtimeout"></a>`releaseSwTimeout`<br>releaseSw timeout duration（モータごと） | int<br>10000 | 単位: ms。コマンド: [`/setReleaseSwTimeout`](../reference/homing.md#setreleaseswtimeout) |
| <a id="driversettings-stepmode"></a>`stepMode`<br>Microstepping mode（モータごと） | int<br>7 | コマンド: [`/setMicrostepMode`](../reference/motor-driver-settings.md#setmicrostepmode) |
| <a id="driversettings-iscurrentmode"></a>`isCurrentMode`<br>Current mode（モータごと）（STEP400のみ） | bool<br>false | コマンド: [`/setVoltageMode`](../reference/voltage-and-current-mode-settings.md#setvoltagemode)、[`/setCurrentMode`](../reference/voltage-and-current-mode-settings.md#setcurrentmode) |
| <a id="driversettings-slewrate"></a>`slewRate`<br>Slew rate（モータごと） | int<br>STEP400: 5（980V/us）<br>STEP800: 2（530V/us） | 範囲: 0-5（STEP400）、0-2（STEP800）<br>STEP400: 0: 114V/us、1: 220V/us、2: 400V/us、3: 520V/us、4: 790V/us、5: 980V/us<br>STEP800: 0: 180V/us、1: 290V/us、2: 530V/us。モータドライバから出力されるモータ制御電流のスリューレート（立ち上がりの鋭さ）をSTEP400では6段階、STEP800では3段階で指定します。設定ファイルの範囲外の値は拒否されず、範囲内に制限されます（負の値は0、大きい値は最大の値になります）。 |
| <a id="driversettings-electromagnetbrakeenable"></a>`electromagnetBrakeEnable`<br>Electromagnetic brake enable（モータごと） | bool<br>false | コマンド: [`/enableElectromagnetBrake`](../reference/brake.md#enableelectromagnetbrake) |
| <a id="driversettings-braketransitionduration"></a>`brakeTransitionDuration`<br>Brake transition duration（モータごと） | int<br>100 | 範囲: 0-65535ms。電磁ブレーキの解放や保持を待つ時間です。[`/setBrakeTransitionDuration`](../reference/brake.md#setbraketransitionduration)を参照してください。設定ファイルの読み込み時（およびUSBシリアルからの書き込み時）には、範囲は検査されません。範囲外の値は、最大値の次を0として数え直した値になります（65536は0、65537は1、-1は65535になります）。[`/setBrakeTransitionDuration`](../reference/brake.md#setbraketransitionduration)はこのような値を`CommandIgnored`で拒否します。コマンド: [`/setBrakeTransitionDuration`](../reference/brake.md#setbraketransitionduration) |

## speedProfile {#speedprofile}

| キー / 名称 | 型 / 初期値 | 説明 |
| --- | --- | --- |
| <a id="speedprofile-acc"></a>`acc`<br>Acceleration（モータごと） | float<br>1000（ファームウェア）、2000（テンプレート） | 単位: step/s/s。コマンド: [`/setAcc`](../reference/speed-profile.md#setacc)、[`/setSpeedProfile`](../reference/speed-profile.md#setspeedprofile) |
| <a id="speedprofile-dec"></a>`dec`<br>Deceleration（モータごと） | float<br>1000（ファームウェア）、2000（テンプレート） | 単位: step/s/s。コマンド: [`/setDec`](../reference/speed-profile.md#setdec)、[`/setSpeedProfile`](../reference/speed-profile.md#setspeedprofile) |
| <a id="speedprofile-maxspeed"></a>`maxSpeed`<br>Max speed（モータごと） | float<br>650（ファームウェア）、620（テンプレート） | 単位: step/s。コマンド: [`/setMaxSpeed`](../reference/speed-profile.md#setmaxspeed)、[`/setSpeedProfile`](../reference/speed-profile.md#setspeedprofile) |
| <a id="speedprofile-fullstepspeed"></a>`fullStepSpeed`<br>Transit to fullstep threshold speed（モータごと） | float<br>15610（ファームウェア）、15625（テンプレート） | 単位: step/s。コマンド: [`/setFullstepSpeed`](../reference/speed-profile.md#setfullstepspeed) |
| <a id="speedprofile-minspeed"></a>`minSpeed`<br>Minimum speed（モータごと） | float<br>0 | 単位: step/s。コマンド: [`/setMinSpeed`](../reference/speed-profile.md#setminspeed) |

## voltageMode {#voltagemode}

| キー / 名称 | 型 / 初期値 | 説明 |
| --- | --- | --- |
| <a id="voltagemode-kval_hold"></a>`KVAL_HOLD`<br>KVAL_HOLD（モータごと） | int<br>0 | 電磁ブレーキが有効なとき、モータが再び励磁されるたびに、KVAL_HOLDがKVAL_RUNの半分以上に引き上げられます。引き上げられた値は保存されている設定を置き換えるため（`/saveConfig`で保存されます）、[`/getKval`](../reference/voltage-and-current-mode-settings.md#getkval)でも返されます。コマンド: [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval)、[`/setHoldKval`](../reference/voltage-and-current-mode-settings.md#setholdkval) |
| <a id="voltagemode-kval_run"></a>`KVAL_RUN`<br>KVAL_RUN（モータごと） | int<br>16 | コマンド: [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval)、[`/setRunKval`](../reference/voltage-and-current-mode-settings.md#setrunkval) |
| <a id="voltagemode-kval_acc"></a>`KVAL_ACC`<br>KVAL_ACC（モータごと） | int<br>16 | コマンド: [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval)、[`/setAccKval`](../reference/voltage-and-current-mode-settings.md#setacckval) |
| <a id="voltagemode-kval_dec"></a>`KVAL_DEC`<br>KVAL_DEC（モータごと） | int<br>16 | コマンド: [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval)、[`/setDecKval`](../reference/voltage-and-current-mode-settings.md#setdeckval) |
| <a id="voltagemode-int_speed"></a>`INT_SPEED`<br>INT_SPEED（モータごと） | int<br>1032 | コマンド: [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) |
| <a id="voltagemode-st_slp"></a>`ST_SLP`<br>ST_SLP（モータごと） | int<br>25 | コマンド: [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) |
| <a id="voltagemode-fn_slp_acc"></a>`FN_SLP_ACC`<br>FN_SLP_ACC（モータごと） | int<br>41 | コマンド: [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) |
| <a id="voltagemode-fn_slp_dec"></a>`FN_SLP_DEC`<br>FN_SLP_DEC（モータごと） | int<br>41 | コマンド: [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) |
| <a id="voltagemode-stall_th"></a>`STALL_TH`<br>STALL_TH（モータごと） | int<br>STEP400: 31（10A）<br>STEP800: 127（4A） | コマンド: [`/setStallThreshold`](../reference/alarm-settings.md#setstallthreshold) |
| <a id="voltagemode-lowspeedoptimizeenable"></a>`lowSpeedOptimizeEnable`<br>Low speed optimize enable（モータごと） | bool<br>false | コマンド: [`/enableLowSpeedOptimize`](../reference/motor-driver-settings.md#enablelowspeedoptimize) |
| <a id="voltagemode-lowspeedoptimize"></a>`lowSpeedOptimize`<br>lowSpeedOptimize（モータごと） | float<br>20 | 単位: step/s。コマンド: [`/setLowSpeedOptimizeThreshold`](../reference/motor-driver-settings.md#setlowspeedoptimizethreshold) |

## currentMode {#currentmode}

| キー / 名称 | 型 / 初期値 | 説明 |
| --- | --- | --- |
| <a id="currentmode-tval_hold"></a>`TVAL_HOLD`<br>TVAL_HOLD（モータごと）（STEP400のみ） | int<br>0（78.125mA） | 電磁ブレーキが有効なとき、モータが再び励磁されるたびに、TVAL_HOLDがTVAL_RUNの半分以上に引き上げられます。引き上げられた値は保存されている設定を置き換えるため（`/saveConfig`で保存されます）、[`/getTval`](../reference/voltage-and-current-mode-settings.md#gettval)でも返されます。コマンド: [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval)、[`/setHoldTval`](../reference/voltage-and-current-mode-settings.md#setholdtval) |
| <a id="currentmode-tval_run"></a>`TVAL_RUN`<br>TVAL_RUN（モータごと）（STEP400のみ） | int<br>16（1.328A） | コマンド: [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval)、[`/setRunTval`](../reference/voltage-and-current-mode-settings.md#setruntval) |
| <a id="currentmode-tval_acc"></a>`TVAL_ACC`<br>TVAL_ACC（モータごと）（STEP400のみ） | int<br>16（1.328A） | コマンド: [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval)、[`/setAccTval`](../reference/voltage-and-current-mode-settings.md#setacctval) |
| <a id="currentmode-tval_dec"></a>`TVAL_DEC`<br>TVAL_DEC（モータごと）（STEP400のみ） | int<br>16（1.328A） | コマンド: [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval)、[`/setDecTval`](../reference/voltage-and-current-mode-settings.md#setdectval) |
| <a id="currentmode-t_fast"></a>`T_FAST`<br>T_FAST（モータごと）（STEP400のみ） | int<br>25 | コマンド: [`/setDecayModeParam`](../reference/voltage-and-current-mode-settings.md#setdecaymodeparam) |
| <a id="currentmode-ton_min"></a>`TON_MIN`<br>TON_MIN（モータごと）（STEP400のみ） | int<br>41 | コマンド: [`/setDecayModeParam`](../reference/voltage-and-current-mode-settings.md#setdecaymodeparam) |
| <a id="currentmode-toff_min"></a>`TOFF_MIN`<br>TOFF_MIN（モータごと）（STEP400のみ） | int<br>41 | コマンド: [`/setDecayModeParam`](../reference/voltage-and-current-mode-settings.md#setdecaymodeparam) |

## servoMode {#servomode}

| キー / 名称 | 型 / 初期値 | 説明 |
| --- | --- | --- |
| <a id="servomode-kp"></a>`kP`<br>kP（モータごと） | float<br>0.06 | コマンド: [`/setServoParam`](../reference/servo-mode_reference.md#setservoparam) |
| <a id="servomode-ki"></a>`kI`<br>kI（モータごと） | float<br>0 | コマンド: [`/setServoParam`](../reference/servo-mode_reference.md#setservoparam) |
| <a id="servomode-kd"></a>`kD`<br>kD（モータごと） | float<br>0 | コマンド: [`/setServoParam`](../reference/servo-mode_reference.md#setservoparam) |
