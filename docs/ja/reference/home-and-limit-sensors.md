---
title: HOME/LIMITスイッチ
---

# HOME/LIMITスイッチ

原点復帰でのHOMEスイッチとLIMITスイッチの使い方は、[原点復帰と位置管理](../guides/homing-and-position.md)をご覧ください。

## 状態の取得

<!-- osc: /enableHomeSwReport -->
<!-- generated:begin osc /enableHomeSwReport -->
### `/enableHomeSwReport` (int)motorID (bool)enable {#enablehomeswreport}

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

指定したモータのHOME端子の状態に変化があったら自動でメッセージを送信する設定を行います。送信されるメッセージは[`/getHomeSw`](home-and-limit-sensors.md#gethomesw)の返信と同じです。

#### 返信

[`/homeSw`](automatically-sent-messages.md#homesw)

```
/homeSw (int)motorID (int)swState (int)direction
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| swState | int |  | 状態 |
| direction | int |  | 方向 |

`swState`

| 値 | 意味 |
| --- | --- |
| 0 | オフ |
| 1 | オン |

`direction`

| 値 | 意味 |
| --- | --- |
| 1 | 正転方向 |
| 0 | 逆転方向 |

#### 初期値

- `enable`: false（無効）（[alarmAndReport.reportHomeSwStatus](../connections/configuration-items.md#alarmandreport-reporthomeswstatus)）
<!-- generated:end osc /enableHomeSwReport -->

<!-- osc: /enableSwEventReport -->
<!-- generated:begin osc /enableSwEventReport -->
### `/enableSwEventReport` (int)motorID (bool)enable {#enablesweventreport}

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

指定したモータのHOME端子の状態がHIGHレベルからLOWレベルに遷移した際（Falling Edge）に自動でメッセージを送信する設定を行います。  
[`/enableHomeSwReport`](home-and-limit-sensors.md#enablehomeswreport)はMCUのファームウェア上から約1ms毎にモータドライバICのSTATUSレジスタをポーリングすることによって状態を監視していますが、この`/enableSwEventReport`のほうはドライバIC内でハードウェアによってイベントが検出されるため、1ms以下のごくわずかな時間だけスイッチがオンになった場合でももとり逃しません。

#### 返信

[`/swEvent`](automatically-sent-messages.md#swevent)

```
/swEvent (int)motorID
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |

#### 初期値

- `enable`: false（無効）（[alarmAndReport.reportSwEvn](../connections/configuration-items.md#alarmandreport-reportswevn)）
<!-- generated:end osc /enableSwEventReport -->

<!-- osc: /getHomeSw -->
<!-- generated:begin osc /getHomeSw -->
### `/getHomeSw` (int)motorID {#gethomesw}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

HOMEスイッチの状態を取得します。

#### 返信

[`/homeSw`](automatically-sent-messages.md#homesw)

```
/homeSw (int)motorID (int)swState (int)direction
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| swState | int |  | 状態 |
| direction | int |  | 方向 |

`swState`

| 値 | 意味 |
| --- | --- |
| 0 | オフ |
| 1 | オン |

`direction`

| 値 | 意味 |
| --- | --- |
| 1 | 正転方向 |
| 0 | 逆転方向 |
<!-- generated:end osc /getHomeSw -->

<!-- osc: /enableLimitSwReport -->
<!-- generated:begin osc /enableLimitSwReport -->
### `/enableLimitSwReport` (int)motorID (bool)enable {#enablelimitswreport}

STEP400のみ。

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

指定したモータのLIMIT端子の状態に変化があったら自動でメッセージを送信する設定を行います。送信されるメッセージは[`/getLimitSw`](home-and-limit-sensors.md#getlimitsw)の返信と同じです。

#### 返信

[`/limitSw`](automatically-sent-messages.md#limitsw)

STEP400のみ。

```
/limitSw (int)motorID (int)swState (int)direction
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| swState | int |  | 状態 |
| direction | int |  | 方向 |

`swState`

| 値 | 意味 |
| --- | --- |
| 0 | オフ |
| 1 | オン |

`direction`

| 値 | 意味 |
| --- | --- |
| 1 | 正転方向 |
| 0 | 逆転方向 |

#### 初期値

- `enable`: false（無効）（[alarmAndReport.reportLimitSwStatus](../connections/configuration-items.md#alarmandreport-reportlimitswstatus)）
<!-- generated:end osc /enableLimitSwReport -->

<!-- osc: /getLimitSw -->
<!-- generated:begin osc /getLimitSw -->
### `/getLimitSw` (int)motorID {#getlimitsw}

STEP400のみ。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

LIMITスイッチの状態を取得します。

#### 返信

[`/limitSw`](automatically-sent-messages.md#limitsw)

STEP400のみ。

```
/limitSw (int)motorID (int)swState (int)direction
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| swState | int |  | 状態 |
| direction | int |  | 方向 |

`swState`

| 値 | 意味 |
| --- | --- |
| 0 | オフ |
| 1 | オン |

`direction`

| 値 | 意味 |
| --- | --- |
| 1 | 正転方向 |
| 0 | 逆転方向 |
<!-- generated:end osc /getLimitSw -->

## 反応時の動作設定

<!-- osc: /setHomeSwMode -->
<!-- generated:begin osc /setHomeSwMode -->
### `/setHomeSwMode` (int)motorID (bool)SW_MODE {#sethomeswmode}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| SW_MODE | bool |  | スイッチがオンになったときの動作 |

`SW_MODE`

| 値 | 意味 |
| --- | --- |
| 0 | HardStop interrupt（即停止する） |
| 1 | User disposal（停止しない） |

#### 実行可能タイミング

無励磁状態

#### 説明

HOME端子に入力があった際に即停止するかどうか（Switch mode）を指定します。

出力は無励磁でなければなりません。そうでないときは`MotorNotHiZ`を返し、何も適用されません。

#### 変更

- **v2.2.0**: 出力は無励磁でなければなりません（CONFIGレジスタのSW_MODEは無励磁のときだけ書き込めます）。そうでないときは`/error/command MotorNotHiZ`を返し、何も適用されません。

#### エラー

- `MotorNotHiZ`: ドライバのレジスタのうち、出力が無励磁のときだけ書き込めるものをコマンドが書き込もうとしたが、モータが無励磁ではなかった。励磁して位置を保っているモータは無励磁ではない。先に`/softHiZ`か`/hardHiZ`を送る。何も適用されない。v2.2.0で追加。

#### 初期値

- `SW_MODE`: true（User disposal（停止しない））（[driverSettings.homeSwMode](../connections/configuration-items.md#driversettings-homeswmode)）

#### 関連

[`/getHomeSwMode`](home-and-limit-sensors.md#gethomeswmode)
<!-- generated:end osc /setHomeSwMode -->

<!-- osc: /getHomeSwMode -->
<!-- generated:begin osc /getHomeSwMode -->
### `/getHomeSwMode` (int)motorID {#gethomeswmode}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

上記のSwitch modeを取得します。

#### 返信

```
/homeSwMode (int)motorID (int)swMode
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| swMode | int | 0-1 |  |

#### 関連

[`/setHomeSwMode`](home-and-limit-sensors.md#sethomeswmode)
<!-- generated:end osc /getHomeSwMode -->

<!-- osc: /setLimitSwMode -->
<!-- generated:begin osc /setLimitSwMode -->
### `/setLimitSwMode` (int)motorID (bool)SW_MODE {#setlimitswmode}

STEP400のみ。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| SW_MODE | bool |  | スイッチがオンになったときの動作 |

`SW_MODE`

| 値 | 意味 |
| --- | --- |
| 0 | HardStop interrupt（即停止する） |
| 1 | User disposal（停止しない） |

#### 実行可能タイミング

常時

#### 説明

LIMIT端子に入力があった際に即停止するかどうか（Switch mode）を指定します。

#### 変更

- **v2.2.0**: ドライバが無励磁のモータには、LIMITスイッチでの自動の即停止（`SW_HARD_STOP`）を送りません。電磁ブレーキが無効でも同じです（即停止は無励磁のドライバを励磁してしまうため）。

#### 初期値

- `SW_MODE`: true（User disposal（停止しない））（[driverSettings.limitSwMode](../connections/configuration-items.md#driversettings-limitswmode)）

#### 関連

[`/getLimitSwMode`](home-and-limit-sensors.md#getlimitswmode)
<!-- generated:end osc /setLimitSwMode -->

<!-- osc: /getLimitSwMode -->
<!-- generated:begin osc /getLimitSwMode -->
### `/getLimitSwMode` (int)motorID {#getlimitswmode}

STEP400のみ。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

上記のSwitch modeを取得します。

#### 返信

STEP400のみ。

```
/limitSwMode (int)motorID (int)swMode
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| swMode | int | 0-1 |  |

#### 関連

[`/setLimitSwMode`](home-and-limit-sensors.md#setlimitswmode)
<!-- generated:end osc /getLimitSwMode -->
