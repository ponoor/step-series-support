---
title: ファームウェアのコンパイル
---

# ファームウェアのコンパイル

ファームウェアを更新したりカスタマイズしたりするには、ご自身の環境でファームウェアをビルドして、ボードに書き込みます。MCUは[Arduino Zero](https://www.arduino.cc/en/Main/ArduinoBoardZero&)互換なので、ファームウェアはArduino互換のプロジェクトとしてビルドします。おすすめの方法はPlatformIOです。Arduino IDEも使えます。

ソースコードは[GitHubのリポジトリ](https://github.com/ponoor/step-series-universal-firmware)に、各バージョンは[Releases](https://github.com/ponoor/step-series-universal-firmware/releases)のページにあります。リリースには、すぐに使えるバイナリファイル（`.bin`）はありません。ファームウェアをビルドして、USBのブートローダで書き込みます。このページの手順は、リポジトリのREADMEに従っています。

## PlatformIOでコンパイルする（おすすめ） {#platformio}

ファームウェアは、[PlatformIO](https://platformio.org/)（Arduinoフレームワーク）で開発しています。リポジトリをクローンするか、ZIPでダウンロードして解凍し、そのフォルダをPlatformIOで開きます。初めてコンパイルするときに、必要なものが`platformio.ini`から自動でインストールされます。

![file](https://ponoor.com/cms/wp-content/uploads/2020/08/image-1648187813165.png)

### ボードの選び方 {#select-board}

PlatformIOでは、`platformio.ini`の**環境**でボードを選びます。`step400`、`step800`、`step100`、`step200`のどれかです（v2.1.0までは、`src/boardsDef.h`の1行のコメントを外してボードを選んでいました。PlatformIOでは、この方法は使いません）。

- `platformio.ini`の`default_envs`をお使いのボードにして、VS CodeのPlatformIOのボタン、または`pio run`と`pio run -t upload`でビルドと書き込みをします。

  ```ini
  [platformio]
  default_envs = step800
  ```

- または、そのたびに環境を選びます。`pio run -e step800 -t upload`、またはVS Codeの画面下部のバーの環境の選択で`env:step800`を選びます。
- `boardsDef.h`のボードの行は、すべてコメントアウトのままにしてください。両方で指定したボードは、コンパイルできません。
- 以前のバージョンの環境`zeroUSB`は残してあり、STEP400用にビルドします。
- 複数のボードをつないでいるときは、環境にポートを足してください。たとえば、`[env:step800]`の下に`upload_port = /dev/cu.usbmodem1101`と書きます。

ドライバのライブラリは、`platformio.ini`のとおり、GitHubのタグのZIPから取得します。PlatformIOのレジストリからはインストールしないでください。

## Arduino IDEでコンパイルする {#arduino-ide}

Arduino IDEは、PlatformIOより手作業が多くなります。

1. IDEのボードマネージャーで、**Arduino SAMD Boards**のコアをインストールします。<https://docs.arduino.cc/hardware/zero>の「Quick Start」をご覧ください。
2. ライブラリ（下記）を、ライブラリマネージャーでインストールします。インストールの方法は<https://www.arduino.cc/en/guide/libraries>にあります。
3. 最新の[リリース](https://github.com/ponoor/step-series-universal-firmware/releases)の「Assets」から`step-series-universal-firmware.zip`をダウンロードして解凍します。フォルダの中にスケッチがあるので、`.ino`ファイルをArduino IDEで開きます。

   ![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643348613641.png)

4. `boardsDef.h`でボードを選びます。ファイルの先頭にあるボードのうち、1つのコメント`//`を外します。STEP400の場合は次のようになります。ボードを何も選ばないと、STEP400（`STEP400_R1`）になります。

   ```c
   // Products
   #define STEP400_R1
   // #define STEP800_R1

   // X-Nucleos
   // #define STEP100_R1 // X-NUCLEO-IHM03A1, PowerSTEP01 x1
   // #define STEP200_R1 // X-NUCLEO-IHM02A1, L6470 x2
   ```

5. 「Tools」->「Board」から「Arduino Zero（Native USB Port）」を選んで、コンパイルします。エラーがなければ、ボードとパソコンをUSBでつなぎ、「Tools」->「Port」からシリアルポートを選んで、書き込みます。

### ライブラリ {#libraries}

次のライブラリを、ライブラリマネージャーでインストールします。

| ライブラリ | バージョン | 使う製品 |
| --- | --- | --- |
| [Ponoor PowerSTEP01 Library](https://github.com/ponoor/Ponoor_PowerSTEP01_Library) | 1.2.0以降 | STEP400、STEP100 |
| [Ponoor L6470 Library](https://github.com/ponoor/Ponoor_L6470_Library) | 1.2.0以降 | STEP800、STEP200 |
| [Ethernet](https://github.com/arduino-libraries/Ethernet) | 2.0.2以降 | |
| [SdFat](https://github.com/greiman/SdFat)（Bill Greiman） | 2.2.3以降 | |
| [ArduinoJson](https://arduinojson.org/) | 7.4.1以降（7.x） | |

OSCのパーサとウォッチドッグはファームウェアに入っているので、CNMATのOSCライブラリとAdafruit SleepyDogライブラリは、もう要りません。

ドライバのライブラリのバージョンは、ファームウェアのバージョンに合わせる必要があります。

| ファームウェア | Ponoor L6470 / PowerSTEP01 Library |
| --- | --- |
| 2.2.0 | 1.2.0 |
| 2.1.0以前 | 1.1.x |

## STEP100とSTEP200 {#step100-200}

ファームウェアは、STEP100とSTEP200向けにもビルドできます（環境`step100`と`step200`）。ただし、v2.1.0以降、実機では確かめていません。[STEP100 / STEP200](../step100-200/index.md)をご覧ください。

## ファームウェアを書き込むときの注意 {#uploading}

- **書き込む前に、電磁ブレーキを外してください。** 書き込みの間は、ファームウェアが動かず、ブレーキ出力は制御されていません。STEP800では、出力が解放側になることがあります。ブレーキが保持している負荷が落下するおそれがあります。[電磁ブレーキの接続](../connections/electromagnetic-brake-wiring.md#power-on)をご覧ください。
- USBだけでは、ドライバICに電源が入りません。ファームウェアを書き込んだり、基本的なコマンドを使ったりはできますが、モータの電源を入れないと、モータを動かせず、ドライバとのやり取りもできません。
- 書き込みに失敗することがあります。その場合は、RESETスイッチをダブルクリックして、ブートローダのモードにして、もう一度試してください。このモードでは、ファームウェアは起動せず、LEDの`L`がゆっくりフェードします。シリアルポートが通常の起動のときとは別になるので、ポートを選び直してください。
