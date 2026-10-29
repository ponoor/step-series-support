---
title: X-Nucleoの準備 - STEP200
---

# X-Nucleoの準備 - STEP200

X-NUCLEO-IHM02A1を、Ethernetシールドに重ねられるように改造する方法です。

## STEP200（X-NUCLEO-IHM02A1） {#step200}

| Arduino | (Ethernet) | 初期状態 | 変更後 | ファームウェア | 備考 |
| --- | --- | --- | --- | --- | --- |
| D0 |  |  |  |  |  |
| D1 |  |  |  |  |  |
| D2 |  |  |  |  |  |
| D3 |  | SCK | LED | LED | #1 |
| D4 | SD CS | STBY/RST | SD CS | SD CS | #2 |
| D5 |  |  |  |  |  |
| D6 |  |  |  |  |  |
| D7 |  |  |  |  |  |
| D8 |  |  | STBY/RST | RST - L6470 | #2 |
| D9 |  |  |  |  |  |
| D10 | CS |  |  | CS - W5500 |  |
| D11 |  | MOSI | MOSI | MOSI - L6470 |  |
| D12 |  | MISO | MISO | MISO - L6470 |  |
| D13 |  |  | SCK | SCK - L6470 | #1 |
| A0 |  |  |  |  |  |
| A1 |  |  |  |  |  |
| A2 |  | CS | CS | CS - L6470 |  |
| A3 |  |  |  |  |  |
| A4 |  |  |  |  |  |
| A5 |  |  |  |  |  |
| MOSI | MOSI |  |  | MOSI - W5500 | SPIピンヘッダ |
| MISO | MISO |  |  | MISO - W5500 | SPIピンヘッダ |
| SCK | SCK |  |  | SCK - W5500 | SPIピンヘッダ |

### 1: L6470のSCKの移動 {#sck}

初期状態では、IHM02A1に載っているL6470のSCKピンがD3になっていますが、これをArduinoのSPIピン配置に合わせて、D13へ移動します。IHM02A1の`SB34`についている0Ω抵抗を取り外し、`SB12`のパッドへ取り付けてください。この作業も、はんだごてが2本ないと難しいと思います。`SB34`の抵抗はニッパーで粉砕し、`SB12`のパッドをはんだを盛ってショートさせる方法もあるかもしれません。

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643345862191.png)  
この写真では、取り外した抵抗を`SB12`に取り付け直すのに苦戦して、汚くなってしまいました。

### 2: SD CSとL6470のSTBY/RST {#stby-rst}

STEP100の場合と同様に、microSDカードのCSピンとL6470のSTBY/RSTピンが、同じD4に割り当てられていますので、IHM02A1のほうで脚をカットします。ただし、カットしたSTBY/RSTピンはL6470の起動に必要ですので、ジャンパーワイヤで別のピンに割り当て直します。使っていないピンであればどこでもよいのですが、ここではD8を使います。X-NUCLEOボードのピンソケットで、D4とD8をつなぎます。

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643345928788.png)  
ArduinoとEthernetシールドに重ねた様子です。これで、X-NUCLEOボードのD4がD8に割り当て直されました。
