---
title: microSDカードでの設定
---

# microSDカードでの設定

設定ファイルを書き込んだmicroSDカードをボードに差し込んで起動すると、ファイルに書かれた設定でボードを設定できます。このページでは、カードの準備、ボードが読むファイル、ボードがカードに設定を保存する方法を説明します。設定の全体像は[設定の仕組み](how-settings-work.md)をご覧ください。

カードがないとき、または有効なファイルがないときに起動すると、ボードはファームウェアの初期値を使います。

## カードの準備 {#card}

**FAT16またはFAT32**でフォーマットしたmicroSDカードを使ってください。**exFATは使えません。**

- 64GB以上のSDXCカードは、初期状態ではexFATです。FAT32でフォーマットし直してください（macOSのディスクユーティリティでは「MS-DOS（FAT）」を選びます）。
- ボードは、exFATのカードを、カードがないものとして扱い、中身には触れません。読み込みはできず、保存は`No SD card`で失敗します。
- FAT16のルートフォルダには、512エントリまでしか置けません。長いファイル名は、1つで複数のエントリを使います。ファイルを多く置くときは、FAT32にしてください。

> **v2.2.0から:** Arduino IDEでビルドしたファームウェアも、exFATのカードを、カードがないものとして扱います。以前のArduino IDEのビルドでは、exFATのカードに設定を保存すると、カードの中のファイルが消えていました。

## ボードが読むファイル {#files}

### 順序 {#order}

ボードは、次の順にファイルを探します。

1. カードのルートフォルダにある`config.txt`。
2. `config.txt`がないとき、または解析できないとき: ルートフォルダで、アルファベット順に最初の`*.json`ファイル。拡張子の大文字と小文字は区別しません。
3. 有効なファイルがないとき: 初期値。

最初の`.json`ファイルが有効でないとき（JSONではない、または`information.configVersion`がない）は、次の`.json`ファイルには進まず、初期値を使います。**v2.2.0からは、受け付けなかったファイルの値は、まったく適用しません。**

従って、以前の`config.txt`はそのまま使えます。新しいカードには、`STEP800_ST-42BYH1684_24V.json`のように、好きな名前のファイルを置けます。

### ファイル名 {#names}

- 長いファイル名を使えます。先頭の`/`を含めたパスは、**63文字まで**です。
- `.`で始まるファイルとフォルダは無視します。macOSは、FATのカードにファイルをコピーするたびに、`._*`のファイルや`.Trashes`を作ります。これらが本物のファイルを隠してしまうのを防ぐためです。
- サブフォルダの中は探しません。ファイルはルートフォルダに置いてください。

## カードを読むとき {#when-read}

**ボードがカードを読むのは、起動するときだけです。** 起動したあとにカードを挿したときは、ボードを再起動してください。起動したあとにカードを抜くと、設定は起動時のままで、保存は`SD open failed`で失敗します。

