---
title: サーボモード
---

# サーボモード

サーボモードでは、リアルタイムに変わる目標位置にモータを追従させられます。このページでは、サーボモードとは何か、開始の方法と目標位置の与え方、PIDゲインの調整方法を説明します。

## サーボモードとは {#what}

サーボモードは、モータドライバICの機能ではありません。ドライバの位置決め運転では、運転の前に目標位置を決めておく必要があり、運転が完了するまで新しい目標位置は受け付けられません。サーボモードでは、*モータが動いている間に*新しい目標位置を指定できます。ラジコンのサーボモータのような動作方法です。このモードで動いている間は、ほかのモータ動作コマンドは送れません。`InServoMode`で拒否されます。

![サーボモードの制御](https://python-step-series.readthedocs.io/en/documentation/_images/pid-control.jpg)

ファームウェアは、5msごとにモータの速度を更新します。更新のたびに、現在位置と目標位置を比べ、次に説明するPID制御で速度を計算して、一定速運転のコマンドとしてドライバに送ります（v2.1.0までは、更新の周期は10msでした）。積分と微分の項は周期で換算してあり、同じゲインでほぼ同じ動きになるように作ってあります。それでも動きが少し違うことがあるため、必要ならゲインを調整し直してください。

## サーボモードの開始 {#starting}

### 開始と終了 {#toggling}

[`/enableServoMode`](../reference/servo-mode_reference.md#enableservomode)で、サーボモードを開始・終了します。開始するとき、ボードはモータを即停止し、現在位置を目標位置にして、PID制御の積分と前回の誤差を消します。電磁ブレーキのモータでは、`/enableServoMode 1`は動作コマンドです。ブレーキが保持状態のときは`BrakeEngaged`を返し、開始しません（[動作開始条件](../reference/index.md#motion-start-condition)をご覧ください）。

終了するときは、ボードはモータを減速停止し、励磁したままにします。電磁ブレーキのモータでは、`/enableServoMode 0`の動作はブレーキの状態によって異なります。[電磁ブレーキ](electromagnetic-brake.md#commands)をご覧ください。

**通知が無効になります。** サーボモードを開始すると、[`/busy`](../reference/automatically-sent-messages.md#busy)、[`/motorStatus`](../reference/automatically-sent-messages.md#motorstatus)、[`/dir`](../reference/automatically-sent-messages.md#dir)の通知が無効になります（[`/enableBusyReport`](../reference/motor-driver-settings.md#enablebusyreport)、[`/enableMotorStatusReport`](../reference/motor-driver-settings.md#enablemotorstatusreport)、[`/enableDirReport`](../reference/motor-driver-settings.md#enabledirreport)で設定する通知です）。サーボモードを終了しても、有効には戻りません。必要なときは、有効にし直してください。

### 目標位置の更新 {#target}

[`/setTargetPosition`](../reference/servo-mode_reference.md#settargetposition)で、目標位置を更新します。ファームウェアは新しい目標位置を受け取ると、現在位置と比べて、モータの回転速度を変更します。[`/setTargetPositionList`](../reference/servo-mode_reference.md#settargetpositionlist)で、全モータの目標位置をまとめて送れます。

### サーボモードが解除される場合と、使えない場合 {#limits}

- サーボモード中は、[`/goUntil`](../reference/homing.md#gountil)、[`/goUntilRaw`](../reference/motor-control.md#gountilraw)、[`/releaseSw`](../reference/homing.md#releasesw)は、ほかの動作コマンドや[`/homing`](../reference/homing.md#homing)と同様に、`InServoMode`を返して何もしません。
- **サーボモード中は、[`/setPosition`](../reference/position-management.md#setposition)と[`/resetPos`](../reference/position-management.md#resetpos)を使わないでください。** ボードはこれを防ぐ処理をしていません。
- ドライバが自分でモータを無励磁にしたとき（過電流、過熱、電源電圧の低下）、サーボモードは解除され、`ServoModeCancelledOnHiZ`が送られます。モータを無励磁にするコマンドは、先にサーボモードを解除します。再開するには、もう一度`/enableServoMode 1`を送ります。現在位置が目標位置になります。[アラームと保護](alarms-and-protection.md#hiz-by-itself)をご覧ください。
- STEP400では、HOMEスイッチとLIMITスイッチを別々に判定します。衝突防止の設定か、スイッチの即停止モードにしているとき、HOMEスイッチがオンなら`homingDirection`の向きの動作を、LIMITスイッチがオンなら逆向きの動作を止めます（[原点復帰と位置管理](homing-and-position.md#collision-prevention)をご覧ください）。

## 制御パラメータの種類 {#parameters}

モータの回転速度は、PID制御という手法で算出します。[`/setServoParam`](../reference/servo-mode_reference.md#setservoparam)で、3つのゲインを設定します。

### 比例ゲイン（kP） {#kp}

PID制御は、現在位置と目標位置の差（偏差）を使います。偏差が大きいときは速く、小さいときは遅く回転させて、目標位置に近づけます。比例ゲインは、偏差を回転速度にどの程度反映させるかを決めます。値が小さすぎると目標位置に近づくのに時間がかかり、大きすぎると目標位置を通り過ぎるオーバーシュートが発生します。

### 積分ゲイン（kI） {#ki}

比例制御だけだと、目標位置に近づくにつれて回転が遅くなり、最後のわずかな偏差を解消するのに非常に時間がかかります。偏差を時間で積分して制御量に加えると、この偏差を解消できます。積分ゲインを大きくすると、偏差を素早く解消できますが、オーバーシュートしたり、それを解消する動作によって振動が続いたりすることがあります。

### 微分ゲイン（kD） {#kd}

オーバーシュートや振動が発生しているときに、偏差の急な変化を打ち消すように働くゲインです。振動を減衰させるダンパーのように作用します。

## 制御パラメータの決定方法 {#tuning}

### 全体の流れ {#steps}

PID制御のゲインは、モータが実際に使える加速度、減速度、最大速度（スピードプロファイル）によって変わります。次の順に決めてください。

1. モータの定格や負荷に合ったKVAL（電流モードではTVAL）を決めます。[電圧モードと電流モード](voltage-and-current-mode.md)をご覧ください。
2. モータが使える加速度、減速度、最大速度を決めます。[スピードプロファイルと動作](speed-profile-and-motions.md)をご覧ください。
3. PIDゲインを調整します。

### ゲインの決め方 {#deciding}

最適なゲインの決め方には、さまざまな方法があります。目標位置の更新頻度や、動きの目的によっても変わります。実際の機材で、次の順に試行錯誤することをお勧めします。

#### 1. kP {#tune-kp}

kP、kI、kDをすべて0.0にして、モータが目標位置の周りで振動し始めるまで、kPを少しずつ上げます。目標位置が時々しか変わらないときは、kPだけを設定し、kIとkDは0.0のままにすることが多いです。

#### 2. kI {#tune-ki}

目標位置が数秒に1回しか変わらないときは、kIを上げると、動きが俊敏になります。ただし、60fpsで目標位置を送るようなときは、目標位置が更新されるたびの加速で振動が発生し、滑らかさが損なわれることがあります。目標位置に素早く到達することと、全体が滑らかに動くことのどちらを重視するかで、値は変わります。

#### 3. kD {#tune-kd}

目標位置に近づくときにオーバーシュートや振動が見られる場合は、kDを少しずつ上げます。

## 関連するコマンドと設定項目 {#related}

<!-- osc-related: servo -->
<!-- generated:begin osc-related servo -->
**関連するコマンド**

| コマンド | 引数 | 説明 |
| --- | --- | --- |
| [`/enableServoMode`](../reference/servo-mode_reference.md#enableservomode) | (int)motorID (bool)enable | サーボモード（位置追従モード）をオンオフします。急に動き出すことを避けるため、有効になった瞬間の現在位置が目標位置にセットされます。 |
| [`/setServoParam`](../reference/servo-mode_reference.md#setservoparam) | (int)motorID (float)kP (float)kI (float)kD | PID制御のゲインを調整します。 |
| [`/getServoParam`](../reference/servo-mode_reference.md#getservoparam) | (int)motorID | サーボモードのPIDゲイン（kP、kI、kD）を取得します。 |
| [`/setTargetPosition`](../reference/servo-mode_reference.md#settargetposition) | (int)motorID (int)position | サーボモードの目標位置を設定します。 |
| [`/setTargetPositionList`](../reference/servo-mode_reference.md#settargetpositionlist) | (int)position1 ... (int)positionN | サーボモードの目標位置を全軸分まとめて設定します。引数として各軸の目標位置を指定しますので、STEP400の場合は4個、STEP800の場合は8個の引数が必要です。 |
<!-- generated:end osc-related servo -->

<!-- osc-settings: servoMode -->
<!-- generated:begin osc-settings servoMode -->
**関連する設定項目**

| キー | 名称 | コマンド |
| --- | --- | --- |
| [`servoMode.kP`](../connections/configuration-items.md#servomode-kp) | kP | `/setServoParam` |
| [`servoMode.kI`](../connections/configuration-items.md#servomode-ki) | kI | `/setServoParam` |
| [`servoMode.kD`](../connections/configuration-items.md#servomode-kd) | kD | `/setServoParam` |
<!-- generated:end osc-settings servoMode -->
