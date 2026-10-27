---
title: 電磁ブレーキの接続
---

# 電磁ブレーキの接続

STEP400とSTEP800に電磁ブレーキをつなぐ方法です。ファームウェアは、どちらのボードでもブレーキを同じように制御します。ブレーキの役割と状態の変わり方は、[電磁ブレーキ](../guides/electromagnetic-brake.md)で説明しています。

## 全体像 {#overview}

どちらのボードにも、モータごとのブレーキ出力があります。出力は3.3Vのロジック信号で、ブレーキを直接駆動することはできません。ブレーキの電源を切り替える駆動回路が必要です。

- **STEP400**: STEP400用のブレーキ基板EMB-STEP400を使います。4つのブレーキを駆動する回路が載っています。仕様は[EMB-STEP400](../hardware/emb-step400.md)をご覧ください。
- **STEP800**: ボードにブレーキ出力（J2）がありますが、公式の駆動基板はありません。トランジスタ、MOSFET、リレーなどで、駆動回路を作ってください。

出力のコネクタのピン配置は、[STEP400](../hardware/step400.md#brake-output)と[STEP800](../hardware/step800.md#brake-output)にあります。

ブレーキを使うときは、モータごとに[`electromagnetBrakeEnable`](configuration-items.md#driversettings-electromagnetbrakeenable)（`/enableElectromagnetBrake`）で有効にして、移行時間（[`brakeTransitionDuration`](configuration-items.md#driversettings-braketransitionduration)。決め方は[移行時間](../guides/electromagnetic-brake.md#transition-duration)）を設定します。

### 出力のレベル {#logic}

**HIGHでブレーキを解放し、LOWで保持します。** これは両方のボードで同じです。STEP400はMCUのピンから出力し、STEP800はシフトレジスタ（74HC595）を通して出力します。駆動回路は、入力がLOWのときにブレーキが保持されるようにしてください。

## STEP400とEMB-STEP400 {#step400}

### ブレーキの電源 {#brake-power}

電磁ブレーキに必要な電圧を、EMB-STEP400に供給します。ブレーキの多くは24Vですが、使うモータのデータシートで確認してください。**電源は、モータの電源と共通にしてください**（理由は[使い方の注意](../guides/electromagnetic-brake.md#usage)をご覧ください）。

ボードには、DCジャックとユーロブロックの2種類の電源端子があります。2つの端子はボード上で並列につながっているので、**同時に給電することは絶対にしないでください。**

#### DCジャック {#brake-dc-jack}

- 外径5.5mm
- 内径2.1mm
- センタープラス

#### ユーロブロック {#brake-terminal-block}

3.81mmピッチ、2ピンのユーロブロックです。ボードに表示してある極性のとおりに接続してください。

[![](https://ponoor.com/cms/wp-content/uploads/2021/03/brake-power-700x525.jpg)](https://ponoor.com/cms/wp-content/uploads/2021/03/brake-power.jpg)

### ブレーキの接続 {#connecting-brake}

ブレーキ用の端子に、電磁ブレーキの線を接続します。ブレーキ基板の端子には、STEP400のモータと同じように番号が付いています。モータとブレーキは、それぞれ同じ番号の端子につないでください。

電磁ブレーキの多くには極性があります。ボードに書かれた正負の記号を見て接続してください。

### STEP400との接続 {#connecting-step400}

STEP400とEMB-STEP400は、付属の6ピンのリボンケーブルでつなぎます。

[![](https://ponoor.com/cms/wp-content/uploads/2021/03/brake-riboncable-700x525.jpg)](https://ponoor.com/cms/wp-content/uploads/2021/03/brake-riboncable.jpg)

## STEP800 {#step800}

STEP800のブレーキ出力（J2）には、8つのモータそれぞれの信号と、3.3V、GNDがあります。各信号を、作った駆動回路の入力につなぎます。公式の駆動基板はありません。

## 電源投入時とリセット時の出力 {#power-on}

電源の投入やリセットから、ファームウェアが起動するまでの間、出力はファームウェアの制御下にありません。モータに負荷が吊り下げられていると、負荷が落下するおそれがあるので、駆動回路で対策してください。ファームウェアでは防げません。[負荷を支えられない時間](../guides/electromagnetic-brake.md#unsupported)をご覧ください。

- **STEP400**: ファームウェアが起動するまで、出力のピンはどこにもつながっていない、浮いた状態です。駆動回路の入力をプルダウンして、出力が浮いている間はブレーキが保持されるようにしてください。EMB-STEP400は、各入力に抵抗を付けてプルダウンしています。
- **STEP800**: 電源投入時、シフトレジスタの状態は不定で、すべての出力が解放側になることがあります。その長さは、電源を入れてから約250msで、ほとんどはブートローダの時間です。リセット（リセットボタンや電源電圧の低下）のあとも、ファームウェアが起動するまでの約0.5sの間、出力は解放の状態のままです。

STEP800での対策は次のとおりです。

- ボードが[`/booted`](../reference/automatically-sent-messages.md#booted)を送ってから、ブレーキの電源を入れる。
- または、駆動回路を、電源を入れてからしばらくはブレーキを解放しない構成にする。

## 注意 {#notes}

- **ファームウェアを書き込む間は、電磁ブレーキを外してください。** 書き込みの間はファームウェアが動かず、STEP800ではブレーキ出力が解放側になることがあります。[ファームウェアのコンパイル](../maintenance/compile-the-arduino-sketch.md#uploading)をご覧ください。
- **ブレーキの電源は、モータの電源と共通にしてください。** [使い方の注意](../guides/electromagnetic-brake.md#usage)をご覧ください。
- 再起動、ウォッチドッグ、CPU動作異常: ボードは、再起動の前にブレーキを保持状態にします。[再起動、ウォッチドッグ、CPU動作異常](../guides/electromagnetic-brake.md#restart)をご覧ください。

## 関連するコマンドと設定項目 {#related}

<!-- osc-related: /enableElectromagnetBrake -->
<!-- generated:begin osc-related /enableElectromagnetBrake -->
**関連するコマンド**

| コマンド | 引数 | 説明 |
| --- | --- | --- |
| [`/enableElectromagnetBrake`](../reference/brake.md#enableelectromagnetbrake) | (int)motorID (bool)enable | 電磁ブレーキモードを有効・無効にします。 |
<!-- generated:end osc-related /enableElectromagnetBrake -->

<!-- osc-settings: driverSettings.electromagnetBrakeEnable, driverSettings.brakeTransitionDuration -->
<!-- generated:begin osc-settings driverSettings.electromagnetBrakeEnable, driverSettings.brakeTransitionDuration -->
**関連する設定項目**

| キー | 名称 | コマンド |
| --- | --- | --- |
| [`driverSettings.electromagnetBrakeEnable`](configuration-items.md#driversettings-electromagnetbrakeenable) | Electromagnetic brake enable | `/enableElectromagnetBrake` |
| [`driverSettings.brakeTransitionDuration`](configuration-items.md#driversettings-braketransitionduration) | Brake transition duration | `/setBrakeTransitionDuration` |
<!-- generated:end osc-settings driverSettings.electromagnetBrakeEnable, driverSettings.brakeTransitionDuration -->
