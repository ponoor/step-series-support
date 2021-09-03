## ハードウェアの概要
### 基板のサイズ
120x80, 板厚1.6mm

M3用取付穴が基板の各隅+中央付近の5か所にあります。

![](https://ponoor.com/cms/wp-content/uploads/2021/09/step800_r1_0_0_dimension-1.png)
この画像の上下の細長い部分は捨て基板で、製造終了後に切り離されています。

原寸PDF : [step800_r1_0_0_dimension.pdf](https://ponoor.com/cms/wp-content/uploads/2021/09/step800_r1_0_0_dimension.pdf)

### 構成

主な構成要素は以下のとおりです。

| 部品 | メーカ | 型番 |
|--------|-----------|--------|
| MCU | Microchip | [ATSAMD21G18A](https://www.microchip.com/wwwproducts/en/ATsamd21g18) |
| Ethernet Controller | Wiznet | [W5500](https://www.wiznet.io/product-item/w5500/) |
| Stepper Driver | STMicroelectronics | [L6470](https://www.st.com/ja/motor-drivers/L6470.html) |
| DC-DC Converter | CUI | [P78E05-1000](https://www.jp.cui.com/product/dc-dc-converters/non-isolated/p78e-1000-series) |

### ピン割り振り

| pin | function | etc |
|-----|----------|-----|
| D0 | Shift Register SCK |  |
| D1 | NC | はんだ面にパッド有 |
| D2 | Shift Register MOSI |  |
| D3 | Shift Register MISO |  |
| D4 | SD_CS |  |
| D5 | Shift Register ENABLE |  |
| D6 | L6470 MISO |  |
| D7 | NC | はんだ面にパッド有 |
| D8 | NC | はんだ面にパッド有 |
| D9 | NC | はんだ面にパッド有 |
| D10 | W5500_CS |  |
| D11 | L6470 MOSI |  |
| D12 | L6470 SCK |  |
| D13 | L |  |
| D20/SDA | NC | はんだ面にパッド有 |
| D21/SCL | NC | はんだ面にパッド有 |
| D22/MISO | W5500_MISO |  |
| D23/MOSI | W5500_MOSI |  |
| D24/SCK | W5500_SCK |  |
| D30 | NC |  |
| D31 | NC |  |
| D38 | NC | はんだ面にパッド有 |
| A0 | L6470_CS |  |
| A1 | NC | はんだ面にパッド有 |
| A2 | L6470_RESET |  |
| A3 | W5500_RESET |  |
| A4 | SD_DETECT |  |
| A5 | Shift Register CS |  |

L6470_RESETとW5500_RESETはそれぞれL6470とW5500のリセットピンに接続されていますので、必ずpinModeをOUTPUTに設定したうえで、HIGH状態にしてください。

### 基板裏面のパッド
使用していないピンと電源のパッドが裏面にあります。2.54mmピッチですので、表面実装のピンヘッダやピンソケットを取り付けることができます。裏面のR6, R7はi2cピン(SDA, SCL)のプルアップに使用できます。サイズは1608(0603)サイズです。

これらのピンはファームウェアでは何も処理を行っていませんので、使用方法に応じたファームウェアの追加・書き換えが必要です。

![](https://ponoor.com/cms/wp-content/uploads/2021/09/step800_reserved_pads.jpg)

## SPIの割り振り
STEP800ではファームウェアの処理を簡単にするためにL6470, W5500, シフトレジスタで別々のSPIポートを使用しています。
ATSAMD21におけるSPIの割り振り方法はこちらが大変参考になります。

[https://learn.adafruit.com/using-atsamd21-sercom-to-add-more-spi-i2c-serial-ports](https://learn.adafruit.com/using-atsamd21-sercom-to-add-more-spi-i2c-serial-ports)

### W5500

| Pin | Function | SERCOM | SERCOM Alt |
|-----|----------|--------|------------|
| D22/MISO | MISO | - | SERCOM4.0 |
| D23/MOSI | MOSI | - | SERCOM4.2 |
| D24/SCK | SCK | - | SERCOM4.3 |

### L6470

| Pin | Function | SERCOM | SERCOM Alt |
|-----|----------|--------|------------|
| D6 | MISO | - | SERCOM3.2 |
| D11 | MOSI | - | SERCOM3.0 |
| D12 | SCK | - | SERCOM3.3 |

### Shift registers (DIP switch, brake output)

| Pin | Function | SERCOM | SERCOM Alt |
|-----|----------|--------|------------|
| D3 | MISO | - | SERCOM2.1 |
| D2 | MOSI | SERCOM2.2 | - |
| D0 | SCK | - | SERCOM2.3 |

## L6470

### クロック

motor ID 1のL64670のOSCINに16MHzの水晶発振器が接続されています。そこからIDの順に、OSCOUTとOSCINがデイジーチェーンされていますので、各L6470は「外部16MHz入力、反転出力(`EXT_16MHZ_OSCOUT_INVERT`)」に設定してください。 内部クロックを使うと、一定速運転時などに動きが徐々にずれてくる現象が発生します。

## ハードウェア的に使えないL6470の機能

### STCK

配線されていないので、Step Clock動作はできません。

### ADCIN

GNDに直結されていて使用できません。