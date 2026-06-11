---
title: 接続
wp_id: 2275
slug: connections
lang: ja
link: "https://ponoor.com/docs/step100-200/assemble/connections/"
date: "2022-02-02T21:48:15"
modified: "2022-02-03T14:01:28"
parent: 2169
menu_order: 44
---

# 接続

## 重ねる順序

Arduinoの上にEthernet ShieldとX-Nucleoをスタッキングしますが、Ethernet Shieldの通信に必要なSPIピンヘッダがX-Nucleoについていないのと、X-Nucleoの事前準備でカットしたD4ピンもEthernet Shieldに接続する必要があるので、重ねる際は必ず

1. Arduinoの上にEthernet Shield
2. そのうえにX-Nucleo

という順序にします。

![file](https://ponoor.com/cms/wp-content/uploads/2022/01/image-1643346463746.png)  
写真はSTEP200. Arduino M0の上にEthernet Shield, その上にX-NUCLEO-IHM02A1が載っています。

## 接続

### 電源

X-Nucleoに電源を接続します。基板上の表示との対応関係は以下の通りです。ただし通電するのは、ファームウェアを書き込み終わってからにしましょう。

| 極性 | IHM03A1 (STEP100) | IHM02A1 (STEP200) |
| --- | --- | --- |
| プラス | `Vin` | `VS+` |
| マイナス | `GND` | `-` |

![](https://ponoor.com/cms/wp-content/uploads/2022/01/IMG_4315.jpg)![](https://ponoor.com/cms/wp-content/uploads/2022/01/IMG_4314.jpg)

### モータ

バイポーラ型ステッピングモータを接続します。このタイプのモータには2ペアのコイルが入っていて、このペアとドライバ側のペア出力とが対応するように接続します。ぺアはモータのデータシートを確認するか、あるいはテスタで抵抗値を測ることによっても確認できます。

ペアの基板上の表記は以下の通りですが、特にIHM02A1(L6470) ではわかりにくいので要注意です。

| Motor coil | IHM03A1 | IHM02A1 |
| --- | --- | --- |
| Coil 1 | A+, A- | 1A, 2A |
| Coil 2 | B+, B- | 1B, 2B |

[![](https://ponoor.com/cms/wp-content/uploads/2022/02/step200_wiring-700x510.png)](https://ponoor.com/cms/wp-content/uploads/2022/02/step200_wiring.png)
