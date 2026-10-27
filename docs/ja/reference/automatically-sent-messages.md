---
title: 自動送信されるメッセージ
---

# 自動送信されるメッセージ

## 概要

ボードから送信されるメッセージの多くは、コマンド（問い合わせ）への返信です。たとえば、モータの現在位置を取得する[`/getPosition`](position-management.md#getposition)を送ると、ボードは[`/position`](#position)を返信します。一方、いくつかのメッセージは、特定のコマンドへの返信ではなく、ボードの状態が変化したときなどに、自動的に送信されます（通知）。このページでは、自動送信されるメッセージを説明します。返信だけで送信されるメッセージは、各コマンドの「返信」の欄に載せています。

## 起動の通知

<!-- osc-message: /booted -->
<!-- generated:begin osc-message /booted -->
### `/booted` (int)deviceID (int)resetCause {#booted}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| deviceID | int | 0-255 | DIPスイッチで設定されたデバイスのID |
| resetCause | int |  | MCUが示す、リセットの原因です。（v2.2.0で追加。） |

`resetCause`

| 値 | 意味 |
| --- | --- |
| 0 | 不明 |
| 1 | 電源投入。1と2は、どちらも電源によるリセットとして扱ってください |
| 2 | 電源電圧の低下（ブラウンアウト）。SAMD21では、通常の電源投入が2になることが多くあります |
| 3 | リセットピン |
| 4 | ウォッチドッグ |
| 5 | ソフトウェアリセット（たとえば[`/resetDevice`](system-settings.md#resetdevice)の後や、USBでのファームウェア書き込みの後） |
| 6 | CPU動作異常: CPU例外（SAMD21ではHardFault）の後のリセット |

#### 説明

ボードが（再）起動した際に自動的にボードから送信されるメッセージです。何らかの理由でボードがリセットされたことを検出できます。

ファームウェアが起動して、Ethernetがリンク状態になった1秒後に送信されます。サブネット内のすべてのノード（`255.255.255.255`）へブロードキャストされます。

Config Toolの設定を用いて、このメッセージを送信しないようにも設定できます。

`resetCause`: 番号は仕様の一部です。新しい原因は7、8、... として追加されます。クライアントは、知らない番号を「その他」として扱い、6を受け付けてください。複数の原因が記録されているときは、CPU動作異常、電源電圧の低下（ブラウンアウト）、電源投入、ウォッチドッグ、リセットピン、ソフトウェアの順で最初のものが`resetCause`になります。電源投入やブラウンアウトの後にはCPU動作異常は記録されないため、CPU動作異常の後に電源を入れ直すと1か2になります。番号はMCUが返したものがそのまま使われます。将来別のMCUを使うと、同じ操作でも別の番号になることがあります（各番号の意味は変わりません）。

#### 変更

- **v2.2.0**: 第2引数`resetCause`（`i`）が追加されました: `/booted myId resetCause`。引数の数を厳密に確認しているクライアントは影響を受けます。
- **v2.2.0**: ウォッチドッグが停止を検出すると（最後のウォッチドッグのリセットから約250ms後）、まずすべてのブレーキ出力を保持し、電磁ブレーキが有効でブレーキが保持されていないモータのうち最長の`brakeTransitionDuration`（最大1秒）を待ってから、ボードをリセットします。そのため、リセットは以前より最大1秒遅れます。`resetCause`は4のままです。v2.1.0は、停止から約62.5ms後にボードをリセットしていました。
- **v2.2.0**: CPU動作異常（HardFault）では、すべてのブレーキ出力をすぐに保持し、上と同じように待って（最大1秒）から、`resetCause` 6で再起動します。
- **v2.2.0**: [`/resetDevice`](system-settings.md#resetdevice)によるリセットでは、`resetCause`が5（ソフトウェア）になります。
<!-- generated:end osc-message /booted -->

## エラー

<!-- osc-message: /error/osc -->
<!-- generated:begin osc-message /error/osc -->
### `/error/osc` (string)errorText {#error-osc}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| errorText | string |  | エラーの内容を示す文字列です。 |

`errorText`

| 値 | 意味 |
| --- | --- |
| MessageNotMatch | 該当するコマンドがない。 |
| OscSyntaxError | OSCのフォーマットが規格に沿っていなかった。512バイトを超えるパケットと、16個を超える引数を持つメッセージにも送信される。**v2.2.0**: 512バイトを超えるパケットと、16個を超える引数を持つメッセージにも送信されます。 |
| WrongDataType | OSCメッセージの引数の型が異なっている: 数値の位置に文字列、NaN、無限大、または`/setConfigName`に文字列以外。何も適用されない。**v2.2.0**: 何も適用されません。以前は、このような引数は0として適用されていました。 |
| MissingArgument | メッセージの引数の数が、コマンドに必要な数より少なかった。何も適用されない。v2.2.0で追加。 |

#### 説明

受け取ったOSCメッセージに何らかのエラーがあった場合に送信されます。

コマンドを適用する前に、すべてのコマンドの引数が検査されます。コマンドが必要とする数を超える引数は無視されます。エラーの通知が無効の間（[`/reportError`](system-settings.md#reporterror)）は送信されません。

#### 変更

- **v2.2.0**: `MissingArgument`が新しく追加されました。引数が足りないコマンドにはこのエラーを返し、何も適用しません。以前は、足りない引数が0として適用されていました（`/setKval 1`はモータ1のすべてのKVALを0に、`/setSpeedProfile 1`はacc、dec、最大速度を0にし、`/setTargetPositionList`の足りない位置は0になっていました）。
- **v2.2.0**: `WrongDataType`は、型の誤った引数（数値の位置の文字列、NaN、無限大、`/setConfigName`の文字列以外）に対して返され、何も適用されません。以前は、その引数が0として適用されていました。
- **v2.2.0**: 512バイトを超えるパケットと、16個を超える引数を持つメッセージには、`OscSyntaxError`を返します。
- **v2.2.0**: 以前のOSCライブラリがアドレスパターンの末尾を越えて読んでいた一部の特殊なケース（たとえば`{...}`のリストの後ろに文字が続く場合）では、マッチの結果が以前と異なることがあります。
<!-- generated:end osc-message /error/osc -->

<!-- osc-message: /error/command -->
<!-- generated:begin osc-message /error/command -->
### `/error/command` (string)errorText (int)motorID {#error-command}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| errorText | string |  | エラーの内容を示す文字列です。 |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |

`errorText`

| 値 | 意味 |
| --- | --- |
| CommandIgnored | コマンドが実行可能なタイミングではない。タイミング参照。値がコマンドの範囲外のときにも送信され、何も適用されない（`/setPositionListReportInterval`のモータIDは255）。 |
| MotorIdNotMatch | モータIDが適切でない値になっている。0〜255の範囲外のモータIDは、送信された値のまま返される。**v2.2.0**: 0〜255の範囲外のモータIDは、送信された値のまま返されます。以前は、257と511が1と255として読まれていました。 |
| BrakeEngaged | 電磁ブレーキが効いた状態のままモーションコマンドを送信した。ブレーキが保持されている間、解放中、保持への移行中の`/enableServoMode 1`と`/homing`でも送信される（停止処理中と`/free`の後は除く）。 |
| HomeSwActivating | HOMEスイッチがオンの状態から原点復帰方向に移動しようとした。HOMEスイッチがすでにオンのときの`/goUntil`と`/goUntilRaw`でも送信される。**v2.2.0**: `/goUntil`と`/goUntilRaw`が、HOMEスイッチがすでにオンのときに送信します。以前は`HomeSwActivated`として送信されていました。 |
| LimitSwActivating | LIMITスイッチがオンの状態から原点復帰方向の逆向きに移動しようとした。（STEP400のみ） |
| GoUntilTimeout | `/goUntil`コマンド実行中にタイムアウトした。 |
| ReleaseSwTimeout | `/releaseSw`コマンド実行中にタイムアウトした。 |
| InServoMode | サーボモードでは実行できないコマンドを送信した。**v2.2.0**: `/goUntil`、`/goUntilRaw`、`/releaseSw`でも送信されます。 |
| BrakeReleaseFailed | `/activate 1`を送信したが、ドライバが無励磁のままだった（たとえばモータ電源がない）ため、ブレーキは保持されたままになった。v2.2.0で追加。 |
| BrakeEngagedOnHiZ | ブレーキが解放されている間に、ドライバのアラーム（過電流、過熱、電源電圧の低下）で無励磁になった結果、ブレーキを保持した。v2.2.0で追加。 |
| ServoModeCancelledOnHiZ | サーボモード中に、ドライバのアラーム（過電流、過熱、電源電圧の低下）で無励磁になった結果、サーボモードを取り消した。`/enableServoMode 1`でもう一度有効にする。v2.2.0で追加。 |
| MotorNotHiZ | ドライバのレジスタのうち、出力が無励磁のときだけ書き込めるものをコマンドが書き込もうとしたが、モータが無励磁ではなかった。励磁して位置を保っているモータは無励磁ではない。先に`/softHiZ`か`/hardHiZ`を送る。何も適用されない。v2.2.0で追加。 |
| MotorNotStopped | 停止中か無励磁のときだけ書き込めるドライバのレジスタをコマンドが書き込もうとしたが、モータが回転していた。何も適用されない。v2.2.0で追加。 |

#### 説明

コマンドの実行時にエラーが発生した場合に送信されます。  
[`/reportError`](system-settings.md#reporterror)によって、送信の有効/無効を切り替えることができます。

255（全モータ）のとき、モータの状態に依存するエラー（`MotorNotHiZ`、`MotorNotStopped`）は、モータごとに判定されます。必要な状態のモータは変更され、他のモータはエラーを返します。

#### 変更

- **v2.2.0**: 新しいエラー: `BrakeReleaseFailed`、`BrakeEngagedOnHiZ`、`ServoModeCancelledOnHiZ`（電磁ブレーキとサーボモード）、`MotorNotHiZ`と`MotorNotStopped`（特定の状態でしか書き込めないレジスタ）。いずれも[`/reportError`](system-settings.md#reporterror)に従います。
- **v2.2.0**: `CommandIgnored`は、値がコマンドの範囲外のときにも返され、何も適用されません: 65535を超える[`/setPositionReportInterval`](motor-driver-settings.md#setpositionreportinterval)と[`/setPositionListReportInterval`](motor-driver-settings.md#setpositionlistreportinterval)（リストは255）、0未満の[`/setGoUntilTimeout`](homing.md#setgountiltimeout)と[`/setReleaseSwTimeout`](homing.md#setreleaseswtimeout)、0〜3の範囲外のフルステップまたは0〜127の範囲外のマイクロステップの[`/setElPos`](position-management.md#setelpos)、負のゲインの[`/setServoParam`](servo-mode_reference.md#setservoparam)、0〜65535の範囲外の[`/setBrakeTransitionDuration`](brake.md#setbraketransitionduration)、127を超えるTON_MINまたはTOFF_MINの[`/setDecayModeParam`](voltage-and-current-mode-settings.md#setdecaymodeparam)。
- **v2.2.0**: `MotorIdNotMatch`は、0〜255の範囲外のモータIDに対して、送信された値とともに返されます。以前は、257と511が1と255として読まれていました。
- **v2.2.0**: `HomeSwActivating`は、HOMEスイッチがオンのときの`/goUntil`と`/goUntilRaw`が返します。以前は`HomeSwActivated`として送信され、今は他のコマンドのエラーと同じように`/reportError`に従います。
<!-- generated:end osc-message /error/command -->

## 状態の通知

<!-- osc-message: /busy -->
<!-- generated:begin osc-message /busy -->
### `/busy` (int)motorID (int)state {#busy}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| state | int |  |  |

`state`

| 値 | 意味 |
| --- | --- |
| 1 | BUSYの場合 |
| 0 | BUSYでない場合 |
<!-- generated:end osc-message /busy -->

<!-- osc-message: /HiZ -->
<!-- generated:begin osc-message /HiZ -->
### `/HiZ` (int)motorID (int)state {#hiz}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| state | int | 0-1 | 1:無励磁状態の場合, 0:無励磁状態でない場合 |
<!-- generated:end osc-message /HiZ -->

<!-- osc-message: /dir -->
<!-- generated:begin osc-message /dir -->
### `/dir` (int)motorID (int)direction {#dir}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| direction | int |  |  |

`direction`

| 値 | 意味 |
| --- | --- |
| 1 | 正転方向 |
| 0 | 逆転方向 |
<!-- generated:end osc-message /dir -->

<!-- osc-message: /motorStatus -->
<!-- generated:begin osc-message /motorStatus -->
### `/motorStatus` (int)motorID (int)MOT_STATUS {#motorstatus}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| MOT_STATUS | int | 0-3 | モータの状態 |

`MOT_STATUS`

| 値 | 意味 |
| --- | --- |
| 0 | モータ停止 |
| 1 | 加速中 |
| 2 | 減速中 |
| 3 | 一定速運転中 |
<!-- generated:end osc-message /motorStatus -->

<!-- osc-message: /homingStatus -->
<!-- generated:begin osc-message /homingStatus -->
### `/homingStatus` (int)motorID (int)homingStatus {#homingstatus}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| homingStatus | int | 0-4 | 原点復帰の状態 |

##### 原点復帰の状態

| homingStatus | 原点復帰の状態 | 説明 |
| --- | --- | --- |
| 0 | HOMING_UNDEFINED | 原点復帰をまだしていない状態 |
| 1 | HOMING_GOUNTIL | `/goUntil`実行中 |
| 2 | HOMING_RELEASESW | `/releaseSw`実行中 |
| 3 | HOMING_COMPLETED | 原点復帰完了 |
| 4 | HOMING_TIMEOUT | 規定時間内に動作が完了しなかった |
<!-- generated:end osc-message /homingStatus -->

<!-- osc-message: /position -->
<!-- generated:begin osc-message /position -->
### `/position` (int)motorID (int)ABS_POS {#position}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| ABS_POS | int | -2097152-2097151 | 現在位置 |
<!-- generated:end osc-message /position -->

<!-- osc-message: /positionList -->
<!-- generated:begin osc-message /positionList -->
### `/positionList` (int)position1 ... (int)positionN {#positionlist}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| position1 ... positionN | int | -2097152-2097151 | n個目のモータの現在位置 |
<!-- generated:end osc-message /positionList -->

<!-- osc-message: /homeSw -->
<!-- generated:begin osc-message /homeSw -->
### `/homeSw` (int)motorID (int)swState (int)direction {#homesw}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| swState | int |  | 状態 |
| direction | int |  | 方向 |

`swState`

| 値 | 意味 |
| --- | --- |
| 0 | オフ |
| 1 | オン |

`direction`

| 値 | 意味 |
| --- | --- |
| 1 | 正転方向 |
| 0 | 逆転方向 |
<!-- generated:end osc-message /homeSw -->

<!-- osc-message: /swEvent -->
<!-- generated:begin osc-message /swEvent -->
### `/swEvent` (int)motorID {#swevent}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
<!-- generated:end osc-message /swEvent -->

<!-- osc-message: /limitSw -->
<!-- generated:begin osc-message /limitSw -->
### `/limitSw` (int)motorID (int)swState (int)direction {#limitsw}

STEP400のみ。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| swState | int |  | 状態 |
| direction | int |  | 方向 |

`swState`

| 値 | 意味 |
| --- | --- |
| 0 | オフ |
| 1 | オン |

`direction`

| 値 | 意味 |
| --- | --- |
| 1 | 正転方向 |
| 0 | 逆転方向 |
<!-- generated:end osc-message /limitSw -->

## アラームの通知

<!-- osc-message: /uvlo -->
<!-- generated:begin osc-message /uvlo -->
### `/uvlo` (int)motorID (int)state {#uvlo}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| state | int |  |  |

`state`

| 値 | 意味 |
| --- | --- |
| 1 | UVLO発生状態 |
| 0 | UVLO発生無し |

#### 変更

- **v2.2.0**: 電源電圧の低下（UVLO）の状態が変わったときの通知（[`/enableUvloReport`](alarm-settings.md#enableuvloreport)で有効にします）は、[`/getUvlo`](alarm-settings.md#getuvlo)への返信と同じく、整数の型タグ`i`（0 / 1）で送信されます。以前の通知は`T` / `F`でした。`T` / `F`を想定しているクライアントは、更新が必要です。
<!-- generated:end osc-message /uvlo -->

<!-- osc-message: /thermalStatus -->
<!-- generated:begin osc-message /thermalStatus -->
### `/thermalStatus` (int)motorID (int)thermalStatus {#thermalstatus}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |
| thermalStatus | int | 0-3 | 温度の状態 |

##### 温度の状態 - STEP400

| thermalStatus | 温度の状態 | 発生条件 | 解除条件 | 説明 |
| --- | --- | --- | --- | --- |
| 0 | Normal | - | - | 通常 |
| 1 | Warning | 135℃ | 125℃ | 温度警告。動作は制限されません。 |
| 2 | Bridge shutdown | 155℃ | 145℃ | 過熱遮断。ブリッジを止めます。 |
| 3 | Device shutdown | 170℃ | 130℃ | 過熱遮断。内部の電源も止めます。 |

##### 温度の状態 - STEP800

| thermalStatus | 温度の状態 | 発生条件 | 解除条件 | 説明 |
| --- | --- | --- | --- | --- |
| 0 | Normal | - | - | 通常 |
| 1 | Warning | 130℃ | 130℃ | 温度警告。動作は制限されません。 |
| 2 | Bridge shutdown | 160℃ | 130℃ | 過熱遮断。ブリッジを止めます。 |
<!-- generated:end osc-message /thermalStatus -->

<!-- osc-message: /overCurrent -->
<!-- generated:begin osc-message /overCurrent -->
### `/overCurrent` (int)motorID {#overcurrent}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |

#### 説明

過電流の状態が始まったときにすぐ送信し（直近200msにそのモータの同種の通知がなかった場合）、状態が続く間はモータごとに最短200msの間隔で送信します。200msの間の検出は失われず、その間隔の終わりに1つのメッセージとして送信されます。通知が無効の間（[`/enableOverCurrentReport`](alarm-settings.md#enableovercurrentreport)）の検出は、後から送信されません。

#### 変更

- **v2.2.0**: 状態が始まったときにすぐ送信し（直近200msにそのモータの同種の通知がなかった場合）、状態が続く間はモータごとに最短200msの間隔で送信します。以前は、状態が続く間、STATUSレジスタを読み出すたびに（10msごとに）送信していました。メッセージ自体は変わりません。
<!-- generated:end osc-message /overCurrent -->

<!-- osc-message: /stall -->
<!-- generated:begin osc-message /stall -->
### `/stall` (int)motorID {#stall}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| motorID | int | 1-4（STEP400）、1-8（STEP800） | モータのID |

#### 説明

ストールの状態が始まったときにすぐ送信し（直近200msにそのモータの同種の通知がなかった場合）、状態が続く間はモータごとに最短200msの間隔で送信します。200msの間の検出は失われず、その間隔の終わりに1つのメッセージとして送信されます。通知が無効の間（[`/enableStallReport`](alarm-settings.md#enablestallreport)）の検出は、後から送信されません。

ストール検出は、モータが負荷に負けて回れなくなった状態を、ドライバが電流から検出する機能です。閾値（[`/setStallThreshold`](alarm-settings.md#setstallthreshold)）は、実際に流れている電流にできるだけ近く、少し上になるように探って決めます。脱調（ステップのずれ）程度の小さなずれは検出できませんが、位置が大きくずれたときには検出できることがあります。

#### 変更

- **v2.2.0**: 状態が始まったときにすぐ送信し（直近200msにそのモータの同種の通知がなかった場合）、状態が続く間はモータごとに最短200msの間隔で送信します。以前は、状態が続く間、STATUSレジスタを読み出すたびに（10msごとに）送信していました。メッセージ自体は変わりません。
<!-- generated:end osc-message /stall -->