ボードが何を読んだかは、[`/getConfigName`](../reference/system-settings.md#getconfigname)やUSBシリアルの出力で確かめられます。[設定の仕組み](how-settings-work.md#at-start)をご覧ください。

## カードへの保存 {#saving}

### 保存先 {#save-target}

[`/saveConfig`](../reference/system-settings.md#saveconfig)、[ブラウザ設定ツール](browser-config-tool.md)の**Save to SD**ボタン、USBシリアルのコマンド`{`は、起動時に読んだファイルに設定を保存します。ファイルを読んでいないときは、`/config.txt`に保存します。ファイル名は、次の再起動まで変えられます（下記）。

ボードは、同じフォルダの隠しファイル`.<名前>.tmp`に設定を書き、書き込んで閉じてから、保存先のファイルをそれで置き換えます。書き込みに失敗したときは、保存先のファイルは元のままです。

**v2.2.0の既知の問題:** 設定ファイルなしで起動した（カードがない、または有効なファイルがない）ボードで保存すると、ボードには書くべきバージョンと製品がありません。ファイルの`information.configVersion`は`[-1, 0]`、`information.targetProduct`は`"---"`になります。値は保存され、次の起動でボードはそのファイルを読みますが、診断には、設定のバージョンが-1.0、"Config and product match"がfalseと表示されます。正しいバージョンと製品のファイルが必要なときは、[ブラウザ設定ツール](browser-config-tool.md)（**Download JSON**）で作ってください。また、保存では`canSendMsgBeforeDestIp`が正しく書かれないことがあります。[`network.canSendMsgBeforeDestIp`](configuration-items.md#network-cansendmsgbeforedestip)をご覧ください。

保存の間は、ボードの処理が少しの間止まります。保存する前に、モータを止めてください。[保存の間](how-settings-work.md#saving)をご覧ください。

### エラー {#errors}

| メッセージ | 意味と原因 |
| --- | --- |
| `No SD card` | ボードに書き込めるカードがありません。起動時にカードが挿されていなかった、カードがexFATである、またはカードを初期化できなかった場合です |
| `SD open failed` | カードに書き込めませんでした。起動後にカードを抜いた、カードまたはルートフォルダがいっぱい、ファイル名のフォルダがない、または書き込みエラーの場合です。保存先のファイルは元のままです |

OSCコマンド`/saveConfig`は、同じ文字列を`/error/saveConfig`で返します。ボードがファイルを置き換えている間に電源が切れると、一時ファイルだけが残ることがあります。ボードは、次の起動で、それを復旧しません。

### `F<path>`で決めた名前 {#f-path}

USBシリアルのコマンド`F<path>`で、次の再起動まで、ボードが保存するファイルを変えられます。ボードは、`/`で始まり、`.json`か`.txt`で終わる、63文字までの名前なら、何でも受け付けます。

ボードは、それより長い名前も拒否しません。**64バイト以上の名前は、エラーなしで63バイトに切られ**（v2.2.0）、切られた名前で保存されます。

**起動時にボードが読むのは、ルートフォルダの`config.txt`と`*.json`だけです。** `/foo.txt`やサブフォルダに保存した設定は、次の起動で読まれません。ブラウザ設定ツールは、この場合に警告を出します。

## 設定ファイルの作り方 {#making}

!!! warning "ファイルの値には、ファームウェアが範囲を検査しないものがあります"
    範囲の検査は、OSCコマンドを送ったときと、[ブラウザ設定ツール](browser-config-tool.md)が行います。**ボードが設定ファイルを読むときは、範囲を検査しない値があります。** 最も重要なのは**TVAL**です。OSCコマンドは64（約5A）に制限しますが、ファイルでは制限されません。127までの値がそのままドライバに書かれ、モータとドライバに大きな電流（STEP400で127なら約10A）が流れることがあります。過電流の閾値とストールの閾値も検査されないので、範囲外の値にすると、意図と違う閾値になります。すべての値を、[設定項目一覧](configuration-items.md)の範囲に収めてください。USBシリアルのコマンド`{`で送る設定も同じです。

- [ブラウザ設定ツール](browser-config-tool.md)で: USBでボードから設定を読むか、ファイルから始めて、値を編集し、カードに保存するか、ファイルをダウンロードします。
- 例から: いくつかのモータの設定ファイルが、リポジトリの[configGeneratorフォルダ](https://github.com/ponoor/step-series-support/tree/main/configGenerator)にあります。[モータ別のパラメータ例](example-parameters.md)をご覧ください。
- OSCコマンドで: コマンドを送ってから、[`/saveConfig`](../reference/system-settings.md#saveconfig)を送ります（ファームウェアv2.1.0以降）。カードを抜く必要はありません。

ファイルの項目は[設定項目一覧](configuration-items.md)にあります。

## 古いファームウェア（v2.1.0より前） {#legacy}

v2.1.0より前のファームウェアが読むのは、ルートフォルダの`config.txt`という名前のファイルだけです。古いSDライブラリが短いファイル名しか扱えなかったため、JSONのファイルの拡張子は`.txt`でした。このファームウェアには、製品ごとの設定ツールを使います。ページの末尾の"Export"ボタンで`config.txt`をダウンロードし、カードのルートフォルダにコピーして、ボードを起動またはリセットします。設定は起動時にだけ読み込まれます。

| 機種 | URL | ソース（GitHub） |
| --- | --- | --- |
| STEP400 | <http://ponoor.com/tools/step400-config/> | [/configTool](https://github.com/ponoor/STEP400/tree/master/configTool) |
| STEP800 | <http://ponoor.com/tools/step800-config/> | [/configTool](https://github.com/ponoor/STEP800/tree/master/configTool) |

## 設定項目 {#items}

設定ファイルの項目、初期値、範囲、変更するコマンドは、[設定項目一覧](configuration-items.md)にあります。

## 関連するコマンド {#related}

<!-- osc-related: /getConfigName, /saveConfig -->
<!-- generated:begin osc-related /getConfigName, /saveConfig -->
**関連するコマンド**

| コマンド | 引数 | 説明 |
| --- | --- | --- |
| [`/getConfigName`](../reference/system-settings.md#getconfigname) | - | `/configName`を返します。設定名、microSDカードを使えたか、設定ファイルを開けたか・解析できたか、設定ファイルのパスが含まれます。 |
| [`/saveConfig`](../reference/system-settings.md#saveconfig) | - | 現在動作中の設定を、JSONファイルとしてmicroSDカードに保存します。保存先は、起動時に読み込んだファイルです。ファイルを読み込まなかったときは`/config.txt`です。USBシリアルの`F<path>`で、保存先のパスを変えられます。 |
<!-- generated:end osc-related /getConfigName, /saveConfig -->
