## 概要
本デバイスから送信されるメッセージの多くは、問い合わせメッセージに対する返答です。例えば現在位置を取得する`/getPosition`というメッセージを本デバイスに送ると、本デバイスからは`/position`という返答メッセージが直ちに送信されます。
しかし、いくつかのメッセージは、特定のメッセージに対する返答ではなく、本デバイスの状態が変化した場合に自動的に送信されます。ここでは、それらの自動送信されるメッセージについて説明しています。

## 起動の通知
### `/booted`
#### 説明
本デバイスが（再）起動した際に自動的に本デバイスから送信されるメッセージです。何らかの理由で本デバイスがリセットされたことを検出できます。

ファームウェアが起動して、Ethernetがリンク状態になった1秒後に送信されます。サブネット内のすべてのノード (`255.255.255.255`) へブロードキャストされます。

Config Toolの設定を用いて、このメッセージを送信しないようにも設定できます。

#### 送信されるメッセージ

```
/booted (int)deviceID
```

| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| deviceID | 0-255| DIPスイッチで設定されたデバイスのID |

## エラー
### `/error/osc`
#### 説明
受け取ったOSCメッセージに何らかのエラーがあった場合に送信されます。

#### 送信されるメッセージ

```
/error/osc (symbol)errorText
```

| アーギュメント  | 説明 |
| --- | --- |
| ErrorText | エラーの内容を示す文字列です。 |

##### Error Text
| ErrorText  | 説明 |
| --- | --- |
| `MessageNotMatch` | 該当するコマンドがない。 |
| `OscSyntaxError` | OSCのフォーマットが規格に沿っていなかった |
| `WrongDataType` | OSCメッセージの引数の型が異なっている |

### `/error/command`
#### 説明
コマンドの実行時にエラーが発生した場合に送信されます。

[`/reportError`](https://ponoor.com/docs/step-series/osc-command-reference/system-settings/#reporterror_boolenable) によって、送信の有効/無効を切り替えることができます。

#### 送信されるメッセージ

```
/error/command (Symbol)ErrorText (int)motorID
```

|アーギュメント|範囲|説明|
|---|---|---|
| ErrorText | | エラーの内容を示す文字列です。 |
|motorID| 1-4/1-8 |モータのID|

##### Error Text
| ErrorText  | 説明 |
| --- | --- |
| `CommandIgnored` | コマンドが実行可能なタイミングではない。[タイミング](https://ponoor.com/docs/step-series/osc-command-reference/#i-4)参照。 |
| `MotorIdNotMatch` | モータIDが適切でない値になっている。 |
| `BrakeEngaging` | 電磁ブレーキが効いた状態のままモーションコマンドを送信した。|
| `HomeSwActivating` | ホームセンサ上から原点復帰方向に移動しようとした。 |
| `LimitSwActivating` | リミットセンサ上から原点復帰方向の逆向きに移動しようとした。 |
| `GoUntilTimeout` | `/goUntil`コマンド実行中にタイムアウトした。 |
| `ReleaseSwTimeout` | `/releaseSw`コマンド実行中にタイムアウトした。 |
| `InServoMode` | サーボモードでは実行できないコマンドを送信した。 |

## 状態の通知
### `/busy`
[`/enableBusyReport`](https://ponoor.com/docs/step-series/osc-command-reference/system-settings/#enablebusyreport_intmotorid_boolenable)をご確認ください。

### `/HiZ`
[`/enableHizReport`](https://ponoor.com/docs/step-series/osc-command-reference/system-settings/#enablehizreport_intmotorid_boolenable)をご確認ください。

### `/dir`
[`/enableDirReport`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#enabledirreport_intmotorid_boolenable)をご確認ください。

### `/motorStatus`
[`/enableMotorStatusReport`](https://ponoor.com/docs/step-series/osc-command-reference/system-settings/#enablemotorstatusreport_intmotorid_boolenable) をご確認ください。

### `/homingStatus`
[`/homing`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#homing_intmotorid) をご確認ください。

### `/position`
[`/setPositionReportInterval`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#setpositionreportinterval_intmotorid_intinterval)をご確認ください。

### `/positionList`
[`/setPositionListReportInterval`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#setpositionlistreportinterval_intinterval)をご確認ください。

## アラームの通知

### `/uvlo`
[`/enableUvloReport`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#enableuvloreport_intmotorid_boolenable)をご確認ください。

### `/thermalStatus`
[`/enableThermalStatusReport`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#enablethermalstatusreport_intmotorid_boolenable)をご確認ください。

### `/overCurrent`
[`/enableOverCurrentReport`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#enableovercurrentreport_intmotorid_boolenable)をご確認ください。

### `/stall`
[`/enableStallReport`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#enablestallreport_intmotorid_boolenable)をご確認ください。

