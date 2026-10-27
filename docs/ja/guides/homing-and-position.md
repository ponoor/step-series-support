---
title: 原点復帰と位置管理
---

# 原点復帰と位置管理

ステッピングモータは、ボードが起動した時点では自分の位置を知りません。このページでは、なぜ原点復帰が必要か、HOMEスイッチとLIMITスイッチをどう使うか、原点復帰のコマンドの動き、位置を管理するときの注意を説明します。

## ステッピングモータと原点復帰 {#why-homing}

システムの電源投入時は、モータが現在どの位置で止まっているかが不明です。前回電源を切ったときのタイミング次第で、いろいろな方向を向いている可能性があります。

また、ステッピングモータは、限界を超える外力がかかると、ステップがずれてしまいます（**ストール**）。そうなると、プログラム上の位置と物理的な位置がずれたまま動き続けてしまいます。

そのため、位置や向きがある使い方の場合は、起動時に、あるいは定期的に、センサを使って基準位置を検出する必要があります。この動作を**原点復帰**と呼びます。

ボードが再起動したあとと、モータが無励磁になったあとは、原点復帰をやり直してください。位置が信頼できなくなっています。電磁ブレーキのモータでは特に重要です。[電磁ブレーキ](electromagnetic-brake.md#usage)をご覧ください。

## センサとスイッチ {#switches}

![原点センサの2つの構成](http://ponoor.com/manage/wp-content/uploads/2020/10/two-homing-sensors.png)

原点センサには、フォトインタラプタがよく使われます。左は、スライダに取り付けた白い樹脂がフォトインタラプタの発光部と受光部の間を遮る構成です。右は回転テーブルの例で、フォトインタラプタが黒いねじに反応します。ほかにも、マイクロスイッチや光電センサが使われます。

## HOMEスイッチとLIMITスイッチ {#home-limit}

STEP400とSTEP800の各軸には、センサやスイッチをつなげるHOME端子があり、センサ用の5V電源も供給されています。STEP400には、HOME端子に加えてLIMIT端子もあります。端子につないだセンサやスイッチを、HOMEスイッチ、LIMITスイッチと呼びます。ピン配置と、スイッチやセンサのつなぎ方は、[センサとスイッチ](../connections/sensors-and-switches.md)をご覧ください。

### HOME {#home}

HOME端子はモータドライバに直接つながっていて、ドライバの原点復帰の機能と組み合わせて使えます。通常は、原点センサに使います。

### LIMIT（STEP400のみ） {#limit}

使い方によっては、センサが2つ必要になります。例えばスライダは動作範囲が限られているため、動作中にストールすると、どちらかの端にぶつかるおそれがあります。両端にセンサを置くと、衝突を防げます。

スイッチがオンになったときに、モータを強制的に停止する設定ができます。また、モータの動作とは切り離して、単なる入力としても使えます。例えば押しボタンをつないで、押されたらOSCメッセージで通知する、という使い方もできます。

入力がLowのときに、スイッチはオンです。原点位置で、センサの信号がHIGHからLOWになるように、機構とセンサを組み合わせてください（センサと配線は、[センサとスイッチ](../connections/sensors-and-switches.md)をご覧ください）。スイッチがオンになったときにボードが何をするかは、[`/setHomeSwMode`](../reference/home-and-limit-sensors.md#sethomeswmode)と[`/setLimitSwMode`](../reference/home-and-limit-sensors.md#setlimitswmode)で設定します。

### 即停止モードと`SW_USER` {#sw-mode}

HOMEスイッチ（STEP400ではLIMITスイッチも）の設定は、`SW_HARD_STOP`か`SW_USER`のどちらかです。[`/setHomeSwMode`](../reference/home-and-limit-sensors.md#sethomeswmode)と[`/setLimitSwMode`](../reference/home-and-limit-sensors.md#setlimitswmode)をご覧ください。`SW_HARD_STOP`では、スイッチがオンになった瞬間に、モータを即停止します。動作の向きは見ません。スイッチから離れる向きに動いているモータも止まります。向きを制限したいときは、次の衝突防止の設定を使ってください。

### 衝突防止の設定 {#collision-prevention}

HOMEスイッチやLIMITスイッチがオンのときに、モータが回転できる向きを制限できます。[`/setProhibitMotionOnHomeSw`](../reference/alarm-settings.md#setprohibitmotiononhomesw)と[`/setProhibitMotionOnLimitSw`](../reference/alarm-settings.md#setprohibitmotiononlimitsw)で、HOMEスイッチがオンのときは`homingDirection`の向きへの動作を、LIMITスイッチがオンのときは`homingDirection`と逆向きへの動作を禁止できます。誤ったコマンドで機構がぶつかるのを防げます。条件を満たさない動作コマンドは、`HomeSwActivating`か`LimitSwActivating`で拒否されます。[動作開始条件](../reference/index.md#motion-start-condition)をご覧ください。

[`/goTo`](../reference/motor-control.md#goto)、[`/goHome`](../reference/position-management.md#gohome)、[`/goMark`](../reference/position-management.md#gomark)、[`/goToDir`](../reference/motor-control.md#gotodir)では、動作の向きは、ドライバが目標までに通る向き（最短の向き。範囲の端を越えて回り込む場合も含みます）で判定します。v2.2.0より前は、目標が近いときにこの向きを誤って判定し、スイッチから離れる向きの短い移動が拒否されていました。

`homingDirection`は、[`/setHomingDirection`](../reference/homing.md#sethomingdirection)か設定ツールで設定します。[`/homing`](../reference/homing.md#homing)でも使われます。

![原点復帰の方向](https://ponoor.com/cms/wp-content/uploads/2020/08/homingDirection-800x533.jpg)

## 原点復帰コマンド {#homing-commands}

原点復帰のコマンドは[`/homing`](../reference/homing.md#homing)です。モータドライバから引き継いだ[`/goUntil`](../reference/homing.md#gountil)と[`/releaseSw`](../reference/homing.md#releasesw)の2つのコマンドを組み合わせたものです。まず、この2つのコマンドの動きを見ます。

### `/goUntil` {#gountil}

最初に、[`/goUntil`](../reference/homing.md#gountil)で原点センサに向かって移動します。センサがオンになると、（そのように設定している場合は）モータが減速して停止します。

### `/releaseSw` {#releasesw}

[`/releaseSw`](../reference/homing.md#releasesw)は、現在位置から逆向きにゆっくり移動し、センサがオフになったところで即座に停止します。モータが停止した位置が原点です。ただし厳密には、`/goUntil`はセンサがオンになった瞬間に停止するのではなく、減速して停止します。このため、センサが反応した点から少しずれた位置で止まります。これはファームウェアでは補正しません。環境によって異なるためです。

どちらのコマンドも、センサがオンになった瞬間に現在位置を0にリセットする設定にできます。[`/setHomeSwMode`](../reference/home-and-limit-sensors.md#sethomeswmode)をご覧ください。

### `/homing` {#homing}

2つのコマンドをOSCで続けて送ることもできますが、[`/homing`](../reference/homing.md#homing)は、この手順を1つのコマンドで実行します。[ブラウザ設定ツール](../connections/browser-config-tool.md)や、[`/setHomingDirection`](../reference/homing.md#sethomingdirection)と[`/setHomingSpeed`](../reference/homing.md#sethomingspeed)で、あらかじめ設定した原点復帰の方向と速度に従って、原点復帰の手順が自動で完了します。

進行は[`/homingStatus`](../reference/automatically-sent-messages.md#homingstatus)で通知されます（[`/getHomingStatus`](../reference/homing.md#gethomingstatus)で問い合わせられます）。`/releaseSw`が終わると`HOMING_COMPLETED`で、タイムアウトになると（次の項）`HOMING_TIMEOUT`で終わります。値は[`/homingStatus`](../reference/automatically-sent-messages.md#homingstatus)に載せています。原点復帰の途中で動作コマンドを送ると、原点復帰の状態は消えます。

モータがサーボモードのときは、[`/goUntil`](../reference/homing.md#gountil)、[`/goUntilRaw`](../reference/motor-control.md#gountilraw)、[`/releaseSw`](../reference/homing.md#releasesw)は`InServoMode`で拒否されます。モータのブレーキが解放されていないときは、[`/homing`](../reference/homing.md#homing)は`BrakeEngaged`で拒否されます。

### タイムアウト {#timeouts}

`/goUntil`と`/releaseSw`には、それぞれタイムアウトを設定できます（[`/setGoUntilTimeout`](../reference/homing.md#setgountiltimeout)、[`/setReleaseSwTimeout`](../reference/homing.md#setreleaseswtimeout)）。この時間内にセンサの状態が変わらなかったときは、ボードはモータを即停止し、`/error/command GoUntilTimeout`か`ReleaseSwTimeout`を送ります。センサが反応しなくなったときに、機構が行き止まりに押し当てられ続けるのを防ぎます。

### 起動時の原点復帰 {#homing-at-startup}

[`driverSettings.homingAtStartup`](../connections/configuration-items.md#driversettings-homingatstartup)を設定すると、起動後にボードが原点復帰を始めます。電磁ブレーキのモータでは、先にブレーキを解放し、解放されてから原点復帰を始めます。

## 回転テーブルの場合 {#rotary-tables}

原点センサの2つの構成の写真の右にある回転テーブルでは、時計回りの場合と反時計回りの場合で、原点センサが反応する位置が、穴のサイズ分だけずれます。ボードは、原点センサのHIGHからLOWへの変化と、LOWからHIGHへの変化の、どちらもOSCメッセージで通知できます。メッセージには回転方向も含まれているので、回転方向ごとに場合分けすれば、原点位置をそろえられます。この通知は[`/enableHomeSwReport`](../reference/home-and-limit-sensors.md#enablehomeswreport)で有効にします。

## 位置管理 {#position}

- [`/setPosition`](../reference/position-management.md#setposition)と[`/resetPos`](../reference/position-management.md#resetpos)は、ボードが持つ位置を変更します。**サーボモード中や動作中には使わないでください。** ボードはこれを防ぐ処理をしていないため、モータが思わぬ動きをすることがあります。
- [`/setMark`](../reference/position-management.md#setmark)は、[`/goMark`](../reference/position-management.md#gomark)が向かう位置を記憶します。
- マイクロステップの設定が変わると、座標系も変わります。[電圧モードと電流モード](voltage-and-current-mode.md#switching)をご覧ください。

## 関連するコマンドと設定項目 {#related}

<!-- osc-related: homing, sensors, position, /setProhibitMotionOnHomeSw, /setProhibitMotionOnLimitSw -->
<!-- generated:begin osc-related homing, sensors, position, /setProhibitMotionOnHomeSw, /setProhibitMotionOnLimitSw -->
**関連するコマンド**

| コマンド | 引数 | 説明 |
| --- | --- | --- |
| [`/homing`](../reference/homing.md#homing) | (int)motorID | 原点復帰動作を行います。原点復帰方向に移動し、HOMEスイッチがオンになると停止し、方向を反転してゆっくり移動し、HOMEスイッチがオフになった時点で停止し、現在位置を0にします。 |
| [`/getHomingStatus`](../reference/homing.md#gethomingstatus) | (int)motorID | 原点復帰の現在の状態を返します。 |
| [`/setHomingDirection`](../reference/homing.md#sethomingdirection) | (int)motorID (bool)direction | `/homing`実行時の原点復帰方向`homingDirection`を指定します。configToolからも指定できます。 |
| [`/getHomingDirection`](../reference/homing.md#gethomingdirection) | (int)motorID | `homingDirection`を取得します。 |
| [`/setHomingSpeed`](../reference/homing.md#sethomingspeed) | (int)motorID (float)speed | `/homing`実行時の原点復帰の速度`homingSpeed`を指定します。configToolからも指定できます。 |
| [`/getHomingSpeed`](../reference/homing.md#gethomingspeed) | (int)motorID | `homingSpeed`を取得します。 |
| [`/goUntil`](../reference/homing.md#gountil) | (int)motorID (bool)ACT (float)speed | 指定の速度で回転し、HOMEスイッチがオンになるとACTの値に応じた処理を行います。 |
| [`/setGoUntilTimeout`](../reference/homing.md#setgountiltimeout) | (int)motorID (int)timeOut | `/goUntil`実行時のタイムアウト時間を指定します。この時間内にスイッチがオンにならなかった場合にはtimeoutとして動作を中止します。0を指定するとタイムアウトが無効になります。configToolからも指定できます。 |
| [`/getGoUntilTimeout`](../reference/homing.md#getgountiltimeout) | (int)motorID | `/goUntil`実行時のタイムアウト時間を取得します。 |
| [`/releaseSw`](../reference/homing.md#releasesw) | (int)motorID (bool)ACT (bool)DIR | 指定方向にminimum speed（初期状態では5[step/s]）で回転し、HOMEスイッチがオフになると、ACTの値に応じた処理を行います。ACTの処理内容は`/goUntil`と同じです。その後hardStopします。 |
| [`/setReleaseSwTimeout`](../reference/homing.md#setreleaseswtimeout) | (int)motorID (int)timeOut | `/releaseSw`実行時のタイムアウト時間を指定します。この時間内にスイッチがオフにならなかった場合にはtimeoutとして動作を中止します。0を指定するとタイムアウトが無効になります。configToolからも指定できます。 |
| [`/getReleaseSwTimeout`](../reference/homing.md#getreleaseswtimeout) | (int)motorID | `/releaseSw`実行時のタイムアウト時間を取得します。 |
| [`/enableHomeSwReport`](../reference/home-and-limit-sensors.md#enablehomeswreport) | (int)motorID (bool)enable | 指定したモータのHOME端子の状態に変化があったら自動でメッセージを送信する設定を行います。送信されるメッセージは`/getHomeSw`の返信と同じです。 |
| [`/enableSwEventReport`](../reference/home-and-limit-sensors.md#enablesweventreport) | (int)motorID (bool)enable | 指定したモータのHOME端子の状態がHIGHレベルからLOWレベルに遷移した際（Falling Edge）に自動でメッセージを送信する設定を行います。 |
| [`/getHomeSw`](../reference/home-and-limit-sensors.md#gethomesw) | (int)motorID | HOMEスイッチの状態を取得します。 |
| [`/enableLimitSwReport`](../reference/home-and-limit-sensors.md#enablelimitswreport) | (int)motorID (bool)enable | 指定したモータのLIMIT端子の状態に変化があったら自動でメッセージを送信する設定を行います。送信されるメッセージは`/getLimitSw`の返信と同じです。 |
| [`/getLimitSw`](../reference/home-and-limit-sensors.md#getlimitsw) | (int)motorID | LIMITスイッチの状態を取得します。 |
| [`/setHomeSwMode`](../reference/home-and-limit-sensors.md#sethomeswmode) | (int)motorID (bool)SW_MODE | HOME端子に入力があった際に即停止するかどうか（Switch mode）を指定します。 |
| [`/getHomeSwMode`](../reference/home-and-limit-sensors.md#gethomeswmode) | (int)motorID | 上記のSwitch modeを取得します。 |
| [`/setLimitSwMode`](../reference/home-and-limit-sensors.md#setlimitswmode) | (int)motorID (bool)SW_MODE | LIMIT端子に入力があった際に即停止するかどうか（Switch mode）を指定します。 |
| [`/getLimitSwMode`](../reference/home-and-limit-sensors.md#getlimitswmode) | (int)motorID | 上記のSwitch modeを取得します。 |
| [`/setPosition`](../reference/position-management.md#setposition) | (int)motorID (int)newPosition | ABS_POSレジスタを指定座標に書き換えます。現在のモータ位置が指定座標になります。 |
| [`/getPosition`](../reference/position-management.md#getposition) | (int)motorID | ABS_POSレジスタの内容（現在位置）を取得します。 |
| [`/getPositionList`](../reference/position-management.md#getpositionlist) | - | 全モータの現在位置（`ABS_POS`）を取得します。`/getPosition 255`を送信した場合は、モータの軸数分の個別のメッセージが返されますが、このコマンドは、すべてのモータの位置をリストにまとめた1個のメッセージが返されます。 |
| [`/resetPos`](../reference/position-management.md#resetpos) | (int)motorID | ABS_POSレジスタを0にリセットします。 |
| [`/setElPos`](../reference/position-management.md#setelpos) | (int)motorID (int)newFullstep (int)newMicrostep | モータの電気的位置（electrical position）を設定します。マイクロステップは0〜127の128段階で表現されていますので、設定時は現在のマイクロステップと齟齬のない値を設定する必要があります。 |
| [`/getElPos`](../reference/position-management.md#getelpos) | (int)motorID | モータの電気的位置（electrical position）を取得します。 |
| [`/setMark`](../reference/position-management.md#setmark) | (int)motorID (int)MARK | markを任意の位置に設定します。 |
| [`/getMark`](../reference/position-management.md#getmark) | (int)motorID | MARKの位置を取得します。 |
| [`/goHome`](../reference/position-management.md#gohome) | (int)motorID | HOME位置までスピードプロファイルに従って移動します。 |
| [`/goMark`](../reference/position-management.md#gomark) | (int)motorID | MARK位置までスピードプロファイルに従って移動します。 |
| [`/setProhibitMotionOnHomeSw`](../reference/alarm-settings.md#setprohibitmotiononhomesw) | (int)motorID (bool)enable | HOMEスイッチがオンの状態で、原点復帰方向へのモーションコマンドを禁止します。原点復帰方向はconfigToolや`/setHomingDirection`で設定できます。 |
| [`/setProhibitMotionOnLimitSw`](../reference/alarm-settings.md#setprohibitmotiononlimitsw) | (int)motorID (bool)enable | LIMITスイッチがオンの状態で、原点復帰方向の逆方向へのモーションコマンドを禁止します。原点復帰方向はconfigToolや`/setHomingDirection`で設定できます。 |
<!-- generated:end osc-related homing, sensors, position, /setProhibitMotionOnHomeSw, /setProhibitMotionOnLimitSw -->

<!-- osc-settings: driverSettings.homingAtStartup, driverSettings.homingDirection, driverSettings.homingSpeed, driverSettings.homeSwMode, driverSettings.prohibitMotionOnHomeSw, driverSettings.limitSwMode, driverSettings.prohibitMotionOnLimitSw, driverSettings.goUntilTimeout, driverSettings.releaseSwTimeout, alarmAndReport.reportHomeSwStatus, alarmAndReport.reportLimitSwStatus, alarmAndReport.reportSwEvn -->
<!-- generated:begin osc-settings driverSettings.homingAtStartup, driverSettings.homingDirection, driverSettings.homingSpeed, driverSettings.homeSwMode, driverSettings.prohibitMotionOnHomeSw, driverSettings.limitSwMode, driverSettings.prohibitMotionOnLimitSw, driverSettings.goUntilTimeout, driverSettings.releaseSwTimeout, alarmAndReport.reportHomeSwStatus, alarmAndReport.reportLimitSwStatus, alarmAndReport.reportSwEvn -->
**関連する設定項目**

| キー | 名称 | コマンド |
| --- | --- | --- |
| [`driverSettings.homingAtStartup`](../connections/configuration-items.md#driversettings-homingatstartup) | Homing when the system starts |  |
| [`driverSettings.homingDirection`](../connections/configuration-items.md#driversettings-homingdirection) | Homing Direction | `/setHomingDirection` |
| [`driverSettings.homingSpeed`](../connections/configuration-items.md#driversettings-homingspeed) | Homing Speed | `/setHomingSpeed` |
| [`driverSettings.homeSwMode`](../connections/configuration-items.md#driversettings-homeswmode) | Home switch won't cause HardStop | `/setHomeSwMode` |
| [`driverSettings.prohibitMotionOnHomeSw`](../connections/configuration-items.md#driversettings-prohibitmotiononhomesw) | Prohibit motions on HomeSw | `/setProhibitMotionOnHomeSw` |
| [`driverSettings.limitSwMode`](../connections/configuration-items.md#driversettings-limitswmode) | Limit switch won't cause HardStop | `/setLimitSwMode` |
| [`driverSettings.prohibitMotionOnLimitSw`](../connections/configuration-items.md#driversettings-prohibitmotiononlimitsw) | Prohibit motions on LimitSw | `/setProhibitMotionOnLimitSw` |
| [`driverSettings.goUntilTimeout`](../connections/configuration-items.md#driversettings-gountiltimeout) | goUntil timeout duration | `/setGoUntilTimeout` |
| [`driverSettings.releaseSwTimeout`](../connections/configuration-items.md#driversettings-releaseswtimeout) | releaseSw timeout duration | `/setReleaseSwTimeout` |
| [`alarmAndReport.reportHomeSwStatus`](../connections/configuration-items.md#alarmandreport-reporthomeswstatus) | Report HOME switch status | `/enableHomeSwReport` |
| [`alarmAndReport.reportLimitSwStatus`](../connections/configuration-items.md#alarmandreport-reportlimitswstatus) | Report LIMIT switch status | `/enableLimitSwReport` |
| [`alarmAndReport.reportSwEvn`](../connections/configuration-items.md#alarmandreport-reportswevn) | Report HOME switch event | `/enableSwEventReport` |
<!-- generated:end osc-settings driverSettings.homingAtStartup, driverSettings.homingDirection, driverSettings.homingSpeed, driverSettings.homeSwMode, driverSettings.prohibitMotionOnHomeSw, driverSettings.limitSwMode, driverSettings.prohibitMotionOnLimitSw, driverSettings.goUntilTimeout, driverSettings.releaseSwTimeout, alarmAndReport.reportHomeSwStatus, alarmAndReport.reportLimitSwStatus, alarmAndReport.reportSwEvn -->
