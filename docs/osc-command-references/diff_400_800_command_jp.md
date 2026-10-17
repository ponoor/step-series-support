---
title: STEP400とSTEP800で異なる部分
wp_id: 2057
slug: diff_400_800_command
lang: ja
link: "https://ponoor.com/docs/step-series/osc-command-reference/diff_400_800_command/"
date: "2021-12-03T12:01:36"
modified: "2021-12-03T12:08:31"
parent: 33
menu_order: 95
---

# STEP400 と STEP800 の違い

<!-- This page is generated from spec/osc-commands.yaml by tools/generate.py. Do not edit it directly. (自動生成・直接編集しない) -->

## STEP400 のみで使えるコマンド

- [`/getAdcVal`](motor-driver-settings_jp.md#getadcval) (int)motorID (ファームウェアは STEP800 でも受け付けますが、意味のある値は得られません)
- [`/setProhibitMotionOnLimitSw`](alarm-settings_jp.md#setprohibitmotiononlimitsw) (int)motorID (bool)enable
- [`/getProhibitMotionOnLimitSw`](alarm-settings_jp.md#getprohibitmotiononlimitsw) (int)motorID
- [`/setVoltageMode`](voltage-and-current-mode-settings_jp.md#setvoltagemode) (int)motorID
- [`/setCurrentMode`](voltage-and-current-mode-settings_jp.md#setcurrentmode) (int)motorID
- [`/setTval`](voltage-and-current-mode-settings_jp.md#settval) (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL
- [`/getTval`](voltage-and-current-mode-settings_jp.md#gettval) (int)motorID
- [`/getTval_mA`](voltage-and-current-mode-settings_jp.md#gettval_ma) (int)motorID
- [`/setDecayModeParam`](voltage-and-current-mode-settings_jp.md#setdecaymodeparam) (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN
- [`/getDecayModeParam`](voltage-and-current-mode-settings_jp.md#getdecaymodeparam) (int)motorID
- [`/setHoldTval`](voltage-and-current-mode-settings_jp.md#setholdtval) (int)motorID (int)holdTVAL
- [`/setRunTval`](voltage-and-current-mode-settings_jp.md#setruntval) (int)motorID (int)runTVAL
- [`/setAccTval`](voltage-and-current-mode-settings_jp.md#setacctval) (int)motorID (int)accTVAL
- [`/setDecTval`](voltage-and-current-mode-settings_jp.md#setdectval) (int)motorID (int)decTVAL
- [`/enableLimitSwReport`](home-and-limit-sensers_jp.md#enablelimitswreport) (int)motorID (bool)enable
- [`/getLimitSw`](home-and-limit-sensers_jp.md#getlimitsw) (int)motorID
- [`/setLimitSwMode`](home-and-limit-sensers_jp.md#setlimitswmode) (int)motorID (bool)SW_MODE
- [`/getLimitSwMode`](home-and-limit-sensers_jp.md#getlimitswmode) (int)motorID

## STEP400 のみが送信するメッセージ

- [`/prohibitMotionOnLimitSw`](automatically-sent-messages-from-step-400_jp.md#prohibitmotiononlimitsw) (int)motorID (int)enable
- [`/tval`](automatically-sent-messages-from-step-400_jp.md#tval) (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL
- [`/tval_mA`](automatically-sent-messages-from-step-400_jp.md#tval_ma) (int)motorID (float)holdTVAL_mA (float)runTVAL_mA (float)accTVAL_mA (float)decTVAL_mA
- [`/decayModeParam`](automatically-sent-messages-from-step-400_jp.md#decaymodeparam) (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN
- [`/limitSw`](automatically-sent-messages-from-step-400_jp.md#limitsw) (int)motorID (int)swState (int)direction
- [`/limitSwMode`](automatically-sent-messages-from-step-400_jp.md#limitswmode) (int)motorID (int)swMode

## STEP800 のみで使えるコマンド

なし。

## STEP800 のみが送信するメッセージ

なし。

## ボードによって値が異なるコマンド

| コマンド | アーギュメント | STEP400 | STEP800 |
| --- | --- | --- | --- |
| [`/setOverCurrentThreshold`](alarm-settings_jp.md#setovercurrentthreshold) | OCD_TH (範囲) | 0-31 | 0-15 |
| [`/setOverCurrentThreshold`](alarm-settings_jp.md#setovercurrentthreshold) | OCD_TH (初期値) | 15 | 7 (ファームウェア) / 15 (テンプレート) |
| [`/setStallThreshold`](alarm-settings_jp.md#setstallthreshold) | STALL_TH (範囲) | 0-31 | 0-127 |
| [`/setStallThreshold`](alarm-settings_jp.md#setstallthreshold) | STALL_TH (初期値) | 31 | 127 |

## ボードによって値が異なるメッセージ

| コマンド | アーギュメント | STEP400 | STEP800 |
| --- | --- | --- | --- |
| [`/overCurrentThreshold`](automatically-sent-messages-from-step-400_jp.md#overcurrentthreshold) | overCurrentThreshold (範囲) | 312.5-10000 | 375-6000 |
| [`/stallThreshold`](automatically-sent-messages-from-step-400_jp.md#stallthreshold) | stallThreshold (範囲) | 312.5-10000 | 31.25-4000 |

## ボード別の表

| コマンド | 説明 |
| --- | --- |
| [`/setOverCurrentThreshold`](alarm-settings_jp.md#setovercurrentthreshold) | Overcurrent detection threshold |
| [`/setStallThreshold`](alarm-settings_jp.md#setstallthreshold) | Stall detection threshold |
| [`/thermalStatus`](automatically-sent-messages-from-step-400_jp.md#thermalstatus) | Thermal status |

## STEP400 のみの設定項目

- [`alarmAndReport.reportLimitSwStatus`](../connections-and-settings/configuration-items_jp.md#alarmandreport-reportlimitswstatus)
- [`driverSettings.limitSwMode`](../connections-and-settings/configuration-items_jp.md#driversettings-limitswmode)
- [`driverSettings.prohibitMotionOnLimitSw`](../connections-and-settings/configuration-items_jp.md#driversettings-prohibitmotiononlimitsw)
- [`driverSettings.isCurrentMode`](../connections-and-settings/configuration-items_jp.md#driversettings-iscurrentmode)
- [`currentMode.TVAL_HOLD`](../connections-and-settings/configuration-items_jp.md#currentmode-tval_hold)
- [`currentMode.TVAL_RUN`](../connections-and-settings/configuration-items_jp.md#currentmode-tval_run)
- [`currentMode.TVAL_ACC`](../connections-and-settings/configuration-items_jp.md#currentmode-tval_acc)
- [`currentMode.TVAL_DEC`](../connections-and-settings/configuration-items_jp.md#currentmode-tval_dec)
- [`currentMode.T_FAST`](../connections-and-settings/configuration-items_jp.md#currentmode-t_fast)
- [`currentMode.TON_MIN`](../connections-and-settings/configuration-items_jp.md#currentmode-ton_min)
- [`currentMode.TOFF_MIN`](../connections-and-settings/configuration-items_jp.md#currentmode-toff_min)

## STEP800 のみの設定項目

なし。

## ボードによって値が異なる設定項目

| キー | 説明 | STEP400 | STEP800 |
| --- | --- | --- | --- |
| [`information.targetProduct`](../connections-and-settings/configuration-items_jp.md#information-targetproduct) | template | STEP400 | STEP800 |
| [`network.mac`](../connections-and-settings/configuration-items_jp.md#network-mac) | template | 60:95:CE:10:02:00 | 60:95:CE:10:03:00 |
| [`alarmAndReport.OCThreshold`](../connections-and-settings/configuration-items_jp.md#alarmandreport-octhreshold) | default | 15 | 7 |
| [`alarmAndReport.OCThreshold`](../connections-and-settings/configuration-items_jp.md#alarmandreport-octhreshold) | template | - | 15 |
| [`driverSettings.slewRate`](../connections-and-settings/configuration-items_jp.md#driversettings-slewrate) | default | 5 | 2 |
| [`driverSettings.slewRate`](../connections-and-settings/configuration-items_jp.md#driversettings-slewrate) | range | 0-5 | 0-2 |
| [`voltageMode.STALL_TH`](../connections-and-settings/configuration-items_jp.md#voltagemode-stall_th) | default | 31 | 127 |
