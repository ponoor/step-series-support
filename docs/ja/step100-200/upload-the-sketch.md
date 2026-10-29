---
title: スケッチの書き込み
---

# スケッチの書き込み

STEP100またはSTEP200向けにファームウェアをビルドして、Arduinoに書き込む方法です。すべての製品に共通の手順は[ファームウェアのコンパイル](../maintenance/compile-the-arduino-sketch.md)にあります。このページには、STEP100とSTEP200だけの手順を書いています。

!!! warning "v2.1.0以降、実機では確かめていません"
    ファームウェアv2.2.0はSTEP100とSTEP200向けにビルドできますが、v2.1.0以降、実機では確かめていません。このセクションの手順は、ファームウェアのソースコードと、以前のドキュメントに基づいています。

## PlatformIOを使う場合 {#platformio}

<https://github.com/ponoor/step-series-universal-firmware>からファームウェアを入手し、[PlatformIOでのコンパイル](../maintenance/compile-the-arduino-sketch.md#platformio)のとおりにPlatformIOで開きます。ライブラリは自動でインストールされます。

### 環境の選択 {#select-env}

STEP100なら環境`step100`、STEP200なら環境`step200`を選びます。選び方は[ボードの選択](../maintenance/compile-the-arduino-sketch.md#select-board)にあります。`boardsDef.h`のボードの行は、すべてコメントアウトしたままにしてください。

どちらの環境も、ボード`zeroUSB`（Arduino Zero）向けにビルドします。製品に合ったドライバのライブラリが必要です。STEP100はPonoor PowerSTEP01 Library、STEP200はPonoor L6470 Libraryで、`platformio.ini`がGitHubのタグのZIPから取得します。

### Arduino M0とMETRO M0 Expressの場合 {#m0}

v2.2.0の`platformio.ini`には、Arduino M0のボード定義（`mzeroUSB`）やMETRO M0 Express用の環境はありません。以前の版の設定例がコメントアウトされて残っているだけで、v2.2.0ではそのままでは動きません。環境`step100`または`step200`を使って、Arduino Zeroとしてビルドしてください。METRO M0 Expressについては、このボード専用の定義ではUSBシリアルの挙動が異なり、[USBシリアル診断](../maintenance/usb-serial-diagnosis.md)がうまく動かないと、`platformio.ini`のコメントにも書かれています。

Arduino M0のハードウェア（D2とD4が入れ替わっています）のボードでは、`MZERO_WITH_ZERO_BOOTLOADER`を定義します（[Arduino ZeroかM0か](get-the-materials.md#zero-or-m0)）。定義すると、microSDカードのCSピンが、Arduino Zeroの番号でD2になります。これは、M0ではD4にあたります。PlatformIOでは、環境のビルドフラグに足します。

```ini
[env:step100]
extends = samd_base
build_flags =
	${samd_base.build_flags}
	-D STEP100_R1
	-D MZERO_WITH_ZERO_BOOTLOADER
```

## Arduino IDEを使う場合 {#arduino-ide}

手順は[Arduino IDEでのコンパイル](../maintenance/compile-the-arduino-sketch.md#arduino-ide)にあります。SAMDコアをインストールし、ライブラリをインストールし、最新のリリースのスケッチ（"Assets"にある`step-series-universal-firmware.zip`）を開きます。STEP100とSTEP200では、次の点に注意してください。

- **ライブラリ:** 共通のライブラリに加えて、STEP100は[Ponoor PowerSTEP01 Library](https://github.com/ponoor/Ponoor_PowerSTEP01_Library)、STEP200は[Ponoor L6470 Library](https://github.com/ponoor/Ponoor_L6470_Library)をインストールします。版は[ライブラリ](../maintenance/compile-the-arduino-sketch.md#libraries)にあります。
- **`boardsDef.h`でボードを選ぶ:** ファイルの冒頭にある、使う製品のコメント`//`を外します。STEP100の場合は次のようになります。

  ```
  // Products
  // Arduino IDE: uncomment ONE line to select the board.
  // PlatformIO: pass the board as a build flag instead (e.g. -D STEP800_R1).
  // #define STEP400_R1
  // #define STEP800_R1

  // X-Nucleos
  #define STEP100_R1 // X-NUCLEO-IHM03A1, PowerSTEP01 x1
  // #define STEP200_R1 // X-NUCLEO-IHM02A1, L6470 x2
  ```

- **Arduino M0のハードウェア:** D2とD4が入れ替わっているボードでは、次の行のコメントも外します。

  ```
  // #define MZERO_WITH_ZERO_BOOTLOADER
  ```

- **ボード:** "Tools" -> "Board"から"Arduino Zero (Native USB Port)"を選んで、コンパイルします。

## 書き込み {#uploading}

PCとArduinoをUSBでつなぎ、"Tools" -> "Port"からシリアルポートを選んで、書き込みます。先に[ファームウェアを書き込むときの注意](../maintenance/compile-the-arduino-sketch.md#uploading)をご覧ください。
