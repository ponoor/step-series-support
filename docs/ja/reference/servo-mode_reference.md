---
title: サーボモード
---

# サーボモード

サーボモードの仕組みは、[サーボモード](../guides/servo-mode.md)をご覧ください。

<!-- osc: /enableServoMode -->
<!-- generated:begin osc /enableServoMode -->
### `/enableServoMode` (int)motorID (bool)enable {#enableservomode}

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

サーボモード（位置追従モード）をオンオフします。急に動き出すことを避けるため、有効になった瞬間の現在位置が目標位置にセットされます。

このモードで動作している間は、`/run`や`/goTo`など他のモータ制御コマンドを送ることはできません。

サーボモードを有効にすると、そのモータのBUSY、モータの状態、方向の通知（[`/enableBusyReport`](motor-driver-settings.md#enablebusyreport)、[`/enableMotorStatusReport`](motor-driver-settings.md#enablemotorstatusreport)、[`/enableDirReport`](motor-driver-settings.md#enabledirreport)）がオフになります。サーボモードを無効にしても、オンには戻りません。必要なら、有効にするコマンドをもう一度送ってください。積分項とPID制御の前回の誤差もリセットされます。サーボモード中に[`/goUntil`](homing.md#gountil)、[`/goUntilRaw`](motor-control.md#gountilraw)、[`/releaseSw`](homing.md#releasesw)、[`/homing`](homing.md#homing)を送ると`InServoMode`を返します。

電磁ブレーキが有効なとき、ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`は`BrakeEngaged`を返し、何もしません（停止処理中と`/free`の後はコマンドが実行されます）。`/enableServoMode 0`は、ブレーキが保持されている間と[`/free`](brake.md#free)の後は何もしません。

サーボモード中にドライバが過電流、過熱、電源電圧の低下（UVLO）による遮断で自分で無励磁になったとき、サーボモードを取り消し、`ServoModeCancelledOnHiZ`を送信します（電磁ブレーキが有効なときは`BrakeEngagedOnHiZ`も送信されます）。もう一度`/enableServoMode 1`で有効にしてください。現在位置が目標位置になります。

#### 変更

- **v2.2.0**: 電磁ブレーキが有効なとき、ブレーキが保持されている間、解放中、保持への移行中（停止処理中と`/free`の後は除く）の`/enableServoMode 1`は、`/error/command BrakeEngaged`を返し、何もしません。以前は、ブレーキが保持されたままモータを励磁して動かしていました。
- **v2.2.0**: 電磁ブレーキが有効なとき、ブレーキが保持されている間と`/free`の後（モータが無励磁）の`/enableServoMode 0`は、何もしません。以前は、モータを励磁していました。
- **v2.2.0**: サーボモード中にドライバが過電流、過熱、電源電圧の低下（UVLO）による遮断で自分で無励磁になったとき、サーボモードを取り消し、`/error/command ServoModeCancelledOnHiZ`を送信します（[`/reportError`](system-settings.md#reporterror)に従います）。ブレーキの有無によらず同じです。電磁ブレーキが有効なときは、`BrakeEngagedOnHiZ`も送信されます。以前は、ブレーキが無効だと、次のサーボの更新でドライバが再び励磁されていました。ドライバを無励磁にするコマンドは、先にサーボモードを取り消すので、このエラーは送信されません。
- **v2.2.0**: サーボモードを有効にすると、PID制御の積分値と前回の誤差がリセットされます。以前は、前回サーボモードを使ったときの値が残っていました。
- **v2.2.0**: 更新周期が10msから5msになりました（位置レポートが有効なときに7〜13msの間で変動することもなくなりました。複数の返信を送るOSCメッセージが、1回の更新を遅らせることはあります。実測で最大7.75ms）。積分項と微分項は周期に応じて換算されるので、同じ`kP`、`kI`、`kD`でほぼ同じ動きになるように設計されていますが、必要に応じてゲインを調整してください。
- **v2.2.0**: STEP400: HOMEスイッチとLIMITスイッチを別々に判定します。オンのHOMEスイッチは`homingDirection`に向かう動作を止め（`/setProhibitMotionOnHomeSw`が有効か、HOMEスイッチの動作が即停止のとき）、オンのLIMITスイッチはそれと逆向きの動作を止めます（`/setProhibitMotionOnLimitSw`が有効か、LIMITスイッチの動作が即停止のとき）。ここまでは以前と同じです。以前は、HOMEスイッチがオンの間はLIMITスイッチを確認していませんでした。動作が変わるのは、2つのスイッチが両方オンのモータだけです。
- **v2.2.0**: サーボモード中のセンサイベントでの自動の即停止は、ドライバが無励磁のモータには送りません。
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

#### エラー

- `BrakeEngaged`: 電磁ブレーキが効いた状態のままモーションコマンドを送信した。ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`と`/homing`でも送信される（停止処理中と`/free`の後は除く）。

#### 関連

[`/setTargetPosition`](servo-mode_reference.md#settargetposition), [`/setServoParam`](servo-mode_reference.md#setservoparam)
<!-- generated:end osc /enableServoMode -->

<!-- osc: /setServoParam -->
<!-- generated:begin osc /setServoParam -->
### `/setServoParam` (int)motorID (float)kP (float)kI (float)kD {#setservoparam}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| kP | float |  | 比例制御ゲイン |
| kI | float |  | 積分制御ゲイン |
| kD | float |  | 微分制御ゲイン |

#### 実行可能タイミング

常時

#### 説明

PID制御のゲインを調整します。

負のゲインには`CommandIgnored`を返し、何も適用されません。サーボモードの更新周期は5msです。積分項と微分項は周期に応じて換算されます。

#### 変更

- **v2.2.0**: 負のゲインには`/error/command CommandIgnored`を返し、何も適用されません。以前は0に設定されていました。
- **v2.2.0**: サーボの更新周期が10msから5msになりました。同じゲインでほぼ同じ動きになるように設計されていますが、必要に応じて調整してください。

#### エラー

- `CommandIgnored`: コマンドが実行可能なタイミングではない。タイミング参照。値がコマンドの範囲外のときにも送信され、何も適用されない（`/setPositionListReportInterval`のモータIDは255）。

#### 初期値

- `kP`: 0.06（[servoMode.kP](../connections/configuration-items.md#servomode-kp)）
- `kI`: 0（[servoMode.kI](../connections/configuration-items.md#servomode-ki)）
- `kD`: 0（[servoMode.kD](../connections/configuration-items.md#servomode-kd)）

#### 関連

[`/getServoParam`](servo-mode_reference.md#getservoparam)
<!-- generated:end osc /setServoParam -->

<!-- osc: /getServoParam -->
<!-- generated:begin osc /getServoParam -->
### `/getServoParam` (int)motorID {#getservoparam}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

サーボモードのPIDゲイン（kP、kI、kD）を取得します。

#### 返信

```
/servoParam (int)motorID (float)kP (float)kI (float)kD
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| kP | float |  | 比例制御ゲイン |
| kI | float |  | 積分制御ゲイン |
| kD | float |  | 微分制御ゲイン |
<!-- generated:end osc /getServoParam -->

<!-- osc: /setTargetPosition -->
<!-- generated:begin osc /setTargetPosition -->
### `/setTargetPosition` (int)motorID (int)position {#settargetposition}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| position | int | -2097152-2097151 | 目標位置 |

#### 実行可能タイミング

常時

#### 説明

サーボモードの目標位置を設定します。

#### 関連

[`/enableServoMode`](servo-mode_reference.md#enableservomode), [`/setTargetPositionList`](servo-mode_reference.md#settargetpositionlist)
<!-- generated:end osc /setTargetPosition -->

<!-- osc: /setTargetPositionList -->
<!-- generated:begin osc /setTargetPositionList -->
### `/setTargetPositionList` (int)position1 ... (int)positionN {#settargetpositionlist}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| position1 ... positionN | int | -2097152-2097151 | 目標位置 |

#### 実行可能タイミング

常時

#### 説明

サーボモードの目標位置を全軸分まとめて設定します。引数として各軸の目標位置を指定しますので、STEP400の場合は4個、STEP800の場合は8個の引数が必要です。

#### 変更

- **v2.2.0**: モータの数より少ない位置のメッセージには`/error/osc MissingArgument`を返し、何も適用されません。以前は、足りない位置が0になり、サーボモードのモータが0に向かって動いていました。

#### 関連

[`/setTargetPosition`](servo-mode_reference.md#settargetposition)
<!-- generated:end osc /setTargetPositionList -->
