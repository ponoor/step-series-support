---
title: ボード全体の設定
---

# ボード全体の設定

ボードの通信とメッセージの仕組みは、[通信とメッセージ](../guides/communication-and-messages.md)をご覧ください。

<!-- osc: /setDestIp -->
<!-- generated:begin osc /setDestIp -->
### `/setDestIp` {#setdestip}

#### 引数

なし

#### 実行可能タイミング

常時

#### 説明

モータの状態に変化があったときに通知するメッセージや、問い合わせへ返信するメッセージなどの送り先IPアドレス（`destIp`）を指定します。このメッセージを送信したIPアドレスを`destIp`に設定します。

また、`destIp`が設定されるまでは、ボードからOSCメッセージの送信は行いませんので、一番最初にこのコマンドを送信してください。唯一の例外は[`/booted`](automatically-sent-messages.md#booted)メッセージです。

Config Toolの設定を用いて、`destIp`が設定されていなくてもOSCメッセージを送信できるように設定できます。

MACアドレスの解決のために、宛先のUDPポート9（discard）に1バイトを送信します。MacはICMPのport unreachableを返しますが、ボードには影響しません。ボードが動作しているかを確認するには、`/setDestIp`ではなく、[`/getVersion`](system-settings.md#getversion)のように返信のあるコマンドを使ってください。

#### 変更

- **v2.2.0**: この`/setDestIp`が宛先のMACアドレスの解決を始めたときは、解決が終わってから返信の`/destIp`を送信します。そのため、以前より遅れて届くことがあります（有線では数ms、Wi-Fiでは最大数秒）。届かないときは、もう一度`/setDestIp`を送ってください。解決を始めない`/setDestIp`（たとえば死活監視として毎秒送るもの）には、すぐに返信します。
- **v2.2.0**: MACアドレスの解決中（最大数秒）は、宛先へのメッセージ（返信、通知、エラー）は破棄されます。ブロードキャストの`/booted`は送信されます。
- **v2.2.0**: 同じIPアドレスの別のデバイス（別のPCやネットワークアダプタ）から、元のデバイスからの最後のパケットの1.5秒以上後に`/setDestIp`を受け取ると、ボードは新しいデバイスへ送信するようになります。以前は、ボードが再起動するまで古いMACアドレスへ送信し続けていました。
- **v2.2.0**: ARPの応答が一度もない宛先（たとえば誤った宛先アドレス）への送信は、処理を約41ms止めます（以前は1.6秒以上）。これがメッセージごとに起きることはなくなり、その宛先への送信を1秒間止めます。その間のメッセージは破棄され、後から送られることはありません。その宛先からパケットを受信すると、送信はすぐに再開します。ブロードキャストの`/booted`は影響を受けません。

#### 返信

```
/destIp (int)destIp[0] (int)destIp[1] (int)destIp[2] (int)destIp[3] (int)isNewDestIp
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| destIp[0] | int | 0-255 | destIpの各桁 |
| destIp[1] | int | 0-255 | destIpの各桁 |
| destIp[2] | int | 0-255 | destIpの各桁 |
| destIp[3] | int | 0-255 | destIpの各桁 |
| isNewDestIp | int | 0-1 | destIpが変更されたかどうかを示します。変更されていると1, すでに同じアドレスが設定されていた場合は0 |

##### 変更

- **v2.2.0**: `/setDestIp`がMACアドレスの解決を始めるとき（最初の1回、別のアドレスからのとき、宛先からの最後のパケットから1.5秒以上後のとき）は、解決が終わってからこのメッセージを送信するため、最大約2秒遅れることがあります。それ以外のときはすぐに送信されます。届かないときは、もう一度`/setDestIp`を送ってください。
<!-- generated:end osc /setDestIp -->

<!-- osc: /getVersion -->
<!-- generated:begin osc /getVersion -->
### `/getVersion` {#getversion}

#### 引数

なし

#### 実行可能タイミング

常時

#### 説明

本体に書き込まれているファームウェアのバージョン情報を返します。

#### 返信

```
/version (string)version
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| version | string |  |  |
<!-- generated:end osc /getVersion -->

<!-- osc: /getConfigName -->
<!-- generated:begin osc /getConfigName -->
### `/getConfigName` {#getconfigname}

#### 引数

なし

#### 実行可能タイミング

常時

#### 説明

`/configName`を返します。設定名、microSDカードを使えたか、設定ファイルを開けたか・解析できたか、設定ファイルのパスが含まれます。

#### 返信

```
/configName (string)configName (int)sdInitializeSucceeded (int)configFileOpenSucceeded (int)configFileParseSucceeded (string)configFilename
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| configName | string |  | 設定名です（読み込んだ設定ファイルの`information.configName`）。設定ファイルを読み込まなかったとき、またはファイルに設定名がないときは`Default`です。[`/setConfigName`](system-settings.md#setconfigname)で変わります。 |
| sdInitializeSucceeded | int | 0-1 | 起動時にmicroSDカードを使えたかどうかです。使えたときは1です。カードがないとき、FAT16またはFAT32でないカード（exFATなど）のときは0です。カードは起動時にしか確認しません。 |
| configFileOpenSucceeded | int | 0-1 | `config.txt`を開けたとき、または有効な`.json`ファイルを読み込めたときは1です。どちらでもないとき（最初の`.json`ファイルが無効なときを含む）は0です。下の表を参照してください。 |
| configFileParseSucceeded | int | 0-1 | 設定ファイルを読み込んで、その値を適用したかどうかです。JSONとして解析できた`config.txt`、または有効な`.json`ファイル（`information.configVersion`がある）のときは1です。0のときは既定値で動作しています。 |
| configFilename | string |  | 読み込んだ設定ファイルのパスです。先頭に`/`が付きます（例: `/config.txt`、`/STEP400_venue-A.json`）。ファイルを読み込まなかったときは、[`/saveConfig`](system-settings.md#saveconfig)の保存先の`/config.txt`です。USBシリアルの`F<path>`で変わります。パスは63文字までです。ディスク上のパスで、ユーザーが編集できるラベルである`configName`とは別のものです。（v2.1.0で追加。） |

##### configFileOpenSucceededとconfigFileParseSucceededの組み合わせ

| configFileOpenSucceeded | configFileParseSucceeded | 意味 |
| --- | --- | --- |
| 1 | 1 | 設定ファイルを読み込んで、その値を適用しました（`config.txt`、なければ最初の有効な`.json`ファイル）。 |
| 1 | 0 | `config.txt`を開けましたが解析できず、有効な`.json`ファイルもありませんでした。既定値で動作しています。 |
| 0 | 0 | `config.txt`がなく、`.json`ファイルもないか、最初の`.json`ファイルが無効です（カードを使えなかったときも同じです）。既定値で動作しています。 |

##### 変更

- **v2.2.0**: 名前が`.`で始まるファイル（macOSがカードにコピーした各ファイルの隣に書く`._name.json`など）は、設定ファイルの候補になりません。以前は、そのようなファイルが`.json`ファイルの中で先に選ばれ、無効なため、後ろにある有効な`.json`ファイルがすべて使われませんでした。
- **v2.2.0**: 受け付けなかった設定ファイルの値は、適用されなくなりました。対象は、解析できない、または`information.configVersion`がない最初の`.json`ファイル（そこで検索を終えます）と、途中で解析に失敗した`config.txt`です。今は、カードがないときと同じように既定値で動作します。以前は、受け付けなかったファイルの値も使われていました（`configName`にはそのファイルの設定名が表示されました）。

#### 関連

[`/setConfigName`](system-settings.md#setconfigname)
<!-- generated:end osc /getConfigName -->

<!-- osc: /reportError -->
<!-- generated:begin osc /reportError -->
### `/reportError` (bool)enable {#reporterror}

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| enable | bool |  |  |

`enable`

| 値 | 意味 |
| --- | --- |
| 1 | 有効 |
| 0 | 無効 |

#### 実行可能タイミング

常時

#### 説明

[`/error/command`](automatically-sent-messages.md#error-command)および[`/error/osc`](automatically-sent-messages.md#error-osc)メッセージの自動送信の有効/無効を切り替えます。

#### 返信

[`/error/command`](automatically-sent-messages.md#error-command)

```
/error/command (string)errorText (int)motorID
```

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

[`/error/osc`](automatically-sent-messages.md#error-osc)

```
/error/osc (string)errorText
```

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

#### 初期値

- `enable`: true（有効）（[network.reportError](../connections/configuration-items.md#network-reporterror)）
<!-- generated:end osc /reportError -->

<!-- osc: /setConfigName -->
<!-- generated:begin osc /setConfigName -->
### `/setConfigName` (string)configName {#setconfigname}

v2.1.0で追加。

#### 引数

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| configName | string |  | 設定名の文字列 |

#### 実行可能タイミング

常時

#### 説明

ボードに保存される設定名を設定します。設定を見分けるためにユーザーが自由に編集できるラベルで、ディスク上のファイル名とは別のものです。

設定名は、[`/saveConfig`](system-settings.md#saveconfig)で保存するまで、ボードの中だけで変わります。変更の後すぐに[`/getConfigName`](system-settings.md#getconfigname)が新しい設定名を返しますが、保存する前に再起動すると、設定ファイルにある設定名に戻ります。

#### 初期値

- `configName`: Default（ファームウェア）、""（テンプレート）（[information.configName](../connections/configuration-items.md#information-configname)）

#### 関連

[`/getConfigName`](system-settings.md#getconfigname), [`/saveConfig`](system-settings.md#saveconfig)
<!-- generated:end osc /setConfigName -->

<!-- osc: /saveConfig -->
<!-- generated:begin osc /saveConfig -->
### `/saveConfig` {#saveconfig}

v2.1.0で追加。

#### 引数

なし

#### 実行可能タイミング

常時

#### 説明

現在動作中の設定を、JSONファイルとしてmicroSDカードに保存します。保存先は、起動時に読み込んだファイルです。ファイルを読み込まなかったときは`/config.txt`です。USBシリアルの`F<path>`で、保存先のパスを変えられます。

設定は、まず同じフォルダの隠しファイル`.<名前>.tmp`に書き込み、書き込みが終わってから、保存先のファイルを置き換えます。一時ファイルへの書き込みに失敗したときは、保存先のファイルは元のままです。

カードは起動時にしか確認しません。起動時に使えるカードがなかったとき（起動後に挿したカード、exFATのカード）は`No SD card`を返し、起動後にカードを抜いたとき、カードがいっぱいのとき、フォルダがないときは`SD open failed`を返します。保存した設定は、次の起動時に適用されます。

#### 変更

- **v2.2.0**: 設定を同じフォルダの隠しファイル`.<名前>.tmp`に書き込み、一時ファイルの書き込みと閉じる処理が終わってから、保存先のファイルを置き換えます。保存に失敗したとき（カードやフォルダがいっぱい、フォルダがない、書き込みエラー）は、保存先のファイルは元のままで、`SD open failed`を返します。以前は、先に古いファイルを削除していたため、保存に失敗するとカードに設定ファイルが残りませんでした。古いファイルを削除してから新しいファイルの名前を変えるまでの間に電源が切れたとき、または名前の変更に失敗したとき（`SD open failed`を返します）は、一時ファイルだけが残ります（起動時の回復はありません）。一時ファイルの名前は`.`で始まるため、設定ファイルとしては読み込まれません（[`/configName`](system-settings.md#getconfigname)を参照）。
- **v2.2.0**: Arduino IDE版では、exFATのカード（既定ではSDXCの64GB以上）に保存すると、カード上のファイルが消え、`SD open failed`が返っていました。今は、PlatformIO版と同じように、exFATのカードは使われず（`No SD card`）、カードの中身には何もしません。カードはFAT16またはFAT32でフォーマットしてください。

#### 返信

条件: 保存できたとき

v2.1.0で追加。

```
/saveConfig (string)message
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| message | string |  | `Saved to SD. Reboot to apply.` |

条件: 保存できなかったとき

v2.1.0で追加。

```
/error/saveConfig (string)errorText
```

| 引数 | 型 | 範囲 | 説明 |
| --- | --- | --- | --- |
| errorText | string |  |  |

`errorText`

| 値 | 意味 |
| --- | --- |
| SD open failed | 起動時にはカードを使えましたが、ファイルを書き込めませんでした。起動後にカードを抜いた、カードやフォルダがいっぱい、フォルダがない、書き込みエラー、のいずれかです。一時ファイルへの書き込みに失敗したときは、保存先のファイルは元のままです。 |
| No SD card | 起動時に使えるカードがありませんでした。カードがない、またはFAT16やFAT32でないカード（exFATなど）です。起動後に挿したカードは、ボードを再起動するまで使われません。 |

#### 関連

[`/configName`](system-settings.md#getconfigname), [`/setConfigName`](system-settings.md#setconfigname)
<!-- generated:end osc /saveConfig -->

<!-- osc: /resetDevice -->
<!-- generated:begin osc /resetDevice -->
### `/resetDevice` {#resetdevice}

#### 引数

なし

#### 実行可能タイミング

常時

#### 説明

ボード全体をリセットします。ボード上のリセットスイッチを押した場合と同じ動作です。

再起動後、[`/booted`](automatically-sent-messages.md#booted)が`resetCause` 5（ソフトウェアリセット）で送信されます。

#### 変更

- **v2.2.0**: 電磁ブレーキが有効でブレーキが保持されていない、回転中のモータをまず即停止で止め、ブレーキを保持し、それらのモータのうち最長の`brakeTransitionDuration`（最大1秒）を待ってから再起動します。ブレーキのないモータは、ファームウェアでは止められません。以前は、すぐに再起動していました。
- **v2.2.0**: ソフトウェアリセットで再起動します。`/booted`の`resetCause`は5になります。
<!-- generated:end osc /resetDevice -->
