## 概要
設定ファイルを書き込んだmicroSDカードを本デバイスに差し込んで起動すると、起動時にファイルに書かれた設定で初期化をすることができます。
設定ファイルは設定ツール (Config Tool) を使って書き出せます。

microSDカードを差し込まずに起動した場合は、ファームウェアに書かれた初期値が使用されます。

## microSDカードの準備
使用することができるのはmicroSDカードか、microSDHCカードのどちらかのみで、FAT16かFAT32形式でフォーマットされている必要があります。また使用可能なファイル名は8文字まで、拡張子は3文字までに制限されます。

文字数の制限についての詳細は [SDライブラリのリファレンス](https://www.arduino.cc/en/Reference/SD)を参照してください。

## 設定ツール (Config Tool)
設定ファイルはHTMLとJavaScriptによって構成されています。このURLからアクセスできます。
http://ponoor.com/tools/step400-config/

ファイルはこちらから入手できます。
https://github.com/ponoor/STEP400/tree/master/configTool

ページの一番上で、過去に書きだした設定ファイルを読み込むことができます。
設定はページ末尾の "Export" ボタンを押してダウンロードしてください。ファイル名は `config.txt`です。ファイル形式はJSONですが、拡張子が3文字までしか使えないため`.json`ではなく`.txt`になっています。

このファイルをmicroSDカードの一番上の階層へコピーしたうえで本デバイスに差し込みます。この状態で起動、あるいはリセットしてください。設定は起動時にのみ読み込まれます。

項目の多くはOSCメッセージ経由でも設定可能です。対応するOSCメッセージは下の表に示してある通りですが、JSONファイルやArduinoスケッチでの変数名と合わせた一覧表が[こちら](https://docs.google.com/spreadsheets/d/1EAUpzARE69ip6_LolZAv3crpmXGsESjCOz6EqVY1lUo/edit?usp=sharing)にあります。

## Config Toolの項目
### `Information`
| Parameter | OSC command | Default |
|-----------|-------------|---------|
| Configuration name | - | "Default" |
| Configuration version | - | 1.0 |
| Target product | - | "STEP400" または "STEP800" |

#### Configuration name
設定ファイルの名称で、自由に設定できます。
#### Configuration version 
Config Toolsのバージョン番号で、変更できません。
#### Target product
設定ファイルの対象製品名で、変更できません。

### `Network`

| Parameter | OSC command | Default |
|-----------|-------------|---------|
| My IP address |-| 10.0.0.100 |
| ID adds to my IP |-| TRUE |
| Destination IP | [/setDestIp](https://ponoor.com/docs/step-series/osc-command-reference/system-settings/#setdestip) | 10.0.0.10 |
| Gateway |-| 10.0.0.1 |
| DNS |-| 10.0.0.1 |
| Subnet mask |-| 255.255.255.0 |
| Incoming port |-| 50000 |
| Outgoing port |-| 50100 |
| ID adds to Outgoing port |-| TRUE |
| MAC address |-| 0x60, 0x95, 0xCE, 0x10, 0x02, 0x00 |
| ID adds to MAC address |-| TRUE |
| Booted message enable |-| TRUE |
| Allow OSC reply before /setDestIp |-| FALSE |
| Report errors | [/reportError](https://ponoor.com/docs/step-series/osc-command-reference/system-settings/#reporterror_boolenable) | TRUE |

#### My IP address
IPアドレスを設定します。`ID adds to my IP`にチェックが入っている場合は、この数値にIDが加算されたものが実際のIPアドレスになります。例えば`10.0.0.100`に設定してIDスイッチが1になっている場合は、`10.0.0.101`が実際のアドレスになります。加算した数値が254を超えないようにしてください。

#### Incoming port
STEP400がOSCを受信するポート番号です。

#### Outgoing port
STEP400がOSCを送信するポート番号です。`ID adds to Outgoing port`にチェックが入っていると、この数値にIDが加算されます。
#### MAC address
`Hex`チェックボックスで、16進数表示と10進数表示を切替できます。

#### ID adds to MAC address
このチェックボックスが入っていると、MACアドレスの最終バイトにIDが加算されます。

#### Booted message enable
起動時にイーサネットがリンクすると自動で送られる[`/booted`](https://ponoor.com/docs/step-series/osc-command-reference/automatically-sent-messages-from-step-400/#booted)メッセージの有効無効を切り替えます。

#### Allow OSC reply before /setDestIp
初期状態では`/setDestIp`を受信するまではOSCの返送を行わないようになっていますが、このチェックボックスが入っていると、起動してすぐからOSC返送するようにします。

### `Alarm and Report`
| Parameter | OSC command | Default |
|-----------|-------------|---------|
| Report BUSY | [/enableBusyReport](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#enablebusyreport_intmotorid_boolenable) | FALSE |
| Report HiZ | [/enableHizReport](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#enablehizreport_intmotorid_boolenable) | FALSE |
| Report HOME switch status | [/enableHomeSwReport](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#enablehomeswreport_intmotorid_boolenable) | FALSE |
| Report motor direction | /enableDirReport | FALSE |
| Report Motor Status | [/enableMotorStatusReport](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#enablemotorstatusreport_intmotorid_boolenable) | FALSE |
| Report HOME switch event | [/enableSwEventReport](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#enablesweventreport_intmotorid_boolenable) | FALSE |
| Report undervoltage lockout | [/enableUvloReport](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#enableuvloreport_intmotorid_boolenable) | TRUE |
| Report thermal status of driver chip | [/enableThermalStatusReport](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#enablethermalstatusreport_intmotorid_boolenable) | TRUE |
| Report motor stall detection | [/enableStallReport](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#enablestallreport_intmotorid_boolenable) | FALSE |
| Report LIMIT switch status | [/enableLimitSwReport](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#enablelimitswreport_intmotorid_boolenable) | FALSE |
| Overcurrent threshold | [/setOverCurrentThreshold](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#setovercurrentthreshold_intmotorid_intocd_th) | 15 |

### `Driver Settings`
| Parameter | OSC command | Default |
|-----------|-------------|---------|
| Homing when the system starts | ([/homing](https://ponoor.com/docs/step-series/osc-command-reference/homing/#homing_intmotorid)) | FALSE |
| Homing Direction | [/setHomingDirection](https://ponoor.com/docs/step-series/osc-command-reference/homing/#sethomingdirection_intmotorid_booldirection) | Reverse |
| Homing Speed | [/setHomingSpeed](https://ponoor.com/docs/step-series/osc-command-reference/homing/#sethomingspeed_intmotorid_floatspeed) | 50 |
| Home switch won't cause HardStop | [/setHomeSwMode](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#sethomeswmode_intmotorid_boolsw_mode) | SW_USER |
| Prohibit motions on HomeSw | [/setProhibitMotionOnHomeSw](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#setprohibitmotiononhomesw_intmotorid_boolenable) | FALSE |
| Limit switch won't cause HardStop | [/setLimitSwMode](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#setlimitswmode_intmotorid_boolsw_mode) | SW_USER |
| Prohibit motions on LimitSw | [/setProhibitMotionOnLimitSw](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#setprohibitmotiononlimitsw_intmotorid_boolenable) | FALSE |
| goUntil timeout duration | [/setGoUntilTimeout](https://ponoor.com/docs/step-series/osc-command-reference/homing/#setgountiltimeout_intmotorid_inttimeout) | 10000 |
| releaseSw timeout duration | [/setReleaseSwTimeout](https://ponoor.com/docs/step-series/osc-command-reference/homing/#setreleaseswtimeout_intmotorid_inttimeout) | 10000 |
| Microstepping mode | [/setMicrostepMode](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#setmicrostepmode_intmotorid_intstep_sel) | STEP_FS_128 |
| Current mode | [/setVoltageMode](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setvoltagemode_intmotorid), [/setCurrentMode](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setcurrentmode_intmotorid) | FALSE |
| Slew rate | - | SR_980V_us |
| Electromagnetic brake enable | [/enableElectromagnetBrake](https://ponoor.com/docs/step-series/osc-command-reference/brake/#enableelectromagnetbrake_intmotorid_boolenable) | FALSE |
| Brake transition duration | [/setBrakeTransitionDuration](https://ponoor.com/docs/step-series/osc-command-reference/brake/#setbraketransitionduration_intmotorid_intduration) | 100 |

#### Homing when the system starts
このチェックボックスが入っていると、起動すると直ちに原点復帰動作を行います。

#### Slew rate
PowerSTEP01から出力されるモータ制御電流のスリューレート（立ち上がりの鋭さ）を114V/usから980V/usまで6段階で指定します。

### `Speed Profile`
| Parameter | OSC command | Default |
|-----------|-------------|---------|
| Acceleration | [/setSpeedProfile](https://ponoor.com/docs/step-series/osc-command-reference/speed-profile/#setspeedprofile_intmotorid_floatacc_floatdec_floatmaxspeed) | 2000 |
| Decceleration | [/setSpeedProfile](https://ponoor.com/docs/step-series/osc-command-reference/speed-profile/#setspeedprofile_intmotorid_floatacc_floatdec_floatmaxspeed) | 2000 |
| Max speed | [/setSpeedProfile](https://ponoor.com/docs/step-series/osc-command-reference/speed-profile/#setspeedprofile_intmotorid_floatacc_floatdec_floatmaxspeed) | 620 |
| Transit to fullstep threshold speed | [/setFullstepSpeed](https://ponoor.com/docs/step-series/osc-command-reference/speed-profile/#setfullstepspeed_intmotorid_floatfullstepspeed) | 15625 |

### `Voltage Mode`
| Parameter | OSC command | Default |
|-----------|-------------|---------|
| KVAL_HOLD | [/setKval](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setkval_intmotorid_intholdkval_intrunkval_intacckval_intsetdeckval) | 16 |
| KVAL_RUN | [/setKval](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setkval_intmotorid_intholdkval_intrunkval_intacckval_intsetdeckval) | 16 |
| KVAL_ACC | [/setKval](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setkval_intmotorid_intholdkval_intrunkval_intacckval_intsetdeckval) | 16 |
| KVAL_DEC | [/setKval](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setkval_intmotorid_intholdkval_intrunkval_intacckval_intsetdeckval) | 16 |
| INT_SPEED | [/setBemfParam](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setbemfparam_intmotorid_intint_speed_intst_slp_intfn_slp_acc_intfn_slp_dec) | 1032 |
| ST_SLP | [/setBemfParam](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setbemfparam_intmotorid_intint_speed_intst_slp_intfn_slp_acc_intfn_slp_dec) | 25 |
| FN_SLP_ACC | [/setBemfParam](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setbemfparam_intmotorid_intint_speed_intst_slp_intfn_slp_acc_intfn_slp_dec) | 41 |
| FN_SLP_DEC | [/setBemfParam](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setbemfparam_intmotorid_intint_speed_intst_slp_intfn_slp_acc_intfn_slp_dec) | 41 |
| STALL_TH | [/setStallThreshold](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#setstallthreshold_intmotorid_intstall_th) | 31 |
| lowSpeedOptimize | [/setLowSpeedOptimizeThreshold](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#setlowspeedoptimizethreshold_intmotorid_floatlowspeedoptimizationthreshold) | 20 |

### `Current Mode`
| Parameter | OSC command | Default |
|-----------|-------------|---------|
| TVAL_HOLD | [/setTval](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#settval_intmotorid_intholdtval_intruntval_intacctval_intsetdectval) | 16 |
| TVAL_RUN | [/setTval](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#settval_intmotorid_intholdtval_intruntval_intacctval_intsetdectval) | 16 |
| TVAL_ACC | [/setTval](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#settval_intmotorid_intholdtval_intruntval_intacctval_intsetdectval) | 16 |
| TVAL_DEC | [/setTval](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#settval_intmotorid_intholdtval_intruntval_intacctval_intsetdectval) | 16 |
| T_FAST | [/setDecayModeParam](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setdecaymodeparam_intmotorid_intt_fast_intton_min_inttoff_min) | 25 |
| TON_MIN | [/setDecayModeParam](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setdecaymodeparam_intmotorid_intt_fast_intton_min_inttoff_min) | 41 |
| TOFF_MIN | [/setDecayModeParam](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setdecaymodeparam_intmotorid_intt_fast_intton_min_inttoff_min) | 41 |

### `Servo Mode`
| Parameter | OSC command | Default |
|-----------|-------------|---------|
| kP | [/setServoParam](https://ponoor.com/docs/step-series/osc-command-reference/servo-mode/#setservoparam_intmotorid_floatkp_floatki_floatkd) | 0.06 |
| kI | [/setServoParam](https://ponoor.com/docs/step-series/osc-command-reference/servo-mode/#setservoparam_intmotorid_floatkp_floatki_floatkd) | 0 |
| kD | [/setServoParam](https://ponoor.com/docs/step-series/osc-command-reference/servo-mode/#setservoparam_intmotorid_floatkp_floatki_floatkd) | 0 |
