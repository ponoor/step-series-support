---
title: スピードプロファイルと動作
---

# スピードプロファイルと動作

スピードプロファイルは、モータをどのように加速・減速し、どの速度で回すかを決めます。このページでは、スピードプロファイル、それを使ったモータ動作の種類、4種類の停止を説明します。

## スピードプロファイル {#speed-profile}

### 概要 {#overview}

スピードプロファイルは、モータが動作する前にあらかじめ設定しておく、加速度（acc）、減速度（dec）、最大速度（maxSpeed）です。モータが取れる値の範囲は、次のものによって変わります。

- モータのスペック
- 電源電圧
- 負荷
- 電圧モードか電流モードか

ファームウェアには既定の値がありますが、実際の環境に合わせて値を設定する必要があります。試行錯誤が必要です。

### 設定の方法 {#setting}

[`/setSpeedProfile`](../reference/speed-profile.md#setspeedprofile)で、3つの値を設定します。加速度と減速度は、モータが停止している（または無励磁の）ときしか設定できません。モータが回転している間は、`/error/command MotorNotStopped`を返し、元の値のままです。最大速度は、いつでも設定できます。

モータの停止中にしかドライバに書き込めない設定は、ほかにもあります。[`/setAcc`](../reference/speed-profile.md#setacc)、[`/setDec`](../reference/speed-profile.md#setdec)、[`/setMinSpeed`](../reference/speed-profile.md#setminspeed)、[`/enableLowSpeedOptimize`](../reference/motor-driver-settings.md#enablelowspeedoptimize)と、それぞれのRaw版です。どのコマンドがどの状態で実行できるかは、各コマンドの「実行可能タイミング」に載せています。[コマンドを実行可能なタイミング](../reference/index.md)もご覧ください。

加速度と減速度は、ドライバのレジスタで表せる最も近い値に丸められます。[`/getSpeedProfile`](../reference/speed-profile.md#getspeedprofile)が返す値は、設定した値と少し異なることがあります。

[`/setMinSpeed`](../reference/speed-profile.md#setminspeed)で、最小速度（minSpeed）も設定できます。実際の用途で使うことはほとんどありませんが、原点復帰の2段階目の[`/releaseSw`](../reference/homing.md#releasesw)（[原点復帰コマンド](homing-and-position.md#homing-commands)）では、この速度でモータが回ります。`/releaseSw`では、ドライバは少なくとも5step/sで回ります。低速最適化が有効なとき（最小速度が0になります）も同じです。

## モータ動作の種類 {#motions}

### 一定速運転 {#constant-speed}

[`/run`](../reference/motor-control.md#run)は、モータを一定の速度で回します。スピードプロファイルの加速度・減速度に従って指定した速度に達し、`/run 0`か停止コマンドを送るまで、その速度を保ちます。スピードプロファイルの最大速度を超えては回りません。それより速い速度は、最大速度に制限されます。加速中と減速中は、BUSY状態になります。

[`/goUntil`](../reference/homing.md#gountil)と[`/releaseSw`](../reference/homing.md#releasesw)も、一定速運転のコマンドです。

### 位置決め運転 {#positioning}

位置決め運転は、指定した位置へ向かって、スピードプロファイルに従って台形で運転します。設定した加速度で加速し、最大速度に達したら一定速で運転し、設定した減速度で減速します。減速は、指定した位置で停止するように逆算したタイミングで始まります。移動距離が短いときや、加速・減速がゆっくりのときは、最大速度に達する前に減速が始まることがあります。モータが停止するまで、BUSY状態になります。

代表的なコマンドは[`/goTo`](../reference/motor-control.md#goto)と[`/move`](../reference/motor-control.md#move)です。[`/goHome`](../reference/position-management.md#gohome)、[`/goMark`](../reference/position-management.md#gomark)、[`/goToDir`](../reference/motor-control.md#gotodir)も位置決め運転です。

運転中の位置決め運転に、別の位置決め運転で割り込めます。ただし`/move`は除きます。[`/goTo`](../reference/motor-control.md#goto)、[`/goToDir`](../reference/motor-control.md#gotodir)、[`/goHome`](../reference/position-management.md#gohome)、[`/goMark`](../reference/position-management.md#gomark)は、モータがBUSY状態でも受け付けられます（ファームウェアが先にBUSY状態を解除します）。`/move`は受け付けられません。モータが回転している間はドライバが無視し、ボードは`/error/command CommandIgnored`を返します。

### サーボモード {#servo-mode}

サーボモードは、モータドライバの機能ではなく、ファームウェアが実装している運転の種類です。一定速運転を更新し続けて、リアルタイムに与える目標位置へ追従します。ラジコンのサーボモータのような動作方法です。このモードで動いている間は、ほかのモータ動作コマンドは`InServoMode`で拒否されます。[サーボモード](servo-mode.md)をご覧ください。

## 停止の種類 {#stops}

2つの選択肢があり、合計4種類のコマンドがあります。

- スピードプロファイルに従って減速して停止するか、即座に停止するか
- 停止後も励磁したままにするか、無励磁（HiZ）にするか

| 停止後の状態 | 減速停止 | 即停止 |
| --- | --- | --- |
| 励磁 | [`/softStop`](../reference/motor-control.md#softstop) | [`/hardStop`](../reference/motor-control.md#hardstop) |
| 無励磁 | [`/softHiZ`](../reference/motor-control.md#softhiz) | [`/hardHiZ`](../reference/motor-control.md#hardhiz) |

励磁状態では、KVAL_HOLDやTVAL_HOLDに応じた電圧や電流がモータに流れて、モータは位置を保ちます。無励磁（HiZ）とは、モータドライバの出力が高インピーダンスになり、モータに電流が流れない状態です。モータは位置を保てません。**モータが負荷を支えているときは、無励磁にすると、負荷が落下したり、位置がずれたりすることがあります。**

電磁ブレーキのモータでは、無励磁にするコマンドはブレーキも保持状態にします。ブレーキの状態によって、停止コマンドの作用が異なります。[電磁ブレーキ](electromagnetic-brake.md#commands)をご覧ください。

## 関連するコマンドと設定項目 {#related}

<!-- osc-related: speed_profile, motion -->
<!-- generated:begin osc-related speed_profile, motion -->
**関連するコマンド**

| コマンド | 引数 | 説明 |
| --- | --- | --- |
| [`/setSpeedProfile`](../reference/speed-profile.md#setspeedprofile) | (int)motorID (float)acc (float)dec (float)maxSpeed | スピードプロファイルの加速度（`acc`）、減速度（`dec`）、最大速度（`maxSpeed`）をまとめて設定します。 |
| [`/getSpeedProfile`](../reference/speed-profile.md#getspeedprofile) | (int)motorID | スピードプロファイルのacc, dec, maxSpeedをまとめて取得します。 |
| [`/setFullstepSpeed`](../reference/speed-profile.md#setfullstepspeed) | (int)motorID (float)fullstepSpeed | マイクロステップモードが自動でフルステップモードに切り替わる閾値を設定します。 |
| [`/getFullstepSpeed`](../reference/speed-profile.md#getfullstepspeed) | (int)motorID | マイクロステップモードが自動でフルステップモードに切り替わる閾値を取得します。 |
| [`/setMaxSpeed`](../reference/speed-profile.md#setmaxspeed) | (int)motorID (float)maxSpeed | スピードプロファイルの最大速度を設定します。 |
| [`/setAcc`](../reference/speed-profile.md#setacc) | (int)motorID (float)acc | スピードプロファイルの加速度を設定します。 |
| [`/setDec`](../reference/speed-profile.md#setdec) | (int)motorID (float)dec | スピードプロファイルの減速度（deceleration）を設定します。 |
| [`/setMinSpeed`](../reference/speed-profile.md#setminspeed) | (int)motorID (float)minSpeed | スピードプロファイルの最小速度を設定します。この値は`/releaseSw`時のモータ回転速度にも使用されます。Low speed optimization（`/enableLowSpeedOptimize`）が有効になっている場合、minSpeedは強制的に0になります。 |
| [`/getMinSpeed`](../reference/speed-profile.md#getminspeed) | (int)motorID | スピードプロファイルの最小速度を返します。 |
| [`/getSpeed`](../reference/speed-profile.md#getspeed) | (int)motorID | モータの現在の速度を返します。 |
| [`/setSpeedProfileRaw`](../reference/speed-profile.md#setspeedprofileraw) | (int)motorID (int)acc (int)dec (int)maxSpeed | ドライバICのレジスタ値（Raw）で、スピードプロファイルのacc, dec, maxSpeedを設定します。 |
| [`/getSpeedProfileRaw`](../reference/speed-profile.md#getspeedprofileraw) | (int)motorID | ドライバICのレジスタ値（Raw）で、スピードプロファイルのacc, dec, maxSpeedを取得します。 |
| [`/setMaxSpeedRaw`](../reference/speed-profile.md#setmaxspeedraw) | (int)motorID (int)maxSpeed | レジスタ値（Raw）で、スピードプロファイルの最大速度を設定します。 |
| [`/setMinSpeedRaw`](../reference/speed-profile.md#setminspeedraw) | (int)motorID (int)minSpeed | レジスタ値（Raw）で、スピードプロファイルの最小速度を設定します。 |
| [`/setFullstepSpeedRaw`](../reference/speed-profile.md#setfullstepspeedraw) | (int)motorID (int)fullstepSpeed | レジスタ値（Raw）で、フルステップに切り替わる速度の閾値を設定します。 |
| [`/setAccRaw`](../reference/speed-profile.md#setaccraw) | (int)motorID (int)acc | レジスタ値（Raw）で、スピードプロファイルの加速度を設定します。 |
| [`/setDecRaw`](../reference/speed-profile.md#setdecraw) | (int)motorID (int)dec | レジスタ値（Raw）で、スピードプロファイルの減速度を設定します。 |
| [`/run`](../reference/motor-control.md#run) | (int)motorID (float)speed | モータを指定速度で回転させます。事前に設定したスピードプロファイルの加速度に従って加速します。指定する回転速度は、maxSpeedを超えるとmaxSpeedでリミットされます。指定速度に到達するまではBUSY状態になります。 |
| [`/move`](../reference/motor-control.md#move) | (int)motorID (int)step | 事前に設定したスピードプロファイルに従って、指定ステップ数移動します。指定ステップ数を移動し終わるまではBUSY状態になります。このコマンドはモータが停止していないと実行できません。 |
| [`/goTo`](../reference/motor-control.md#goto) | (int)motorID (int)position | 事前に設定したスピードプロファイルに従って、指定位置まで最短経路で移動します。指定位置まで移動し終わるまではBUSY状態になります。 |
| [`/goToDir`](../reference/motor-control.md#gotodir) | (int)motorID (bool)DIR (int)position | 事前に設定したスピードプロファイルに従って、指定位置まで指定方向で移動します。指定位置まで移動し終わるまではBUSY状態になります。 |
| [`/softStop`](../reference/motor-control.md#softstop) | (int)motorID | スピードプロファイルに従って減速したのち、モータを励磁したまま停止します。モータが停止するまではBUSY状態になります。もともと無励磁状態だった場合は、停止したままモータが励磁します。 |
| [`/hardStop`](../reference/motor-control.md#hardstop) | (int)motorID | モータを即停止し、励磁したままにします。モータが停止するまではBUSY状態になります。もともと無励磁状態だった場合は、停止したままモータが励磁します。 |
| [`/softHiZ`](../reference/motor-control.md#softhiz) | (int)motorID | スピードプロファイルに従って減速停止してから、モータを無励磁にします。モータが停止するまではBUSY状態になります。 |
| [`/hardHiZ`](../reference/motor-control.md#hardhiz) | (int)motorID | モータを即座に無励磁にします。モータが停止するまではBUSY状態になります。 |
| [`/combine/run`](../reference/motor-control.md#combine-run) | (int)motorID1 (int)motorID2 (float)speed | 2つのモータに対する`/run`と同じです。速度の符号が方向になります。絶対値が範囲を超える速度は、ドライバライブラリによってレジスタの最大値（0xFFFFF、約15625step/s）に制限されます。 |
| [`/combine/move`](../reference/motor-control.md#combine-move) | (int)motorID1 (int)motorID2 (int)step | 2つのモータに対する`/move`と同じです。絶対値が4,194,303（22ビット）を超えるステップ数は拒否されず、ドライバライブラリによって4,194,303に制限されます。 |
| [`/combine/goTo`](../reference/motor-control.md#combine-goto) | (int)motorID1 (int)motorID2 (int)position | 2つのモータに対する`/goTo`と同じです。範囲外の位置は拒否されません。4,194,303を超える位置は、ドライバライブラリによって4,194,303に制限され、ドライバはこれを-1として読みます。それ以外の位置は、下位22ビットだけが使われ、符号付きの数として読まれます。2,097,152は-2,097,152に、-2,097,153は2,097,151になります。 |
| [`/combine/goToDir`](../reference/motor-control.md#combine-gotodir) | (int)motorID1 (int)motorID2 (bool)DIR (int)position | 2つのモータに対する`/goToDir`と同じです。範囲外の位置は拒否されません。4,194,303を超える位置は、ドライバライブラリによって4,194,303に制限され、ドライバはこれを-1として読みます。それ以外の位置は、下位22ビットだけが使われ、符号付きの数として読まれます。2,097,152は-2,097,152に、-2,097,153は2,097,151になります。 |
| [`/combine/softStop`](../reference/motor-control.md#combine-softstop) | (int)motorID1 (int)motorID2 | 2つのモータに対する`/softStop`と同じです。motorID1、続いてmotorID2に対して、`/softStop`として処理されます。 |
| [`/combine/hardStop`](../reference/motor-control.md#combine-hardstop) | (int)motorID1 (int)motorID2 | 2つのモータに対する`/hardStop`と同じです。motorID1、続いてmotorID2に対して、`/hardStop`として処理されます。 |
| [`/combine/softHiZ`](../reference/motor-control.md#combine-softhiz) | (int)motorID1 (int)motorID2 | 2つのモータに対する`/softHiZ`と同じです。motorID1、続いてmotorID2に対して、`/softHiZ`として処理されます。 |
| [`/combine/hardHiZ`](../reference/motor-control.md#combine-hardhiz) | (int)motorID1 (int)motorID2 | 2つのモータに対する`/hardHiZ`と同じです。motorID1、続いてmotorID2に対して、`/hardHiZ`として処理されます。 |
| [`/runRaw`](../reference/motor-control.md#runraw) | (int)motorID (int)speed | レジスタ値（Raw）で指定した速度で、モータを回転させます。速度の符号が方向になります。 |
| [`/goUntilRaw`](../reference/motor-control.md#gountilraw) | (int)motorID (bool)ACT (int)speed | `/goUntil`と同じですが、速度にレジスタ値（Raw）を使います。速度の符号が方向になります。 |
| [`/combine/runRaw`](../reference/motor-control.md#combine-runraw) | (int)motorID1 (int)motorID2 (int)speed | 20ビットの範囲を超える速度は、ドライバによって20ビットに制限されます。 |
<!-- generated:end osc-related speed_profile, motion -->

<!-- osc-settings: speedProfile -->
<!-- generated:begin osc-settings speedProfile -->
**関連する設定項目**

| キー | 名称 | コマンド |
| --- | --- | --- |
| [`speedProfile.acc`](../connections/configuration-items.md#speedprofile-acc) | Acceleration | `/setAcc`, `/setSpeedProfile` |
| [`speedProfile.dec`](../connections/configuration-items.md#speedprofile-dec) | Deceleration | `/setDec`, `/setSpeedProfile` |
| [`speedProfile.maxSpeed`](../connections/configuration-items.md#speedprofile-maxspeed) | Max speed | `/setMaxSpeed`, `/setSpeedProfile` |
| [`speedProfile.fullStepSpeed`](../connections/configuration-items.md#speedprofile-fullstepspeed) | Transit to fullstep threshold speed | `/setFullstepSpeed` |
| [`speedProfile.minSpeed`](../connections/configuration-items.md#speedprofile-minspeed) | Minimum speed | `/setMinSpeed` |
<!-- generated:end osc-settings speedProfile -->
