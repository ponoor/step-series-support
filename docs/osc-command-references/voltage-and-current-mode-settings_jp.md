## 電圧モード
### `/setVoltageMode (int)motorID`
**STEP400のみ**
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4, 255|モータのID|

#### 実行可能タイミング
HiZ状態

#### 説明
指定したモータを電圧モードに切り替えます。STEP800は常に電圧モードで動作しますので、この切替コマンドはSTEP400のみ利用可能です。

### `/setKval (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)setDecKVAL`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|holdKVAL|0-255|停止時のKVA|
|runKVAL|0-255|一定速運転時のKVAL|
|accKVAL|0-255|加速時のKVAL|
|setDecKVAL|0-255|減速時のKVAL|

#### 実行可能タイミング
常時

#### 説明
KVAL4種をまとめて設定します。

#### 初期値
16

### `/getKval (int)motorID`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|

#### 実行可能タイミング
常時

#### 説明
KVAL4種をまとめて取得します。

#### 返答
```
/kval (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)setDecKVAL
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8|モータのID|
|holdKVAL|0-255|停止時のKVA|
|runKVAL|0-255|一定速運転時のKVAL|
|accKVAL|0-255|加速時のKVAL|
|setDecKVAL|0-255|減速時のKVAL|

### `/setBemfParam (int)motorID (int)INT_SPEED (int)ST_SLP (int)FN_SLP_ACC (int)FN_SLP_DEC`

#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |
| INT_SPEED | 0-16383(0x3FFF) | INT_SPEEDレジスタの値 |
| ST_SLP | 0-255(0xFF) | ST_SLPレジスタの値 |
| FN_SLP_ACC | 0-255(0xFF) | FN_SLP_ACCレジスタの値 |
| FN_SLP_DEC | 0-255(0xFF) | FN_SLP_DECレジスタの値 |


#### 実行可能タイミング
HiZ状態

#### 説明
BEMF補償パラメータのレジスタを設定します。各レジスタの設定値については [電圧モードの設定](https://ponoor.com/docs/step-series/functional-description/voltage-mode-and-current-mode/#i-2) を参照してください。

#### 初期値
| アーギュメント | 初期値 |
| --- | --- |
| INT_SPEED | 1032 (0x0402) |
| ST_SLP | 25 (0x19) |
| FN_SLP_ACC | 41 (0x29) |
| FN_SLP_DEC | 41 (0x29) |

### `/getBemfParam (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
BEMFパラメータを設定するレジスタ値を取得します。

#### 返答
```
/bemfParam (int)motorID (int)INT_SPEED (int)ST_SLP (int)FN_SLP_ACC (int)FN_SLP_DEC
```
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8 | モータのID |
| INT_SPEED | 0-16383(0x3FFF) | INT_SPEEDレジスタの値 |
| ST_SLP | 0-255(0xFF) | ST_SLPレジスタの値 |
| FN_SLP_ACC | 0-255(0xFF) | FN_SLP_ACCレジスタの値 |
| FN_SLP_DEC | 0-255(0xFF) | FN_SLP_DECレジスタの値 |

<!--

### `/setHoldKval (int)motorID (int)holdKVAL`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|holdKVAL|0-255|停止時のKVAL|

#### 実行可能タイミング
常時

#### 説明
停止時のKVALのみを設定します。

#### 初期値
16

### `/setRunKval (int)motorID (int)runKVAL`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|setRunKVAL|0-255|一定速運転時のKVAL|

#### 実行可能タイミング
常時

#### 説明
一定速運転時のKVALのみを設定します。

#### 初期値
16

### `/setAccKval (int)motorID (int)accKVAL`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|accKVAL|0-255|加速時のKVAL|

#### 実行可能タイミング
常時

#### 説明
加速時のKVALのみを設定します。

#### 初期値
16

### `/setDecKval (int)motorID (int)decKVAL`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|decKVAL|0-255|減速時のKVAL|

#### 実行可能タイミング
常時

#### 説明
減速時のKVALのみを設定します。

#### 初期値
16

-->

## 電流モード
### `/setCurrentMode (int)motorID`
**STEP400のみ**
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4, 255|モータのID|


#### 実行可能タイミング
HiZ状態

#### 説明
指定したモータを電流モードに切り替えます。

### `/setTval (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)setDecTVAL`
**STEP400のみ**
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4, 255|モータのID|
|holdTVAL|0-127|停止時のTVAL|
|runTVAL|0-127|一定速運転時のTVAL|
|accTVAL|0-127|加速時のTVAL|
|setDecTVAL|0-127|減速時のTVAL|

#### 実行可能タイミング
常時

#### 説明
TVAL4種をまとめて設定します。

STEP400では、TVALは以下のようになっています。

| TVAL | 設定値[mA] |
| --- | --- |
| 0 | 78mA |
| 1 | 156mA |
| ... | ... |
| 127 | 9,984mA |

#### 初期値
16（1328.125mA）

### `/getTval (int)motorID`
**STEP400のみ**
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4, 255|モータのID|

#### 実行可能タイミング
常時

#### 説明
TVAL4種をまとめて取得します。

#### 返答
```
/tval (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4, 255|モータのID|
|holdTVAL|0-127|停止時のTVAL|
|runTVAL|0-127|一定速運転時のTVAL|
|accTVAL|0-127|加速時のTVAL|
|decTVAL|0-127|減速時のTVAL|

### `/getTval_mA (int)motorID`
**STEP400のみ**
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4, 255|モータのID|

#### 実行可能タイミング
常時

#### 説明
TVAL4種をまとめて取得します。レジスタの値ではなく単位[mA]の設定値で返します。

#### 返答
```
/tval (int)motorID (float)holdTVAL_mA (float)runTVAL_mA (float)accTVAL_mA (float)decTVAL_mA
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4, 255|モータのID|
|holdTVAL_mA| 78.125 - 5000.0 |停止時のTVAL [mA]|
|runTVAL_mA| 78.125 - 5000.0 |一定速運転時のTVAL [mA]|
|accTVAL_mA| 78.125 - 5000.0 |加速時のTVAL [mA]|
|DecTVAL_mA| 78.125 - 5000.0 |減速時のTVAL [mA]|

### `/setDecayModeParam (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN`
**STEP400のみ**
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4, 255 | モータのID |
| T_FAST | 0-255(0xFF) | T_FASTレジスタの値 |
| TON_MIN | 0-255(0xFF) | TON_MINレジスタの値 |
| TOFF_MIN | 0-255(0xFF) | TOFF_MINレジスタの値 |


#### 実行可能タイミング
HiZ状態

#### 説明
電流制御アルゴリズムのパラメータのレジスタを設定します。各レジスタの設定値については PowerSTEP01のデータシートを参照してください。

#### 初期値
| アーギュメント | 初期値 |
| --- | --- |
| T_FAST | 25 (0x19) |
| TON_MIN | 41 (0x29) |
| TOFF_MIN | 41 (0x29) |

### `/getDecayModeParam (int)motorID`
**STEP400のみ**
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
電流制御アルゴリズムのパラメータを設定するレジスタ値を取得します。

#### 返答
```
/decayModeParam (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN
```

| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4 | モータのID |
| T_FAST | 0-255(0xFF) | T_FASTレジスタの値 |
| TON_MIN | 0-255(0xFF) | TON_MINレジスタの値 |
| TOFF_MIN | 0-255(0xFF) | TOFF_MINレジスタの値 |

<!--

### `/setHoldTval (int)motorID (int)holdTVAL`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|holdTVAL|0-255|停止時のTVAL|

#### 実行可能タイミング
常時

#### 説明
停止時のTVALのみを設定します。

#### 初期値
16（1328.125mA）

### `/setRunTval (int)motorID (int)runTVAL`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|setRunTVAL|0-255|一定速運転時のTVAL|

#### 実行可能タイミング
常時

#### 説明
一定速運転時のTVALのみを設定します。

#### 初期値
16（1328.125mA）

### `/setAccTval (int)motorID (int)accTVAL`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|accTVAL|0-255|加速時のTVAL|

#### 実行可能タイミング
常時

#### 説明
加速時のTVALのみを設定します。

#### 初期値
16（1328.125mA）

### `/setDecTval (int)motorID (int)decTVAL`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|decTVAL|0-255|減速時のTVAL|

#### 実行可能タイミング
常時

#### 説明
減速時のTVALのみを設定します。

#### 初期値
16（1328.125mA）

-->
