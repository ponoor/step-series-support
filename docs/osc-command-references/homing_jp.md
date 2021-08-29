### `/homing (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
原点復帰動作を行います。原点復帰方向に移動し、HOMEセンサが反応すると停止し、方向を反転してゆっくり移動し、HOMEセンサが反応しなくなった時点で停止し、現在位置を0にします。

これは[`/goUntil`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed)コマンドを実行し、HOMEセンサが反応すると停止して[`/releaseSW`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#releasesw_intmotorid_boolact_booldir)コマンドを実行することに相当します。

原点復帰方向`homingDirection`と原点復帰スピード`homingSpeed`はそれぞれ[`/setHomingDirection`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#sethomingdirection_intmotorid_booldirection)と[`/setHomingSpeed`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#sethomingspeed_intmotorid_floatspeed)で設定できるほか、configToolからも設定できます。

`/goUntil`と`/releaseSw`それぞれにタイムアウト時間が設定可能で、この時間内にセンサ状態に変化がなかった場合はタイムアウトとして動作を中止します。この時間はぞれぞれ[`/setGoUntilTimeout`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#setgountiltimeout_intmotorid_inttimeout) [`setReleaseSwTimeout`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#setreleaseswtimeout_intmotorid_inttimeout)で設定できます。

原点復帰動作の状態変化に応じて下記の返答があります。

#### 返答
```
/homingStatus (int)motorID (int)homingStatus
```

|アーギュメント|範囲|説明|
|---|---|---|
| motorID | 1-4/1-8 | モータのID |
| homingStatus | 0-4 | Homing Status |

##### Homing Status
| homingStatus | Homing Status | 説明 |
| --- | --- | --- |
| 0 | HOMING_UNDEFINED | 原点復帰をまだしていない状態 |
| 1 | HOMING_GOUNTIL | `/goUntil`実行中 |
| 2 | HOMING_RELEASESW | `/releaseSw`実行中 |
| 3 | HOMIMG_COMPLETED | 原点復帰完了 |
| 4 | HOMING_TIMEOUT | 規定時間内に動作が完了しなかった |

### `/getHomingStatus (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
原点復帰の現在のステータスを返します。

#### 返答
[`/homing`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#homing_intmotorid)の返答と同じです。

### `/setHomingDirection (int)motorID (bool)direction`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |
| direction | 0-1 | 1:Forward, 0:Reverse |

#### 実行可能タイミング
常時

#### 説明
[`/homing`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#homing_intmotorid)実行時の原点復帰方向`homingDirection`を指定します。configToolからも指定できます。

#### 初期値
0 (Reverse)

### `/getHomingDirection (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
`homingDirection`を取得します。

#### 返答
```
/homingDirection (int)motorID (bool)homingDirection
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8|モータのID|
| homingDirection | 0-1 | 1:Forward, 0:Reverse |

### `/setHomingSpeed (int)motorID (float)speed`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |
| speed | 0.0-15625.0[step/s] | homingSpeed |

#### 実行可能タイミング
常時

#### 説明
[`/homing`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#homing_intmotorid)実行時の原点復帰速さ`homingSpeed`を指定します。configToolからも指定できます。

#### 初期値
100.0[step/s]

### `/getHomingSpeed (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
`homingSpeed`を取得します。

#### 返答
```
/homingSpeed (int)motorID (float)homingSpeed
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8|モータのID|
| homingSpeed | 0.0-15625.0[step/s] | Homing Speed |

### `/goUntil (int)motorID (bool)ACT (float)speed`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|ACT|0-1||
|speed|-15625 - 15625 [step/s]||

| ACT | 処理 |
| --- | --- |
| 0 | ABS_POSレジスタをリセットします |
| 1 | ASB_POSレジスタの内容をMARKレジスタにコピーします |

#### 実行可能タイミング
常時

#### 説明
指定の速度で回転し、HOMEスイッチ端子が閉状態になるとACTの値に応じた処理を行います。
その後softStopしますが、[`/setHomeSwMode`](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#sethomeswmode_intmotorid_boolsw_mode)コマンドでSW_MODEが0に設定されていると、softStopではなくhardStopになります。このコマンドは、モータが停止するまでBUSY状態を保ちます。

#### 返答
なし

### `/setGoUntilTimeout (int)motorID (int)timeOut`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |
| timeOut | 0-65535[ms] | タイムアウト時間 |

#### 実行可能タイミング
常時

#### 説明
[`/goUnitl`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed)実行時のタイムアウト時間を指定します。この時間内にセンサに反応がなかった場合にはtimeoutとして動作を中止します。configToolからも指定できます。

#### 初期値
10000[ms]

### `/getGoUntilTimeout (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
[`/goUnitl`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed)実行時のタイムアウト時間を取得します。

#### 返答
```
/goUnitlTimeout (int)motorID (int)timeout
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8|モータのID|
| timeout | 0-65535[ms] | タイムアウト時間 |

### `/releaseSw (int)motorID (bool)ACT (bool)DIR`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|ACT|0-1||
|DIR|0-1||

| ACT | 処理 |
| --- | --- |
| 0 | ABS_POSレジスタをリセットします |
| 1 | ASB_POSレジスタの内容をMARKレジスタにコピーします |

| DIR | 方向 |
| --- | --- |
| 1 | 正転方向 |
| 0 | 逆転方向 |

#### 実行可能タイミング
常時

#### 説明
指定方向にminimum speed（初期状態では5[step/s]）で回転し、HOMEスイッチ端子が開状態になると、ACTの値に応じた処理を行います。ACTの処理内容は [`/goUntil`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed)と同じです。その後hardStopします。

#### 返答
なし

### `/setReleaseSwTimeout (int)motorID (int)timeOut`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |
| timeOut | 0-65535[ms] | タイムアウト時間 |

#### 実行可能タイミング
常時

#### 説明
[`/releaseSw`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#releasesw_intmotorid_boolact_booldir)実行時のタイムアウト時間を指定します。この時間内にセンサ反応範囲から脱出できかった場合にはtimeoutとして動作を中止します。configToolからも指定できます。

#### 初期値
5000[ms]

### `/getReleaseSwTimeout (int)motorID`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | モータのID |

#### 実行可能タイミング
常時

#### 説明
[`/releaseSw`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#releasesw_intmotorid_boolact_booldir)実行時のタイムアウト時間を取得します。

#### 返答
```
/releaseSwTimeout (int)motorID (int)timeout
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8|モータのID|
| timeout | 0-10000[ms] | タイムアウト時間 |

