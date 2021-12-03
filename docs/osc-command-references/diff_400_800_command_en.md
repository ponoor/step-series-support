## Commands only available in STEP400
### Current mode commands
STEP800 doesn't have a current driving mode so following commands related with a current mode are only available in STEP400.

- [`/setVoltageMode (int)motorID`](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setvoltagemode_intmotorid)
- [`/setCurrentMode (int)motorID`](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setcurrentmode_intmotorid)
- [`/setTval (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)setDecTVAL`](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#settval_intmotorid_intholdtval_intruntval_intacctval_intsetdectval)
- [`/getTval (int)motorID`](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#gettval_intmotorid)
- [`/getTval_mA (int)motorID`](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#gettval_ma_intmotorid)
- [`/setDecayModeParam (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN`](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setdecaymodeparam_intmotorid_intt_fast_intton_min_inttoff_min)
- [`/getDecayModeParam (int)motorID`](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#getdecaymodeparam_intmotorid)

### LIMIT input commands
There are no LIMIT inputs in STEP800 (only HOME inputs), so following commands relate with LIMIT inputs are only available in STEP400.

- [`/enableLimitSwReport (int)motorID (bool)enable`](https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#enablelimitswreport_intmotorid_boolenable)
- [`/getLimitSw (int)motorID`](https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#getlimitsw_intmotorid)
- [`/setLimitSwMode (int)motorID (bool)SW_MODE`](https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#setlimitswmode_intmotorid_boolsw_mode)
- [`/getLimitSwMode (int)motorID`](https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#getlimitswmode_intmotorid)


### Other
- [`/getAdcVal (int)motorID`](https://ponoor.com/en/docs/step-series/osc-command-reference/motordriver-settings/#getadcval_intmotorid)
ADC inputs of STEP800 are tied with GND so this command is not available in STEP800.

## Commands which have different setting value
###  [`/setOverCurrentThreshold (int)motorID (int)OCD_TH`](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setovercurrentthreshold_intmotorid_intocd_th)

This command specifies the `OCD_TH` register value directly but possible value ranges and corresponding currents are different between STEP400(PowerSTEP01) and STEP800(L6470) as following;

| Model | OCD_TH range | Corresponding current | Initial value |
| --- | --- | --- | --- |
| STEP400 | 0-31 | 312.5mA - 10A | 15 (5A) |
| STEP800 | 0-15 | 375mA - 6A | 7 (3A) |

### [`/setStallThreshold (int)motorID (int)STALL_TH`](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setstallthreshold_intmotorid_intstall_th)

This command specifies the `STALL_TH` register value directly but possible value ranges and corresponding currents are different between STEP400(PowerSTEP01) and STEP800(L6470) as following;

| Model | STALL_TH range | Corresponding current | Initial value |
| --- | --- | --- | --- |
| STEP400 | 0-31 | 312.5mA - 10A | 31 (10A) |
| STEP800 | 0-127 | 31.25mA - 4A | 127 (4A) |

## Commands which have different response
### [`/getStatus (int)motorID`](https://ponoor.com/en/docs/step-series/osc-command-reference/motordriver-settings/#getstatus_intmotorid)
This command returns `STATUS` register of the motor driver. Information contained in the register is different between STEP400(PowerSTEP01) and STEP800(L6470). Please see the command reference for details.

### [`/getConfigRegister (int)motorID`](https://ponoor.com/en/docs/step-series/osc-command-reference/motordriver-settings/#getconfigregister_intmotorid)
This command returns `CONFIG` register of the motor driver. Information contained in the register is different between STEP400(PowerSTEP01) and STEP800(L6470). Please see the data sheets for details.



