---
title: Arduinoスケッチの書き込み
wp_id: 2210
slug: upload-the-sketch
lang: ja
link: "https://ponoor.com/docs/step100-200/upload-the-sketch/"
date: "2022-01-28T16:18:29"
modified: "2022-03-29T10:36:06"
parent: 2164
menu_order: 25
---

# Arduinoスケッチの書き込み

## PlatformIOを使う場合

### ファームウェアの入手

<https://github.com/ponoor/step-series-universal-firmware>

このファームウェアはPlatformIOを使って開発されているので、上記リポジトリをクローンしてPlatfromIOで開けば、必要なライブラリのダウンロード、コンパイル、アップロードが可能です。  
このファームウェアはSTEPシリーズに共通で使えるものですが、コンパイルする前にターゲットの機種を指定しておく必要があります。下記の「[コンパイルするターゲットの設定](https://ponoor.com/docs/step100-200/upload-the-sketch/#i-3)」を参照してください。

### envの選択

`platformio.ini`にはArudino Zero (`zeroUSB`)とArduino M0 (`mzeroUSB`)の2つの環境の設定が書かれています。どちらか必要な方を残して、不要な方を`;`でコメントアウトしてください。

```
[env:zeroUSB]
platform = atmelsam
board = zeroUSB
framework = arduino
lib_deps = 
    arduino-libraries/Ethernet@^2.0.0
    arduino-libraries/SD@^1.2.4
    cnmat/OSC@0.0.0-alpha+sha.41b44981e3
    adafruit/Adafruit SleepyDog Library@^1.4.0
    bblanchon/ArduinoJson@^6.18.4
    https://github.com/ponoor/Ponoor_L6470_Library/archive/refs/tags/v1.0.3.zip
    ponoor/Ponoor PowerSTEP01 Library@^1.0.2

[env:mzeroUSB]
platform = atmelsam
board = mzeroUSB
framework = arduino
lib_deps = 
    arduino-libraries/Ethernet@^2.0.0
    arduino-libraries/SD@^1.2.4
    cnmat/OSC@0.0.0-alpha+sha.41b44981e3
    adafruit/Adafruit SleepyDog Library@^1.4.0
    bblanchon/ArduinoJson@^6.18.4
    https://github.com/ponoor/Ponoor_L6470_Library/archive/refs/tags/v1.0.3.zip
    ponoor/Ponoor PowerSTEP01 Library@^1.0.2
```

#### Adafruit METRO M0 Expressの場合

Arduino Zero (`[env:zeroUSB]`)としてコンパイル＆書き込みを行ってください。このボード専用の定義もありますが、USBシリアルの挙動が異なっているため、シリアルモニタからの診断ツールがうまく動きません。

## Arduino IDEでのスケッチ書き込み

PlatformIOではなくArduino IDEでコンパイルと書き込みを行う場合は、以下のステップが必要です。

1. Arduino Zero/M0をコンパイルできるようにする
2. 必要なライブラリをインストールする
3. スケッチの入手

### Arduino Zero/M0をコンパイルできるようにSAMD coreをインストールする

Arduino IDEのBoards Managerから、"Arduino SAMD Boards (32-bits ARM Cortex-M0+)" をインストールしてください。  
手順は下記ページの"Quick Start"に説明されています。

<https://docs.arduino.cc/hardware/zero>

### 必要ライブラリのインストール

以下のライブラリをArduino IDEの「ライブラリを管理...」よりインストールします。ライブラリをインストールする詳しい手順は[こちら](https://www.arduino.cc/en/guide/libraries)を参照してください。

- [OSC Library](https://github.com/CNMAT/OSC)
- [ArduinoJSON](https://arduinojson.org/)
- [Adafruit SleepyDog Arduino Library](https://github.com/adafruit/Adafruit_SleepyDog)
- STEP100のみ : [Ponoor PowerSTEP01 Library](https://github.com/ponoor/Ponoor_PowerSTEP01_Library)
- STEP200のみ : [Ponoor L6470 Library](https://github.com/ponoor/Ponoor_L6470_Library)

### Arduino IDE用スケッチファイルの入手

書き込むArduinoスケッチはこちらから入手できます。

<https://github.com/ponoor/step-series-universal-firmware/releases>

ここから最新版のリリースの "Assets" をクリックし、`step-series-universal-firmware.zip`をダウンロードして解凍してください。

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643348613641.png)

解答したフォルダの`.ino`ファイルをArduino IDEで開いてください。

### コンパイルするターゲットの設定

`boardsDef.h`の冒頭にボードのリストがあります。ここから、コンパイルしたいターゲットのコメント`//`を外してください。例えばSTEP100用にコンパイルしたい場合は以下のようになります。

```
// Products
// #define STEP400_R1
// #define STEP800_R1

// Prototypes
// #define STEP400_PROTO_R4
// #define STEP800_PROTO_R3
// #define STEP800_PROTO_R1

// X-Nucleos
#define STEP100_R1 // X-NUCLEO-IHM03A1, PowerSTEP01 x1
// #define STEP200_R1 // X-NUCLEO-IHM02A1, L6470 x2
```

またArduino M0のハードウェアにArduino Zeroのブートローダが書き込まれている場合は、

```
// #define MZERO_WITH_ZERO_BOOTLOADER
```

この行の先頭コメントアウトを消去してください。

### コンパイルと書き込み

Arduino IDEで "Tools" -> "Boards" から "Arduino Zero (Native USB port)" を選択し、コンパイルしてください。

エラーなく完了できたら、書き込みに進みます。PCとArduinoをUSBで接続し、"Tools" -> "Port" からシリアルポートを選択し、書き込みします。

このプロセスについては、STEP400/800のドキュメント内の[Arduinoスケッチのコンパイル](https://ponoor.com/docs/step-series/technical-information/compile-the-arduino-sketch/)も参考にしてください。
