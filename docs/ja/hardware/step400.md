---
title: STEP400
---

# STEP400

STEP400のハードウェアです。基板、主な部品、ピン配置、ほかのページで説明していないコネクタをまとめています。

## ハードウェアの概要 {#overview}

### 基板のサイズ {#size}

120 x 84mm、板厚1.6mm。

M3用の取付穴が、基板の各隅と中央付近の5か所にあります。

![](https://ponoor.com/cms/wp-content/uploads/2020/08/step400-dimension-800x661.png)  
この画像の上下の細長い部分は捨て基板で、製造後に切り離されています。

原寸PDF: [step400_r1_dimension.pdf](https://github.com/ponoor/STEP400/blob/master/hardware/step400_r1_dimension.pdf)

### 構成 {#system}

![diagram](https://ponoor.com/cms/wp-content/uploads/2020/08/image-1648386258465.png)

回路図: [step400_r1_schematics.pdf](https://github.com/ponoor/STEP400/blob/master/hardware/step400_r1_schematics.pdf)

主な構成要素は次のとおりです。

| 部品 | メーカ | 型番 |
| --- | --- | --- |
| MCU | Microchip | [ATSAMD21G18A](https://www.microchip.com/wwwproducts/en/ATsamd21g18) |
| Ethernet Controller | Wiznet | [W5500](https://www.wiznet.io/product-item/w5500/) |
| Stepper Driver | STMicroelectronics | [PowerSTEP01](https://www.st.com/ja/motor-drivers/powerstep01.html) |
| DC-DC Converter | ROHM | [BD9G341AEFJ](https://www.rohm.com/products/power-management/switching-regulators/integrated-fet/buck-converters-nonsynchronous/bd9g341aefj-product) |

### ピン割り振り {#pins}

| pin | function | etc |
| --- | --- | --- |
| D0 | DIPSW8 |  |
| D1 | Brake4 |  |
| D2 | DIPSW5 |  |
| D3 | DIPSW7 |  |
| D4 | SD_CS |  |
| D5 | Brake3 |  |
| D6 | PowerSTEP01_MISO |  |
| D7 | DIPSW1 |  |
| D8 | Brake2 |  |
| D9 | DIPSW6 |  |
| D10 | W5500_CS |  |
| D11 | PowerSTEP01_MOSI |  |
| D12 | PowerSTEP01_SCK |  |
| D13 | L |  |
| D20/SDA | NC | 裏面にパッドあり |
| D21/SCL | NC | 裏面にパッドあり |
| D22/MISO | W5500_MISO |  |
| D23/MOSI | W5500_MOSI |  |
| D24/SCK | W5500_SCK |  |
| D30 | DIPSW2 |  |
| D31 | DIPSW4 |  |
| D38 | NC | 裏面にパッドあり |
| A0 | PowerSTEP01_CS |  |
| A1 | Brake1 |  |
| A2 | PowerSTEP01_RESET |  |
| A3 | W5500_RESET |  |
| A4 | SD_DETECT |  |
| A5 | DIPSW3 |  |
| D22/MISO | MISO | - | SERCOM4.0 |
| D23/MOSI | MOSI | - | SERCOM4.2 |
| D24/SCK | SCK | - | SERCOM4.3 |
| D6 | MISO | - | SERCOM3.2 |
| D11 | MOSI | - | SERCOM3.0 |
| D12 | SCK | - | SERCOM3.3 |

PowerSTEP01_RESETとW5500_RESETは、それぞれPowerSTEP01とW5500のリセットピンに別々につながっています。ピンモードをOUTPUTにしてから、HIGHにしてください。

### 基板裏面のパッド {#rear-pads}

使っていないピンと電源のパッドが、基板の裏面にあります。2.54mmピッチなので、表面実装のピンヘッダやピンソケットを取り付けられます。裏面のR35とR36は、I2Cのピン（SDA、SCL）のプルアップに使えます。チップのサイズは1608（0603）です。

これらのピンは、ファームウェアでは何も処理していません。使うには、ファームウェアの追加や書き換えが必要です。

![](https://ponoor.com/cms/wp-content/uploads/2020/08/step400-pads-800x533.jpg)

6つのパッドは、回路図のコネクタJ8です。Ethernetコネクタを下側にして、上からの信号は次のとおりです。

| 上からの位置 | 信号 |
| --- | --- |
| 1 | GND |
| 2 | 3.3V |
| 3 | SDA（D20） |
| 4 | SCL（D21） |
| 5 | D38 |
| 6 | 5V |

## ブレーキ出力（J7） {#brake-output}

電磁ブレーキの出力は、6ピン（2 x 3）のヘッダJ7です。ピン番号は基板に印刷されています。印刷が読める向きにしたとき、上の段は左から5、3、1、下の段は左から6、4、2です。

| ピン | 信号 |
| --- | --- |
| 1 | EM_1（モータ1のブレーキ） |
| 2 | EM_2（モータ2） |
| 3 | EM_3（モータ3） |
| 4 | EM_4（モータ4） |
| 5 | 3.3V |
| 6 | GND |

出力は、MCUのピン（モータ1から4で、A1、D8、D5、D1）から出る3.3Vのロジック信号です。**HIGHでブレーキを解放し、LOWで保持します。** ファームウェアがピンを初期化するまでは、ピンはどこにもつながっていない、浮いた状態です。配線と、電源投入時の対策は、[電磁ブレーキの接続](../connections/electromagnetic-brake-wiring.md)をご覧ください。

## SPIの割り振り {#spi}

STEP400では、ファームウェアの処理を簡単にするために、PowerSTEP01とW5500で別々のSPIポートを使っています。ATSAMD21でのSPIの割り振り方は、こちらがとても参考になります: <https://learn.adafruit.com/using-atsamd21-sercom-to-add-more-spi-i2c-serial-ports>

### W5500 {#spi-w5500}

| Pin | Function | SERCOM | SERCOM Alt |
| --- | --- | --- | --- |
| D22/MISO | MISO | - | SERCOM4.0 |
| D23/MOSI | MOSI | - | SERCOM4.2 |
| D24/SCK | SCK | - | SERCOM4.3 |

### PowerSTEP01 {#spi-powerstep01}

| Pin | Function | SERCOM | SERCOM Alt |
| --- | --- | --- | --- |
| D6 | MISO | - | SERCOM3.2 |
| D11 | MOSI | - | SERCOM3.0 |
| D12 | SCK | - | SERCOM3.3 |

## PowerSTEP01 {#powerstep01}

### クロック {#clock}

モータID 1のPowerSTEP01のOSCINに、16MHzの水晶発振器がつながっています。そこから、IDの順に、OSCOUTとOSCINがデイジーチェーンでつながっているので、各PowerSTEP01を「外部16MHz入力、反転出力」（`EXT_16MHZ_OSCOUT_INVERT`）に設定します。ファームウェアがそう設定します。内部クロックを使うと、一定速度の運転中などに、動きが少しずつずれることがあります。

### ハードウェアが対応していない機能 {#unavailable}

#### STCK {#stck}

STCKは配線されていないので、ステップクロック動作はできません。

#### ADCIN {#adcin}

ADCINはLIMITの入力に使われているので、本来の機能である電源電圧の補正には使えません。ADC入力の値で発生するアラームのUVLO_ADCは、無効のままにしてください。ファームウェアは、そうしています。

## 既知の問題: USBを抜くとき {#usb-unplug}

EthernetをつないだままUSBケーブルを抜くと、STEP400（R1基板）は再起動することがあります。ハードウェアの問題で、ファームウェアv2.1.0でも同じです。再起動の前に、ブレーキは保持状態になります。ケーブルを抜くのは、モータを止めているときにしてください。STEP800（R1）は再起動しません。[トラブルシューティング](../maintenance/troubleshooting.md#usb-unplug)もご覧ください。
