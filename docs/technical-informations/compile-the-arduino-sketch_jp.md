## Arduinoスケッチのコンパイル
ファームウェアのアップデートやカスタマイズを行うためには、お手元の環境でSTEPシリーズ用のArduinoスケッチをコンパイルして書き込めるようにする必要があります。大きく分けて
- PlatformIOでコンパイルする
- 純正Arduino環境でコンパイルする

という二つの方法があります。

### PlatformIOでコンパイルする
STEPシリーズのファームウェアは [PlatformIO](https://platformio.org/) を使って開発しています。

ファームウェアの[リポジトリ](https://github.com/ponoor/step-series-universal-firmware)をクローン、または"Download ZIP"から落としたファイルを解凍し、そのフォルダをPlatformIOから開けば、初回コンパイル時に必要なファイルはすべて自動でインストールされます。
![file](https://ponoor.com/cms/wp-content/uploads/2020/08/image-1648187813165.png)

このファイルはSTEPシリーズに共通で使えるものですが、コンパイルする前にターゲットの機種を指定しておく必要があります。下記の「コンパイルするターゲットの設定」を参照してください。

### 純正Arduino環境でコンパイルする
[Arduino.cc](https://www.arduino.cc/) からダウンロードできる純正のIDEを用いてコンパイルする場合は、事前に以下の作業が必要です。
- Arduino Zeroをコンパイルできるようにする
- 必要なライブラリをインストールする
- スケッチをダウンロードする

以下このページではこの手順を説明していきます。

#### Arduino Zeroをコンパイルできるようにする
STEPシリーズは[Arduino Zero](https://www.arduino.cc/en/Main/ArduinoBoardZero&)互換です。Arduino IDEのBoards Managerから、"Arduino SAMD Boards (32-bits ARM Cortex-M0+)" をインストールしてください。
手順は下記ページの"Quick Start"に説明されています。

https://docs.arduino.cc/hardware/zero

#### ライブラリのインストール
以下のライブラリをArduino IDEの「ライブラリを管理...」よりインストールします。ライブラリをインストールする詳しい手順は[こちら](https://www.arduino.cc/en/guide/libraries)を参照してください。
- [OSC Library](https://github.com/CNMAT/OSC)
- [ArduinoJSON](https://arduinojson.org/)
- [Adafruit SleepyDog Arduino Library](https://github.com/adafruit/Adafruit_SleepyDog)
- STEP400/STEP100の場合 : [Ponoor PowerSTEP01 Library](https://github.com/ponoor/Ponoor_PowerSTEP01_Library)
- STEP800/STEP200の場合 : [Ponoor L6470 Library](https://github.com/ponoor/Ponoor_L6470_Library)

#### OSC libraryの注意点
OSCのためのライブラリはいくつか種類がありますが、CNMATの[OSC Library](https://github.com/CNMAT/OSC)をインストールします。Arduino IDEの「ライブラリを管理」から "OSC" という名称のライブラリをインストールしてください。製作者が組織名のCNMATではなく、Adrian Freed, Yotam Mann という個人名で表示されていますのでご注意ください。

![](http://ponoor.com/manage/wp-content/uploads/2020/09/OSC_library_manager.png)

#### Arduino IDE用スケッチファイルの入手
書き込むArduinoスケッチはこちらから入手できます。

https://github.com/ponoor/step-series-universal-firmware/releases

ここから最新版のリリースの "Assets" をクリックし、`step-series-universal-firmware.zip`をダウンロードして解凍してください。

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643348613641.png)

解答したフォルダの`.ino`ファイルをArduino IDEで開いてください。

#### コンパイルするターゲットの設定
`boardsDef.h`の冒頭にボードのリストがあります。ここから、コンパイルしたいターゲットのコメント`//`を外してください。例えばSTEP400用にコンパイルしたい場合は以下のようになります。
```
// Products
#define STEP400_R1
// #define STEP800_R1

// X-Nucleos
// #define STEP100_R1 // X-NUCLEO-IHM03A1, PowerSTEP01 x1
// #define STEP200_R1 // X-NUCLEO-IHM02A1, L6470 x2 
```

#### コンパイルと書き込み
Arduino IDEで “Tools” -> “Boards” から “Arduino Zero (Native USB port)” を選択し、コンパイルしてください。

エラーなく完了できたら、書き込みに進みます。PCとArduinoをUSBで接続し、”Tools” -> “Port” からシリアルポートを選択し、書き込みします。
## 書き込み時の留意点
- STEP400で電磁ブレーキ基板を接続している場合は、スケッチ書き込み時は取り外してください。書き込み時にch.4の電磁ブレーキが解放されるため、負荷の落下が起こる可能性があります。これはArduino Zeroのブートローダの設定によるものです。STEP800の場合は電磁ブレーキの制御方法が異なるため、接続したままでも問題ありません。
- 基板にUSBのみを接続した場合、スケッチの書き込みはできますが、モータドライバのチップが起動しないので、ドライバとメッセージのやり取りが発生する操作はできません。
- Arduino Zero の癖なのか、書き込みに失敗することがあるようです。その場合はRESETスイッチをダブルクリックして、bootloaderモードにして再試行してみてください。bootloaderモードではスケッチは起動せず、Lがゆっくりフェードする状態になります。また普通に起動した時とは別のシリアルポートになりますので、Arduino IDEのToolsメニューから選択しなおしてください。