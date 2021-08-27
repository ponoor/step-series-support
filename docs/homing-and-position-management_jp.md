## ステッピングモータと原点復帰
システムの電源投入時は、モータが現在どの位置で止まっているかが不明の状態です。前回電源を切った時のタイミング次第でいろんな方向に向いている可能性があります。

またステッピングモータは限界を超える外力がかかるとステップがずれてしまいます（脱調）。そうなると、プログラム上の位置と物理的な位置がずれたまま動き続けてしまいます。

そのため、位置や向きがある使い方の場合は、起動時に、あるいは定期的にセンサを使って基準位置を検出する必要があります。この動作は原点復帰と呼ばれます。

## センサとスイッチ
![Two configuration of homing sensor](http://ponoor.com/manage/wp-content/uploads/2020/10/two-homing-sensors.png)

原点センサにはフォトインタラプタがよく使われています。左はスライダに取り付けられた白い樹脂がフォトインタラプタの発光部と受光部を遮るようになっています。右は回転テーブルの例で、フォトインタラプタが黒いねじに反応するようになっています。
ほかにもマイクロスイッチや光電センサなどが使われます。

## HOMEセンサとLIMITセンサ
STEP400/800は各軸に対してHOME端子があり、センサやスイッチを接続できるようになっています。また端子にはセンサ用の5V電源も供給されています。
STEP400ではHOME端子に加えてLIMIT端子も準備されています。

### HOME
モータドライバチップに直接接続されていて、ドライバの原点復帰機能と組み合わせて使うことができます。通常はこのコネクタを原点センサ用に使います。

### LIMIT (STEP400のみ)
使用方法によってはセンサが2つ必要なこともあります。例えばスライダなどは動作範囲が限定されているため、動作中に脱調するとどちらかの端に衝突してしまう可能性があります。このような場合に両端にセンサを設置しておくと衝突を防ぐことができます。

これらの端子が反応するとモータを強制的に停止する設定が可能ですが、逆にモータ動作と切り離して単純なスイッチ入力として使うこともできます。例えば押しボタンを接続しておいて、押されたらOSCメッセージで通知する、という使い方もできます。

### 衝突防止設定
HOMEやLIMITセンサが反応しているときに、モータが回転できる方向を制限することができます。
[`/setProhibitMotionOnHomeSw`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#setprohibitmotiononhomesw_intmotorid_boolenable)コマンドと[`/setProhibitMotionOnLimitSw`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#setprohibitmotiononlimitsw_intmotorid_boolenable)コマンドによって、それぞれHOMEセンサが反応している場合は`homingDirection`方向へ、LIMITセンサが反応している場合には`homingDirection`と逆方向へのモータ動作が禁止できます。これによって、誤ったコマンドによるメカの衝突が回避できます。

`homingDirection`は[`/setHomingDirection`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#sethomingdirection_intmotorid_booldirection)またはconfigToolで設定できます。これは下記の`/homing`コマンドでも使用されます。

![Homing Direction](https://ponoor.com/cms/wp-content/uploads/2020/08/homingDirection-800x533.jpg)

## 原点復帰コマンド
本デバイスで原点復帰を行うコマンドは[`/homing`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#homing_intmotorid)です。このコマンドの動作を分解すると、モータドライバチップから継承した`/goUntil`と`/releaseSw`のふたつのコマンドから成り立っています。まずはこれらのコマンドの動きを見てみます。

### `/goUnitl`
まずはこのコマンドで原点センサに向かって移動していきます。（そのように設定している場合は）原点センサが反応するとモータが減速停止します。
-> [`/goUntil`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed)

### `/releaseSw`
モータが停止した位置が原点です！ただ厳密には、`/goUnitl`コマンドでは瞬間に停止するのではなく、減速して停止したため、センサが反応した瞬間からずれて停止します。このコマンドは現在位置からゆっくりと逆方向へ移動し、センサが反応しなくなったところで即時停止します。
-> [`/releaseSw`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#releasesw_intmotorid_boolact_booldir)

どちらのコマンドもセンサが反応した時点で現在位置の座標をゼロにリセットする設定にできます。-> [`/setHomeSwMode`](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#sethomeswmode_intmotorid_boolsw_mode)

これらのコマンドと動作の実例はこちらの映像をご覧ください。 
<div class="embed-video">
<iframe width="560" height="315" src="https://www.youtube.com/embed/AydxbL6-a_g" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

### `/homing`
上記2つのコマンドをOSC経由で順次動かすこともできますが、このシーケンスを一つのコマンドで実行するのが[`/homing`](https://ponoor.com/docs/step-series/osc-command-reference/homing/#homing_intmotorid)です。configToolやOSCコマンドにてあらかじめ設定しておいた原点復帰方向や原点復帰スピードに従って、自動で原点復帰シーケンスが完了します。

### タイムアウト
`/goUntil` `/releaseSw`それぞれにタイムアウト時間が設定可能で、この時間内にセンサ状態に変化がなかった場合はタイムアウトとして動作を中止します。これは何らかの理由でセンサが反応しなくなった場合に、延々とメカが行き止まりに押し当てられているような状況を防ぐために、ある時点で原点復帰動作をあきらめて停止するものです。


## 常時開と常時閉
### 電気的接続
「センサが反応する」をもう少し厳密に考えてみます。
HOMEとLIMITの各コネクタのピン配置は以下の通りです。

| ピン番号 | 機能 |
| ---- | ---- |
| 1 | GND |
| 2 | スイッチ/センサ入力 |
| 3 | 5V電源出力 | 

HOMEとLIMITの各センサピンは3.3Vでプルアップされています。スイッチをつなぐ場合は1番のGNDと2番のセンサ端子を接続します。スイッチが押されるとGNDピンとつながって、3.3Vから0Vへ電圧が落下します。このHIGHレベルからLOWレベルへの電圧の変化時 (**Falling Edge**) に、センサが反応したという判定が発生します。

センサの場合は、[EE-SX671A](http://www.ia.omron.com/product/item/2219/)を例にとると次のような接続になります。

![EE-SX671A Diagram](http://ponoor.com/manage/wp-content/uploads/2020/10/ee-sx67.jpeg)

| ピン番号 | 機能 | センサピン |
| ---- | ---- | ---- |
| 1 | GND | - |
| 2 | SW/センサ入力 | OUT |
| 3 | 5V出力 | + |

## センサの反応時に入光するのか遮光するのか
ここはセンサを買いに行く前によく考えておかなければならない部分です。
![Dark on or Light on](http://ponoor.com/manage/wp-content/uploads/2020/10/sensor_dark_light.png)

左の場合は、原点位置でセンサに入光するようになっていますが、右の場合は原点位置でセンサが遮光されるようになっています。

センサにも、入光時にONになるタイプと遮光時にONになるタイプがあります。また切替式のセンサもあって、上記のオムロン製センサの場合はLという端子と+端子をショートすると動作が切り替わります。

原点位置でセンサピンがHIGH→LOWになるように機構とセンサを組み合わせなければなりません。

## 回転テーブルの場合

例えば上の写真の左の回転テーブルで考えた場合、時計回りの場合と反時計回りの場合で原点センサの反応位置が穴のサイズ分ずれてしまいます。本デバイスでは原点センサのHIGH→LOWとLOW→HIGHの変化どちらともOSCメッセージで通知させることができます。このメッセージには回転方向も含まれていますので、回転方向によって場合分けすれば原点位置をそろえることができます。
-> [`/enableHomeSwReport`](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#enablehomeswreport_intmotorid_boolenable)
