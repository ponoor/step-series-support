## 電圧制御と電流制御の違い
ステッピングモータの制御方式には定電圧制御（**電圧モード**）と定電流制御（**電流モード**）の2種のモードがあり、STEP800は電圧モード、STEP400では電圧モードと電流モードの両方を切り替えて使うことができます。これらの制御モードの違いについては[こちら](https://www.st.com/content/dam/AME/2019/developers-conference-2019/presentations/STDevCon19_3.6_Using%20Powerstep01.pdf)に STMicroelectronics社のプレゼンテーション資料があり、わかりやすくまとめられています。

実際に使う側にとっての違いを簡単にまとめると、以下の通りです。

- 電圧モードは静かに滑らかに回るが、低速でしか回せない。
- 電流モードは音がうるさいが、高速まで回せる。

## STEP400を使ったテスト
この映像では、

- 定電圧制御と定電流制御の違い
- フルステップ駆動とマイクロステッピング駆動の違い

について、順を追って試しています。
<div class="embed-video">
<iframe width="560" height="315" src="https://www.youtube.com/embed/ydPHQfc22kQ" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

まず最初は電圧モードで動かしています。回転数が800step/secを超えたあたりからうまく回らずに振動が発生して、1,400step/secくらいで脱調して完全に停止してしまいます。振動が発生するまでは静かに回りますが、この映像では微細な音もとらえるためにモータ本体にマイクを張り付けています。

次に電流モードに切り替えて動かしています。動作音は大きいですが、高速域まで回転できます。今回のセッティングでは11,000step/sec以上まで回転できました。

## KVALとTVAL
電圧モードの場合は**KVAL**レジスタで電圧を制御して, 電流モードの場合は**TVAL**レジスタで電流を制御します。それらはドライバ内部では物理的に同じレジスタですが、モードを切り替えた際に意図しない値になることを避けるために、ファームウェアでそれぞれ別の値として保持しておいて、モード切替時に書き換えています。

## 電圧モードの設定
STEP400/STEP800の電圧モードでは、KVALというレジスタを使って、電源電圧の何パーセントをモータに印加するかを指定できます。
また高い電圧の電源を使った場合、低速で回っているときには必要以上の電流が流れてしまうことがあります。この電流の不均衡を調整するために、低速回転時には相対的に印加電圧を下げて、回転数が大きくなると印加電圧を上げる補正を行うためのレジスタ群があります。
これらのレジスタ値の算出方法はSTMicroelectronicsの[アプリケーションノート](https://www.st.com/resource/en/application_note/dm00061093-voltage-mode-control-operation-and-parameter-optimization-stmicroelectronics.pdf)に記載されています。これらのレジスタ値は [`/setBemfParam`](https://ponoor.com/docs/step400/osc-command-reference/voltage-and-current-mode-settings/#setbemfparam_intmotorid_intint_speed_intst_slp_intfn_slp_acc_intfn_slp_dec)コマンドで設定できるほか、[Config Tool](http://ponoor.com/tools/step400-config/)からも設定できます。

いくつかのモータについては、データシートの数値と実測した数値をもとにレジスタの値を算出し、[設定ファイル](https://ponoor.com/docs/step-series/settings/example-parameter-values-for-example-steppers/)を公開しています。

## 電流モードの設定
STEP400で利用可能な電流モードでは、TVALというレジスタを使って目標値となる電流値を設定します。STEP400では78mA刻みで5Aまで設定できます。高速に回転させているときに目標の電流を流すにはやはり高い電圧の電源が必要です。PowerSTEP01の本来の能力は10Aまで制御可能ですが、STEP400では電流検出抵抗の定格電力の制限で5Aが上限です。相電流が5Aとなるとかなり強いトルクで、少しのミスが大きな危険につながります。このような状況では産業用ドライバを使用するのが良いと思います。

## モードの切替方法
各モードに切り替える場合は以下のコマンドを使用します。
- [`/setVoltageMode`](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setvoltagemode_intmotorid) - 電圧モードに切り替える
- [`/setCurrentMode`](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setcurrentmode_intmotorid) - 電流モードに切り替える

切り替える前に、当該モータがハイ・インピーダンス状態になっている必要があります。例えばモータ1を電流モードに切り替える場合に送るコマンドは
1. `/hardHiZ 1`
2. `/setCurrentMode 1`

という順になります。


電流制御ではマイクロステッピングモードは1/16までしか使えませんので、それより小さい値になっていた場合は強制的に1/16に切り替わります。マイクロステッピングモードが切り替わると、座標体系も変化します。例えば1周200stepのモータでは、1/128マイクロステッピングモードでは1周は200x128=25600stepですが、1/16マイクロステッピングモードでは200x16=3200stepになります。

