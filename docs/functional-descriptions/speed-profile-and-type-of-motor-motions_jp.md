## スピードプロファイル

### 概要

モータ動作に先立ち、あらかじめ設定しておく動作の加速度、減速度、最大速さです。 これらは

- モータのスペック
- 電源電圧
- 負荷
- 電圧制御か電流制御か

などによって取れる値の範囲が変わりますので、実際の環境で確かめながら値を設定していく必要があります。

### 設定する値

加速度acc, 減速度dec, 最大速さmaxSpeedの3種類の値です。[`/setMinSpeed`](https://ponoor.com/docs/step-series/osc-command-reference/speed-profile/#setminspeed_intmotorid_floatminspeed) によって最低の速さを設定することも可能です。これは実際の使用時に使うことはほぼありませんが、この速さは原点復帰時の [`/releaseSw`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#releasesw_intmotorid_boolact_booldir) の速さに適用されます。

### 設定コマンド

[`/setSpeedProfile`](https://ponoor.com/docs/step400/osc-command-reference/speed-profile/#setspeedprofile_intmotorid_floatacc_floatdec_floatmaxspeed) コマンドで、上記3つの値を設定できます。acc, dec はモータが停止していないと変更できませんが、 maxSpeedは常時変更が可能です。

## モータ動作の種類

### 一定速運転

あらかじめ設定されたスピードプロファイルの加速度・減速度で指定された速度へ到達し、その後一定速を維持するコマンドです。速度に0を指定するか、停止コマンドを送るまで回り続けます。指定できる速度の範囲は、スピードプロファイルの最大速さに制限されます。加速中と減速中はBUSY状態になります。

一定速運転をする代表的なコマンドが [`/run`](https://ponoor.com/docs/step400/osc-command-reference/motor-control/#run_intmotorid_floatspeed) です。そのほかにも [`/goUntil`](https://ponoor.com/docs/step400/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed) や [`/releaseSw`](https://ponoor.com/docs/step400/osc-command-reference/homing/#releasesw_intmotorid_boolact_booldir) なども含まれます。

### 位置決め運転

指定された位置へ向かって、スピードプロファイルに従って台形運転を行います。すなわち、スピードプロファイルの加速度に従って加速し、最大速さまで到達したら一定速で運転し、その後指定の減速度で減速しますが、指定位置で停止するように逆算したタイミングで減速を開始します。移動距離に比べてゆっくり加減速した場合などには、最大速さに達する前に減速を開始することもあります。

モータが停止するまでBUSY状態になります。位置決め運転の途中で割り込んで次の位置決め運転をすることはできません。

位置決め運転をする代表的なコマンドが [`/goTo`](https://ponoor.com/docs/step400/osc-command-reference/motor-control/#goto_intmotorid_intposition) や [`/move`](https://ponoor.com/docs/step400/osc-command-reference/motor-control/#move_intmotorid_intstep) です。その他にも [`/goHome`](https://ponoor.com/docs/step400/osc-command-reference/absolute-position-management/#gohome_intmotorid), [`/goMark`](https://ponoor.com/docs/step400/osc-command-reference/absolute-position-management/#gomark_intmotorid), [`/goToDir`](https://ponoor.com/docs/step400/osc-command-reference/motor-control/#gotodir_intmotorid_booldir_intposition) などが含まれます。

備考: [STEP-series Universal Firmware](https://github.com/ponoor/step-series-universal-firmware) では、 `/move` 以外の位置決めコマンドは、実行中のモーションコマンドに割り込むことができます。

### サーボモード

これはモータドライバの機能ではなく、ファームウェアで実装されている運転の種類です。一定速運転の速度を常時更新して、与えられた目標位置に追従するようにします。ラジコンのサーボモータのような動作方法です。このモードで動いている間は、ほかのモータ動作コマンドを送ることはできません。

詳しくは[サーボモード](https://ponoor.com/docs/step400/functional-description/servo-mode/)のページを参照してください。

### 停止の種類

以下の2種類の選択肢があり、合計4種類のコマンドがあります。

- スピードプロファイルに従って減速するか、瞬時に停止するか
- 停止後も励磁状態を保つか、ハイ・インピーダンス状態 (HiZ) にするか

| 停止後の状態 | 減速停止 | 瞬間停止 |
|--------------------|--------------|--------------|
| **励磁** | [SoftStop](https://ponoor.com/docs/step400/osc-command-reference/motor-control/#softstop_intmotorid) | [HardStop](https://ponoor.com/docs/step400/osc-command-reference/motor-control/#hardstop_intmotorid) |
| **HiZ** | [SoftHiZ](https://ponoor.com/docs/step400/osc-command-reference/motor-control/#softhiz_intmotorid) | [HardHiZ](https://ponoor.com/docs/step400/osc-command-reference/motor-control/#hardhiz_intmotorid) |

励磁状態とは、`KVAL_HOLD`に応じた電圧や`TVAL_HOLD`の値に応じた電流が流れて、モータの位置を保持するトルクがかかっている状態です。ハイ・インピーダンス状態は、電流が遮断されて保持トルクがない状態です。