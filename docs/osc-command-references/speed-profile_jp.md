### `/setSpeedProfile (int)motorID (float)acc (float)dec (float)maxSpeed`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|acc|14.55 - 59590 [step/s/s]|加速度|
|dec|14.55 - 59590 [step/s/s]|減速度|
|maxSpeed|15.25 - 15610 [step/s]|最大速さ|

#### 実行可能タイミング
モータ停止時

#### 説明
スピードプロファイルのacc, dec, maxSpeedをまとめて設定します。

#### 初期値
|アーギュメント|初期値|説明|
|---|---|---|
|acc|2000|加速度|
|dcc|2000|減速度|
|maxSpeed|620|最大速さ|


### `/getSpeedProfile (int)motorID`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|

#### 実行可能タイミング
常時

#### 説明
スピードプロファイルのacc, dec, maxSpeedをまとめて取得します。

#### 返答
```
/speedProfile (int)motorID (float)acc (float)dec (float)maxSpeed
```

|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|acc|14.55 - 59590 [step/s/s]|加速度|
|dec|14.55 - 59590 [step/s/s]|減速度|
|maxSpeed|15.25 - 15610 [step/s]|最大速さ|

### `/setFullstepSpeed (int)motorID (float)fullstepSpeed`
#### アーギュメント

| アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|fullstepSpeed|7.63-15625 [step/s]|切り替わる閾値|

#### 実行可能タイミング
常時

#### 説明
マイクロステッピングモードが自動でフルステップモードに切り替わる閾値を設定します。

#### 初期値
15625 [step/s]

### `/getFullstepSpeed (int)motorID`
#### アーギュメント

| アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|

#### 実行可能タイミング
常時

#### 説明
マイクロステッピングモードが自動でフルステップモードに切り替わる閾値を取得します。

#### 返答
```
/fullstepSpeed (int)motorID (float)fullstepSpeed
```

| アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8|モータのID|
|fullstepSpeed|7.63-15625 [step/s]|切り替わる閾値|

### `/setMaxSpeed (int)motorID (float)maxSpeed`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|maxSpeed|15.25 - 15610 [step/s]|最大速さ|

#### 実行可能タイミング
常時

#### 説明
スピードプロファイルの最大速さを設定します。

#### 初期値
620[step/s]

### `/setAcc (int)motorID (float)acc`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|acc|14.55 - 59590 [step/s/s]|加速度|

#### 実行可能タイミング
モータ停止時

#### 説明
スピードプロファイルの加速度を設定します。

#### 初期値
2000[step/s/s]

### `/setDec (int)motorID (float)dec`
#### アーギュメント
|アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|
|dec|14.55 - 59590 [step/s/s]|減速度|

#### 実行可能タイミング
モータ停止時

#### 説明
スピードプロファイルの減速度 (deceleration) を設定します。

#### 初期値
2000[step/s/s]

### `/getSpeed (int)motorID`
#### アーギュメント

| アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8, 255|モータのID|

#### 実行可能タイミング
常時

#### 説明
モータの現在の速度を返します。

#### 返答
```
/speed (int)motorID (float)speed
```

| アーギュメント|範囲|説明|
|---|---|---|
|motorID|1-4/1-8|モータのID|
|speed|-15625 - 15625 [step/s]|現在の速度|