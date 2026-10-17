---
title: Differences between STEP400 and STEP800
lang: en
---

# Differences between STEP400 and STEP800

<!-- This page is generated from spec/osc-commands.yaml by tools/generate.py. Do not edit it directly. -->

## Commands available on STEP400 only

- [`/getAdcVal`](motor-driver-settings.md#getadcval) (int)motorID (the firmware also accepts it on STEP800, but the value is meaningless there)
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

## Messages sent by STEP400 only

- [`/prohibitMotionOnLimitSw`](automatically-sent-messages.md#prohibitmotiononlimitsw) (int)motorID (int)enable
- [`/tval`](automatically-sent-messages.md#tval) (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL
- [`/tval_mA`](automatically-sent-messages.md#tval_ma) (int)motorID (float)holdTVAL_mA (float)runTVAL_mA (float)accTVAL_mA (float)decTVAL_mA
- [`/decayModeParam`](automatically-sent-messages.md#decaymodeparam) (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN
- [`/limitSw`](automatically-sent-messages.md#limitsw) (int)motorID (int)swState (int)direction
- [`/limitSwMode`](automatically-sent-messages.md#limitswmode) (int)motorID (int)swMode

## Commands available on STEP800 only

None.

## Messages sent by STEP800 only

None.

## Commands with board-specific values

| Command | Argument | STEP400 | STEP800 |
| --- | --- | --- | --- |
| [`/setOverCurrentThreshold`](alarm-settings.md#setovercurrentthreshold) | OCD_TH (Range) | 0-31 | 0-15 |
| [`/setOverCurrentThreshold`](alarm-settings.md#setovercurrentthreshold) | OCD_TH (Initial value) | 15 | 7 (firmware) / 15 (template) |
| [`/setStallThreshold`](alarm-settings.md#setstallthreshold) | STALL_TH (Range) | 0-31 | 0-127 |
| [`/setStallThreshold`](alarm-settings.md#setstallthreshold) | STALL_TH (Initial value) | 31 | 127 |

## Messages with board-specific values

| Command | Argument | STEP400 | STEP800 |
| --- | --- | --- | --- |
| [`/overCurrentThreshold`](automatically-sent-messages.md#overcurrentthreshold) | overCurrentThreshold (Range) | 312.5-10000 | 375-6000 |
| [`/stallThreshold`](automatically-sent-messages.md#stallthreshold) | stallThreshold (Range) | 312.5-10000 | 31.25-4000 |

## Board-specific tables

| Command | Description |
| --- | --- |
| [`/setOverCurrentThreshold`](alarm-settings.md#setovercurrentthreshold) | Overcurrent detection threshold |
| [`/setStallThreshold`](alarm-settings.md#setstallthreshold) | Stall detection threshold |
| [`/thermalStatus`](automatically-sent-messages.md#thermalstatus) | Thermal status |

## Configuration items of STEP400 only

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

## Configuration items of STEP800 only

None.

## Configuration items with board-specific values

| Key | Description | STEP400 | STEP800 |
| --- | --- | --- | --- |
| [`information.targetProduct`](../connections/configuration-items.md#information-targetproduct) | template | STEP400 | STEP800 |
| [`network.mac`](../connections/configuration-items.md#network-mac) | template | 60:95:CE:10:02:00 | 60:95:CE:10:03:00 |
| [`alarmAndReport.OCThreshold`](../connections/configuration-items.md#alarmandreport-octhreshold) | default | 15 | 7 |
| [`alarmAndReport.OCThreshold`](../connections/configuration-items.md#alarmandreport-octhreshold) | template | - | 15 |
| [`driverSettings.slewRate`](../connections/configuration-items.md#driversettings-slewrate) | default | 5 | 2 |
| [`driverSettings.slewRate`](../connections/configuration-items.md#driversettings-slewrate) | range | 0-5 | 0-2 |
| [`voltageMode.STALL_TH`](../connections/configuration-items.md#voltagemode-stall_th) | default | 31 | 127 |
