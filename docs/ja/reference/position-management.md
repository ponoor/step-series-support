---
title: 位置管理
---

# 位置管理

位置管理の仕組みは、[原点復帰と位置管理](../guides/homing-and-position.md)をご覧ください。

## 座標

<!-- osc: /setPosition -->
<!-- generated:begin osc /setPosition -->
### `/setPosition` (int)motorID (int)newPosition {#setposition}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| newPosition | int | -2097152-2097151 | 指定座標 |

#### 実行可能タイミング

モータ停止時

#### 説明

ABS_POSレジスタを指定座標に書き換えます。現在のモータ位置が指定座標になります。

モータの回転中やサーボモード中には使わないでください。ガードはありません。ドライバが書き込みを拒否した場合は`CommandIgnored`が送信されます。

範囲外の値は拒否されません。ドライバが22ビットに切り捨てます。

#### エラー

- `CommandIgnored`: コマンドが実行可能なタイミングではない。タイミング参照。値がコマンドの範囲外のときにも送信され、何も適用されない（`/setPositionListReportInterval`のモータIDは255）。

#### 関連

[`/getPosition`](position-management.md#getposition), [`/resetPos`](position-management.md#resetpos)
<!-- generated:end osc /setPosition -->

<!-- osc: /getPosition -->
<!-- generated:begin osc /getPosition -->
### `/getPosition` (int)motorID {#getposition}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

ABS_POSレジスタの内容（現在位置）を取得します。

[`/setPositionReportInterval`](motor-driver-settings.md#setpositionreportinterval)コマンドで、指定間隔で自動送信させることもできます。

#### 返信

[`/position`](automatically-sent-messages.md#position)

```
/position (int)motorID (int)ABS_POS
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| ABS_POS | int | -2097152-2097151 | 現在位置 |
<!-- generated:end osc /getPosition -->

<!-- osc: /getPositionList -->
<!-- generated:begin osc /getPositionList -->
### `/getPositionList` {#getpositionlist}

#### 引数

なし

#### 実行可能タイミング

常時

#### 説明

全モータの現在位置（`ABS_POS`）を取得します。`/getPosition 255`を送信した場合は、モータの軸数分の個別のメッセージが返されますが、このコマンドは、すべてのモータの位置をリストにまとめた1個のメッセージが返されます。

[`/setPositionListReportInterval`](motor-driver-settings.md#setpositionlistreportinterval)コマンドで、指定間隔で自動送信させることもできます。

#### 返信

[`/positionList`](automatically-sent-messages.md#positionlist)

```
/positionList (int)position1 ... (int)positionN
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| position1 ... positionN | int | -2097152-2097151 | n個目のモータの現在位置 |

#### 関連

[`/getPosition`](position-management.md#getposition)
<!-- generated:end osc /getPositionList -->

<!-- osc: /resetPos -->
<!-- generated:begin osc /resetPos -->
### `/resetPos` (int)motorID {#resetpos}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

ABS_POSレジスタを0にリセットします。

モータの回転中やサーボモード中には使わないでください。ガードはありません。ドライバが書き込みを拒否した場合は`CommandIgnored`が送信されます。

#### エラー

- `CommandIgnored`: コマンドが実行可能なタイミングではない。タイミング参照。値がコマンドの範囲外のときにも送信され、何も適用されない（`/setPositionListReportInterval`のモータIDは255）。

#### 関連

[`/setPosition`](position-management.md#setposition)
<!-- generated:end osc /resetPos -->

<!-- osc: /setElPos -->
<!-- generated:begin osc /setElPos -->
### `/setElPos` (int)motorID (int)newFullstep (int)newMicrostep {#setelpos}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| newFullstep | int | 0-3 | フルステップでの位置 |
| newMicrostep | int | 0-127 | マイクロステップでの位置 |

#### 実行可能タイミング

モータ停止時

#### 説明

モータの電気的位置（electrical position）を設定します。マイクロステップは0〜127の128段階で表現されていますので、設定時は現在のマイクロステップと齟齬のない値を設定する必要があります。

モータが無励磁のときに使ってください。モータの状態に対するガードはありません。L6470は、モータが停止して励磁されているとき（データシートでは書き込める）も書き込みを拒否し、そのときは`CommandIgnored`が送信されます。

0〜3の範囲外のフルステップ、0〜127の範囲外のマイクロステップには`CommandIgnored`を返し、何も適用されません。

#### 変更

- **v2.2.0**: 0〜3の範囲外のフルステップ、0〜127の範囲外のマイクロステップには、`/error/command CommandIgnored`を返し、何も適用されません。以前は範囲内に丸められていました。

#### エラー

- `CommandIgnored`: コマンドが実行可能なタイミングではない。タイミング参照。値がコマンドの範囲外のときにも送信され、何も適用されない（`/setPositionListReportInterval`のモータIDは255）。

#### 関連

[`/getElPos`](position-management.md#getelpos)
<!-- generated:end osc /setElPos -->

<!-- osc: /getElPos -->
<!-- generated:begin osc /getElPos -->
### `/getElPos` (int)motorID {#getelpos}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

モータの電気的位置（electrical position）を取得します。

#### 返信

```
/elPos (int)motorID (int)fullstep (int)microstep
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| fullstep | int | 0-3 | フルステップでの位置 |
| microstep | int | 0-127 | マイクロステップでの位置 |
<!-- generated:end osc /getElPos -->

## HOME/MARK

<!-- osc: /setMark -->
<!-- generated:begin osc /setMark -->
### `/setMark` (int)motorID (int)MARK {#setmark}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| MARK | int |  | 設定する座標 |

#### 実行可能タイミング

常時

#### 説明

markを任意の位置に設定します。

範囲外の値は拒否されません。ドライバが22ビットに切り捨てます。

#### 関連

[`/getMark`](position-management.md#getmark), [`/goMark`](position-management.md#gomark)
<!-- generated:end osc /setMark -->

<!-- osc: /getMark -->
<!-- generated:begin osc /getMark -->
### `/getMark` (int)motorID {#getmark}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

MARKの位置を取得します。

#### 返信

```
/mark (int)motorID (int)MARK
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| MARK | int |  | MARKの座標 |
<!-- generated:end osc /getMark -->

<!-- osc: /goHome -->
<!-- generated:begin osc /goHome -->
### `/goHome` (int)motorID {#gohome}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

動作開始条件時

#### 説明

HOME位置までスピードプロファイルに従って移動します。

#### 変更

- **v2.2.0**: HOMEスイッチまたはLIMITスイッチが動作を禁止する場合（[`/setProhibitMotionOnHomeSw`](alarm-settings.md#setprohibitmotiononhomesw)、[`/setProhibitMotionOnLimitSw`](alarm-settings.md#setprohibitmotiononlimitsw)）の方向を、正しく判定します。目標との22ビットの差の符号で決まり、ドライバが進む向き（最短経路）と同じです。以前は、目標が2048ステップ未満の距離にあると方向が逆になり（スイッチから離れる短い移動が`HomeSwActivating` / `LimitSwActivating`で拒否され、スイッチに向かう短い移動が開始されていました）、2^21ステップを超えるとまた誤っていました。
- **v2.2.0**: BUSYのモータでは、ラッチされたフラグを消さないGetParamでSTATUSレジスタを読みます。以前はGetStatusで読んでいたため、STATUSレジスタの読み出しがフラグを見逃し、通知（`/overCurrent`、`/stall`、`/swEvent`、`/uvlo`など）が失われることがありました。

#### エラー

- `BrakeEngaged`: 電磁ブレーキが効いた状態のままモーションコマンドを送信した。ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`と`/homing`でも送信される（停止処理中と`/free`の後は除く）。
- `HomeSwActivating`: HOMEスイッチがオンの状態から原点復帰方向に移動しようとした。HOMEスイッチがすでにオンのときの`/goUntil`と`/goUntilRaw`でも送信される。**v2.2.0**: `/goUntil`と`/goUntilRaw`が、HOMEスイッチがすでにオンのときに送信します。以前は`HomeSwActivated`として送信されていました。
- `LimitSwActivating`: LIMITスイッチがオンの状態から原点復帰方向の逆向きに移動しようとした。
- `InServoMode`: サーボモードでは実行できないコマンドを送信した。**v2.2.0**: `/goUntil`、`/goUntilRaw`、`/releaseSw`でも送信されます。
<!-- generated:end osc /goHome -->

<!-- osc: /goMark -->
<!-- generated:begin osc /goMark -->
### `/goMark` (int)motorID {#gomark}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

動作開始条件時

#### 説明

MARK位置までスピードプロファイルに従って移動します。

#### 変更

- **v2.2.0**: HOMEスイッチまたはLIMITスイッチが動作を禁止する場合（[`/setProhibitMotionOnHomeSw`](alarm-settings.md#setprohibitmotiononhomesw)、[`/setProhibitMotionOnLimitSw`](alarm-settings.md#setprohibitmotiononlimitsw)）の方向を、正しく判定します。目標との22ビットの差の符号で決まり、ドライバが進む向き（最短経路）と同じです。以前は、目標が2048ステップ未満の距離にあると方向が逆になり（スイッチから離れる短い移動が`HomeSwActivating` / `LimitSwActivating`で拒否され、スイッチに向かう短い移動が開始されていました）、2^21ステップを超えるとまた誤っていました。
- **v2.2.0**: BUSYのモータでは、ラッチされたフラグを消さないGetParamでSTATUSレジスタを読みます。以前はGetStatusで読んでいたため、STATUSレジスタの読み出しがフラグを見逃し、通知（`/overCurrent`、`/stall`、`/swEvent`、`/uvlo`など）が失われることがありました。

#### エラー

- `BrakeEngaged`: 電磁ブレーキが効いた状態のままモーションコマンドを送信した。ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`と`/homing`でも送信される（停止処理中と`/free`の後は除く）。
- `HomeSwActivating`: HOMEスイッチがオンの状態から原点復帰方向に移動しようとした。HOMEスイッチがすでにオンのときの`/goUntil`と`/goUntilRaw`でも送信される。**v2.2.0**: `/goUntil`と`/goUntilRaw`が、HOMEスイッチがすでにオンのときに送信します。以前は`HomeSwActivated`として送信されていました。
- `LimitSwActivating`: LIMITスイッチがオンの状態から原点復帰方向の逆向きに移動しようとした。
- `InServoMode`: サーボモードでは実行できないコマンドを送信した。**v2.2.0**: `/goUntil`、`/goUntilRaw`、`/releaseSw`でも送信されます。

#### 関連

[`/setMark`](position-management.md#setmark)
<!-- generated:end osc /goMark -->
