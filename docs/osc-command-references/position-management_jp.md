## 座標
### `/setPosition (int)motorID (int)newPosition`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|newPosition|-2,097,152 - 2,097,151|指定座標|

#### 実行可能タイミング
モータ停止時

#### 説明
ABS_POSレジスタを指定座標に書き換えます。現在のモータ位置が指定座標になります。

### `/getPosition (int)motorID`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|

#### 実行可能タイミング
常時

#### 説明
ABS_POSレジスタの内容（現在位置）を取得します。

[`/setPositionReportInterval`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#setpositionreportinterval_intmotorid_intinterval) コマンドで、指定間隔で自動送信させることもできます。
#### 返答
```
/position (int)motorID (int)ABS_POS
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8|モータのID|
|ABS_POS|-2,097,152 - 2,097,151|現在位置|

### `/getPositionList`
#### アーギュメント
なし

#### 実行可能タイミング
常時

#### 説明
全モータの現在位置 (`ABS_POS`) を取得します。 `/getPosition 255` を送信した場合は、モータの軸数分の個別のメッセージが返されますが、このコマンドは、すべてのモータの位置をリストにまとめた1個のメッセージが返されます。

[`/setPositionListReportInterval`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#setpositionlistreportinterval_intinterval) コマンドで、指定間隔で自動送信させることもできます。

#### 返答
```
/positionList (int)position#1 ... (int)position#n ... (int)position#4
```

|アーギュメント|範囲|説明|
|---|---|---|
|position#n|-2,097,152 - 2,097,151|n個目のモータの現在位置|

アーギュメント数はSTEP400の場合は4個、STEP800の場合は8個です。

### `/resetPos (int)motorID`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|

#### 実行可能タイミング
常時

#### 説明
ABS_POSレジスタを0にリセットします。

### `/setElPos (int)motorID (int)newFullstep (int)newMicrostep`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|newFullstep|0-3|フルステップでの位置|
|newMicrostep|0-127|マイクロステップでの位置|

#### 実行可能タイミング
モータ停止時

#### 説明
モータの電気的位置(electrical postion)を設定します。マイクロステップは0-127の128段階で表現されていますので、設定時は現在のマイクロステップと齟齬のない値を設定する必要があります。

### `/getElPos (int)motorID`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|

#### 実行可能タイミング
常時

#### 説明
モータの電気的位置 (electrical postion)を取得します。

#### 返答
```
/elPos (int)motorID (int)fullstep (int)microstep
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8|モータのID|
|fullstep|0-3|フルステップでの位置|
|microstep|0-127|マイクロステップでの位置|

## HOME/MARK
### `/setMark (int)motorID (int)mark`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|mark|| 設定する座標 |

#### 実行可能タイミング
常時

#### 説明
markを任意の位置に設定します。
#### 返答
なし

### `/getMark (int)motorID`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|

#### 実行可能タイミング
常時

#### 説明
MARKの位置を取得します。

#### 返答
```
/mark (int)motorID (int)mark
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|mark| - | MARKの座標 |

### `/goHome (int)motorID`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|

#### 実行可能タイミング
BUSY解除時

#### 説明
HOME位置までスピードプロファイルに従って移動します。
#### 返答
なし

### `/goMark (int)motorID`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|

#### タイミング
BUSY解除時

#### 説明
MARK位置までスピードプロファイルに従って移動します。
#### 返答
なし

