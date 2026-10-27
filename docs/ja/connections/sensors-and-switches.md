---
title: センサとスイッチ
---

# センサとスイッチ

スイッチとセンサをつなぐ端子、ピン配置、配線の方法です。スイッチがオンになったときにボードが何をするか（原点復帰、即停止など）は、[原点復帰と位置管理](../guides/homing-and-position.md)で説明しています。

## HOME端子とLIMIT端子 {#terminals}

STEP400とSTEP800の各軸には、スイッチやセンサをつなぐHOME端子があります。STEP400には、それに加えてLIMIT端子もあります。端子につないだセンサも、HOMEスイッチ、LIMITスイッチと呼びます。

### HOME {#home}

原点検出用の入力端子です。ステッピングモータは自分の位置を検出できないので、起動時に原点を見つけるためのセンサが必要です。HOME端子はドライバICに直接つながっていて、ドライバでの位置管理に使えます。入力は3.3Vにプルアップされています。使い方は[原点復帰と位置管理](../guides/homing-and-position.md#home)で説明しています。

### LIMIT（STEP400のみ） {#limit}

各モータの動作範囲を制限するほか、別の用途の入力にも使える端子です。入力はHOMEと同じように3.3Vにプルアップされています。STEP400（R1）では、ドライバICのADC入力（ADCIN）につながっていて、ファームウェアがそこから読み取ります。STEP800にはLIMIT端子はありません。[原点復帰と位置管理](../guides/homing-and-position.md#limit)をご覧ください。

### コネクタ {#connector}

端子は、JST（日本圧着端子製造株式会社）のXAシリーズのコネクタです。適合する部品は次のとおりです。

| 品名 | 型番 | 備考 |
| --- | --- | --- |
| （参考）基板ポスト | B03B-XASK-1 (LF)(SN) | ボード上に実装されている部品 |
| ハウジング | XAP-03V-1 | 差し込むコネクタ本体 |
| コンタクト | BXA-001T-P0.6 | ハウジングに挿入する接続部 |

### ピン配置 {#pins}

ピン配置は、HOMEとLIMITで共通です。ピン番号はハウジングに印刷されています。

| ピン番号 | 機能 |
| --- | --- |
| 1 | GND |
| 2 | スイッチまたはセンサの入力 |
| 3 | 5V出力 |

## スイッチとセンサの配線 {#wiring}

### 電気的な接続 {#electrical}

入力（ピン2）は3.3Vにプルアップされています。スイッチは、GND（ピン1）と入力（ピン2）の間につなぎます。スイッチが閉じると、入力がGNDにつながり、電圧が3.3V（HIGH）から0V（LOW）に下がります。**入力がLOWのとき、スイッチはオンです。**

スイッチがオンになったとき、つまり入力がHIGHからLOWに変わったとき（立ち下がり）に、ファームウェアとドライバが反応します。従って、原点位置で入力がHIGHからLOWになるように、機構とスイッチを組み合わせる必要があります。スイッチがオンになったときにボードが何をするかは、[`/setHomeSwMode`](../reference/home-and-limit-sensors.md#sethomeswmode)と[`/setLimitSwMode`](../reference/home-and-limit-sensors.md#setlimitswmode)で設定します。[即停止モードと`SW_USER`](../guides/homing-and-position.md#sw-mode)をご覧ください。

### どのスイッチを使うか {#switches}

- **ノーマルオープン（NO）の接点のスイッチ**が、最も簡単です。NOの接点を、ピン1とピン2の間につなぎます。入力は通常時はHIGHで、スイッチを操作するとLOWになります。
- **ノーマルクローズ（NC）の接点のスイッチ**は、動作が逆になります。入力は通常時にLOWなので、スイッチから機構が離れているときにボードがスイッチをオンと見なし、スイッチを操作すると入力がHIGHになります。NCの接点は使わないでください。切り替え接点のスイッチなら、NOの端子と共通端子を使います。
- **センサ**は、オンのときに出力が0Vになるものが必要です。出力をピン2に、センサのグランドをピン1に、センサの電源をピン3（5V）につなぎます。

`/setHomeSwMode`と`/setLimitSwMode`は、信号を反転させません。スイッチがオンになったときにボードが何をするかを選ぶだけです。

### 例: フォトマイクロセンサEE-SX671A {#ee-sx671a}

オムロンのフォトマイクロセンサ[EE-SX671A](http://www.ia.omron.com/product/item/2219/)をつなぐ例です。

![EE-SX671A Diagram](http://ponoor.com/manage/wp-content/uploads/2020/10/ee-sx67.jpeg)

| ピン番号 | 機能 | センサのピン |
| --- | --- | --- |
| 1 | GND | - |
| 2 | スイッチまたはセンサの入力 | OUT |
| 3 | 5V出力 | + |

### 入光時にオンのセンサと遮光時にオンのセンサ {#light-dark}

センサを買う前によく考えてください。

![Dark on or Light on](http://ponoor.com/manage/wp-content/uploads/2020/10/sensor_dark_light.png)

左の図では、原点位置でセンサに光が入ります。右の図では、原点位置でセンサの光が遮られます。

センサには、光が入るとオンになるタイプ（入光時オン）と、光が遮られるとオンになるタイプ（遮光時オン）があります。切り替えができるセンサもあり、上のオムロンのセンサは、Lの端子と+の端子をつなぐと動作が切り替わります。

原点位置で入力がHIGHからLOWになるように、機構とセンサを組み合わせてください。

## 関連するコマンドと設定項目 {#related}

<!-- osc-related: /setHomeSwMode, /setLimitSwMode, /getHomeSw, /getLimitSw -->
<!-- generated:begin osc-related /setHomeSwMode, /setLimitSwMode, /getHomeSw, /getLimitSw -->
**関連するコマンド**

| コマンド | 引数 | 説明 |
| --- | --- | --- |
| [`/setHomeSwMode`](../reference/home-and-limit-sensors.md#sethomeswmode) | (int)motorID (bool)SW_MODE | HOME端子に入力があった際に即停止するかどうか（Switch mode）を指定します。 |
| [`/setLimitSwMode`](../reference/home-and-limit-sensors.md#setlimitswmode) | (int)motorID (bool)SW_MODE | LIMIT端子に入力があった際に即停止するかどうか（Switch mode）を指定します。 |
| [`/getHomeSw`](../reference/home-and-limit-sensors.md#gethomesw) | (int)motorID | HOMEスイッチの状態を取得します。 |
| [`/getLimitSw`](../reference/home-and-limit-sensors.md#getlimitsw) | (int)motorID | LIMITスイッチの状態を取得します。 |
<!-- generated:end osc-related /setHomeSwMode, /setLimitSwMode, /getHomeSw, /getLimitSw -->

<!-- osc-settings: driverSettings.homeSwMode, driverSettings.limitSwMode, alarmAndReport.reportHomeSwStatus, alarmAndReport.reportLimitSwStatus -->
<!-- generated:begin osc-settings driverSettings.homeSwMode, driverSettings.limitSwMode, alarmAndReport.reportHomeSwStatus, alarmAndReport.reportLimitSwStatus -->
**関連する設定項目**

| キー | 名称 | コマンド |
| --- | --- | --- |
| [`driverSettings.homeSwMode`](configuration-items.md#driversettings-homeswmode) | Home switch won't cause HardStop | `/setHomeSwMode` |
| [`driverSettings.limitSwMode`](configuration-items.md#driversettings-limitswmode) | Limit switch won't cause HardStop | `/setLimitSwMode` |
| [`alarmAndReport.reportHomeSwStatus`](configuration-items.md#alarmandreport-reporthomeswstatus) | Report HOME switch status | `/enableHomeSwReport` |
| [`alarmAndReport.reportLimitSwStatus`](configuration-items.md#alarmandreport-reportlimitswstatus) | Report LIMIT switch status | `/enableLimitSwReport` |
<!-- generated:end osc-settings driverSettings.homeSwMode, driverSettings.limitSwMode, alarmAndReport.reportHomeSwStatus, alarmAndReport.reportLimitSwStatus -->
