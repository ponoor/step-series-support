---
title: 原点復帰
---

# 原点復帰

原点復帰と位置管理の仕組みは、[原点復帰と位置管理](../guides/homing-and-position.md)をご覧ください。

<!-- osc: /homing -->
<!-- generated:begin osc /homing -->
### `/homing` (int)motorID {#homing}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

原点復帰動作を行います。原点復帰方向に移動し、HOMEスイッチがオンになると停止し、方向を反転してゆっくり移動し、HOMEスイッチがオフになった時点で停止し、現在位置を0にします。

これは[`/goUntil`](homing.md#gountil)コマンドを実行し、HOMEスイッチがオンになると停止して[`/releaseSw`](homing.md#releasesw)コマンドを実行することに相当します。

原点復帰方向`homingDirection`と原点復帰の速度`homingSpeed`はそれぞれ[`/setHomingDirection`](homing.md#sethomingdirection)と[`/setHomingSpeed`](homing.md#sethomingspeed)で設定できるほか、configToolからも設定できます。

`/goUntil`と`/releaseSw`それぞれにタイムアウト時間が設定可能で、この時間内にスイッチの状態に変化がなかった場合はタイムアウトとして動作を中止します。この時間はそれぞれ[`/setGoUntilTimeout`](homing.md#setgountiltimeout)、[`/setReleaseSwTimeout`](homing.md#setreleaseswtimeout)で設定できます。

原点復帰動作の状態変化に応じて下記の通知があります。

#### 変更

- **v2.2.0**: ブレーキが保持されている間、解放中、保持への移行中（停止処理中と`/free`の後は除く）は、`/error/command BrakeEngaged`を返し、何もしません。以前は、原点復帰が始まらないのに原点復帰の状態になっていました。
- **v2.2.0**: 原点復帰が、センサを検出した約1ms後に、3（ReleaseSW完了）ではなく`/homingStatus` 4と`ReleaseSwTimeout`で終わることが多かった問題を修正しました（タイムアウト判定の時刻の誤差が原因で、起動のしかたによって、ほとんどの原点復帰で起きるか、ほとんど起きないかのどちらかでした）。

#### 返信

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
- `BrakeEngaged`: 電磁ブレーキが効いた状態のままモーションコマンドを送信した。ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`と`/homing`でも送信される（停止処理中と`/free`の後は除く）。
- `GoUntilTimeout`: `/goUntil`コマンド実行中にタイムアウトした。
- `ReleaseSwTimeout`: `/releaseSw`コマンド実行中にタイムアウトした。
- `InServoMode`: サーボモードでは実行できないコマンドを送信した。**v2.2.0**: `/goUntil`、`/goUntilRaw`、`/releaseSw`でも送信されます。

#### 関連

[`/getHomingStatus`](homing.md#gethomingstatus)
<!-- generated:end osc /homing -->

<!-- osc: /getHomingStatus -->
<!-- generated:begin osc /getHomingStatus -->
### `/getHomingStatus` (int)motorID {#gethomingstatus}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

原点復帰の現在の状態を返します。

#### 返信

[`/homingStatus`](automatically-sent-messages.md#homingstatus)

```
/homingStatus (int)motorID (int)homingStatus
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| homingStatus | int | 0-4 | 原点復帰の状態 |
<!-- generated:end osc /getHomingStatus -->

<!-- osc: /setHomingDirection -->
<!-- generated:begin osc /setHomingDirection -->
### `/setHomingDirection` (int)motorID (bool)direction {#sethomingdirection}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| direction | bool |  |  |

`direction`

| 値 | 意味 |
| --- | --- |
| 1 | Forward |
| 0 | Reverse |

#### 実行可能タイミング

常時

#### 説明

[`/homing`](homing.md#homing)実行時の原点復帰方向`homingDirection`を指定します。configToolからも指定できます。

#### 初期値

- `direction`: 0（Reverse）（[driverSettings.homingDirection](../connections/configuration-items.md#driversettings-homingdirection)）

#### 関連

[`/getHomingDirection`](homing.md#gethomingdirection)
<!-- generated:end osc /setHomingDirection -->

<!-- osc: /getHomingDirection -->
<!-- generated:begin osc /getHomingDirection -->
### `/getHomingDirection` (int)motorID {#gethomingdirection}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

`homingDirection`を取得します。

#### 返信

```
/homingDirection (int)motorID (int)homingDirection
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| homingDirection | int |  |  |

`homingDirection`

| 値 | 意味 |
| --- | --- |
| 1 | Forward |
| 0 | Reverse |
<!-- generated:end osc /getHomingDirection -->

<!-- osc: /setHomingSpeed -->
<!-- generated:begin osc /setHomingSpeed -->
### `/setHomingSpeed` (int)motorID (float)speed {#sethomingspeed}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| speed | float | 0-15610 step/s | 原点復帰の速度 |

#### 実行可能タイミング

常時

#### 説明

[`/homing`](homing.md#homing)実行時の原点復帰の速度`homingSpeed`を指定します。configToolからも指定できます。

範囲外の値は拒否されず、0〜15610に制限されます。

#### 初期値

- `speed`: 50（[driverSettings.homingSpeed](../connections/configuration-items.md#driversettings-homingspeed)）

#### 関連

[`/getHomingSpeed`](homing.md#gethomingspeed)
<!-- generated:end osc /setHomingSpeed -->

<!-- osc: /getHomingSpeed -->
<!-- generated:begin osc /getHomingSpeed -->
### `/getHomingSpeed` (int)motorID {#gethomingspeed}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

`homingSpeed`を取得します。

#### 返信

```
/homingSpeed (int)motorID (float)homingSpeed
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| homingSpeed | float | 0-15610 step/s | 原点復帰の速度 |
<!-- generated:end osc /getHomingSpeed -->

<!-- osc: /goUntil -->
<!-- generated:begin osc /goUntil -->
### `/goUntil` (int)motorID (bool)ACT (float)speed {#gountil}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| ACT | bool |  |  |
| speed | float | -15625-15625 step/s |  |

`ACT`

| 値 | 意味 |
| --- | --- |
| 0 | ABS_POSレジスタをリセットします |
| 1 | ABS_POSレジスタの内容をMARKレジスタにコピーします |

#### 実行可能タイミング

常時

#### 説明

指定の速度で回転し、HOMEスイッチがオンになるとACTの値に応じた処理を行います。  
その後softStopしますが、[`/setHomeSwMode`](home-and-limit-sensors.md#sethomeswmode)コマンドでSW_MODEが0に設定されていると、softStopではなくhardStopになります。このコマンドは、モータが停止するまでBUSY状態を保ちます。

速度の符号が方向になります。絶対値が範囲を超える速度は、ドライバライブラリによってレジスタの最大値（0xFFFFF、約15625step/s）に制限されます。

#### 変更

- **v2.2.0**: HOMEスイッチがオンの場合は、エラーの一覧にあるとおり`/error/command HomeSwActivating`として送信されます。以前は`HomeSwActivated`として送信されていました。他のコマンドのエラーと同じように、[`/reportError`](system-settings.md#reporterror)に従います。
- **v2.2.0**: サーボモードのモータには`/error/command InServoMode`を返し、何もしません。以前は、コマンドがドライバに送られていました。255のときは、サーボモードのモータだけがエラーを返し、他のモータはコマンドを実行します。

#### エラー

- `BrakeEngaged`: 電磁ブレーキが効いた状態のままモーションコマンドを送信した。ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`と`/homing`でも送信される（停止処理中と`/free`の後は除く）。
- `GoUntilTimeout`: `/goUntil`コマンド実行中にタイムアウトした。
- `HomeSwActivating`: HOMEスイッチがオンの状態から原点復帰方向に移動しようとした。HOMEスイッチがすでにオンのときの`/goUntil`と`/goUntilRaw`でも送信される。**v2.2.0**: `/goUntil`と`/goUntilRaw`が、HOMEスイッチがすでにオンのときに送信します。以前は`HomeSwActivated`として送信されていました。
- `InServoMode`: サーボモードでは実行できないコマンドを送信した。**v2.2.0**: `/goUntil`、`/goUntilRaw`、`/releaseSw`でも送信されます。

#### 関連

[`/setGoUntilTimeout`](homing.md#setgountiltimeout), [`/releaseSw`](homing.md#releasesw), [`/goUntilRaw`](motor-control.md#gountilraw)
<!-- generated:end osc /goUntil -->

<!-- osc: /setGoUntilTimeout -->
<!-- generated:begin osc /setGoUntilTimeout -->
### `/setGoUntilTimeout` (int)motorID (int)timeOut {#setgountiltimeout}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| timeOut | int | 0-2147483647 ms | タイムアウト時間 |

#### 実行可能タイミング

常時

#### 説明

[`/goUntil`](homing.md#gountil)実行時のタイムアウト時間を指定します。この時間内にスイッチがオンにならなかった場合にはtimeoutとして動作を中止します。0を指定するとタイムアウトが無効になります。configToolからも指定できます。

負の値には`CommandIgnored`を返し、何も適用されません。最大値は2147483647です。タイムアウトでの自動の即停止は、ドライバが無励磁のモータには送られません（タイムアウトのエラーは送信されます）。

#### 変更

- **v2.2.0**: 負の値には`/error/command CommandIgnored`を返し、何も適用されません。以前は約49日になっていました。
- **v2.2.0**: タイムアウト時の即停止は、ドライバが無励磁のモータには送りません。電磁ブレーキが無効でも同じです（即停止は無励磁のドライバを励磁してしまうため）。タイムアウトのエラーは送信されます。

#### エラー

- `CommandIgnored`: コマンドが実行可能なタイミングではない。タイミング参照。値がコマンドの範囲外のときにも送信され、何も適用されない（`/setPositionListReportInterval`のモータIDは255）。

#### 初期値

- `timeOut`: 10000（[driverSettings.goUntilTimeout](../connections/configuration-items.md#driversettings-gountiltimeout)）

#### 関連

[`/getGoUntilTimeout`](homing.md#getgountiltimeout)
<!-- generated:end osc /setGoUntilTimeout -->

<!-- osc: /getGoUntilTimeout -->
<!-- generated:begin osc /getGoUntilTimeout -->
### `/getGoUntilTimeout` (int)motorID {#getgountiltimeout}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

[`/goUntil`](homing.md#gountil)実行時のタイムアウト時間を取得します。

#### 返信

```
/goUntilTimeout (int)motorID (int)timeout
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| timeout | int | 0-2147483647 ms | タイムアウト時間 |
<!-- generated:end osc /getGoUntilTimeout -->

<!-- osc: /releaseSw -->
<!-- generated:begin osc /releaseSw -->
### `/releaseSw` (int)motorID (bool)ACT (bool)DIR {#releasesw}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| ACT | bool |  |  |
| DIR | bool |  |  |

`ACT`

| 値 | 意味 |
| --- | --- |
| 0 | ABS_POSレジスタをリセットします |
| 1 | ABS_POSレジスタの内容をMARKレジスタにコピーします |

`DIR`

| 値 | 意味 |
| --- | --- |
| 1 | 正転方向 |
| 0 | 逆転方向 |

#### 実行可能タイミング

常時

#### 説明

指定方向にminimum speed（初期状態では5[step/s]）で回転し、HOMEスイッチがオフになると、ACTの値に応じた処理を行います。ACTの処理内容は[`/goUntil`](homing.md#gountil)と同じです。その後hardStopします。

#### 変更

- **v2.2.0**: `ACT`は、他の真偽値の引数と同じように読まれます（1.0以上の数か、正の整数が真）。以前は整数として読まれていたため、0.5は0になっていました。
- **v2.2.0**: サーボモードのモータには`/error/command InServoMode`を返し、何もしません。以前は、コマンドがドライバに送られていました。255のときは、サーボモードのモータだけがエラーを返し、他のモータはコマンドを実行します。

#### エラー

- `BrakeEngaged`: 電磁ブレーキが効いた状態のままモーションコマンドを送信した。ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`と`/homing`でも送信される（停止処理中と`/free`の後は除く）。
- `ReleaseSwTimeout`: `/releaseSw`コマンド実行中にタイムアウトした。
- `InServoMode`: サーボモードでは実行できないコマンドを送信した。**v2.2.0**: `/goUntil`、`/goUntilRaw`、`/releaseSw`でも送信されます。

#### 関連

[`/setReleaseSwTimeout`](homing.md#setreleaseswtimeout), [`/setMinSpeed`](speed-profile.md#setminspeed)
<!-- generated:end osc /releaseSw -->

<!-- osc: /setReleaseSwTimeout -->
<!-- generated:begin osc /setReleaseSwTimeout -->
### `/setReleaseSwTimeout` (int)motorID (int)timeOut {#setreleaseswtimeout}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| timeOut | int | 0-2147483647 ms | タイムアウト時間 |

#### 実行可能タイミング

常時

#### 説明

[`/releaseSw`](homing.md#releasesw)実行時のタイムアウト時間を指定します。この時間内にスイッチがオフにならなかった場合にはtimeoutとして動作を中止します。0を指定するとタイムアウトが無効になります。configToolからも指定できます。

負の値には`CommandIgnored`を返し、何も適用されません。最大値は2147483647です。タイムアウトでの自動の即停止は、ドライバが無励磁のモータには送られません（タイムアウトのエラーは送信されます）。

#### 変更

- **v2.2.0**: 負の値には`/error/command CommandIgnored`を返し、何も適用されません。以前は約49日になっていました。
- **v2.2.0**: タイムアウト時の即停止は、ドライバが無励磁のモータには送りません。電磁ブレーキが無効でも同じです（即停止は無励磁のドライバを励磁してしまうため）。タイムアウトのエラーは送信されます。

#### エラー

- `CommandIgnored`: コマンドが実行可能なタイミングではない。タイミング参照。値がコマンドの範囲外のときにも送信され、何も適用されない（`/setPositionListReportInterval`のモータIDは255）。

#### 初期値

- `timeOut`: 10000（[driverSettings.releaseSwTimeout](../connections/configuration-items.md#driversettings-releaseswtimeout)）

#### 関連

[`/getReleaseSwTimeout`](homing.md#getreleaseswtimeout)
<!-- generated:end osc /setReleaseSwTimeout -->

<!-- osc: /getReleaseSwTimeout -->
<!-- generated:begin osc /getReleaseSwTimeout -->
### `/getReleaseSwTimeout` (int)motorID {#getreleaseswtimeout}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

[`/releaseSw`](homing.md#releasesw)実行時のタイムアウト時間を取得します。

#### 返信

```
/releaseSwTimeout (int)motorID (int)timeout
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| timeout | int | 0-2147483647 ms | タイムアウト時間 |
<!-- generated:end osc /getReleaseSwTimeout -->
