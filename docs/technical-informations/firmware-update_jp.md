## ファームウェアのアップデート
バグの修正や機能の追加等でファームウェアがアップデートされることがあります。

まず現在基板に書き込まれているファームウェアのバージョンを確認し、もしGithubで公開されているバージョンよりも古い場合はアップデートをお願いします。

## 書き込まれているファームウェアバージョンの確認方法
Ethernet経由でOSCから確認する方法と、USB経由でシリアルモニタから確認する方法があります。
### OSCから確認する
`/getVersion` メッセージで現在のファームウェアバージョンを確認できます。詳しくはコマンドリファレンスの[`/getVersion`](https://ponoor.com/docs/step-series/osc-command-reference/system-settings/#getversion)を確認してください。

#### 返答例
```
/version "STEP800_R1_UNIVERSAL 1.0.1 Mar 24 2022 11:17:29"
```

### USBから確認する
本デバイスとPCをUSBで接続し、シリアルモニタから`s`を送信すると得られるステータスから現在のファームウェアバージョンを確認できます。
詳しくは[USBシリアルからの診断](https://ponoor.com/docs/step-series/technical-information/diagnosis/)の「[Firmware](https://ponoor.com/docs/step-series/technical-information/diagnosis/#firmware)」を確認してください。

#### 返答例
```
-------------- Firmware --------------
Firmware name : STEP800_R1_UNIVERSAL
Firmware version : 1.0.1
Compile date : Mar 24 2022, 11:17:29
```
　
## 現在の最新バージョン番号の確認方法
ファームウェアを管理しているリポジトリの"[Releases](https://github.com/ponoor/step-series-universal-firmware/releases)"から確認できます。

これまでSTEP400とSTEP800は別々のリポジトリでファームウェアを管理していましたが、2022年3月より統一した "[STEP-series Universal Firmware](https://github.com/ponoor/step-series-universal-firmware)" に移行しました。それに伴ってバージョン番号も一度リセットされていますので、以下の手順で最新かどうかを確かめてください。

1. 基板から取得したファームウェアの名称に `UNIVERSAL` が入っているかどうかを確かめる
2. 入っていない→最新ではないので要アップデート
3. 入っている→リポジトリの "[Releases](https://github.com/ponoor/step-series-universal-firmware/releases)"のバージョンと比較して、古い場合は要アップデート


なお、以下の場所に以前のファームウェアが置いてありますが、メンテナンスはされていません。

| 機種 | 旧リポジトリ |
| --- | ---|
| STEP400 | https://github.com/ponoor/STEP400/releases |
| STEP800 | https://github.com/ponoor/STEP800/releases |


## ファームウェアをアップデートする
基板に書き込まれているファームウェアが古くなっていた場合はアップデートをお願いします。アップデートはArduino IDEからArduinoスケッチをコンパイル＆書き込みすることによって行います。詳しくは「[Arduinoスケッチのコンパイル](https://ponoor.com/docs/step-series/technical-information/compile-the-arduino-sketch/)」を参照してください。


