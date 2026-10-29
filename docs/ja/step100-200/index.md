---
title: STEP100/200
---

# STEP100/200

STEP100とSTEP200は、市販のモジュールを集めてご自身で組み立てる、完全に自作のモータドライバです。このセクションでは、材料の入手、組み立て、ファームウェアの書き込み、使い方の違いを説明します。

!!! warning "v2.1.0以降、実機では確かめていません"
    ファームウェアv2.2.0はSTEP100とSTEP200向けにビルドできますが、v2.1.0以降、実機では確かめていません。このセクションの手順は、ファームウェアのソースコードと、以前のドキュメントに基づいています。

## 概要 {#overview}

| 製品 | ドライバIC | モータの数 | 要するに |
| --- | --- | --- | --- |
| STEP100 | PowerSTEP01 | 1 | 小さいSTEP400 |
| STEP200 | L6470 | 2 | 小さいSTEP800 |

[ファームウェア](https://github.com/ponoor/step-series-universal-firmware)はオープンソースで提供しています。STEPシリーズのすべての製品を、同じソースからビルドします。

このセクションでは、主に組み立て方と、ファームウェアの書き込み方を説明します。実際の使い方は、STEP400とSTEP800のドキュメントを参照し、モータIDの範囲を適宜読み替えてください（表は[使い方](usage.md#motor-id)にあります）。そのほかの違いは[使い方](usage.md)で説明しています。

## ページの一覧 {#pages}

1. [材料](get-the-materials.md): Arduino、Ethernetシールド、X-NUCLEOボード、電源です。
2. [組み立て](assemble/index.md): X-NUCLEOボードの準備（[STEP100](assemble/step100.md)、[STEP200](assemble/step200.md)）、ボードの重ね方、電源とモータの[接続](assemble/connections.md)です。
3. [スケッチの書き込み](upload-the-sketch.md): ファームウェアをビルドして、Arduinoに書き込みます。
4. [使い方](usage.md): STEP400やSTEP800との違いです。

## 関連の情報 {#resources}

- [製品: STEP100-200](https://ponoor.com/products/step100-200/)
- [Updates: ステッピングモータについて](https://ponoor.com/updates/2020/10/step400-weekly-update-01/)
- [Updates: OSCとプログラミング環境](https://ponoor.com/updates/2020/10/step400-weekly-update-02/)
- [Updates: 機構部品の第一歩](https://ponoor.com/updates/2020/10/get-started-with-mechanical-parts/)

ファームウェア、フォーラム、ブラウザ設定ツールは、[トップページ](../index.md#resources)にあります。
