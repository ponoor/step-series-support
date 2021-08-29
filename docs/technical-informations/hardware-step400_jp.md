## ハードウェアの概要
### 基板のサイズ
120x84, 板厚1.6mm

M3用取付穴が基板の各隅+中央付近の5か所にあります。

![](https://ponoor.com/cms/wp-content/uploads/2020/08/step400-dimension-800x661.png)
この画像の上下の細長い部分は捨て基板で、製造終了後に切り離されています。

原寸PDF : [step400_r1_dimenstion.pdf](https://ponoor.com/cms/wp-content/uploads/2020/08/step400_r1_dimenstion.pdf "step400_r1_dimenstion")

### 構成

主な構成要素は以下のとおりです。

| 部品 | メーカ | 型番 |
|--------|-----------|--------|
| MCU | Microchip | [ATSAMD21G18A](https://www.microchip.com/wwwproducts/en/ATsamd21g18) |
| Ethernet Controller | Wiznet | [W5500](https://www.wiznet.io/product-item/w5500/) |
| Stepper Driver | STMicroelectronics | [PowerSTEP01](https://www.st.com/ja/motor-drivers/powerstep01.html) |
| DC-DC Converter | ROHM | [BD9G341AEFJ](https://www.rohm.co.jp/products/power-management/switching-regulators/integrated-fet/buck-converters-nonsynchronous/bd9g341aefj-product) |

### ピン割り振り

| pin | function | etc |
|-----|----------|-----|
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
| D20/SDA | NC | はんだ面にパッド有 |
| D21/SCL | NC | はんだ面にパッド有 |
| D22/MISO | W5500_MISO |  |
| D23/MOSI | W5500_MOSI |  |
| D24/SCK | W5500_SCK |  |
| D30 | DIPSW2 |  |
| D31 | DIPSW4 |  |
| D38 | NC | はんだ面にパッド有 |
| A0 | PowerSTEP01_CS |  |
| A1 | Brake1 |  |
| A2 | PowerSTEP01_RESET |  |
| A3 | W5500_RESET |  |
| A4 | SD_DETECT |  |
| A5 | DIPSW3 |  |

PowerSTEP01_RESETとW5500_RESETはそれぞれPowerSTEP01とW5500のリセットピンに接続されていますので、必ずpinModeをOUTPUTに設定したうえで、HIGH状態にしてください。

### 基板裏面のパッド
使用していないピンと電源のパッドが裏面にあります。2.54mmピッチですので、表面実装のピンヘッダやピンソケットを取り付けることができます。裏面のR35, R36はi2cピン(SDA, SCL)のプルアップに使用できます。サイズは1608(0603)サイズです。

これらのピンはファームウェアでは何も処理を行っていませんので、使用方法に応じたファームウェアの追加・書き換えが必要です。

![](https://ponoor.com/cms/wp-content/uploads/2020/08/step400-pads-800x533.jpg)

## SPIの割り振り
STEP400ではファームウェアの処理を簡単にするためにPowerSTEP01とW5500で別々のSPIポートを使用しています。
ATSAMD21におけるSPIの割り振り方法はこちらが大変参考になります。

[https://learn.adafruit.com/using-atsamd21-sercom-to-add-more-spi-i2c-serial-ports](https://learn.adafruit.com/using-atsamd21-sercom-to-add-more-spi-i2c-serial-ports)

### W5500

| Pin | Function | SERCOM | SERCOM Alt |
|-----|----------|--------|------------|
| D22/MISO | MISO | - | SERCOM4.0 |
| D23/MOSI | MOSI | - | SERCOM4.2 |
| D24/SCK | SCK | - | SERCOM4.3 |

### PowerSTEP01

| Pin | Function | SERCOM | SERCOM Alt |
|-----|----------|--------|------------|
| D6 | MISO | - | SERCOM3.2 |
| D11 | MOSI | - | SERCOM3.0 |
| D12 | SCK | - | SERCOM3.3 |

## PowerSTEP01

### クロック

motor ID 1のPowerSTEP01のOSCINに16MHzの水晶発振器が接続されています。そこからIDの順に、OSCOUTとOSCINがデイジーチェーンされていますので、各PowerSTEP01は「外部16MHz入力、反転出力(`EXT_16MHZ_OSCOUT_INVERT`)」に設定してください。 内部クロックを使うと、一定速運転時などに動きが徐々にずれてくる現象が発生します。

## ハードウェア的に使えないPowerSTEP01の機能

### STCK

配線されていないので、Step Clock動作はできません。

### ADCIN

リミットセンサ入力して使われていますので、本来の機能である電源電圧補正用には使用できません。ADC入力の値をもとにアラームを発生させるUVLO_ADCは必ず無効にしてください。