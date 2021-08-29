## サーボモードとは
モータドライバICの機能として備わっている位置決め運転では、事前に目標位置を定めておく必要があり、また運転が完了するまでは新しい目標位置を設定することはできないため、リアルタイムに目標位置が変化するような動作はできません。
サーボモードでは、Arduinoスケッチでの処理によって、目標位置へリアルタイムに追従する動作を可能にします。ラジコンのサーボモータのような動作方法です。このモードで動いている間は、ほかのモータ動作コマンドを送ることはできません。


<div class="embed-video">
<iframe width="560" height="315" src="https://www.youtube.com/embed/1dd_bBqWpMQ" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

*サーボモードの動作例*

## サーボモードの起動手順
### 動作開始と終了
[`/enableServoMode`](https://ponoor.com/docs/step-series/osc-command-reference/servo-mode/#enableservomode_intmotorid_boolenable) メッセージによってサーボモードを開始・終了します。サーボモードの開始時は、BUSY解除状態である必要があります。
### 目標位置の更新
[`/setTargetPosition`](https://ponoor.com/docs/step-series/osc-command-reference/servo-mode/#settargetposition_intmotorid_intposition)メッセージによって目標位置を更新します。Arduinoスケッチでは新しい目標位置を受け取ると、現在位置と比較して、モータの回転速度を更新します。
全モータ分の目標位置をまとめて送るための[`/setTargetPositionList`](https://ponoor.com/docs/step-series/osc-command-reference/servo-mode/#settargetpositionlist_intposition1_intposition2_intposition3_intposition4)メッセージもあります。

## 制御パラメータの種類
モータの回転速度は、PID制御という手法によって算出しています。[`/setServoParam`](https://ponoor.com/docs/step-series/osc-command-reference/servo-mode/#setservoparam_intmotorid_floatkp_floatki_floatkd)コマンドによって制御パラメータを調整できます。パラメータは以下の3つです。

### 比例ゲイン(kP)
PID制御は目標位置と現在位置の差（偏差）を使って制御します。すなわち、偏差が大きい場合は速く、差が小さい場合は遅く回転させて目標位置に近づけています。比例ゲインは偏差をどの程度回転速度に反映させるかを決定します。値が小さすぎると目標位置に近づくのに時間がかかり、大きすぎると目標位置を通り過ぎるオーバーシュートが発生します。

### 積分ゲイン(kI)
比例制御だけだと、目標位置に近づくにつれ回転が遅くなっていき、最後のわずかな偏差を解消するのに非常に時間がかかってしまいます。そこで偏差を時間積分して制御量に加えることによって、最後に長く残ってしまう偏差を解消できます。積分ゲインを大きくするとより素早く偏差を解消できますが、オーバーシュートしたり、さらにそれを解消するための動作が発生して振動が続く状態になってしまうことがあります。

### 微分ゲイン(kD)
オーバーシュートや振動が発生している場合などに、偏差の急な変化を打ち消す用に作用するパラメータです。

## 制御パラメータの決定方法
### 全体の流れ
PID制御のパラメータは、動作可能な加減速度、回転速さの最大値（スピードプロファイル）によって変化します。従って、制御パラメータを決めるには以下の手順になります。

1. モータの定格や負荷に合わせたKVAL（電流モードの場合はTVAL）を決める
2. 動作可能な加減速度、回転速さの最大値（スピードプロファイル）を決める
3. PID制御ゲインを決める

### PID制御ゲインの決定
最適なPID制御ゲインの決定方法は様々な手段が提案されているようですが、目標位置の更新頻度や動きの目的にもよって変化しますので、弊社では以下のような手順で実際に動かしてみながらトライ＆エラーで決めています。

#### 1. kP
kP, kI, kDすべてを0.0にして、kPを徐々に上げていきます。目標位置が随時変化する場合は、kI, kDは0.0のままで、kPを設定するだけにすることも多いです。

#### 2. kI
目標位置が数秒に1回しか変化しないような場合は、kIの値を上げていくと、動きを俊敏にできます。ただし、例えば60fpsで目標位置を送っているような場合は、目標位置更新の度に動き出しの加速の振動が発生し、動きの滑らかさが損なわれることがあります。目標位置に素早く到達することが重要なのか、全体で滑らかな動きを実現することが重要なのか、によって設定するべき値は変化します。

#### 3. kD
目標位置に近づく際に少しオーバーシュートや振動が出ている場合は、kDを上げていきます。




