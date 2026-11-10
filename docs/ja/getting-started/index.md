---
title: 概要
---

# 概要

STEPシリーズの製品の違い、できること、OSCを送るソフトウェア、このドキュメントの読み方を紹介します。

## 製品 {#products}

どの製品も同じファームウェアで動きます。違いは、ドライバIC、モータの数、ボードの入出力です。

| 製品 | ドライバIC | モータの数 | 駆動方式 | スイッチ入力 | 電磁ブレーキの出力 | 形 |
| --- | --- | --- | --- | --- | --- | --- |
| [STEP400](../hardware/step400.md) | PowerSTEP01 | 4 | 電圧モードと電流モード | HOMEとLIMIT | 3.3Vのロジック出力（J7）。ブレーキの駆動には[EMB-STEP400](../hardware/emb-step400.md)ボードを使用 | 完成品 |
| [STEP800](../hardware/step800.md) | L6470 | 8 | 電圧モード | HOME | 3.3Vのロジック出力（J2）。駆動回路が別に必要 | 完成品 |
| STEP100 | PowerSTEP01 | 1 | 電圧モードと電流モード | HOME | なし | 自作 |
| STEP200 | L6470 | 2 | 電圧モード | HOME | なし | 自作 |

STEP400とSTEP800のブレーキの出力はロジック信号なので、ブレーキを駆動するには駆動回路が必要です。[電磁ブレーキの接続](../connections/electromagnetic-brake-wiring.md)をご覧ください。

コマンドは製品に共通ですが、ボードにない機能のコマンドは、そのボードでは使えません。STEP400とSTEP800で異なるコマンドは、[STEP400とSTEP800の違い](../reference/differences-step400-step800.md)にまとめています。電圧モードと電流モードについては、[電圧モードと電流モード](../guides/voltage-and-current-mode.md)をご覧ください。

STEP100とSTEP200は、Arduino Zero、Ethernetシールド、X-NUCLEOボードで作ります。ファームウェアはビルドできますが、v2.1.0以降は実機で確かめていません。[STEP100 / STEP200](../step100-200/index.md)をご覧ください。

## できること {#features}

- **モータを指定の速度で回す、指定の位置まで動かす:** [スピードプロファイルと動作の種類](../guides/speed-profile-and-motions.md)。
- **基準の位置を見つける:** [原点復帰と位置管理](../guides/homing-and-position.md)。HOMEスイッチとLIMITスイッチを使います。
- **リアルタイムに変わる目標にモータを追従させる:** [サーボモード](../guides/servo-mode.md)。
- **モータの駆動方式を選ぶ:** [電圧モードと電流モード](../guides/voltage-and-current-mode.md)。KVALとTVALの決め方も説明しています。
- **モータに通電していないときに負荷を保持する:** [電磁ブレーキ](../guides/electromagnetic-brake.md)。
- **ボードの保護と通知を知る:** [アラームと保護](../guides/alarms-and-protection.md)。ボードが返す返信と、ボードが自分から送るメッセージは[通信とメッセージ](../guides/communication-and-messages.md)で説明しています。
- **設定を保存する:** [設定の仕組み](../connections/how-settings-work.md)。ボードは起動時にmicroSDカードから設定を読みます。設定は[ブラウザ設定ツール](../connections/browser-config-tool.md)で編集できます。

## OSCを送るソフトウェア {#software}

STEPシリーズはOpen Sound Control（OSC）プロトコルで通信しますので、OSCを送受信するアプリケーション（またはプログラム）が必要です。多くの環境で扱えます。次のサンプルファイルを用意しています。

- [Max](https://github.com/ponoor/step-series-example-Max)（おすすめです。サンプルが最も機能を網羅しています。[Maxをダウンロード](https://cycling74.com/downloads)）
- [Processing](https://github.com/yuskegoto/STEP400_Processing)（提供: [@yuskegoto](https://github.com/yuskegoto)）
- [openFrameworks](https://github.com/ponoor/step-series-example-openFrameworks)（提供: [@niimi](https://github.com/niimi)）
- [Unity](https://github.com/ponoor/step-series-example-Unity)（提供: [@niimi](https://github.com/niimi)）
- [TouchDesigner](https://github.com/ponoor/step-series-example-TouchDesigner)（提供: [@loveandsheep](https://github.com/loveandsheep)、[@yuskegoto](https://github.com/yuskegoto)）
- [Node-RED](https://github.com/yuskegoto/STEP400_Node-RED)（提供: [@yuskegoto](https://github.com/yuskegoto)）
- [Pythonライブラリ](https://github.com/ponoor/python-step-series)（提供: [@JulianOrteil](https://github.com/JulianOrteil)）

## このドキュメントの構成 {#organization}

ページは、読む目的によって4種類に分かれています。それぞれの種類にはその目的に必要な情報を書き、ほかはほかの種類に任せて、ページどうしをリンクでつないでいます。

- **はじめに**（このセクション）: 初めて動かす手順です。1本道で、説明は最小限です。[クイックスタート](quickstart.md)をご覧ください。
- **[接続と設定](../connections/index.md)**: 手順です。配線、ネットワーク、ボードの設定の方法を書いています。
- **[機能ガイド](../guides/index.md)**: 説明です。機能の仕組み、どのコマンドをどの順に使うか、注意点を書いています。
- **[OSCリファレンス](../reference/index.md)**: 調べるためのページです。各コマンドの正確な仕様（引数、範囲、初期値、返信）を書いています。値を確かめるときはここをご覧ください。値はリファレンスにだけ書いています。

このほか、[ハードウェア](../hardware/step400.md)にはボードのデータ、[保守](../maintenance/index.md)にはファームウェアの更新、ビルド、診断、トラブルシューティング、[STEP100 / STEP200](../step100-200/index.md)には自作版のための説明があります。
