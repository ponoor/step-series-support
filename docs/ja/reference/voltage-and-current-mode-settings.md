---
title: 電圧モードと電流モード
---

# 電圧モードと電流モード

KVALとTVALの決め方は、[電圧モードと電流モード](../guides/voltage-and-current-mode.md)をご覧ください。

## 電圧モード

<!-- osc: /setVoltageMode -->
<!-- generated:begin osc /setVoltageMode -->
### `/setVoltageMode` (int)motorID {#setvoltagemode}

STEP400のみ。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

無励磁状態

#### 説明

指定したモータを電圧モードに切り替えます。STEP800は常に電圧モードで動作しますので、この切替コマンドはSTEP400のみ利用可能です。

#### 変更

- **v2.2.0**: 出力は無励磁でなければなりません。そうでないときは`/error/command MotorNotHiZ`を返し、何も適用されません。
- **v2.2.0**: ドライバがモードを受け付けたとき（STEP_MODEを読み戻して確認します）だけモードを変更します。そうでないときは`/error/command CommandIgnored`を返します。以前は、ドライバが元のモードのままなのに保存されるモードだけが変わっていたため、その後の[`/setKval`](voltage-and-current-mode-settings.md#setkval)と[`/setTval`](voltage-and-current-mode-settings.md#settval)が誤ったレジスタに書き込んでいました。

#### エラー

- `MotorNotHiZ`: ドライバのレジスタのうち、出力が無励磁のときだけ書き込めるものをコマンドが書き込もうとしたが、モータが無励磁ではなかった。励磁して位置を保っているモータは無励磁ではない。先に`/softHiZ`か`/hardHiZ`を送る。何も適用されない。v2.2.0で追加。
- `CommandIgnored`: コマンドが実行可能なタイミングではない。タイミング参照。値がコマンドの範囲外のときにも送信され、何も適用されない（`/setPositionListReportInterval`のモータIDは255）。

#### 関連

[`/setCurrentMode`](voltage-and-current-mode-settings.md#setcurrentmode)
<!-- generated:end osc /setVoltageMode -->

<!-- osc: /setKval -->
<!-- generated:begin osc /setKval -->
### `/setKval` (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)decKVAL {#setkval}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| holdKVAL | int | 0-255 | 停止時のKVAL |
| runKVAL | int | 0-255 | 一定速運転時のKVAL |
| accKVAL | int | 0-255 | 加速時のKVAL |
| decKVAL | int | 0-255 | 減速時のKVAL |

#### 実行可能タイミング

常時

#### 説明

KVAL4種をまとめて設定します。

0〜255の範囲外の値は拒否されず、0〜255に制限されます。

STEP400の電流モードでは、保存される設定だけが変わります。[`/setVoltageMode`](voltage-and-current-mode-settings.md#setvoltagemode)でレジスタに書き込まれます。

#### 初期値

- `holdKVAL`: 0（[voltageMode.KVAL_HOLD](../connections/configuration-items.md#voltagemode-kval_hold)）
- `runKVAL`: 16（[voltageMode.KVAL_RUN](../connections/configuration-items.md#voltagemode-kval_run)）
- `accKVAL`: 16（[voltageMode.KVAL_ACC](../connections/configuration-items.md#voltagemode-kval_acc)）
- `decKVAL`: 16（[voltageMode.KVAL_DEC](../connections/configuration-items.md#voltagemode-kval_dec)）

#### 関連

[`/getKval`](voltage-and-current-mode-settings.md#getkval), [`/setHoldKval`](voltage-and-current-mode-settings.md#setholdkval), [`/setRunKval`](voltage-and-current-mode-settings.md#setrunkval), [`/setAccKval`](voltage-and-current-mode-settings.md#setacckval), [`/setDecKval`](voltage-and-current-mode-settings.md#setdeckval)
<!-- generated:end osc /setKval -->

<!-- osc: /getKval -->
<!-- generated:begin osc /getKval -->
### `/getKval` (int)motorID {#getkval}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

KVAL4種をまとめて取得します。

電磁ブレーキが有効で電圧モードのとき、モータが再び励磁されるたびに（保持、保持への移行中、`/free`の後から）KVAL_HOLDがKVAL_RUNの半分以上に引き上げられ、このコマンドは引き上げられた値を返します。電流モードでは、代わりにTVAL_HOLDが引き上げられます。

#### 変更

- **v2.2.0**: ドライバのレジスタではなく、設定（[`/setKval`](voltage-and-current-mode-settings.md#setkval)で設定し、`/saveConfig`で保存される値）を返します。電流モードではKVALのレジスタは以前の値のままで、電圧モードではレジスタの値です。電磁ブレーキのモータで引き上げられたKVAL_HOLDも返されます。STEP800の返信は以前と同じです。

#### 返信

```
/kval (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)decKVAL
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| holdKVAL | int | 0-255 | 停止時のKVAL |
| runKVAL | int | 0-255 | 一定速運転時のKVAL |
| accKVAL | int | 0-255 | 加速時のKVAL |
| decKVAL | int | 0-255 | 減速時のKVAL |
<!-- generated:end osc /getKval -->

<!-- osc: /setBemfParam -->
<!-- generated:begin osc /setBemfParam -->
### `/setBemfParam` (int)motorID (int)INT_SPEED (int)ST_SLP (int)FN_SLP_ACC (int)FN_SLP_DEC {#setbemfparam}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| INT_SPEED | int | 0-16383 | INT_SPEEDレジスタの値 |
| ST_SLP | int | 0-255 | ST_SLPレジスタの値 |
| FN_SLP_ACC | int | 0-255 | FN_SLP_ACCレジスタの値 |
| FN_SLP_DEC | int | 0-255 | FN_SLP_DECレジスタの値 |

#### 実行可能タイミング

無励磁状態

#### 説明

BEMF補償パラメータのレジスタを設定します。各レジスタの設定値については電圧モードの設定を参照してください。

出力は無励磁でなければなりません。そうでないときは`MotorNotHiZ`を返し、何も適用されません。

範囲外の値は拒否されません。INT_SPEEDは0〜16383に、他のパラメータは0〜255に制限されます。

#### 変更

- **v2.2.0**: 出力は無励磁でなければなりません（INT_SPEED、ST_SLP、FN_SLP_ACC、FN_SLP_DECは無励磁のときだけ書き込めます）。そうでないときは`/error/command MotorNotHiZ`を返し、何も適用されません。

#### エラー

- `MotorNotHiZ`: ドライバのレジスタのうち、出力が無励磁のときだけ書き込めるものをコマンドが書き込もうとしたが、モータが無励磁ではなかった。励磁して位置を保っているモータは無励磁ではない。先に`/softHiZ`か`/hardHiZ`を送る。何も適用されない。v2.2.0で追加。

#### 初期値

- `INT_SPEED`: 1032（[voltageMode.INT_SPEED](../connections/configuration-items.md#voltagemode-int_speed)）
- `ST_SLP`: 25（[voltageMode.ST_SLP](../connections/configuration-items.md#voltagemode-st_slp)）
- `FN_SLP_ACC`: 41（[voltageMode.FN_SLP_ACC](../connections/configuration-items.md#voltagemode-fn_slp_acc)）
- `FN_SLP_DEC`: 41（[voltageMode.FN_SLP_DEC](../connections/configuration-items.md#voltagemode-fn_slp_dec)）

#### 関連

[`/getBemfParam`](voltage-and-current-mode-settings.md#getbemfparam)
<!-- generated:end osc /setBemfParam -->

<!-- osc: /getBemfParam -->
<!-- generated:begin osc /getBemfParam -->
### `/getBemfParam` (int)motorID {#getbemfparam}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

BEMFパラメータを設定するレジスタ値を取得します。

#### 返信

```
/bemfParam (int)motorID (int)INT_SPEED (int)ST_SLP (int)FN_SLP_ACC (int)FN_SLP_DEC
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| INT_SPEED | int | 0-16383 | INT_SPEEDレジスタの値 |
| ST_SLP | int | 0-255 | ST_SLPレジスタの値 |
| FN_SLP_ACC | int | 0-255 | FN_SLP_ACCレジスタの値 |
| FN_SLP_DEC | int | 0-255 | FN_SLP_DECレジスタの値 |
<!-- generated:end osc /getBemfParam -->

<!-- osc: /setHoldKval -->
<!-- generated:begin osc /setHoldKval -->
### `/setHoldKval` (int)motorID (int)holdKVAL {#setholdkval}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| holdKVAL | int | 0-255 | 停止時のKVAL |

#### 実行可能タイミング

常時

#### 説明

停止時のKVALのみを設定します。

0〜255の範囲外の値は拒否されず、0〜255に制限されます。

STEP400の電流モードでは、保存される設定だけが変わります。[`/setVoltageMode`](voltage-and-current-mode-settings.md#setvoltagemode)でレジスタに書き込まれます。

#### 初期値

- `holdKVAL`: 0（[voltageMode.KVAL_HOLD](../connections/configuration-items.md#voltagemode-kval_hold)）

#### 関連

[`/setKval`](voltage-and-current-mode-settings.md#setkval)
<!-- generated:end osc /setHoldKval -->

<!-- osc: /setRunKval -->
<!-- generated:begin osc /setRunKval -->
### `/setRunKval` (int)motorID (int)runKVAL {#setrunkval}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| runKVAL | int | 0-255 | 一定速運転時のKVAL |

#### 実行可能タイミング

常時

#### 説明

一定速運転時のKVALのみを設定します。

0〜255の範囲外の値は拒否されず、0〜255に制限されます。

STEP400の電流モードでは、保存される設定だけが変わります。[`/setVoltageMode`](voltage-and-current-mode-settings.md#setvoltagemode)でレジスタに書き込まれます。

#### 初期値

- `runKVAL`: 16（[voltageMode.KVAL_RUN](../connections/configuration-items.md#voltagemode-kval_run)）

#### 関連

[`/setKval`](voltage-and-current-mode-settings.md#setkval)
<!-- generated:end osc /setRunKval -->

<!-- osc: /setAccKval -->
<!-- generated:begin osc /setAccKval -->
### `/setAccKval` (int)motorID (int)accKVAL {#setacckval}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| accKVAL | int | 0-255 | 加速時のKVAL |

#### 実行可能タイミング

常時

#### 説明

加速時のKVALのみを設定します。

0〜255の範囲外の値は拒否されず、0〜255に制限されます。

STEP400の電流モードでは、保存される設定だけが変わります。[`/setVoltageMode`](voltage-and-current-mode-settings.md#setvoltagemode)でレジスタに書き込まれます。

#### 初期値

- `accKVAL`: 16（[voltageMode.KVAL_ACC](../connections/configuration-items.md#voltagemode-kval_acc)）

#### 関連

[`/setKval`](voltage-and-current-mode-settings.md#setkval)
<!-- generated:end osc /setAccKval -->

<!-- osc: /setDecKval -->
<!-- generated:begin osc /setDecKval -->
### `/setDecKval` (int)motorID (int)decKVAL {#setdeckval}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| decKVAL | int | 0-255 | 減速時のKVAL |

#### 実行可能タイミング

常時

#### 説明

減速時のKVALのみを設定します。

0〜255の範囲外の値は拒否されず、0〜255に制限されます。

STEP400の電流モードでは、保存される設定だけが変わります。[`/setVoltageMode`](voltage-and-current-mode-settings.md#setvoltagemode)でレジスタに書き込まれます。

#### 初期値

- `decKVAL`: 16（[voltageMode.KVAL_DEC](../connections/configuration-items.md#voltagemode-kval_dec)）

#### 関連

[`/setKval`](voltage-and-current-mode-settings.md#setkval)
<!-- generated:end osc /setDecKval -->

## 電流モード

<!-- osc: /setCurrentMode -->
<!-- generated:begin osc /setCurrentMode -->
### `/setCurrentMode` (int)motorID {#setcurrentmode}

STEP400のみ。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

無励磁状態

#### 説明

指定したモータを電流モードに切り替えます。

PowerSTEP01の電流モードは1/16マイクロステップまでです。それより細かいマイクロステップモードは1/16に下げられ、保存されている設定（[`/setMicrostepMode`](motor-driver-settings.md#setmicrostepmode)、`driverSettings.stepMode`）も一緒に変わります。

#### 変更

- **v2.2.0**: 出力は無励磁でなければなりません。そうでないときは`/error/command MotorNotHiZ`を返し、何も適用されません。
- **v2.2.0**: ドライバがモードを受け付けたとき（STEP_MODEを読み戻して確認します）だけモードを変更します。そうでないときは`/error/command CommandIgnored`を返します。以前は、ドライバが元のモードのままなのに保存されるモードだけが変わっていたため、その後の[`/setKval`](voltage-and-current-mode-settings.md#setkval)と[`/setTval`](voltage-and-current-mode-settings.md#settval)が誤ったレジスタに書き込んでいました。

#### エラー

- `MotorNotHiZ`: ドライバのレジスタのうち、出力が無励磁のときだけ書き込めるものをコマンドが書き込もうとしたが、モータが無励磁ではなかった。励磁して位置を保っているモータは無励磁ではない。先に`/softHiZ`か`/hardHiZ`を送る。何も適用されない。v2.2.0で追加。
- `CommandIgnored`: コマンドが実行可能なタイミングではない。タイミング参照。値がコマンドの範囲外のときにも送信され、何も適用されない（`/setPositionListReportInterval`のモータIDは255）。

#### 関連

[`/setVoltageMode`](voltage-and-current-mode-settings.md#setvoltagemode), [`/setMicrostepMode`](motor-driver-settings.md#setmicrostepmode)
<!-- generated:end osc /setCurrentMode -->

<!-- osc: /setTval -->
<!-- generated:begin osc /setTval -->
### `/setTval` (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL {#settval}

STEP400のみ。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| holdTVAL | int | 0-64 | 停止時のTVAL |
| runTVAL | int | 0-64 | 一定速運転時のTVAL |
| accTVAL | int | 0-64 | 加速時のTVAL |
| decTVAL | int | 0-64 | 減速時のTVAL |

#### 実行可能タイミング

常時

#### 説明

TVAL4種をまとめて設定します。

STEP400では、TVALは以下のようになっています。

0〜64の範囲外の値は拒否されず、0〜64に制限されます。上限の64（約5A）はファームウェアの安全上の上限です。

電圧モードでは、保存される設定だけが変わります。[`/setCurrentMode`](voltage-and-current-mode-settings.md#setcurrentmode)でレジスタに書き込まれます。

#### 初期値

- `holdTVAL`: 0（[currentMode.TVAL_HOLD](../connections/configuration-items.md#currentmode-tval_hold)）
- `runTVAL`: 16（[currentMode.TVAL_RUN](../connections/configuration-items.md#currentmode-tval_run)）
- `accTVAL`: 16（[currentMode.TVAL_ACC](../connections/configuration-items.md#currentmode-tval_acc)）
- `decTVAL`: 16（[currentMode.TVAL_DEC](../connections/configuration-items.md#currentmode-tval_dec)）

| TVAL | 設定値[mA] |
| --- | --- |
| 0 | 78mA |
| 1 | 156mA |
| ... | ... |
| 127 | 9,984mA |

#### 関連

[`/getTval`](voltage-and-current-mode-settings.md#gettval), [`/getTval_mA`](voltage-and-current-mode-settings.md#gettval_ma), [`/setHoldTval`](voltage-and-current-mode-settings.md#setholdtval), [`/setRunTval`](voltage-and-current-mode-settings.md#setruntval), [`/setAccTval`](voltage-and-current-mode-settings.md#setacctval), [`/setDecTval`](voltage-and-current-mode-settings.md#setdectval)
<!-- generated:end osc /setTval -->

<!-- osc: /getTval -->
<!-- generated:begin osc /getTval -->
### `/getTval` (int)motorID {#gettval}

STEP400のみ。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

TVAL4種をまとめて取得します。

電磁ブレーキが有効で電流モードのとき、モータが再び励磁されるたびに（保持、保持への移行中、`/free`の後から）TVAL_HOLDがTVAL_RUNの半分以上に引き上げられ、このコマンドは引き上げられた値を返します。電圧モードでは、代わりにKVAL_HOLDが引き上げられます。

#### 変更

- **v2.2.0**: ドライバのレジスタではなく、設定（[`/setTval`](voltage-and-current-mode-settings.md#settval)で設定し、`/saveConfig`で保存される値）を返します。電圧モードではTVALのレジスタは以前の値のままです。電磁ブレーキのモータで引き上げられたTVAL_HOLDも返されます。

#### 返信

STEP400のみ。

```
/tval (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| holdTVAL | int | 0-64 | 停止時のTVAL |
| runTVAL | int | 0-64 | 一定速運転時のTVAL |
| accTVAL | int | 0-64 | 加速時のTVAL |
| decTVAL | int | 0-64 | 減速時のTVAL |

#### 関連

[`/getTval_mA`](voltage-and-current-mode-settings.md#gettval_ma)
<!-- generated:end osc /getTval -->

<!-- osc: /getTval_mA -->
<!-- generated:begin osc /getTval_mA -->
### `/getTval_mA` (int)motorID {#gettval_ma}

STEP400のみ。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

TVAL4種をまとめて取得します。レジスタの値ではなく単位[mA]の設定値で返します。

#### 変更

- **v2.2.0**: ドライバのレジスタではなく、設定（[`/setTval`](voltage-and-current-mode-settings.md#settval)で設定し、`/saveConfig`で保存される値）を返します。電圧モードではTVALのレジスタは以前の値のままです。電磁ブレーキのモータで引き上げられたTVAL_HOLDも返されます。

#### 返信

STEP400のみ。

```
/tval_mA (int)motorID (float)holdTVAL_mA (float)runTVAL_mA (float)accTVAL_mA (float)decTVAL_mA
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| holdTVAL_mA | float | 78.125-5078.12 mA | 停止時のTVAL |
| runTVAL_mA | float | 78.125-5078.12 mA | 一定速運転時のTVAL |
| accTVAL_mA | float | 78.125-5078.12 mA | 加速時のTVAL |
| decTVAL_mA | float | 78.125-5078.12 mA | 減速時のTVAL |

#### 関連

[`/getTval`](voltage-and-current-mode-settings.md#gettval)
<!-- generated:end osc /getTval_mA -->

<!-- osc: /setDecayModeParam -->
<!-- generated:begin osc /setDecayModeParam -->
### `/setDecayModeParam` (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN {#setdecaymodeparam}

STEP400のみ。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| T_FAST | int | 0-255 | T_FASTレジスタの値 |
| TON_MIN | int | 0-127 | TON_MINレジスタの値 |
| TOFF_MIN | int | 0-127 | TOFF_MINレジスタの値 |

#### 実行可能タイミング

無励磁状態

#### 説明

電流制御アルゴリズムのパラメータのレジスタを設定します。各レジスタの設定値についてはPowerSTEP01のデータシートを参照してください。

出力は無励磁でなければなりません。そうでないときは`MotorNotHiZ`を返し、何も適用されません。

TON_MINとTOFF_MINは7ビット（0〜127）です。範囲外の値には`CommandIgnored`を返し、何も適用されません。0〜255の範囲外のT_FASTは0〜255に制限されます。

#### 変更

- **v2.2.0**: TON_MINとTOFF_MINは0〜127（7ビット）です。範囲外の値には`/error/command CommandIgnored`を返し、何も適用されません。以前は、128〜255はドライバで128の剰余として扱われる一方、保存される値は128〜255のままでした。T_FASTは以前と同じく0〜255です。
- **v2.2.0**: 出力は無励磁でなければなりません。そうでないときは`/error/command MotorNotHiZ`を返し、何も適用されません。

#### エラー

- `MotorNotHiZ`: ドライバのレジスタのうち、出力が無励磁のときだけ書き込めるものをコマンドが書き込もうとしたが、モータが無励磁ではなかった。励磁して位置を保っているモータは無励磁ではない。先に`/softHiZ`か`/hardHiZ`を送る。何も適用されない。v2.2.0で追加。
- `CommandIgnored`: コマンドが実行可能なタイミングではない。タイミング参照。値がコマンドの範囲外のときにも送信され、何も適用されない（`/setPositionListReportInterval`のモータIDは255）。

#### 初期値

- `T_FAST`: 25（[currentMode.T_FAST](../connections/configuration-items.md#currentmode-t_fast)）
- `TON_MIN`: 41（[currentMode.TON_MIN](../connections/configuration-items.md#currentmode-ton_min)）
- `TOFF_MIN`: 41（[currentMode.TOFF_MIN](../connections/configuration-items.md#currentmode-toff_min)）

#### 関連

[`/getDecayModeParam`](voltage-and-current-mode-settings.md#getdecaymodeparam)
<!-- generated:end osc /setDecayModeParam -->

<!-- osc: /getDecayModeParam -->
<!-- generated:begin osc /getDecayModeParam -->
### `/getDecayModeParam` (int)motorID {#getdecaymodeparam}

STEP400のみ。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |

#### 実行可能タイミング

常時

#### 説明

電流制御アルゴリズムのパラメータを設定するレジスタ値を取得します。

#### 返信

STEP400のみ。

```
/decayModeParam (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| T_FAST | int | 0-255 | T_FASTレジスタの値 |
| TON_MIN | int | 0-127 | TON_MINレジスタの値 |
| TOFF_MIN | int | 0-127 | TOFF_MINレジスタの値 |
<!-- generated:end osc /getDecayModeParam -->

<!-- osc: /setHoldTval -->
<!-- generated:begin osc /setHoldTval -->
### `/setHoldTval` (int)motorID (int)holdTVAL {#setholdtval}

STEP400のみ。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| holdTVAL | int | 0-64 | 停止時のTVAL |

#### 実行可能タイミング

常時

#### 説明

停止時のTVALのみを設定します。

0〜64の範囲外の値は拒否されず、0〜64に制限されます。上限の64（約5A）はファームウェアの安全上の上限です。

電圧モードでは、保存される設定だけが変わります。[`/setCurrentMode`](voltage-and-current-mode-settings.md#setcurrentmode)でレジスタに書き込まれます。

#### 初期値

- `holdTVAL`: 0（[currentMode.TVAL_HOLD](../connections/configuration-items.md#currentmode-tval_hold)）

#### 関連

[`/setTval`](voltage-and-current-mode-settings.md#settval)
<!-- generated:end osc /setHoldTval -->

<!-- osc: /setRunTval -->
<!-- generated:begin osc /setRunTval -->
### `/setRunTval` (int)motorID (int)runTVAL {#setruntval}

STEP400のみ。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| runTVAL | int | 0-64 | 一定速運転時のTVAL |

#### 実行可能タイミング

常時

#### 説明

一定速運転時のTVALのみを設定します。

0〜64の範囲外の値は拒否されず、0〜64に制限されます。上限の64（約5A）はファームウェアの安全上の上限です。

電圧モードでは、保存される設定だけが変わります。[`/setCurrentMode`](voltage-and-current-mode-settings.md#setcurrentmode)でレジスタに書き込まれます。

#### 初期値

- `runTVAL`: 16（[currentMode.TVAL_RUN](../connections/configuration-items.md#currentmode-tval_run)）

#### 関連

[`/setTval`](voltage-and-current-mode-settings.md#settval)
<!-- generated:end osc /setRunTval -->

<!-- osc: /setAccTval -->
<!-- generated:begin osc /setAccTval -->
### `/setAccTval` (int)motorID (int)accTVAL {#setacctval}

STEP400のみ。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| accTVAL | int | 0-64 | 加速時のTVAL |

#### 実行可能タイミング

常時

#### 説明

加速時のTVALのみを設定します。

0〜64の範囲外の値は拒否されず、0〜64に制限されます。上限の64（約5A）はファームウェアの安全上の上限です。

電圧モードでは、保存される設定だけが変わります。[`/setCurrentMode`](voltage-and-current-mode-settings.md#setcurrentmode)でレジスタに書き込まれます。

#### 初期値

- `accTVAL`: 16（[currentMode.TVAL_ACC](../connections/configuration-items.md#currentmode-tval_acc)）

#### 関連

[`/setTval`](voltage-and-current-mode-settings.md#settval)
<!-- generated:end osc /setAccTval -->

<!-- osc: /setDecTval -->
<!-- generated:begin osc /setDecTval -->
### `/setDecTval` (int)motorID (int)decTVAL {#setdectval}

STEP400のみ。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800）、255（全モータ） | モータのID |
| decTVAL | int | 0-64 | 減速時のTVAL |

#### 実行可能タイミング

常時

#### 説明

減速時のTVALのみを設定します。

0〜64の範囲外の値は拒否されず、0〜64に制限されます。上限の64（約5A）はファームウェアの安全上の上限です。

電圧モードでは、保存される設定だけが変わります。[`/setCurrentMode`](voltage-and-current-mode-settings.md#setcurrentmode)でレジスタに書き込まれます。

#### 初期値

- `decTVAL`: 16（[currentMode.TVAL_DEC](../connections/configuration-items.md#currentmode-tval_dec)）

#### 関連

[`/setTval`](voltage-and-current-mode-settings.md#settval)
<!-- generated:end osc /setDecTval -->
