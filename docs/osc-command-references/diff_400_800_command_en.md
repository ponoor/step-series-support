---
title: Differences between STEP400 and STEP800
wp_id: 2071
slug: differences-between-step400-and-step800
lang: en
link: "https://ponoor.com/en/docs/step-series/osc-command-reference/differences-between-step400-and-step800/"
date: "2021-12-03T13:03:39"
modified: "2021-12-03T13:19:13"
parent: 888
menu_order: 96
---

# Differences between STEP400 and STEP800

<!-- This page is generated from spec/osc-commands.yaml by tools/generate.py. Do not edit it directly. -->

## Commands available on STEP400 only

- [`/getAdcVal`](motor-driver-settings_en.md#getadcval) (int)motorID (the firmware also accepts it on STEP800, but the value is meaningless there)
- [`/setProhibitMotionOnLimitSw`](alarm-settings_en.md#setprohibitmotiononlimitsw) (int)motorID (bool)enable
- [`/getProhibitMotionOnLimitSw`](alarm-settings_en.md#getprohibitmotiononlimitsw) (int)motorID
- [`/setVoltageMode`](voltage-and-current-mode-settings_en.md#setvoltagemode) (int)motorID
- [`/setCurrentMode`](voltage-and-current-mode-settings_en.md#setcurrentmode) (int)motorID
- [`/setTval`](voltage-and-current-mode-settings_en.md#settval) (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL
- [`/getTval`](voltage-and-current-mode-settings_en.md#gettval) (int)motorID
- [`/getTval_mA`](voltage-and-current-mode-settings_en.md#gettval_ma) (int)motorID
- [`/setDecayModeParam`](voltage-and-current-mode-settings_en.md#setdecaymodeparam) (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN
- [`/getDecayModeParam`](voltage-and-current-mode-settings_en.md#getdecaymodeparam) (int)motorID
- [`/setHoldTval`](voltage-and-current-mode-settings_en.md#setholdtval) (int)motorID (int)holdTVAL
- [`/setRunTval`](voltage-and-current-mode-settings_en.md#setruntval) (int)motorID (int)runTVAL
- [`/setAccTval`](voltage-and-current-mode-settings_en.md#setacctval) (int)motorID (int)accTVAL
- [`/setDecTval`](voltage-and-current-mode-settings_en.md#setdectval) (int)motorID (int)decTVAL
- [`/enableLimitSwReport`](home-and-limit-sensors_en.md#enablelimitswreport) (int)motorID (bool)enable
- [`/getLimitSw`](home-and-limit-sensors_en.md#getlimitsw) (int)motorID
- [`/setLimitSwMode`](home-and-limit-sensors_en.md#setlimitswmode) (int)motorID (bool)SW_MODE
- [`/getLimitSwMode`](home-and-limit-sensors_en.md#getlimitswmode) (int)motorID

## Messages sent by STEP400 only

- [`/prohibitMotionOnLimitSw`](automatically-sent-messages-from-step-400_en.md#prohibitmotiononlimitsw) (int)motorID (int)enable
- [`/tval`](automatically-sent-messages-from-step-400_en.md#tval) (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL
- [`/tval_mA`](automatically-sent-messages-from-step-400_en.md#tval_ma) (int)motorID (float)holdTVAL_mA (float)runTVAL_mA (float)accTVAL_mA (float)decTVAL_mA
- [`/decayModeParam`](automatically-sent-messages-from-step-400_en.md#decaymodeparam) (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN
- [`/limitSw`](automatically-sent-messages-from-step-400_en.md#limitsw) (int)motorID (int)swState (int)direction
- [`/limitSwMode`](automatically-sent-messages-from-step-400_en.md#limitswmode) (int)motorID (int)swMode

## Commands available on STEP800 only

None.

## Messages sent by STEP800 only

None.

## Commands with board-specific values

| Command | Argument | STEP400 | STEP800 |
| --- | --- | --- | --- |
| [`/setOverCurrentThreshold`](alarm-settings_en.md#setovercurrentthreshold) | OCD_TH (Range) | 0-31 | 0-15 |
| [`/setOverCurrentThreshold`](alarm-settings_en.md#setovercurrentthreshold) | OCD_TH (Initial value) | 15 | 7 (firmware) / 15 (template) |
| [`/setStallThreshold`](alarm-settings_en.md#setstallthreshold) | STALL_TH (Range) | 0-31 | 0-127 |
| [`/setStallThreshold`](alarm-settings_en.md#setstallthreshold) | STALL_TH (Initial value) | 31 | 127 |

## Messages with board-specific values

| Command | Argument | STEP400 | STEP800 |
| --- | --- | --- | --- |
| [`/overCurrentThreshold`](automatically-sent-messages-from-step-400_en.md#overcurrentthreshold) | overCurrentThreshold (Range) | 312.5-10000 | 375-6000 |
| [`/stallThreshold`](automatically-sent-messages-from-step-400_en.md#stallthreshold) | stallThreshold (Range) | 312.5-10000 | 31.25-4000 |

## Board-specific tables

| Command | Description |
| --- | --- |
| [`/setOverCurrentThreshold`](alarm-settings_en.md#setovercurrentthreshold) | Overcurrent detection threshold |
| [`/setStallThreshold`](alarm-settings_en.md#setstallthreshold) | Stall detection threshold |
| [`/thermalStatus`](automatically-sent-messages-from-step-400_en.md#thermalstatus) | Thermal status |

## Configuration items of STEP400 only

- [`alarmAndReport.reportLimitSwStatus`](../connections-and-settings/configuration-items_en.md#alarmandreport-reportlimitswstatus)
- [`driverSettings.limitSwMode`](../connections-and-settings/configuration-items_en.md#driversettings-limitswmode)
- [`driverSettings.prohibitMotionOnLimitSw`](../connections-and-settings/configuration-items_en.md#driversettings-prohibitmotiononlimitsw)
- [`driverSettings.isCurrentMode`](../connections-and-settings/configuration-items_en.md#driversettings-iscurrentmode)
- [`currentMode.TVAL_HOLD`](../connections-and-settings/configuration-items_en.md#currentmode-tval_hold)
- [`currentMode.TVAL_RUN`](../connections-and-settings/configuration-items_en.md#currentmode-tval_run)
- [`currentMode.TVAL_ACC`](../connections-and-settings/configuration-items_en.md#currentmode-tval_acc)
- [`currentMode.TVAL_DEC`](../connections-and-settings/configuration-items_en.md#currentmode-tval_dec)
- [`currentMode.T_FAST`](../connections-and-settings/configuration-items_en.md#currentmode-t_fast)
- [`currentMode.TON_MIN`](../connections-and-settings/configuration-items_en.md#currentmode-ton_min)
- [`currentMode.TOFF_MIN`](../connections-and-settings/configuration-items_en.md#currentmode-toff_min)

## Configuration items of STEP800 only

None.

## Configuration items with board-specific values

| Key | Description | STEP400 | STEP800 |
| --- | --- | --- | --- |
| [`information.targetProduct`](../connections-and-settings/configuration-items_en.md#information-targetproduct) | template | STEP400 | STEP800 |
| [`network.mac`](../connections-and-settings/configuration-items_en.md#network-mac) | template | 60:95:CE:10:02:00 | 60:95:CE:10:03:00 |
| [`alarmAndReport.OCThreshold`](../connections-and-settings/configuration-items_en.md#alarmandreport-octhreshold) | default | 15 | 7 |
| [`alarmAndReport.OCThreshold`](../connections-and-settings/configuration-items_en.md#alarmandreport-octhreshold) | template | - | 15 |
| [`driverSettings.slewRate`](../connections-and-settings/configuration-items_en.md#driversettings-slewrate) | default | 5 | 2 |
| [`driverSettings.slewRate`](../connections-and-settings/configuration-items_en.md#driversettings-slewrate) | range | 0-5 | 0-2 |
| [`voltageMode.STALL_TH`](../connections-and-settings/configuration-items_en.md#voltagemode-stall_th) | default | 31 | 127 |
