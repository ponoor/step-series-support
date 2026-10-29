---
title: 電磁ブレーキ
---

# 電磁ブレーキ

電磁ブレーキは、電源が入っていないときにモータの軸をロックします。このページでは、ボードがブレーキとモータをどう連動して制御するか、ブレーキの状態、各コマンドがブレーキに何をするか、負荷を吊るす前に知っておくべきことを説明します。

## 電磁ブレーキとは {#what}

ステッピングモータの中には、電磁ブレーキが取り付けられているものがあります。ステッピングモータは、停止して励磁しているときは、トルクで負荷を支えられます。しかし、電源が落ちるとそのトルクがなくなり、吊り下げた負荷は動いたり落下したりします。電磁ブレーキは、電源が切れたとき（またはコマンドで指示したとき）に軸をロックし、通電したときに軸を解放する装置です。負荷を上下に動かすときには特に必要です。

ボードは、モータごとにブレーキの出力を制御します。対応しているのは、EMB-STEP400を接続したSTEP400と、STEP800本体のブレーキ出力です。配線は[電磁ブレーキの接続](../connections/electromagnetic-brake-wiring.md#overview)を、ブレーキ基板の仕様は[EMB-STEP400](../hardware/emb-step400.md#specifications)をご覧ください。

## ブレーキを有効にする {#enable}

モータのブレーキは、[`/enableElectromagnetBrake`](../reference/brake.md#enableelectromagnetbrake)か、設定の[`driverSettings.electromagnetBrakeEnable`](../connections/configuration-items.md#driversettings-electromagnetbrakeenable)で有効にします。有効にしている間、ボードは、モータが励磁されるとブレーキを解放し、励磁されないとブレーキを保持状態にします。ブレーキを有効にしていないモータは、このページのことの影響を受けません。

設定の変更は、ドライバが無励磁のときだけできます。ブレーキを無効にするときは、ブレーキが保持状態のときか`/free`の後だけできます。そうでなければ、ボードは`CommandIgnored`を返します。

## ブレーキの状態 {#states}

各モータのブレーキは、6つの状態のどれかです。[`/getBrakeStatus`](../reference/brake.md#getbrakestatus)で番号を取得できます。番号は仕様で、新しい状態は6、7、...として追加されるだけです。ブレーキを無効にしているモータの状態は-1です。

| 状態 | 名前 | ブレーキ出力 | ドライバ | 意味 |
| --- | --- | --- | --- | --- |
| 0 | Engaged | 保持 | 無励磁 | ブレーキが軸を保持しています。モータは励磁されていません。 |
| 1 | Releasing | 保持 | 励磁 | `/activate 1`を受け取りました。移行時間を待ってから、ブレーキを解放します。 |
| 2 | Released | 解放 | 励磁 | モータが励磁され、軸は自由です。動作コマンドを受け付けます。 |
| 3 | Stopping | 解放 | 励磁 | `/softHiZ`か`/activate 0`でモータを減速しています。停止したらブレーキを保持状態にします。 |
| 4 | Engaging | 保持 | 励磁 | ブレーキは保持状態で、モータはまだ励磁されています。移行時間の後、ドライバが無励磁になります。 |
| 5 | Free | 解放 | 無励磁 | `/free`を受け取りました。ブレーキは解放され、モータは励磁されていません。 |

### 状態の変わり方 {#transitions}

コマンドによる変化（次の項）のほかに、ボードが自分で状態を変えます。ボードは5msごとにドライバの状態を読み、その時点で判断します。

| 変化の前 | 条件 | 変化の後 |
| --- | --- | --- |
| Releasing | ドライバが励磁されていて、移行時間が経過した | Released（ブレーキ出力を解放） |
| Releasing | ドライバが無励磁のまま（例えばモータに電源がない） | Engaged。`/error/command BrakeReleaseFailed`を送る |
| Stopping | モータが停止した | Engaging |
| Engaging | 移行時間が経過した、またはドライバが無励磁になっていた | Engaged（前者ではドライバを無励磁にする） |
| Released、Stopping | ドライバが自分で無励磁になった（過電流、過熱、電源電圧の低下） | すぐにEngaged。`/error/command BrakeEngagedOnHiZ`を送る。保留中の動作は取り消される |

状態は5msごとに読むため、コマンドの後、最大5ms遅れて変化します。

## コマンドとブレーキ {#commands}

ブレーキを有効にしているモータに対して、各コマンドが何をするかを示します。「何もしない」は、コマンドが実行されず、エラーも送られないことです。

| コマンド | Engaged（0） | Releasing（1） | Released（2） | Stopping（3） | Engaging（4） | Free（5） |
| --- | --- | --- | --- | --- | --- | --- |
| `/activate 1` | ドライバを励磁し、Releasing | 何もしない | 何もしない | 保持の予定を取り消し、Released。減速は続く | Releasingに戻る（待ち時間は最初から） | ドライバを励磁し、Released |
| `/activate 0`、`/softHiZ` | 何もしない | Engaging | モータを減速し、Stopping | 何もしない | 何もしない | Engaged |
| `/hardHiZ` | 何もしない | Engaging | モータを即停止し、Engaging | モータを即停止し、Engaging | 何もしない | Engaged |
| `/free` | ブレーキを解放したまま無励磁にし、Free | 同左 | 同左 | 同左 | 同左 | 何もしない |
| 動作コマンド（`/run`、`/move`、`/goTo`など、`/homing`、`/enableServoMode 1`） | `BrakeEngaged` | `BrakeEngaged` | 実行する | 実行する。Released（保持の予定を取り消す） | `BrakeEngaged` | 実行する。モータが励磁され、Released |
| `/softStop`、`/hardStop`、`/enableServoMode 0` | 何もしない | 実行する | 実行する | 実行する。Released（保持の予定を取り消す） | 実行する | 何もしない |
| `/resetMotorDriver` | 実行する | `CommandIgnored` | `CommandIgnored` | `CommandIgnored` | `CommandIgnored` | 実行する |

ブレーキが保持状態のときの動作コマンドは、`BrakeEngaged`で拒否されます。これは[動作開始条件](../reference/index.md#motion-start-condition)の1つです。

全モータ（255）に送るコマンドや、連動コマンド（`/combine/...`）も、モータごとにこのとおりに作用します。

### ブレーキを保持状態にする途中での停止 {#stopping}

`/softHiZ`や`/activate 0`で減速している間（Stopping）は、**最後に受け取ったコマンドが優先されます**。

- `/softStop`、`/hardStop`、`/enableServoMode 0`は、ブレーキを保持状態にする予定を取り消します。状態はReleasedに戻り、モータは停止して励磁されたままになります。これらのコマンドは「止めて保持する」という意味なので、先の「止めてブレーキを保持状態にする」を上書きします。そのあとブレーキを保持状態にしたいときは、`/softHiZ`、`/activate 0`、`/hardHiZ`をもう一度送ってください。
- `/hardHiZ`は予定を取り消しません。モータをすぐに止めて、ブレーキを保持状態にします。
- `/softHiZ`と`/activate 0`は何もしません。減速と予定はそのまま続きます。
- 動作コマンドと`/activate 1`も予定を取り消します。ブレーキは解放されたままです。

ブレーキを有効にしていないモータでも同じです。`/softHiZ`の減速中に`/softStop`を送ると、モータは励磁されたまま停止します。

## 移行時間 {#transition-duration}

ブレーキが機械的に動作するには少し時間がかかるため、その間は、モータとブレーキの両方で軸を保持しておく必要があります。**移行時間**（[`/setBrakeTransitionDuration`](../reference/brake.md#setbraketransitionduration)、[`driverSettings.brakeTransitionDuration`](../connections/configuration-items.md#driversettings-braketransitionduration)）は、この重なりの時間です。

- 解放するとき: ボードはモータを励磁し、移行時間を待ってから、ブレーキを解放します。
- 保持状態にするとき: ボードはブレーキを保持状態にし、移行時間を待ってから、モータを無励磁にします。

[![ブレーキの移行時間](https://ponoor.com/cms/wp-content/uploads/2021/03/brakeTransition.png)](https://ponoor.com/cms/wp-content/uploads/2021/03/brakeTransition.png)

移行時間は、ブレーキがロックするまでの時間には影響しません。ブレーキの後に、モータを無励磁にしたり、ブレーキを解放したりするまでの待ち時間に影響します。待ち時間は5ms単位で数えるため、実際の時間は、設定値より0〜5ms長くなります。

推奨値は示しません。使うブレーキの応答時間、負荷、装置によって決まるためです。使うブレーキの仕様にある吸引・釈放時間に、余裕を足した値にしてください。初期値と範囲は[`/setBrakeTransitionDuration`](../reference/brake.md#setbraketransitionduration)をご覧ください。

## 保持の電流 {#hold-current}

ブレーキを有効にしているモータが再び励磁されるとき（`/activate 1`と、`/free`の後の動作コマンド）、KVAL_HOLD（電流モードではTVAL_HOLD）は、KVAL_RUN（TVAL_RUN）の半分以上に引き上げられます。ブレーキを解放している間、モータが負荷を支えるためです。[`/getKval`](../reference/voltage-and-current-mode-settings.md#getkval)は引き上げられた値を返します。[電圧モードと電流モード](voltage-and-current-mode.md#kval-tval)をご覧ください。

## 再起動、ウォッチドッグ、CPU動作異常 {#restart}

ボードは、どんな理由でも、再起動の前にブレーキを保持状態にします。

- **[`/resetDevice`](../reference/system-settings.md#resetdevice)とUSBシリアルの`R`コマンド**: 回転しているモータを即停止し、ブレーキを保持状態にして、それらの移行時間の最大値（最大1s）を待ってから再起動します。
- **ウォッチドッグ**: 処理が約250ms止まると、すべてのブレーキを保持状態にし、移行時間の最大値（最大1s）を待ってから、ウォッチドッグがボードを再起動します。ドライバには何も送りません。回転中のモータは、そのままブレーキで止まります。`/booted`はリセットの原因を4として通知します。
- **CPU動作異常**（CPUの例外）: すべてのブレーキをすぐに保持状態にし、同じように待ってから再起動します。`/booted`はリセットの原因を6として通知します。

リセットの原因は、[`/booted`](../reference/automatically-sent-messages.md#booted)の2番目の引数です。番号は[`/booted`](../reference/automatically-sent-messages.md#booted)をご覧ください。

EthernetをつないだままUSBを抜くと、STEP400（R1基板）は再起動することがあります（ハードウェアの問題です）。先にブレーキは保持状態になりますが、抜くのはモータを止めているときにしてください。

## 負荷を支えられない時間 {#unsupported}

ファームウェアでは防げない、負荷を支えられない時間があります。

- **STEP800の電源投入**: 電源を入れてから約250msの間、すべてのブレーキが解放されたままになります。ほとんどはブートローダの時間です。**電源や条件によっては長くなり、24Vでは約2s解放されたままだった実測があります。** ファームウェアではなく、ハードウェアによるものです。
- **リセットボタンと電源電圧の低下**: ドライバはスタンバイになり、（STEP800の）ブレーキは、ファームウェアが起動するまでの約0.5s、解放されたままになります。
- EMB-STEP400を接続したSTEP400では、リセットのときもブレーキはすぐに保持状態になります（ブレーキ基板が引き下げます）。
- 電気的にはブレーキが先に保持状態になっても、軸が保持されるのは、ブレーキが機械的にロックしてからです。数十msかかります。

負荷を吊るすときは、これらの時間を考慮してください。

## 使い方の注意 {#usage}

- **ブレーキの電源は、モータと同じ電源から取るか、モータの電源と一緒に切れる電源にしてください。** モータの電源だけが先に切れる状態は避けてください。モータの電源だけが切れると、電源電圧の低下（UVLO）が働く前に保持力が抜けて、負荷が落下します。モータとブレーキの電圧が違う構成（例: 48Vのモータと24Vのブレーキ）でも、ブレーキの電源がモータの電源に連動して切れるようにします。
- **再起動のあとと、モータが無励磁になったあとは、原点復帰をやり直してください。** 位置が信頼できなくなっています。モータが再び励磁されたあとの最初のブレーキの解放で、軸がずれることがあります。[原点復帰と位置管理](homing-and-position.md)をご覧ください。
- **`/free`はメンテナンス用です。** ブレーキを解放したままモータを無励磁にするため、モータに負荷が吊り下げられていると、負荷が落下します。このコマンドは十分に注意して送ってください。送る前に、負荷を安全な状態にしてください。
- モータが回るのは、ブレーキが解放されているときだけです。上の動作開始条件をご覧ください。
- ドライバが自分で無励磁になったときは、ボードがブレーキを保持状態にします（`BrakeEngagedOnHiZ`）。[アラームと保護](alarms-and-protection.md#hiz-by-itself)をご覧ください。

## 電磁ブレーキのついたステッピングモータの例 {#examples}

[![ブレーキ付きステッピングモータ](https://ponoor.com/cms/wp-content/uploads/2021/03/nema-23-stepper-19nm269ozin-w-brake-friction-torque-20nm283ozin-52372-1000x1000-1.jpg)](https://ponoor.com/cms/wp-content/uploads/2021/03/nema-23-stepper-19nm269ozin-w-brake-friction-torque-20nm283ozin-52372-1000x1000-1.jpg)

[STEPPER ONLINE](https://www.omc-stepperonline.com/stepper-motor-brake/nema-23-stepper-19nm269ozin-w-brake-friction-torque-20nm283ozin-23hs30-2804d-b200.html)

[![PKP243D23M2](https://ponoor.com/cms/wp-content/uploads/2021/03/pkp243d-700x525.jpg)](https://ponoor.com/cms/wp-content/uploads/2021/03/pkp243d.jpg)

[Oriental Motor](https://www.orientalmotor.co.jp/) PKP243D23M2

## 関連するコマンドと設定項目 {#related}

<!-- osc-related: brake -->
<!-- generated:begin osc-related brake -->
**関連するコマンド**

| コマンド | 引数 | 説明 |
| --- | --- | --- |
| [`/enableElectromagnetBrake`](../reference/brake.md#enableelectromagnetbrake) | (int)motorID (bool)enable | 電磁ブレーキモードを有効・無効にします。 |
| [`/activate`](../reference/brake.md#activate) | (int)motorID (bool)state | 電磁ブレーキモードの場合に、モータの励磁、励磁解除を切り替えます。電磁ブレーキも連動して動作します。このコマンドでモータが励磁状態になっていないと、モータを回転させるコマンドを送ることはできません。 |
| [`/free`](../reference/brake.md#free) | (int)motorID | 電磁ブレーキモードの場合に、モータ軸を自由に回せる状態にします。モータの励磁を解除し、電磁ブレーキも解放のままになります。 |
| [`/setBrakeTransitionDuration`](../reference/brake.md#setbraketransitionduration) | (int)motorID (int)duration | 電磁ブレーキの保持・解放時に、モータを励磁したままにしておく移行時間を指定します。これは物理的にブレーキ機構が動作する時間がかかるため、ブレーキの動作が完了するまでモータ軸を励磁したまま保っておくために必要な時間です。 |
| [`/getBrakeTransitionDuration`](../reference/brake.md#getbraketransitionduration) | (int)motorID | 電磁ブレーキの保持・解放時に、モータを励磁したままにしておく移行時間を取得します。 |
| [`/getBrakeStatus`](../reference/brake.md#getbrakestatus) | (int)motorID | 指定したモータの電磁ブレーキの状態を返します。ブレーキが無効なモータでは-1です。 |
<!-- generated:end osc-related brake -->

<!-- osc-settings: driverSettings.electromagnetBrakeEnable, driverSettings.brakeTransitionDuration -->
<!-- generated:begin osc-settings driverSettings.electromagnetBrakeEnable, driverSettings.brakeTransitionDuration -->
**関連する設定項目**

| キー | 名称 | コマンド |
| --- | --- | --- |
| [`driverSettings.electromagnetBrakeEnable`](../connections/configuration-items.md#driversettings-electromagnetbrakeenable) | Electromagnetic brake enable | `/enableElectromagnetBrake` |
| [`driverSettings.brakeTransitionDuration`](../connections/configuration-items.md#driversettings-braketransitionduration) | Brake transition duration | `/setBrakeTransitionDuration` |
<!-- generated:end osc-settings driverSettings.electromagnetBrakeEnable, driverSettings.brakeTransitionDuration -->
