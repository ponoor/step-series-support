---
title: 電圧モードと電流モード
---

# 電圧モードと電流モード

ステッピングモータは、一定の電圧で駆動する方式（電圧モード）と、一定の電流で駆動する方式（電流モード）で動かせます。このページでは、2つのモードの違い、KVALとTVAL、モードの切り替え方を説明します。

## 電圧制御と電流制御の違い {#difference}

ステッピングモータの制御方式には、定電圧制御（**電圧モード**）と定電流制御（**電流モード**）の2種類があります。電圧モードと電流モードを切り替えて使えるのはSTEP400だけで、STEP800は電圧モードのみです。`/setCurrentMode`や`/setTval`など電流モードのコマンドは、STEP800にはありません。詳しくは[STEP400とSTEP800の違い](../reference/differences-step400-step800.md)をご覧ください。2つのモードの違いは、STMicroelectronics社の[プレゼンテーション資料](https://www.st.com/content/dam/AME/2019/developers-conference-2019/presentations/STDevCon19_3.6_Using%20Powerstep01.pdf)にわかりやすくまとめられています。

実際に使う側にとっての違いを簡単にまとめると、次のとおりです。

- 電圧モードは静かで滑らかに回りますが、低速でしか回せません。
- 電流モードは音が大きいですが、高速まで回せます。

### STEP400を使ったテスト {#test}

テストのデモ動画: [電圧モードと電流モードのテスト（Vimeo）](https://vimeo.com/1239730082)

STEP400と、本体にマイクを取り付けたモータで、2つのモードを試しました。微細な音もとらえるためです。電圧モードでは、静かに回りましたが、800step/sを超えたあたりから振動が発生し、1,400step/sくらいでストールしました。電流モードでは、動作音は大きいものの、11,000step/sを超えるまで回り、その後に振動してストールしました。

## KVALとTVAL {#kval-tval}

電圧モードでは**KVAL**レジスタで駆動電圧を、電流モードでは**TVAL**レジスタで駆動電流を制御します。どちらも係数として働きます。KVALはモータに加える電圧が電源電圧の何割か、TVALは目標の電流を決めます。ドライバの内部では同じレジスタですが、ファームウェアは2つの値を別々に持ち、モードを切り替えるときにレジスタを書き換えます。一方のモードの値が、誤ってもう一方のモードで使われることはありません。

どちらも、HOLD、RUN、ACC、DECの4つの値があります。[`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval)と[`/setTval`](../reference/voltage-and-current-mode-settings.md#settval)は4つを一度に設定し、[`/setHoldKval`](../reference/voltage-and-current-mode-settings.md#setholdkval)、[`/setRunKval`](../reference/voltage-and-current-mode-settings.md#setrunkval)などは1つを設定します。[`/getKval`](../reference/voltage-and-current-mode-settings.md#getkval)、[`/getTval`](../reference/voltage-and-current-mode-settings.md#gettval)、[`/getTval_mA`](../reference/voltage-and-current-mode-settings.md#gettval_ma)は、レジスタではなく、設定した値を返します（電圧モードではTVALのレジスタに、電流モードではKVALのレジスタに書き込まれません）。

電磁ブレーキのモータでは、保持の値が自動的に引き上げられます。[電磁ブレーキ](electromagnetic-brake.md#hold-current)をご覧ください。

## 電圧モードの設定 {#voltage-mode-setting}

電圧モードでは、KVALで、電源電圧の何パーセントをモータに印加するかを指定します。高い電圧の電源を使うと、低速で回っているときに必要以上の電流が流れることがあります。この不均衡を補正するために、低速では印加電圧を下げ、速度が上がると印加電圧を上げるレジスタ群（BEMF補償）があります。[`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam)コマンドか、[ブラウザ設定ツール](../connections/browser-config-tool.md)で設定します。

レジスタ値の算出方法は、STMicroelectronics社のアプリケーションノート[AN4144](https://www.st.com/resource/en/application_note/dm00061093-voltage-mode-control-operation-and-parameter-optimization-stmicroelectronics.pdf)に記載されています。いくつかのモータについては、データシートの数値と実測値から算出した値を[モータ別のパラメータ例](../connections/example-parameters.md)に載せています。現在は少数ですが、今後増やす予定です。載っていないモータで、ご自身で値を求められた方は、私たちやコミュニティと共有していただけるとありがたいです。

これらの値は電源電圧によって変わります。ある電圧に合わせた値が、別の電圧では強すぎることがあります。24Vでは、既定のBEMF補償が強すぎました。電源を変えたときは、値を確かめ直してください。

## 電流モードの設定 {#current-mode-setting}

電流モードはSTEP400だけで使えます。TVALレジスタで、目標の電流を設定します。電流は、TVALの値に1を足して、78.125mAを掛けた値です。このため、値が0のときは0Aではなく、78.125mAです。PowerSTEP01の電流制御は10Aまで可能ですが、STEP400では電流検出抵抗の定格電力の制限で、TVALを約5Aまでに制限しています。上限を超える値は、拒否されずに上限に丸められます。値と電流の対応は[`/setTval`](../reference/voltage-and-current-mode-settings.md#settval)に載せています。現在は少数ですが、今後増やす予定です。載っていないモータで、ご自身で値を求められた方は、私たちやコミュニティと共有していただけるとありがたいです。過電流とストールの閾値にも、同じ種類の換算があります。[アラームと保護](alarms-and-protection.md#thresholds)をご覧ください。

高速で回しているときに目標の電流を流すには、高い電圧の電源が必要です。相電流が5Aになるとトルクはかなり強く、少しのミスが大きな危険につながります。このような場合は、産業用のモータドライバの使用をお勧めします。

## モードの切り替え {#switching}

モードの切り替えには、次のコマンドを使います。

- [`/setVoltageMode`](../reference/voltage-and-current-mode-settings.md#setvoltagemode): 電圧モードに切り替えます。
- [`/setCurrentMode`](../reference/voltage-and-current-mode-settings.md#setcurrentmode): 電流モードに切り替えます。

切り替える前に、モータが無励磁（HiZ）になっている必要があります。位置を保っている（励磁している）モータは無励磁ではありません。例えば、モータ1を電流モードに切り替えるときは、次の順にコマンドを送ります。

1. `/hardHiZ 1`
2. `/setCurrentMode 1`

モータが無励磁でないときは、`/error/command MotorNotHiZ`を返し、モードは変わりません。

電流モードでは、マイクロステップは1/16までしか使えません。それより細かい設定のモータを電流モードに切り替えると、マイクロステップの設定は1/16になります。電流モードのモータに対する[`/setMicrostepMode`](../reference/motor-driver-settings.md#setmicrostepmode)は、1/16より細かい設定に対して`CommandIgnored`を返します。マイクロステップの設定が変わると、座標系も変わります。例えば、1回転200ステップのモータでは、1/128マイクロステップで1回転が200×128=25600ステップ、1/16マイクロステップでは200×16=3200ステップです。

## 関連するコマンドと設定項目 {#related}

<!-- osc-related: drive_mode -->
<!-- generated:begin osc-related drive_mode -->
**関連するコマンド**

| コマンド | 引数 | 説明 |
| --- | --- | --- |
| [`/setVoltageMode`](../reference/voltage-and-current-mode-settings.md#setvoltagemode) | (int)motorID | 指定したモータを電圧モードに切り替えます。STEP800は常に電圧モードで動作しますので、この切替コマンドはSTEP400のみ利用可能です。 |
| [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval) | (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)decKVAL | KVAL4種をまとめて設定します。 |
| [`/getKval`](../reference/voltage-and-current-mode-settings.md#getkval) | (int)motorID | KVAL4種をまとめて取得します。 |
| [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) | (int)motorID (int)INT_SPEED (int)ST_SLP (int)FN_SLP_ACC (int)FN_SLP_DEC | BEMF補償パラメータのレジスタを設定します。各レジスタの設定値については電圧モードの設定を参照してください。 |
| [`/getBemfParam`](../reference/voltage-and-current-mode-settings.md#getbemfparam) | (int)motorID | BEMFパラメータを設定するレジスタ値を取得します。 |
| [`/setHoldKval`](../reference/voltage-and-current-mode-settings.md#setholdkval) | (int)motorID (int)holdKVAL | 停止時のKVALのみを設定します。 |
| [`/setRunKval`](../reference/voltage-and-current-mode-settings.md#setrunkval) | (int)motorID (int)runKVAL | 一定速運転時のKVALのみを設定します。 |
| [`/setAccKval`](../reference/voltage-and-current-mode-settings.md#setacckval) | (int)motorID (int)accKVAL | 加速時のKVALのみを設定します。 |
| [`/setDecKval`](../reference/voltage-and-current-mode-settings.md#setdeckval) | (int)motorID (int)decKVAL | 減速時のKVALのみを設定します。 |
| [`/setCurrentMode`](../reference/voltage-and-current-mode-settings.md#setcurrentmode) | (int)motorID | 指定したモータを電流モードに切り替えます。 |
| [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval) | (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL | TVAL4種をまとめて設定します。 |
| [`/getTval`](../reference/voltage-and-current-mode-settings.md#gettval) | (int)motorID | TVAL4種をまとめて取得します。 |
| [`/getTval_mA`](../reference/voltage-and-current-mode-settings.md#gettval_ma) | (int)motorID | TVAL4種をまとめて取得します。レジスタの値ではなく単位[mA]の設定値で返します。 |
| [`/setDecayModeParam`](../reference/voltage-and-current-mode-settings.md#setdecaymodeparam) | (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN | 電流制御アルゴリズムのパラメータのレジスタを設定します。各レジスタの設定値についてはPowerSTEP01のデータシートを参照してください。 |
| [`/getDecayModeParam`](../reference/voltage-and-current-mode-settings.md#getdecaymodeparam) | (int)motorID | 電流制御アルゴリズムのパラメータを設定するレジスタ値を取得します。 |
| [`/setHoldTval`](../reference/voltage-and-current-mode-settings.md#setholdtval) | (int)motorID (int)holdTVAL | 停止時のTVALのみを設定します。 |
| [`/setRunTval`](../reference/voltage-and-current-mode-settings.md#setruntval) | (int)motorID (int)runTVAL | 一定速運転時のTVALのみを設定します。 |
| [`/setAccTval`](../reference/voltage-and-current-mode-settings.md#setacctval) | (int)motorID (int)accTVAL | 加速時のTVALのみを設定します。 |
| [`/setDecTval`](../reference/voltage-and-current-mode-settings.md#setdectval) | (int)motorID (int)decTVAL | 減速時のTVALのみを設定します。 |
<!-- generated:end osc-related drive_mode -->

<!-- osc-settings: driverSettings.isCurrentMode, voltageMode, currentMode -->
<!-- generated:begin osc-settings driverSettings.isCurrentMode, voltageMode, currentMode -->
**関連する設定項目**

| キー | 名称 | コマンド |
| --- | --- | --- |
| [`driverSettings.isCurrentMode`](../connections/configuration-items.md#driversettings-iscurrentmode) | Current mode | `/setVoltageMode`, `/setCurrentMode` |
| [`voltageMode.KVAL_HOLD`](../connections/configuration-items.md#voltagemode-kval_hold) | KVAL_HOLD | `/setKval`, `/setHoldKval` |
| [`voltageMode.KVAL_RUN`](../connections/configuration-items.md#voltagemode-kval_run) | KVAL_RUN | `/setKval`, `/setRunKval` |
| [`voltageMode.KVAL_ACC`](../connections/configuration-items.md#voltagemode-kval_acc) | KVAL_ACC | `/setKval`, `/setAccKval` |
| [`voltageMode.KVAL_DEC`](../connections/configuration-items.md#voltagemode-kval_dec) | KVAL_DEC | `/setKval`, `/setDecKval` |
| [`voltageMode.INT_SPEED`](../connections/configuration-items.md#voltagemode-int_speed) | INT_SPEED | `/setBemfParam` |
| [`voltageMode.ST_SLP`](../connections/configuration-items.md#voltagemode-st_slp) | ST_SLP | `/setBemfParam` |
| [`voltageMode.FN_SLP_ACC`](../connections/configuration-items.md#voltagemode-fn_slp_acc) | FN_SLP_ACC | `/setBemfParam` |
| [`voltageMode.FN_SLP_DEC`](../connections/configuration-items.md#voltagemode-fn_slp_dec) | FN_SLP_DEC | `/setBemfParam` |
| [`voltageMode.STALL_TH`](../connections/configuration-items.md#voltagemode-stall_th) | STALL_TH | `/setStallThreshold` |
| [`voltageMode.lowSpeedOptimizeEnable`](../connections/configuration-items.md#voltagemode-lowspeedoptimizeenable) | Low speed optimize enable | `/enableLowSpeedOptimize` |
| [`voltageMode.lowSpeedOptimize`](../connections/configuration-items.md#voltagemode-lowspeedoptimize) | lowSpeedOptimize | `/setLowSpeedOptimizeThreshold` |
| [`currentMode.TVAL_HOLD`](../connections/configuration-items.md#currentmode-tval_hold) | TVAL_HOLD | `/setTval`, `/setHoldTval` |
| [`currentMode.TVAL_RUN`](../connections/configuration-items.md#currentmode-tval_run) | TVAL_RUN | `/setTval`, `/setRunTval` |
| [`currentMode.TVAL_ACC`](../connections/configuration-items.md#currentmode-tval_acc) | TVAL_ACC | `/setTval`, `/setAccTval` |
| [`currentMode.TVAL_DEC`](../connections/configuration-items.md#currentmode-tval_dec) | TVAL_DEC | `/setTval`, `/setDecTval` |
| [`currentMode.T_FAST`](../connections/configuration-items.md#currentmode-t_fast) | T_FAST | `/setDecayModeParam` |
| [`currentMode.TON_MIN`](../connections/configuration-items.md#currentmode-ton_min) | TON_MIN | `/setDecayModeParam` |
| [`currentMode.TOFF_MIN`](../connections/configuration-items.md#currentmode-toff_min) | TOFF_MIN | `/setDecayModeParam` |
<!-- generated:end osc-settings driverSettings.isCurrentMode, voltageMode, currentMode -->
