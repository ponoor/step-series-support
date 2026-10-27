---
title: アラームと保護
---

# アラームと保護

モータドライバチップは、4種類のアラームを検出します。電源電圧の低下（UVLO）、過熱、過電流、ストールです。このページでは、各アラームの意味、ドライバが何をするか、ボードが何を通知するかを説明します。

## 概要 {#overview}

各アラームには、ドライバの状態にフラグがあります。ボードは5msごとにすべてのドライバの状態を読み、変化したときにメッセージを送ります（[通知のタイミング](#timing)をご覧ください）。メッセージを送るかどうかは、アラームごとの`/enable...Report`コマンドで設定します。ドライバが何をするかは、アラームによって異なります。

| アラーム | ドライバの動作 | メッセージ |
| --- | --- | --- |
| 電源電圧の低下（UVLO） | 出力を止める。モータは無励磁になる | [`/uvlo`](../reference/automatically-sent-messages.md#uvlo) |
| 過熱 | 警告のとき: 何もしない。ブリッジの遮断かデバイスの遮断のとき: モータは無励磁になる | [`/thermalStatus`](../reference/automatically-sent-messages.md#thermalstatus) |
| 過電流 | 出力を止める。モータは無励磁になる | [`/overCurrent`](../reference/automatically-sent-messages.md#overcurrent) |
| ストール | 何もしない（フラグだけ） | [`/stall`](../reference/automatically-sent-messages.md#stall) |

STEP400のPowerSTEP01とSTEP800のL6470では、細かい点が異なります。異なる点は、そのつど書いています。

## アラームごとの説明 {#alarms}

### UVLO: 電源電圧の低下 {#uvlo}

ドライバの電源電圧が、遮断の閾値を下回ると、UVLOが起きます。ドライバはすべての出力をすぐに止めるため、モータは無励磁になり、この状態の間は動かせません。電圧が復帰の閾値を上回ると、状態は終わります。そのあとは[再開](#resuming)をご覧ください。閾値はSTEP400とSTEP800で異なります。ドライバチップのデータシートをご覧ください。

[`/enableUvloReport`](../reference/alarm-settings.md#enableuvloreport)で通知を有効にします（状態が変わると[`/uvlo`](../reference/automatically-sent-messages.md#uvlo)が送られます）。[`/getUvlo`](../reference/alarm-settings.md#getuvlo)で状態を読み出せます。

### 過熱 {#thermal}

ドライバは自分の温度を監視しています。警告のレベルでは、フラグが立つだけで、動作は制限されません。遮断のレベルでは、出力が止まり、モータは無励磁になります。STEP400には遮断のレベルが2つ（ブリッジの遮断とデバイスの遮断）あり、STEP800には1つあります。温度は[`/thermalStatus`](../reference/automatically-sent-messages.md#thermalstatus)に載せています。

[`/enableThermalStatusReport`](../reference/alarm-settings.md#enablethermalstatusreport)で通知を有効にし、[`/getThermalStatus`](../reference/alarm-settings.md#getthermalstatus)で状態を読み出します。通知の有無によらず、モータは無励磁になります。遮断のあとは[再開](#resuming)をご覧ください。

### 過電流 {#overcurrent}

ドライバは、パワートランジスタの電流を測っています。電流が閾値を超えると、ドライバは出力を止めます（ファームウェアはこの保護を有効にしています）。モータは無励磁になります。この保護は重要なものなので、無効にすることは想定していません。

[`/setOverCurrentThreshold`](../reference/alarm-settings.md#setovercurrentthreshold)で閾値を設定し、[`/enableOverCurrentReport`](../reference/alarm-settings.md#enableovercurrentreport)で通知を有効にします。[`/overCurrent`](../reference/automatically-sent-messages.md#overcurrent)が送られます。原因がなくなったあとにモータをもう一度動かす方法は、[再開](#resuming)をご覧ください（電磁ブレーキのモータでは、先に`/activate 1`が必要です）。

### ストール {#stall}

ストール検出は、モータの電流から、モータが負荷に逆らって回れなくなったことをドライバが見つける機能です。ドライバはフラグを立てるだけで、モータは止めません。STEP400では、電圧モードでだけ検出が動作します。電流モードでは使えません。

[`/setStallThreshold`](../reference/alarm-settings.md#setstallthreshold)で閾値を設定し、[`/enableStallReport`](../reference/alarm-settings.md#enablestallreport)で通知を有効にします。[ストール検出の使い方](#using-stall)をご覧ください。

## 通知のタイミング {#timing}

- ボードは5msごとにドライバの状態を読みます。[`/busy`](../reference/automatically-sent-messages.md#busy)、[`/HiZ`](../reference/automatically-sent-messages.md#hiz)、[`/uvlo`](../reference/automatically-sent-messages.md#uvlo)、[`/thermalStatus`](../reference/automatically-sent-messages.md#thermalstatus)などのメッセージは、状態が変わったときに送られ、読み出しのたびには送られません。
- [`/overCurrent`](../reference/automatically-sent-messages.md#overcurrent)と[`/stall`](../reference/automatically-sent-messages.md#stall)は、状態が始まったときにすぐ送られます。続いている間は、モータごと、種類ごとに、最短200ms間隔で送られます。200msの間の検出は失われず、間隔の終わりに1つのメッセージになります。通知が無効の間の検出は、あとで送られません。
- [`/getStatus`](../reference/motor-driver-settings.md#getstatus)と[`/getStatusList`](../reference/motor-driver-settings.md#getstatuslist)は、ラッチされたフラグ（OCD、ストール、UVLO、SW_EVNなど）を消さずに、ドライバのSTATUSレジスタを読みます。フラグを消すのは、ボードが5msごとに行う読み出しだけです。このため、`/getStatus`や`/getStatusList`を続けて送ると、前の返信に出ていたフラグが次の返信にも出ることがあります（次の読み出しまで、最大5ms）。

## ドライバが自分で無励磁になったとき {#hiz-by-itself}

過電流の遮断、過熱の遮断、UVLOで、ドライバがモータを無励磁にしたとき、ボードは次の順に動作します（各メッセージは、それぞれの設定に従います）。

1. [`/HiZ`](../reference/automatically-sent-messages.md#hiz)（[`/enableHizReport`](../reference/motor-driver-settings.md#enablehizreport)が有効のとき）
2. モータがサーボモードのとき: サーボモードを解除し、`/error/command ServoModeCancelledOnHiZ`を送ります。ドライバには何も送りません。
3. 電磁ブレーキのモータで、ブレーキが解放されているとき: 次の状態の読み出し（最大5ms後）でブレーキを保持状態にし、`/error/command BrakeEngagedOnHiZ`を送ります。[電磁ブレーキ](electromagnetic-brake.md#transitions)をご覧ください。

エラーは[`/reportError`](../reference/system-settings.md#reporterror)に従います。モータを無励磁にするコマンド（`/softHiZ`、`/hardHiZ`、`/activate 0`、`/free`、`/resetMotorDriver`）は、先にサーボモードを解除し、`ServoModeCancelledOnHiZ`は送りません。

### 再開 {#resuming}

原因（過電流、温度、電源電圧）がなくなっても、モータは無励磁のままです。動作コマンドで、もう一度動かします。電磁ブレーキを有効にしているモータでは、ボードがブレーキを保持状態にしているため、先に`/activate 1`が必要です（ブレーキが保持状態の間、動作コマンドは`BrakeEngaged`で拒否されます）。サーボモードを再開するには、`/enableServoMode 1`を送ります（ブレーキのモータでは`/activate 1`の後です）。現在位置が目標位置になります。原因が残っていると、ドライバはまた遮断します。

## 閾値と電流の換算 {#thresholds}

過電流とストールの閾値は数値で設定します。数値に対応する電流は、次のとおりです。

> 電流 = （値 + 1）× 刻み

刻みはドライバによって異なります。

| | 過電流 | ストール |
| --- | --- | --- |
| STEP400（PowerSTEP01） | 312.5mA | 312.5mA |
| STEP800（L6470） | 375mA | 31.25mA |

値が0のときは0Aではなく、1刻みの電流です。PowerSTEP01のデータシートはこの閾値を電圧で書いています（ストールは31.25mV刻み）。電流への換算は、STEP400の基板の電流検出回路によるものです。電流モードのTVALにも、同じ種類の換算があります（刻みは78.125mA）。[電圧モードと電流モード](voltage-and-current-mode.md#current-mode-setting)をご覧ください。範囲と初期値はボードによって異なるため、[`/setOverCurrentThreshold`](../reference/alarm-settings.md#setovercurrentthreshold)と[`/setStallThreshold`](../reference/alarm-settings.md#setstallthreshold)にだけ載せています。

## ストール検出の使い方 {#using-stall}

ストール検出は、モータの電流を閾値と比べます。閾値は、試しながら決めます。実際に流れている電流にできるだけ近く、少し上にします。脱調（ステップのずれ）程度の小さなずれは検出できませんが、大きな位置のずれは検出できることがあります。

電流は、KVALとBEMF補償によって変わります。先に、モータと電源電圧に合わせて調整してください。[電圧モードと電流モード](voltage-and-current-mode.md#voltage-mode-setting)をご覧ください。

## スイッチによる動作の禁止 {#switches}

HOMEスイッチとLIMITスイッチによる動作の禁止（[`/setProhibitMotionOnHomeSw`](../reference/alarm-settings.md#setprohibitmotiononhomesw)、[`/setProhibitMotionOnLimitSw`](../reference/alarm-settings.md#setprohibitmotiononlimitsw)）は、[原点復帰と位置管理](homing-and-position.md#collision-prevention)で説明しています。

## 関連するコマンドと設定項目 {#related}

<!-- osc-related: alarm, /getStatus, /getStatusList -->
<!-- generated:begin osc-related alarm, /getStatus, /getStatusList -->
**関連するコマンド**

| コマンド | 引数 | 説明 |
| --- | --- | --- |
| [`/enableUvloReport`](../reference/alarm-settings.md#enableuvloreport) | (int)motorID (bool)enable | 指定したモータドライバで電源電圧の低下（UVLO, Undervoltage Lockout）が発生した際に自動で通知メッセージを送信するかどうかを指定します。 |
| [`/getUvlo`](../reference/alarm-settings.md#getuvlo) | (int)motorID | 電源電圧の低下（UVLO）の現在の状態を取得します。 |
| [`/enableThermalStatusReport`](../reference/alarm-settings.md#enablethermalstatusreport) | (int)motorID (bool)enable | 指定したモータドライバの温度状態（thermalStatus）に変化があったら自動でメッセージを送信するかどうかを指定します。Bridge shutdown, Device shutdown状態では、通知の有無にかかわらずモータは無励磁状態になります。 |
| [`/getThermalStatus`](../reference/alarm-settings.md#getthermalstatus) | (int)motorID | ThermalStatusの現在の状態を取得します。STEP400とSTEP800ではThermal statusの種類や発生条件が異なります。 |
| [`/enableOverCurrentReport`](../reference/alarm-settings.md#enableovercurrentreport) | (int)motorID (bool)enable | 指定したモータドライバが過電流状態（OCD, Over Current Detection）になった場合に自動でメッセージを送信するかどうかを指定します。 |
| [`/setOverCurrentThreshold`](../reference/alarm-settings.md#setovercurrentthreshold) | (int)motorID (int)OCD_TH | 過電流の閾値を設定します。STEP400とSTEP800では設定値の範囲と対応する電流が異なっています。 |
| [`/getOverCurrentThreshold`](../reference/alarm-settings.md#getovercurrentthreshold) | (int)motorID | 過電流の閾値を取得します。 |
| [`/enableStallReport`](../reference/alarm-settings.md#enablestallreport) | (int)motorID (bool)enable | 閾値は`/setStallThreshold`で設定できます。 |
| [`/setStallThreshold`](../reference/alarm-settings.md#setstallthreshold) | (int)motorID (int)STALL_TH | ストール検出の閾値を設定します。STEP400とSTEP800で設定する値の範囲は異なります。 |
| [`/getStallThreshold`](../reference/alarm-settings.md#getstallthreshold) | (int)motorID | ストール検出の閾値を取得します。 |
| [`/setProhibitMotionOnHomeSw`](../reference/alarm-settings.md#setprohibitmotiononhomesw) | (int)motorID (bool)enable | HOMEスイッチがオンの状態で、原点復帰方向へのモーションコマンドを禁止します。原点復帰方向はconfigToolや`/setHomingDirection`で設定できます。 |
| [`/getProhibitMotionOnHomeSw`](../reference/alarm-settings.md#getprohibitmotiononhomesw) | (int)motorID | HOMEスイッチがオンの状態で、原点復帰方向へのモーションコマンドが禁止されているかどうかを返します。 |
| [`/setProhibitMotionOnLimitSw`](../reference/alarm-settings.md#setprohibitmotiononlimitsw) | (int)motorID (bool)enable | LIMITスイッチがオンの状態で、原点復帰方向の逆方向へのモーションコマンドを禁止します。原点復帰方向はconfigToolや`/setHomingDirection`で設定できます。 |
| [`/getProhibitMotionOnLimitSw`](../reference/alarm-settings.md#getprohibitmotiononlimitsw) | (int)motorID | LIMITスイッチがオンの状態で、原点復帰方向の逆方向へのモーションコマンドが禁止されているかどうかを返します。 |
| [`/getStatus`](../reference/motor-driver-settings.md#getstatus) | (int)motorID | モータドライバ（PowerSTEP01/L6470）のSTATUSレジスタを取得します。STATUSレジスタにはモータやアラーム、スイッチの状態などが含まれます。 |
| [`/getStatusList`](../reference/motor-driver-settings.md#getstatuslist) | - | すべてのモータのSTATUSレジスタをまとめて取得します。レジスタの内容は`/getStatus`を参照してください。 |
<!-- generated:end osc-related alarm, /getStatus, /getStatusList -->

<!-- osc-settings: alarmAndReport.reportUVLO, alarmAndReport.reportThermalStatus, alarmAndReport.reportOCD, alarmAndReport.reportStall, alarmAndReport.OCThreshold, voltageMode.STALL_TH -->
<!-- generated:begin osc-settings alarmAndReport.reportUVLO, alarmAndReport.reportThermalStatus, alarmAndReport.reportOCD, alarmAndReport.reportStall, alarmAndReport.OCThreshold, voltageMode.STALL_TH -->
**関連する設定項目**

| キー | 名称 | コマンド |
| --- | --- | --- |
| [`alarmAndReport.reportUVLO`](../connections/configuration-items.md#alarmandreport-reportuvlo) | Report undervoltage lockout | `/enableUvloReport` |
| [`alarmAndReport.reportThermalStatus`](../connections/configuration-items.md#alarmandreport-reportthermalstatus) | Report thermal status of driver chip | `/enableThermalStatusReport` |
| [`alarmAndReport.reportOCD`](../connections/configuration-items.md#alarmandreport-reportocd) | Report overcurrent detection | `/enableOverCurrentReport` |
| [`alarmAndReport.reportStall`](../connections/configuration-items.md#alarmandreport-reportstall) | Report motor stall detection | `/enableStallReport` |
| [`alarmAndReport.OCThreshold`](../connections/configuration-items.md#alarmandreport-octhreshold) | Overcurrent threshold | `/setOverCurrentThreshold` |
| [`voltageMode.STALL_TH`](../connections/configuration-items.md#voltagemode-stall_th) | STALL_TH | `/setStallThreshold` |
<!-- generated:end osc-settings alarmAndReport.reportUVLO, alarmAndReport.reportThermalStatus, alarmAndReport.reportOCD, alarmAndReport.reportStall, alarmAndReport.OCThreshold, voltageMode.STALL_TH -->
