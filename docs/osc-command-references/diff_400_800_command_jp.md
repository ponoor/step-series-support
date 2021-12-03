## STEP400のみにあるコマンド
### 電流モード関連
電流モードはSTEP800にはありませんので、以下の電圧・電流モード切替のコマンドや電流モードの設定コマンドはSTEP400でのみ使用できます。
- [`/setVoltageMode (int)motorID`](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setvoltagemode_intmotorid)
- [`/setCurrentMode (int)motorID`](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setcurrentmode_intmotorid)
- [`/setTval (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)setDecTVAL`](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#settval_intmotorid_intholdtval_intruntval_intacctval_intsetdectval)
- [`/getTval (int)motorID`](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#gettval_intmotorid)
- [`/getTval_mA (int)motorID`](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#gettval_ma_intmotorid)
- [`/setDecayModeParam (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN`](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setdecaymodeparam_intmotorid_intt_fast_intton_min_inttoff_min)
- [`/getDecayModeParam (int)motorID`](https://ponoor.com/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#getdecaymodeparam_intmotorid)

### リミットスイッチ関連
LIMIT入力はSTEP800にはありません（HOME入力のみ）ので、以下のLIMIT入力に関係するコマンドはSTEP400でのみ使用できます。
- [`/enableLimitSwReport (int)motorID (bool)enable`](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#enablelimitswreport_intmotorid_boolenable)
- [`/getLimitSw (int)motorID`](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#getlimitsw_intmotorid)
- [`/setLimitSwMode (int)motorID (bool)SW_MODE`](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#setlimitswmode_intmotorid_boolsw_mode)
- [`/getLimitSwMode (int)motorID`](https://ponoor.com/docs/step-series/osc-command-reference/home-limit-sensors/#getlimitswmode_intmotorid)


### その他
- [`/getAdcVal (int)motorID`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#getadcval_intmotorid)
ADC入力はSTEP800ではGNDに接続されていて使用できません。

## 設定値が異なるコマンド
###  [`/setOverCurrentThreshold (int)motorID (int)OCD_TH`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#setovercurrentthreshold_intmotorid_intocd_th)

このコマンドでは`OCD_TH`としてレジスタの値を直接指定しますが、設定値の範囲と対応する電流は以下の通り異なっています。

| 機種 | OCD_THの範囲 | 対応する電流 | 初期値 |
| --- | --- | --- | --- |
| STEP400 | 0-31 | 312.5mA - 10A | 15 (5A) |
| STEP800 | 0-15 | 375mA - 6A | 7 (3A) |

### [`/setStallThreshold (int)motorID (int)STALL_TH`](https://ponoor.com/docs/step-series/osc-command-reference/alarm-settings/#setstallthreshold_intmotorid_intstall_th)

このコマンドでは`STALL_TH`としてレジスタの値を直接指定しますが、設定値の範囲と対応する電流は以下の通り異なっています。

| 機種 | STALL_THの範囲 | 対応する電流 | 初期値 |
| --- | --- | --- | --- |
| STEP400 | 0-31 | 312.5mA - 10A | 31 (10A) |
| STEP800 | 0-127 | 31.25mA - 4A | 127 (4A) |

## 返答が異なるコマンド
### [`/getStatus (int)motorID`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#getstatus_intmotorid)
このコマンドはモータドライバの`STATUS`レジスタの値を返します。この値の意味はSTEP400(PowerSTEP01)とSTEP800(L6470)で異なっています。詳しくはコマンドリファレンスをご確認ください。

### [`/getConfigRegister (int)motorID`](https://ponoor.com/docs/step-series/osc-command-reference/motordriver-settings/#getconfigregister_intmotorid)
このコマンドはモータドライバの`CONFIG`レジスタの値を返します。この値の意味はSTEP400(PowerSTEP01)とSTEP800(L6470)で異なっています。詳しくは各モータドライバチップのデータシートをご確認ください。



