## 診断ツール
### 概要
本デバイスのUSBコネクタとPCを接続し、PCから動作状況や設定を確認することができます。ネットワークからうまく接続できないときなどに問題を調べることができます。

### 接続
USB Type-CケーブルでPCと接続してください。USB端子からはマイコンと周辺回路の制御電源のみ供給されます。この状態ではモータドライバが起動していないため、モータドライバと通信ができません。必ずモータ電源を供給してください。

またUSBで給電をした後にモータ電源を接続した場合、モータドライバの初期設定が行われていない状態になるため、予想外の動作になる可能性があります。モータ電源を通電した後にUSBを差し込むか、あるいはモータ電源を通電した後に基板上のRESETスイッチを押して全体をリセットしてください。

### シリアルモニタ
本デバイスはPCからはArduino Zeroとして認識され、仮想シリアルポートになっています。例えばArduino IDEのシリアルモニタを使う場合は、以下の手順で接続してください。
Arduino IDEでなくても、シリアルポートと通信して文字列を入出力できるソフトウェアであればどのようなもので使えます。
#### Portの選択
Tools->Portから、Arduino Zero (Native USB Port)が見えると思いますので、そちらを選択してください。
![file](https://ponoor.com/cms/wp-content/uploads/2021/03/image-1616473811329.png)

#### シリアルモニタを開く
右上の虫眼鏡マークをクリックすると、シリアルモニタのウィンドウが開きます。

[![](https://ponoor.com/cms/wp-content/uploads/2021/03/openserialmonitor-486x525.png)](https://ponoor.com/cms/wp-content/uploads/2021/03/openserialmonitor.png)

#### メニューを表示させてみる
問題なく接続できていれば、上の送信フォームに`m`と入力してSendを押せば（あるいはリターンキーを押せば）、診断ツールのメニューが表示されるはずです。

![file](https://ponoor.com/cms/wp-content/uploads/2021/03/image-1616474112646.png)

これら3つの項目について説明していきます。
## Status
`s`を送信すると、主にハードウェアの状態を取得できます。
### Firmware
```
============== Current Status ==============
-------------- Firmware --------------
Firmware name : STEP400
Firmware version : 1.0.0
Compile date : Mar 19 2021, 10:27:55
Applicable config version : 1.0
Loaded config version : 1.0 [CONFIG_VERSION_APPLICABLE]
```
このセクションは主に書き込まれているファームウェアについての情報です。`Firmware name`の部分は機種によって異なります。

`Loaded config version`: microSDから読み込まれているconfig.txtファイルのバージョン番号が表示されます。configとファームウェアの新旧に応じて以下のうちどれかが表示されます。

| 文言 | 説明 |
| --- | ---|
|CONFIG_VERSION_UNDEFINED| configのバージョン未定義|
|CONFIG_VERSION_NOTLOADED|configがmicroSDから読み込まれていない|
|CONFIG_VERSION_OLD|configのバージョンが古い|
|CONFIG_VERSION_APPLICABLE|configとファームウェアのバージョンが合っている|
|CONFIG_VERSION_NEW|configのバージョンが新しい（ファームウェアが古い）|


### DIP Switch
```
-------------- DIP Switch --------------
BIN : 0000 0001
DEC : 1
```
基板上の`ID`スイッチの状態を示しています。
- `BIN`: スイッチの位置を0/1であらわしたものです。基板では左側が小さい桁ですが、診断ツールでは右側が小さい桁になっていることに注意してください。
- `DEC`: IDを10進数で表示したものです。

### Ethernet
```
-------------- Ethernet --------------
Ethernet hardware status: 3 -EthernetW5500
Ethernet link status: 2 -LinkOff
isDestIpSet : No
```

- `Ethernet hardware status`: イーサネットコントローラIC, W5500への接続状況を示しています。`EthernetW5500`が正しい反応で、`EthernetNoHardware`となる場合はW5500との通信に何らかの問題が生じています。
- `Ethernet link status`: Ethernetのリンク状況を示しています。

|Link Status| Description|
|---|---|
|LinkON|リンクしている|
|LinkOff|リンクしていない|
|Unknown|ステータスを取得できない|

- `isDestIpSet `: `destIp`がセットされたかどうかを示しています。`/setDestIp`コマンドが送られ、OSCの返送が可能になっている状態は`Yes`, そうではない場合は`No`です。

### microSD
```
-------------- microSD --------------
SD library initialize succeeded : Yes
SD config file open succeeded : Yes
SD config JSON parse succeeded : Yes
```
- `SD library initialize succeeded`: microSDカードがささっていないと`No`になります。
- `SD config file open succeeded`: SDカードの`config.txt`ファイルが開けたかどうかを示しています。
- `SD config JSON parse succeeded`: `config.txt`の内容(JSON)が読み込めたかどうかを示しています。

### Motor Driver
#### STEP400
```
-------------- Motor Driver --------------
PowerSTEP01 SPI connection established : Yes
PowerSTEP01 ID#1
	STATUS: 0xE603
	High impedance state : Yes
	BUSY : No
	Motor direction : Reverse
	Motor status : Stopped
	UVLO (Undervoltage lock out) : No
	Thermal status : Normal
	OCD (Overcurent detection) : No
	Stalled : No
	SW_F: 0 -HOME senser input open.
	ADC_OUT: 31 -LIMIT senser input open.
```

- `PowerSTEP01 SPI connection established`: PowerSTEP01と通信ができたかどうか。
`No`になる場合はモータ電源が給電されていない可能性があります。
- 以降の項目は通信ができた場合のみ表示されます。#1-#4まで4個分表示されます。

#### STEP800
```
-------------- Motor Driver --------------
L6470 SPI connection established : Yes
L6470 ID#1
        STATUS: 0x7E03
        High impedance state : Yes
        BUSY : No
        Motor direction : Reverse
        Motor status : Stopped
        UVLO (Undervoltage lock out) : No
        Thermal status : Stopped
        OCD (Overcurent detection) : No
        Stalled : No
        SW_F: 0 -HOME senser input open.
```

- `L6470 SPI connection established`: L6470と通信ができたかどうか。
`No`になる場合はモータ電源が給電されていない可能性があります。
- 以降の項目は通信ができた場合のみ表示されます。#1-#8まで8個分表示されます。


### Modes
```
-------------- Modes --------------
Servo Mode :  No, No, No, No
Current Mode :  No, No, No, No
Electromagnetic Brake Enable :  No, No, No, No
Brake status :
#1 : BRAKE_ENGAGED
#2 : BRAKE_ENGAGED
#3 : BRAKE_ENGAGED
#4 : BRAKE_ENGAGED
Homing status : 0, 0, 0, 0
```
#### Brake status
|Brake status| Description |
|---|---|
|BRAKE_ENGAGED|ブレーキ保持状態|
|BRAKE_DISENGAGE_WAITING|ブレーキ開放状態へ移行中|
|BRAKE_DISENGAGED|ブレーキ開放状態|
|BRAKE_MOTORHIZ_WAITING|ブレーキ保持状態へ移行中|

#### Homing status
|Number|Homing status|Description|
|---|---|---
|0|HOMING_UNDEFINED|原点復帰を行っていない状態|
|1|HOMING_GOUNTIL|センサへ向かって移動中|
|2|HOMING_RELEASESW|センサ反応範囲から脱出中|
|3|HOMING_COMPLETED|原点復帰完了済み|
|4|HOMING_TIMEOUT|原点復帰中にタイムアウトした|

## Config
`c`を送信すると、現在の設定値を読み出します。これはconfigToolのファイル内の値ではなく、IDスイッチの設定や、その後のOSCメッセージでの設定を反映した値になっていることに注意してください。例えばSTEP400でmicroSDカードを差し込まずに起動した場合の反応は以下のようになります。

```
============== Configurations ==============
-------------- Config file --------------
SD config file open succeeded : No
SD config file parse succeeded : No
configTargetProduct : ---
configName : Default
config version : -1.0 [CONFIG_VERSION_NOTLOADED]
-------------- Network --------------
My Ip : 10.0.0.101
isMyIpAddId : Yes
Dest Ip : 10.0.0.10
DNS : 10.0.0.1
Gateway : 10.0.0.1
Subnet mask : 255.255.255.0
MAC address : 60:95:CE:10:05:01
isMacAddId : Yes
inPort : 50000
outPort : 50101
isOutPortAddId : Yes
bootedMsgEnable : Yes
isDestIpSet : No
reportErrors : Yes
-------------- Report & Alarm --------------
reportBUSY :  No, No, No, No
reportBUSY :  No, No, No, No
reportHiZ :  No, No, No, No
reportHomeSwStatus :  No, No, No, No
reportLimitSwStatus :  No, No, No, No
reportDir :  No, No, No, No
reportMotorStatus :  No, No, No, No
reportSwEvn :  No, No, No, No
reportUVLO :  Yes, Yes, Yes, Yes
reportThermalStatus :  Yes, Yes, Yes, Yes
reportOCD :  Yes, Yes, Yes, Yes
reportStall :  Yes, Yes, Yes, Yes
reportOCD :  Yes, Yes, Yes, Yes
OCThreshold : 15, 15, 15, 15
-------------- driverSettings --------------
homingAtStartup :  No, No, No, No
homingDirection(1:FWD,0:REV) : 0, 0, 0, 0
homingSpeed : 50.00, 50.00, 50.00, 50.00
homeSwMode : 1, 1, 1, 1
prohibitMotionOnHomeSw :  No, No, No, No
limitSwMode : 1, 1, 1, 1
prohibitMotionOnLimitSw :  No, No, No, No
goUntilTimeout : 10000, 10000, 10000, 10000
releaseSwTimeout : 10000, 10000, 10000, 10000
microStepMode : 7, 7, 7, 7
isCurrentMode :  No, No, No, No
slewRate : 5, 5, 5, 5
electromagnetBrakeEnable :  No, No, No, No
brakeTransitionDuration : 100, 100, 100, 100
-------------- speedProfile --------------
acc : 1000.00, 1000.00, 1000.00, 1000.00
dec : 1000.00, 1000.00, 1000.00, 1000.00
maxSpeed : 650.00, 650.00, 650.00, 650.00
fullStepSpeed : 15610.00, 15610.00, 15610.00, 15610.00
-------------- Voltage mode --------------
kvalHold : 0, 0, 0, 0
kvalRun : 16, 16, 16, 16
kvalAcc : 16, 16, 16, 16
kvalDec : 16, 16, 16, 16
intersectSpeed : 1032, 1032, 1032, 1032
startSlope : 25, 25, 25, 25
accFinalSlope : 41, 41, 41, 41
decFinalSlope : 41, 41, 41, 41
stallThreshold : 31, 31, 31, 31
lowSpeedOptimize : 20.00, 20.00, 20.00, 20.00
-------------- Current mode --------------
tvalHold : 0, 0, 0, 0
tvalRun : 16, 16, 16, 16
tvalAcc : 16, 16, 16, 16
tvalDec : 16, 16, 16, 16
fastDecaySetting : 25, 25, 25, 25
minOnTime : 41, 41, 41, 41
minOffTime : 41, 41, 41, 41
-------------- Servo mode --------------
kP : 0.06, 0.06, 0.06, 0.06
kI : 0.00, 0.00, 0.00, 0.00
kD : 0.00, 0.00, 0.00, 0.00
```

## Test Motion
`t`を送信すると、すべてのモータが25600step正方向に動きます。
これは1周200stepのステッピングモータを1/128マイクロステッピングモードで動かした場合の1回転のステップ数に相当します。
