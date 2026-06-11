---
title: モータ毎のパラメータの例
wp_id: 845
slug: example-parameter-values-for-example-steppers
lang: ja
link: "https://ponoor.com/docs/step-series/settings/example-parameter-values-for-example-steppers/"
date: "2020-10-31T14:33:09"
modified: "2021-12-09T17:20:40"
parent: 31
menu_order: 59
---

# モータ毎のパラメータの例

## モータのパラメータの例

モータのデータシート、および実測した値から割り出したパラメータの設定例を、configファイルの形式で公開しています。  
<https://github.com/ponoor/step-series-support/tree/main/configGenerator>

### 設定しているパラメータ

#### config名

`型番_電圧`というconfig名称になっています。

#### 電圧モード

- 各KVALの値（KVAL\_HOLDはKVAL\_RUNの半分に設定しています）
- BEMF補償パラメータ。算出方法は[こちら](https://ponoor.com/docs/step400/functional-description/voltage-mode-and-current-mode/)を参照してください。

#### 電流モード

- 各TVALの値（TVAL\_HOLDはTVAL\_RUNの半分に設定しています）

#### スピードプロファイルについて

モータの最大速さや加減速度は、負荷の重さ、形状、取り付け方法などによって大きく異なりますので、これらの値はすべて初期値のままになっています。実際に負荷を動かしながら、`/setSpeedProfile`コマンドなどで調整してください。

### ファイル名

リンク先のファイルは区別をするために名称が`機種_型番_電圧.json`の形になっていますが、microSDカードにコピーする際に`config.txt`にファイル名を変更する必要があります。詳しくは[miroSDカードを用いた設定](https://ponoor.com/docs/step-series/settings/setup-with-a-microsd-card/)を参照してください。
