---
title: モータドライバの設定
---

# モータドライバの設定

## モータドライバの設定

<!-- osc: /setMicrostepMode -->
<!-- generated:begin osc /setMicrostepMode -->
### `/setMicrostepMode` (int)motorID (int)STEP_SEL {#setmicrostepmode}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| STEP_SEL | int | 0-7 | マイクロステップのモード |

`STEP_SEL`

| 値 | 意味 |
| --- | --- |
| 0 | Full-step |
| 1 | Half-step |
| 2 | 1/4 microstep |
| 3 | 1/8 microstep |
| 4 | 1/16 microstep |
| 5 | 1/32 microstep |
| 6 | 1/64 microstep |
| 7 | 1/128 microstep |

#### 実行可能タイミング

無励磁状態

#### 説明

マイクロステップのモードを切り替えます。

定電流制御モード（current mode）では、Full-stepから1/16 microstepまでしか使えません。

モータは無励磁でなければなりません。励磁して位置を保っているモータは無励磁ではありません。先に[`/softHiZ`](motor-control.md#softhiz)か[`/hardHiZ`](motor-control.md#hardhiz)を送ってください。そうでないときは`MotorNotHiZ`を返し、何も適用されません。STEP400の電流モードでは、1/16より細かいステップモードに`CommandIgnored`を返します。

0〜7の範囲外の値は拒否されません。8ビットに変換されてから0〜7に制限されます（-1は7、256は0になります）。

#### 変更

- **v2.2.0**: モータは無励磁でなければなりません。そうでないときは`/error/command MotorNotHiZ`を返し、何も適用されません。以前は、ドライバが書き込みを無視する一方で、ファームウェアの変数と保存される設定は新しい値になっていました。
- **v2.2.0**: STEP400の電流モードでは、1/16より細かいステップモードに`CommandIgnored`を返します（PowerSTEP01の電流モードは1/16までです）。

#### エラー

- `MotorNotHiZ`: ドライバのレジスタのうち、出力が無励磁のときだけ書き込めるものをコマンドが書き込もうとしたが、モータが無励磁ではなかった。励磁して位置を保っているモータは無励磁ではない。先に`/softHiZ`か`/hardHiZ`を送る。何も適用されない。v2.2.0で追加。
- `CommandIgnored`: コマンドが実行可能なタイミングではない。タイミング参照。値がコマンドの範囲外のときにも送信され、何も適用されない（`/setPositionListReportInterval`のモータIDは255）。

#### 初期値

- `STEP_SEL`: 7（1/128 microstep）（[driverSettings.stepMode](../connections/configuration-items.md#driversettings-stepmode)）

#### 関連

[`/getMicrostepMode`](motor-driver-settings.md#getmicrostepmode), [`/setCurrentMode`](voltage-and-current-mode-settings.md#setcurrentmode)
<!-- generated:end osc /setMicrostepMode -->

<!-- osc: /getMicrostepMode -->
<!-- generated:begin osc /getMicrostepMode -->
### `/getMicrostepMode` (int)motorID {#getmicrostepmode}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

マイクロステップのモードを取得します。STEP_SELについては[`/setMicrostepMode`](motor-driver-settings.md#setmicrostepmode)の項目を参照してください。

#### 返信

```
/microstepMode (int)motorID (int)STEP_SEL
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| STEP_SEL | int | 0-7 | マイクロステップのモード |

`STEP_SEL`

| 値 | 意味 |
| --- | --- |
| 0 | Full-step |
| 1 | Half-step |
| 2 | 1/4 microstep |
| 3 | 1/8 microstep |
| 4 | 1/16 microstep |
| 5 | 1/32 microstep |
| 6 | 1/64 microstep |
| 7 | 1/128 microstep |
<!-- generated:end osc /getMicrostepMode -->

<!-- osc: /enableLowSpeedOptimize -->
<!-- generated:begin osc /enableLowSpeedOptimize -->
### `/enableLowSpeedOptimize` (int)motorID (bool)enable {#enablelowspeedoptimize}

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

モータ停止時

#### 説明

低速回転時の相電流ひずみ補正（Low speed optimization）の有効無効を切り替えます。この設定が有効になっていると、`Min Speed`は自動的に0になります。この補正は電圧モードでのみ利用可能です。詳しくは対応するデータシートの "Low speed optimization"を参照してください。

#### 変更

- **v2.2.0**: モータは停止中か無励磁でなければなりません。回転中のモータには`/error/command MotorNotStopped`を返し、何も適用されません。

#### エラー

- `MotorNotStopped`: 停止中か無励磁のときだけ書き込めるドライバのレジスタをコマンドが書き込もうとしたが、モータが回転していた。何も適用されない。v2.2.0で追加。

#### 初期値

- `enable`: false（無効）（[voltageMode.lowSpeedOptimizeEnable](../connections/configuration-items.md#voltagemode-lowspeedoptimizeenable)）

#### 関連

[`/setLowSpeedOptimizeThreshold`](motor-driver-settings.md#setlowspeedoptimizethreshold), [`/setMinSpeed`](speed-profile.md#setminspeed)
<!-- generated:end osc /enableLowSpeedOptimize -->

<!-- osc: /setLowSpeedOptimizeThreshold -->
<!-- generated:begin osc /setLowSpeedOptimizeThreshold -->
### `/setLowSpeedOptimizeThreshold` (int)motorID (float)lowSpeedOptimizationThreshold {#setlowspeedoptimizethreshold}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| lowSpeedOptimizationThreshold | float | 0-976.3 step/s | 低速最適化の閾値 |

#### 実行可能タイミング

常時

#### 説明

低速回転時の相電流ひずみ補正を行う閾値を設定します。

返信はありません。値は[`/getLowSpeedOptimizeThreshold`](motor-driver-settings.md#getlowspeedoptimizethreshold)で読み戻してください。

低速最適化が有効の間は、モータは停止中か無励磁でなければなりません。回転中のモータには`MotorNotStopped`を返し、何も適用されません。

#### 変更

- **v2.2.0**: 低速最適化が有効の間は、回転中のモータに`/error/command MotorNotStopped`を返し、何も適用されません。

#### エラー

- `MotorNotStopped`: 停止中か無励磁のときだけ書き込めるドライバのレジスタをコマンドが書き込もうとしたが、モータが回転していた。何も適用されない。v2.2.0で追加。

#### 初期値

- `lowSpeedOptimizationThreshold`: 20（[voltageMode.lowSpeedOptimize](../connections/configuration-items.md#voltagemode-lowspeedoptimize)）

#### 関連

[`/getLowSpeedOptimizeThreshold`](motor-driver-settings.md#getlowspeedoptimizethreshold), [`/enableLowSpeedOptimize`](motor-driver-settings.md#enablelowspeedoptimize)
<!-- generated:end osc /setLowSpeedOptimizeThreshold -->

<!-- osc: /getLowSpeedOptimizeThreshold -->
<!-- generated:begin osc /getLowSpeedOptimizeThreshold -->
### `/getLowSpeedOptimizeThreshold` (int)motorID {#getlowspeedoptimizethreshold}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

Low speed optimization thresholdの現在の設定値を取得します。

#### 返信

```
/lowSpeedOptimizeThreshold (int)motorID (float)lowSpeedOptimizeThreshold (int)optimizationEnabled
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| lowSpeedOptimizeThreshold | float | 0-976.3 step/s | 低速最適化の閾値 |
| optimizationEnabled | int |  |  |

`optimizationEnabled`

| 値 | 意味 |
| --- | --- |
| 1 | Low speed optimization有効 |
| 0 | Low speed optimization無効 |

##### 変更

- **v2.2.0**: 第3引数の`optimizationEnabled`は、整数の型タグ`i`（0 / 1）で送信されます。以前は`T` / `F`でした。`T` / `F`を想定しているクライアントは、更新が必要です。
<!-- generated:end osc /getLowSpeedOptimizeThreshold -->

## 状態の取得

<!-- osc: /enableBusyReport -->
<!-- generated:begin osc /enableBusyReport -->
### `/enableBusyReport` (int)motorID (bool)enable {#enablebusyreport}

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

指定したモータのBUSY状態に変化があったら自動でメッセージを送信する設定を行います。メッセージは[`/getBusy`](motor-driver-settings.md#getbusy)の返信と同じです。

#### 返信

[`/busy`](automatically-sent-messages.md#busy)

```
/busy (int)motorID (int)state
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| state | int |  |  |

`state`

| 値 | 意味 |
| --- | --- |
| 1 | BUSYの場合 |
| 0 | BUSYでない場合 |

#### 初期値

- `enable`: false（無効）（[alarmAndReport.reportBUSY](../connections/configuration-items.md#alarmandreport-reportbusy)）
<!-- generated:end osc /enableBusyReport -->

<!-- osc: /getBusy -->
<!-- generated:begin osc /getBusy -->
### `/getBusy` (int)motorID {#getbusy}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

指定したモータのBUSY状態を取得します。

#### 返信

[`/busy`](automatically-sent-messages.md#busy)

```
/busy (int)motorID (int)state
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| state | int |  |  |

`state`

| 値 | 意味 |
| --- | --- |
| 1 | BUSYの場合 |
| 0 | BUSYでない場合 |
<!-- generated:end osc /getBusy -->

<!-- osc: /enableHizReport -->
<!-- generated:begin osc /enableHizReport -->
### `/enableHizReport` (int)motorID (bool)enable {#enablehizreport}

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

指定したモータの無励磁状態に変化があったら自動でメッセージを送信する設定を行います。送信されるメッセージは[`/getHiZ`](motor-driver-settings.md#gethiz)の返信と同じです。

#### 返信

[`/HiZ`](automatically-sent-messages.md#hiz)

```
/HiZ (int)motorID (int)state
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| state | int | 0-1 | 1:無励磁状態の場合, 0:無励磁状態でない場合 |

#### 初期値

- `enable`: false（無効）（[alarmAndReport.reportHiZ](../connections/configuration-items.md#alarmandreport-reporthiz)）
<!-- generated:end osc /enableHizReport -->

<!-- osc: /getHiZ -->
<!-- generated:begin osc /getHiZ -->
### `/getHiZ` (int)motorID {#gethiz}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

指定したモータの無励磁状態を取得します。

#### 返信

[`/HiZ`](automatically-sent-messages.md#hiz)

```
/HiZ (int)motorID (int)state
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| state | int | 0-1 | 1:無励磁状態の場合, 0:無励磁状態でない場合 |
<!-- generated:end osc /getHiZ -->

<!-- osc: /enableDirReport -->
<!-- generated:begin osc /enableDirReport -->
### `/enableDirReport` (int)motorID (bool)enable {#enabledirreport}

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

指定したモータの回転方向に変化があったら自動でメッセージを送信する設定を行います。送信されるメッセージは[`/getDir`](motor-driver-settings.md#getdir)の返信と同じです。

#### 返信

[`/dir`](automatically-sent-messages.md#dir)

```
/dir (int)motorID (int)direction
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| direction | int |  |  |

`direction`

| 値 | 意味 |
| --- | --- |
| 1 | 正転方向 |
| 0 | 逆転方向 |

#### 初期値

- `enable`: false（無効）（[alarmAndReport.reportDir](../connections/configuration-items.md#alarmandreport-reportdir)）
<!-- generated:end osc /enableDirReport -->

<!-- osc: /getDir -->
<!-- generated:begin osc /getDir -->
### `/getDir` (int)motorID {#getdir}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

指定したモータの回転方向を取得します。

#### 変更

- **v2.2.0**: `/getDir 255`（全モータ）が方向を返します。以前は無励磁の状態が返っていました。

#### 返信

[`/dir`](automatically-sent-messages.md#dir)

```
/dir (int)motorID (int)direction
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| direction | int |  |  |

`direction`

| 値 | 意味 |
| --- | --- |
| 1 | 正転方向 |
| 0 | 逆転方向 |
<!-- generated:end osc /getDir -->

<!-- osc: /enableMotorStatusReport -->
<!-- generated:begin osc /enableMotorStatusReport -->
### `/enableMotorStatusReport` (int)motorID (bool)enable {#enablemotorstatusreport}

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

指定したモータの動作状態（MOT_STATUS）に変化があったら自動でメッセージを送信する設定を行います。メッセージは[`/getMotorStatus`](motor-driver-settings.md#getmotorstatus)の返信と同じです。

#### 返信

[`/motorStatus`](automatically-sent-messages.md#motorstatus)

```
/motorStatus (int)motorID (int)MOT_STATUS
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| MOT_STATUS | int | 0-3 | モータの状態 |

`MOT_STATUS`

| 値 | 意味 |
| --- | --- |
| 0 | モータ停止 |
| 1 | 加速中 |
| 2 | 減速中 |
| 3 | 一定速運転中 |

#### 初期値

- `enable`: false（無効）（[alarmAndReport.reportMotorStatus](../connections/configuration-items.md#alarmandreport-reportmotorstatus)）
<!-- generated:end osc /enableMotorStatusReport -->

<!-- osc: /getMotorStatus -->
<!-- generated:begin osc /getMotorStatus -->
### `/getMotorStatus` (int)motorID {#getmotorstatus}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

指定したモータの動作状態（MOT_STATUS）を取得します。

#### 返信

[`/motorStatus`](automatically-sent-messages.md#motorstatus)

```
/motorStatus (int)motorID (int)MOT_STATUS
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| MOT_STATUS | int | 0-3 | モータの状態 |

`MOT_STATUS`

| 値 | 意味 |
| --- | --- |
| 0 | モータ停止 |
| 1 | 加速中 |
| 2 | 減速中 |
| 3 | 一定速運転中 |
<!-- generated:end osc /getMotorStatus -->

<!-- osc: /setPositionReportInterval -->
<!-- generated:begin osc /setPositionReportInterval -->
### `/setPositionReportInterval` (int)motorID (int)interval {#setpositionreportinterval}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| interval | int | 0-65535 ms | 送信間隔 |

#### 実行可能タイミング

常時

#### 説明

指定したモータの現在位置（`ABS_POS`）を指定間隔で自動送信します。0を指定すると無効化され、送信を停止します。  
いずれかのモータで有効化された場合、`/setPositionListReportInterval`は無効になり自動停止します。

65535を超える間隔には`CommandIgnored`を返し、何も適用されません。負の間隔は、0と同じく通知を無効にします。

#### 変更

- **v2.2.0**: 65535を超える値には`/error/command CommandIgnored`を返し、何も適用されません。以前は32768以上が負の値として読まれ、通知が止まっていました。負の間隔で通知が止まる点は変わりません。
- **v2.2.0**: 1つのモータで通知を有効にしたとき（間隔が0より大きいとき）は、保存されている位置リスト通知の間隔も、255の場合と同じように消去されます。以前は、リスト通知から1つのモータの通知に切り替えて保存した設定が、次の起動でリスト通知を再び始め、そのモータの通知を消していました。

#### 返信

[`/position`](automatically-sent-messages.md#position)

```
/position (int)motorID (int)ABS_POS
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| ABS_POS | int | -2097152-2097151 | 現在位置 |

#### エラー

- `CommandIgnored`: コマンドが実行可能なタイミングではない。タイミング参照。値がコマンドの範囲外のときにも送信され、何も適用されない（`/setPositionListReportInterval`のモータIDは255）。

#### 初期値

- `interval`: 0（[alarmAndReport.reportPositionInterval](../connections/configuration-items.md#alarmandreport-reportpositioninterval)）

#### 関連

[`/getPosition`](position-management.md#getposition), [`/setPositionListReportInterval`](motor-driver-settings.md#setpositionlistreportinterval)
<!-- generated:end osc /setPositionReportInterval -->

<!-- osc: /setPositionListReportInterval -->
<!-- generated:begin osc /setPositionListReportInterval -->
### `/setPositionListReportInterval` (int)interval {#setpositionlistreportinterval}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| interval | int | 0-65535 ms | 送信間隔 |

#### 実行可能タイミング

常時

#### 説明

全モータの現在位置（`ABS_POS`）をひとつのリストにまとめたメッセージを指定間隔で自動送信します。0を指定すると無効化され、送信を停止します。  
このコマンドが有効化される際には`/setPositionReportInterval`はすべての軸で無効になり自動停止します。

65535を超える間隔には、モータID 255で`CommandIgnored`を返し、何も適用されません。負の間隔は、0と同じく通知を無効にします。

#### 変更

- **v2.2.0**: 65535を超える値には`/error/command CommandIgnored 255`を返し、何も適用されません。以前は32768以上が負の値として読まれ、通知が止まっていました。負の間隔で通知が止まる点は変わりません。

#### 返信

[`/positionList`](automatically-sent-messages.md#positionlist)

```
/positionList (int)position1 ... (int)positionN
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| position1 ... positionN | int | -2097152-2097151 | n個目のモータの現在位置 |

#### エラー

- `CommandIgnored`: コマンドが実行可能なタイミングではない。タイミング参照。値がコマンドの範囲外のときにも送信され、何も適用されない（`/setPositionListReportInterval`のモータIDは255）。

#### 初期値

- `interval`: 0（[alarmAndReport.reportPositionListInterval](../connections/configuration-items.md#alarmandreport-reportpositionlistinterval)）

#### 関連

[`/getPositionList`](position-management.md#getpositionlist), [`/setPositionReportInterval`](motor-driver-settings.md#setpositionreportinterval)
<!-- generated:end osc /setPositionListReportInterval -->

## デバッグ

<!-- osc: /getAdcVal -->
<!-- generated:begin osc /getAdcVal -->
### `/getAdcVal` (int)motorID {#getadcval}

STEP400のみ。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

PowerSTEP01チップのADC_OUTレジスタの値を取得します。このレジスタはADCピンの電圧を5ビットでAD変換した値が収められています。このピンは10kΩでプルアップされていて、LIMITSWコネクタに接続されています。

STEP400のみです。ファームウェアはSTEP800でもこのコマンドを受け付けますが、意味のある値は得られません。

#### 返信

```
/adcVal (int)motorID (int)ADC_OUT
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| ADC_OUT | int | 0-31 | 5bitのADC_OUTレジスタ |
<!-- generated:end osc /getAdcVal -->

<!-- osc: /getStatus -->
<!-- generated:begin osc /getStatus -->
### `/getStatus` (int)motorID {#getstatus}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

モータドライバ（PowerSTEP01/L6470）のSTATUSレジスタを取得します。STATUSレジスタにはモータやアラーム、スイッチの状態などが含まれます。

レジスタに含まれる情報は、データシートを参照してください。このうち、一部の値はラッチされていて、STATUSレジスタを読み出すとリセットされます。ボードではファームウェアによって常時STATUSレジスタを繰り返し取得しているため、これらの値はすぐにリセットされてしまいます。これらの事象を個別に通知する設定が可能ですので、そちらを利用してください。

このコマンドはラッチされたフラグを消しません。消すのはファームウェアのSTATUSレジスタの読み出し（5msごと）だけです。

#### 変更

- **v2.2.0**: STATUSレジスタをGetStatusではなくGetParamで読み出すため、ラッチされたドライバのフラグ（OCD、ストールのフラグ、UVLO、SW_EVNなど）を消さなくなりました。レジスタの値は同じです。フラグを消すのはファームウェアのSTATUSレジスタの読み出し（5msごと）だけになったため、直前に別の`/getStatus`を送っていても、先の返信に出ていたフラグが次の返信にも出ることがあります（次の読み出しまでの最大5ms）。

#### 返信

```
/status (int)motorID (int)status
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| status | int | 0-65535 | 16bitのSTATUSレジスタ |

| STATUSレジスタのビット名（STEP400） | STATUSレジスタのビット名（STEP800） | 対応する設定コマンド |
| --- | --- | --- |
| UVLO | UVLO | [`/enableUvloReport`](alarm-settings.md#enableuvloreport) |
| UVLO_ADC | - | この機能はSTEP400では使えませんので常時無効になっています。 |
| OCD | OCD | [`/enableOverCurrentReport`](alarm-settings.md#enableovercurrentreport) |
| STALL_A, STALL_B | STEP_LOSS_A, STEP_LOSS_B | [`/enableStallReport`](alarm-settings.md#enablestallreport) |
| CMD_ERROR | WRONG_CMD, NOTPREF_CMD | [`/reportError`](system-settings.md#reporterror) |
| TH_STATUS | TH_WRN, TH_SD | [`/enableThermalStatusReport`](alarm-settings.md#enablethermalstatusreport) |
| SW_EVN | SW_EVN | [`/enableSwEventReport`](home-and-limit-sensors.md#enablesweventreport) |
| MOT_STATUS | MOT_STATUS | [`/enableMotorStatusReport`](motor-driver-settings.md#enablemotorstatusreport) |
| SW_F | SW_F | [`/enableHomeSwReport`](home-and-limit-sensors.md#enablehomeswreport) |
| BUSY | BUSY | [`/enableBusyReport`](motor-driver-settings.md#enablebusyreport) |
| HiZ | HiZ | [`/enableHizReport`](motor-driver-settings.md#enablehizreport) |

#### 関連

[`/getStatusList`](motor-driver-settings.md#getstatuslist)
<!-- generated:end osc /getStatus -->

<!-- osc: /getConfigRegister -->
<!-- generated:begin osc /getConfigRegister -->
### `/getConfigRegister` (int)motorID {#getconfigregister}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

モータドライバ（PowerSTEP01/L6470）のCONFIGレジスタを取得します。CONFIGレジスタにはモータやアラーム、スイッチの状態などが含まれます。

CONFIGレジスタにはモータドライバの各種設定が収められています。詳細についてはモータドライバのデータシートを参照してください。

#### 返信

```
/configRegister (int)motorID (int)CONFIG
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| CONFIG | int | 0-65535 | 16bitのCONFIGレジスタ |
<!-- generated:end osc /getConfigRegister -->

<!-- osc: /resetMotorDriver -->
<!-- generated:begin osc /resetMotorDriver -->
### `/resetMotorDriver` (int)motorID {#resetmotordriver}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

モータドライバ（PowerSTEP01/L6470）をリセットし、初期設定値を再度書き込みます。

電磁ブレーキが有効なときは、ブレーキが保持されている間か[`/free`](brake.md#free)の後（モータが無励磁）だけ受け付けます。それ以外では`CommandIgnored`を返します。受け付けたときは（ブレーキが無効でも）、保留中の動作とサーボモードを取り消します。拒否されたコマンド（`CommandIgnored`）は、何も取り消しません。

#### 変更

- **v2.2.0**: 電磁ブレーキが有効なときは、ブレーキが保持されている間か`/free`の後だけ受け付けます。それ以外では`/error/command CommandIgnored`を返します。以前は、ブレーキを解放したままドライバを無励磁にしていました。
- **v2.2.0**: 受け付けたときは、保留中の動作（BUSYフラグが下りるのを待つ`/goTo`など、原点復帰、サーボモード）を取り消します。ブレーキが無効なモータでも同じです。拒否されたコマンド（`CommandIgnored`）は、何も取り消しません。
- **v2.2.0**: リセット後に再び適用される設定には、Rawコマンドで設定したもの（[`/setAccRaw`](speed-profile.md#setaccraw)を参照）も含まれます。

#### エラー

- `CommandIgnored`: コマンドが実行可能なタイミングではない。タイミング参照。値がコマンドの範囲外のときにも送信され、何も適用されない（`/setPositionListReportInterval`のモータIDは255）。
<!-- generated:end osc /resetMotorDriver -->

<!-- osc: /getStatusList -->
<!-- generated:begin osc /getStatusList -->
### `/getStatusList` {#getstatuslist}

#### 引数

なし

#### 実行可能タイミング

常時

#### 説明

すべてのモータのSTATUSレジスタをまとめて取得します。レジスタの内容は[`/getStatus`](motor-driver-settings.md#getstatus)を参照してください。

#### 変更

- **v2.2.0**: STATUSレジスタをGetStatusではなくGetParamで読み出すため、ラッチされたドライバのフラグを消さなくなりました。[`/getStatus`](motor-driver-settings.md#getstatus)を参照してください。

#### 返信

```
/statusList (int)status1 ... (int)statusN
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| status1 ... statusN | int | 0-65535 |  |

#### 関連

[`/getStatus`](motor-driver-settings.md#getstatus)
<!-- generated:end osc /getStatusList -->
