## モータドライバ
### `/enableUvloReport (int)motorID (bool)enable`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|enable|0-1|1で有効, 0で無効|

#### 実行可能タイミング
常時

#### 説明
指定したモータドライバで UVLO (Undervoltage Lockout) が発生した際に自動で通知メッセージを送信するかどうかを指定します。
UVLOはモータドライバへ供給されている電圧が9.2Vを下回ったら通知の有無にかかわらず発生します。この状態ではモータを動かすことはできません。供給電圧が10.4Vを上回ったら解除されます。

#### 返答
ULVO発生時に [`/getUlvo`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#getuvlo_intmotorid)と同じ返答があります。

#### 初期値
1（有効）

### `/getUvlo (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
UVLOの現在の状態を取得します。

#### 返答
```
/uvlo (int)motorID (bool)state
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8|モータのID|
| state | 0-1 | 1:UVLO発生状態 0:UVLO発生無し |

### `/enableThermalStatusReport (int)motorID (bool)enable`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|enable|0-1|1で有効, 0で無効|

#### 実行可能タイミング
常時

#### 説明
指定したモータドライバの温度状態(thermalStatus)に変化があったら自動でメッセージを送信するかどうかを指定します。Bridge shutdown, Device shutdown 状態では、通知の有無にかかわらずモータはHiZ状態になります。

#### 返答
thermalStatusの変化時に [`/getThermalStatus`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#getthermalstatus_intmotorid) と同じ返答があります。


#### 初期値
1（有効）

### `/getThermalStatus (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
ThermalStatusの現在の状態を取得します。

#### 返答
```
/thermalStatus (int)motorID (int)thermalStatus
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8|モータのID|
|thermalStatus|0-3|Thermal status|

##### Thermal status
| thermalStatus | Thermal status | 発生条件 | 解除条件 |
| --- | --- | --- | --- |
| 0 | 通常 | - | - |
| 1 | Warning | 135℃ | 125℃ |
| 2 | Bridge shutdown | 155℃ | 145℃ |
| 3 | Device shutdown | 170℃ | 130℃ |

Bridge shutdown, Device shutdown 状態では、通知の有無にかかわらずモータはHiZ状態になります。


### `/enableOverCurrentReport (int)motorID (bool)enable`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|enable|0-1|1で有効, 0で無効|

#### 実行可能タイミング
常時

#### 説明
指定したモータドライバが過電流状態(OCD, Over Current Detection)になった場合に自動でメッセージを送信するかどうかを指定します。
過電流状態になった場合は、通知の有無にかかわらず自動でHiZ状態になります。閾値は [`/setOverCurrentThreshold`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#setovercurrentthreshold_intmotorid_intocd_th) で設定できます。

#### 返答
OCD状態になっている場合に以下のメッセージが送信されます。
```
/overCurrent (int)motorID
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8|モータのID|

#### 初期値
1（有効）

### `/setOverCurrentThreshold (int)motorID (int)OCD_TH`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|OCD_TH|0-31|Overcurrent detection threshold|

##### Overcurrent detection threshold
| OCD_TH | Overcurrent detection threshold |
| --- | --- |
| 0 | 312.5mA |
| 1 | 625mA |
| ... | ... |
| 30 | 9.6875A |
| 31 | 10A |

#### 実行可能タイミング
常時

#### 説明
過電流の閾値を設定します。312.5mAから10Aまで、312.5mA刻みで設定します。

#### 返答
下記の [`/getOverCurrentThreshold`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#getovercurrentthreshold_intmotorid) と同じ返答があり、実際の設定値を確認できます。

#### 初期値
15 (5A)

### `/getOverCurrentThreshold (int)motorID`
#### アーギュメント　
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|

#### 実行可能タイミング
常時

#### 説明
過電流の閾値を取得します。

#### 返答
```
/overCurrentThreshold (int)motorID (float)overCurrentThreshold
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8|モータのID|
|overCurrentThreshold|0-15|閾値をmA単位であらわしたものです|

#### 初期値
15 (5A)

### `/enableStallReport (int)motorID (bool)enable`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|enable|0-1|1で有効, 0で無効|

#### 実行可能タイミング
常時

#### 説明
閾値は [`/setStallThreshold`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#setstallthreshold_intmotorid_intstall_th) で設定できます。
指定したモータドライバでストール（脱調）が検出された場合、自動で下記のメッセージを送信します。

#### 返答
```
/stall (int)motorID
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8|モータのID|

#### 初期値
0（無効）

### `/setStallThreshold (int)motorID (int)STALL_TH`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|STALL_TH|0-31|Stall detection threshold|

##### Stall detection threshold
| STALL_TH | Stall detection threshold |
| --- | --- |
| 0 | 312.5mA |
| 1 | 625mA |
| ... | ... |
| 30| 9.6875A |
| 31 | 10A |

#### 実行可能タイミング
常時

#### 説明
ストール検出の閾値を設定します。312.5mAから10Aまで、312.5mA刻みで設定します。

#### 返答
下記の [`/getStallThreshold`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#getstallthreshold_intmotorid) と同じ返答があり、実際の設定値を確認できます。

#### 初期値
31 (10A)

### `/getStallThreshold (int)motorID`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|

#### 実行可能タイミング
常時

#### 説明
ストール検出の閾値を取得します。

#### 返答
```
/stallThreshold (int)motorID (float)stallThreshold
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8|モータのID|
|stallThreshold|0-31|閾値をmA単位であらわしたものです|

#### 初期値
31 (10A)

## センサ
### `/setProhibitMotionOnHomeSw (int)motorID (bool)enable`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |
| enable | 0-1 | 1で禁止, 0で許可 |

#### 実行可能タイミング
常時

#### 説明
Homeセンサが反応している状態で、原点復帰方向へのモーションコマンドを禁止します。原点復帰方向は configTool や `/setHomingDirection`で設定できます。

#### 初期値
0 (無効)

### `/getProhibitMotionOnHomeSw (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
Homeセンサが反応している状態で、原点復帰方向へのモーションコマンドが禁止されているかどうかを返します。

#### 返答
```
/prohibitMotionOnHomeSw (int)motorID (bool)enable
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8|モータのID|
| enable | 0-1 | 1:禁止, 0:許可 |

### `/setProhibitMotionOnLimitSw (int)motorID (bool)enable`
**STEP400のみ**
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4, 255 | モータのID |
| enable | 0-1 | 1で禁止, 0で許可 |

#### 実行可能タイミング
常時

#### 説明
Limitセンサが反応している状態で、原点復帰方向の逆方向へのモーションコマンドを禁止します。原点復帰方向は configTool や `/setHomingDirection`で設定できます。

#### 初期値
0 (無効)

### `/getProhibitMotionOnLimitSw (int)motorID`
**STEP400のみ**
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
Limitセンサが反応している状態で、原点復帰方向の逆方向へのモーションコマンドが禁止されているかどうかを返します。

#### 返答
```
/prohibitMotionOnLimitSw (int)motorID (bool)enable
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4|モータのID|
| enable | 0-1 | 1:禁止, 0:許可 |