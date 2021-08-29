### `/setDestIp`
#### アーギュメント
なし

#### 実行可能タイミング
常時

#### 説明
モータの状態に変化があったときに通知するメッセージや、問い合わせへ返答するメッセージなどの送り先IPアドレス(`destIp`)を指定します。このメッセージを送信したIPアドレスを`destIp`に設定します。

また、`destIp`が設定されるまでは、本デバイスからOSCメッセージの送信は行いませんので、一番最初にこのコマンドを送信してください。唯一の例外は [`/booted`](https://ponoor.com/docs/step-series/osc-command-reference/automatically-sent-messages-from-step-400/#booted) メッセージです。

Config Toolの設定を用いて、`destIp`が設定されていなくてもOSCメッセージを送信できるように設定できます。

#### 返答

```
/destIp (int)destIp[0] (int)destIp[1] (int)destIp[2] (int)destIp[3] (bool)isNewDestIp
```
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| destIp[0-3] | 0-255| destIpの各桁 |
| isNewDestIp | 0-1 | destIpが変更されたかどうかを示します。変更されていると1, すでに同じアドレスが設定されていた場合は0 |

#### 初期値
10.0.0.10

### `/getVersion`
#### アーギュメント
なし

#### 実行可能タイミング
常時

#### 説明
本体に書き込まれているファームウェアのバージョン情報を返します。

#### 返答

```
/version (Symbol)firmwareName (Symbol)firmwareVersion (Symbol)compileDate
```
| アーギュメント | 説明 |
| --- | --- |
| firmwareName | ファームウェアの名称。 |
| firmwareVersion | ファームウェアのバージョン |
| compileDate | ファームウェアがコンパイルされた日時 |

### `/getConfigName`
#### アーギュメント
なし

#### 実行可能タイミング
常時

#### 説明
起動時にmicroSDカードから読み込まれたコンフィギュレーションファイルの名称を返します。

#### 返答

```
/configName (Symbol)configName (bool)sdInitializeSucceeded (bool)configFileOpenSucceeded
```
| アーギュメント | 説明 |
| --- | --- |
| configName | コンフィギュレーションの名称。 |
| sdInitializeSucceeded | microSDカードとの通信に成功したかどうか |
| configFileOpenSucceeded | コンフィギュレーションファイルを開くことができたかどうか |

### `/reportError (bool)enable`
#### アーギュメント
| アーギュメント | 範囲 | 説明 |
| --- | --- | --- |
| enable | 0-1 | 1で有効, 0で無効 |

#### 実行可能タイミング
常時

#### 説明
[`/error/command`](https://ponoor.com/docs/step-series/osc-command-reference/automatically-sent-messages-from-step-400/#errorcommand) および [`/error/osc`](https://ponoor.com/docs/step-series/osc-command-reference/automatically-sent-messages-from-step-400/#errorosc) メッセージの自動送信の有効/無効を切り替えます。

#### 初期値
1 (有効)
