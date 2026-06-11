---
title: X-Nucleoの事前準備 – STEP200
wp_id: 2197
slug: step200
lang: ja
link: "https://ponoor.com/docs/step100-200/assemble/step200/"
date: "2022-01-28T14:01:45"
modified: "2022-02-03T13:17:35"
parent: 2169
menu_order: 27
---

# X-Nucleoの事前準備 &#8211; STEP200

### STEP200 (X-NUCLEO-IHM02A1)

| Arduino | (Ethernet) | Default | Modified | firmware | 備考 |
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

#### 1: L6470 SCK の移動

初期状態ではIHM02A1に乗っているL6470のCSピンがD3になっていますが、これをArduino側のSPIピン配置に合わせるためにD13へ移動します。IHM02A1の`SB34`についている0Ω抵抗を取り外し、それを`SB12`のパッドへ取り付けてください。この作業もはんだごてが2本ないと難しいと思います。  
`SB34`の抵抗はニッパーで粉砕し、`SB12`のパッドははんだを盛ってショートさせる方法もあるかもしれません。。

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643345862191.png)  
この写真では取り外した抵抗を再度SB12に取り付けるのに苦戦し、汚くなってしまいました。。

#### 2: SD CS と L6470 STBY/RST

STEP100の場合と同様、SDカードのCSピンとL6470のSTBY/RSTピンが同じD4にアサインされていますので、IHM02A1のほうで脚をカットしてしまいます。ただしカットしたSTBY/RSTピンはL6470の起動に必要ですので、ジャンプワイヤで別のピンへ再アサインします。これは使ってないピンであればどこでもよいのですが、ここではD8を使用することにします。X-NucleoのピンソケットでD4とD8を接続します。

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643345928788.png)  
ArduinoとEthernet Shieldに重ねてみた様子。これでX-NucleoのD4がD8に再アサインされました。
