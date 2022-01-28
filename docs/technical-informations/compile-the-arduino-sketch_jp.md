## Arduinoスケッチのコンパイル
ファームウェアのアップデートやカスタマイズを行うためには、お手元の環境でSTEPシリーズ用のArduinoスケッチをコンパイルして書き込めるようにする必要があります。大きく分けて
- PlatformIOでコンパイルする
- 純正Arduino環境でコンパイルする

という二つの方法があります。

### PlatformIOでコンパイルする
STEPシリーズのファームウェアは [PlatformIO](https://platformio.org/) を使って開発しています。STEP400/800各リポジトリにPlatformIOのデータが置いてあるフォルダがあり、このフォルダをPlatformIOから開けば、初回コンパイル時に必要なファイルはすべて自動でインストールされます。

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
- STEP400のみ : [Ponoor PowerSTEP01 Library](https://github.com/ponoor/Ponoor_PowerSTEP01_Library)
- STEP800のみ : [Ponoor L6470 Library](https://github.com/ponoor/Ponoor_L6470_Library)

### OSC libraryの注意点
OSCのためのライブラリはいくつか種類がありますが、CNMATの[OSC Library](https://github.com/CNMAT/OSC)をインストールします。Arduino IDEの「ライブラリを管理」から "OSC" という名称のライブラリをインストールしてください。製作者が組織名のCNMATではなく、Adrian Freed, Yotam Mann という個人名で表示されていますのでご注意ください。

![](http://ponoor.com/manage/wp-content/uploads/2020/09/OSC_library_manager.png)

## スケッチのコンパイル


対応する機種のリポジトリからファイルをクローンします。
<!--
| 機種 | Arduino Sketch Directory | PlatformIO Directory |
| --- | --- | ---|
| [STEP400](https://github.com/ponoor/STEP400) | [/STEP400_firmware](https://github.com/ponoor/STEP400/tree/master/STEP400_firmware) | [/firmware-platformio/STEP400_firmware](https://github.com/ponoor/STEP400/tree/master/firmware-platformio/STEP400_firmware) |
| [STEP800](https://github.com/ponoor/STEP800) | [/STEP800_firmware](https://github.com/ponoor/STEP800/tree/main/STEP800_firmware) | [/firmware-platformIO/STEP800_firmware](https://github.com/ponoor/STEP800/tree/main/firmware-platformIO/STEP800_firmware) |
-->

| 機種 | リポジトリ | Releases | 
| --- | --- | --- |
| STEP400 | https://github.com/ponoor/STEP400 | https://github.com/ponoor/STEP400/releases |
| STEP800 | https://github.com/ponoor/STEP800 | https://github.com/ponoor/STEP800/releases |

あるいは、上記リポジトリのReleasesからzipファイルを入手できます。最新版のReleaseのAssetsから、`STEP400_firmware.zip`または`STEP800_firmware.zip`をダウンロードしてください。このzipファイルは、Arduino IDEでのコンパイルに必要なファイルのみが圧縮されています。

Arduinoスケッチフォルダの`.ino`ファイルをArduino IDEで開いてください。Tools -> Boards から "Arduino Zero (Native USB port)" を選択し、コンパイルしてください。

## 書き込み時の留意点
- STEP400で電磁ブレーキ基板を接続している場合は、スケッチ書き込み時は取り外してください。書き込み時にch.4の電磁ブレーキが解放されるため、負荷の落下が起こる可能性があります。これはArduino Zeroのブートローダの設定によるものです。STEP800の場合は電磁ブレーキの制御方法が異なるため、接続したままでも問題ありません。
- 基板にUSBのみを接続した場合、スケッチの書き込みはできますが、モータドライバのチップが起動しないので、ドライバとメッセージのやり取りが発生する操作はできません。
- Arduino Zero の癖なのか、書き込みに失敗することがあるようです。その場合はRESETスイッチをダブルクリックして、bootloaderモードにして再試行してみてください。bootloaderモードではスケッチは起動せず、Lがゆっくりフェードする状態になります。また普通に起動した時とは別のシリアルポートになりますので、Arduino IDEのToolsメニューから選択しなおしてください。