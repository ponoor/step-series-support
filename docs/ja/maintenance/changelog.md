---
title: ファームウェアの変更履歴
---

# ファームウェアの変更履歴

このページは、ファームウェアの各バージョンの変更点を、OSCクライアントを書く人、設定ファイルを作る人、ボードを使う人、ファームウェアを自分でビルドする人の立場でまとめたものです。全文はリポジトリの[CHANGELOG](https://github.com/ponoor/step-series-universal-firmware/blob/main/CHANGELOG.md)に、各バージョンのリリースはGitHubの[Releases](https://github.com/ponoor/step-series-universal-firmware/releases)にあります。リリースにはArduinoスケッチのソースだけが付いていて、ビルド済みのバイナリファイルはありません。ファームウェアは自分でビルドしてください（[ファームウェアのコンパイル](compile-the-arduino-sketch.md)）。

## v2.2.0 {#v2-2-0}

2026-10-20公開。OSCのアドレスはv2.1.0と互換ですが、多くのコマンドの動作が変わり、一部のコマンドはエラーを返すようになりました。**v2.1.0から更新するときは、先に[移行ガイド](migration-guide.md)をお読みください。** ファームウェアにはドライバライブラリv1.2.0が必要です（[ビルドとライブラリ](#v2-2-0-build)）。

### 動作の変更 {#v2-2-0-behavior}

#### 引数の検査とエラー {#v2-2-0-arguments}

- **コマンドを適用する前に引数を検査します**（すべてのコマンド）。引数が足りないと`/error/osc MissingArgument`、型が違う引数（数値の代わりの文字列、NaN、無限大、文字列以外を送った`/setConfigName`）には`/error/osc WrongDataType`を返し、どちらも何も適用しません。以前は、足りない引数や違う型の引数を0として適用していました（`/setKval 1`はそのモータのKVALをすべて0にしました）。余分な引数は今も無視します。0〜255の外のモータIDには`MotorIdNotMatch`を返し、エラーのモータIDには送った値が入ります。[エラー](../guides/communication-and-messages.md#errors)と[`/error/osc`](../reference/automatically-sent-messages.md#error-osc)をご覧ください。
- **コマンドの範囲の外の値は拒否します**。`/error/command CommandIgnored`を返し、何も適用しません。対象は、65535を超える[`/setPositionReportInterval`](../reference/motor-driver-settings.md#setpositionreportinterval)と[`/setPositionListReportInterval`](../reference/motor-driver-settings.md#setpositionlistreportinterval)（以前は32768以上が負の値として読まれ、レポートが無効になっていました）、0未満の[`/setGoUntilTimeout`](../reference/homing.md#setgountiltimeout)と[`/setReleaseSwTimeout`](../reference/homing.md#setreleaseswtimeout)（以前は約49日になっていました）、フルステップが0〜3の外またはマイクロステップが0〜127の外の[`/setElPos`](../reference/position-management.md#setelpos)、負のゲインの[`/setServoParam`](../reference/servo-mode_reference.md#setservoparam)、0〜65535の外の[`/setBrakeTransitionDuration`](../reference/brake.md#setbraketransitionduration)、そして[`/setDecayModeParam`](../reference/voltage-and-current-mode-settings.md#setdecaymodeparam)（STEP400）の127を超えるTON_MINとTOFF_MINです。
- **512バイトを超えるパケットと、17個以上の引数を持つメッセージ**には、`/error/osc OscSyntaxError`を返します。
- **ドライバが一部の状態でしか受け付けないレジスタ。** このレジスタに書き込むコマンドは、その状態にないモータには`/error/command MotorNotHiZ`または`MotorNotStopped`を返し、何も適用しません。たとえば[`/setMicrostepMode`](../reference/motor-driver-settings.md#setmicrostepmode)は出力が無励磁のとき、[`/setAcc`](../reference/speed-profile.md#setacc)は停止中にだけ受け付けます。以前は、ドライバが書き込みを無視してもファームウェアと保存される設定が値を受け取ったため、レジスタと保存された値が食い違っていました。[`/setVoltageMode`](../reference/voltage-and-current-mode-settings.md#setvoltagemode)と[`/setCurrentMode`](../reference/voltage-and-current-mode-settings.md#setcurrentmode)は、ドライバが受け付けたときだけモードを変えます。電流モードのSTEP400のモータへの`/setMicrostepMode`は、1/16より細かいステップモードには`CommandIgnored`を返します。255のときは、モータごとに判定します。
- **`HomeSwActivating`。** [`/goUntil`](../reference/homing.md#gountil)と[`/goUntilRaw`](../reference/motor-control.md#gountilraw)は、エラーの一覧にあるとおり`HomeSwActivating`を送ります（以前は`HomeSwActivated`でした）。`/reportError`に従います。サーボモード中のモータに対する`/goUntil`、`/goUntilRaw`、[`/releaseSw`](../reference/homing.md#releasesw)は`InServoMode`を返し、何もしません。
- 新しいコマンドのエラー: `BrakeReleaseFailed`、`BrakeEngagedOnHiZ`、`ServoModeCancelledOnHiZ`、`MotorNotHiZ`、`MotorNotStopped`。[`/error/command`](../reference/automatically-sent-messages.md#error-command)をご覧ください。

#### ボードが送るメッセージ {#v2-2-0-messages}

- **`/booted`に2番目の引数`resetCause`が付きました**: `/booted myId resetCause`。引数の数を厳密に確かめるクライアントは更新が必要です。番号は、0が不明、1が電源投入、2が電源電圧の低下、3がリセットピン、4がウォッチドッグ、5がソフトウェアリセット、6がCPU動作異常です。1と2はどちらも電源によるリセットとして扱い（SAMD21では、普通の電源投入でも2になることが多くあります）、知らない番号は「その他」として扱ってください。[`/booted`](../reference/automatically-sent-messages.md#booted)をご覧ください。
- **`T`/`F`で送っていた真偽値は、整数の0/1になりました**（型タグ`i`）。対象は、`/uvlo`の通知（[`/uvlo`](../reference/automatically-sent-messages.md#uvlo)）と、`/lowSpeedOptimizeThreshold`の3番目の引数（[`/getLowSpeedOptimizeThreshold`](../reference/motor-driver-settings.md#getlowspeedoptimizethreshold)）です。
- **[`/overCurrent`](../reference/automatically-sent-messages.md#overcurrent)と[`/stall`](../reference/automatically-sent-messages.md#stall)**は、状態が始まったときにすぐ送られ、続く間は、モータごと・種類ごとに最短200ms間隔で送られます。以前は、状態を読むたびに送っていました。
- **ドライバの状態を5msごとに読みます**（以前は10ms）。状態の通知（`/busy`、`/HiZ`、`/homeSw`、`/dir`、`/motorStatus`、`/swEvent`、`/uvlo`、`/thermalStatus`、`/limitSw`）は最大5ms早く届き、変化したときだけ送られる点は同じです。位置レポートとほかの10msごとの処理は変わりません。[通知のタイミング](../guides/alarms-and-protection.md#timing)をご覧ください。
- **[`/getStatus`](../reference/motor-driver-settings.md#getstatus)と[`/getStatusList`](../reference/motor-driver-settings.md#getstatuslist)は、ドライバのラッチされたフラグを消さなくなりました**。`/getStatus`がフラグを消したために通知が失われることはありません。フラグを消すのは状態のポーリングだけなので、最初の`/getStatus`の直後にもう一度送ると、同じフラグが見えることがあります。
- サーボモード中にドライバが自分で無励磁になったとき（過電流、過熱、UVLO）は、ブレーキの有無によらずサーボモードを解除して`/error/command ServoModeCancelledOnHiZ`を送ります。[ドライバが自分で無励磁になったとき](../guides/alarms-and-protection.md#hiz-by-itself)をご覧ください。
- 受信したアドレスパターンは、ファームウェア自身のパーサで照合します。まれなケース（たとえば`{...}`のリストの後ろに文字が続く場合）では、結果が以前と異なることがあります。

#### 設定と値 {#v2-2-0-settings}

- **Rawコマンドで行った設定は残ります**。`/setSpeedProfileRaw`、`/setMaxSpeedRaw`、`/setMinSpeedRaw`、`/setFullstepSpeedRaw`、`/setAccRaw`、`/setDecRaw`は、`/saveConfig`が保存し`/resetMotorDriver`が再び適用する設定も変えます。以前はレジスタだけを変えていました。`/setMinSpeedRaw`はビット12を無視します。[`/setAccRaw`](../reference/speed-profile.md#setaccraw)をご覧ください。
- [`/setStallThreshold`](../reference/alarm-settings.md#setstallthreshold)は、保存される値も変えます（以前はレジスタだけを変えていました）。1つのモータへの[`/setPositionReportInterval`](../reference/motor-driver-settings.md#setpositionreportinterval)は、保存されている位置リストレポートの間隔も消します。
- [`/getKval`](../reference/voltage-and-current-mode-settings.md#getkval)、[`/getTval`](../reference/voltage-and-current-mode-settings.md#gettval)、[`/getTval_mA`](../reference/voltage-and-current-mode-settings.md#gettval_ma)（STEP400）は、レジスタではなく設定を返します。ブレーキのあるモータで引き上げられたKVAL_HOLDも含みます。
- **[`/getSpeedProfile`](../reference/speed-profile.md#getspeedprofile)が返す加速度と減速度が約4.9%小さくなります**。データシートと一致するようになりました（ドライバライブラリv1.2.0）。[`/setAcc`](../reference/speed-profile.md#setacc)、`/setDec`、`/setSpeedProfile`は最も近いレジスタの値に丸めるので、書き込まれる値が1LSBずれることがあります。
- [`/getMinSpeed`](../reference/speed-profile.md#getminspeed)は、低速最適化が有効なモータには、1つのモータでも255でも0.0を返します。`/setMinSpeed 255`は、モータごとの低速最適化の設定を確かめます。[`/getDir`](../reference/motor-driver-settings.md#getdir)` 255`は回転方向を返します（以前は無励磁の状態を返していました）。
- STEP400: スルーレートの値5（980V/µs、初期値）が、データシートのとおりに書き込まれるようになり、初期設定のままでのスイッチングが以前より速くなります（[`driverSettings.slewRate`](../connections/configuration-items.md#driversettings-slewrate)）。最大速度0は、`/setMaxSpeed`、`/setSpeedProfile`、設定`maxSpeed`で1として書き込まれます。`/setFullstepSpeed`はBOOST_MODEビットを保ちます。
- `/setMinSpeedRaw`は、低速最適化が有効な間は保存される値だけを変えます。`/activate 1`はLEDを切り替えなくなりました（デバッグ用のコードでした）。[`/goUntilRaw`](../reference/motor-control.md#gountilraw)は速度を20ビットに制限し、`/goUntilRaw 255`は速度をレジスタの値として読みます。[`/releaseSw`](../reference/homing.md#releasesw)は、動作の引数をほかの真偽値の引数と同じように読みます（0.5は0でした）。
- **起動時の原点復帰**（`homingAtStartup`）は、ブレーキが有効なとき、先にブレーキを解放してから原点復帰を始めます（[`driverSettings.homingAtStartup`](../connections/configuration-items.md#driversettings-homingatstartup)）。

#### 動作、スイッチ、原点復帰 {#v2-2-0-motion}

- **[`/goTo`](../reference/motor-control.md#goto)、[`/goHome`](../reference/position-management.md#gohome)、[`/goMark`](../reference/position-management.md#gomark)、`/combine/goTo`が、HOMEスイッチまたはLIMITスイッチで動作を禁止しているときの回転方向を正しく判定します**（[`/setProhibitMotionOnHomeSw`](../reference/alarm-settings.md#setprohibitmotiononhomesw)、[`/setProhibitMotionOnLimitSw`](../reference/alarm-settings.md#setprohibitmotiononlimitsw)）。以前は、目標が2048ステップより近いと向きが逆になり、2^21ステップを超えるとまた誤っていました。今は、ドライバと同じ最短の向きです。スイッチの近くの動作が、v2.1.0と異なることがあります。
- **1つのモータへの[`/hardHiZ`](../reference/motor-control.md#hardhiz)は、先に減速停止を送らなくなりました**。どの形でも同じ動作になります。
- **停止と無励磁のコマンドは、ブレーキが無効なモータでも、待機中の動作を取り消します**。`/softStop`、`/hardStop`、`/softHiZ`、`/hardHiZ`、`/enableServoMode`、`/resetMotorDriver`が、BUSYフラグを待っている`/goTo`など、原点復帰、サーボモードを取り消します。以前は、止まったモータが再び動き出したり、取り消した原点復帰のタイムアウトが、無励磁にしたモータに即停止を送ったりしました。受け付けられた動作コマンドは、待っている`/goTo`も取り消します。
- 自動の即停止は、ブレーキが無効でも、ドライバが無励磁のモータには送られません（`/setProhibitMotionOnHomeSw`によるHOMEスイッチ、LIMITスイッチ、サーボモード中のスイッチのイベント、`/goUntil`と`/releaseSw`のタイムアウト）。即停止は無励磁のドライバを励磁します。原点復帰の状態を消す動作コマンドは、直接送った`/goUntil`の状態も消すようになりました。

#### サーボモード {#v2-2-0-servo}

- **更新周期は5msです**（以前は10msで、位置レポートが有効だと約7〜13msの間で揺れていました）。積分と微分の項は周期で換算するので、同じ`kP`、`kI`、`kD`でほぼ同じ応答になるように作られていますが、応答が変わることがあるので、必要ならゲインを調整し直してください。[サーボモード](../guides/servo-mode.md)をご覧ください。
- サーボモードを有効にすると、PID制御の積分と前回の誤差が消えます。位置の誤差は、ABS_POSの範囲の端を正しく折り返します。STEP400: HOMEスイッチとLIMITスイッチを別々に判定します。

#### 電磁ブレーキ {#v2-2-0-brake}

- **STEP800では、ブレーキ出力は、ブレーキの状態が変わるとすぐ変わります**（0.2〜0.3ms）。以前は10〜20ms後でした。
- **ブレーキは6つの状態を持つ状態機械に従います**。[`/getBrakeStatus`](../reference/brake.md#getbrakestatus)で取得できます。ブレーキが有効なモータでは、コマンドの動作が変わりました。詳しくは[コマンドとブレーキ](../guides/electromagnetic-brake.md#commands)の表をご覧ください。主な点は次のとおりです。
  - ブレーキが解放されているときの`/activate 1`は何もしません（以前は即停止を送っていました）。コマンドの後の状態の読み出しで、ドライバが励磁されているときだけブレーキを解放します。そうでなければブレーキは保持状態のままで、`BrakeReleaseFailed`を送ります。
  - 回転中のモータへの`/activate 0`は、減速し、停止したらブレーキを保持状態にします。`/softHiZ`と同じです。
  - `/free`の後は、動作コマンドか`/activate 1`でモータがReleased（解放）の状態に戻ります。モータが止まっても、ブレーキを保持状態にしなくなりました。
  - ブレーキが保持状態のとき、または`/free`の後は、`/softStop`、`/hardStop`、`/enableServoMode 0`は何もしません。ブレーキが解放されていないときの`/enableServoMode 1`と`/homing`は`BrakeEngaged`を返します。
  - `/resetMotorDriver`と`/enableElectromagnetBrake`は、安全な状態でだけ受け付けます。そうでなければ`CommandIgnored`です（USBシリアルで読み込む設定にも同じ規則が働き、警告を表示します）。
  - `/softHiZ`か`/activate 0`で減速している間に`/activate 1`や動作コマンドを受けると、ブレーキを保持状態にする予定が取り消され、ブレーキは解放されたままになります（以前は`/activate 1`が即停止を送り、あとでモータが止まるとブレーキが保持状態になりました）。停止中のモータでは、`/softHiZ`と`/activate 0`は次の状態の読み出し（最大5ms後）でブレーキを保持状態にします。`/free`の後の`/activate 0`、`/softHiZ`、`/hardHiZ`はすぐに保持状態にします。ブレーキが解放されているモータへの`/hardHiZ`は、先にモータを即停止します。
  - ドライバが自分で無励磁になると、ブレーキを保持状態にし、`BrakeEngagedOnHiZ`を送ります。
  - `/softHiZ`か`/activate 0`のために減速している間（Stopping）に停止コマンドを受けると、ブレーキを保持状態にする予定が取り消され、状態はReleasedに戻ります。これは意図した動作で、最後に受けたコマンドが優先されます（[ブレーキを保持状態にする途中での停止](../guides/electromagnetic-brake.md#stopping)）。
- **保持電流**: ブレーキが有効なモータが再び励磁されるたびに、KVAL_HOLD（TVAL_HOLD）がKVAL_RUN（TVAL_RUN）の半分以上に引き上げられます。`/free`の後も同じになりました（[保持電流](../guides/electromagnetic-brake.md#hold-current)）。
- **再起動、ウォッチドッグ、CPU動作異常**: [`/resetDevice`](../reference/system-settings.md#resetdevice)とUSBシリアルの`R`コマンドは、先に回転中のモータを止め、ブレーキを保持状態にし、移行時間の最大値（最大1s）を待ちます。**ウォッチドッグは、ボードの処理が約250ms止まると、それを検出します**。ブレーキの有無によりません（v2.1.0は約62.5ms）。これより長く処理を止めるコマンドや負荷があると再起動しますが、知られているものはありません。ブレーキがあるときは、先にすべてのブレーキを保持状態にし、最大1s後に再起動します（`resetCause`は4）。CPU動作異常のときは、すべてのブレーキを保持状態にして再起動し、`resetCause`は6です（[再起動、ウォッチドッグ、CPU動作異常](../guides/electromagnetic-brake.md#restart)）。
- **負荷を支えられない時間はなくなりません**。STEP800では、`setup()`でドライバをリセットする前にブレーキ出力を保持状態にします。電源投入時は、それまでの約250ms（ほとんどはブートローダ）は解放されたままで、電源によってはさらに長くなります（24Vで約2sの実測があります）。リセットや電源電圧の低下の後は、約0.5s解放されたままです。[負荷を支えられない時間](../guides/electromagnetic-brake.md#unsupported)をご覧ください。

#### ネットワーク {#v2-2-0-network}

- **`/destIp`が遅れて返ることがあります。** [`/setDestIp`](../reference/system-settings.md#setdestip)が送信先のMACアドレスの解決を始めたときは、アドレスが解決されてから返信します。有線では数ms、Wi-Fiでは数秒までかかります。返ってこなければ、`/setDestIp`を送り直してください。解決の間（数秒まで）は、送信先へのメッセージを捨てます。ブロードキャストの`/booted`は送られます。ボードが動いているかは、`/getVersion`のように返信のあるコマンドで確かめてください。[送信先と`/setDestIp`](../guides/communication-and-messages.md#setdestip)をご覧ください。
- **同じIPアドレスの別の機器（別のPCやネットワークアダプタ）に替えたクライアント**は、前の機器の最後のパケットから1.5s以上あとに、新しい機器から`/setDestIp`を送ると、使えるようになります。以前は、ボードを再起動するまで古いMACアドレスに送り続けていました。
- ARPに一度も答えない送信先への送信が、メッセージごとに処理を止めることはなくなりました。送信を1s止めてから再試行します（その間のメッセージは捨てられます）。W5500の再送時間は20ms、再試行は2回です。
- MACアドレスは、起動時、IDの変更の後、Ethernetのリンクが復帰したとき（`destIp`が設定されていれば）にも解決します。ボードは、ブロードキャストアドレスのUDPポート9と`destIp`のUDPポート9に、それぞれ1バイトを送り、その間`destIp`へのメッセージは捨てられます。`destIp`への送信が失敗すると送信を1s止め、`destIp`からのパケットで再開します。
- `isMyIpAddId`や`isOutPortAddId`で、.254を超えるアドレスや65535を超えるポートは使われなくなりました。IDを足さず、USBシリアルに警告を表示します（[ネットワークとDIPスイッチ](../connections/network-and-dip-switch.md)）。

#### microSDカード {#v2-2-0-sd}

- 名前が`.`で始まるファイル（macOSが書き込む`._name.json`など）は、設定ファイルの候補にしません。
- 受け付けられなかった設定ファイルの値は適用しません。初期値を使います。最初の`.json`ファイルが無効なら、そこで探索を終えます。優先順位は同じで、`config.txt`、続いて最初の有効な`.json`です。
- exFATのカードは`No SD card`として扱い、中身には触れません。PlatformIOのビルドもArduino IDEのビルドも同じです。カードはFAT16かFAT32でフォーマットしてください。
- 保存は、同じフォルダの隠しファイル`.<name>.tmp`に書き込み、書き終えてから保存先のファイルを置き換えます。保存に失敗しても古いファイルが残ります。[カードへの保存](../connections/microsd-card.md#saving)をご覧ください。
- ブラウザ設定ツールから受け取った設定は、IDの変更の後でDIPスイッチのIDが2回足されることはなくなりました。受け取ったIPアドレス、ポート、MACアドレスは、再起動で反映されます。

### 追加 {#v2-2-0-added}

- [`/getBrakeStatus`](../reference/brake.md#getbrakestatus): `/brakeStatus motorID state`を返信します（ブレーキが無効なモータは-1、そうでなければ0〜5）。番号は仕様です。
- USBシリアル: 送信先のMACアドレス（`s`、`T`の`destMac`と`arpPending`）、名前つきのブレーキの状態、`T`の`mcu`、`resetCause`、`resetCauseRaw`、コマンド`p`（処理時間の統計）。テスト用のビルド（`HIL_PROBE`）にはさらにコマンドがあります。[USBシリアル診断](usb-serial-diagnosis.md)をご覧ください。
- ハードウェアインザループのテスト装置`tools/hil/`と、処理時間の測定用のプローブ（STEP800、`HIL_PROBE`ビルド）は、ファームウェアの開発者向けです。

### 変更（内部） {#v2-2-0-changed}

OSCクライアントからは見えない、または処理時間にだけ現れる変更です。

- ウォッチドッグはAdafruit SleepyDogライブラリではなくファームウェア自身が動かします。メインループは5msごとのスロットで動きます。OSCメッセージは静的バッファで受信、振り分け、送信します（CNMAT OSCライブラリは使いません）。ドライバは1回のデイジーチェーン転送でまとめて読みます。
- USBシリアルの`R`は、返信の後で最低50ms待ってから再起動するので、返信が届きます。
- USBシリアルの`b`（ブレーキ出力のテスト）は、テスト用のビルドだけで使えます。通常のビルドからはなくなりました。

### 修正 {#v2-2-0-fixed}

- 2^31ms以上のタイムアウト（`goUntilTimeout`、`releaseSwTimeout`）が発生しなくなりました。以前は24.8日以上たつと発生していました。
- **CPU動作異常（HardFault）。** すべてのブレーキをすぐに保持状態にし、移行時間の後に再起動して、`resetCause`は6です。STEP400（R1）では、Ethernetをつないだ状態でUSBケーブルを抜くとCPU動作異常になることがあります。これはボードのハードウェアの問題で、v2.1.0でも起きるので、動作異常そのものは直っていません。変わったのは扱いです。先にブレーキを保持状態にし、再起動を通知します。[USBを抜くとSTEP400が再起動する](troubleshooting.md#usb-unplug)をご覧ください。
- `/setStallThreshold`が保存されない、位置レポートの間隔が32768以上でレポートが無効になる、`/setConfigName`が文字列以外を受け付ける（今は`WrongDataType`を返します）という不具合を直しました。[設定と値](#v2-2-0-settings)と[引数の検査とエラー](#v2-2-0-arguments)をご覧ください。
- サーボモード: 位置レポートがあると更新周期が約7〜13msの間で揺れていました。ブレーキが無効なとき、ドライバが自分で無励磁になっても、次の更新で再び励磁されていました。
- ボードの送信LED（TX）が、位置レポートの送信でも点滅するようになりました（以前はすぐに消えていました）。見た目だけの変更です。
- USBシリアル: 手で入力した`F<filename>`でボードが再起動する、`R`の返信が失われる、診断の出力のいくつかの項目が誤っていた、という不具合を直しました。
- `/resetDevice`がHardFaultを起こし、ウォッチドッグで再起動されていました。今はソフトウェアリセットで再起動し、`/booted`は5を通知します。
- 動作中のモータへの`/goTo`、`/goToDir`、`/goHome`、`/goMark`と、USBシリアルの`s`が、ドライバのラッチされたフラグを消し、通知が失われることがありました。
- Arduino IDEのビルド: exFATのカードに保存すると、カードのファイルが削除されていました。
- 古いファイルを削除した後で保存に失敗すると、設定ファイルがなくなっていました（[microSDカード](#v2-2-0-sd)）。
- DIPスイッチのIDをIPアドレスに足すとき、.254を超えるとブロードキャストアドレスになったり、数え直されたりしていました。

### ビルドとライブラリ {#v2-2-0-build}

- **ドライバライブラリv1.2.0が必要です**。Ponoor PowerSTEP01 Library（STEP400、STEP100）とPonoor L6470 Library（STEP800、STEP200）です。ファームウェアv2.1.0以前は1.1.xを使います。
- PlatformIOでは、ボードを`platformio.ini`の環境（`step400`、`step800`、`step100`、`step200`）で選びます。`src/boardsDef.h`の行のコメントを外す方法は使いません。Arduino IDEは今も`boardsDef.h`を使います。
- CNMAT OSCライブラリとAdafruit SleepyDogライブラリは不要になりました。SdFat 2.2.3以上、Ethernet 2.0.2以上、ArduinoJson 7.4.1以上（7.x）が必要です。SdFatのバージョンはv2.1.0と同じです。
- [ファームウェアのコンパイル](compile-the-arduino-sketch.md)をご覧ください。

### v2.2.0の既知の問題 {#v2-2-0-known-issues}

- **`canSendMsgBeforeDestIp`は、「`/setDestIp`を受信したか」と値を共有しています。** `/setDestIp`を受信した後に設定を保存する（`/saveConfig`、またはブラウザ設定ツール）と、カードに`true`が書き込まれます。ブラウザ設定ツールが`false`を書き込むと、`/setDestIp`をもう一度送るまで、ボードは返信を送りません。保存の後で`/setDestIp`をもう一度送り、保存したファイルの値を確かめてください。[`network.canSendMsgBeforeDestIp`](../connections/configuration-items.md#network-cansendmsgbeforedestip)と[`canSendMsgBeforeDestIp`の既知の問題](../connections/browser-config-tool.md#known-issue)をご覧ください。
- **設定ファイルなしでの保存。** 設定ファイルなしで起動した（カードがない、または有効なファイルがない）ボードで保存すると、書き込むバージョンと製品名がないので、ファイルは`information.configVersion`が`[-1, 0]`、`information.targetProduct`が`"---"`で書き込まれます。値は保存されます。正しいバージョンと製品名のファイルが必要なときは、ブラウザ設定ツールで作ってください（**Download JSON**）。[保存先](../connections/microsd-card.md#save-target)をご覧ください。
- **STEP400（R1）は、Ethernetをつないだ状態でUSBケーブルを抜くと再起動することがあります。** ハードウェアの問題で、v2.1.0と同じです。[STEP400](../hardware/step400.md#usb-unplug)をご覧ください。

## v2.1.0 {#v2-1-0}

2026年6月公開（[GitHub Release](https://github.com/ponoor/step-series-universal-firmware/releases/tag/v2.1.0)）。

### 新機能 {#v2-1-0-new}

- **ブラウザ設定ツールへの対応。** シリアルコマンドの`G`、`T`、`{...}`、`R`、`F`で、[ブラウザ設定ツール](../connections/browser-config-tool.md)がUSB（Web Serial API）で設定を読み書きできます。
- **[`/saveConfig`](../reference/system-settings.md#saveconfig)**は、カードを抜かずに、動作中の設定をmicroSDカードに保存します。
- **[`/setConfigName`](../reference/system-settings.md#setconfigname)**は設定名を設定します。[`/getConfigName`](../reference/system-settings.md#getconfigname)の返信には、5番目の引数`configFilename`（カード上のファイル名）が付きました。
- **長いファイル名。** 設定ファイルは8.3形式のファイル名に限られなくなりました。ファームウェアは先に`config.txt`を読み、次にアルファベット順で最初の`.json`ファイルを読みます（[ボードが読むファイル](../connections/microsd-card.md#files)）。

### 変更 {#v2-1-0-changes}

- SDライブラリを`arduino-libraries/SD`から`greiman/SdFat`v2に変えました（長いファイル名のため）。Arduino IDE用のスケッチのフォルダはリポジトリから削除しました。Arduino IDE用のスケッチは、各リリースのアセットの`step-series-universal-firmware.zip`です。
- STEP400の設定のキー`goUnitlTimeout`（テンプレートの綴りの誤り）を受け付けます。ファームウェアは`goUntilTimeout`を読み、なければ`goUnitlTimeout`を読みます。以前（v2.0.0）は`goUntilTimeout`しか読まなかったので、綴りの誤ったキーの値は黙って無視され、初期値（10000ms）が使われていました。

### 移行時の注意 {#v2-1-0-migration}

- v2.0.0の設定ファイルは互換です（設定のバージョンは同じです）。古いテンプレートから作ったSTEP400の設定ファイルには、`goUnitlTimeout`が入っていることがあります。v2.0.0はこの値を無視し、v2.1.0以降は使います。意図した値か確かめてください。キーを`goUntilTimeout`に直すことを勧めますが、必須ではありません。
- 長いファイル名が使えますが、`config.txt`が先に読まれる点は変わりません。

## v2.0.0 {#v2-0-0}

2025年10月公開（[GitHub Release](https://github.com/ponoor/step-series-universal-firmware/releases/tag/v2.0.0)）。**同じコマンドでも、実際の動きが変わります。**

- **速度の計算を、実際の動きに合うように直しました**。加速と減速には、v1.xの2倍の時間がかかります。速度はわずかに遅くなります。詳しくは、[PowerSTEP01ライブラリのissue](https://github.com/ponoor/Ponoor_PowerSTEP01_Library/issues/4)をご覧ください。
- **状態のポーリング周期を1msから10msに、サーボの更新周期を10msに変えました**。測定した処理速度に基づく変更で、OSC通信による干渉を減らします。サーボモードの目標位置への追従が、v1.xと異なることがあります（v2.2.0で、状態の読み出しとサーボの更新が5msになりました）。
- v1.xから更新するときは、動きを確かめ、スピードプロファイル、コマンドのタイミング、上位の制御を調整してください。

## それ以前のバージョン {#earlier}

STEPシリーズ（STEP400、STEP800、およびSTEP100 / STEP200の派生）のファームウェアは、v2.0.0より前は、リポジトリ[step-series-universal-firmware](https://github.com/ponoor/step-series-universal-firmware)でv0.xとv1.xとして開発されていました。これらのバージョンの詳しい変更履歴はありません。GitHubの[Releases](https://github.com/ponoor/step-series-universal-firmware/releases)とタグをご覧ください。それより前のSTEP400とSTEP800のファームウェアは、リポジトリ[ponoor/STEP400](https://github.com/ponoor/STEP400)と[ponoor/STEP800](https://github.com/ponoor/STEP800)にあります。
