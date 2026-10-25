---
title: STEP400 と STEP800 の違い
lang: ja
---

# STEP400とSTEP800の違い

<!-- This page is generated from spec/osc-commands.yaml by tools/generate.py. Do not edit it directly. (自動生成・直接編集しない) -->

## STEP400のみで使えるコマンド

- [`/getAdcVal`](motor-driver-settings.md#getadcval) (int)motorID（ファームウェアはSTEP800でも受け付けますが、意味のある値は得られません）
- [`/setProhibitMotionOnLimitSw`](alarm-settings.md#setprohibitmotiononlimitsw) (int)motorID (bool)enable
- [`/getProhibitMotionOnLimitSw`](alarm-settings.md#getprohibitmotiononlimitsw) (int)motorID
- [`/setVoltageMode`](voltage-and-current-mode-settings.md#setvoltagemode) (int)motorID
- [`/setCurrentMode`](voltage-and-current-mode-settings.md#setcurrentmode) (int)motorID
- [`/setTval`](voltage-and-current-mode-settings.md#settval) (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL
- [`/getTval`](voltage-and-current-mode-settings.md#gettval) (int)motorID
- [`/getTval_mA`](voltage-and-current-mode-settings.md#gettval_ma) (int)motorID
- [`/setDecayModeParam`](voltage-and-current-mode-settings.md#setdecaymodeparam) (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN
- [`/getDecayModeParam`](voltage-and-current-mode-settings.md#getdecaymodeparam) (int)motorID
- [`/setHoldTval`](voltage-and-current-mode-settings.md#setholdtval) (int)motorID (int)holdTVAL
- [`/setRunTval`](voltage-and-current-mode-settings.md#setruntval) (int)motorID (int)runTVAL
- [`/setAccTval`](voltage-and-current-mode-settings.md#setacctval) (int)motorID (int)accTVAL
- [`/setDecTval`](voltage-and-current-mode-settings.md#setdectval) (int)motorID (int)decTVAL
- [`/enableLimitSwReport`](home-and-limit-sensors.md#enablelimitswreport) (int)motorID (bool)enable
- [`/getLimitSw`](home-and-limit-sensors.md#getlimitsw) (int)motorID
- [`/setLimitSwMode`](home-and-limit-sensors.md#setlimitswmode) (int)motorID (bool)SW_MODE
- [`/getLimitSwMode`](home-and-limit-sensors.md#getlimitswmode) (int)motorID

## STEP400のみが送信するメッセージ

- [`/prohibitMotionOnLimitSw`](alarm-settings.md#getprohibitmotiononlimitsw) (int)motorID (int)enable
- [`/tval`](voltage-and-current-mode-settings.md#gettval) (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL
- [`/tval_mA`](voltage-and-current-mode-settings.md#gettval_ma) (int)motorID (float)holdTVAL_mA (float)runTVAL_mA (float)accTVAL_mA (float)decTVAL_mA
- [`/decayModeParam`](voltage-and-current-mode-settings.md#getdecaymodeparam) (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN
- [`/limitSw`](automatically-sent-messages.md#limitsw) (int)motorID (int)swState (int)direction
- [`/limitSwMode`](home-and-limit-sensors.md#getlimitswmode) (int)motorID (int)swMode

## STEP800のみで使えるコマンド

なし。

## STEP800のみが送信するメッセージ

なし。

## ボードによって値が異なるコマンド

| コマンド | 引数 | STEP400 | STEP800 |
| --- | --- | --- | --- |
| [`/setOverCurrentThreshold`](alarm-settings.md#setovercurrentthreshold) | OCD_TH (範囲) | 0-31 | 0-15 |
| [`/setOverCurrentThreshold`](alarm-settings.md#setovercurrentthreshold) | OCD_TH (初期値) | 15 | 7 (ファームウェア) / 15 (テンプレート) |
| [`/setStallThreshold`](alarm-settings.md#setstallthreshold) | STALL_TH (範囲) | 0-31 | 0-127 |
| [`/setStallThreshold`](alarm-settings.md#setstallthreshold) | STALL_TH (初期値) | 31 | 127 |
| [`/setSpeedProfile`](speed-profile.md#setspeedprofile) | dec (範囲) | 14.55-59590 | 14.55-59575 |
| [`/setDec`](speed-profile.md#setdec) | dec (範囲) | 14.55-59590 | 14.55-59575 |

## ボードによって値が異なるメッセージ

| コマンド | 引数 | STEP400 | STEP800 |
| --- | --- | --- | --- |
| [`/overCurrentThreshold`](alarm-settings.md#setovercurrentthreshold) | overCurrentThreshold (範囲) | 312.5-10000 | 375-6000 |
| [`/stallThreshold`](alarm-settings.md#setstallthreshold) | stallThreshold (範囲) | 312.5-10000 | 31.25-4000 |

## ボード別の表

| コマンド | 説明 |
| --- | --- |
| [`/setOverCurrentThreshold`](alarm-settings.md#setovercurrentthreshold) | 過電流検出の閾値 |
| [`/setStallThreshold`](alarm-settings.md#setstallthreshold) | ストール検出の閾値 |
| [`/thermalStatus`](automatically-sent-messages.md#thermalstatus) | 温度の状態 |

## STEP400のみの設定項目

- [`alarmAndReport.reportLimitSwStatus`](../connections/configuration-items.md#alarmandreport-reportlimitswstatus)
- [`driverSettings.limitSwMode`](../connections/configuration-items.md#driversettings-limitswmode)
- [`driverSettings.prohibitMotionOnLimitSw`](../connections/configuration-items.md#driversettings-prohibitmotiononlimitsw)
- [`driverSettings.isCurrentMode`](../connections/configuration-items.md#driversettings-iscurrentmode)
- [`currentMode.TVAL_HOLD`](../connections/configuration-items.md#currentmode-tval_hold)
- [`currentMode.TVAL_RUN`](../connections/configuration-items.md#currentmode-tval_run)
- [`currentMode.TVAL_ACC`](../connections/configuration-items.md#currentmode-tval_acc)
- [`currentMode.TVAL_DEC`](../connections/configuration-items.md#currentmode-tval_dec)
- [`currentMode.T_FAST`](../connections/configuration-items.md#currentmode-t_fast)
- [`currentMode.TON_MIN`](../connections/configuration-items.md#currentmode-ton_min)
- [`currentMode.TOFF_MIN`](../connections/configuration-items.md#currentmode-toff_min)

## STEP800のみの設定項目

なし。

## ボードによって値が異なる設定項目

| キー | 説明 | STEP400 | STEP800 |
| --- | --- | --- | --- |
| [`information.targetProduct`](../connections/configuration-items.md#information-targetproduct) | template | STEP400 | STEP800 |
| [`network.mac`](../connections/configuration-items.md#network-mac) | template | 60:95:CE:10:02:00 | 60:95:CE:10:03:00 |
| [`alarmAndReport.OCThreshold`](../connections/configuration-items.md#alarmandreport-octhreshold) | default | 15 | 7 |
| [`alarmAndReport.OCThreshold`](../connections/configuration-items.md#alarmandreport-octhreshold) | template | - | 15 |
| [`driverSettings.slewRate`](../connections/configuration-items.md#driversettings-slewrate) | default | 5 | 2 |
| [`driverSettings.slewRate`](../connections/configuration-items.md#driversettings-slewrate) | range | 0-5 | 0-2 |
| [`voltageMode.STALL_TH`](../connections/configuration-items.md#voltagemode-stall_th) | default | 31 | 127 |
