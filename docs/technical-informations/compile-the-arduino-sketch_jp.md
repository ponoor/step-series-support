## Arduinoスケッチのコンパイル
ファームウェアのアップデートやカスタマイズを行うためには、お手元の環境でSTEP400用のArduinoスケッチをコンパイルして書き込めるようにする必要があります。大きく分けて
- PlatformIOでコンパイルする
- 純正Arduino環境でコンパイルする

という二つの方法があります。

### PlatformIOでコンパイルする
STEP400のファームウェアはVisual Studio Codeの機能拡張 [PlatformIO](https://platformio.org/) を使って開発しています。[STEP400リポジトリ](https://github.com/ponoor/STEP400)の [`STEP400/firmware-platformio/STEP400_firmware/`](https://github.com/ponoor/STEP400/tree/master/firmware-platformio/STEP400_firmware) フォルダをPlatformIOから開けば、初回コンパイル時に必要なファイルはすべて自動インストールされます。

### 純正Arduino環境でコンパイルする
[Arduino.cc](https://www.arduino.cc/) からダウンロードできる純正のIDEを用いてコンパイルする場合は、事前に以下の作業が必要です。
- Arduino Zeroをコンパイルできるようにする
- 必要なライブラリをインストールする
- スケッチをダウンロードする

以下このページではこの手順を説明していきます。

## Arduino Zeroをコンパイルできるようにする
STEP400は[Arduino Zero](https://www.arduino.cc/en/Main/ArduinoBoardZero&)互換です。Arduino IDEのBoards Managerから、"Arduino SAMD Boards (32-bits ARM Cortex-M0+)" をインストールしてください。この手順は以下のページが参考になります。

[Getting started with the Arduino Zero](https://www.arduino.cc/en/Guide/ArduinoZero)


## ライブラリのインストール
### インストールするライブラリ
以下のライブラリをArduino IDEの「ライブラリを管理...」よりインストールします。ライブラリをインストールする詳しい手順は[こちら](https://www.arduino.cc/en/guide/libraries)を参照してください。
- [OSC Library](https://github.com/CNMAT/OSC)
- [ArduinoJSON](https://arduinojson.org/)
- [Adafruit SleepyDog Arduino Library](https://github.com/adafruit/Adafruit_SleepyDog)
- [Ponoor PowerSTEP01 Library](https://github.com/ponoor/Ponoor_PowerSTEP01_Library)

### OSC libraryの注意点
OSCのためのライブラリはいくつか種類がありますが、CNMATの[OSC Library](https://github.com/CNMAT/OSC)をインストールします。Arduino IDEの「ライブラリを管理」から "OSC" という名称のライブラリをインストールしてください。製作者が組織名のCNMATではなく、Adrian Freed, Yotam Mann という個人名で表示されていますのでご注意ください。

![](http://ponoor.com/manage/wp-content/uploads/2020/09/OSC_library_manager.png)

## スケッチのコンパイル
[STEP400のGithubリポジトリ](https://github.com/ponoor/STEP400)からファイルをクローンします。gitのシステムに詳しくない場合は右上の`Code`から`Download ZIP`を選択すればZIP形式でダウンロードできます。

![file](https://ponoor.com/cms/wp-content/uploads/2020/08/image-1617454087280.png)

`/STEP400_firmware` フォルダの`STEP400_firmware.ino`をArduino IDEで開いてください。Tools -> Boards から "Arduino Zero (Native USB port)" を選択し、コンパイルしてください。

## 書き込み時の留意点
- 電磁ブレーキ基板を接続している場合は、スケッチ書き込み時は取り外してください。書き込み時にch.4の電磁ブレーキが解放されるため、負荷の落下が起こる可能性があります。これはArduino Zeroのブートローダの設定によるものです。
- 基板にUSBのみを接続した場合、スケッチの書き込みはできますが、モータドライバのチップが起動しないので、ドライバとメッセージのやり取りが発生する操作はできません。
- Arduino Zero の癖なのか、書き込みに失敗することがあるようです。その場合はRESETスイッチをダブルクリックして、bootloaderモードにして再試行してみてください。bootloaderモードではスケッチは起動せず、Lがゆっくりフェードする状態になります。また普通に起動した時とは別のシリアルポートになりますので、Arduino IDEのToolsメニューから選択しなおしてください。