---
title: X-Nucleoの事前準備 – STEP100
wp_id: 2187
slug: step100
lang: ja
link: "https://ponoor.com/docs/step100-200/assemble/step100/"
date: "2022-01-28T13:54:28"
modified: "2022-02-02T21:49:36"
parent: 2169
menu_order: 14
---

# X-Nucleoの事前準備 &#8211; STEP100

## STEP100 (X-NUCLEO-IHM03A1)

IHM03A1 と Ethernet Shield では使用するピンが以下の通り重複するため、IHM03A1 側でピンの変更を行います。

| Arduino | (Ethernet) | 初期状態 | 変更後 | firmware | 備考 |
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

### 1: SD CS と PowerSTEP01 BUSY

Ethernet Shieldに乗っているSDカードを読み取る際にD4ピンをCSとして使用しますが、IHM03A1 においてもBUSYピンとして使われています。残念ながら両者ともピンを簡単に変更できないので、IHM03A1のほうで脚をカットしてしまいます。BUSYピンはPowerSTEP01がBUSY状態であることを表すピンですが、同じ情報をSPI経由で取得できるため、特段Arduinoと接続する必要はありません。切ってしまって大丈夫です。

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643345614045.png)

### 2: W5500 CS と PowerSTEP01 CS

Ethernet Shieldに乗っているW5500（またはW5100）のCSピンと、IHM03A1上のPowerSTEP01のCSピンがどちらもD10に配線されていますので、IHM03A1側を変更します。IHM03A1の`R10`についている0Ω抵抗を取り外し、それを`R9`のパッドに取り付けます。そうすると、PowerSTEP01のCSピンはD10からA2ピンへ変更されます。

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643345121196.png)

抵抗を取り外す際は、両側のパッドを同時に加熱する必要があります。はんだごてを2本使うのが最もやりやすいです。
