## 電磁ブレーキモード
電磁ブレーキを使用する場合は、まずSTEP400を電磁ブレーキモードにする必要があります。OSCから [`/enableElectromagnetBrake`](https://ponoor.com/docs/step400/osc-command-reference/brake/#enableelectromagnetbrake_intmotorid_boolenable)コマンドで設定できるほか、configToolの`Electromagnetic brake enable`からも設定できます。

このモードがオンになっていると、モータの励磁に合わせて電磁ブレーキが自動的に制御されます。

## 励磁と無励磁の切替
[`/activate`](https://ponoor.com/docs/step400/osc-command-reference/brake/#activate_intmotorid_boolstate)コマンドによって、モータの励磁と無励磁を切り替えます。モータ励磁時にはブレーキ開放、モータ無励磁のときにはブレーキが保持状態になります。

ブレーキとモータの保持力が重なるbrakeTransitionDurationは[`/setBrakeTransitionDuration`](https://ponoor.com/docs/step400/osc-command-reference/brake/#setbraketransitionduration_intmotorid_intduration)で設定できるほか、configToolの`Brake transition duration`からも設定できます。

## 軸の解放
電磁ブレーキを開放したままモータを無励磁にすると負荷が落下しますが、メンテナンスなどの理由により軸を開放する必要があるときは[`/free`](https://ponoor.com/docs/step400/osc-command-reference/brake/#free_intmotorid_boolstate)コマンドを使用します。

負荷が吊り下げられたままの状態では危険ですのでこのコマンドは十分注意して送ってください。

## 各コマンドの挙動
電磁ブレーキが保持状態のときは、
- [`/run`](https://ponoor.com/docs/step400/osc-command-reference/motor-control/#run_intmotorid_floatspeed)
- [`/goTo`](https://ponoor.com/docs/step400/osc-command-reference/motor-control/#goto_intmotorid_intposition)
- [`/move`](https://ponoor.com/docs/step400/osc-command-reference/motor-control/#move_intmotorid_intstep)

といったモーションコマンドを送っても実行されず、[`ERROR_BRAKE_ENGAGED`](https://ponoor.com/docs/step400/osc-command-reference/automatically-sent-messages-from-step-400/#errorcommand)を返します。

またモータを無励磁にする以下のコマンドは、次のような挙動になります。
- [`/softHiZ`](https://ponoor.com/docs/step400/osc-command-reference/motor-control/#softhiz_intmotorid): モータを減速停止し、停止したら電磁ブレーキを保持状態にしたのち、モータをHiZ状態にする
- [`/hardHiz`](https://ponoor.com/docs/step400/osc-command-reference/motor-control/#hardhiz_intmotorid): モータを瞬間停止し、電磁ブレーキを保持状態にしたのち、モータをHiZ状態にする

[`/softStop`](https://ponoor.com/docs/step400/osc-command-reference/motor-control/#softstop_intmotorid) [`/hardStop`](https://ponoor.com/docs/step400/osc-command-reference/motor-control/#hardstop_intmotorid)は停止後もモータは励磁したままですので、電磁ブレーキモードでも通常時と同じ挙動です。


