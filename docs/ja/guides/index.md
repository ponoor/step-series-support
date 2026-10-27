---
title: 機能ガイド
---

# 機能ガイド

機能ガイドでは、STEPシリーズの各機能の仕組みを説明します。考え方、状態とその変わり方、どのコマンドをどの順に使うかを書いています。引数や範囲、返信の形式は[OSCコマンドリファレンス](../reference/index.md)をご覧ください。ガイドから、必要なコマンドへリンクしています。

## ガイド一覧 {#guides}

- [通信とメッセージ](communication-and-messages.md): OSCメッセージの送受信の仕組み、`/setDestIp`、返信と自動送信されるメッセージ、引数のエラー。
- [電圧モードと電流モード](voltage-and-current-mode.md): モータの2つの駆動方式、KVALとTVAL、モードの切り替え方。
- [スピードプロファイルと動作](speed-profile-and-motions.md): 加速度・減速度・最大速度、一定速運転と位置決め運転、4種類の停止。
- [原点復帰と位置管理](homing-and-position.md): HOMEスイッチとLIMITスイッチによる基準位置の検出、衝突防止の設定。
- [サーボモード](servo-mode.md): リアルタイムに変わる目標位置への追従、PIDゲインの調整。
- [電磁ブレーキ](electromagnetic-brake.md): ブレーキの状態、各コマンドの作用、負荷を吊るときの注意。
- [アラームと保護](alarms-and-protection.md): 電源電圧の低下、過熱、過電流、ストールと、ボードからの通知。

接続と設定については、[接続と設定](../connections/index.md)をご覧ください。
