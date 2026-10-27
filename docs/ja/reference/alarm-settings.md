---
title: アラームの設定
---

# アラームの設定

アラームと保護の仕組みは、[アラームと保護](../guides/alarms-and-protection.md)をご覧ください。

## モータドライバ

<!-- osc: /enableUvloReport -->
<!-- generated:begin osc /enableUvloReport -->
### `/enableUvloReport` (int)motorID (bool)enable {#enableuvloreport}

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

指定したモータドライバで電源電圧の低下（UVLO, Undervoltage Lockout）が発生した際に自動で通知メッセージを送信するかどうかを指定します。  
UVLOはモータドライバへ供給されている電圧がUVLO発生条件電圧を下回ったら通知の有無にかかわらず発生します。この状態ではモータを動かすことはできません。供給電圧がUVLO解除条件電圧を上回ったら解除されます。

これらの電圧はSTEP400（PowerSTEP01）とSTEP800（L6470）で異なっていますので、詳しくは対応するデータシートで確認してください。

#### 返信

[`/uvlo`](automatically-sent-messages.md#uvlo)

```
/uvlo (int)motorID (int)state
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| state | int |  |  |

`state`

| 値 | 意味 |
| --- | --- |
| 1 | UVLO発生状態 |
| 0 | UVLO発生無し |

#### 初期値

- `enable`: true（有効）（[alarmAndReport.reportUVLO](../connections/configuration-items.md#alarmandreport-reportuvlo)）

#### 関連

[`/getUvlo`](alarm-settings.md#getuvlo)
<!-- generated:end osc /enableUvloReport -->

<!-- osc: /getUvlo -->
<!-- generated:begin osc /getUvlo -->
### `/getUvlo` (int)motorID {#getuvlo}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

電源電圧の低下（UVLO）の現在の状態を取得します。

#### 返信

[`/uvlo`](automatically-sent-messages.md#uvlo)

```
/uvlo (int)motorID (int)state
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| state | int |  |  |

`state`

| 値 | 意味 |
| --- | --- |
| 1 | UVLO発生状態 |
| 0 | UVLO発生無し |
<!-- generated:end osc /getUvlo -->

<!-- osc: /enableThermalStatusReport -->
<!-- generated:begin osc /enableThermalStatusReport -->
### `/enableThermalStatusReport` (int)motorID (bool)enable {#enablethermalstatusreport}

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

指定したモータドライバの温度状態（thermalStatus）に変化があったら自動でメッセージを送信するかどうかを指定します。Bridge shutdown, Device shutdown状態では、通知の有無にかかわらずモータは無励磁状態になります。

#### 返信

[`/thermalStatus`](automatically-sent-messages.md#thermalstatus)

```
/thermalStatus (int)motorID (int)thermalStatus
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| thermalStatus | int | 0-3 | 温度の状態 |

#### 初期値

- `enable`: true（有効）（[alarmAndReport.reportThermalStatus](../connections/configuration-items.md#alarmandreport-reportthermalstatus)）

#### 関連

[`/getThermalStatus`](alarm-settings.md#getthermalstatus)
<!-- generated:end osc /enableThermalStatusReport -->

<!-- osc: /getThermalStatus -->
<!-- generated:begin osc /getThermalStatus -->
### `/getThermalStatus` (int)motorID {#getthermalstatus}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

ThermalStatusの現在の状態を取得します。STEP400とSTEP800ではThermal statusの種類や発生条件が異なります。

Bridge shutdown, Device shutdown状態では、通知の有無にかかわらずモータは無励磁状態になります。

#### 返信

[`/thermalStatus`](automatically-sent-messages.md#thermalstatus)

```
/thermalStatus (int)motorID (int)thermalStatus
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| thermalStatus | int | 0-3 | 温度の状態 |
<!-- generated:end osc /getThermalStatus -->

<!-- osc: /enableOverCurrentReport -->
<!-- generated:begin osc /enableOverCurrentReport -->
### `/enableOverCurrentReport` (int)motorID (bool)enable {#enableovercurrentreport}

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

指定したモータドライバが過電流状態（OCD, Over Current Detection）になった場合に自動でメッセージを送信するかどうかを指定します。  
過電流状態になった場合は、通知の有無にかかわらず自動で無励磁状態になります。閾値は[`/setOverCurrentThreshold`](alarm-settings.md#setovercurrentthreshold)で設定できます。

#### 返信

[`/overCurrent`](automatically-sent-messages.md#overcurrent)

```
/overCurrent (int)motorID
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |

#### 初期値

- `enable`: true（有効）（[alarmAndReport.reportOCD](../connections/configuration-items.md#alarmandreport-reportocd)）
<!-- generated:end osc /enableOverCurrentReport -->

<!-- osc: /setOverCurrentThreshold -->
<!-- generated:begin osc /setOverCurrentThreshold -->
### `/setOverCurrentThreshold` (int)motorID (int)OCD_TH {#setovercurrentthreshold}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| OCD_TH | int | 0-31（STEP400）、0-15（STEP800） | 過電流検出の閾値 |

#### 実行可能タイミング

常時

#### 説明

過電流の閾値を設定します。STEP400とSTEP800では設定値の範囲と対応する電流が異なっています。

範囲を超える値は拒否されず、最大値の次を0として数え直した値になります（STEP800で16は0、17は1）。

#### 返信

```
/overCurrentThreshold (int)motorID (float)overCurrentThreshold
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| overCurrentThreshold | float | 312.5-10000（STEP400）、375-6000（STEP800）mA | 閾値をmA単位であらわしたものです |

#### 初期値

- `OCD_TH`: STEP400: 15（5A）；STEP800: 7（3A）（[alarmAndReport.OCThreshold](../connections/configuration-items.md#alarmandreport-octhreshold)）

##### 過電流検出の閾値 - STEP400

| OCD_TH | 過電流検出の閾値 |
| --- | --- |
| 0 | 312.5mA |
| 1 | 625mA |
| ... | ... |
| 30 | 9.6875A |
| 31 | 10A |

##### 過電流検出の閾値 - STEP800

| OCD_TH | 過電流検出の閾値 |
| --- | --- |
| 0 | 375mA |
| 1 | 750mA |
| ... | ... |
| 14 | 5.625A |
| 15 | 6A |

#### 関連

[`/getOverCurrentThreshold`](alarm-settings.md#getovercurrentthreshold), [`/enableOverCurrentReport`](alarm-settings.md#enableovercurrentreport)
<!-- generated:end osc /setOverCurrentThreshold -->

<!-- osc: /getOverCurrentThreshold -->
<!-- generated:begin osc /getOverCurrentThreshold -->
### `/getOverCurrentThreshold` (int)motorID {#getovercurrentthreshold}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

過電流の閾値を取得します。

#### 返信

```
/overCurrentThreshold (int)motorID (float)overCurrentThreshold
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| overCurrentThreshold | float | 312.5-10000（STEP400）、375-6000（STEP800）mA | 閾値をmA単位であらわしたものです |
<!-- generated:end osc /getOverCurrentThreshold -->

<!-- osc: /enableStallReport -->
<!-- generated:begin osc /enableStallReport -->
### `/enableStallReport` (int)motorID (bool)enable {#enablestallreport}

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

閾値は[`/setStallThreshold`](alarm-settings.md#setstallthreshold)で設定できます。  
指定したモータドライバでストールが検出された場合、自動で下記のメッセージを送信します。

#### 返信

[`/stall`](automatically-sent-messages.md#stall)

```
/stall (int)motorID
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |

#### 初期値

- `enable`: false（無効）（[alarmAndReport.reportStall](../connections/configuration-items.md#alarmandreport-reportstall)）
<!-- generated:end osc /enableStallReport -->

<!-- osc: /setStallThreshold -->
<!-- generated:begin osc /setStallThreshold -->
### `/setStallThreshold` (int)motorID (int)STALL_TH {#setstallthreshold}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| STALL_TH | int | 0-31（STEP400）、0-127（STEP800） | ストール検出の閾値 |

#### 実行可能タイミング

常時

#### 説明

ストール検出の閾値を設定します。STEP400とSTEP800で設定する値の範囲は異なります。

ストール検出は、モータが負荷に負けて回れなくなった状態を、ドライバが電流から検出する機能です。閾値（`/setStallThreshold`）は、実際に流れている電流にできるだけ近く、少し上になるように探って決めます。脱調（ステップのずれ）程度の小さなずれは検出できませんが、位置が大きくずれたときには検出できることがあります。

範囲を超える値は拒否されず、最大値の次を0として数え直した値になります（STEP800で128は0、129は1）。

#### 変更

- **v2.2.0**: 保存されるSTALL_TH（`/saveConfig`、`/resetMotorDriver`）も変更します。以前は、レジスタだけを変更していました。

#### 返信

```
/stallThreshold (int)motorID (float)stallThreshold
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| stallThreshold | float | 312.5-10000（STEP400）、31.25-4000（STEP800）mA | 閾値をmA単位であらわしたものです |

#### 初期値

- `STALL_TH`: STEP400: 31（10A）；STEP800: 127（4A）（[voltageMode.STALL_TH](../connections/configuration-items.md#voltagemode-stall_th)）

##### ストール検出の閾値 - STEP400

| STALL_TH | ストール検出の閾値 |
| --- | --- |
| 0 | 312.5mA |
| 1 | 625mA |
| ... | ... |
| 30 | 9.6875A |
| 31 | 10A |

##### ストール検出の閾値 - STEP800

| STALL_TH | ストール検出の閾値 |
| --- | --- |
| 0 | 31.25mA |
| 1 | 62.5mA |
| ... | ... |
| 126 | 3.969A |
| 127 | 4A |

#### 関連

[`/getStallThreshold`](alarm-settings.md#getstallthreshold), [`/enableStallReport`](alarm-settings.md#enablestallreport)
<!-- generated:end osc /setStallThreshold -->

<!-- osc: /getStallThreshold -->
<!-- generated:begin osc /getStallThreshold -->
### `/getStallThreshold` (int)motorID {#getstallthreshold}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

ストール検出の閾値を取得します。

#### 返信

```
/stallThreshold (int)motorID (float)stallThreshold
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| stallThreshold | float | 312.5-10000（STEP400）、31.25-4000（STEP800）mA | 閾値をmA単位であらわしたものです |
<!-- generated:end osc /getStallThreshold -->

## センサ

<!-- osc: /setProhibitMotionOnHomeSw -->
<!-- generated:begin osc /setProhibitMotionOnHomeSw -->
### `/setProhibitMotionOnHomeSw` (int)motorID (bool)enable {#setprohibitmotiononhomesw}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| enable | bool |  |  |

`enable`

| 値 | 意味 |
| --- | --- |
| 1 | 禁止 |
| 0 | 許可 |

#### 実行可能タイミング

常時

#### 説明

HOMEスイッチがオンの状態で、原点復帰方向へのモーションコマンドを禁止します。原点復帰方向はconfigToolや`/setHomingDirection`で設定できます。

#### 変更

- **v2.2.0**: ドライバが無励磁のモータには、HOMEスイッチでの自動の即停止を送りません。電磁ブレーキが無効でも同じです（即停止は無励磁のドライバを励磁してしまうため）。

#### 初期値

- `enable`: false（許可）（[driverSettings.prohibitMotionOnHomeSw](../connections/configuration-items.md#driversettings-prohibitmotiononhomesw)）

#### 関連

[`/getProhibitMotionOnHomeSw`](alarm-settings.md#getprohibitmotiononhomesw), [`/setHomingDirection`](homing.md#sethomingdirection)
<!-- generated:end osc /setProhibitMotionOnHomeSw -->

<!-- osc: /getProhibitMotionOnHomeSw -->
<!-- generated:begin osc /getProhibitMotionOnHomeSw -->
### `/getProhibitMotionOnHomeSw` (int)motorID {#getprohibitmotiononhomesw}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

HOMEスイッチがオンの状態で、原点復帰方向へのモーションコマンドが禁止されているかどうかを返します。

#### 返信

```
/prohibitMotionOnHomeSw (int)motorID (int)enable
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| enable | int |  |  |

`enable`

| 値 | 意味 |
| --- | --- |
| 1 | 禁止 |
| 0 | 許可 |
<!-- generated:end osc /getProhibitMotionOnHomeSw -->

<!-- osc: /setProhibitMotionOnLimitSw -->
<!-- generated:begin osc /setProhibitMotionOnLimitSw -->
### `/setProhibitMotionOnLimitSw` (int)motorID (bool)enable {#setprohibitmotiononlimitsw}

STEP400のみ。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| enable | bool |  |  |

`enable`

| 値 | 意味 |
| --- | --- |
| 1 | 禁止 |
| 0 | 許可 |

#### 実行可能タイミング

常時

#### 説明

LIMITスイッチがオンの状態で、原点復帰方向の逆方向へのモーションコマンドを禁止します。原点復帰方向はconfigToolや`/setHomingDirection`で設定できます。

#### 初期値

- `enable`: false（許可）（[driverSettings.prohibitMotionOnLimitSw](../connections/configuration-items.md#driversettings-prohibitmotiononlimitsw)）

#### 関連

[`/getProhibitMotionOnLimitSw`](alarm-settings.md#getprohibitmotiononlimitsw), [`/setHomingDirection`](homing.md#sethomingdirection)
<!-- generated:end osc /setProhibitMotionOnLimitSw -->

<!-- osc: /getProhibitMotionOnLimitSw -->
<!-- generated:begin osc /getProhibitMotionOnLimitSw -->
### `/getProhibitMotionOnLimitSw` (int)motorID {#getprohibitmotiononlimitsw}

STEP400のみ。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

LIMITスイッチがオンの状態で、原点復帰方向の逆方向へのモーションコマンドが禁止されているかどうかを返します。

#### 返信

STEP400のみ。

```
/prohibitMotionOnLimitSw (int)motorID (int)enable
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| enable | int |  |  |

`enable`

| 値 | 意味 |
| --- | --- |
| 1 | 禁止 |
| 0 | 許可 |
<!-- generated:end osc /getProhibitMotionOnLimitSw -->
