---
title: クイックスタート
---

# クイックスタート

買ったままのボードで、モータを回すところまでの手順です。ボード1台をPCに直接つなぎ、OSC（Open Sound Control）メッセージでモータを1台回し、モータがなめらかに回るように駆動電圧（KVAL）を調整します。各手順の詳しい説明は、リンク先のページにあります。

## 用意するもの {#what-you-need}

- STEP400またはSTEP800。
- 4線のバイポーラ型ステッピングモータ。このページでは、入手しやすく安価な、MERCURY MOTORの`SM-42BYG011-25`を使います。別のモータを使う場合は、そのモータに合わせて、いくつかの設定を変える必要があるかもしれません。
- 電源。このサイズのモータ1台なら、24V 1AのACアダプタで十分です。
- LANケーブルと、Ethernetポートのあるパソコン（またはUSB-Ethernet変換）。
- OSCメッセージを送るソフトウェア。[OSCを送るソフトウェア](index.md#software)をご覧ください。

microSDカードは使いません。

## 接続 {#connecting}

手順で指示するまで、電源は入れないでください。電源をつないでおいてかまいませんが、オフにしておいてください。

### Ethernet {#ethernet}

LANケーブルでボードとPCを直接つなぎます（一対一の接続）。ネットワークスイッチ経由でもかまいません。

!!! warning "ボードをルーターにつながないでください"
    ルーター、特にDHCPサーバ機能のあるルーターは、スイッチとは動作が異なり、問題が起きる可能性があります。PCと直接つなぐか、本物のネットワークスイッチにつないでください。

### モータ {#motor}

使えるのは、4線のバイポーラ型ステッピングモータだけです。`SM-42BYG011-25`は、たとえば次の店で購入できます（各店とは関係がありません）。

- [Strawberry Linux](http://strawberry-linux.com/catalog/items?code=12026)
- [秋月電子通商](https://akizukidenshi.com/catalog/g/gP-05372/)
- [SparkFun](https://www.sparkfun.com/products/9238)

![](http://ponoor.com/manage/wp-content/uploads/2020/10/09238-01.jpg)

モータの1つのコイルの2本の線を端子の1組に、もう1つのコイルの2本の線をもう1組につなぎます。このモータの[データシート](https://www.sparkfun.com/datasheets/Robotics/SM-42BYG011-25.pdf)の配線図を見ると、コイルのペアは`Red - Green`と`Yellow - Blue`です。

[![](https://ponoor.com/cms/wp-content/uploads/2020/08/motor-wiring-diagram-sample.png)](https://ponoor.com/cms/wp-content/uploads/2020/08/motor-wiring-diagram-sample.png)

端子台へは次のようにつなぎます。

[![](https://ponoor.com/cms/wp-content/uploads/2020/08/SM-42BYG-wiring-700x525.jpg)](https://ponoor.com/cms/wp-content/uploads/2020/08/SM-42BYG-wiring.jpg)

ほかのモータでコイルのペアを見つける方法と端子については、[モータの端子](../connections/power-supply-and-motor.md#motor-terminals)をご覧ください。

### 電源 {#power-supply}

ACアダプタをDCジャックにつなぎます。プラグは、外径5.5mm、内径2.1mmで、センタープラスのものです。電源はオフにしておきます。

![](https://ponoor.com/cms/wp-content/uploads/2020/08/image-1609563897700.png)

このサイズのモータなら、DCジャックからの給電で十分です。より大きなモータで、高電圧や大電流が必要な場合は、ジャックの隣のねじ式端子を使います。**両方に電源をつながないでください。**詳しくは、[電源の端子](../connections/power-supply-and-motor.md#power-terminals)をご覧ください。

## ボードの設定 {#board-settings}

このページでは初期設定を使いますので、microSDカードのスロットは空のままにします。カードがないときは、ボードはファームウェアの初期値で起動します（[起動時](../connections/how-settings-work.md#at-start)）。設定はあとで変更して保存できます。[設定の仕組み](../connections/how-settings-work.md)をご覧ください。

DIPスイッチを1にします。一番左のスイッチだけをON側にスライドさせ、ほかはOFF側にします。DIPスイッチに印刷された数字が読める向きにしたとき、一番左が最も下の桁です。[DIPスイッチの設定](../connections/network-and-dip-switch.md#dip-switch)をご覧ください。

![](https://ponoor.com/cms/wp-content/uploads/2020/10/step400-dipSw.jpg)  
DIPスイッチを1にした状態です（STEP400）。

DIPスイッチが1で、初期設定のとき、ボードのネットワーク設定は次のとおりです。IDは、ボードのIPアドレスと送信ポートに加算されます。

<!-- quickstart-network:begin -->
| 項目 | 設定値 |
| --- | --- |
| ボードのIPアドレス | 10.0.0.101 <!-- qs-network: boardIp --> |
| PCのIPアドレス（ボードの返信先） | 10.0.0.10 <!-- qs-network: pcIp --> |
| サブネットマスク | 255.255.255.0 <!-- qs-network: subnet --> |
| ボードが受信するポート | 50000 <!-- qs-network: boardPort --> |
| PCが受信するポート | 50101 <!-- qs-network: pcPort --> |
<!-- quickstart-network:end -->

これは、IDが1で、ファームウェアの初期値のときの値です。初期値の一覧とIDの加算は、[初期設定](../connections/network-and-dip-switch.md#initial)と[IDの加算](../connections/network-and-dip-switch.md#adding-id)をご覧ください。

ここで電源を入れます。ボードの裏側には、電源電圧や大電流がかかる端子があります。基板を壊したり、けがをしたりしないように、電気を通さない台の上に置くか、基板の穴にスペーサを取り付けてください。

## PCの設定 {#pc-settings}

ボードはPCのIPアドレスにメッセージを送りますので、ボードをつないだEthernetポートに固定のIPアドレスを設定します。PCのIPv4を次のように設定してください。

| 項目 | 設定値 |
| --- | --- |
| IPアドレス | 10.0.0.10 |
| サブネットマスク | 255.255.255.0 |

固定のIPアドレスの設定のしかたは、OSによって異なります。

- [Windows](https://support.microsoft.com/ja-jp/help/15089/windows-change-tcp-ip-settings)
- [Mac](https://support.apple.com/ja-jp/HT202480)
- [Linux](https://www.youtube.com/watch?v=Yr6qI6v1QCY)

## 通信の確認 {#checking}

Macのターミナルや、Windowsのコマンドプロンプトで、`ping 10.0.0.101`を実行します。pingが通れば、接続できています。

ここから先は、使う環境によって実際の操作が異なりますので、送受信するOSCメッセージだけを書きます。メッセージは、ボードのIPアドレスと、ボードが受信するポートに送ります。どちらも上の表にあります。

まず、[`/setDestIp`](../reference/system-settings.md#setdestip)を送って、返信の送り先をボードに教えます。

```
/setDestIp
```

初期設定では、ボードはこのコマンドを受け取るまで、`/booted`以外のOSCメッセージを送りません。コマンドを受け取ると、ボードはPCが受信するポートに、返信の[`/destIp`](../reference/system-settings.md#setdestip)を送ります。

PCを替えたときやネットワークを変えたときは、`/setDestIp`を送り直してください。そのときに、ボードがPCのMACアドレスを調べます。詳しくは、[送信先と`/setDestIp`](../guides/communication-and-messages.md#setdestip)をご覧ください。

`/destIp`が届かないときは、PCのネットワーク設定をもう一度確認してください。Windowsでは、使っているアプリケーションの通信がファイアウォールで許可されているかも確認してください。[返信や位置レポートが届かない](../maintenance/troubleshooting.md#no-reply)もご覧ください。

## モータを回す {#running}

[`/run`](../reference/motor-control.md#run)を送ると、モータが指定の速度で回ります。

```
/run 1 200.
```

最初の引数はモータIDで、モータをつないだコネクタの横に、ボードに印刷されている番号です。255はすべてのモータを表します。[モータID](../reference/index.md#motor-id)をご覧ください。2番目の引数は速度で、単位はstep/sです。マイナスの値を指定すると、逆向きに回ります。1回転が200stepのモータ（`SM-42BYG011-25`など）では、`200.`で1秒に1回転します。速度の範囲は、[`/run`](../reference/motor-control.md#run)のリファレンスにあります。

モータは回りましたか？止めるときは、`/run 1 0`を送るか、[`/softStop`](../reference/motor-control.md#softstop)（減速して止めます）または[`/hardHiZ`](../reference/motor-control.md#hardhiz)で、すべてのモータを止めます。

```
/softStop 255
```

`/hardHiZ`のあとは、モータが無励磁になりますので、位置を保てません。

!!! warning "回転中にモータを外さないでください"
    モータに通電しているときや回転中に、モータを外さないでください。ボードが壊れます。

モータが動かないときは、[モータが動かない](../maintenance/troubleshooting.md#motor-not-moving)をご覧ください。

おそらく、モータはきれいに回らなかったと思います。振動が大きかったり、うるさかったりします。駆動電圧がモータに合っていないためです。次の手順で、KVALを使って調整します。

## KVALの調整 {#kval}

電圧モードでのモータの駆動電圧は、電源電圧に対する割合として、KVALで設定します。KVALが0なら電圧がかからず（モータは回りません）、最大値ならほぼ電源電圧がそのままかかります。低すぎても高すぎても、モータはきれいに回りません。KVALは、停止中、一定速度、加速中、減速中の4つの値に分かれています。[KVALとTVAL](../guides/voltage-and-current-mode.md#kval-tval)をご覧ください。初期値と範囲は、[`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval)のリファレンスにあります。

もう一度、モータを回します。

```
/run 1 200.
```

回しながら、[`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval)で、モータ1の4つの値をまとめて設定します。停止中の値は0にし、ほかの3つは同じ値にして、少しずつ上げていきます。

```
/setKval 1 0 24 24 24
```

引数は、モータID、停止中の値、一定速度の値、加速中の値、減速中の値の順です。電源が24Vのとき、24は電源電圧の約9%です。値を少しずつ上げていくと、どこかで静かに回り始めます。

```
/setKval 1 0 32 32 32
/setKval 1 0 40 40 40
```

KVALを上げるとトルクが上がりますが、モータの発熱が大きくなったり、振動がまた大きくなったりします。負荷に合わせて調整してください。STEP400では、電流を一定にして駆動する方式（電流モード）も使えます。[電流モードの設定](../guides/voltage-and-current-mode.md#current-mode-setting)をご覧ください。

いくつかのモータについては、値を計算して設定ファイルを用意しています。[モータ別のパラメータ例](../connections/example-parameters.md)をご覧ください。

## 次のステップ {#next-steps}

- 調整した設定を、ボードを再起動しても残るように保存する: [`/saveConfig`](../reference/system-settings.md#saveconfig)と[設定の仕組み](../connections/how-settings-work.md)。
- 複数のボードを使う: DIPスイッチでIDを変えます。[IDの加算](../connections/network-and-dip-switch.md#adding-id)。
- モータの基準の位置を見つける: [原点復帰と位置管理](../guides/homing-and-position.md)。
- 各機能の仕組みを知る: [機能ガイド](../guides/index.md)。
- コマンドを調べる: [OSCリファレンス](../reference/index.md)。

## 関連するコマンドと設定項目 {#related}

<!-- osc-related: /setDestIp, /run, /softStop, /hardHiZ, /setKval -->
<!-- generated:begin osc-related /setDestIp, /run, /softStop, /hardHiZ, /setKval -->
**関連するコマンド**

| コマンド | 引数 | 説明 |
| --- | --- | --- |
| [`/setDestIp`](../reference/system-settings.md#setdestip) | - | モータの状態に変化があったときに通知するメッセージや、問い合わせへ返信するメッセージなどの送り先IPアドレス（`destIp`）を指定します。このメッセージを送信したIPアドレスを`destIp`に設定します。 |
| [`/run`](../reference/motor-control.md#run) | (int)motorID (float)speed | モータを指定速度で回転させます。事前に設定したスピードプロファイルの加速度に従って加速します。指定する回転速度は、maxSpeedを超えるとmaxSpeedでリミットされます。指定速度に到達するまではBUSY状態になります。 |
| [`/softStop`](../reference/motor-control.md#softstop) | (int)motorID | スピードプロファイルに従って減速したのち、モータを励磁したまま停止します。モータが停止するまではBUSY状態になります。もともと無励磁状態だった場合は、停止したままモータが励磁します。 |
| [`/hardHiZ`](../reference/motor-control.md#hardhiz) | (int)motorID | モータを即座に無励磁にします。モータが停止するまではBUSY状態になります。 |
| [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval) | (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)decKVAL | KVAL4種をまとめて設定します。 |
<!-- generated:end osc-related /setDestIp, /run, /softStop, /hardHiZ, /setKval -->
