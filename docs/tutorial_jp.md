## チュートリアル用コード
本デバイスはOpen Sound Control (OSC) プロトコルで通信しますので、OSCを送受信するホストアプリケーション（またはプログラム）が必要です。

- [Max](https://github.com/ponoor/step-series-example-Max) 現状Maxのサンプルファイルが最も機能を網羅しています。[Maxをダウンロード](https://cycling74.com/downloads "Maxをダウンロード")・インストールして使用してください。
- [Processing](https://github.com/yuskegoto/STEP400_Processing)
Contribution of [@yuskegoto](https://github.com/yuskegoto)
- [openFrameworks](https://github.com/ponoor/step-series-example-openFrameworks)
Contribution of [@niimi](https://github.com/niimi)
- [Unity](https://github.com/ponoor/step-series-example-Unity)
Contribution of [@niimi](https://github.com/niimi)
- [Touch Designer](https://github.com/ponoor/step-series-example-TouchDesigner)
Contribution of [@loveandsheep](https://github.com/loveandsheep), [@yuskegoto](https://github.com/yuskegoto)
- [Node-RED](https://github.com/yuskegoto/STEP400_Node-RED)
Contribution of [@yuskegoto](https://github.com/yuskegoto)

## 接続
### ネットワーク
まずPCと基板をLANケーブルで接続します。PCにEthernet端子がない場合は USB-Ethernet変換などが必要です。自動でIPアドレスを割り振るDHCPサーバ機能がついたルータなどを経由すると問題が起きる可能性がありますので、まずはPCと本デバイスを一対一で接続するとわかりやすいです。

### ステッピングモータ
本デバイスで使用できるのは、「バイポーラ型」のステッピングモータです。使うモータによって電源の容量や各種設定が変わってきます。入手しやすいモータの例としては、MERCURY MOTORのSM-42BYG011-25があります。例えば以下の場所で購入できます。
- [Strawberry Linux](http://strawberry-linux.com/catalog/items?code=12026)
- [秋月電子通商](https://akizukidenshi.com/catalog/g/gP-05372/)
- [Sparkfun](https://www.sparkfun.com/products/9238)

![](http://ponoor.com/manage/wp-content/uploads/2020/10/09238-01.jpg)

以下、具体的な設定数値についてはこのモータを例にしていきます。
このモータをコネクタに取り付けるにあたり、まずはこの[接続方法](https://ponoor.com/docs/step-series/settings/power-supply-and-motor/#i-5)を確認してください。

このモータのデータシートは[こちら](https://www.sparkfun.com/datasheets/Robotics/SM-42BYG011-25.pdf)にあります。
これをみると、コイルのペアは 赤と緑、黄と青、になっていることがわかります。
[![](https://ponoor.com/cms/wp-content/uploads/2020/08/motor-wiring-diagram-sample.png)](https://ponoor.com/cms/wp-content/uploads/2020/08/motor-wiring-diagram-sample.png)

同じコイルから出てきた線をペアにしますので、例えばコネクタへの接続は以下のようになります。
[![](https://ponoor.com/cms/wp-content/uploads/2020/08/SM-42BYG-wiring-700x525.jpg)](https://ponoor.com/cms/wp-content/uploads/2020/08/SM-42BYG-wiring.jpg)


### 電源
上の例に出てきたモータを1台回す場合は、ACアダプタの容量は24V1Aあれば十分です。本デバイスに接続可能なのは、外径5.5mm, 内径2.1mmでセンタープラスのACアダプタです。
<img src="https://ponoor.com/cms/wp-content/uploads/2020/08/image-1609563897700.png" width="600" />

このサイズのモータを回すのにはDCジャックからの給電で構いませんが、より高電圧、大電流を流す必要がある場合は隣のねじ式端子に電源を接続してください。

実際に電源を投入するのは、下記のDIPスイッチの設定が完了してからにします。

## ネットワークの設定
### Config Tool
microSDカードへ入れる設定ファイルを書き出すための [Config Tool](http://ponoor.com/tools/step400-config/) (HTML+JavaScript)を使ってネットワークの設定を変更できますが、ここではSDカードを差し込まず、初期設定を使用することにします。

### 基板側
基板上のIDスイッチ(8桁のDIPスイッチ)は1に設定してください。すなわち1の桁のみON, ほかの桁はすべてOFFの状態です。向かって左側が小さい桁になっていることに注意してください。

このスイッチで設定したIDは、初期設定状態ではIPアドレスやOSC送信ポートなどに加算されます。IPアドレスの初期値は10.0.0.100ですので、IDスイッチが1にセットされているときは10.0.0.101になります。この状態での基板はネットワーク設定は以下になります。

| 項目 | 設定値 |
| ---- | ---- |
| IPアドレス | 10.0.0.101 |
| 返信先アドレス | 10.0.0.10 |
| OSC受信ポート | 50000 |
| OSC送信ポート | 50101 |

<img src="https://ponoor.com/cms/wp-content/uploads/2020/10/step400-dipSw.jpg" width="600" />

この状態までできたら本デバイスに接続した電源を投入してみます。本デバイスの裏側には電源電圧がそのままかかっている端子が複数ありますので、基板の穴にスペーサなどを取り付けるか、電気を通さない台の上に置いてください。

### PC側
本デバイスを接続しているEthernetポートに固定IPを設定します。IPv4を以下のように設定してください。

| 項目 | 設定値 |
| ---- | ---- |
| IPアドレス | 10.0.0.10 |
| サブネットマスク | 255.255.255.0 |

固定IPの設定の仕方はOSによって異なります。

- [Windows10](https://support.microsoft.com/ja-jp/help/15089/windows-change-tcp-ip-settings)
- [Mac](https://support.apple.com/ja-jp/HT202480)

ここまでうまく設定できていれば、MacのターミナルやWindowsのコマンドプロンプトなどから`ping 10.0.0.101`などのコマンドで接続が確認できると思います。 

## 通信の確認
ここから先は制御に使用する環境によって実際の操作は異なりますが、実際に送受信する Open Sound Control のメッセージのみ記載していきます。

まず、本デバイスにメッセージの返信先アドレスを教えるコマンドである `/setDestIp` を送ります。送る際の送信先アドレスは 10.0.0.101, 送信ポートは 50000 です。このコマンドが届くまでは、本デバイス側からはOSCメッセージの送信を行いません。存在しないあて先にOSCメッセージを送り続けると本デバイスの動作が不安定になることがあるためです。

`/setDestIp`が問題なく受信されると、以下のような応答があるはずです。受信ポートは 50101 です。

```
/destIp (int)destIp[0] (int)destIp[1] (int)destIp[2] (int)destIp[3] (bool)isNewDestIp
```

- `destIp[0-3]` : destIpの各桁
- `isNewDestIp` : destIpが変更されたかどうかを示します。変更されていると1, すでに同じアドレスが設定されていた場合は0です。

これでメッセージをやり取りする準備が整いました。

うまくいかない場合は、PCのネットワーク設定を再度確認してください。Windowsの場合は、使用しているアプリケーションの通信がファイヤーウォールで許可されているかどうかも確認してください。

## 動かしてみる
早速モータを動かすコマンドを送ってみましょう。`/run (int)motorID (float)speed`というコマンドでモータが指定速度で回ります。

`motorID`とは、どのモータを動かすかを本デバイスの基板に印刷されている番号で指定するものです。`255`をIDに指定すると、すべてのモータへコマンドを送ることができます。これはIDを指定するほとんどのコマンドで使用できます。

`speed`はモータの回転速さと向きを指定します。指定できる範囲は -15625.0 - 15625.0 で、単位は [step/s] です。もし1周が200stepのモータを使っているとすると、1秒で1回転させるには200.0を指定します。マイナスの値を指定すると逆向きに回ります。

例えば、コネクタ1番に接続したモータを1秒で1回転させるには、次のようなOSCメッセージになります。

```
/run 1 200.
```

無事回ったでしょうか？何かモータの様子が変でとりあえず停止させたい場合は、`speed`に`0.0`を指定するか、すべてのモータを停止する

`/hardHiZ 255`

というメッセージを送ってください。

おそらく多くの場合ではきれいに回らなかったと思います。モータに合わせたパラメータの調整が必要ですので、引き続き設定していきます。

## KVALの設定
きれいに回らない原因の多くは駆動電圧が不足していることによるもの（高すぎてきれいに回らないこともあります）で、KVALレジスタで調整します。これはモータを駆動する電圧を0から255の数値で指定するもので、0にすると0V（回りません）、255にすると電源電圧のほぼそのままがモータ駆動電圧になります。
例えば24Vの電源を使っていて、KVALに128を指定した場合は、モータは約12Vで駆動されることになります。

KVALは以下のように4種類に分かれています。

| 名称 | 内容 |　本デバイスの初期値 |
| --- | --- | --- |
| KVAL_HOLD | モータ停止中のKVAL | 0 |
| KVAL_RUN | モータが一定速で回転中のKVAL | 16 |
| KVAL_ACC | モータが加速中のKVAL | 16 |
| KVAL_DEC | モータが減速中のKVAL | 16 |

モータを一定速で回転させながら、KVAL_RUNを調整してみましょう。

```
/run 1 200.
```

を送ってモータを回転させます。

`/setRunKval`というコマンドで KVAL_RUN だけ設定することもできますが、ここでは4つまとめて設定できる次のメッセージを使用してみます。

```
/setKval (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)setDecKVAL
```

motorIDは`/run`と同様、STEP400の場合は`1-4, 255`、STEP800の場合は`1-8, 255`で指定し、KVALはいずれも0-255で指定します。ここでは停止中のKVALは0, 加速、減速については一定速のKVALと同じ値に設定しながら、徐々に数値を増やしてみます。

```
/setKval 1 0 24 24 24
```

このOSCメッセージを送ると、1番目のモータのKVALを、停止時は0, それ以外は24（電源電圧の約9%）に設定します。ここから徐々に数値を

```
/setKval 1 0 32 32 32
```

のように上げていくと、どこかで静かに回り始めます。KVALを上げるとトルクが上がっていきますが、モータの発熱が大きくなったり、振動が再び大きくなってきたりしますので、負荷に合わせて調整してください。