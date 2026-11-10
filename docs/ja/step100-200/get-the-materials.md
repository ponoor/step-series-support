---
title: 材料
---

# 材料

STEP100とSTEP200は、Arduino Zero（または互換ボード）、Ethernetシールド、X-NUCLEOボードで作ります。このページでは、用意するものを説明します。

## Arduino ZeroまたはM0 {#arduino}

![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342497869.png)![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342518306.png)

ファームウェアが対応しているのは、次のボードです。

- Arduino Zero
- Arduino M0
- [Adafruit METRO M0 Express](https://www.adafruit.com/product/3505)

互換ボードも使えます。Arduino Zeroは、Microchip社のMCU`ATSAMD21G18`を使っています（ファームウェアが使うPlatformIOのボード定義`zeroUSB`は、`ATSAMD21G18A`のものです）。互換ボードを探すときは、このMCUを使った、Arduino Zero型のボードを探してください。互換ボードには、Arduino Zeroのブートローダのものと、Arduino M0のブートローダのものがあります。見分けかたは、[Arduino ZeroかM0か](#zero-or-m0)をご覧ください。

### Arduino ZeroかM0か {#zero-or-m0}

この2機種は、Arduinoが2つに分かれていた時代の影響で別の機種に分かれていますが、ほとんど同じもので、どちらでも使えます。とはいえ違いもありますので、ファームウェアをビルドして書き込むときには、その違いに合わせる必要があります（[スケッチの書き込み](upload-the-sketch.md#m0)）。

ハードウェアでは、D2ピンとD4ピンが両機種の間で入れ替わっています。紛らわしいのですが、互換品の中には、Arduino M0相当のハードウェアにArduino Zeroのブートローダが書き込まれているものがあります。Arduino Zeroとして認識されるボードでも、D2を点滅させるスケッチを書き込んで、D2とD4のどちらが点滅するかを確認したほうが安全です。

Arduino Zeroとして認識されるボードでD2とD4が入れ替わっているときは、ファームウェアのビルドで`MZERO_WITH_ZERO_BOOTLOADER`を定義します。`boardsDef.h`にある次の行です。

```
// #define MZERO_WITH_ZERO_BOOTLOADER
```

### そのほかのArduino {#other-arduinos}

STEP100/200で使うX-NUCLEOボードのSPIピンは、SPIコネクタではなく、D11、D12、D13を使っています。Arduino ZeroとM0では、これらのピンにSPIの機能が割り当てられています。Arduino UNOでもこれらのピンはSPIのピンとして使われていますので、X-NUCLEOボードを制御することはできますが、UNOはRAMとフラッシュのサイズが小さいので、STEPシリーズのファームウェアは動かせません。

LeonardoやMEGAでは、D11-D13にSPIの機能が割り当てられていないので、使えません。

## Ethernetシールド {#ethernet-shield}

![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342683554.png)![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643702336632.png)

ファームウェアは、Wiznet W5500を使った[Arduino Ethernet Shield 2](https://docs.arduino.cc/hardware/ethernet-shield-rev2)で動作を確かめています。正式な名前は「Arduino Ethernet Shield 2」で、メーカーの品番は`A000024`です。大手の電子部品のディストリビューターで取り扱いがあります。

通販サイトなどには、W5100を使った古いタイプの互換品もたくさんあります。これは、実機でテストしたところ、STEP100（X-NUCLEO-IHM03A1）では動作しませんでした。STEP200（X-NUCLEO-IHM02A1）では動きます。

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643702118944.png)

このタイプは、上にさらにシールドを載せることができないので使えません。ArduinoとEthernetシールドは6ピンのSPIコネクタを介して通信しますが、X-NUCLEOボードにはこのコネクタがありません。そのため、Arduinoの上には必ずEthernetシールドを重ね、その上にX-NUCLEOボードを差し込みます。

## X-NUCLEOボード {#x-nucleo}

![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342852324.png)![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342863866.png)

STMicroelectronics社から発売されている評価ボードです。

| 製品 | X-NUCLEO | ドライバIC |
| --- | --- | --- |
| STEP100 | [X-NUCLEO-IHM03A1](https://www.st.com/en/ecosystems/x-nucleo-ihm03a1.html) | PowerSTEP01 |
| STEP200 | [X-NUCLEO-IHM02A1](https://www.st.com/en/ecosystems/x-nucleo-ihm02a1.html) | L6470 |

STの製品ページのほか、大手の電子部品のディストリビューターで取り扱いがあります。

## 電源 {#power-supply}

X-NUCLEOボードのデータシートによると、モータ電源の電圧は次のとおりです。

- IHM03A1（PowerSTEP01）: 10.5V〜50V
- IHM02A1（L6470）: 8V〜45V

どちらも、24Vで4〜5A程度の電源を用意して実験を始めるとよいでしょう。電源とモータの選び方は、[電源とモータの定格](../connections/power-supply-and-motor.md#ratings)をご覧ください。

X-NUCLEOボードにはねじ式端子があるので、ACアダプタから給電するときは、DCジャックのケーブルがあると便利です。

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643347656810.png)

モータ電源を供給しても、Arduinoには給電されませんので、Arduino用の電源も必要です。USB経由でPCやUSB充電器から給電してください。
