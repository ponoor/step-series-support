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

Arduino ZeroとM0は[公式のサイト](https://store-usa.arduino.cc/collections/boards/products/arduino-zero)では在庫切れになっていますが、秋月電子通商で[M0](https://akizukidenshi.com/catalog/g/gM-09079/)が入手できます。また、AliExpressなどで[互換品](https://www.aliexpress.com/item/4000544537659.html)が入手できます。

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

ファームウェアは、Wiznet W5500を使った[Arduino Ethernet Shield 2](https://docs.arduino.cc/hardware/ethernet-shield-rev2)で動作を確かめています。こちらも公式ストアでは在庫切れですが、大手のディストリビューター（[Mouser](https://www.mouser.jp/ProductDetail/Arduino/A000024?qs=sGAEpiMZZMvfWfew95%2FxXPtlEf46RordNAHqnNtyb4k%3D)、[Digikey](https://www.digikey.jp/ja/products/detail/arduino/A000024/3476356)、[RS](https://jp.rs-online.com/web/p/shields-for-arduino/8732285?sra=pmpn)など）で取り扱いがあります。

AliExpressなどには、W5100を使った古いタイプの互換品もたくさんあります。これは、実機でテストしたところ、STEP100（X-NUCLEO-IHM03A1）では動作しませんでした。STEP200（X-NUCLEO-IHM02A1）では動きます。

秋月電子通商で売っている[Ethernet Shield for Arduino v2.2](https://akizukidenshi.com/catalog/g/gM-13165/)は、`boardsDef.h`のピン配置の定義を書き換えれば動作すると思われますが、実機での動作は確かめていません。

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643702118944.png)

このタイプは、上にさらにシールドを載せることができないので使えません。ArduinoとEthernetシールドは6ピンのSPIコネクタを介して通信しますが、X-NUCLEOボードにはこのコネクタがありません。そのため、Arduinoの上には必ずEthernetシールドを重ね、その上にX-NUCLEOボードを差し込みます。

## X-NUCLEOボード {#x-nucleo}

![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342852324.png)![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342863866.png)

STMicroelectronics社から発売されている評価ボードです。こちらも大手ディストリビューターなどから入手できます。

| 製品 | X-NUCLEO | ドライバIC | Mouser | Digikey | RS | Chip1stop |
| --- | --- | --- | --- | --- | --- | --- |
| STEP100 | [X-NUCLEO-IHM03A1](https://www.st.com/en/ecosystems/x-nucleo-ihm03a1.html) | PowerSTEP01 | [link](https://www.mouser.jp/ProductDetail/STMicroelectronics/X-NUCLEO-IHM03A1?qs=ILgNtqsyH21VjhjjaAqaGQ%3D%3D) | [link](https://www.digikey.jp/ja/products/detail/stmicroelectronics/X-NUCLEO-IHM03A1/5325495?s=N4IgTCBcDaIJYAsC2AGAzAQwIwgLoF8g) | [link](https://jp.rs-online.com/web/p/power-motor-robotics-development-tools/9064656) | [link](https://www.chip1stop.com/view/dispDetail/DispDetail?lang=en&cont=USA&partId=STMI-0106873&mpn=X-NUCLEO-IHM03A1&keyword=X-NUCLEO-IHM03A1) |
| STEP200 | [X-NUCLEO-IHM02A1](https://www.st.com/en/ecosystems/x-nucleo-ihm02a1.html) | L6470 | [link](https://www.mouser.jp/ProductDetail/STMicroelectronics/X-NUCLEO-IHM02A1?qs=468p3M0KQ1q0beHvLX%2FUnA%3D%3D) | [link](https://www.digikey.jp/ja/products/detail/stmicroelectronics/X-NUCLEO-IHM02A1/5768392?s=N4IgTCBcDaIJYAsC2AGMBDAjCAugXyA) | [link](https://jp.rs-online.com/web/p/power-motor-robotics-development-tools/1646982?sra=pmpn) | [link](https://www.chip1stop.com/view/dispDetail/DispDetail?lang=en&cont=USA&partId=STMI-0102961&mpn=X-NUCLEO-IHM02A1&keyword=ihm02a1) |

## 電源 {#power-supply}

X-NUCLEOボードのデータシートによると、モータ電源の電圧は次のとおりです。

- IHM03A1（PowerSTEP01）: 10.5V〜50V
- IHM02A1（L6470）: 8V〜45V

どちらも、24Vで4〜5A程度の電源を用意して実験を始めるとよいでしょう。電源とモータの選び方は、[電源とモータの定格](../connections/power-supply-and-motor.md#ratings)をご覧ください。

X-NUCLEOボードにはねじ式端子があるので、ACアダプタから給電するときは、DCジャックのケーブルがあると便利です。

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643347656810.png)

モータ電源を供給しても、Arduinoには給電されませんので、Arduino用の電源も必要です。USB経由でPCやUSB充電器から給電してください。
