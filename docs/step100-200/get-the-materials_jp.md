---
title: 材料を手に入れる
wp_id: 2273
slug: get-the-materials
lang: ja
link: "https://ponoor.com/docs/step100-200/get-the-materials/"
date: "2022-02-02T21:41:09"
modified: "2022-03-29T10:21:59"
parent: 2164
menu_order: 5
---

# 材料を手に入れる

## Arduino Zero または M0

![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342497869.png)![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342518306.png)

現在のところSTEP100/200のファームウェアは

- Arduino Zero
- Arduino M0
- [Adafruit METRO M0 Express](https://www.adafruit.com/product/3505)

に対応しています。  
Arduino Zero/M0は[公式のサイト](https://store-usa.arduino.cc/collections/boards/products/arduino-zero)では在庫切れになっていますが、秋月電子通商で[M0](https://akizukidenshi.com/catalog/g/gM-09079/)が入手可能です。またAli Expressなどで[互換品](https://www.aliexpress.com/item/4000544537659.html)が入手できます。

### Arduino Zero or M0?

この2機種はArduinoが2つに分かれていた時代の影響で別の機種に分かれてしまっていますが、ほとんど同じもので、どちらでも使用可能です。とはいえ違いもありますので、スケッチをコンパイル・書き込みする際には対応する機種名を選んで行う必要があります。

ハードウェア面では、D2ピンとD4ピンが両機種の間で入れ替わっています。紛らわしいのですが、互換品の中には Arduino M0 相当のハードウェアに Arduino Zero のブートローダが書き込まれていることがあります。Arduino Zeroとして認識される基板でも、実際にD2を点滅させるスケッチを書き込んでみて、D2とD4どちらが点滅するかを確認したほうが安全です。もしD2とD4が入れ替わっているArduino Zeroの場合は、[スケッチの書き込み](https://ponoor.com/docs/step100-200/upload-the-sketch/)に進んだ際に`boardsDef.h`の32行目付近

```
// #define MZERO_WITH_ZERO_BOOTLOADER
```

この行についているコメントアウト`//`を消去してコンパイルしてください。

### その他のArduinoについて

STEP100/200で使用するX-NucleoシリーズのSPIピンはSPIコネクタではなく、D11,D12,D13を使用しています。Arduino Zero/M0ではこれらのピンにSPI機能を割り当てて使用しています。これらの端子はArduino UNOでもSPI端子として使われていますので制御は可能ですが、UNOはRAMやFlashサイズが小さいのでSTEPシリーズのファームウェアは動かせません。

LeonardoやMEGAでは、D11-D13にSPIの機能が割り振られていないので使用できません。

## Ethernet Shield

![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342683554.png)![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643702336632.png)

ファームウェアはWiznet W5500を使用した[Arduino Ethernet Shield2](https://docs.arduino.cc/hardware/ethernet-shield-rev2)で動作確認をしています。こちらも公式ストアでは在庫切れですが、大手のディストリビューター（[Mouser](https://www.mouser.jp/ProductDetail/Arduino/A000024?qs=sGAEpiMZZMvfWfew95%2FxXPtlEf46RordNAHqnNtyb4k%3D), [Digikey](https://www.digikey.jp/ja/products/detail/arduino/A000024/3476356), [RS](https://jp.rs-online.com/web/p/shields-for-arduino/8732285?sra=pmpn)など）で取り扱いがあります。  
またAli Expressなどで互換品がたくさん出ているW5100を使った古いタイプの互換品もありますが、これは実機テストをしたところ STEP100(X-NUCLEO-IHM03A1) では動作しませんでした。STEP200(X-NUCLEO-IHM02A1)では動きます。  
秋月電子通商で売っている[Ethernet Shield for Arduino v2.2](https://akizukidenshi.com/catalog/g/gM-13165/)は`boardsDef.h`のピンアサインの定義を書き換えれば動作すると思われますが、実機動作は未確認です。

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643702118944.png)

こういうタイプは上にさらにシールドを載せることができないので使えません。ArduinoとEthernetシールドは6ピンのSPIを介して通信しますが、X-Nucleoシリーズにはこのコネクタがないので、重ねる順序はArduinoの上は必ずEthernetシールドにして、その上にX-Nucleoシリーズを差し込む必要があります。

## X-NUCLEOシリーズ

![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342852324.png)![](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643342863866.png)

STMicroelectronics社から発売されている評価ボードです。こちらも大手ディストリビューターなどから入手できます。

| Model | X-Nucleo | Driver | Mouser | Digikey | RS | Chip1stop |
| --- | --- | --- | --- | --- | --- | --- |
| STEP100 | [X-NUCLEO-IHM03A1](https://www.st.com/en/ecosystems/x-nucleo-ihm03a1.html) | PowerSTEP01 | [link](https://www.mouser.jp/ProductDetail/STMicroelectronics/X-NUCLEO-IHM03A1?qs=ILgNtqsyH21VjhjjaAqaGQ%3D%3D) | [link](https://www.digikey.jp/ja/products/detail/stmicroelectronics/X-NUCLEO-IHM03A1/5325495?s=N4IgTCBcDaIJYAsC2AGAzAQwIwgLoF8g) | [link](https://jp.rs-online.com/web/p/power-motor-robotics-development-tools/9064656) | [link](https://www.chip1stop.com/view/dispDetail/DispDetail?lang=en&cont=USA&partId=STMI-0106873&mpn=X-NUCLEO-IHM03A1&keyword=X-NUCLEO-IHM03A1) |
| STEP200 | [X-NUCLEO-IHM02A1](https://www.st.com/en/ecosystems/x-nucleo-ihm02a1.html) | L6470 | [link](https://www.mouser.jp/ProductDetail/STMicroelectronics/X-NUCLEO-IHM02A1?qs=468p3M0KQ1q0beHvLX%2FUnA%3D%3D) | [link](https://www.digikey.jp/ja/products/detail/stmicroelectronics/X-NUCLEO-IHM02A1/5768392?s=N4IgTCBcDaIJYAsC2AGMBDAjCAugXyA) | [link](https://jp.rs-online.com/web/p/power-motor-robotics-development-tools/1646982?sra=pmpn) | [link](https://www.chip1stop.com/view/dispDetail/DispDetail?lang=en&cont=USA&partId=STMI-0102961&mpn=X-NUCLEO-IHM02A1&keyword=ihm02a1) |

## 電源

モータ電源の電圧は、X-Nucleoのデータシートによると

- IHM03A1(PowerSTEP01): 10.5V-50V
- IHM02A1(L6470): 8V-45V

となっています。とりあえずどちらも24V 4-5Aくらいの電源を準備して実験を始めるのが良いのではないでしょうか。[電源とモータの選定](https://ponoor.com/docs/step-series/settings/power-supply-and-motor/)も参考にしてください。

X-Nucleo側はねじ式ターミナルになっているので、ACアダプタとつなぐ場合はDCジャックのケーブルがあると便利です。  
![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643347656810.png)

またモータ電源を供給してもArduinoには給電されないので、Arduino用の電源も必要です。USB経由でPCやUSB充電器などから給電すればokです。
