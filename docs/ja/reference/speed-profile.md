---
title: スピードプロファイル
---

# スピードプロファイル

スピードプロファイルと動作の仕組みは、[スピードプロファイルと動作](../guides/speed-profile-and-motions.md)をご覧ください。

<!-- osc: /setSpeedProfile -->
<!-- generated:begin osc /setSpeedProfile -->
### `/setSpeedProfile` (int)motorID (float)acc (float)dec (float)maxSpeed {#setspeedprofile}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| acc | float | 14.55-59575 step/s/s | 加速度 |
| dec | float | 14.55-59590（STEP400）、14.55-59575（STEP800）step/s/s | 減速度 |
| maxSpeed | float | 15.25-15610 step/s | 最大速度 |

#### 実行可能タイミング

モータ停止時

#### 説明

スピードプロファイルの加速度（`acc`）、減速度（`dec`）、最大速度（`maxSpeed`）をまとめて設定します。

スピードプロファイルは、モータドライバに書き込んでおく加速度・減速度・最大速度の組です。コマンドごとに送るものではなく、書き込んだ後のすべての動作（[`/run`](motor-control.md#run)、[`/goTo`](motor-control.md#goto)など）に使われます。最小速度は[`/setMinSpeed`](speed-profile.md#setminspeed)で別に設定します。

ACCとDECは最も近いレジスタ値に丸められるため、書き込まれる値は1LSBずれることがあります。MAX_SPEEDだけはいつでも書き込めますが、`MotorNotStopped`を返したモータには何も書き込まれません。範囲外の値は、ドライバライブラリによって制限されます。STEP400では、最大速度0は1として書き込まれます（レジスタ値0は予約されています）。

#### 変更

- **v2.2.0**: モータは停止中か無励磁でなければなりません。回転中のモータには`/error/command MotorNotStopped`を返し、元の値のままにします。
- **v2.2.0**: `acc`と`dec`は最も近いレジスタ値に丸められるため、書き込まれる値は1LSBずれることがあります。
- **v2.2.0**: STEP400: 最大速度0は1として書き込まれます（レジスタ値0は予約されています）。

#### エラー

- `MotorNotStopped`: 停止中か無励磁のときだけ書き込めるドライバのレジスタをコマンドが書き込もうとしたが、モータが回転していた。何も適用されない。v2.2.0で追加。

#### 初期値

- `acc`: 1000（ファームウェア）、2000（テンプレート）（[speedProfile.acc](../connections/configuration-items.md#speedprofile-acc)）
- `dec`: 1000（ファームウェア）、2000（テンプレート）（[speedProfile.dec](../connections/configuration-items.md#speedprofile-dec)）
- `maxSpeed`: 650（ファームウェア）、620（テンプレート）（[speedProfile.maxSpeed](../connections/configuration-items.md#speedprofile-maxspeed)）

#### 関連

[`/getSpeedProfile`](speed-profile.md#getspeedprofile), [`/setAcc`](speed-profile.md#setacc), [`/setDec`](speed-profile.md#setdec), [`/setMaxSpeed`](speed-profile.md#setmaxspeed)
<!-- generated:end osc /setSpeedProfile -->

<!-- osc: /getSpeedProfile -->
<!-- generated:begin osc /getSpeedProfile -->
### `/getSpeedProfile` (int)motorID {#getspeedprofile}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

スピードプロファイルのacc, dec, maxSpeedをまとめて取得します。

#### 変更

- **v2.2.0**: 加速度と減速度の返信値が、以前より約4.9% 小さくなりました。データシートに一致する値になっています（ドライバライブラリv1.2.0）。

#### 返信

```
/speedProfile (int)motorID (float)acc (float)dec (float)maxSpeed
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| acc | float | 14.55-59590 step/s/s | 加速度 |
| dec | float | 14.55-59590 step/s/s | 減速度 |
| maxSpeed | float | 15.25-15610 step/s | 最大速度 |
<!-- generated:end osc /getSpeedProfile -->

<!-- osc: /setFullstepSpeed -->
<!-- generated:begin osc /setFullstepSpeed -->
### `/setFullstepSpeed` (int)motorID (float)fullstepSpeed {#setfullstepspeed}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| fullstepSpeed | float | 7.63-15625 step/s | 切り替わる閾値 |

#### 実行可能タイミング

常時

#### 説明

マイクロステップモードが自動でフルステップモードに切り替わる閾値を設定します。

範囲を超える値は、ドライバライブラリによって15625step/sに制限されます。0から範囲の下限までの値は、下限（7.63step/s）として書き込まれます。-7.6程度より小さい負の値は下限に制限されません。ドライバライブラリが大きな符号なしの数に変換してから最大値に制限するため、15625step/sになります。

#### 初期値

- `fullstepSpeed`: 15610（ファームウェア）、15625（テンプレート）（[speedProfile.fullStepSpeed](../connections/configuration-items.md#speedprofile-fullstepspeed)）

#### 関連

[`/getFullstepSpeed`](speed-profile.md#getfullstepspeed)
<!-- generated:end osc /setFullstepSpeed -->

<!-- osc: /getFullstepSpeed -->
<!-- generated:begin osc /getFullstepSpeed -->
### `/getFullstepSpeed` (int)motorID {#getfullstepspeed}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

マイクロステップモードが自動でフルステップモードに切り替わる閾値を取得します。

#### 返信

```
/fullstepSpeed (int)motorID (float)fullstepSpeed
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| fullstepSpeed | float | 7.63-15625 step/s | 切り替わる閾値 |
<!-- generated:end osc /getFullstepSpeed -->

<!-- osc: /setMaxSpeed -->
<!-- generated:begin osc /setMaxSpeed -->
### `/setMaxSpeed` (int)motorID (float)maxSpeed {#setmaxspeed}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| maxSpeed | float | 15.25-15610 step/s | 最大速度 |

#### 実行可能タイミング

常時

#### 説明

スピードプロファイルの最大速度を設定します。

範囲外の値は、ドライバライブラリによって制限されます。STEP400では、最大速度0は1として書き込まれます（レジスタ値0は予約されています）。

#### 変更

- **v2.2.0**: STEP400: 最大速度0は1として書き込まれます（レジスタ値0は予約されています）。STEP800は変わりません。

#### 初期値

- `maxSpeed`: 650（ファームウェア）、620（テンプレート）（[speedProfile.maxSpeed](../connections/configuration-items.md#speedprofile-maxspeed)）

#### 関連

[`/setSpeedProfile`](speed-profile.md#setspeedprofile)
<!-- generated:end osc /setMaxSpeed -->

<!-- osc: /setAcc -->
<!-- generated:begin osc /setAcc -->
### `/setAcc` (int)motorID (float)acc {#setacc}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| acc | float | 14.55-59575 step/s/s | 加速度 |

#### 実行可能タイミング

モータ停止時

#### 説明

スピードプロファイルの加速度を設定します。

最も近いレジスタ値に丸められるため、書き込まれる値は1LSBずれることがあります。範囲外の値は、ドライバライブラリによって制限されます。

モータは停止中か無励磁でなければなりません。回転中のモータには`MotorNotStopped`を返し、元の値のままにします。

#### 変更

- **v2.2.0**: モータは停止中か無励磁でなければなりません。回転中のモータには`/error/command MotorNotStopped`を返し、元の値のままにします。
- **v2.2.0**: 最も近いレジスタ値に丸められるため、書き込まれる値は1LSBずれることがあります。

#### エラー

- `MotorNotStopped`: 停止中か無励磁のときだけ書き込めるドライバのレジスタをコマンドが書き込もうとしたが、モータが回転していた。何も適用されない。v2.2.0で追加。

#### 初期値

- `acc`: 1000（ファームウェア）、2000（テンプレート）（[speedProfile.acc](../connections/configuration-items.md#speedprofile-acc)）

#### 関連

[`/setSpeedProfile`](speed-profile.md#setspeedprofile)
<!-- generated:end osc /setAcc -->

<!-- osc: /setDec -->
<!-- generated:begin osc /setDec -->
### `/setDec` (int)motorID (float)dec {#setdec}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| dec | float | 14.55-59590（STEP400）、14.55-59575（STEP800）step/s/s | 減速度 |

#### 実行可能タイミング

モータ停止時

#### 説明

スピードプロファイルの減速度（deceleration）を設定します。

最も近いレジスタ値に丸められるため、書き込まれる値は1LSBずれることがあります。範囲外の値は、ドライバライブラリによって制限されます。

モータは停止中か無励磁でなければなりません。回転中のモータには`MotorNotStopped`を返し、元の値のままにします。

#### 変更

- **v2.2.0**: モータは停止中か無励磁でなければなりません。回転中のモータには`/error/command MotorNotStopped`を返し、元の値のままにします。
- **v2.2.0**: 最も近いレジスタ値に丸められるため、書き込まれる値は1LSBずれることがあります。

#### エラー

- `MotorNotStopped`: 停止中か無励磁のときだけ書き込めるドライバのレジスタをコマンドが書き込もうとしたが、モータが回転していた。何も適用されない。v2.2.0で追加。

#### 初期値

- `dec`: 1000（ファームウェア）、2000（テンプレート）（[speedProfile.dec](../connections/configuration-items.md#speedprofile-dec)）

#### 関連

[`/setSpeedProfile`](speed-profile.md#setspeedprofile)
<!-- generated:end osc /setDec -->

<!-- osc: /setMinSpeed -->
<!-- generated:begin osc /setMinSpeed -->
### `/setMinSpeed` (int)motorID (float)minSpeed {#setminspeed}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| minSpeed | float | 0-976.3 step/s | 最小速度 |

#### 実行可能タイミング

モータ停止時

#### 説明

スピードプロファイルの最小速度を設定します。この値は[`/releaseSw`](homing.md#releasesw)時のモータ回転速度にも使用されます。Low speed optimization（[`/enableLowSpeedOptimize`](motor-driver-settings.md#enablelowspeedoptimize)）が有効になっている場合、minSpeedは強制的に0になります。

低速最適化が無効の間は、モータは停止中か無励磁でなければなりません。回転中のモータには`MotorNotStopped`を返し、元の値のままにします。有効の間は、保存される値だけが変わり、エラーは送信されません。

範囲を超える値は、ドライバライブラリによって976.3step/sに制限されます。-0.24程度より小さい負の値は0に制限されません。ドライバライブラリが大きな符号なしの数に変換してから最大値に制限するため、976.3step/sになります。

#### 変更

- **v2.2.0**: 低速最適化が無効の間は、モータは停止中か無励磁でなければなりません。回転中のモータには`/error/command MotorNotStopped`を返し、元の値のままにします。
- **v2.2.0**: `/setMinSpeed 255`（全モータ）は、モータごとに低速最適化の設定を確認します。以前は、不正な配列の要素を読んでいました。

#### エラー

- `MotorNotStopped`: 停止中か無励磁のときだけ書き込めるドライバのレジスタをコマンドが書き込もうとしたが、モータが回転していた。何も適用されない。v2.2.0で追加。

#### 初期値

- `minSpeed`: 0（[speedProfile.minSpeed](../connections/configuration-items.md#speedprofile-minspeed)）

#### 関連

[`/getMinSpeed`](speed-profile.md#getminspeed)
<!-- generated:end osc /setMinSpeed -->

<!-- osc: /getMinSpeed -->
<!-- generated:begin osc /getMinSpeed -->
### `/getMinSpeed` (int)motorID {#getminspeed}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

スピードプロファイルの最小速度を返します。

低速最適化が有効なモータでは0.0を返します。このときMIN_SPEEDレジスタには最適化の閾値が入っていて（[`/getLowSpeedOptimizeThreshold`](motor-driver-settings.md#getlowspeedoptimizethreshold)で読み出せます）、実際の最小速度は0です。低速最適化が無効のモータでは、ドライバのMIN_SPEEDレジスタの値をstep/sで返します。

#### 変更

- **v2.2.0**: 低速最適化が有効なモータでは0.0を返します。以前は、1つのモータではMIN_SPEEDレジスタの値（閾値）を返し、`255`（全モータ）では保存されている最小速度の設定を返していました。今はどちらも同じ動作です。

#### 返信

```
/minSpeed (int)motorID (float)minSpeed
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| minSpeed | float | 0-976.3 step/s | 最小速度 |
<!-- generated:end osc /getMinSpeed -->

<!-- osc: /getSpeed -->
<!-- generated:begin osc /getSpeed -->
### `/getSpeed` (int)motorID {#getspeed}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

モータの現在の速度を返します。

#### 返信

```
/speed (int)motorID (float)speed
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| speed | float | -15625-15625 step/s | 現在の速度 |
<!-- generated:end osc /getSpeed -->

## Rawレジスタ値のコマンド

以下のコマンドは、単位を換算しない、ドライバICのレジスタ値そのままで、スピードプロファイルのパラメータを設定・取得します。ほとんどの場合は、標準のコマンド（単位つきの値で指定するもの）をお勧めします。これらは、レジスタを直接制御したい場合のコマンドです。

<!-- osc: /setSpeedProfileRaw -->
<!-- generated:begin osc /setSpeedProfileRaw -->
### `/setSpeedProfileRaw` (int)motorID (int)acc (int)dec (int)maxSpeed {#setspeedprofileraw}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| acc | int | 0-4095 | 加速度（Rawレジスタ値） |
| dec | int | 0-4095 | 減速度（Rawレジスタ値） |
| maxSpeed | int | 0-1023 | 最大速度（Rawレジスタ値） |

#### 実行可能タイミング

モータ停止時

#### 説明

ドライバICのレジスタ値（Raw）で、スピードプロファイルのacc, dec, maxSpeedを設定します。

範囲外の値は拒否されません。16ビットに変換され（70000は4464になります）、さらにドライバがレジスタの幅でマスクします。モータは停止中か無励磁でなければなりません。回転中のモータには`MotorNotStopped`を返し、元の値のままにします。

#### 変更

- **v2.2.0**: 保存される設定（`/saveConfig`）と、`/resetMotorDriver`で再び適用される加速度、減速度、最大速度の設定も変更します。以前はレジスタだけを変更していたため、リセットや保存した設定で元の値に戻っていました。
- **v2.2.0**: モータは停止中か無励磁でなければなりません。回転中のモータには`/error/command MotorNotStopped`を返し、元の値のままにします。

#### エラー

- `MotorNotStopped`: 停止中か無励磁のときだけ書き込めるドライバのレジスタをコマンドが書き込もうとしたが、モータが回転していた。何も適用されない。v2.2.0で追加。

#### 関連

[`/getSpeedProfileRaw`](speed-profile.md#getspeedprofileraw), [`/setSpeedProfile`](speed-profile.md#setspeedprofile)
<!-- generated:end osc /setSpeedProfileRaw -->

<!-- osc: /getSpeedProfileRaw -->
<!-- generated:begin osc /getSpeedProfileRaw -->
### `/getSpeedProfileRaw` (int)motorID {#getspeedprofileraw}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

ドライバICのレジスタ値（Raw）で、スピードプロファイルのacc, dec, maxSpeedを取得します。

#### 返信

```
/speedProfileRaw (int)motorID (int)acc (int)dec (int)maxSpeed
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| acc | int | 0-4095 | 加速度（Rawレジスタ値） |
| dec | int | 0-4095 | 減速度（Rawレジスタ値） |
| maxSpeed | int | 0-1023 | 最大速度（Rawレジスタ値） |
<!-- generated:end osc /getSpeedProfileRaw -->

<!-- osc: /setMaxSpeedRaw -->
<!-- generated:begin osc /setMaxSpeedRaw -->
### `/setMaxSpeedRaw` (int)motorID (int)maxSpeed {#setmaxspeedraw}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| maxSpeed | int | 0-1023 | 最大速度（Rawレジスタ値） |

#### 実行可能タイミング

常時

#### 説明

レジスタ値（Raw）で、スピードプロファイルの最大速度を設定します。

範囲外の値は拒否されません。16ビットに変換され（70000は4464になります）、さらにドライバがレジスタの幅でマスクします。

`/setMaxSpeedRaw 0`は、STEP400でも0を書き込みます。

#### 変更

- **v2.2.0**: 保存される設定（`/saveConfig`）と、`/resetMotorDriver`で再び適用される最大速度の設定も変更します。以前はレジスタだけを変更していたため、リセットや保存した設定で元の値に戻っていました。

#### 関連

[`/setMaxSpeed`](speed-profile.md#setmaxspeed)
<!-- generated:end osc /setMaxSpeedRaw -->

<!-- osc: /setMinSpeedRaw -->
<!-- generated:begin osc /setMinSpeedRaw -->
### `/setMinSpeedRaw` (int)motorID (int)minSpeed {#setminspeedraw}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| minSpeed | int | 0-4095 | 最小速度（Rawレジスタ値） |

#### 実行可能タイミング

モータ停止時

#### 説明

レジスタ値（Raw）で、スピードプロファイルの最小速度を設定します。

範囲外の値は拒否されません。16ビットに変換され（70000は4464になります）、さらにドライバがレジスタの幅でマスクします。低速最適化が無効の間は、モータは停止中か無励磁でなければなりません。回転中のモータには`MotorNotStopped`を返し、元の値のままにします。有効の間は、保存される値だけが変わり、エラーは送信されません。

#### 変更

- **v2.2.0**: 保存される設定（`/saveConfig`）と、`/resetMotorDriver`で再び適用される最小速度の設定も変更します。以前はレジスタだけを変更していたため、リセットや保存した設定で元の値に戻っていました。
- **v2.2.0**: 低速最適化が無効の間は、モータは停止中か無励磁でなければなりません。回転中のモータには`/error/command MotorNotStopped`を返し、元の値のままにします。
- **v2.2.0**: ビット12は無視されます（以前は、[`/enableLowSpeedOptimize`](motor-driver-settings.md#enablelowspeedoptimize)なしで低速最適化が有効になっていました）。低速最適化が有効の間は、[`/setMinSpeed`](speed-profile.md#setminspeed)と同じく、保存される値だけを変更します。

#### エラー

- `MotorNotStopped`: 停止中か無励磁のときだけ書き込めるドライバのレジスタをコマンドが書き込もうとしたが、モータが回転していた。何も適用されない。v2.2.0で追加。

#### 関連

[`/setMinSpeed`](speed-profile.md#setminspeed)
<!-- generated:end osc /setMinSpeedRaw -->

<!-- osc: /setFullstepSpeedRaw -->
<!-- generated:begin osc /setFullstepSpeedRaw -->
### `/setFullstepSpeedRaw` (int)motorID (int)fullstepSpeed {#setfullstepspeedraw}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| fullstepSpeed | int | 0-1023 | フルステップ速度の閾値（Rawレジスタ値） |

#### 実行可能タイミング

常時

#### 説明

レジスタ値（Raw）で、フルステップに切り替わる速度の閾値を設定します。

範囲外の値は拒否されません。16ビットに変換され（70000は4464になります）、さらにドライバがレジスタの幅でマスクします。

#### 変更

- **v2.2.0**: 保存される設定（`/saveConfig`）と、`/resetMotorDriver`で再び適用されるフルステップ速度の設定も変更します。以前はレジスタだけを変更していたため、リセットや保存した設定で元の値に戻っていました。

#### 関連

[`/setFullstepSpeed`](speed-profile.md#setfullstepspeed)
<!-- generated:end osc /setFullstepSpeedRaw -->

<!-- osc: /setAccRaw -->
<!-- generated:begin osc /setAccRaw -->
### `/setAccRaw` (int)motorID (int)acc {#setaccraw}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| acc | int | 0-4095 | 加速度（Rawレジスタ値） |

#### 実行可能タイミング

モータ停止時

#### 説明

レジスタ値（Raw）で、スピードプロファイルの加速度を設定します。

範囲外の値は拒否されません。16ビットに変換され（70000は4464になります）、さらにドライバがレジスタの幅でマスクします。モータは停止中か無励磁でなければなりません。回転中のモータには`MotorNotStopped`を返し、元の値のままにします。

#### 変更

- **v2.2.0**: 保存される設定（`/saveConfig`）と、`/resetMotorDriver`で再び適用される加速度の設定も変更します。以前はレジスタだけを変更していたため、リセットや保存した設定で元の値に戻っていました。
- **v2.2.0**: モータは停止中か無励磁でなければなりません。回転中のモータには`/error/command MotorNotStopped`を返し、元の値のままにします。

#### エラー

- `MotorNotStopped`: 停止中か無励磁のときだけ書き込めるドライバのレジスタをコマンドが書き込もうとしたが、モータが回転していた。何も適用されない。v2.2.0で追加。

#### 関連

[`/setAcc`](speed-profile.md#setacc)
<!-- generated:end osc /setAccRaw -->

<!-- osc: /setDecRaw -->
<!-- generated:begin osc /setDecRaw -->
### `/setDecRaw` (int)motorID (int)dec {#setdecraw}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| dec | int | 0-4095 | 減速度（Rawレジスタ値） |

#### 実行可能タイミング

モータ停止時

#### 説明

レジスタ値（Raw）で、スピードプロファイルの減速度を設定します。

範囲外の値は拒否されません。16ビットに変換され（70000は4464になります）、さらにドライバがレジスタの幅でマスクします。モータは停止中か無励磁でなければなりません。回転中のモータには`MotorNotStopped`を返し、元の値のままにします。

#### 変更

- **v2.2.0**: 保存される設定（`/saveConfig`）と、`/resetMotorDriver`で再び適用される減速度の設定も変更します。以前はレジスタだけを変更していたため、リセットや保存した設定で元の値に戻っていました。
- **v2.2.0**: モータは停止中か無励磁でなければなりません。回転中のモータには`/error/command MotorNotStopped`を返し、元の値のままにします。

#### エラー

- `MotorNotStopped`: 停止中か無励磁のときだけ書き込めるドライバのレジスタをコマンドが書き込もうとしたが、モータが回転していた。何も適用されない。v2.2.0で追加。

#### 関連

[`/setDec`](speed-profile.md#setdec)
<!-- generated:end osc /setDecRaw -->
