---
title: トラブルシューティング
---

# トラブルシューティング

症状ごとに、原因と対処を示します。各項目から、その内容を説明しているページにリンクしています。症状がここにないときは、USBケーブルをつないで、[ボードの状態](usb-serial-diagnosis.md#status)を確認してください。

## 通信 {#communication}

### 返信や位置レポートが届かない {#no-reply}

コマンドは効くのに、何も返ってこないことがあります。次の点を確認してください。

- **`/setDestIp`を送っていない。** ボードは、[`/setDestIp`](../reference/system-settings.md#setdestip)を受け取るまで、PCに何も送りません（`canSendMsgBeforeDestIp`の設定がオンのときを除きます）。[送信先と`/setDestIp`](../guides/communication-and-messages.md#setdestip)をご覧ください。
- **`/destIp`が返ってこない。** ボードは、返信する前に送信先のMACアドレスを解決しますが、失敗することがあります。`/setDestIp`を送り直してください。[MACアドレスの解決](../guides/communication-and-messages.md#arp)をご覧ください。
- **IPアドレス、サブネット、ポートが違う。** ボードとPCは、同じネットワークにある必要があります。DIPスイッチのIDは、IPアドレスと送信ポートに加算されるので、PCは、IDを加算したポートで受信する必要があります。結果が範囲を超えるときは、ボードはIDを加算せず、USBシリアルに警告を表示します。[ネットワークとDIPスイッチ](../connections/network-and-dip-switch.md#adding-id)をご覧ください。
- **PCのファイアウォールがメッセージを止めている。**
- USBで`s`を送り、`Ethernet link status`、`isDestIpSet`、`Destination Ip`を確認してください（[Ethernet](usb-serial-diagnosis.md#status-ethernet)）。

### PCを替えたら返信が届かなくなった（ファームウェアv2.1.0まで） {#pc-replaced}

v2.1.0までのファームウェアでは、同じIPアドレスの別のPC（または別のネットワークアダプタ）に替えると、ボードは古いPCのMACアドレスに送り続けます。コマンドは効きますが、返信もレポートも届かず、`/setDestIp`を送っても直りません。ボードを再起動するか、別のIPアドレスから先に`/setDestIp`を送ってから、元のIPアドレスで送り直してください。

v2.2.0では、新しいPCから`/setDestIp`を送ります。古いPCの最後のパケットから、1.5s以上あけてください。[`/setDestIp`を送るとき](../guides/communication-and-messages.md#when)をご覧ください。

## 設定とカード {#settings}

### 設定ファイルが読まれない {#config-not-read}

ボードは、ファイルを受け付けないと、初期値を使います。次の点を確認してください。

- **カードがexFATである。** 使えるのはFAT16とFAT32だけです。[カードの準備](../connections/microsd-card.md#card)をご覧ください。
- **起動したあとにカードを挿した。** ボードがカードを読むのは、起動するときだけです。ボードを再起動してください。
- **ファイルの名前や場所。** ボードが読むのは、ルートフォルダの`config.txt`と、最初の`*.json`（アルファベット順）だけです。`.`で始まるファイルとサブフォルダは無視され、パスは63文字までです。[ボードが読むファイル](../connections/microsd-card.md#files)をご覧ください。
- **`F<path>`で、ボードが読まない名前で保存した。** [`F<path>`で決めた名前](../connections/microsd-card.md#f-path)をご覧ください。
- **ファイルが有効でない。** `information.configVersion`のない`.json`ファイルや、JSONでないファイルは、適用されません。

ボードが何を読んだかは、[`/getConfigName`](../reference/system-settings.md#getconfigname)を送るか、USBシリアルの状態の[microSD](usb-serial-diagnosis.md#status-microsd)で確認できます。

### 設定の保存に失敗する {#save-fails}

メッセージは`No SD card`と`SD open failed`です。原因は[エラー](../connections/microsd-card.md#errors)をご覧ください。

### ブラウザ設定ツールにつながらない {#tool-no-connect}

ChromeまたはEdgeと、データ通信ができるUSBケーブルを使い、シリアルポートの一覧を確認してください。ツールの[トラブルシューティング](../connections/browser-config-tool.md#troubleshooting)をご覧ください。

## 動作 {#motion}

### モータが動かない {#motor-not-moving}

- **USBだけをつないでいる。** USBでは、ドライバICに電源が入りません。モータの電源を入れてください。[接続](usb-serial-diagnosis.md#connection)をご覧ください。
- **コマンドに`/error/command`が返ってくる。** エラーが理由を示します。たとえば、`BrakeEngaged`（ブレーキが解放されていない）、`MotorNotHiZ`、`MotorNotStopped`、`InServoMode`です。[`/error/command`](../reference/automatically-sent-messages.md#error-command)と[エラー](../guides/communication-and-messages.md#errors)をご覧ください。動作を始める条件は[動作開始条件](../reference/index.md#motion-start-condition)に、ブレーキの場合は[電磁ブレーキ](../guides/electromagnetic-brake.md#commands)にあります。エラーが届かないときは、エラーの報告をオフにしていないか確認してください（[`/reportError`](../reference/system-settings.md#reporterror)）。
- **スイッチが動作を禁止している。** [動作を禁止するスイッチ](../guides/alarms-and-protection.md#switches)をご覧ください。
- **ドライバが自分で無励磁になった**（過電流、過熱、電源電圧の低下）。[ドライバが自分で無励磁になったとき](../guides/alarms-and-protection.md#hiz-by-itself)をご覧ください。

### 原点復帰がすぐに`ReleaseSwTimeout`で終わる {#release-sw-timeout}

v2.1.0までのファームウェアでは、原点復帰がすぐに`ReleaseSwTimeout`（`/homingStatus`の4）で終わることがありました。起動のたびに、ほとんど毎回起きるか、ほとんど起きないかのどちらかでした。v2.2.0で修正されています。ファームウェアを更新してください（[ファームウェアの更新](firmware-update.md)）。

## ボードとファームウェア {#board}

### USBを抜くとSTEP400が再起動する {#usb-unplug}

Ethernetをつないだままでは、USBケーブルを抜くと、STEP400（R1基板）が再起動することがあります。ハードウェアの問題です。先にブレーキは保持状態になります。ケーブルを抜く前に、モータを止めてください。[STEP400](../hardware/step400.md#usb-unplug)をご覧ください。

### ファームウェアを書き込めない {#cannot-write}

RESETスイッチをダブルクリックして、ブートローダのモードにし、シリアルポートを選び直して、もう一度試してください。[ファームウェアを書き込むときの注意](compile-the-arduino-sketch.md#uploading)をご覧ください。

### 原因の分からない再起動をする {#unexpected-restart}

リセットの原因を見てください。[`/booted`](../reference/automatically-sent-messages.md#booted)の2番目の引数です（USBシリアルの`T`コマンドの`resetCause`でも分かります）。ウォッチドッグやCPU動作異常による再起動は、[再起動、ウォッチドッグ、CPU動作異常](../guides/electromagnetic-brake.md#restart)で説明しています。STEP400は、モータの突入電流で電源の電圧が下がったときにも、リセットされることがあります（[電源電圧](../connections/power-supply-and-motor.md#voltage)をご覧ください）。
