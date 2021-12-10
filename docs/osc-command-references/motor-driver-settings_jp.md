## モータドライバの設定
### `/setMicrostepMode (int)motorID (int)STEP_SEL`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |
| STEP_SEL | 0-7 | Micro stepping mode |

#### 実行可能タイミング
HiZ状態

#### 説明
マイクロステッピングのモードを切り替えます。

| STEP_SEL | Micro stepping mode |
| --- | --- |
| 0 | Full-step |
| 1 | Half-step |
| 2 | 1/4 microstep |
| 3 | 1/8 microstep |
| 4 | 1/16 microstep |
| 5 | 1/32 microstep |
| 6 | 1/64 microstep |
| 7 | 1/128 microstep |

初期状態では1/128マイクロステップモードになっています。

定電流制御モード (current mode) では、Full-stepから1/16 microstepまでしか使えません。

#### 初期値
7 (1/128 microstep)

### `/getMicrostepMode (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
マイクロステッピングのモードを取得します。STEP_SELについては[`/setMicrostepMode`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#setmicrostepmode_intmotorid_intstep_sel)の項目を参照してください。

#### 返答

```
/microstepMode (int)motorID (int)STEP_SEL
```
### `/enableLowSpeedOptimize (int)motorID (bool)enable`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |
| enable | 0-1 | 1で有効, 0で無効 |

#### 実行可能タイミング
モータ停止時

#### 説明
低速回転時の相電流ひずみ補正 (Low speed optimization) の有効無効を切り替えます。この設定が有効になっていると、`Min Speed` は自動的に0になります。この補正は電圧モードでのみ利用可能です。詳しくは対応するデータシートの "Low speed optimization"を参照してください。

#### 初期値
0 (無効)

### `/setLowSpeedOptimizeThreshold (int)motorID (float)lowSpeedOptimizationThreshold`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |
| lowSpeedOptimizationThreshold | 0.0 - 976.3 [step/s] | Low speed optimization threshold |

#### 実行可能タイミング
モータ停止時 

#### 説明
低速回転時の相電流ひずみ補正を行う閾値を設定します。

下記の[`/getLowSpeedOptimizeThreshold`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#getlowspeedoptimizethreshold_intmotorid)と同じ返答があります。

#### 初期値
20.0 [step/s]

### `/getLowSpeedOptimizeThreshold (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
Low speed optimization threshold の現在の設定値を取得します。

#### 返答

```
/lowSpeedOptimizeThreshold (int)motorID (float)lowSpeedOptimizeThreshold
```

## 状態の取得
### `/enableBusyReport (int)motorID (bool)enable`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |
| enable | 0-1 | 1で有効, 0で無効 |

#### 実行可能タイミング
常時

#### 説明
指定したモータのBUSY状態に変化があったら自動でメッセージを送信する設定を行います。メッセージは[`/getBusy`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#getbusy_intmotorid)の返答と同じです。

#### 初期値
0 (無効)

### `/getBusy (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
指定したモータのBUSY状態を取得します。

#### 返答
```
/busy (int)motorID (bool)state
```
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8 | モータのID |
| state| 0-1 | 1:BUSYの場合, 0:BUSYでない場合 |

### `/enableHizReport (int)motorID (bool)enable`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |
| enable | 0-1 | 1で有効, 0で無効 |

#### 実行可能タイミング
常時

#### 説明
指定したモータのHiZ（ハイインピーダンス）状態に変化があったら自動でメッセージを送信する設定を行います。送信されるメッセージは[`/getHiZ`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#gethiz_intmotorid)の返答と同じです。

#### 初期値
0 (無効)

### `/getHiZ (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
指定したモータのHiZ状態を取得します。

#### 返答
```
/HiZ (int)motorID (bool)state
```
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8 | モータのID |
| state | 0-1 | 1:HiZ状態の場合, 0:HiZ状態でない場合 |

### `/enableDirReport (int)motorID (bool)enable`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |
| enable | 0-1 | 1で有効, 0で無効 |

#### 実行可能タイミング
常時

#### 説明
指定したモータの回転方向に変化があったら自動でメッセージを送信する設定を行います。送信されるメッセージは[`/getDir`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#getdir_intmotorid)の返答と同じです。

#### 初期値
0 (無効)

### `/getDir (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
指定したモータの回転方向を取得します。

#### 返答
```
/dir (int)motorID (bool)direction
```
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8 | モータのID |
| direction | 0-1 | 1:正転方向, 0:逆転方向 |

### `/enableMotorStatusReport (int)motorID (bool)enable`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |
| enable | 0-1 | 1で有効, 0で無効 |

#### 実行可能タイミング
常時

#### 説明
指定したモータの動作状態(MOT_STATUS)に変化があったら自動でメッセージを送信する設定を行います。メッセージは[`/getMotorStatus`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#getmotorstatus_intmotorid)の返答と同じです。

#### 初期値
0 (無効)

### `/getMotorStatus (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
指定したモータの動作状態(MOT_STATUS)を取得します。

#### 返答
```
/motorStatus (int)motorID (int)MOT_STATUS
```
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8 | モータのID |
| MOT_STATUS | 0-3 | Motor status |

##### Motor status
| MOT_STATUS | Motor status |
| --- | --- |
| 0 | モータ停止 |
| 1 | 加速中 |
| 2 | 減速中 |
| 3 | 一定速運転中 |

### `/setPositionReportInterval (int)motorID (int)interval`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |
| interval | 0-2147483647  | 送信間隔 [ms] |

#### 実行可能タイミング
常時

#### 説明
指定したモータの現在位置 (`ABS_POS`) を指定間隔で自動送信します。0を指定すると無効化され、送信を停止します。

いずれかのモータで有効化された場合、`/setPositionListReportInterval`は無効になり自動停止します。

#### 返答
[`/getPosition`](https://ponoor.com/docs/step-series/osc-command-reference/absolute-position-management/#getposition_intmotorid) と同じ返答があります。

#### 初期値
0 (無効)

### `/setPositionListReportInterval (int)interval`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| interval | 0-2147483647  | 送信間隔 [ms] |

#### 実行可能タイミング
常時

#### 説明
全モータの現在位置 (`ABS_POS`) をひとつのリストにまとめたメッセージを指定間隔で自動送信します。0を指定すると無効化され、送信を停止します。

このコマンドが有効化される際には `/setPositionInterval`はすべての軸で無効になり自動停止します。

#### 返答
[`/getPositionList`](https://ponoor.com/docs/step-series/osc-command-reference/absolute-position-management/#getpositionlist) と同じ返答があります。

#### 初期値
0 (無効)

## デバッグ
### `/getAdcVal (int)motorID`
**STEP400のみ**
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
PowerSTEP01チップのADC_OUTレジスタの値を取得します。このレジスタはADCピンの電圧を5ビットでAD変換した値が収められています。このピンは10kΩでプルアップされていて、LIMITSWコネクタに接続されています。

#### 返答
```
/adcVal (int)motorID (int)ADC_OUT
```
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4, 255 | モータのID |
| ADC_OUT | 0-31 | 5bitのADC_OUTレジスタ |

### `/getStatus (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
モータドライバ(PowerSTEP01/L6470)のステータスレジスタを取得します。ステータスレジスタにはモータやアラーム、スイッチの状態などが含まれます。

#### 返答

```
/status (int)motorID (int)status
```
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |
| status | 0-65535(0xFFFF) | 16bitのSTATUSレジスタ |

レジスタに含まれる情報は、データシートを参照してください。このうち、一部の値はラッチされていて、ステータスレジスタを読み出すとリセットされます。本デバイスではファームウェアによって常時ステータスレジスタを繰り返し取得しているため、これらの値はすぐにリセットされてしまいます。これらの事象を個別に報告する設定が可能ですので、そちらを利用してください。

| ステータスbit名 (STEP400) | ステータスbit名 (STEP800) | 対応する設定コマンド |
| --- | --- | --- |
| UVLO | UVLO | [`/enableUvloReport`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#enableuvloreport_intmotorid_boolenable) |
| UVLO_ADC | - | この機能はSTEP400では使えませんので常時無効になっています。 |
| OCD | OCD | [`/enableOverCurrentReport`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#enableovercurrentreport_intmotorid_boolenable) |
| STALL_A, STALL_B | STEP_LOSS_A, STEP_LOSS_B | [`/enableStallReport`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#enablestallreport_intmotorid_boolenable)  |
| CMD_ERROR | WRONG_CMD, NOTPREF_CMD | [`/enableCommandErrorReport`](https://ponoor.com/docs/step-series/osc-command-reference/system-settings/#reporterror_boolenable) |
| TH_STATUS | TH_WRN, TH_SD | [`/enableThermalStatusReport`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#enablethermalstatusreport_intmotorid_boolenable) |
| SW_EVN | SW_EVN | [`/enableHomeSwReport`](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#enablesweventreport_intmotorid_boolenable) |
| MOT_STATUS | MOT_STATUS | [`/enableMotorStatusReport`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#enablemotorstatusreport_intmotorid_boolenable) |
| SW_F | SW_F | [`/enableHomeSwReport`](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#enablehomeswreport_intmotorid_boolenable) |
| BUSY | BUSY | [`/enableBusyReport`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#enablebusyreport_intmotorid_boolenable) |
| HiZ | HiZ | [`/enableHizReport`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#enablehizreport_intmotorid_boolenable) |

### `/getConfigRegister (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
モータドライバ(PowerSTEP01/L6470)のCONFIGレジスタを取得します。CONFIGレジスタにはモータやアラーム、スイッチの状態などが含まれます。

#### 返答

```
/configRegister (int)motorID (int)CONFIG
```
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8 | モータのID |
| CONFIG | 0-65535(0xFFFF) | 16bitのCONFIGレジスタ |

CONFIGレジスタにはモータドライバの各種設定が収められています。詳細についてはモータドライバのデータシートを参照してください。

### `/resetMotorDriver (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
モータドライバ (PowerSTEP01/L6470) をリセットし、初期設定値を再度書き込みます。