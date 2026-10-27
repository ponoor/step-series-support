---
title: ファームウェアの更新
---

# ファームウェアの更新

ファームウェアは、バグの修正や機能の追加のために更新されます。まず、ボードに書き込まれているファームウェアのバージョンを確認してください。[GitHubの最新のリリース](https://github.com/ponoor/step-series-universal-firmware/releases)より古いときは、更新してください。

各バージョンの変更点は[変更履歴](changelog.md)にあります。動いているシステムを更新する前に、新しいバージョンの注意を[移行ガイド](migration-guide.md)で読んでください。バージョンによっては、OSCコマンドの動作が変わったり、エラーの返信が増えたりします。

## ボードのファームウェアのバージョンの確認 {#checking}

確認する方法は2つあります。

- OSC（Open Sound Control）のコマンド`/getVersion`を送る。
- ボードにUSBケーブルをつないで、シリアルモニタから`s`を送る。

### OSCコマンドで {#osc}

ボードに[`/getVersion`](../reference/system-settings.md#getversion)を送ります。返信に、ファームウェアの名前、バージョン、ビルドの日付が入っています。たとえば次のようになります。

```
/version "STEP800_R1_UNIVERSAL 2.2.0 Oct 20 2026 10:00:00"
```

### USBで {#usb}

ボードとパソコンをUSB-Cケーブルでつなぎ、シリアルモニタを開いて、`s`を送ります。状態の最初の部分に、ファームウェアの情報が出ます。たとえば次のようになります。

```
-------------- Firmware --------------
Firmware name : STEP800_R1_UNIVERSAL
Firmware version : 2.2.0
Compile date : Oct 20 2026, 10:00:00
```

続きは[USBシリアル診断](usb-serial-diagnosis.md#status)をご覧ください。

## 最新のバージョンの確認 {#latest}

最新のバージョンは、ファームウェアのリポジトリの[Releases](https://github.com/ponoor/step-series-universal-firmware/releases)のページにあります。

2022年3月までは、STEP400とSTEP800のファームウェアは、別々のリポジトリで管理していました。その後、1つの「STEP-series Universal Firmware」に移り、バージョン番号も一度リセットしました。ボードのファームウェアが最新かどうかは、次の手順で確かめてください。

1. ボードから取得したファームウェアの名前に`UNIVERSAL`が入っているかどうかを確かめます。
2. 入っていなければ、ファームウェアが古いので、更新が必要です。
3. 入っていれば、バージョンを[Releases](https://github.com/ponoor/step-series-universal-firmware/releases)のページのバージョンと比べます。

以前のファームウェアは次の場所にありますが、メンテナンスはしていません。

| ボード | 旧リポジトリ |
| --- | --- |
| STEP400 | <https://github.com/ponoor/STEP400/releases> |
| STEP800 | <https://github.com/ponoor/STEP800/releases> |

## 更新する {#updating}

ボードのファームウェアが古いときは、最新のファームウェアをビルドして、USBのブートローダで書き込んで更新します。リリースには、すぐに使えるバイナリファイルはありません。[ファームウェアのコンパイル](compile-the-arduino-sketch.md)をご覧ください。

更新する前に、OSCコマンドで変えた設定を保存してください。カードの設定ファイルは残りますが、変えたまま保存していない値は消えます。[設定の仕組み](../connections/how-settings-work.md#saved-values)をご覧ください。
