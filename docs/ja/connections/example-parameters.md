---
title: モータ別のパラメータ例
---

# モータ別のパラメータ例

弊社の研究室にあるモータについて、データシートと実測した値から割り出したパラメータを、設定ファイルの形で公開しています。ファイルをmicroSDカードにコピーするか、[ブラウザ設定ツール](browser-config-tool.md)で開いて調整できます。

ファイルはここにあります: <https://github.com/ponoor/step-series-support/tree/main/configGenerator>

## 設定しているパラメータ {#parameters}

### 設定名とファイル名 {#names}

ファイルの中の設定名は、`<型番>_<電圧>`の形で、たとえば`17HS08-1004S_24V`です。ファイル名は、リポジトリの中で区別できるように、`<ボード>_<型番>_<電圧>.json`の形で、たとえば`STEP400_17HS08-1004S_24V.json`です。

### 電圧モード {#voltage-mode}

- 各KVALの値（KVAL_HOLDはKVAL_RUNの半分に設定しています）。
- BEMF補償のパラメータ。算出方法は[電圧モードの設定](../guides/voltage-and-current-mode.md#voltage-mode-setting)をご覧ください。

値は、モータの電源電圧によって変わります。ある電圧に合う値が、別の電圧では強すぎることがあります。[KVALとTVAL](../guides/voltage-and-current-mode.md#kval-tval)をご覧ください。

### 電流モード {#current-mode}

- 各TVALの値（TVAL_HOLDはTVAL_RUNの半分に設定しています）。

### スピードプロファイル {#speed-profile}

モータの最大速度や加速度、減速度は、負荷の重さ、形状、取り付け方法によって大きく異なります。そのため、これらの値は初期値のままです。実際に負荷を動かしながら、[`/setSpeedProfile`](../reference/speed-profile.md#setspeedprofile)などのコマンドで調整してください。

## ファイルの使い方 {#using}

ファイルは、そのままmicroSDカードのルートフォルダにコピーします。ボードは、ルートフォルダのどの`.json`ファイルでも読むので、名前を変える必要はありません（v2.1.0より前のファームウェアが読むのは、`config.txt`という名前のファイルだけです）。規則は[ボードが読むファイル](microsd-card.md#files)をご覧ください。
