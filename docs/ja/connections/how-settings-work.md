---
title: 設定の仕組み
---

# 設定の仕組み

ボードの設定がどこにあり、変更がいつ効き、どこに保存されるかを説明します。最初にこのページをお読みください。カードとツールの詳細は、[microSDカードでの設定](microsd-card.md)と[ブラウザ設定ツール](browser-config-tool.md)にあります。

## 設定を変える3つの方法 {#overview}

- **microSDカードの設定ファイル。** ボードが起動するときに読みます。ファイルは、パソコンで作ることも、ブラウザ設定ツールで作ることもできます。
- **ブラウザ設定ツール。** USBでボードから設定を読み、編集した設定を適用して、カードに保存します。
- **OSCコマンド。** 動いているボードの値を、すぐに変えます。[`/saveConfig`](../reference/system-settings.md#saveconfig)で、動いている値をカードに保存します。

設定ファイルのすべての項目は、変更するコマンドとともに、[設定項目一覧](configuration-items.md)にあります。

## 起動時 {#at-start}

ボードがカードを読むのは、起動するときだけです。次の順にファイルを探し、ファイルがないとき、またはファイルが有効でないときは、ファームウェアの初期値を使います。

1. カードのルートフォルダにある`config.txt`。
2. ルートフォルダで、アルファベット順に最初の`*.json`。
3. 初期値。

詳しくは[ボードが読むファイル](microsd-card.md#files)をご覧ください。v2.2.0からは、受け付けなかったファイルの値は、まったく適用しません。カードがないときと同じように、初期値を使います。

ボードが何を読んだかは、[`/getConfigName`](../reference/system-settings.md#getconfigname)を送ると分かります。返信の`/configName`には、設定名、カードとファイルを読めたか、ファイルのパス（先頭に`/`が付きます）が入っています。USBシリアルの出力でも確かめられます（[USBシリアル診断](../maintenance/usb-serial-diagnosis.md)）。

## 動いている値と保存された値 {#saved-values}

ボードは、動いている間、設定をメモリに持っています。OSCコマンドで変えた値は、メモリの中で変わります。**保存しないと、電源を切ったときに消えます。**

- [`/saveConfig`](../reference/system-settings.md#saveconfig)は、動いている設定をカードに書きます。
- 書き込み先は、起動時に読んだファイルです。ファイルを読んでいないときは、`/config.txt`です。USBシリアルのコマンド`F<path>`で、次に再起動するまで書き込み先を変えられます。[`F<path>`で決めた名前](microsd-card.md#f-path)をご覧ください。
- ブラウザ設定ツールの**Save to SD**も、編集した値を適用してから、同じように保存します。

ボードが次の起動で読む値は、保存したファイルの値です。保存したあとに変えた値は入っていません。

## 変更が効くとき {#when}

**OSCコマンド**は、すぐに効きます。コマンドによっては、モータが無励磁のときだけなど、使える状態が決まっています。各コマンドの条件は[リファレンス](../reference/index.md)にあります。

**ブラウザ設定ツール**は、動いているファームウェアのメモリに値を適用して、カードに保存します。すべての値がすぐに効くわけではありません。

| 設定 | 効くとき |
| --- | --- |
| 設定名 | すぐ |
| IPアドレス、サブネットマスク、ゲートウェイ、DNS、ポート、MACアドレス、IDを加算するスイッチ | 次の再起動のとき（またはIDを変えたとき）。動いている値は変わりません |
| `destIp`、`canSendMsgBeforeDestIp`、`reportError`（送信先を決める通常の方法は[`/setDestIp`](../reference/system-settings.md#setdestip)です） | すぐ |
| レポートのスイッチと間隔、原点復帰（方向、速度、タイムアウト、動作の禁止）、LIMITスイッチの設定、ブレーキの設定（下記）、サーボモード（kP、kI、kD） | すぐ |
| `bootedMsgEnable`、起動時の原点復帰 | 次の起動のとき |
| HOMEスイッチのモード | 2つに分かれます。サーボモードでHOMEスイッチで止める動作は、ファームウェアが新しい値をすぐに使います。ドライバは次の再起動から使います。ボードは、起動するときにドライバのレジスタに書くためです（次の行の設定と同じです）。従って、サーボモード以外でHOMEスイッチで止める動作は、次の再起動で変わります |
| ボードがドライバに書く設定（スピードプロファイル、電圧モードと電流モード（KVAL、TVAL、BEMFなど）、最小速度と低速最適化、マイクロステップモード、スルーレート、過電流とストールの閾値） | 次の再起動のとき。ボードは、起動するときにドライバのレジスタに書きます。[`/resetMotorDriver`](../reference/motor-driver-settings.md#resetmotordriver)でも、もう一度書きます |

ブレーキは、`electromagnetBrakeEnable`をオンにできるのはドライバが無励磁のときだけ、オフにできるのはドライバが無励磁で、ブレーキが保持されているとき（または`/free`のあと）だけです。そうでないときは、USBシリアルに警告を表示して、古い値のままにします（保存されるのは、変わらなかった値です）。保存したあとに、設定を読み直して確かめてください。

従って、ツールで保存したあとは、**ボードを再起動**して、すべての値を効かせてください。ツールは、保存のあとに再起動するかどうかを尋ねます。

## 保存されるもの {#what-is-saved}

[設定項目一覧](configuration-items.md)の項目の値が保存されます。v2.2.0からは、Rawコマンド（`/setSpeedProfileRaw`、`/setMaxSpeedRaw`、`/setMinSpeedRaw`、`/setFullstepSpeedRaw`、`/setAccRaw`、`/setDecRaw`）で設定した値も、保存されます。以前は、レジスタだけが変わっていました。

設定項目にないものは、保存されません。たとえば、位置、サーボモードの目標、サーボモードがオンかどうかです。

## 保存の間 {#saving}

ボードが設定を保存している間は、何も処理しません。`/saveConfig`で約0.1s（実測）、USBシリアルのコマンド`{`で転送を含めて最大約0.3s（実測）、カードを挿して最初の保存は最大約0.7s（実測）です。この間、ウォッチドッグは止まります。**保存する前に、モータを止めてください。**

## 方法の使い分け {#which-method}

- 現場で調整する: システムを動かしながらOSCコマンドで値を変え、よくなったら`/saveConfig`を送ります。
- パソコンで用意する: パソコンで設定ファイルを作り（[ブラウザ設定ツール](browser-config-tool.md)、または[パラメータ例](example-parameters.md)から）、カードにコピーします。
- ボードの設定を読んで、編集して保存する: USBで、ブラウザ設定ツールを使います。

## 関連するコマンドと設定項目 {#related}

<!-- osc-related: /getConfigName, /setConfigName, /saveConfig, /resetDevice -->
<!-- generated:begin osc-related /getConfigName, /setConfigName, /saveConfig, /resetDevice -->
**関連するコマンド**

| コマンド | 引数 | 説明 |
| --- | --- | --- |
| [`/getConfigName`](../reference/system-settings.md#getconfigname) | - | `/configName`を返します。設定名、microSDカードを使えたか、設定ファイルを開けたか・解析できたか、設定ファイルのパスが含まれます。 |
| [`/setConfigName`](../reference/system-settings.md#setconfigname) | (string)configName | ボードに保存される設定名を設定します。設定を見分けるためにユーザーが自由に編集できるラベルで、ディスク上のファイル名とは別のものです。 |
| [`/saveConfig`](../reference/system-settings.md#saveconfig) | - | 現在動作中の設定を、JSONファイルとしてmicroSDカードに保存します。保存先は、起動時に読み込んだファイルです。ファイルを読み込まなかったときは`/config.txt`です。USBシリアルの`F<path>`で、保存先のパスを変えられます。 |
| [`/resetDevice`](../reference/system-settings.md#resetdevice) | - | ボード全体をリセットします。ボード上のリセットスイッチを押した場合と同じ動作です。 |
<!-- generated:end osc-related /getConfigName, /setConfigName, /saveConfig, /resetDevice -->

<!-- osc-settings: information -->
<!-- generated:begin osc-settings information -->
**関連する設定項目**

| キー | 名称 | コマンド |
| --- | --- | --- |
| [`information.configName`](configuration-items.md#information-configname) | Configuration name | `/setConfigName` |
| [`information.configVersion`](configuration-items.md#information-configversion) | Configuration version |  |
| [`information.targetProduct`](configuration-items.md#information-targetproduct) | Target product |  |
<!-- generated:end osc-settings information -->
