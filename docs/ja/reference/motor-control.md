---
title: モータの回転・停止
---

# モータの回転・停止

動作の仕組みは、[スピードプロファイルと動作](../guides/speed-profile-and-motions.md)をご覧ください。

## モータの回転

<!-- osc: /run -->
<!-- generated:begin osc /run -->
### `/run` (int)motorID (float)speed {#run}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| speed | float | -15625-15625 step/s | 回転速度 |

#### 実行可能タイミング

動作開始条件時

#### 説明

モータを指定速度で回転させます。事前に設定したスピードプロファイルの加速度に従って加速します。指定する回転速度は、maxSpeedを超えるとmaxSpeedでリミットされます。指定速度に到達するまではBUSY状態になります。

速度の符号が方向になります。絶対値が範囲を超える速度は、ドライバライブラリによってレジスタの最大値（0xFFFFF、約15625step/s）に制限されます。

#### 返信

条件: 原点復帰動作中のとき

[`/homingStatus`](automatically-sent-messages.md#homingstatus)

```
/homingStatus (int)motorID (int)homingStatus
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| homingStatus | int | 0-4 | 原点復帰の状態 |

#### エラー

- `BrakeEngaged`: 電磁ブレーキが効いた状態のままモーションコマンドを送信した。ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`と`/homing`でも送信される（停止処理中と`/free`の後は除く）。
- `HomeSwActivating`: HOMEスイッチがオンの状態から原点復帰方向に移動しようとした。HOMEスイッチがすでにオンのときの`/goUntil`と`/goUntilRaw`でも送信される。**v2.2.0**: `/goUntil`と`/goUntilRaw`が、HOMEスイッチがすでにオンのときに送信します。以前は`HomeSwActivated`として送信されていました。
- `LimitSwActivating`: LIMITスイッチがオンの状態から原点復帰方向の逆向きに移動しようとした。
- `InServoMode`: サーボモードでは実行できないコマンドを送信した。**v2.2.0**: `/goUntil`、`/goUntilRaw`、`/releaseSw`でも送信されます。

#### 関連

[`/runRaw`](motor-control.md#runraw), [`/combine/run`](motor-control.md#combine-run)
<!-- generated:end osc /run -->

<!-- osc: /move -->
<!-- generated:begin osc /move -->
### `/move` (int)motorID (int)step {#move}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| step | int |  | 移動ステップ数 |

#### 実行可能タイミング

モータ停止時, 動作開始条件時

#### 説明

事前に設定したスピードプロファイルに従って、指定ステップ数移動します。指定ステップ数を移動し終わるまではBUSY状態になります。このコマンドはモータが停止していないと実行できません。

絶対値が4,194,303（22ビット）を超えるステップ数は拒否されず、ドライバライブラリによって4,194,303に制限されます。

#### エラー

- `BrakeEngaged`: 電磁ブレーキが効いた状態のままモーションコマンドを送信した。ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`と`/homing`でも送信される（停止処理中と`/free`の後は除く）。
- `HomeSwActivating`: HOMEスイッチがオンの状態から原点復帰方向に移動しようとした。HOMEスイッチがすでにオンのときの`/goUntil`と`/goUntilRaw`でも送信される。**v2.2.0**: `/goUntil`と`/goUntilRaw`が、HOMEスイッチがすでにオンのときに送信します。以前は`HomeSwActivated`として送信されていました。
- `LimitSwActivating`: LIMITスイッチがオンの状態から原点復帰方向の逆向きに移動しようとした。
- `InServoMode`: サーボモードでは実行できないコマンドを送信した。**v2.2.0**: `/goUntil`、`/goUntilRaw`、`/releaseSw`でも送信されます。

#### 関連

[`/combine/move`](motor-control.md#combine-move)
<!-- generated:end osc /move -->

<!-- osc: /goTo -->
<!-- generated:begin osc /goTo -->
### `/goTo` (int)motorID (int)position {#goto}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| position | int | -2097152-2097151 | 目標位置 |

#### 実行可能タイミング

動作開始条件時

#### 説明

事前に設定したスピードプロファイルに従って、指定位置まで最短経路で移動します。指定位置まで移動し終わるまではBUSY状態になります。

※ドライバ内部では-2,097,152と2,097,151は1周して隣り合った位置になっています。

範囲外の位置は拒否されません。4,194,303を超える位置は、ドライバライブラリによって4,194,303に制限され、ドライバはこれを-1として読みます。それ以外の位置は、下位22ビットだけが使われ、符号付きの数として読まれます。2,097,152は-2,097,152に、-2,097,153は2,097,151になります。

#### 変更

- **v2.2.0**: HOMEスイッチまたはLIMITスイッチが動作を禁止する場合（[`/setProhibitMotionOnHomeSw`](alarm-settings.md#setprohibitmotiononhomesw)、[`/setProhibitMotionOnLimitSw`](alarm-settings.md#setprohibitmotiononlimitsw)）の方向を、正しく判定します。目標との22ビットの差の符号で決まり、ドライバが進む向き（最短経路）と同じです。以前は、目標が2048ステップ未満の距離にあると方向が逆になり（スイッチから離れる短い移動が`HomeSwActivating` / `LimitSwActivating`で拒否され、スイッチに向かう短い移動が開始されていました）、2^21ステップを超えるとまた誤っていました。
- **v2.2.0**: BUSYのモータでは、ラッチされたフラグを消さないGetParamでSTATUSレジスタを読みます。以前はGetStatusで読んでいたため、STATUSレジスタの読み出しがフラグを見逃し、通知（`/overCurrent`、`/stall`、`/swEvent`、`/uvlo`など）が失われることがありました。

#### 返信

条件: 原点復帰動作中のとき

[`/homingStatus`](automatically-sent-messages.md#homingstatus)

```
/homingStatus (int)motorID (int)homingStatus
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| homingStatus | int | 0-4 | 原点復帰の状態 |

#### エラー

- `BrakeEngaged`: 電磁ブレーキが効いた状態のままモーションコマンドを送信した。ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`と`/homing`でも送信される（停止処理中と`/free`の後は除く）。
- `HomeSwActivating`: HOMEスイッチがオンの状態から原点復帰方向に移動しようとした。HOMEスイッチがすでにオンのときの`/goUntil`と`/goUntilRaw`でも送信される。**v2.2.0**: `/goUntil`と`/goUntilRaw`が、HOMEスイッチがすでにオンのときに送信します。以前は`HomeSwActivated`として送信されていました。
- `LimitSwActivating`: LIMITスイッチがオンの状態から原点復帰方向の逆向きに移動しようとした。
- `InServoMode`: サーボモードでは実行できないコマンドを送信した。**v2.2.0**: `/goUntil`、`/goUntilRaw`、`/releaseSw`でも送信されます。

#### 関連

[`/goToDir`](motor-control.md#gotodir), [`/combine/goTo`](motor-control.md#combine-goto)
<!-- generated:end osc /goTo -->

<!-- osc: /goToDir -->
<!-- generated:begin osc /goToDir -->
### `/goToDir` (int)motorID (bool)DIR (int)position {#gotodir}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| DIR | bool |  | 回転方向 |
| position | int | -2097152-2097151 | 目標位置 |

#### 実行可能タイミング

動作開始条件時

#### 説明

事前に設定したスピードプロファイルに従って、指定位置まで指定方向で移動します。指定位置まで移動し終わるまではBUSY状態になります。

範囲外の位置は拒否されません。4,194,303を超える位置は、ドライバライブラリによって4,194,303に制限され、ドライバはこれを-1として読みます。それ以外の位置は、下位22ビットだけが使われ、符号付きの数として読まれます。2,097,152は-2,097,152に、-2,097,153は2,097,151になります。

#### 変更

- **v2.2.0**: BUSYのモータでは、ラッチされたフラグを消さないGetParamでSTATUSレジスタを読みます。以前はGetStatusで読んでいたため、STATUSレジスタの読み出しがフラグを見逃し、通知（`/overCurrent`、`/stall`、`/swEvent`、`/uvlo`など）が失われることがありました。

#### エラー

- `BrakeEngaged`: 電磁ブレーキが効いた状態のままモーションコマンドを送信した。ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`と`/homing`でも送信される（停止処理中と`/free`の後は除く）。
- `HomeSwActivating`: HOMEスイッチがオンの状態から原点復帰方向に移動しようとした。HOMEスイッチがすでにオンのときの`/goUntil`と`/goUntilRaw`でも送信される。**v2.2.0**: `/goUntil`と`/goUntilRaw`が、HOMEスイッチがすでにオンのときに送信します。以前は`HomeSwActivated`として送信されていました。
- `LimitSwActivating`: LIMITスイッチがオンの状態から原点復帰方向の逆向きに移動しようとした。
- `InServoMode`: サーボモードでは実行できないコマンドを送信した。**v2.2.0**: `/goUntil`、`/goUntilRaw`、`/releaseSw`でも送信されます。

#### 関連

[`/goTo`](motor-control.md#goto), [`/combine/goToDir`](motor-control.md#combine-gotodir)
<!-- generated:end osc /goToDir -->

## モータの停止

<!-- osc: /softStop -->
<!-- generated:begin osc /softStop -->
### `/softStop` (int)motorID {#softstop}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

スピードプロファイルに従って減速したのち、モータを励磁したまま停止します。モータが停止するまではBUSY状態になります。もともと無励磁状態だった場合は、停止したままモータが励磁します。

サーボモードだった場合は解除されます。

電磁ブレーキが有効なとき、ブレーキが保持されている間と[`/free`](brake.md#free)の後（モータが無励磁）は、何もしません。[`/softHiZ`](motor-control.md#softhiz)または`/activate 0`の減速中（ブレーキの状態3）は、コマンドが実行され、ブレーキの保持を取り消します。ブレーキは解放されたままになります（状態2）。

#### 変更

- **v2.2.0**: 電磁ブレーキが有効なとき、ブレーキが保持されている間と`/free`の後（モータが無励磁）は、何もしません。以前は、モータを励磁してブレーキの状態は保持のままにしていたため、`/activate 0`と`/hardHiZ`でモータを再び無励磁にできませんでした。
- **v2.2.0**: 保留中の動作を取り消します。ブレーキが無効なモータでも同じです。取り消されるのは、BUSYフラグが下りるのを待っている`/goTo`、`/goToDir`、`/goHome`、`/goMark`（以前は、モータがBUSYでなくなったときに送られていたため、止まっていたモータが再び動き出していました）、原点復帰（以前は、そのタイムアウトで送られる即停止が、その間に無励磁になったモータを励磁していました）、サーボモードです。

#### 返信

条件: 原点復帰動作中のとき

[`/homingStatus`](automatically-sent-messages.md#homingstatus)

```
/homingStatus (int)motorID (int)homingStatus
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| homingStatus | int | 0-4 | 原点復帰の状態 |

#### 関連

[`/combine/softStop`](motor-control.md#combine-softstop)
<!-- generated:end osc /softStop -->

<!-- osc: /hardStop -->
<!-- generated:begin osc /hardStop -->
### `/hardStop` (int)motorID {#hardstop}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

モータを即停止し、励磁したままにします。モータが停止するまではBUSY状態になります。もともと無励磁状態だった場合は、停止したままモータが励磁します。

サーボモードだった場合は解除されます。

電磁ブレーキが有効なとき、ブレーキが保持されている間と[`/free`](brake.md#free)の後（モータが無励磁）は、何もしません。[`/softHiZ`](motor-control.md#softhiz)または`/activate 0`の減速中（ブレーキの状態3）は、コマンドが実行され、ブレーキの保持を取り消します。ブレーキは解放されたままになります（状態2）。

#### 変更

- **v2.2.0**: 電磁ブレーキが有効なとき、ブレーキが保持されている間と`/free`の後（モータが無励磁）は、何もしません。以前は、モータを励磁してブレーキの状態は保持のままにしていたため、`/activate 0`と`/hardHiZ`でモータを再び無励磁にできませんでした。
- **v2.2.0**: 保留中の動作を取り消します。ブレーキが無効なモータでも同じです。取り消されるのは、BUSYフラグが下りるのを待っている`/goTo`、`/goToDir`、`/goHome`、`/goMark`（以前は、モータがBUSYでなくなったときに送られていたため、止まっていたモータが再び動き出していました）、原点復帰（以前は、そのタイムアウトで送られる即停止が、その間に無励磁になったモータを励磁していました）、サーボモードです。

#### 返信

条件: 原点復帰動作中のとき

[`/homingStatus`](automatically-sent-messages.md#homingstatus)

```
/homingStatus (int)motorID (int)homingStatus
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| homingStatus | int | 0-4 | 原点復帰の状態 |

#### 関連

[`/combine/hardStop`](motor-control.md#combine-hardstop)
<!-- generated:end osc /hardStop -->

<!-- osc: /softHiZ -->
<!-- generated:begin osc /softHiZ -->
### `/softHiZ` (int)motorID {#softhiz}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

スピードプロファイルに従って減速停止してから、モータを無励磁にします。モータが停止するまではBUSY状態になります。

サーボモードだった場合は解除されます。

電磁ブレーキモードが有効になっている場合は、電磁ブレーキを保持状態にしてから無励磁状態に移行します。

#### 変更

- **v2.2.0**: 電磁ブレーキが有効で、モータが停止しているときは、次のSTATUSレジスタの読み出し（最大5ms後）でブレーキを保持します。停止の判定は、コマンドの後のSTATUSレジスタの読み出しで行います。
- **v2.2.0**: 減速中に動作コマンド（`/run`、`/move`、`/goTo`など）か`/activate 1`を受け取ると、ブレーキの保持を取り消し、ブレーキは解放されたままになります。以前は、モータがその後止まったときにブレーキが保持されていました。
- **v2.2.0**: `/free`の後は、ブレーキをすぐに保持します（モータはすでに無励磁です）。
- **v2.2.0**: 保留中の動作を取り消します。ブレーキが無効なモータでも同じです。取り消されるのは、BUSYフラグが下りるのを待っている`/goTo`、`/goToDir`、`/goHome`、`/goMark`（以前は、モータがBUSYでなくなったときに送られていたため、止まっていたモータが再び動き出していました）、原点復帰（以前は、そのタイムアウトで送られる即停止が、その間に無励磁になったモータを励磁していました）、サーボモードです。

#### 返信

条件: 原点復帰動作中のとき

[`/homingStatus`](automatically-sent-messages.md#homingstatus)

```
/homingStatus (int)motorID (int)homingStatus
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| homingStatus | int | 0-4 | 原点復帰の状態 |

#### 関連

[`/combine/softHiZ`](motor-control.md#combine-softhiz), [`/enableElectromagnetBrake`](brake.md#enableelectromagnetbrake)
<!-- generated:end osc /softHiZ -->

<!-- osc: /hardHiZ -->
<!-- generated:begin osc /hardHiZ -->
### `/hardHiZ` (int)motorID {#hardhiz}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

モータを即座に無励磁にします。モータが停止するまではBUSY状態になります。

サーボモードだった場合は解除されます。

電磁ブレーキモードが有効になっている場合は、電磁ブレーキを保持状態にしてから無励磁状態に移行します。

#### 変更

- **v2.2.0**: 1つのモータでも、`/hardHiZ`の前に減速停止を送らなくなりました。1つのモータ、全モータ（255）、`/combine/hardHiZ`は同じ動作です。電磁ブレーキが有効で解放されている（`/activate 1`の後の）ときは、ブレーキを保持する前に、即停止でモータを止めます（励磁されたまま）。ブレーキの移行時間の間にモータが回り続けることはありません。ブレーキが保持されている間と保持への移行中は、以前と同じく何もしません。
- **v2.2.0**: `/free`の後は、ブレーキをすぐに保持します（モータはすでに無励磁です）。
- **v2.2.0**: 保留中の動作を取り消します。ブレーキが無効なモータでも同じです。取り消されるのは、BUSYフラグが下りるのを待っている`/goTo`、`/goToDir`、`/goHome`、`/goMark`（以前は、モータがBUSYでなくなったときに送られていたため、止まっていたモータが再び動き出していました）、原点復帰（以前は、そのタイムアウトで送られる即停止が、その間に無励磁になったモータを励磁していました）、サーボモードです。

#### 返信

条件: 原点復帰動作中のとき

[`/homingStatus`](automatically-sent-messages.md#homingstatus)

```
/homingStatus (int)motorID (int)homingStatus
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| homingStatus | int | 0-4 | 原点復帰の状態 |

#### 関連

[`/combine/hardHiZ`](motor-control.md#combine-hardhiz), [`/enableElectromagnetBrake`](brake.md#enableelectromagnetbrake)
<!-- generated:end osc /hardHiZ -->

## 複合コマンド

<!-- osc: /combine/run -->
<!-- generated:begin osc /combine/run -->
### `/combine/run` (int)motorID1 (int)motorID2 (float)speed {#combine-run}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID1 | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| motorID2 | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| speed | float | -15625-15625 step/s | 回転速度 |

#### 実行可能タイミング

動作開始条件時

#### 説明

2つのモータに対する[`/run`](motor-control.md#run)と同じです。速度の符号が方向になります。絶対値が範囲を超える速度は、ドライバライブラリによってレジスタの最大値（0xFFFFF、約15625step/s）に制限されます。

#### 返信

条件: 原点復帰動作中のとき

[`/homingStatus`](automatically-sent-messages.md#homingstatus)

```
/homingStatus (int)motorID (int)homingStatus
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| homingStatus | int | 0-4 | 原点復帰の状態 |

#### エラー

- `BrakeEngaged`: 電磁ブレーキが効いた状態のままモーションコマンドを送信した。ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`と`/homing`でも送信される（停止処理中と`/free`の後は除く）。
- `HomeSwActivating`: HOMEスイッチがオンの状態から原点復帰方向に移動しようとした。HOMEスイッチがすでにオンのときの`/goUntil`と`/goUntilRaw`でも送信される。**v2.2.0**: `/goUntil`と`/goUntilRaw`が、HOMEスイッチがすでにオンのときに送信します。以前は`HomeSwActivated`として送信されていました。
- `LimitSwActivating`: LIMITスイッチがオンの状態から原点復帰方向の逆向きに移動しようとした。
- `InServoMode`: サーボモードでは実行できないコマンドを送信した。**v2.2.0**: `/goUntil`、`/goUntilRaw`、`/releaseSw`でも送信されます。

#### 関連

[`/run`](motor-control.md#run)
<!-- generated:end osc /combine/run -->

<!-- osc: /combine/move -->
<!-- generated:begin osc /combine/move -->
### `/combine/move` (int)motorID1 (int)motorID2 (int)step {#combine-move}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID1 | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| motorID2 | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| step | int |  | 移動ステップ数 |

#### 実行可能タイミング

モータ停止時, 動作開始条件時

#### 説明

2つのモータに対する[`/move`](motor-control.md#move)と同じです。絶対値が4,194,303（22ビット）を超えるステップ数は拒否されず、ドライバライブラリによって4,194,303に制限されます。

#### エラー

- `BrakeEngaged`: 電磁ブレーキが効いた状態のままモーションコマンドを送信した。ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`と`/homing`でも送信される（停止処理中と`/free`の後は除く）。
- `HomeSwActivating`: HOMEスイッチがオンの状態から原点復帰方向に移動しようとした。HOMEスイッチがすでにオンのときの`/goUntil`と`/goUntilRaw`でも送信される。**v2.2.0**: `/goUntil`と`/goUntilRaw`が、HOMEスイッチがすでにオンのときに送信します。以前は`HomeSwActivated`として送信されていました。
- `LimitSwActivating`: LIMITスイッチがオンの状態から原点復帰方向の逆向きに移動しようとした。
- `InServoMode`: サーボモードでは実行できないコマンドを送信した。**v2.2.0**: `/goUntil`、`/goUntilRaw`、`/releaseSw`でも送信されます。

#### 関連

[`/move`](motor-control.md#move)
<!-- generated:end osc /combine/move -->

<!-- osc: /combine/goTo -->
<!-- generated:begin osc /combine/goTo -->
### `/combine/goTo` (int)motorID1 (int)motorID2 (int)position {#combine-goto}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID1 | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| motorID2 | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| position | int | -2097152-2097151 | 目標位置 |

#### 実行可能タイミング

動作開始条件時

#### 説明

2つのモータに対する[`/goTo`](motor-control.md#goto)と同じです。範囲外の位置は拒否されません。4,194,303を超える位置は、ドライバライブラリによって4,194,303に制限され、ドライバはこれを-1として読みます。それ以外の位置は、下位22ビットだけが使われ、符号付きの数として読まれます。2,097,152は-2,097,152に、-2,097,153は2,097,151になります。

#### 変更

- **v2.2.0**: HOMEスイッチまたはLIMITスイッチが動作を禁止する場合（[`/setProhibitMotionOnHomeSw`](alarm-settings.md#setprohibitmotiononhomesw)、[`/setProhibitMotionOnLimitSw`](alarm-settings.md#setprohibitmotiononlimitsw)）の方向を、正しく判定します。目標との22ビットの差の符号で決まり、ドライバが進む向き（最短経路）と同じです。以前は、目標が2048ステップ未満の距離にあると方向が逆になり（スイッチから離れる短い移動が`HomeSwActivating` / `LimitSwActivating`で拒否され、スイッチに向かう短い移動が開始されていました）、2^21ステップを超えるとまた誤っていました。

#### 返信

条件: 原点復帰動作中のとき

[`/homingStatus`](automatically-sent-messages.md#homingstatus)

```
/homingStatus (int)motorID (int)homingStatus
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| homingStatus | int | 0-4 | 原点復帰の状態 |

#### エラー

- `BrakeEngaged`: 電磁ブレーキが効いた状態のままモーションコマンドを送信した。ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`と`/homing`でも送信される（停止処理中と`/free`の後は除く）。
- `HomeSwActivating`: HOMEスイッチがオンの状態から原点復帰方向に移動しようとした。HOMEスイッチがすでにオンのときの`/goUntil`と`/goUntilRaw`でも送信される。**v2.2.0**: `/goUntil`と`/goUntilRaw`が、HOMEスイッチがすでにオンのときに送信します。以前は`HomeSwActivated`として送信されていました。
- `LimitSwActivating`: LIMITスイッチがオンの状態から原点復帰方向の逆向きに移動しようとした。
- `InServoMode`: サーボモードでは実行できないコマンドを送信した。**v2.2.0**: `/goUntil`、`/goUntilRaw`、`/releaseSw`でも送信されます。

#### 関連

[`/goTo`](motor-control.md#goto)
<!-- generated:end osc /combine/goTo -->

<!-- osc: /combine/goToDir -->
<!-- generated:begin osc /combine/goToDir -->
### `/combine/goToDir` (int)motorID1 (int)motorID2 (bool)DIR (int)position {#combine-gotodir}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID1 | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| motorID2 | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| DIR | bool |  | 回転方向 |
| position | int | -2097152-2097151 | 目標位置 |

#### 実行可能タイミング

動作開始条件時

#### 説明

2つのモータに対する[`/goToDir`](motor-control.md#gotodir)と同じです。範囲外の位置は拒否されません。4,194,303を超える位置は、ドライバライブラリによって4,194,303に制限され、ドライバはこれを-1として読みます。それ以外の位置は、下位22ビットだけが使われ、符号付きの数として読まれます。2,097,152は-2,097,152に、-2,097,153は2,097,151になります。

#### エラー

- `BrakeEngaged`: 電磁ブレーキが効いた状態のままモーションコマンドを送信した。ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`と`/homing`でも送信される（停止処理中と`/free`の後は除く）。
- `HomeSwActivating`: HOMEスイッチがオンの状態から原点復帰方向に移動しようとした。HOMEスイッチがすでにオンのときの`/goUntil`と`/goUntilRaw`でも送信される。**v2.2.0**: `/goUntil`と`/goUntilRaw`が、HOMEスイッチがすでにオンのときに送信します。以前は`HomeSwActivated`として送信されていました。
- `LimitSwActivating`: LIMITスイッチがオンの状態から原点復帰方向の逆向きに移動しようとした。
- `InServoMode`: サーボモードでは実行できないコマンドを送信した。**v2.2.0**: `/goUntil`、`/goUntilRaw`、`/releaseSw`でも送信されます。

#### 関連

[`/goToDir`](motor-control.md#gotodir)
<!-- generated:end osc /combine/goToDir -->

<!-- osc: /combine/softStop -->
<!-- generated:begin osc /combine/softStop -->
### `/combine/softStop` (int)motorID1 (int)motorID2 {#combine-softstop}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID1 | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| motorID2 | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

2つのモータに対する[`/softStop`](motor-control.md#softstop)と同じです。motorID1、続いてmotorID2に対して、[`/softStop`](motor-control.md#softstop)として処理されます。

#### 変更

- **v2.2.0**: [`/softStop`](motor-control.md#softstop)と同じように、保留中の動作を取り消します（2つのモータは、それぞれ別の[`/softStop`](motor-control.md#softstop)として処理されます）。ブレーキが無効なモータでも同じです。

#### 返信

条件: 原点復帰動作中のとき

[`/homingStatus`](automatically-sent-messages.md#homingstatus)

```
/homingStatus (int)motorID (int)homingStatus
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| homingStatus | int | 0-4 | 原点復帰の状態 |

#### 関連

[`/softStop`](motor-control.md#softstop)
<!-- generated:end osc /combine/softStop -->

<!-- osc: /combine/hardStop -->
<!-- generated:begin osc /combine/hardStop -->
### `/combine/hardStop` (int)motorID1 (int)motorID2 {#combine-hardstop}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID1 | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| motorID2 | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

2つのモータに対する[`/hardStop`](motor-control.md#hardstop)と同じです。motorID1、続いてmotorID2に対して、[`/hardStop`](motor-control.md#hardstop)として処理されます。

#### 変更

- **v2.2.0**: [`/hardStop`](motor-control.md#hardstop)と同じように、保留中の動作を取り消します（2つのモータは、それぞれ別の[`/hardStop`](motor-control.md#hardstop)として処理されます）。ブレーキが無効なモータでも同じです。

#### 返信

条件: 原点復帰動作中のとき

[`/homingStatus`](automatically-sent-messages.md#homingstatus)

```
/homingStatus (int)motorID (int)homingStatus
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| homingStatus | int | 0-4 | 原点復帰の状態 |

#### 関連

[`/hardStop`](motor-control.md#hardstop)
<!-- generated:end osc /combine/hardStop -->

<!-- osc: /combine/softHiZ -->
<!-- generated:begin osc /combine/softHiZ -->
### `/combine/softHiZ` (int)motorID1 (int)motorID2 {#combine-softhiz}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID1 | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| motorID2 | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

2つのモータに対する[`/softHiZ`](motor-control.md#softhiz)と同じです。motorID1、続いてmotorID2に対して、[`/softHiZ`](motor-control.md#softhiz)として処理されます。

#### 変更

- **v2.2.0**: [`/softHiZ`](motor-control.md#softhiz)と同じように、保留中の動作を取り消します（2つのモータは、それぞれ別の[`/softHiZ`](motor-control.md#softhiz)として処理されます）。ブレーキが無効なモータでも同じです。

#### 返信

条件: 原点復帰動作中のとき

[`/homingStatus`](automatically-sent-messages.md#homingstatus)

```
/homingStatus (int)motorID (int)homingStatus
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| homingStatus | int | 0-4 | 原点復帰の状態 |

#### 関連

[`/softHiZ`](motor-control.md#softhiz)
<!-- generated:end osc /combine/softHiZ -->

<!-- osc: /combine/hardHiZ -->
<!-- generated:begin osc /combine/hardHiZ -->
### `/combine/hardHiZ` (int)motorID1 (int)motorID2 {#combine-hardhiz}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID1 | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| motorID2 | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

2つのモータに対する[`/hardHiZ`](motor-control.md#hardhiz)と同じです。motorID1、続いてmotorID2に対して、[`/hardHiZ`](motor-control.md#hardhiz)として処理されます。

#### 変更

- **v2.2.0**: [`/hardHiZ`](motor-control.md#hardhiz)と同じように、保留中の動作を取り消します（2つのモータは、それぞれ別の[`/hardHiZ`](motor-control.md#hardhiz)として処理されます）。ブレーキが無効なモータでも同じです。

#### 返信

条件: 原点復帰動作中のとき

[`/homingStatus`](automatically-sent-messages.md#homingstatus)

```
/homingStatus (int)motorID (int)homingStatus
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| homingStatus | int | 0-4 | 原点復帰の状態 |

#### 関連

[`/hardHiZ`](motor-control.md#hardhiz)
<!-- generated:end osc /combine/hardHiZ -->

## Rawレジスタ値のコマンド

以下のコマンドは、速度を単位換算せずに、ドライバICのレジスタ値そのままで指定します。

<!-- osc: /runRaw -->
<!-- generated:begin osc /runRaw -->
### `/runRaw` (int)motorID (int)speed {#runraw}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| speed | int |  | 回転速度（Rawレジスタ値、符号付き） |

#### 実行可能タイミング

動作開始条件時

#### 説明

レジスタ値（Raw）で指定した速度で、モータを回転させます。速度の符号が方向になります。

20ビットの範囲を超える速度は、ドライバによって20ビットに制限されます。

#### 返信

条件: 原点復帰動作中のとき

[`/homingStatus`](automatically-sent-messages.md#homingstatus)

```
/homingStatus (int)motorID (int)homingStatus
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| homingStatus | int | 0-4 | 原点復帰の状態 |

#### エラー

- `BrakeEngaged`: 電磁ブレーキが効いた状態のままモーションコマンドを送信した。ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`と`/homing`でも送信される（停止処理中と`/free`の後は除く）。
- `HomeSwActivating`: HOMEスイッチがオンの状態から原点復帰方向に移動しようとした。HOMEスイッチがすでにオンのときの`/goUntil`と`/goUntilRaw`でも送信される。**v2.2.0**: `/goUntil`と`/goUntilRaw`が、HOMEスイッチがすでにオンのときに送信します。以前は`HomeSwActivated`として送信されていました。
- `LimitSwActivating`: LIMITスイッチがオンの状態から原点復帰方向の逆向きに移動しようとした。
- `InServoMode`: サーボモードでは実行できないコマンドを送信した。**v2.2.0**: `/goUntil`、`/goUntilRaw`、`/releaseSw`でも送信されます。

#### 関連

[`/run`](motor-control.md#run), [`/combine/runRaw`](motor-control.md#combine-runraw)
<!-- generated:end osc /runRaw -->

<!-- osc: /goUntilRaw -->
<!-- generated:begin osc /goUntilRaw -->
### `/goUntilRaw` (int)motorID (bool)ACT (int)speed {#gountilraw}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| ACT | bool |  | `/goUntil`と同じ |
| speed | int |  | 速度（Rawレジスタ値、符号付き） |

#### 実行可能タイミング

常時

#### 説明

`/goUntil`と同じですが、速度にレジスタ値（Raw）を使います。速度の符号が方向になります。

速度は、ファームウェアとドライバライブラリによって20ビット（0xFFFFF）に制限されます。`/goUntilRaw 255`（全モータ）は、1つのモータのときと同じように、速度をレジスタ値として解釈します。

#### 変更

- **v2.2.0**: [`/runRaw`](motor-control.md#runraw)と同じように、速度を20ビット（`0xFFFFF`）に制限します。以前は、大きな値がそのまま送られ、ドライバは上位ビットを無視していました。
- **v2.2.0**: `/goUntilRaw 255`（全モータ）は、1つのモータのときと同じように、速度をレジスタ値として解釈します。以前はstep/sとして扱われていました。
- **v2.2.0**: HOMEスイッチがオンの場合は、エラーの一覧にあるとおり`/error/command HomeSwActivating`として送信されます。以前は`HomeSwActivated`として送信されていました。他のコマンドのエラーと同じように、[`/reportError`](system-settings.md#reporterror)に従います。
- **v2.2.0**: サーボモードのモータには`/error/command InServoMode`を返し、何もしません。以前は、コマンドがドライバに送られていました。255のときは、サーボモードのモータだけがエラーを返し、他のモータはコマンドを実行します。

#### エラー

- `BrakeEngaged`: 電磁ブレーキが効いた状態のままモーションコマンドを送信した。ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`と`/homing`でも送信される（停止処理中と`/free`の後は除く）。
- `GoUntilTimeout`: `/goUntil`コマンド実行中にタイムアウトした。
- `HomeSwActivating`: HOMEスイッチがオンの状態から原点復帰方向に移動しようとした。HOMEスイッチがすでにオンのときの`/goUntil`と`/goUntilRaw`でも送信される。**v2.2.0**: `/goUntil`と`/goUntilRaw`が、HOMEスイッチがすでにオンのときに送信します。以前は`HomeSwActivated`として送信されていました。
- `InServoMode`: サーボモードでは実行できないコマンドを送信した。**v2.2.0**: `/goUntil`、`/goUntilRaw`、`/releaseSw`でも送信されます。

#### 関連

[`/goUntil`](homing.md#gountil)
<!-- generated:end osc /goUntilRaw -->

<!-- osc: /combine/runRaw -->
<!-- generated:begin osc /combine/runRaw -->
### `/combine/runRaw` (int)motorID1 (int)motorID2 (int)speed {#combine-runraw}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID1 | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| motorID2 | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| speed | int |  | 回転速度（Rawレジスタ値、符号付き） |

#### 実行可能タイミング

動作開始条件時

#### 説明

20ビットの範囲を超える速度は、ドライバによって20ビットに制限されます。

#### 返信

条件: 原点復帰動作中のとき

[`/homingStatus`](automatically-sent-messages.md#homingstatus)

```
/homingStatus (int)motorID (int)homingStatus
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| homingStatus | int | 0-4 | 原点復帰の状態 |

#### エラー

- `BrakeEngaged`: 電磁ブレーキが効いた状態のままモーションコマンドを送信した。ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`と`/homing`でも送信される（停止処理中と`/free`の後は除く）。
- `HomeSwActivating`: HOMEスイッチがオンの状態から原点復帰方向に移動しようとした。HOMEスイッチがすでにオンのときの`/goUntil`と`/goUntilRaw`でも送信される。**v2.2.0**: `/goUntil`と`/goUntilRaw`が、HOMEスイッチがすでにオンのときに送信します。以前は`HomeSwActivated`として送信されていました。
- `LimitSwActivating`: LIMITスイッチがオンの状態から原点復帰方向の逆向きに移動しようとした。
- `InServoMode`: サーボモードでは実行できないコマンドを送信した。**v2.2.0**: `/goUntil`、`/goUntilRaw`、`/releaseSw`でも送信されます。

#### 関連

[`/runRaw`](motor-control.md#runraw)
<!-- generated:end osc /combine/runRaw -->
