---
title: 使い方
wp_id: 2227
slug: usage
lang: ja
link: "https://ponoor.com/docs/step100-200/usage/"
date: "2022-01-28T22:45:54"
modified: "2022-02-03T15:52:51"
parent: 2164
menu_order: 36
---

# 使い方

## 使い方

基本的にはSTEP400/800と同じように制御できますので、STEP400/800の[チュートリアル](https://ponoor.com/docs/step-series/tutorial/)や、[コマンドリファレンス](https://ponoor.com/docs/step-series/osc-command-reference/)を参照してください。

STEP100はSTEP400のコマンドが、STEP200ではSTEP800のコマンドが使用できますが、モータの軸数が異なるので、MotorIDの範囲は以下の通りに変わります。

| Model | 対応する機種 | MotorIDの範囲 |
| --- | --- | --- |
| STEP100 | STEP400 | 1, 255 |
| STEP200 | STEP800 | 1-2, 255 |

チュートリアル用のサンプルファイルもMotorIDの範囲の違い以外は同様に使えます。

しかし異なっている点もいろいろとありますので、次に異なる項目ごとに説明します。

## 起動

X-Nucleoボードへモータ電源を供給しても、Arduino側へは電源が供給されませんので、別途ArduinoボードのDCジャックやUSBなどから別途電源を供給する必要があります。  
そのため、モータ電源をArduinoの後に入れると、Arduinoが起動時に送ったコマンドがモータドライバで受信されず、初期化に失敗してしまいます。とはいえ、逆にArduinoの電源が入っていない状態でモータドライバ側に電源を供給すると、Arduinoのピンの状態が不確定な状態のままになり、何か予期しない動作が起こる可能性も考えられます。  
またW5100を使った旧式のEthernetシールドでは、起動時のリセットに失敗する現象が頻繁にみられます。  
これらのことを考えると、確実な起動方法は以下です。

1. Arduino電源を供給する
2. モータ電源を供給する
3. ArduinoまたはEthernetシールドののリセットボタンを押して全体を再起動する

※STEP400/800ではモータ電源を供給すれば、確実にArduino部もEthernetシールドにあたる部分も起動するようになっています。

## SDカード

EthernetシールドにはSDカードスロットがついているものが多くあり、それを使えばconfigToolを用いた初期設定も可能です。ただし現状ではSTEP100/200に対応した設定書き出しツールは準備できていないため、STEP100はSTEP400のconfigファイルを、STEP200はSTEP800のconfigファイルを利用してください。  
STEP100/200で制御可能なモータ数を超えた設定データや、LIMITスイッチ関連の設定などは無視されます。

## DIPスイッチ

STEP100/200のファームウェアでは、IDを強制的に`1`に設定しています。複数台をネットワークに接続したい場合は、基板ごとにIDを書き換える必要があります。  
`boardsDef.h`に各基板ごとの定義があり、その中にある`#define ID 1`の部分の数値を書き換えてコンパイルしてください。

あるいはX-Nucleoボードのさらに上にシールドを差し込んで、自前でDIPスイッチをはんだ付けして取り付ける方法が考えられます。この場合はファームウェアのカスタムが必要です。例えば4桁のDIPスイッチをA1,A3,A4,A5ピンに接続した場合、`boardsDef.h` で、対応するボード定義に以下のコードを追加します。

```
    #define HAVE_DIP_SW
    #define DIP_SW_DIGITS   4
    const uint8_t dipSwPin[DIP_SW_DIGITS] = { A1, A3, A4, A5 };
```

## HOMEセンサ

STEP400/800ではHOMEセンサ用の端子はモータドライバICのSWピンから引き出されています。STEP100/200でも同様に、X-Nucleo上に引き出されているSWピンへセンサを接続します。このピンはプルアップされているので、センサやスイッチが反応したらGNDに接続されるようにします。

### STEP100 (X-NUCLEO-IHM03A1)

X-NUCLEO-IHM03A1上の`TP1`とラベリングされている、赤色のテストピンがSWピンです。この端子に直接はんだ付けして配線を取り出す必要があります。

![](https://ponoor.com/cms/wp-content/uploads/2022/01/IMG_4317.jpg)

ここにセンサからのケーブルを直接つけてしまうと不便なので、途中にコネクタを入れたほうがいいかもしれません。

### STEP200 (X-NUCLEO-IHM02A1)

IHM02A1では`J2`コネクタがSW端子です。基板上の白丸（●）が回路図での1番ピンを表しています。

![](https://ponoor.com/cms/wp-content/uploads/2022/01/IMG_4312.jpg)  
![](https://ponoor.com/cms/wp-content/uploads/2022/02/image.png)

例えば1番目のドライバのSW端子に接続する場合はこのような感じです。スイッチの変わりにジャンプワイヤーで動作をテストしています。

![](https://ponoor.com/cms/wp-content/uploads/2022/02/IMG_4321.jpg)

## LIMITセンサ

STEP100/200ではLIMITセンサ端子は定義していませんが、Arduinoの余っているピンをLIMITセンサとして利用することも可能です。この場合はファームウェアのカスタムが必要です。`boardsDef.h`にある各ボードの定義を編集します。

例えば以下のような定義を追加すると `D6`, `D7` にLIMITセンサ端子の役割を割り振ることができます。

```
    #define HAVE_LIMIT_GPIO
    // STEP100の場合
    const uint8_t limitSwPin[1] = { 6 };
    // STEP200の場合
    const uint8_t limitSwPin[2] = { 6,7 };
```
