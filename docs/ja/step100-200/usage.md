---
title: 使い方
---

# 使い方

STEP100とSTEP200は、STEP400やSTEP800と同じように使えます。このページでは、違いを説明します。

!!! warning "v2.1.0以降、実機では確かめていません"
    ファームウェアv2.2.0はSTEP100とSTEP200向けにビルドできますが、v2.1.0以降、実機では確かめていません。このセクションの手順は、ファームウェアのソースコードと、以前のドキュメントに基づいています。

## 使い方 {#usage}

STEP400とSTEP800の[クイックスタート](../getting-started/quickstart.md)と[OSCリファレンス](../reference/index.md)をご覧ください。STEP100ではSTEP400のコマンドが、STEP200ではSTEP800のコマンドが使えます。サンプルファイルも同じように使えます。ボードにない機能のコマンドは使えません（下の[ブレーキ](#brake)と[LIMITスイッチ](#limit)をご覧ください）。

### モータID {#motor-id}

モータの数が異なりますので、モータIDの範囲は次のようになります。

| 製品 | 対応する製品 | モータIDの範囲 |
| --- | --- | --- |
| STEP100 | STEP400 | 1, 255 |
| STEP200 | STEP800 | 1-2, 255 |

範囲外のモータIDには、`MotorIdNotMatch`が返ります（[ボードへのメッセージ](../reference/index.md#messages-to-the-board)）。

## 起動 {#start-up}

X-NUCLEOボードにモータ電源を供給しても、Arduino側には給電されませんので、ArduinoのDCジャックやUSBから、別に電源を供給する必要があります。モータ電源をArduinoのあとに入れると、Arduinoが起動時に送ったコマンドがドライバICに届かず、初期化に失敗します。逆に、Arduinoの電源が入っていない状態でドライバ側に電源を供給すると、Arduinoのピンの状態が不定のままになり、予期しない動作が起こる可能性があります。W5100を使った旧式のEthernetシールドでは、起動時のリセットに失敗することもよくあります。

確実に起動する方法は、次のとおりです。

1. Arduinoに電源を供給する。
2. モータ電源を供給する。
3. ArduinoまたはEthernetシールドのリセットボタンを押して、全体を再起動する。

STEP400とSTEP800では、モータ電源を供給すれば、Arduino部分もEthernet部分も確実に起動します。

## microSDカード {#microsd}

Ethernetシールドには、microSDカードのスロットがあるものが多くあります。これを使って、[microSDカードでの設定](../connections/microsd-card.md)のとおりに設定ファイルを使えます。ボードがカードを読むのは、起動時だけです。

[ブラウザ設定ツール](../connections/browser-config-tool.md)は、STEP100とSTEP200を対応するボードとして扱います。ボードから製品名を受け取り、**Current Mode**のパネルはSTEP100だけに表示し、LIMITスイッチとブレーキの項目は表示しません（`HAVE_LIMIT_GPIO`を有効にすると、LIMITスイッチの項目が表示されます。下をご覧ください）。実際のSTEP100やSTEP200では試していません。対応する製品の設定ファイルも使えます。STEP100にはSTEP400の設定ファイルを、STEP200にはSTEP800の設定ファイルを使います。ファイルの製品名が異なっていても、ファームウェアは読み込みます（USBシリアルの`s`に、ファイルと製品が一致しないと表示されます）。ボードのモータの数を超える設定と、LIMITスイッチの設定は適用されません。

これらのボードには、カードを検出するピンがありませんので、ファームウェアは起動時にいつもカードの初期化を試みます。カードがないときは、初期化に失敗して、STEP400やSTEP800と同じように、初期値で起動します。

## DIPスイッチ {#dip-switch}

ファームウェアは、`boardsDef.h`にあるボードの定義でIDを固定しています。値は`1`です。ネットワークで複数のボードを使うときは、ボードごとにIDを変えます。`#define ID 1`の数値を書き換えて、ファームウェアをビルドしてください。IDの使われ方は、[ネットワークとDIPスイッチ](../connections/network-and-dip-switch.md#adding-id)をご覧ください。

あるいは、X-NUCLEOボードのさらに上にシールドを差し込んで、自前でDIPスイッチをはんだ付けする方法もあります。この場合は、ファームウェアのカスタマイズが必要です。たとえば、4桁のDIPスイッチをA1、A3、A4、A5ピンにつないだときは、`boardsDef.h`のボードの定義にある、コメントアウトされた`// #define HAVE_DIP_SW`の行を、次のコードに置き換えます（IDはスイッチから読まれ、`ID`は使われません）。

```
    #define HAVE_DIP_SW
    #define DIP_SW_DIGITS   4
    const uint8_t dipSwPin[DIP_SW_DIGITS] = { A1, A3, A4, A5 };
```

## HOMEスイッチ {#home}

STEP400とSTEP800では、HOMEスイッチ用のコネクタは、ドライバICのSWピンにつながっています。STEP100とSTEP200でも、同じように、X-NUCLEOボード上のSWピンにスイッチをつなぎます。このピンはプルアップされていますので、スイッチやセンサが反応したときに、ピンがGNDにつながるようにします。電気的な接続は、[スイッチやセンサの配線](../connections/sensors-and-switches.md#wiring)で説明しています。

### STEP100（X-NUCLEO-IHM03A1） {#home-step100}

X-NUCLEO-IHM03A1の`TP1`と書かれた赤いテストピンが、SWピンです。この端子に、直接はんだ付けして線を取り出す必要があります。

![](https://ponoor.com/cms/wp-content/uploads/2022/01/IMG_4317.jpg)

ここにセンサのケーブルを直接つけると不便ですので、途中にコネクタを入れたほうがよいでしょう。

### STEP200（X-NUCLEO-IHM02A1） {#home-step200}

IHM02A1では、`J2`コネクタがSWピンです。基板上の白丸（●）が、回路図の1番ピンを表しています。

![](https://ponoor.com/cms/wp-content/uploads/2022/01/IMG_4312.jpg)![](https://ponoor.com/cms/wp-content/uploads/2022/02/image.png)

1番目のドライバのSW端子につなぐ例です。スイッチの代わりに、ジャンパーワイヤで動作を試しています。

![](https://ponoor.com/cms/wp-content/uploads/2022/02/IMG_4321.jpg)

## LIMITスイッチ {#limit}

STEP100とSTEP200では、LIMITスイッチのピンは定義されていませんが、Arduinoの余っているピンをLIMITスイッチとして使えます。この場合は、ファームウェアのカスタマイズが必要です。`boardsDef.h`のボードの定義を編集します（コメントアウトされた`// #define HAVE_LIMIT_GPIO`の行を置き換えます）。定義すると、そのボードでLIMITスイッチのコマンドが使えるようになります。

たとえば、次の定義を足すと、`D6`と`D7`がLIMITスイッチのピンとして働きます。ピンはプルアップされていますので、スイッチはピンとGNDの間につなぎます。

```
    #define HAVE_LIMIT_GPIO
    // STEP100の場合
    const uint8_t limitSwPin[1] = { 6 };
    // STEP200の場合
    const uint8_t limitSwPin[2] = { 6,7 };
```

## 電磁ブレーキ {#brake}

STEP100とSTEP200には、電磁ブレーキの出力がありません。ブレーキのコマンドも使えません。
