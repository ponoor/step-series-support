---
title: EMB-STEP400
---

# EMB-STEP400

EMB-STEP400は、STEP400用のブレーキ基板です。4つのモータの電磁ブレーキを駆動し、STEP400が制御します。電磁ブレーキとは何か、ボードがどう制御するかは、[電磁ブレーキ](../guides/electromagnetic-brake.md#what)で説明しています。配線は[電磁ブレーキの接続](../connections/electromagnetic-brake-wiring.md)をご覧ください。

## 仕様 {#specifications}

- 入力電圧: 5Vから48V
- 制御できるチャンネル数: 4
- 基板サイズ: 45 x 56mm

12V未満の電圧で使うときは、インジケータのLEDが見えないことがあります。

### 駆動電流 {#driving-current}

オンとオフを切り替えるMOSFETの[データシート](https://datasheet.lcsc.com/szlcsc/Winsok-Semicon-WSF28N06_C148431.pdf)上の定格は、60V、28Aです。実際の限界は、電源入力のターミナルブロックの定格の7Aです。この範囲内で、LEDやモータなど、別の負荷も駆動できます。

### 電源投入時の動作 {#power-on}

各MOSFETのゲートは、抵抗（回路図では10kΩ）でプルダウンされています。STEP400のファームウェアが起動するまでなど、STEP400からの入力が駆動されていないときは、ブレーキが保持されます。

## 基板外形図 {#drawing}

[![](https://ponoor.com/cms/wp-content/uploads/2021/03/step400-emb-dimension.png)](https://ponoor.com/cms/wp-content/uploads/2021/03/step400-emb-dimension.png)

[step400-emb-dimension.pdf](https://ponoor.com/cms/wp-content/uploads/2021/03/step400-emb-dimension.pdf)

## 回路図 {#schematic}

[![](https://ponoor.com/cms/wp-content/uploads/2021/03/stem400-emb-schematic.png)](https://ponoor.com/cms/wp-content/uploads/2021/03/stem400-emb-schematic.png)

[step400-brakeBoard-schematic.pdf](https://ponoor.com/cms/wp-content/uploads/2021/03/step400-brakeBoard-schematic.pdf)

## 付属品 {#accessories}

- 3.81mmピッチ、2ピンのユーロスタイル・ターミナルブロック5個
- 6ピンのリボンケーブル
