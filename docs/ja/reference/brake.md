---
title: 電磁ブレーキ
---

# 電磁ブレーキ

電磁ブレーキの仕組みは、[電磁ブレーキ](../guides/electromagnetic-brake.md)をご覧ください。

<!-- osc: /enableElectromagnetBrake -->
<!-- generated:begin osc /enableElectromagnetBrake -->
### `/enableElectromagnetBrake` (int)motorID (bool)enable {#enableelectromagnetbrake}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| enable | bool |  |  |

`enable`

| 値 | 意味 |
| --- | --- |
| 1 | 有効 |
| 0 | 無効 |

#### 実行可能タイミング

常時

#### 説明

電磁ブレーキモードを有効・無効にします。  
電磁ブレーキモードが有効になると、電磁ブレーキを解放しないままモータを回すコマンドを送っても`BrakeEngaged`（[`/error/command`](automatically-sent-messages.md#error-command)）エラーになります。

#### 変更

- **v2.2.0**: ドライバが無励磁のときだけ設定を変更し、ブレーキを無効にできるのは、ブレーキが保持されている間か`/free`の後だけです。それ以外では`/error/command CommandIgnored`を返します。現在の値を送っても何も起きません。変更後は、ブレーキ出力が保持され、状態も保持になります。以前は、解放中のブレーキを無効にすると、回転中のモータでブレーキが保持され、励磁中のモータで有効にすると、`/activate 0`と`/hardHiZ`が何もしない状態になっていました。

#### エラー

- `CommandIgnored`: コマンドが実行可能なタイミングではない。タイミング参照。値がコマンドの範囲外のときにも送信され、何も適用されない（`/setPositionListReportInterval`のモータIDは255）。

#### 初期値

- `enable`: false（無効）（[driverSettings.electromagnetBrakeEnable](../connections/configuration-items.md#driversettings-electromagnetbrakeenable)）

#### 関連

[`/activate`](brake.md#activate), [`/free`](brake.md#free), [`/setBrakeTransitionDuration`](brake.md#setbraketransitionduration), [`/getBrakeStatus`](brake.md#getbrakestatus)
<!-- generated:end osc /enableElectromagnetBrake -->

<!-- osc: /activate -->
<!-- generated:begin osc /activate -->
### `/activate` (int)motorID (bool)state {#activate}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| state | bool |  |  |

`state`

| 値 | 意味 |
| --- | --- |
| 1 | モータ励磁, 電磁ブレーキ解放 |
| 0 | モータ励磁解除, 電磁ブレーキ保持 |

#### 実行可能タイミング

常時

#### 説明

電磁ブレーキモードの場合に、モータの励磁、励磁解除を切り替えます。電磁ブレーキも連動して動作します。このコマンドでモータが励磁状態になっていないと、モータを回転させるコマンドを送ることはできません。

電磁ブレーキモードが無効の場合は拒否されます。`CommandIgnored`だけが送信され、保留中の動作は取り消されません。

ブレーキが解放されているときの`/activate 1`は、何もしません。ブレーキが保持されている状態からは、ドライバを励磁し、`brakeTransitionDuration`の後にブレーキを解放しますが、コマンドの後のSTATUSレジスタの読み出しでドライバが励磁されていることを確認できたときだけです（保持への移行中は解放の手順に戻り（移行時間は最初からやり直しです）、停止処理中は保持の取り消しだけを行い、[`/free`](brake.md#free)の後はすぐに解放します）。ドライバが無励磁のまま（たとえばモータ電源がない）のときは、ブレーキは保持されたままになり、`BrakeReleaseFailed`が送信されます。

回転中のモータへの`/activate 0`は、[`/softHiZ`](motor-control.md#softhiz)と同じように減速し、停止してからブレーキを保持します。停止中のモータでは、次のSTATUSレジスタの読み出し（最大5ms後）でブレーキを保持します。`brakeTransitionDuration`の後にドライバが無励磁になります。ブレーキの状態は[`/getBrakeStatus`](brake.md#getbrakestatus)で読み出せます。

#### 変更

- **v2.2.0**: ブレーキが解放されているときの`/activate 1`は、何もしません。以前は即停止を送り、回転中のモータを急停止させていました。
- **v2.2.0**: `/activate 1`は、コマンドの後のSTATUSレジスタの読み出しでドライバが励磁されていることを確認できたときだけ、ブレーキを解放します。ドライバが無励磁のままのとき（たとえばモータ電源がないとき）は、ブレーキは保持されたままになり、`/error/command BrakeReleaseFailed motorID`が送信されます。以前は、常に`brakeTransitionDuration`の後にブレーキを解放していました。
- **v2.2.0**: `/softHiZ`（または`/activate 0`）の減速中の`/activate 1`は、ブレーキの保持を取り消し、ブレーキは解放されたままになります。減速は続きます。以前は、即停止でモータを止め、モータが止まるとブレーキが保持されていました。
- **v2.2.0**: 回転中のモータへの`/activate 0`は、`/softHiZ`と同じように、減速してモータが止まってからブレーキを保持します。以前は、モータを止めずにブレーキを保持していました。
- **v2.2.0**: 停止中のモータへの`/activate 0`は、次のSTATUSレジスタの読み出し（最大5ms後）でブレーキを保持します。停止の判定は、コマンドの後のSTATUSレジスタの読み出しで行うようになりました。
- **v2.2.0**: `/free`の後: `/activate 1`はモータを解放（励磁）の状態に戻し、`/activate 0`はブレーキをすぐに保持します（モータはすでに無励磁です）。
- **v2.2.0**: モータが再び励磁されるたびに、KVAL_HOLD（電流モードではTVAL_HOLD）がKVAL_RUN（TVAL_RUN）の半分以上に引き上げられます。ブレーキが保持中または保持への移行中だった場合は以前と同じで、`/free`の後も引き上げられるようになりました。
- **v2.2.0**: `/activate 0`は、電磁ブレーキが有効なモータの保留中の動作を取り消します（ブレーキが無効なモータには`CommandIgnored`を返し、何も取り消しません）。取り消されるのは、BUSYフラグが下りるのを待っている`/goTo`、`/goToDir`、`/goHome`、`/goMark`（以前は、モータがBUSYでなくなったときに送られていたため、止まっていたモータが再び動き出していました）、原点復帰（以前は、そのタイムアウトで送られる即停止が、その間に無励磁になったモータを励磁していました）、サーボモードが対象です。

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

- `CommandIgnored`: コマンドが実行可能なタイミングではない。タイミング参照。値がコマンドの範囲外のときにも送信され、何も適用されない（`/setPositionListReportInterval`のモータIDは255）。
- `BrakeReleaseFailed`: `/activate 1`を送信したが、ドライバが無励磁のままだった（たとえばモータ電源がない）ため、ブレーキは保持されたままになった。v2.2.0で追加。

#### 関連

[`/enableElectromagnetBrake`](brake.md#enableelectromagnetbrake), [`/free`](brake.md#free), [`/getBrakeStatus`](brake.md#getbrakestatus)
<!-- generated:end osc /activate -->

<!-- osc: /free -->
<!-- generated:begin osc /free -->
### `/free` (int)motorID {#free}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

電磁ブレーキモードの場合に、モータ軸を自由に回せる状態にします。モータの励磁を解除し、電磁ブレーキも解放のままになります。

負荷を吊り下げている場合は、支えがなくなって負荷が落下する原因になりますので、送信時には十分注意してください。

電磁ブレーキモードが無効の場合は拒否されます。`CommandIgnored`だけが送信され、保留中の動作は取り消されません。

`/free`の後は、モータが停止してもブレーキを保持しなくなります（`/softHiZ`の減速中に`/free`を送った場合）。動作コマンド（`/run`、`/move`、`/goTo`など）か`/activate 1`を送ると、モータが再び励磁されて、解放の状態に戻ります。`/activate 0`、`/softHiZ`、`/hardHiZ`は、ブレーキをすぐに保持します。

#### 変更

- **v2.2.0**: `/free`の後は、モータが停止してもブレーキを保持しなくなりました（`/softHiZ`の減速中に`/free`を送った場合）。
- **v2.2.0**: `/free`の後に動作コマンド（`/run`、`/move`、`/goTo`など）を送ると、コマンドが実行され、モータは解放（励磁）の状態に戻ります。`/activate 1`も同じです。`/activate 0`、`/softHiZ`、`/hardHiZ`は、ブレーキをすぐに保持します（モータはすでに無励磁です）。
- **v2.2.0**: `/free`の後でモータが再び励磁されるとき、KVAL_HOLD（電流モードではTVAL_HOLD）がKVAL_RUN（TVAL_RUN）の半分以上に引き上げられます。以前は、設定された停止時の値で励磁されていました。
- **v2.2.0**: `/free`は、電磁ブレーキが有効なモータの保留中の動作を取り消します（ブレーキが無効なモータには`CommandIgnored`を返します）。取り消されるのは、BUSYフラグが下りるのを待っている`/goTo`、`/goToDir`、`/goHome`、`/goMark`（以前は、モータがBUSYでなくなったときに送られていたため、止まっていたモータが再び動き出していました）、原点復帰（以前は、そのタイムアウトで送られる即停止が、その間に無励磁になったモータを励磁していました）、サーボモードが対象です。

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

- `CommandIgnored`: コマンドが実行可能なタイミングではない。タイミング参照。値がコマンドの範囲外のときにも送信され、何も適用されない（`/setPositionListReportInterval`のモータIDは255）。

#### 関連

[`/enableElectromagnetBrake`](brake.md#enableelectromagnetbrake), [`/activate`](brake.md#activate), [`/getBrakeStatus`](brake.md#getbrakestatus)
<!-- generated:end osc /free -->

<!-- osc: /setBrakeTransitionDuration -->
<!-- generated:begin osc /setBrakeTransitionDuration -->
### `/setBrakeTransitionDuration` (int)motorID (int)duration {#setbraketransitionduration}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| duration | int | 0-65535 ms | 移行時間 |

#### 実行可能タイミング

常時

#### 説明

電磁ブレーキの保持・解放時に、モータを励磁したままにしておく移行時間を指定します。これは物理的にブレーキ機構が動作する時間がかかるため、ブレーキの動作が完了するまでモータ軸を励磁したまま保っておくために必要な時間です。

0〜65535の範囲外の値には`CommandIgnored`を返し、設定は変わりません。ブレーキは5msごとに処理されるため、[`/activate`](brake.md#activate)の後の解放は、設定した時間の0〜5ms後になります。

#### 変更

- **v2.2.0**: 0〜65535の範囲外の値には`/error/command CommandIgnored`を返し、設定は変わりません。以前は、値が16ビットの符号なし整数として扱われ、下位16ビットだけが使われていました（65536は0、-1は65535になっていました）。
- **v2.2.0**: ブレーキの時間は5ms単位です。`/activate 1`の後の解放は、`brakeTransitionDuration`の0〜5ms後になります（100msの設定で実測99.8〜105.4ms。以前は99.8〜107.6ms）。停止や無励磁の後のブレーキの保持は、次のSTATUSレジスタの読み出しで判定されます。

#### エラー

- `CommandIgnored`: コマンドが実行可能なタイミングではない。タイミング参照。値がコマンドの範囲外のときにも送信され、何も適用されない（`/setPositionListReportInterval`のモータIDは255）。

#### 初期値

- `duration`: 100（[driverSettings.brakeTransitionDuration](../connections/configuration-items.md#driversettings-braketransitionduration)）

#### 関連

[`/getBrakeTransitionDuration`](brake.md#getbraketransitionduration)
<!-- generated:end osc /setBrakeTransitionDuration -->

<!-- osc: /getBrakeTransitionDuration -->
<!-- generated:begin osc /getBrakeTransitionDuration -->
### `/getBrakeTransitionDuration` (int)motorID {#getbraketransitionduration}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

電磁ブレーキの保持・解放時に、モータを励磁したままにしておく移行時間を取得します。

#### 返信

```
/brakeTransitionDuration (int)motorID (int)duration
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| duration | int | 0-65535 ms | 移行時間 |
<!-- generated:end osc /getBrakeTransitionDuration -->

<!-- osc: /getBrakeStatus -->
<!-- generated:begin osc /getBrakeStatus -->
### `/getBrakeStatus` (int)motorID {#getbrakestatus}

v2.2.0で追加。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

指定したモータの電磁ブレーキの状態を返します。ブレーキが無効なモータでは-1です。

#### 返信

v2.2.0で追加。

```
/brakeStatus (int)motorID (int)state
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| state | int |  | ブレーキの状態 |

`state`

| 値 | 意味 |
| --- | --- |
| -1 | このモータの電磁ブレーキは無効です |
| 0 | 保持。ブレーキ出力: 保持。ドライバ: 無励磁 |
| 1 | 解放中（`/activate 1`、`brakeTransitionDuration`を待っています）。ブレーキ出力: 保持。ドライバ: 励磁 |
| 2 | 解放。ブレーキ出力: 解放。ドライバ: 励磁 |
| 3 | 停止処理中（`/softHiZ`、`/activate 0`: 減速中で、停止すると保持します）。ブレーキ出力: 解放。ドライバ: 励磁 |
| 4 | 保持への移行中（`brakeTransitionDuration`を待ち、その後無励磁にします）。ブレーキ出力: 保持。ドライバ: 励磁 |
| 5 | フリー（`/free`）。ブレーキ出力: 解放。ドライバ: 無励磁 |

##### 説明

`/getBrakeStatus`への返信です。状態の番号は仕様の一部です。新しい状態は6、7、... として追加されます。

#### 関連

[`/activate`](brake.md#activate), [`/free`](brake.md#free), [`/enableElectromagnetBrake`](brake.md#enableelectromagnetbrake)
<!-- generated:end osc /getBrakeStatus -->
