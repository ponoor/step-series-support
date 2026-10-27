---
title: 通信とメッセージ
---

# 通信とメッセージ

このページでは、ボードがコンピュータとOSC（Open Sound Control）のメッセージをやり取りする仕組みを説明します。送信先をどう知るか、ボードが自分から何を送るか、受け取った引数をどう扱うかです。

## 概要 {#overview}

ボードは、OSCメッセージをUDPのパケットとして受け取ります。ボードが送るメッセージには2種類あります。[`/getVersion`](../reference/system-settings.md#getversion)のように、問い合わせるコマンドへの**返信**と、何かが起きたときや一定の間隔で、ボードが**自分から**送るメッセージ（[`/busy`](../reference/automatically-sent-messages.md#busy)や[`/position`](../reference/automatically-sent-messages.md#position)など）です。どちらも、ボードが送信先として持っているIPアドレスとポートへ送られます。

ボードのIPアドレス、ポート番号、DIPスイッチの設定は、[ネットワークとDIPスイッチ](../connections/network-and-dip-switch.md)をご覧ください。ここには書き写していません。

コマンドは、単体のOSCメッセージとして送ってください。OSCバンドルには対応していません。

## 送信先と`/setDestIp` {#setdestip}

### `/setDestIp`を送るとき {#when}

ボードは、[`/setDestIp`](../reference/system-settings.md#setdestip)を受け取るまで、メッセージの送り先を知りません。このメッセージの送信元を、送信先として扱います。それまでは、ブロードキャストの[`/booted`](../reference/automatically-sent-messages.md#booted)を除いて、何も送りません（[`network.canSendMsgBeforeDestIp`](../connections/configuration-items.md#network-cansendmsgbeforedestip)を設定すると、最初から[`network.destIp`](../connections/configuration-items.md#network-destip)へ送ります）。

`/setDestIp`は、次のときに送ってください。

- 接続を始めるとき
- ネットワークやコンピュータを替えたとき。同じIPアドレスの別のコンピュータやネットワークアダプタ、Wi-Fiと有線の切り替えなどです。コンピュータを替えるときは、前のコンピュータが最後に送信してから、1.5s以上空けてください。

送らないと、ボードは古いコンピュータのMACアドレスへ送り続けます。コマンドは効きますが、返信も通知も届きません（コンピュータと直結していて、リンクが切れてまた戻ったときは、ボードが自分で回復します。スイッチを経由しているときは回復しません）。

### MACアドレスの解決 {#arp}

新しいアドレスからの`/setDestIp`や、送信先からの最後のパケットから1.5s以上あとの`/setDestIp`で送信先を設定する（または変える）と、ボードは（1秒ごとに送るようなハートビートの`/setDestIp`では始まりません）送信先のMACアドレスを調べる必要があります。ブロードキャストアドレスのUDPポート9（discard）に1バイトを送り、続けて送信先のポート9にすぐ1バイトを送り、送信先がARPの要求に答えるか約2sが経つまで、150msごとに繰り返し送ります。コンピュータは、このパケットのそれぞれにICMPのport unreachableを返すことがありますが、無害です。ファイアウォールのログに出ることがあります。

この解決を始める`/setDestIp`の返信[`/destIp`](../reference/system-settings.md#setdestip)は、解決が終わってから送られます。有線では、コマンドの数ms後に返ります。**コンピュータがWi-Fiでつながっているときは、最大で数秒かかります。** [`/destIp`](../reference/system-settings.md#setdestip)が返らなければ、`/setDestIp`を送り直してください。

MACアドレスを解決している間（このような`/setDestIp`の後、リンクが再び上がった後。`/setDestIp`の前に送る設定のときは、起動後も）は、送信先へのメッセージは**破棄されます**。あとで送られることはありません。返信も通知も届きません。ブロードキャストの`/booted`は送られます。

答えない送信先を待っている間、ボードはOSCメッセージを処理できません。コンピュータがWi-Fiでつながっているときは、解決の間、150msごとに最大で約41ms、処理が止まります。このため、電磁ブレーキの監視とサーボモードが乱れます。**`/setDestIp`は、モータを止めた状態で送ることをお勧めします。**

ARPに一度も答えない送信先（例えば誤った送信先のアドレス）への送信は失敗します。ボードはその送信先への送信を1s止め、その間のメッセージを破棄します。1s後に、次のメッセージで再び試します。送信先からパケットが届くと、送信はすぐに再開します。

### 接続の監視 {#keepalive}

ボードが動いているかを確かめるには、`/getVersion`など、返信のあるコマンドを送ってください。`/setDestIp`は使わないでください。

## 返信と、ボードが自分から送るメッセージ {#messages}

- **返信**: 値を問い合わせるコマンド（`/get...`）には、メッセージで答えます。設定のコマンドにも返信があるものがあります。コマンドが何を返すかは、各コマンドのリファレンスに載せています。
- **変化の通知**: ボードは5msごとにドライバの状態を読み、状態が変わったときにメッセージを送ります。[`/busy`](../reference/automatically-sent-messages.md#busy)、[`/HiZ`](../reference/automatically-sent-messages.md#hiz)、[`/dir`](../reference/automatically-sent-messages.md#dir)、[`/motorStatus`](../reference/automatically-sent-messages.md#motorstatus)、[`/homeSw`](../reference/automatically-sent-messages.md#homesw)、[`/limitSw`](../reference/automatically-sent-messages.md#limitsw)、[`/swEvent`](../reference/automatically-sent-messages.md#swevent)、[`/uvlo`](../reference/automatically-sent-messages.md#uvlo)、[`/thermalStatus`](../reference/automatically-sent-messages.md#thermalstatus)、[`/overCurrent`](../reference/automatically-sent-messages.md#overcurrent)、[`/stall`](../reference/automatically-sent-messages.md#stall)などです。それぞれ、専用の`/enable...Report`コマンドで有効・無効にします。起動時にどれが有効かは、ボードの設定で決まります。状態は変化したときだけ送られます。アラームについては、[アラームと保護](alarms-and-protection.md#timing)をご覧ください。
- **一定の間隔で送る位置レポート**: [`/setPositionReportInterval`](../reference/motor-driver-settings.md#setpositionreportinterval)で、モータごとの[`/position`](../reference/automatically-sent-messages.md#position)を一定の間隔で送ります。[`/setPositionListReportInterval`](../reference/motor-driver-settings.md#setpositionlistreportinterval)では、全モータの位置を1つのメッセージ[`/positionList`](../reference/automatically-sent-messages.md#positionlist)で送ります。全モータの位置を短い間隔で取るときは、位置リストのレポートを使ってください。モータごとのレポートよりも、ボードのCPUの負荷が大きく下がります。
- **[`/booted`](../reference/automatically-sent-messages.md#booted)**: ボードが起動したときに、ブロードキャストで送ります。リセットの原因が含まれます。

一覧は、[自動送信されるメッセージ](../reference/automatically-sent-messages.md)をご覧ください。

## ボードが受け取る引数 {#arguments}

ボードは、コマンドを適用する前に引数を検査します。検査に通らないときは、**何も適用されません**。

| 場合 | メッセージ |
| --- | --- |
| コマンドに必要な数より引数が少ない | [`/error/osc`](../reference/automatically-sent-messages.md#error-osc) `MissingArgument` |
| 型が違う引数（数値の代わりの文字列、NaNや無限大、`/setConfigName`に文字列以外） | `/error/osc` `WrongDataType` |
| ボードにないモータID（ボードのモータでも255でもない値）、または0〜255の範囲外のモータID | [`/error/command`](../reference/automatically-sent-messages.md#error-command) `MotorIdNotMatch`（送ったモータIDつき） |
| コマンドの範囲外の値 | `/error/command` `CommandIgnored` |
| 512バイトを超えるパケット、または16個を超える引数 | `/error/osc` `OscSyntaxError` |

v2.2.0より前は、引数の不足や型違いは0として適用されていました。例えば、`/setKval 1`は、そのモータのKVALをすべて0にしていました。

- コマンドに必要な数を超える引数は無視されます。
- 範囲外の値を拒否せずに、制限したり、最大値の次を0として数え直したりするコマンドがあります。どれかは各コマンドのリファレンスに載せています。[共通の決まり](../reference/index.md)もご覧ください。
- 整数と浮動小数点数は、受信時に相互に変換されます。**論理値は、整数の0か1で送ってください**（型タグ`i`）。STEPシリーズの仕様で、ボードも論理値をいつもこの形で送ります。ボードは、数値（0より大きい整数、または1.0以上の浮動小数点数が真）と、OSCの論理値True・Falseも受け付けます。
- OSCバンドルには対応していません。

## エラー {#errors}

エラーを通知するメッセージは2つあります。

- [`/error/osc`](../reference/automatically-sent-messages.md#error-osc): メッセージそのものが使えなかったとき。引数の不足、型違い、構文のエラー、ボードが知らないアドレス（`MessageNotMatch`）です。
- [`/error/command`](../reference/automatically-sent-messages.md#error-command): メッセージは理解できたが、コマンドを実行できなかった、または適用されなかったとき。モータの状態が許さない（`MotorNotHiZ`、`BrakeEngaged`、`InServoMode`など）、値が範囲外、モータIDがない、タイムアウトした、などです。

[`/reportError`](../reference/system-settings.md#reporterror)を0にすると、ボードはどちらも送りません。エラーの一覧は[自動送信されるメッセージ](../reference/automatically-sent-messages.md#error-command)に、コマンドごとのエラーは各コマンドのリファレンスに載せています。

## 診断 {#diagnosis}

USBシリアルポートで、送信先のMACアドレスなど、接続の詳しい状態を確かめられます。[USBシリアル診断](../maintenance/usb-serial-diagnosis.md)をご覧ください。

## 関連するコマンドと設定項目 {#related}

<!-- osc-related: system, /setPositionReportInterval, /setPositionListReportInterval -->
<!-- generated:begin osc-related system, /setPositionReportInterval, /setPositionListReportInterval -->
**関連するコマンド**

| コマンド | 引数 | 説明 |
| --- | --- | --- |
| [`/setDestIp`](../reference/system-settings.md#setdestip) | - | モータの状態に変化があったときに通知するメッセージや、問い合わせへ返信するメッセージなどの送り先IPアドレス（`destIp`）を指定します。このメッセージを送信したIPアドレスを`destIp`に設定します。 |
| [`/getVersion`](../reference/system-settings.md#getversion) | - | 本体に書き込まれているファームウェアのバージョン情報を返します。 |
| [`/getConfigName`](../reference/system-settings.md#getconfigname) | - | `/configName`を返します。設定名、microSDカードを使えたか、設定ファイルを開けたか・解析できたか、設定ファイルのパスが含まれます。 |
| [`/reportError`](../reference/system-settings.md#reporterror) | (bool)enable | `/error/command`および`/error/osc`メッセージの自動送信の有効/無効を切り替えます。 |
| [`/setConfigName`](../reference/system-settings.md#setconfigname) | (string)configName | ボードに保存される設定名を設定します。設定を見分けるためにユーザーが自由に編集できるラベルで、ディスク上のファイル名とは別のものです。 |
| [`/saveConfig`](../reference/system-settings.md#saveconfig) | - | 現在動作中の設定を、JSONファイルとしてmicroSDカードに保存します。保存先は、起動時に読み込んだファイルです。ファイルを読み込まなかったときは`/config.txt`です。USBシリアルの`F<path>`で、保存先のパスを変えられます。 |
| [`/resetDevice`](../reference/system-settings.md#resetdevice) | - | ボード全体をリセットします。ボード上のリセットスイッチを押した場合と同じ動作です。 |
| [`/setPositionReportInterval`](../reference/motor-driver-settings.md#setpositionreportinterval) | (int)motorID (int)interval | 指定したモータの現在位置（`ABS_POS`）を指定間隔で自動送信します。0を指定すると無効化され、送信を停止します。 |
| [`/setPositionListReportInterval`](../reference/motor-driver-settings.md#setpositionlistreportinterval) | (int)interval | 全モータの現在位置（`ABS_POS`）をひとつのリストにまとめたメッセージを指定間隔で自動送信します。0を指定すると無効化され、送信を停止します。 |
<!-- generated:end osc-related system, /setPositionReportInterval, /setPositionListReportInterval -->

<!-- osc-settings: network -->
<!-- generated:begin osc-settings network -->
**関連する設定項目**

| キー | 名称 | コマンド |
| --- | --- | --- |
| [`network.myIp`](../connections/configuration-items.md#network-myip) | My IP address |  |
| [`network.isMyIpAddId`](../connections/configuration-items.md#network-ismyipaddid) | ID adds to my IP |  |
| [`network.destIp`](../connections/configuration-items.md#network-destip) | Destination IP | `/setDestIp` |
| [`network.dns`](../connections/configuration-items.md#network-dns) | DNS |  |
| [`network.gateway`](../connections/configuration-items.md#network-gateway) | Gateway |  |
| [`network.subnet`](../connections/configuration-items.md#network-subnet) | Subnet mask |  |
| [`network.inPort`](../connections/configuration-items.md#network-inport) | Incoming port |  |
| [`network.outPort`](../connections/configuration-items.md#network-outport) | Outgoing port |  |
| [`network.isOutPortAddId`](../connections/configuration-items.md#network-isoutportaddid) | ID adds to Outgoing port |  |
| [`network.mac`](../connections/configuration-items.md#network-mac) | MAC address |  |
| [`network.isMacAddId`](../connections/configuration-items.md#network-ismacaddid) | ID adds to MAC address |  |
| [`network.bootedMsgEnable`](../connections/configuration-items.md#network-bootedmsgenable) | Booted message enable |  |
| [`network.canSendMsgBeforeDestIp`](../connections/configuration-items.md#network-cansendmsgbeforedestip) | Allow OSC reply before /setDestIp |  |
| [`network.reportError`](../connections/configuration-items.md#network-reporterror) | Report errors | `/reportError` |
<!-- generated:end osc-settings network -->
