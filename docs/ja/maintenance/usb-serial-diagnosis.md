---
title: USBシリアル診断
---

# USBシリアル診断

ボードのUSBコネクタにパソコンをつないで、状態や設定を確認できます。ネットワークからボードに届かないときなど、トラブルシューティングに役立ちます。USBシリアルは、[ブラウザ設定ツール](../connections/browser-config-tool.md)が使うコマンドも受け付けます。

> このページの出力の例は、実機からの出力ではなく、ファームウェアv2.2.0のソースコードから作りました。値は例です。

## 接続 {#connection}

ボードとパソコンを、USB Type-Cケーブルでつなぎます。USBから電源が供給されるのは、MCUと周辺回路だけです。この状態では、ドライバICに電源が入っていないので、ボードはドライバICと通信できません。モータの電源も入れてください。

USBを先につないで、モータの電源をあとから入れると、ドライバICは初期化されていない状態になります。ボードがドライバICを初期化するのは、起動するときだけだからです。先にモータの電源を入れてからUSBをつなぐか、モータの電源を入れたあとにRESETボタンを押してください。すべてのモータ（255）に[`/resetMotorDriver`](../reference/motor-driver-settings.md#resetmotordriver)を送ってもよいです。

EthernetをつないだままUSBケーブルを抜くと、STEP400（R1基板）は再起動することがあります。ハードウェアの問題です。ケーブルを抜く前に、モータを止めてください。[STEP400](../hardware/step400.md#usb-unplug)をご覧ください。

## シリアルモニタ {#serial-monitor}

ボードは、パソコンからはArduino Zeroとして認識され、仮想シリアルポートになります。例として、Arduino IDEのシリアルモニタを使う手順を示します。シリアルポートで文字列を送受信できるソフトウェアなら、どれでも使えます。

### ポートの選択 {#port}

「Tools」->「Port」から、「Arduino Zero（Native USB Port）」を選びます。

![file](https://ponoor.com/cms/wp-content/uploads/2021/03/image-1616473811329.png)

### シリアルモニタを開く {#open-monitor}

虫眼鏡のアイコンをクリックすると、シリアルモニタのウィンドウが開きます。

[![](https://ponoor.com/cms/wp-content/uploads/2021/03/openserialmonitor-486x525.png)](https://ponoor.com/cms/wp-content/uploads/2021/03/openserialmonitor.png)

### メニューを表示する {#menu}

上のテキストボックスに`m`と入力して、Sendボタン（またはReturnキー）を押します。接続できていれば、診断のメニューが表示されます。

![file](https://ponoor.com/cms/wp-content/uploads/2021/03/image-1616474112646.png)

ファームウェアv2.2.0のメニューは次のとおりです。

```
============== Diagnosis menu ==============
s: show status
c: show config
t: test motion
G: print config as JSON
T: print status as JSON
{: receive config JSON
F<filename>: set save filename
R: reboot board
p: print timing stats [us] and reset them
```

各コマンドを以下で説明します。Ethernetのリンクが変わったときは、`Ethernet link up`と`Ethernet link down`も表示されます。応答しない送信先への送信を止めたとき、再開したときにも、メッセージが表示されます。

## 状態（`s`） {#status}

`s`で、ハードウェアとファームウェアの状態が分かります。

### Firmware {#status-firmware}

```
============== Current Status ==============
-------------- Firmware --------------
Firmware name : STEP400_R1_UNIVERSAL
Firmware version : 2.2.0
Compile date : Oct 20 2026, 10:00:00
Applicable config version : 1.2
Loaded config version : 1.2 [CONFIG_VERSION_APPLICABLE]
Config and product match : Yes
```

ボードに書き込まれているファームウェアの情報です。`Firmware name`は製品によって異なります。

`Loaded config version`は、microSDカードから読み込んだ設定ファイルのバージョンです。設定とファームウェアのバージョンによって、次のどれかが表示されます。

| メッセージ | 説明 |
| --- | --- |
| CONFIG_VERSION_UNDEFINED | 設定のバージョンが未定義です |
| CONFIG_VERSION_NOTLOADED | 設定をmicroSDカードから読み込んでいません |
| CONFIG_VERSION_OLD | 設定のバージョンが古いです |
| CONFIG_VERSION_APPLICABLE | 設定とファームウェアのバージョンが合っています |
| CONFIG_VERSION_NEW | 設定のバージョンが、ファームウェアより新しいです（ファームウェアが古いです） |

`Config and product match`は、設定ファイルの製品名（`information.targetProduct`）がボードの製品と違うときに`No`になります。

### DIPスイッチ {#status-dip-switch}

```
-------------- DIP Switch --------------
BIN : 0000 0001
DEC : 1
```

ボードがDIPスイッチから読んだIDです。

- `BIN`: スイッチを0と1で表します。この出力では、最も下の桁が右にありますが、ボード上では左にあります（STEP400のDIPSW1）。
- `DEC`: IDを10進数で表します。

### Ethernet {#status-ethernet}

```
-------------- Ethernet --------------
Ethernet hardware status: 3 -EthernetW5500
Ethernet link status: 1 -LinkON
isDestIpSet : Yes
Destination Ip : 10.0.0.10
Current My Ip : 10.0.0.101
Current MAC address : 60:95:CE:10:06:01
Destination MAC address : AA:BB:CC:DD:EE:FF
Current outPort : 50101
```

- `Ethernet hardware status`: EthernetコントローラのW5500の状態です。正常なら`EthernetW5500`です。`EthernetNoHardware`は、ボードがW5500と通信できないことを表します。
- `Ethernet link status`: `LinkON`（リンクしている）、`LinkOff`（リンクしていない）、`Unknown`（状態を取得できない）のどれかです。
- `isDestIpSet`: 送信先が設定されていて、つまり[`/setDestIp`](../reference/system-settings.md#setdestip)を受信している（または、受信前にも送信する設定になっている）、ボードがOSCメッセージを送信できるときに`Yes`です。
- `Destination Ip`、`Current My Ip`、`Current MAC address`、`Current outPort`: 送信先と、ボードが今使っているIPアドレス、MACアドレス、送信ポートです。IDが加算されています。
- `Destination MAC address`: 最後の送信の宛先のMACアドレスです。最後の送信がブロードキャストだったときは、`FF:FF:FF:FF:FF:FF`です。

### microSD {#status-microsd}

```
-------------- microSD --------------
SD library initialize succeeded : Yes
SD config file open succeeded : Yes
SD config JSON parse succeeded : Yes
```

- `SD library initialize succeeded`: カードが挿されていないとき（またはカードがexFATのとき）は`No`です。
- `SD config file open succeeded`: カードの設定ファイルを開けたかどうかです。
- `SD config JSON parse succeeded`: ファイルの内容（JSON）を解析できたかどうかです。受け付けなかったファイルは適用されません。[microSDカードでの設定](../connections/microsd-card.md#order)をご覧ください。

### モータドライバ {#status-motor-driver}

```
-------------- Motor Driver --------------
Motor driver SPI connection established : Yes
Driver ID#1
	ABS_POS: 0x0 (0step)
	EL_POS: 0x0 (Fullstep:0, Microstep:0)
	...
	OCD_TH: 0xF (5000.0mA)
	STALL_TH: 0x1F (10000.0mA)
	...
	STATUS: 0x7E03
	  High impedance state : Yes
	  BUSY : No
	  Motor direction : Reverse
	  Motor status : Stopped
	  UVLO (Undervoltage lock out) : No
	  Thermal status : Normal
	  OCD (Overcurrent detection) : No
	  Stalled : No
	  SW_F: 0 -HOME sensor input open.
```

- `Motor driver SPI connection established`: `No`は、ボードがドライバICと通信できないことを表します。モータの電源が切れているのかもしれません。
- 各ドライバの詳細は、通信できているときだけ表示されます。レジスタ（位置、速度、KVAL、閾値、アラームの有効、CONFIGレジスタとそのフィールド）と、STATUSレジスタです。`OCD_TH`と`STALL_TH`の電流は、ボードのドライバに合わせて計算した値です。ドライバICは、モータ1から4（STEP400）、モータ1から8（STEP800）の順に表示されます。STEP400では、`UVLO_ADC`の行も表示されます。STEP400では、LIMITスイッチがオンになるとADCINがGNDに引かれて、`Yes`になります。
- STATUSのフラグは、ラッチされたフラグを消さずに読んでいます。

### モード {#status-modes}

```
-------------- Modes --------------
Servo Mode :  No, No, No, No
Current Mode :  No, No, No, No
Electromagnetic Brake Enable :  No, No, No, No
Brake status :
#1 : 0 ENGAGED
#2 : 0 ENGAGED
#3 : 0 ENGAGED
#4 : 0 ENGAGED
Homing status : 0, 0, 0, 0
```

- `Brake status`は、モータごとのブレーキの状態を、番号とともに表します。0 ENGAGED、1 RELEASING、2 RELEASED、3 STOPPING、4 ENGAGING、5 FREEです。[ブレーキの状態](../guides/electromagnetic-brake.md#states)をご覧ください。`Current Mode`は電流モードのあるボード（STEP400）に、ブレーキの行はブレーキ出力のあるボードに出ます。
- `Homing status`: [`/homingStatus`](../reference/automatically-sent-messages.md#homingstatus)の番号です。

## 設定（`c`） {#config}

`c`で、今動いている設定が分かります。設定ファイルの内容ではありません。DIPスイッチと、起動後にOSCメッセージで変えた内容が反映された、ボードが今使っている設定です。たとえば、カードなしで起動したときの先頭は次のようになります。

```
============== Configurations ==============
-------------- Config file --------------
SD config file open succeeded : No
SD config file parse succeeded : No
configTargetProduct : ---
Config and product match : No
configName : Default
config version : -1.0 [CONFIG_VERSION_NOTLOADED]
-------------- Network --------------
My Ip from Config : 10.0.0.100
isMyIpAddId : Yes
Dest Ip : 10.0.0.10
...
```

表示される項目は、設定ファイルの項目です。[設定項目一覧](../connections/configuration-items.md)をご覧ください。「from Config」と付いたアドレスとポートは、IDを加算する前の値です。

## テスト動作（`t`） {#test-motion}

`t`で、すべてのモータが25600ステップだけ正転します。200ステップのモータを1/128マイクロステップで動かしたときの、1回転です。今は始められないモータ（たとえば、ブレーキが有効で移行が終わっていないモータや、サーボモードのモータ）は、動きません。

## 設定のコマンド {#commands}

これらのコマンドは、[ブラウザ設定ツール](../connections/browser-config-tool.md)が使います。ふつうのシリアルターミナルからも送れます。

| コマンド | 説明 |
| --- | --- |
| `G` | 動いている設定を、1行のJSONで出力します |
| `T` | ボードとモータの状態を、1行のJSONで出力します |
| `{...}` | 設定のJSONオブジェクトを適用して、カードに保存します |
| `F<path>` | 次の再起動まで、次の保存の保存先を変えます |
| `R` | ボードを再起動します |
| `p` | 処理時間の統計を出力して、リセットします |

- **`G`**: `board`（製品、モータの数、ファームウェアのバージョン、設定ファイル名）と、設定の各セクションです。
- **`T`**: `board`には、製品、MCU（`mcu`）、リセットの原因（`resetCause`と、MCUの`resetCauseRaw`）、ファームウェアのバージョン、IPアドレス、ID、リンク、送信先のMACアドレス（`destMac`、6つの数。ブロードキャストのあとは255が6つ）、`arpPending`（送信先のMACアドレスを解決中かどうか）、カードと設定の状態が入っています。`motors`の各要素には、位置、速度、状態、スイッチの状態などが入っています。`ocd`と`stall`は、常にfalseです。これらにはOSCメッセージを使ってください。`resetCause`の意味は[`/booted`](../reference/automatically-sent-messages.md#booted)にあります。
- **`{...}`**: ボードは、設定を適用して、カードに書き、`{"result":"ok", ...}`またはエラーを返します。**送る前に、モータを止めてください。** 保存の間、ボードは何も処理しません（[設定の仕組み](../connections/how-settings-work.md#saving)をご覧ください）。効くときは[変更が効くとき](../connections/how-settings-work.md#when)をご覧ください。
- **`F<path>`**: 規則と、起動時にボードが読まないファイル名は、[`F<path>`で決めた名前](../connections/microsd-card.md#f-path)をご覧ください。
- **`R`**: 最初に`{"result":"ok","message":"Rebooting..."}`を返します。ボードは、少なくとも50ms待ち、回転しているモータを止めて、ブレーキを保持状態にし、移行時間（最大1s）を待ってから、再起動します。[再起動、ウォッチドッグ、CPU動作異常](../guides/electromagnetic-brake.md#restart)をご覧ください。
- **`p`**: ループと処理の時間（最大、平均、回数。単位はマイクロ秒）と、送信と、送信先のMACアドレスの解決のカウンタ（`udpSendFailed`、`udpSendDropped`、`arpResolve`、`arpProbe`など）です。[MACアドレスの解決](../guides/communication-and-messages.md#arp)をご覧ください。
