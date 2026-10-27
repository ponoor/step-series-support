---
title: ネットワークとDIPスイッチ
---

# ネットワークとDIPスイッチ

DIPスイッチでボードのIDを設定します。このページでは、IDの使われ方、ネットワークの初期設定、MACアドレスを説明します。

## DIPスイッチの設定 {#dip-switch}

![](https://ponoor.com/cms/wp-content/uploads/2020/10/step400-dipSw.jpg)

ボード上のDIPスイッチでIDを設定します。IDはOSCメッセージの返信に使われるほか、IPアドレス、送信先のポート番号、MACアドレスに加算されます（下記）。

IDは8桁の2進数で、0から255です。ONの位置のスイッチを1として数えます。STEP400では、DIPSW1が最も下の桁（1）、DIPSW8が最も上の桁（128）です。STEP400は8つのスイッチを直接読み、STEP800はシフトレジスタを通して読みます。DIPスイッチで2進数を設定する方法は、[ディップスイッチによるチャンネル設定](https://www.soundhouse.co.jp/howto/light/dmx-dip/)が参考になります。

ボードがDIPスイッチを読むのは、起動時だけではありません。ボードが動いているときにIDを変えると、新しいIDでネットワークを設定し直します。ボードが読んだIDは、USBシリアルのコマンド`s`で確認できます。[USBシリアル診断](../maintenance/usb-serial-diagnosis.md#status)をご覧ください。

## ネットワークの設定 {#network-settings}

### 初期設定 {#initial}

設定ファイルがないとき、またはファイルにキーがないときに、ボードは次の値を使います。「ファームウェア」はファームウェアに組み込まれた値、「テンプレート」は設定ツールのテンプレートファイルの値です。両者が異なるときは、両方を示します。

<!-- osc-settings-values: network -->
<!-- generated:begin osc-settings-values network -->
| キー | 名称 | 初期値 | 範囲 / 単位 |
| --- | --- | --- | --- |
| [`network.myIp`](configuration-items.md#network-myip) | My IP address | 10.0.0.100 |  |
| [`network.isMyIpAddId`](configuration-items.md#network-ismyipaddid) | ID adds to my IP | true |  |
| [`network.destIp`](configuration-items.md#network-destip) | Destination IP | 10.0.0.10 |  |
| [`network.dns`](configuration-items.md#network-dns) | DNS | 10.0.0.1 |  |
| [`network.gateway`](configuration-items.md#network-gateway) | Gateway | 10.0.0.1 |  |
| [`network.subnet`](configuration-items.md#network-subnet) | Subnet mask | 255.255.255.0 |  |
| [`network.inPort`](configuration-items.md#network-inport) | Incoming port | 50000 |  |
| [`network.outPort`](configuration-items.md#network-outport) | Outgoing port | 50100 |  |
| [`network.isOutPortAddId`](configuration-items.md#network-isoutportaddid) | ID adds to Outgoing port | true |  |
| [`network.mac`](configuration-items.md#network-mac) | MAC address | STEP400: 60:95:CE:10:06:00（ファームウェア）、60:95:CE:10:02:00（テンプレート）; STEP800: 60:95:CE:10:06:00（ファームウェア）、60:95:CE:10:03:00（テンプレート） |  |
| [`network.isMacAddId`](configuration-items.md#network-ismacaddid) | ID adds to MAC address | true |  |
| [`network.bootedMsgEnable`](configuration-items.md#network-bootedmsgenable) | Booted message enable | true |  |
| [`network.canSendMsgBeforeDestIp`](configuration-items.md#network-cansendmsgbeforedestip) | Allow OSC reply before /setDestIp | false |  |
| [`network.reportError`](configuration-items.md#network-reporterror) | Report errors | true |  |
<!-- generated:end osc-settings-values network -->

### IPアドレスとポートへのIDの加算 {#adding-id}

初期状態では、IPアドレスの最後の数、送信先（OSC送信）ポート、MACアドレスにIDが加算されます。これによって、同じファームウェアと同じ設定ファイルで、多くのボードを使えます。受信側でメッセージの送信元のIPアドレスを取り出せるときは、ポートへの加算をやめて、すべてのボードから同じポートに送ることもできます。

それぞれの加算は、設定でオフにできます。[`isMyIpAddId`](configuration-items.md#network-ismyipaddid)、[`isOutPortAddId`](configuration-items.md#network-isoutportaddid)、[`isMacAddId`](configuration-items.md#network-ismacaddid)です。

加算した結果は、次の範囲に収まる必要があります。

- IPアドレス（`myIp`）の最後の数とIDの和は、254を超えられません。
- 送信先ポート（`outPort`）とIDの和は、65535を超えられません。

超えるときは、ボードはIDを加算せず、設定した値をそのまま使い、USBシリアルに警告を表示します。使う最大のIDが範囲に収まるように、IPアドレスとポートを決めてください。

### MACアドレス {#mac-address}

ボードにはそれぞれ固有のMACアドレスがありますが、初期値はそのアドレスではありません。弊社がテスト用に使っているMACアドレスです。ボードのMACアドレスは、ボードの裏面のシールで確認できます。シリアル番号のシールの下にあります。Pで始まる番号がシリアル番号で、その下の12桁の16進数がMACアドレスです。

![](https://ponoor.com/cms/wp-content/uploads/2020/10/step400-solderside-mac-800x533.jpg)

このアドレスを使うには、設定ファイルまたは[ブラウザ設定ツール](browser-config-tool.md)でMACアドレスに設定して設定を保存し、ボードを再起動します。[設定の仕組み](how-settings-work.md)をご覧ください。ファームウェアのソースの初期値を書き換えてビルドする方法もあります。[ファームウェアのコンパイル](../maintenance/compile-the-arduino-sketch.md)をご覧ください。

### 送信先 {#destination}

ボードは、返信とメッセージを、送信先のIPアドレスに送ります。ボードに[`/setDestIp`](../reference/system-settings.md#setdestip)を送って設定します。いつ送るか、ネットワークで何が起きるかは、[通信とメッセージ](../guides/communication-and-messages.md#setdestip)で説明しています。

### 設定が効くとき {#when}

設定に保存したIPアドレス、ポート、MACアドレスは、ボードを再起動すると効きます。動いている値は変わりません。[設定の仕組み](how-settings-work.md#when)をご覧ください。

## 関連するコマンド {#related}

<!-- osc-related: /setDestIp -->
<!-- generated:begin osc-related /setDestIp -->
**関連するコマンド**

| コマンド | 引数 | 説明 |
| --- | --- | --- |
| [`/setDestIp`](../reference/system-settings.md#setdestip) | - | モータの状態に変化があったときに通知するメッセージや、問い合わせへ返信するメッセージなどの送り先IPアドレス（`destIp`）を指定します。このメッセージを送信したIPアドレスを`destIp`に設定します。 |
<!-- generated:end osc-related /setDestIp -->
