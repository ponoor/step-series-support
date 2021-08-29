## 状態の取得
### `/enableHomeSwReport (int)motorID (bool)enable`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|enable|0-1|1で有効, 0で無効|

#### 実行可能タイミング
常時

#### 説明
指定したモータのHOMEスイッチ端子の状態に変化があったら自動でメッセージを送信する設定を行います。送信されるメッセージは[`/getHomeSw`](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#gethomesw_intmotorid)の返答と同じです。

#### 初期値
0（無効）

### `/enableSwEventReport (int)motorID (bool)enable`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|enable|0-1|1で有効, 0で無効|

#### 実行可能タイミング
常時

#### 説明
指定したモータのHOMEスイッチ端子の状態がHIGHレベルからLOWレベルに遷移した際(Falling Edge)に自動でメッセージを送信する設定を行います。
[`/enableHomeSwReport`](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#enablehomeswreport_intmotorid_boolenable)はマイコンのファームウェア上から約1ms毎にモータドライバICのSTATUSレジスタをポーリングすることによって状態を監視していますが、この`/enableSwEventReport`のほうはドライバIC内でハードウェアによってイベントが検出されるため、1ms以下のごくわずかな時間だけセンサが反応した場合でももとり逃しません。
送信されるメッセージは以下の通りです。

```
/swEvent (int)motorID
```
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8|モータのID|

#### 初期値
0（無効）

### `/getHomeSw (int)motorID`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|

#### 実行可能タイミング
常時

#### 説明
HOMEスイッチの状態を取得します。

#### 返答
```
/homeSw (int)motorID (bool)swState (bool)direction
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|swState|0-1|状態|
|direction|0-1|方向|

| swState | 状態 |
| --- | --- |
| 0 | Open, 反応していない状態 |
| 1 | Closed, 反応している状態 | 

| direction | 方向 |
| --- | --- |
| 1 | 正転方向 |
| 0 | 逆転方向 |

### `/enableLimitSwReport (int)motorID (bool)enable`
**STEP400のみ**
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4, 255|モータのID|
|enable|0-1|1で有効, 0で無効|

#### 実行可能タイミング
常時

#### 説明
指定したモータのLIMITスイッチ端子の状態に変化があったら自動でメッセージを送信する設定を行います。送信されるメッセージは[`/getLimitSw`](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#getlimitsw_intmotorid)の返答と同じです。

#### 初期値
0（無効）

### `/getLimitSw (int)motorID`
**STEP400のみ**
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4, 255|モータのID|

#### 実行可能タイミング
常時

#### 説明
LIMITスイッチの状態を取得します。

#### 返答
```
/limitSw (int)motorID (bool)swState (bool)direction
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|swState|0-1|状態|
|direction|0-1|方向|

| swState | 状態 |
| --- | --- |
| 0 | Open, 反応していない状態 |
| 1 | Closed, 反応している状態 | 

| direction | 方向 |
| --- | --- |
| 1 | 正転方向 |
| 0 | 逆転方向 |

## 反応時の動作設定
### `/setHomeSwMode (int)motorID (bool)SW_MODE`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|SW_MODE|0-1|Switch mode|

| SW_MODE | Switch mode |
| --- | --- |
| 0 | HardStop interrupt （即時停止する）|
| 1 | User disposal （停止しない）|

#### 実行可能タイミング
HiZ状態

#### 説明
HOMEスイッチ端子に入力があった際に即時停止するかどうか(Switch mode)を指定します。

#### 初期値
1 (User disposal)

### `/getHomeSwMode (int)motorID`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|

#### 実行可能タイミング
常時

#### 説明
上記のSwitch modeを取得します。

#### 返答
```
/homeSwMode (int)motorID (bool)swMode
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|swMode|0-1||

### `/setLimitSwMode (int)motorID (bool)SW_MODE`
**STEP400のみ**
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4, 255|モータのID|
|SW_MODE|0-1|Switch mode|

| SW_MODE | Switch mode |
| --- | --- |
| 0 | HardStop interrupt （即時停止する）|
| 1 | User disposal （停止しない）|

#### 実行可能タイミング
常時

#### 説明
LIMITスイッチ端子に入力があった際に即時停止するかどうか(Switch mode)を指定します。

#### 初期値
1 (User disposal)

### `/getLimitSwMode (int)motorID`
**STEP400のみ**
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4, 255|モータのID|

#### 実行可能タイミング
常時

#### 説明
上記のSwitch modeを取得します。

#### 返答
```
/limitSwMode (int)motorID (bool)swMode
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4, 255|モータのID|
|swMode|0-1||
