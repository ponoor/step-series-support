---
title: X-Nucleoの準備 - STEP100
---

# X-Nucleoの準備 - STEP100

X-NUCLEO-IHM03A1を、Ethernetシールドに重ねられるように改造する方法です。

## STEP100（X-NUCLEO-IHM03A1） {#step100}

IHM03A1とEthernetシールドでは、使うピンが次のように重なりますので、IHM03A1側でピンを変更します。

| Arduino | (Ethernet) | 初期状態 | 変更後 | ファームウェア | 備考 |
| --- | --- | --- | --- | --- | --- |
| D0 |  |  |  |  |  |
| D1 |  |  |  |  |  |
| D2 |  | FLAG | FLAG |  | 不使用 |
| D3 |  |  |  | LED | オプション |
| D4 | SD CS | BUSY |  | SD CS | #1 |
| D5 |  |  |  |  |  |
| D6 |  |  |  |  |  |
| D7 |  |  |  |  |  |
| D8 |  | RST | RST | RST - PowerSTEP01 |  |
| D9 |  | STCK | STCK |  | 不使用 |
| D10 | CS | CS |  | CS - W5500 | #2 |
| D11 |  | MOSI | MOSI | MOSI - PowerSTEP01 |  |
| D12 |  | MISO | MISO | MISO - PowerSTEP01 |  |
| D13 |  | SCK | SCK | SCK - PowerSTEP01 |  |
| A0 |  | ID | ID |  | 不使用 |
| A1 |  |  |  |  |  |
| A2 |  |  | CS | CS - PowerSTEP01 | #2 |
| A3 |  |  |  |  |  |
| A4 |  |  |  |  |  |
| A5 |  |  |  |  |  |
| MOSI | MOSI |  |  | MOSI - W5500 | SPIピンヘッダ |
| MISO | MISO |  |  | MISO - W5500 | SPIピンヘッダ |
| SCK | SCK |  |  | SCK - W5500 | SPIピンヘッダ |

### 1: SD CSとPowerSTEP01のBUSY {#sd-cs}

D4ピンは、EthernetシールドがmicroSDカードを読み取るときのCSピンですが、IHM03A1ではBUSYピンとしても使われています。残念ながら、どちらも簡単にはピンを変更できませんので、IHM03A1のほうで脚をカットします。BUSYピンは、PowerSTEP01がBUSY状態であることを表すピンですが、同じ情報をSPI経由で取得できますので、Arduinoにつなぐ必要はありません。切ってしまってかまいません。

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643345614045.png)

### 2: W5500のCSとPowerSTEP01のCS {#cs}

Ethernetシールドに載っているW5500（またはW5100）のCSピンと、IHM03A1に載っているPowerSTEP01のCSピンが、どちらもD10に配線されていますので、IHM03A1側を変更します。IHM03A1の`R10`についている0Ω抵抗を取り外し、`R9`のパッドに取り付けます。これで、PowerSTEP01のCSピンは、D10からA2ピンに変わります。

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643345121196.png)

抵抗を取り外すときは、両側のパッドを同時に加熱する必要があります。はんだごてを2本使うのが最もやりやすい方法です。
