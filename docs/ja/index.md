---
title: STEPシリーズ
---

# STEPシリーズ

STEPシリーズは、EthernetでOSC（Open Sound Control）メッセージを送って制御するステッピングモータドライバです。STEP400は4台、STEP800は8台のモータを駆動します。STEP100とSTEP200は、それぞれ1台と2台のモータを駆動する自作版です。

このドキュメントが対象とするファームウェアのバージョンは**v2.2.0**です。古いバージョンをお使いの場合は、更新の前に[移行ガイド](maintenance/migration-guide.md)をご覧ください。

初めての方は、[概要](getting-started/index.md)をご覧になってから、[クイックスタート](getting-started/quickstart.md)でモータを回してみてください。

## 目的から探す {#sections}

- **初めて動かす:** [概要](getting-started/index.md)（製品の違い、できること、OSCを送るソフトウェア）と[クイックスタート](getting-started/quickstart.md)（モータ1台を手順どおりに動かします）。
- **配線する、設定する:** [接続と設定](connections/power-supply-and-motor.md)。電源とモータ、センサとスイッチ、ネットワークとDIPスイッチ、電磁ブレーキ、microSDカードとブラウザ設定ツールでの設定です。
- **機能の仕組みを知る:** [機能ガイド](guides/communication-and-messages.md)。通信、電圧モードと電流モード、スピードプロファイル、原点復帰、サーボモード、電磁ブレーキ、アラームです。
- **コマンドを調べる:** [OSCリファレンス](reference/index.md)と[コマンド一覧](reference/command-list.md)。各コマンドの引数、範囲、初期値、返信です。
- **ボードの仕様を確かめる:** [ハードウェア](hardware/step400.md)（[STEP400](hardware/step400.md)、[STEP800](hardware/step800.md)、[EMB-STEP400](hardware/emb-step400.md)）。寸法、ピン割り振り、主な部品です。
- **ファームウェアを更新する、原因を調べる:** [保守](maintenance/firmware-update.md)。ファームウェアの更新、ビルド、USBシリアル診断、トラブルシューティング、変更履歴、移行ガイドです。
- **STEP100やSTEP200を作る:** [STEP100 / STEP200](step100-200/index.md)。材料、組み立て、ファームウェアです。

## 関連の情報 {#resources}

- 製品: [STEP400](https://ponoor.com/products/step400/)、[STEP800](https://ponoor.com/products/step800/)、[STEP100 / STEP200](https://ponoor.com/products/step100-200/)、[EMB-STEP400](https://ponoor.com/products/brakeboard-for-step400/)
- [ファームウェア](https://github.com/ponoor/step-series-universal-firmware)（オープンソース）
- [ブラウザ設定ツール](https://ponoor.com/tools/step-config/)
- [フォーラム](https://github.com/ponoor/step-series-support/discussions)（質問と議論）
