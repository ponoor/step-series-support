---
title: STEP800
---

# STEP800

STEP800のハードウェアです。基板、主な部品、ピン配置、ほかのページで説明していないコネクタをまとめています。

## ハードウェアの概要 {#overview}

### 基板のサイズ {#size}

120 x 80mm、板厚1.6mm。

M3用の取付穴が、基板の各隅と中央付近の5か所にあります。

![](https://ponoor.com/cms/wp-content/uploads/2021/09/step800_r1_0_0_dimension-1.png)  
この画像の上下の細長い部分は捨て基板で、製造後に切り離されています。

原寸PDF: [step800_r1_0_0_dimension.pdf](https://github.com/ponoor/STEP800/blob/main/hardware/step800_r1_0_0_dimension.pdf)

### 構成 {#system}

![file](https://ponoor.com/cms/wp-content/uploads/2021/09/image-1648468983329.png)

回路図: [step800_r1_0_0_schematics.pdf](https://github.com/ponoor/STEP800/blob/main/hardware/step800_r1_0_0_schematics.pdf)

主な構成要素は次のとおりです。

| 部品 | メーカ | 型番 |
| --- | --- | --- |
| MCU | Microchip | [ATSAMD21G18A](https://www.microchip.com/wwwproducts/en/ATsamd21g18) |
| Ethernet Controller | Wiznet | [W5500](https://www.wiznet.io/product-item/w5500/) |
| Stepper Driver | STMicroelectronics | [L6470](https://www.st.com/ja/motor-drivers/L6470.html) |
| DC-DC Converter | CUI | [P78E05-1000](https://www.jp.cui.com/product/dc-dc-converters/non-isolated/p78e-1000-series) |

### ピン割り振り {#pins}

| pin | function | etc |
| --- | --- | --- |
| D0 | Shift Register SCK |  |
| D1 | NC | 裏面にパッドあり |
| D2 | Shift Register MOSI |  |
| D3 | Shift Register MISO |  |
| D4 | SD_CS |  |
| D5 | Shift Register ENABLE |  |
| D6 | L6470 MISO |  |
| D7 | NC | 裏面にパッドあり |
| D8 | NC | 裏面にパッドあり |
| D9 | NC | 裏面にパッドあり |
| D10 | W5500_CS |  |
| D11 | L6470 MOSI |  |
| D12 | L6470 SCK |  |
| D13 | L |  |
| D20/SDA | NC | 裏面にパッドあり |
| D21/SCL | NC | 裏面にパッドあり |
| D22/MISO | W5500_MISO |  |
| D23/MOSI | W5500_MOSI |  |
| D24/SCK | W5500_SCK |  |
| D30 | NC |  |
| D31 | NC |  |
| D38 | NC | 裏面にパッドあり |
| A0 | L6470_CS |  |
| A1 | NC | 裏面にパッドあり |
| A2 | L6470_RESET |  |
| A3 | W5500_RESET |  |
| A4 | SD_DETECT |  |
| A5 | Shift Register CS |  |
| D22/MISO | MISO | - | SERCOM4.0 |
| D23/MOSI | MOSI | - | SERCOM4.2 |
| D24/SCK | SCK | - | SERCOM4.3 |
| D6 | MISO | - | SERCOM3.2 |
| D11 | MOSI | - | SERCOM3.0 |
| D12 | SCK | - | SERCOM3.3 |
| D3 | MISO | - | SERCOM2.1 |
| D2 | MOSI | SERCOM2.2 | - |
| D0 | SCK | - | SERCOM2.3 |

L6470_RESETとW5500_RESETは、それぞれL6470とW5500のリセットピンに別々につながっています。ピンモードをOUTPUTにしてから、HIGHにしてください。

### 基板裏面のパッド {#rear-pads}

使っていないピンと電源のパッドが、基板の裏面にあります。2.54mmピッチなので、表面実装のピンヘッダやピンソケットを取り付けられます。裏面のR6とR7は、I2Cのピン（SDA、SCL）のプルアップに使えます。チップのサイズは1608（0603）です。

これらのピンは、ファームウェアでは何も処理していません。使うには、ファームウェアの追加や書き換えが必要です。

![](https://ponoor.com/cms/wp-content/uploads/2021/09/step800_reserved_pads.jpg)

## ブレーキ出力（J2） {#brake-output}

電磁ブレーキの出力は、10ピン（2 x 5）のボックスヘッダJ2です。ピン番号は標準的なボックスヘッダと同じです。上から見て、キー（切り欠き）を下にしたとき、下の段が左から1、3、5、7、9、上の段が左から2、4、6、8、10です。出力1から8は、シフトレジスタの出力QAからQHです。

| ピン | 信号 |
| --- | --- |
| 1から8 | モータ1からモータ8のブレーキ |
| 9 | 3.3V |
| 10 | GND |

出力は、シフトレジスタ（74HC595）のデジタル出力から出る3.3Vのロジック信号です。**HIGHでブレーキを解放し、LOWで保持します。** 電源投入時、シフトレジスタの状態は不定なので、ファームウェアが起動するまで（時間は、[負荷を支えられない時間](../guides/electromagnetic-brake.md#unsupported)をご覧ください）、すべての出力が解放側になることがあります。配線と、電源投入時の対策は、[電磁ブレーキの接続](../connections/electromagnetic-brake-wiring.md)をご覧ください。

## SPIの割り振り {#spi}

STEP800では、ファームウェアの処理を簡単にするために、L6470、W5500、シフトレジスタで別々のSPIポートを使っています。ATSAMD21でのSPIの割り振り方は、こちらがとても参考になります: <https://learn.adafruit.com/using-atsamd21-sercom-to-add-more-spi-i2c-serial-ports>

### W5500 {#spi-w5500}

| Pin | Function | SERCOM | SERCOM Alt |
| --- | --- | --- | --- |
| D22/MISO | MISO | - | SERCOM4.0 |
| D23/MOSI | MOSI | - | SERCOM4.2 |
| D24/SCK | SCK | - | SERCOM4.3 |

### L6470 {#spi-l6470}

| Pin | Function | SERCOM | SERCOM Alt |
| --- | --- | --- | --- |
| D6 | MISO | - | SERCOM3.2 |
| D11 | MOSI | - | SERCOM3.0 |
| D12 | SCK | - | SERCOM3.3 |

### シフトレジスタ（DIPスイッチ、ブレーキ出力） {#spi-shift-register}

| Pin | Function | SERCOM | SERCOM Alt |
| --- | --- | --- | --- |
| D3 | MISO | - | SERCOM2.1 |
| D2 | MOSI | SERCOM2.2 | - |
| D0 | SCK | - | SERCOM2.3 |

## L6470 {#l6470}

### クロック {#clock}

モータID 1のL6470のOSCINに、16MHzの水晶発振器がつながっています。そこから、IDの順に、OSCOUTとOSCINがデイジーチェーンでつながっているので、各L6470を「外部16MHz入力、反転出力」（`EXT_16MHZ_OSCOUT_INVERT`）に設定します。ファームウェアがそう設定します。内部クロックを使うと、一定速度の運転中などに、動きが少しずつずれることがあります。

### ハードウェアが対応していない機能 {#unavailable}

#### STCK {#stck}

STCKは配線されていないので、ステップクロック動作はできません。

#### ADCIN {#adcin}

ADCINはGNDに直接つながっていて、使えません。
