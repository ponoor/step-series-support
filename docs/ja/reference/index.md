---
title: "OSCコマンドリファレンス: 共通の決まり"
---

# OSCコマンドリファレンス: 共通の決まり

## 概要

すべてのコマンドの一覧表は、[コマンド一覧](command-list.md)をご覧ください。

Open Sound Control（OSC）で制御するコマンドのリファレンスです。コマンドはSTEP400とSTEP800で共通ですが、STEP400のみで使えるコマンド（「STEP400のみ。」と表記）や、ボードによって値が異なるコマンドがあります。詳しくは[STEP400とSTEP800の違い](differences-step400-step800.md)をご覧ください。

コマンドは、OSCバンドル（複数のOSCメッセージを束ねたもの）ではなく、単体のOSCメッセージとして送ってください。バンドルには対応していません。

## モータのID

OSCコマンドのモータIDは、基板に印刷してある番号と一致しています。コマンドによっては、全モータに一斉に同じ指令を送れます。その場合は、モータIDに255を指定します。

コマンドで使えるモータIDは、次のとおりです。

| 機種 | モータIDの範囲 |
| --- | --- |
| STEP400 | 1-4, 255 |
| STEP800 | 1-8, 255 |

## 表記

### 引数の型

| 表記 | 説明 |
| --- | --- |
| (int) | 整数です。実際に送れる範囲は、コマンドによって異なります。 |
| (float) | 浮動小数点数です。実際に送れる範囲は、コマンドによって異なります。 |
| (bool) | 論理値で、1または0の整数として送ります。値の範囲を明確にするために、boolと表記しています。 |
| (string) | 文字列（OSC-string）です。 |

### ボードから送信されるメッセージ

[OSCの規格](https://opensoundcontrol.stanford.edu/spec-1_0.html)では、引数の型として、整数（int32）、浮動小数点数（float32）、文字列（OSC-string）などのほかに、非標準の型として論理値のTrue / Falseなどが定められています。STEPシリーズは、論理値をTrue / Falseでは送らず、いつも0または1の整数（型タグ`i`）として送ります。v2.2.0より前は、一部のメッセージがTrue / Falseを使っていました（[移行ガイド](../maintenance/migration-guide.md)をご覧ください）。

### ボードへ送信するメッセージ

ボードは、コマンドを適用する前に引数を検査します。検査に通らないときは、何も適用されません。

| 場合 | 返るエラー |
| --- | --- |
| コマンドに必要な数より引数が少ない | `/error/osc MissingArgument` |
| 型が違う引数: 数値の代わりの文字列、NaN、∞、`/setConfigName`に文字列以外 | `/error/osc WrongDataType` |
| ボードにないモータID | `/error/command MotorIdNotMatch`（送ったモータIDつき） |
| コマンドの範囲外の値 | `/error/command CommandIgnored` |
| 16個を超える引数、または512バイトを超えるパケット | `/error/osc OscSyntaxError` |

範囲外の値を拒否せず、制限や切り捨てをして適用するコマンドもあります。各コマンドの説明をご覧ください。

必要な数を超える引数は無視されます。エラーの送信を無効にしている間（[`/reportError`](system-settings.md#reporterror)）は、エラーは送信されません。エラーのメッセージは、[自動送信されるメッセージ](automatically-sent-messages.md)をご覧ください。

整数と浮動小数点数は、受信時に相互に変換されます。論理値は、整数、浮動小数点数、OSCの論理値のTrue / Falseのどれでも受け付けます。

| 型 | 1と判定 | 0と判定 |
| --- | --- | --- |
| int32 | 0より大きい | 0以下 |
| float32 | 1.0以上 | 1.0未満 |
| 論理値 | True | False |

### コマンドを実行可能なタイミング

コマンドによっては、実行できる状態が限られています。各コマンドのリファレンスに「実行可能タイミング」として表示しています。

| 表記 | 説明 |
| --- | --- |
| 常時 | いつでも実行できます。 |
| モータ停止時 | モータが停止しているときに実行できます（無励磁のモータも含みます）。モータが回転している間は、`/error/command MotorNotStopped`を返し、何も適用されません。 |
| 無励磁状態 | ドライバの出力が無励磁のときに実行できます。位置を保っている（励磁している）モータは無励磁ではありません。先に[`/softHiZ`](motor-control.md#softhiz)または[`/hardHiZ`](motor-control.md#hardhiz)を送ってください。そうしないと`/error/command MotorNotHiZ`を返し、何も適用されません。 |
| 動作開始条件時 | モータの動作の開始条件がそろっているときに実行できます（下記）。 |

無励磁（HiZ）とは、モータドライバの出力が高インピーダンスになり、モータに電流が流れない状態です。モータは励磁されません。

#### 動作開始条件 {#motion-start-condition}

次の条件を、どちらも満たしている状態です。

- 電磁ブレーキが解放されている
- サーボモードではない

また、送ろうとしているコマンドの値は、次の条件を満たしている必要があります。

- [`/setProhibitMotionOnHomeSw`](alarm-settings.md#setprohibitmotiononhomesw)が設定されていて、HOMEスイッチがオンのときに、`homingDirection`へ動作しようとしていない
- [`/setProhibitMotionOnLimitSw`](alarm-settings.md#setprohibitmotiononlimitsw)が設定されていて、LIMITスイッチがオンのときに、`homingDirection`の逆方向へ動作しようとしていない

条件を満たさない動作コマンドは、`BrakeEngaged`、`InServoMode`、`HomeSwActivating`、`LimitSwActivating`などのエラーで拒否されます。コマンドごとのエラーは、各コマンドのリファレンスに載せています。

## 留意点

- ボードは、[`/setDestIp`](system-settings.md#setdestip)を受信するまで、ブロードキャストの[`/booted`](automatically-sent-messages.md#booted)を除いて、OSCメッセージを送信しません。宛先に届かないメッセージを大量に送ると、ボードの挙動がおかしくなることがあるためです（設定ツールで、`/setDestIp`を待たずに送信を始めるようにもできます。[`network.canSendMsgBeforeDestIp`](../connections/configuration-items.md#network-cansendmsgbeforedestip)をご覧ください）。
- ボードが宛先のMACアドレスを解決している間（`/setDestIp`の後の最大数秒）も、宛先へのメッセージは破棄されます。詳しくは、[通信とメッセージ](../guides/communication-and-messages.md)をご覧ください。
