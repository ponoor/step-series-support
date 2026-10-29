---
title: 接続
---

# 接続

ボードの重ね方と、X-NUCLEOボードへの電源とモータの接続です。

## 重ねる順序 {#stacking-order}

ArduinoとEthernetシールドは6ピンのSPIコネクタを介して通信しますが、X-NUCLEOボードにはこのコネクタがありません。また、X-NUCLEOボードの準備でカットしたD4ピンも、Ethernetシールドに接続する必要があります。

そのため、重ねる順序は必ず次のとおりにします。

1. Arduinoの上にEthernetシールド
2. その上にX-NUCLEOボード

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643346463746.png)  
写真はSTEP200です。Arduino M0の上にEthernetシールド、その上にX-NUCLEO-IHM02A1が載っています。

## 接続 {#connections}

### 電源 {#power-supply}

X-NUCLEOボードに電源をつなぎます。基板上の表示との対応は次のとおりです。

!!! warning "ファームウェアを書き込むまで電源を入れないでください"
    電源を入れるのは、ファームウェアを書き込み終わってからです（[スケッチの書き込み](../upload-the-sketch.md)）。

| 極性 | IHM03A1（STEP100） | IHM02A1（STEP200） |
| --- | --- | --- |
| プラス | `Vin` | `VS+` |
| マイナス | `GND` | `-` |

![](https://ponoor.com/cms/wp-content/uploads/2022/01/IMG_4315.jpg)![](https://ponoor.com/cms/wp-content/uploads/2022/01/IMG_4314.jpg)

### モータ {#motor}

バイポーラ型のステッピングモータをつなぎます。このタイプのモータには2つのコイルがあり、それぞれのコイルを、ドライバの出力の1組につなぎます。コイルのペアは、モータのデータシートで確認するか、テスタで4本の線の間の抵抗値を測って確認できます。

ペアの基板上の表記は次のとおりですが、特にIHM02A1（L6470）ではわかりにくいので注意してください。

| モータのコイル | IHM03A1 | IHM02A1 |
| --- | --- | --- |
| コイル1 | A+, A- | 1A, 2A |
| コイル2 | B+, B- | 1B, 2B |

[![](https://ponoor.com/cms/wp-content/uploads/2022/02/step200_wiring-700x510.png)](https://ponoor.com/cms/wp-content/uploads/2022/02/step200_wiring.png)
