---
title: STEP100/200
wp_id: 2164
slug: step100-200
lang: ja
link: "https://ponoor.com/docs/step100-200/"
date: "2022-01-28T11:46:43"
modified: "2022-02-03T16:16:49"
parent: 0
menu_order: 40
---

# STEP100/200

## 概要

STEP100/200はご自身で市販のモジュールを集めて組み立てていただく完全DIYの製品(?)です。

| Model | Motor Driver | 制御モータ数 | 要するに... |
| --- | --- | --- | --- |
| STEP100 | PowerSTEP01 | 1 | 小さいSTEP400 |
| STEP200 | L6470 | 2 | 小さいSTEP800 |

[ファームウェア](https://github.com/ponoor/step-series-universal-firmware)はオープンソースで提供しています。

このドキュメントでは主に組み立て方と、ファームウェアの書き込み方について説明しています。実際の使い方については、STEP400/800のドキュメントを参照の上、下記のように適宜MotorIDの範囲を読み替えてください。

| Model | 対応する機種 | MotorIDの範囲 |
| --- | --- | --- |
| STEP100 | STEP400 | 1, 255 |
| STEP200 | STEP800 | 1-2, 255 |

その他の異なる部分については[使い方](https://ponoor.com/docs/step100-200/usage/)で説明しています。

## 資料

- [Product/STEP100-200](https://ponoor.com/products/step100-200/)
- [ファームウェア](https://github.com/ponoor/step-series-universal-firmware)
- [フォーラム](https://github.com/ponoor/step-series-support/discussions)
- [Updates/ステッピングモータについて](https://ponoor.com/updates/2020/10/step400-weekly-update-01/)
- [Updates/OSCとプログラミング環境](https://ponoor.com/updates/2020/10/step400-weekly-update-02/)
- [Updates/機構部品の第一歩](https://ponoor.com/updates/2020/10/get-started-with-mechanical-parts/)
