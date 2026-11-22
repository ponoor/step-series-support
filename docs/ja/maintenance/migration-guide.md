---
title: 移行ガイド
---

# 移行ガイド

このページは、ファームウェアをv2.1.0からv2.2.0に更新する人のためのものです。OSCのアドレスは互換ですが、多くのコマンドの動作が変わっていて、v2.1.0で動いていたクライアントや装置の動きが変わることがあります。以下の各項目に、何が変わったか、影響を受けるのはどんな場合か、何をすればよいかを書きました。詳しい説明は機能ガイドとリファレンスにあります。このページには要点と対処だけを書いています。変更点の全体は[変更履歴](changelog.md#v2-2-0)をご覧ください。

v2.0.0から更新する場合は、先に[v2.0.0からの更新](#from-v2-0-0)をお読みください。v2.1.0に戻したい場合は、[v2.1.0に戻す](#downgrade)をご覧ください。

## チェックリスト {#checklist}

一覧を見て、当てはまる項目を読んでください。

**OSCクライアント（ボードにコマンドを送るソフトウェア）を書いている場合:**

- [ ] クライアントが`/booted`の引数の数を確かめている → [`/booted`に引数が増えました](#booted)
- [ ] クライアントが`/uvlo`や`/lowSpeedOptimizeThreshold`を読んでいる → [真偽値は整数で送られます](#boolean-args)
- [ ] 引数が足りない、型が違う、範囲外の値になりうるコマンドを送っている → [誤ったコマンドは拒否されます](#rejected-args)
- [ ] モータが回転中、または励磁して位置を保っている間に、マイクロステップモード、スピードプロファイル、電圧モードか電流モード、減衰モードを変えている → [一部の状態でしか受け付けない設定](#register-states)
- [ ] KVAL、TVAL、スピードプロファイル、最小速度を読み返している → [getコマンドが返す値](#getters)
- [ ] Wi-Fiでボードと通信している、PCを替える、`/setDestIp`を死活監視に使っている → [`/setDestIp`と`/destIp`](#destip)
- [ ] `/getStatus`を読んでいる、`/overCurrent`や`/stall`を数えている → [状態のフラグと通知](#status-reports)
- [ ] サーボモードを使っている → [サーボモード](#servo)
- [ ] `/setProhibitMotionOnHomeSw`や`/setProhibitMotionOnLimitSw`を`/goTo`、`/goHome`、`/goMark`と一緒に使っている → [スイッチの近くでの回転方向](#switch-direction)
- [ ] 1つのモータへの`/hardHiZ`、または`/goTo`の待機中の停止コマンドを送っている → [停止コマンド](#stop-commands)
- [ ] 位置レポートの間隔を32767より大きくしている → [位置レポートの間隔](#report-interval)
- [ ] クライアントが原点復帰を再試行する、または`/homingStatus`の4を成功として扱っている → [原点復帰がすぐ`ReleaseSwTimeout`で終わらなくなりました](#homing-timeout)

**設定ファイルを作る、またはmicroSDカードを使う場合:**

- [ ] `/setAccRaw`などのRawコマンドを、`/saveConfig`や`/resetMotorDriver`と一緒に使っている → [Rawの設定は残ります](#raw-saved)
- [ ] 64GB以上のSDXCカード、またはMacでフォーマットしたカードを使っている → [exFATのカードと隠しファイル](#exfat)
- [ ] カードに無効な設定ファイルが入っていることがある → [無効なファイルは適用されません](#invalid-files)
- [ ] `myIp`や送信先ポートにIDを足している → [IDを足したアドレスとポート](#id-limits)
- [ ] `goUnitlTimeout`を含むSTEP400の設定ファイルがある → [`goUnitlTimeout`](#go-until-timeout)
- [ ] STEP400の既定のスルーレートを使っている → [STEP400のスルーレート](#slew-rate)
- [ ] ブラウザ設定ツールで設定を書き込んでいる → [ブラウザ設定ツールからの書き込み](#config-tool)

**電磁ブレーキを使っている場合:**

- [ ] ブレーキが有効なモータにコマンドを送っている → [コマンドと状態](#brake-commands)
- [ ] ブレーキと一緒に`homingAtStartup`やサーボモードを使っている → [コマンドと状態](#brake-commands)
- [ ] モータで負荷を支えている → [保持電流](#brake-hold-current)、[再起動、ウォッチドッグ、CPU動作異常](#brake-restart)、[負荷を支えられない時間](#brake-unsupported)

**ファームウェアを自分でビルドしている場合:**

- [ ] PlatformIOでビルドしている → [ボードの選び方](#board-select)
- [ ] Arduino IDEを使っている、またはライブラリを自分で管理している → [ライブラリ](#libraries)

## OSCクライアント {#osc-clients}

### `/booted`に引数が増えました {#booted}

**何が変わったか。** v2.1.0は`/booted myId`を送っていました。v2.2.0は`/booted myId resetCause`を送ります。`resetCause`は整数（`i`）です。

**影響を受けるのは。** `/booted`の引数の数を厳密に確かめるクライアントと、知らないリセットの原因で止まってしまうクライアントです。

**何をすればよいか。** 引数2つを受け付けてください。`1`（電源投入）と`2`（電源電圧の低下）は、どちらも電源によるリセットとして扱ってください。SAMD21では、普通の電源投入でも`2`になることが多くあります。新しく加わった`6`（CPU動作異常）も受け付け、知らない番号は「その他」として扱ってください。番号の意味は変わらず、新しい番号は7、8、...として加わります。詳しくは[`/booted`](../reference/automatically-sent-messages.md#booted)をご覧ください。

### 真偽値は整数で送られます {#boolean-args}

**何が変わったか。** `/uvlo`の通知（`/enableUvloReport`で有効にします）と、`/lowSpeedOptimizeThreshold`（`/getLowSpeedOptimizeThreshold`の返信）の3番目の引数は、OSCの型`T`と`F`で送られていました。今は、STEPシリーズのほかの真偽値と同じ整数の`0`と`1`（型タグ`i`）です。`/getUvlo`の返信は、以前から整数でした。

**影響を受けるのは。** この2つのメッセージで`T`/`F`を期待しているクライアントです。

**何をすればよいか。** この2つの引数を、整数の0/1として読んでください。真偽値を送るときは、整数の0/1を送ってください。ボードが受け付けるのは、1.0以上の数、正の整数、`T`で、これは変わっていません。詳しくは[`/uvlo`](../reference/automatically-sent-messages.md#uvlo)をご覧ください。

### 誤ったコマンドは拒否されます {#rejected-args}

**何が変わったか。** v2.1.0は、足りない引数や違う型の引数を0として適用していました。`/setKval 1`はモータ1のKVALをすべて0にし、`/setSpeedProfile 1`は加速度、減速度、最大速度を0にし、位置の数が足りない`/setTargetPositionList`は、足りないモータを位置0に向かわせました。v2.2.0は、何かを適用する前にコマンドを検査します。

- 引数が足りない: `/error/osc MissingArgument`
- 型が違う引数（数値の代わりの文字列、NaN、無限大）: `/error/osc WrongDataType`
- コマンドの範囲の外の値: `/error/command CommandIgnored motorID`（`/setPositionListReportInterval`では`255`）
- 0〜255の外のモータID: 送った値のまま`/error/command MotorIdNotMatch`（257と511は、1と255として読まれていました）
- 512バイトを超えるパケット、17個以上の引数を持つメッセージ: `/error/osc OscSyntaxError`
- 拒否ではありませんが、アドレスパターンはファームウェア自身のパーサで照合するようになり、まれなケース（たとえば`{...}`のリストの後ろに文字が続く場合）では結果がv2.1.0と異なることがあります。

コマンドを拒否したときは、何も適用しません。余分な引数は今も無視します。このほか、`/goUntil`と`/goUntilRaw`は、HOMEスイッチがオンのとき`HomeSwActivating`を送ります。v2.1.0は`HomeSwActivated`という文字列を送っていました。

**影響を受けるのは。** 不完全なコマンドや型の違うコマンドを送っているクライアント、以前の値に頼っているクライアント、特定のエラーの文字列を待つクライアント、範囲外の値でもコマンドが効くと考えているクライアントです。

**何をすればよいか。** 型と範囲が正しい数で、引数のそろったコマンドを送ってください。`/error/osc`と`/error/command`を表示するか記録し、エラーの通知は有効にしておいてください（`/reportError 1`。`/reportError 0`では何も送られませんが、コマンドは拒否されます）。エラーの文字列は`HomeSwActivating`で照合してください。範囲は各コマンドのリファレンスにあります。詳しくは[エラー](../guides/communication-and-messages.md#errors)と[ボードが受け取る引数](../guides/communication-and-messages.md#arguments)をご覧ください。

### 一部の状態でしか受け付けない設定 {#register-states}

**何が変わったか。** ドライバは、一部のレジスタを特定の状態でしか受け付けません。v2.1.0では、条件を満たさないset系のコマンドをドライバは無視しましたが、ファームウェアと保存される設定は新しい値を受け取ったため、レジスタと保存された値が食い違いました。v2.2.0は、コマンドを受けたときに状態を読み、状態に合わないモータにはエラーを返して何も適用しません。

- `/error/command MotorNotHiZ`: 出力が無励磁でなければなりません。`/setMicrostepMode`、`/setHomeSwMode`、`/setBemfParam`、`/setDecayModeParam`と、（STEP400の）`/setVoltageMode`、`/setCurrentMode`です。**励磁して位置を保っているモータは、無励磁ではありません。**
- `/error/command MotorNotStopped`: モータが停止中か無励磁でなければなりません。`/setAcc`、`/setDec`、`/setMinSpeed`、`/setSpeedProfile`、これらのRaw版、`/enableLowSpeedOptimize`、低速最適化が有効なときの`/setLowSpeedOptimizeThreshold`です。
- STEP400のモータが電流モードのときの`/setMicrostepMode`: 1/16より細かいステップモードには`CommandIgnored`を返します。
- `/setVoltageMode`と`/setCurrentMode`は、ドライバが受け付けたときだけモードを変えます。そうでなければ`CommandIgnored`です。

255のときは、モータごとに判定します。その状態にあるモータは変更され、ほかのモータはエラーを返します。

**影響を受けるのは。** モータの回転中や、励磁して位置を保っている間にこれらの設定を変えるクライアントです。

**何をすればよいか。** MotorNotHiZのグループは、先に`/softHiZ`か`/hardHiZ`を送ってください。MotorNotStoppedのグループは、先にモータを止めてください（停止して位置を保っている状態は受け付けられます）。エラーを処理してください。詳しくは[エラー](../guides/communication-and-messages.md#errors)と、各コマンドのリファレンス（たとえば[`/setMicrostepMode`](../reference/motor-driver-settings.md#setmicrostepmode)）をご覧ください。

### getコマンドが返す値 {#getters}

**何が変わったか。**

- `/getKval`、`/getTval`、`/getTval_mA`（STEP400）は、レジスタではなく設定（`/setKval`と`/setTval`が設定し、`/saveConfig`が保存する値）を返します。`/setKval`が書き換えるのは電圧モードのKVALのレジスタだけ、`/setTval`が書き換えるのは電流モードのTVALのレジスタだけです。そのため、使っていないほうのモードのレジスタには、以前の値が残っています。ブレーキのあるモータでは、引き上げられたKVAL_HOLD（TVAL_HOLD）を返します。STEP800は変わりません。
- `/getSpeedProfile`が返す加速度と減速度は、同じ動きでもv2.1.0より約4.9%小さくなります。データシートと一致するようになりました。`/setAcc`、`/setDec`、`/setSpeedProfile`は最も近いレジスタの値に丸めるので、書き込まれる値が1LSBずれることがあります。
- `/getMinSpeed`は、低速最適化が有効なモータには、1つのモータでも`255`でも`0.0`を返します。
- `/getDir 255`は回転方向を返します（以前は無励磁の状態を返していました）。
- STEP400: 最大速度0は1として書き込まれます。

**影響を受けるのは。** 設定した値と読み出した値を比べるクライアントや、これらの値を表示するクライアントです。

**何をすればよいか。** 数値を厳密に比べず、丸めを許してください。`/getSpeedProfile`が返す加速度を、値が適用されたかの確認に使わないでください。実際の動きが4.9%変わるのではなく、返される値が変わるだけです。詳しくは[`/getKval`](../reference/voltage-and-current-mode-settings.md#getkval)と[`/getSpeedProfile`](../reference/speed-profile.md#getspeedprofile)をご覧ください。

### `/setDestIp`と`/destIp` {#destip}

**何が変わったか。** `/setDestIp`が送信先のMACアドレスの解決を始めるとき（最初の`/setDestIp`、今の送信先と別のアドレスからの`/setDestIp`、送信先からの最後のパケットから1.5s以上あとの`/setDestIp`）は、アドレスが解決されてから返信`/destIp`を送ります。有線では数ms、Wi-Fiでは数秒までかかります。解決の間は、送信先へのメッセージ（返信、位置レポート、エラー）は、後で送られるのではなく捨てられます。ブロードキャストの`/booted`は送られます。そのかわり、同じIPアドレスの別の機器に替えたクライアントは、新しい機器から`/setDestIp`を送れば使えるようになりました。同じ解決は、起動時、IDの変更の後、リンクの復帰のときにも行われます。ARPに一度も答えない送信先があると、送信は1s止まり、その間のメッセージは捨てられます。

**影響を受けるのは。** 短いタイムアウトで`/destIp`を待つクライアント、Wi-Fiのクライアント、1秒ごとに死活監視として`/setDestIp`を送るクライアント、PCやネットワークアダプタを替える装置です。

**何をすればよいか。** `/destIp`を数秒待ち、来なければ`/setDestIp`を送り直してください。`/setDestIp`は、接続を始めるときと、ネットワークやPCを替えたとき（前のものの最後のパケットから1.5s以上あと）に送ってください。Wi-Fiでの解決は、ボードの処理を最大約41msずつ止めることがあるので、モータを止めているときに送ってください。ボードが動いているかは、`/setDestIp`ではなく、`/getVersion`のように返信のあるコマンドで確かめてください。詳しくは[送信先と`/setDestIp`](../guides/communication-and-messages.md#setdestip)と[`/setDestIp`](../reference/system-settings.md#setdestip)をご覧ください。

### 状態のフラグと通知 {#status-reports}

**何が変わったか。**

- `/getStatus`と`/getStatusList`は、ドライバのラッチされたフラグ（OCD、ストールのフラグ、UVLO、SW_EVN）を消さなくなりました。フラグを消すのは、ファームウェアの状態のポーリング（5msごと）だけです。`/getStatus`の直後に続けて`/getStatus`を送ると、前の返信で見えたフラグが、また見えることがあります。
- `/setStallThreshold`は保存される値も変えるので、`/saveConfig`と`/resetMotorDriver`がその値を使います。
- `/overCurrent`と`/stall`は、状態が始まったときにすぐ送られ、続く間は、モータごと・種類ごとに最短200ms間隔で送られます。以前は、状態を読むたびに送られていました。
- 状態を10msではなく5msごとに読むので、状態の通知（`/busy`、`/HiZ`、`/homeSw`など）は最大5ms早く届きます。変化したときだけ送られる点は同じです。

**影響を受けるのは。** `/getStatus`でフラグを消しているクライアントや、`/overCurrent`と`/stall`のメッセージの数を、状態が続いた長さの目安にしているクライアントです。

**何をすればよいか。** フラグを消すために`/getStatus`に頼らないでください。メッセージの数ではなく、メッセージの間隔（最短200ms）を使ってください。詳しくは[通知のタイミング](../guides/alarms-and-protection.md#timing)をご覧ください。

### サーボモード {#servo}

**何が変わったか。** 更新周期は10msから5msになりました（位置レポートが有効なときに約7〜13msの間で揺れることもなくなりました）。積分と微分の項は周期で換算するので、同じ`kP`、`kI`、`kD`でほぼ同じ応答になるように作られていますが、応答が変わることがあります。サーボモードを有効にすると、積分と前回の誤差が消えます。サーボモード中のモータへの`/goUntil`、`/goUntilRaw`、`/releaseSw`は`InServoMode`を返し、何もしません。ドライバが自分で無励磁になったとき（過電流、過熱、UVLO）は、サーボモードが解除され、`ServoModeCancelledOnHiZ`が送られます。再開は`/enableServoMode 1`です（今の位置が目標になります）。ブレーキが有効なときは、[コマンドと状態](#brake-commands)も見てください。

**影響を受けるのは。** サーボモードを使うすべての人と、過電流の遮断の後もサーボモードが続くと考えているクライアントです。

**何をすればよいか。** サーボモードの応答を確かめ、必要ならゲインを調整し直してください（[制御パラメータの決定方法](../guides/servo-mode.md#tuning)）。`ServoModeCancelledOnHiZ`を処理してください。詳しくは[サーボモード](../guides/servo-mode.md)と[ドライバが自分で無励磁になったとき](../guides/alarms-and-protection.md#hiz-by-itself)をご覧ください。

### スイッチの近くでの回転方向 {#switch-direction}

**何が変わったか。** `/goTo`、`/goHome`、`/goMark`、`/combine/goTo`は、HOMEスイッチまたはLIMITスイッチで動作を禁止しているとき（`/setProhibitMotionOnHomeSw`、`/setProhibitMotionOnLimitSw`）の回転方向を正しく判定します。v2.1.0では、目標が2048ステップより近いと向きが逆になり（スイッチから離れる短い移動が`HomeSwActivating`か`LimitSwActivating`で拒否され、スイッチへ向かう短い移動が始まりました）、2^21ステップを超えるとまた誤っていました。今は、ドライバと同じ最短の向きです。

**影響を受けるのは。** これらの設定を、スイッチの近くで`/goTo`などと一緒に使っている装置です。特に短い移動で、v2.1.0と動きが異なることがあります。

**何をすればよいか。** スイッチの近くの動作を、もう一度試してください。以前の向きに合わせて作った回避策は、もう要りません。詳しくは[スイッチによる動作の禁止](../guides/alarms-and-protection.md#switches)をご覧ください。

### 停止コマンド {#stop-commands}

**何が変わったか。**

- 1つのモータへの`/hardHiZ`は、即停止して無励磁にする前に、減速停止を送らなくなりました。1つのモータ、`255`、`/combine/hardHiZ`は同じ動作になります。ブレーキが有効で解放されているときは、ブレーキを保持状態にする前にモータを即停止します。
- `/goUntilRaw 255`は、1つのモータへの`/goUntilRaw`と同じように、速度をレジスタの値として読みます（以前はステップ/sでした）。
- `/softStop`、`/hardStop`、`/softHiZ`、`/hardHiZ`、`/enableServoMode`、`/resetMotorDriver`は、ブレーキが無効なモータでも、待機中の動作を取り消します。BUSYフラグを待つ`/goTo`、`/goToDir`、`/goHome`、`/goMark`、原点復帰、サーボモードです。以前は、停止したモータが後から再び動き出すことがありました。また、取り消した原点復帰のタイムアウトが即停止を送り、無励磁にしたモータを励磁してしまうことがありました。受け付けられた動作コマンドは、待っている`/goTo`も取り消します。
- 自動の即停止（`/setProhibitMotionOnHomeSw`によるHOMEスイッチ、LIMITスイッチ、サーボモード中のスイッチのイベント、`/goUntil`と`/releaseSw`のタイムアウト）は、ドライバが無励磁のモータには送られません。

**影響を受けるのは。** 停止コマンドを送った後で、先に送った`/goTo`が後から始まることに頼っているクライアントや、即停止で無励磁のモータを励磁することに頼っているクライアントです。

**何をすればよいか。** 停止コマンドの後は、動作コマンドを送り直してください。モータを励磁するときは、停止ではなく動作コマンドを使ってください。詳しくは[停止の種類](../guides/speed-profile-and-motions.md#stops)をご覧ください。

### 位置レポートの間隔 {#report-interval}

**何が変わったか。** `/setPositionReportInterval`と`/setPositionListReportInterval`の間隔は0〜65535msです。v2.1.0は32768以上を負の値として読み、レポートを無効にしていました。65535を超える値には`CommandIgnored`を返します。負の間隔は今もレポートを無効にします。1つのモータへの`/setPositionReportInterval`は、保存されている位置リストレポートの間隔も消します。

**影響を受けるのは。** 32768ms以上の間隔を設定するクライアントです。

**何をすればよいか。** 65535までの値を使ってください（0や負の値でレポートを無効にするのは、以前と同じです）。詳しくは[`/setPositionReportInterval`](../reference/motor-driver-settings.md#setpositionreportinterval)をご覧ください。

### 原点復帰がすぐ`ReleaseSwTimeout`で終わらなくなりました {#homing-timeout}

**何が変わったか。** v2.1.0以前では、`/homing`がスイッチを見つけた約1ms後に、3ではなく`/homingStatus`の4と`ReleaseSwTimeout`で終わることがよくありました。ほとんどの原点復帰で起きるか、ほとんど起きないかは、起動のたびに決まっていました。タイムアウトの経過時間の計算の誤りで、v2.2.0で直りました。

**影響を受けるのは。** この誤りを避けるために、原点復帰を再試行したり、`/homingStatus`の4を成功として扱ったりしていたクライアントです。

**何をすればよいか。** 再試行をやめてください。3を原点復帰の終了、4を`/releaseSw`の本当のタイムアウトとして扱ってください。詳しくは[原点復帰がすぐに`ReleaseSwTimeout`で終わる](troubleshooting.md#release-sw-timeout)と[修正](changelog.md#v2-2-0-fixed)をご覧ください。

## 設定ファイルとmicroSDカード {#config-files}

### Rawの設定は残ります {#raw-saved}

**何が変わったか。** `/setSpeedProfileRaw`、`/setMaxSpeedRaw`、`/setMinSpeedRaw`、`/setFullstepSpeedRaw`、`/setAccRaw`、`/setDecRaw`は、`/saveConfig`が保存し`/resetMotorDriver`が再び適用する設定（故障の後のリセットも含みます）も変えるようになりました。v2.1.0ではレジスタだけを変えていたので、リセットや保存された設定で、以前の値に戻りました。残る値は、同じRawの値に換算し直せる値なので、`/getMinSpeed`や`/getFullstepSpeed`の値と、レジスタの刻みの半分だけずれることがあります。`/setMinSpeedRaw`はビット12を無視します（低速最適化を有効にしてしまうためです）。

**影響を受けるのは。** Rawコマンドを`/saveConfig`と一緒に使っている装置や、リセットで以前の値に戻ることを前提にしていた装置です。

**何をすればよいか。** たいていは何も要りません。Rawの設定はリセットの後も残り、保存されます。リセットでRawの設定を取り消すことに頼っていたなら、以前の値を送り直してください。詳しくは[`/setAccRaw`](../reference/speed-profile.md#setaccraw)と[保存されるもの](../connections/how-settings-work.md#what-is-saved)をご覧ください。

### 無効なファイルは適用されません {#invalid-files}

**何が変わったか。** 受け付けられなかった設定ファイルの値は、適用されなくなりました。v2.1.0では、`information.configVersion`のない最初の`.json`ファイルや、途中で解析に失敗した`config.txt`は、`/getConfigName`の返信で読み込めなかったと分かっても、その値（または失敗までの値）が使われていました。今は、カードがないときと同じように、既定値が使われます。優先順位は同じで、`config.txt`、続いてアルファベット順で最初の`.json`ファイルです。そのファイルが無効なら、探索は終わり、既定値になります。

**影響を受けるのは。** 無効なファイルが入っているカードと、Macでコピーしたカード（次の項目）です。

**何をすればよいか。** 起動したら、`/getConfigName`（openとparseの引数）かUSBシリアルの`s`で確かめてください。設定ファイルを有効にするか、無効なファイルを取り除いてください。詳しくは[ボードが読むファイル](../connections/microsd-card.md#files)をご覧ください。

### exFATのカードと隠しファイル {#exfat}

**何が変わったか。**

- 名前が`.`で始まるファイルは、設定ファイルの候補にしません。MacはFATのカードにコピーするファイルごとに、隠しファイル`._name.json`を書き込みます。v2.1.0では、これが先頭に並び、JSONではないため、後ろにある有効な`.json`ファイルがすべて見つからなくなりました。
- exFATのカード（SDXCの64GB以上は既定でexFAT）は「カードなし」として扱い、中身には触れません。v2.1.0のArduino IDEのビルドは、exFATのカードに保存するとき、設定ファイルを削除していました。

**影響を受けるのは。** SDXCカードを使う人と、Macでコピーしたカードを使う人です。

**何をすればよいか。** カードをFAT16かFAT32でフォーマットしてください（64GB以上はFAT32。macOSのディスクユーティリティでは「MS-DOS（FAT）」）。詳しくは[カードの準備](../connections/microsd-card.md#card)をご覧ください。

### 保存と一時ファイル {#saving}

**何が変わったか。** 保存は、同じフォルダの隠しファイル`.<name>.tmp`に設定を書き込み、書き終えて閉じてから、保存先のファイルを置き換えます。保存に失敗しても（カードやルートフォルダがいっぱい、書き込みエラー）、古いファイルは残り、`SD open failed`を返します。保存先は、起動時に読んだファイルです（読んでいなければ`/config.txt`）。古いファイルを削除してから新しいファイルの名前を変えるまでの間に電源が切れると、一時ファイルだけが残り、起動時に回復する処理はありません。

**影響を受けるのは。** 保存するすべての人です。失敗した後のカードに`.tmp`ファイルが見えることがありますが、読まれません。

**何をすればよいか。** 保存中に電源を切らないでください。`.tmp`ファイルだけが残ったときは、設定ファイルの名前に変えてください。詳しくは[カードへの保存](../connections/microsd-card.md#saving)をご覧ください。

### IDを足したアドレスとポート {#id-limits}

**何が変わったか。** `isMyIpAddId`のとき、`myIp`の最後の数にIDを足した値は254までです（既定の10.0.0.100ではID 154まで）。超えると、IDを足さず、設定のアドレスを使い、USBシリアルに警告を表示します。v2.1.0は、ブロードキャストアドレス（.255）になったり、数え直された値（.0〜.99）になったりしていました。`isOutPortAddId`の送信先ポートも、65535を超えると同じです。

**影響を受けるのは。** 多数のボードを使い、IDが上限に達する装置です。

**何をすればよいか。** 足した値が上限に収まるように、`myIp`とIDを選んでください。詳しくは[ネットワークとDIPスイッチ](../connections/network-and-dip-switch.md)をご覧ください。

### `goUnitlTimeout` {#go-until-timeout}

**何が変わったか。** STEP400の設定ファイルのテンプレートには、かつてキー`goUnitlTimeout`（綴りの誤り）がありました。v2.0.0は`goUntilTimeout`しか読まないので、綴りの誤ったキーの値は無視され、既定値（10000ms）が使われました。v2.1.0とv2.2.0は、`goUntilTimeout`を読み、なければ`goUnitlTimeout`を読みます（起動時にファイルを読み込むとき。ブラウザ設定ツールの書き込みは`goUntilTimeout`だけを読みます）。従って、v2.1.0からv2.2.0では何も変わりません。

**影響を受けるのは。** 10000以外の値の`goUnitlTimeout`を含むファイルをv2.0.0から新しいファームウェアに移すと、その値が使われるようになります。

**何をすればよいか。** 値を確かめて、キーを`goUntilTimeout`に直してください。詳しくは[`driverSettings.goUntilTimeout`](../connections/configuration-items.md#driversettings-gountiltimeout)をご覧ください。

### STEP400のスルーレート {#slew-rate}

**何が変わったか。** 初期値であるスルーレートの値5（980V/µs）は、v2.1.0では誤った値（64mAと2375ns）がドライバに書き込まれていて、980V/µsより遅いスイッチングになっていました。v2.2.0はデータシートのとおり（96mA、375ns）に書き込みます。初期設定のままのボードでは、スイッチングが以前より速くなります。0〜4の値は変わりません。STEP800は影響を受けません。

**影響を受けるのは。** 既定のスルーレートを使うSTEP400です。

**何をすればよいか。** 実機でドライバの温度と電磁ノイズ（EMI）を確かめてください。必要なら、`driverSettings.slewRate`をより小さい値にしてください。詳しくは[`driverSettings.slewRate`](../connections/configuration-items.md#driversettings-slewrate)をご覧ください。

### ブラウザ設定ツールからの書き込み {#config-tool}

**何が変わったか。** ブラウザ設定ツールで設定を書き込む（USBシリアルの`{`コマンド）と、ボードの処理が短い間止まります。これは以前と同じです（約0.1〜0.3s、カードを挿して最初の保存は最大約0.7s。実測）。ブレーキの設定の変更は、`/enableElectromagnetBrake`の規則（[コマンドと状態](#brake-commands)）で判定され、励磁されているモータでは適用されず、警告が表示されます。受け取ったIPアドレス、ポート、MACアドレスは、IDを足さずに保存されるので、IDを変えた後でIDが2回足されることはなくなり、次の再起動で反映されます。

**影響を受けるのは。** モータが動いている間に設定を書き込む人です。

**何をすればよいか。** 書き込む前にモータを止めてください。[`canSendMsgBeforeDestIp`の既知の問題](../connections/browser-config-tool.md#known-issue)にも注意してください。詳しくは[ブラウザ設定ツール](../connections/browser-config-tool.md#saving)をご覧ください。

## 電磁ブレーキ {#brake}

この節は、ブレーキを有効にしたモータ（`/enableElectromagnetBrake`）のためのものです。ブレーキが無効なモータは、[停止コマンド](#stop-commands)を除いて影響を受けません。

### コマンドと状態 {#brake-commands}

**何が変わったか。** ブレーキは、6つの状態を持つ新しい状態機械に従います。`/getBrakeStatus`で取得できます。要点は次のとおりです。

- STEP800では、ブレーキの状態が変わるとすぐ、ブレーキ出力が変わります（コマンドの0.3ms以内。以前は10〜20ms後）。
- ブレーキが解放されているときの`/activate 1`は何もしません（以前は即停止を送っていました）。コマンドの後の状態の読み出しで、ドライバが励磁されているときだけブレーキを解放します。そうでなければブレーキは保持状態のままで、`BrakeReleaseFailed`を送ります。以前は、どんな場合も`brakeTransitionDuration`の後にブレーキを解放していました。
- 回転中のモータへの`/activate 0`は、減速し、停止したらブレーキを保持状態にします。`/softHiZ`と同じです。以前は、モータを止めずにブレーキを保持状態にしていました。
- ブレーキが保持状態のとき、または`/free`の後は、`/softStop`、`/hardStop`、`/enableServoMode 0`は何もしません。ブレーキが解放されていないときの`/enableServoMode 1`と`/homing`は、`BrakeEngaged`を返して何もしません。
- `/softHiZ`か`/activate 0`のために減速している間（Stopping状態）に停止コマンドを受けると、ブレーキを保持状態にする予定が取り消され、状態はReleasedに戻ります。モータは励磁されたままです。最後に受けたコマンドが優先されます。ブレーキを保持状態にしたいときは、`/softHiZ`、`/activate 0`、`/hardHiZ`を送り直してください。
- `/free`の後は、動作コマンドか`/activate 1`でモータが励磁され、Releasedに戻ります。
- `/resetMotorDriver`は、ブレーキが保持状態のとき、または`/free`の後にだけ受け付けます。`/enableElectromagnetBrake`は、ドライバが無励磁のときだけ設定を変えます。そうでなければ`CommandIgnored`です。
- ドライバが自分で無励磁になると、次の状態の読み出しでブレーキを保持状態にし、`BrakeEngagedOnHiZ`を送ります。
- `/softHiZ`か`/activate 0`のための減速中の`/activate 1`や動作コマンドは、保持状態にする予定を取り消します（以前は`/activate 1`が即停止を送りました）。
- 起動時の原点復帰（`homingAtStartup`）は、先にブレーキを解放し、解放が終わってから原点復帰を始めます。
- ブレーキの時間は5msの刻みで数えます。解放は、`brakeTransitionDuration`の0〜5ms後になります。

**影響を受けるのは。** ブレーキを有効にしたモータを制御するクライアントです。

**何をすればよいか。** 開始には`/activate 1`を使い（動作コマンドを送る前に、`/getBrakeStatus`で状態が2、Releasedになったことを確かめます）、停止には`/softHiZ`か`/activate 0`を使い、`BrakeEngaged`、`BrakeReleaseFailed`、`BrakeEngagedOnHiZ`を処理してください。`/activate`の以前の動作に頼らないでください。詳しくは[コマンドとブレーキ](../guides/electromagnetic-brake.md#commands)の表、[ブレーキの状態](../guides/electromagnetic-brake.md#states)、[ブレーキを保持状態にする途中での停止](../guides/electromagnetic-brake.md#stopping)をご覧ください。

### 保持電流 {#brake-hold-current}

**何が変わったか。** ブレーキのあるモータが再び励磁されるたびに、KVAL_HOLD（電流モードではTVAL_HOLD）がKVAL_RUN（TVAL_RUN）の半分以上に引き上げられます。`/activate 1`では以前からで、今は`/free`の後も同じです。`/getKval`は引き上げられた値を返します。

**影響を受けるのは。** ブレーキを解放した状態で負荷を支えるモータです。

**何をすればよいか。** 保持電流がモータと負荷に合っているか確かめてください。詳しくは[保持電流](../guides/electromagnetic-brake.md#hold-current)をご覧ください。

### 再起動、ウォッチドッグ、CPU動作異常 {#brake-restart}

**何が変わったか。** ボードは、再起動する前にブレーキを保持状態にします。`/resetDevice`とUSBシリアルの`R`は、回転中のモータを即停止し、ブレーキを保持状態にして、`brakeTransitionDuration`の最大値（最大1s）を待ちます。ボードの処理が止まったことをウォッチドッグが検出する（最後のウォッチドッグのリセットから約250ms後）と、先にすべてのブレーキを保持状態にし、`brakeTransitionDuration`の最大値（最大1s）の後に、`resetCause`4で再起動します。v2.1.0は、処理が止まってから約62.5ms後に再起動しました。CPU動作異常のときは、すべてのブレーキをすぐに保持状態にし、`resetCause`6で再起動します。

**影響を受けるのは。** 再起動が速くなければならない装置や、再起動を監視する装置です。

**何をすればよいか。** 再起動に最大1s長くかかると考えてください。ウォッチドッグ自体は、ブレーキの有無によらず、処理が止まってから約250ms後に働きます（v2.1.0は約62.5ms）。これより長くボードを止めるコマンドは再起動を起こしますが、知られているものはありません。詳しくは[再起動、ウォッチドッグ、CPU動作異常](../guides/electromagnetic-brake.md#restart)をご覧ください。

### 負荷を支えられない時間 {#brake-unsupported}

**何が変わったか。** ファームウェアではこの時間をなくせませんが、v2.2.0は`setup()`で、より早くブレーキ出力を保持状態にします。STEP800では、電源を入れてから約250msの間、すべてのブレーキが解放されたままです（ほとんどはブートローダの時間）。電源によってはさらに長くなり、24Vで約2sの実測があります。リセットや電源電圧の低下の後は、約0.5s解放されたままです。EMB-STEP400を接続したSTEP400は、リセットのときもブレーキがすぐに保持状態になります。それでも、軸が保持されるのは、ブレーキが機械的にロックしてからで、数十msかかります。

**影響を受けるのは。** モータで負荷を吊るす装置、特にSTEP800です。

**何をすればよいか。** ブレーキの電源は、モータと同じ電源から取るか、モータの電源と一緒に切れる電源にしてください。モータの電源だけが先に切れる状態は避けてください。再起動の後と、モータが無励磁になった後は、原点復帰をやり直してください。詳しくは[負荷を支えられない時間](../guides/electromagnetic-brake.md#unsupported)と[使い方の注意](../guides/electromagnetic-brake.md#usage)をご覧ください。

## ファームウェアを自分でビルドしている場合 {#building}

### ボードの選び方 {#board-select}

**何が変わったか。** v2.1.0までは、`src/boardsDef.h`の1行のコメントを外してボードを選んでいました。v2.2.0のPlatformIOでは、`platformio.ini`の環境（`step400`、`step800`、`step100`、`step200`）で選びます。Arduino IDEは今も`boardsDef.h`を使います。

**影響を受けるのは。** PlatformIOでビルドするすべての人です。

**何をすればよいか。** `boardsDef.h`のボードの行は、すべてコメントのままにしてください。両方でボードを指定しないでください。環境は、`pio run -e step800 -t upload`か、`platformio.ini`の`default_envs`で選びます。以前の環境`zeroUSB`は残っていて、STEP400をビルドします。詳しくは[ボードの選び方](compile-the-arduino-sketch.md#select-board)をご覧ください。

### ライブラリ {#libraries}

**何が変わったか。** ファームウェアには、ドライバライブラリの**1.2.0以上**（Ponoor PowerSTEP01 Library、Ponoor L6470 Library）が必要です。v2.1.0以前は1.1.xを使います。Ethernet 2.0.2以上、SdFat 2.2.3以上（v2.1.0と同じ）、ArduinoJson 7.4.1以上（7.x）も必要です。CNMAT OSCライブラリとAdafruit SleepyDogライブラリは、不要になりました。PlatformIO RegistryのL6470 Libraryは今も1.0.0なので、ドライバライブラリをRegistryから入れないでください。

**影響を受けるのは。** ファームウェアをビルドするすべての人で、主にArduino IDEを使う人です。

**何をすればよいか。** ライブラリマネージャでドライバライブラリを更新し（PlatformIOはGitHubのv1.2.0のタグから取得します）、使わなくなった2つのライブラリを外してください。詳しくは[ライブラリ](compile-the-arduino-sketch.md#libraries)をご覧ください。

## v2.0.0からの更新 {#from-v2-0-0}

v2.1.0で加わったものは次のとおりです。読んだうえで、このページの各項目を確かめてください。

- **設定ファイル**: v2.0.0のものと互換です。古いテンプレートから作ったSTEP400のファイルには、綴りの誤ったキー`goUnitlTimeout`が入っていることがあります。v2.0.0はその値を無視し、v2.1.0以降は使います。[`goUnitlTimeout`](#go-until-timeout)をご覧ください。
- **microSDカード**: ファームウェアは先に`config.txt`を読み、次にアルファベット順で最初の`.json`ファイルを読みます。長いファイル名が使えます。`/saveConfig`とブラウザ設定ツールは、動作中の設定をカードに保存します。[microSDカードでの設定](../connections/microsd-card.md)をご覧ください。
- **新しいメッセージ**: `/setConfigName`、`/saveConfig`、`/getConfigName`の返信の5番目の引数`configFilename`です。`/configName`の引数の数を厳密に確かめるクライアントは、5つを受け付けるようにしてください。
- **ビルド**: SDライブラリはSdFatです。Arduino IDE用のスケッチのフォルダはリポジトリから削除され、各リリースのアセットの`step-series-universal-firmware.zip`がArduino IDE用のスケッチです。[ファームウェアを自分でビルドしている場合](#building)をご覧ください。

## v2.1.0に戻す {#downgrade}

v2.2.0からv2.1.0に戻すには、v2.1.0をドライバライブラリ**1.1.x**でビルドして書き込みます。ライブラリ1.2.0はv2.2.0用です。PlatformIOやライブラリマネージャが1.1.xを入れることを確かめてください。v2.1.0の`platformio.ini`の`^1.1.0`は、より新しいバージョンに解決されることがあります（[ライブラリ](#libraries)をご覧ください）。

- **設定ファイル**: v2.2.0が保存した設定は、v2.1.0と同じキーと同じ適用可能な設定のバージョンを持つので、v2.1.0で読めます。Rawの設定は、通常の設定と同じキーに保存されます。
- **`.tmp`ファイル**: 保存の失敗で残った`.tmp`ファイルは、v2.1.0でも設定ファイルの候補にはなりません。
- **隠しファイル**（`._name.json`）: Macでコピーしたカードの隠しファイルは、v2.1.0では再び候補になり、有効な`.json`ファイルを見えなくすることがあります。削除するか、`config.txt`を使ってください。また、v2.1.0の無効なファイルの扱い（[無効なファイルは適用されません](#invalid-files)）に戻ること、v2.1.0のArduino IDEのビルドではexFATのカードを使えないこと（ファイルが削除されることがあります）にも注意してください。
- **クライアント**: v2.2.0向けに書いたクライアントは、[変更履歴](changelog.md#v2-2-0)と照らして確かめてください。v2.1.0は、`resetCause`のない`/booted`を送り、`/uvlo`と`/lowSpeedOptimizeThreshold`で`T`/`F`を送り、足りない引数を0として適用します。
- **電磁ブレーキ**: v2.1.0では、コマンドと再起動の動作はv2.2.0より前のとおりです。[コマンドと状態](#brake-commands)と[再起動、ウォッチドッグ、CPU動作異常](#brake-restart)をご覧ください。
