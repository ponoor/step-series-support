---
title: Voltage mode and current mode
---

# Voltage mode and current mode

A stepper motor can be driven with a constant voltage (voltage mode) or with a constant current (current mode). This page explains how the two differ, what KVAL and TVAL are, and how to switch between the modes.

## The difference between voltage control and current control {#difference}

There are two types of stepping control methods: constant voltage control (**voltage mode**) and constant current control (**current mode**). Only the STEP400 can switch between voltage mode and current mode; the STEP800 works in voltage mode only. The commands for the current mode, such as `/setCurrentMode` and `/setTval`, do not exist on the STEP800; see [Differences between STEP400 and STEP800](../reference/differences-step400-step800.md). The difference between the modes is explained well in [this presentation PDF](https://www.st.com/content/dam/AME/2019/developers-conference-2019/presentations/STDevCon19_3.6_Using%20Powerstep01.pdf) by STMicroelectronics.

In short:

- Voltage mode is quiet and smooth, but it can run only at lower speeds.
- Current mode is noisy, but it can reach higher speeds.

### Test with the STEP400 {#test}

A demonstration video of the test: [Voltage mode and current mode test (Vimeo)](https://vimeo.com/1239730082)

We tested both modes with a STEP400 and a motor with a microphone attached to its body, so that the smallest noises were captured. In voltage mode the motor ran quietly, but from around 800 steps/s it began to vibrate and it stalled at about 1,400 steps/s. In current mode the motor was noisy, but it ran faster than 11,000 steps/s before it began to vibrate and stalled.

## KVAL and TVAL {#kval-tval}

The **KVAL** registers control the drive voltage in voltage mode, and the **TVAL** registers control the drive current in current mode. Both act as multipliers: KVAL sets what fraction of the supply voltage is applied to the motor, and TVAL sets the target current. Inside the driver they are the same registers, but the firmware keeps the two sets of values separate and rewrites the registers when the mode is changed, so that a value for one mode is never used by accident in the other.

Each of them has four values, for holding, running, accelerating and decelerating. [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval) and [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval) set all four at once, and [`/setHoldKval`](../reference/voltage-and-current-mode-settings.md#setholdkval), [`/setRunKval`](../reference/voltage-and-current-mode-settings.md#setrunkval) and so on set one. [`/getKval`](../reference/voltage-and-current-mode-settings.md#getkval), [`/getTval`](../reference/voltage-and-current-mode-settings.md#gettval) and [`/getTval_mA`](../reference/voltage-and-current-mode-settings.md#gettval_ma) return the settings that were made, not the registers (in voltage mode the TVAL registers are not written, and in current mode the KVAL registers are not).

When the motor has an electromagnetic brake, the holding value is raised automatically. See [Electromagnetic brake](electromagnetic-brake.md#hold-current).

## Voltage mode setting {#voltage-mode-setting}

In voltage mode, KVAL sets the percentage of the supply voltage that is applied to the motor. If a high-voltage power source is used, excessive current may flow when the motor is turning at low speed. To compensate for this, there is a group of registers (the back-EMF compensation) that lowers the applied voltage at low speed and raises it at high speed. They are set with [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) or with the [browser configuration tool](../connections/browser-config-tool.md).

How to calculate the register values is described in the STMicroelectronics application note [AN4144](https://www.st.com/resource/en/application_note/dm00061093-voltage-mode-control-operation-and-parameter-optimization-stmicroelectronics.pdf). For some motors we calculated the values from the datasheet and from measurements; they are in [Example parameters for sample motors](../connections/example-parameters.md). There are only a few of them at the moment, and we plan to add more. If you have a motor that is not listed and you have determined the values yourself, we would be glad if you shared them with us and the community.

The values depend on the supply voltage. A set of values that suits one voltage can be too strong at another one: the default back-EMF compensation was too strong at 24 V. When you change the power supply, check the values again.

## Current mode setting {#current-mode-setting}

In current mode, which is available on the STEP400 only, the TVAL registers set the target current. The current of a TVAL value is

> current = (TVAL + 1) × 78.125 mA

so the value 0 is 78.125 mA, not 0 A. The STEP400 limits TVAL to a maximum of about 5 A even though the PowerSTEP01 can drive up to 10 A, because of the power rating of the current-sensing resistor of the board. A value above the limit is limited to it, not rejected. The values and the currents are listed in [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval). The thresholds of overcurrent and stall use the same kind of conversion; see [Alarms and protection](alarms-and-protection.md#thresholds).

A high-voltage power supply is needed to deliver the target current when the motor runs at high speed. At a phase current of 5 A the torque is very strong, and the tiniest mistake can lead to great physical danger. In such situations we recommend using an industrial-grade motor driver.

## Switching between the modes {#switching}

Use these commands to switch between the modes:

- [`/setVoltageMode`](../reference/voltage-and-current-mode-settings.md#setvoltagemode): switch to voltage mode.
- [`/setCurrentMode`](../reference/voltage-and-current-mode-settings.md#setcurrentmode): switch to current mode.

The outputs of the motor must be HiZ before the mode is switched. A motor that is holding its position is not HiZ. For example, to switch motor 1 to current mode, send these commands in this order:

1. `/hardHiZ 1`
2. `/setCurrentMode 1`

If the motor is not HiZ, the board replies `/error/command MotorNotHiZ` and does not change the mode (see [Command executable timing](../reference/index.md#command-executable-timing) in the common rules).

Current mode supports microsteps only up to 1/16. When the motor is switched to current mode with a finer microstep setting, the microstep setting becomes 1/16, and [`/setMicrostepMode`](../reference/motor-driver-settings.md#setmicrostepmode) replies `CommandIgnored` for a finer setting while the motor is in current mode. When the microstep setting changes, the coordinate system changes too: one rotation of a 200-step motor is 200 × 128 = 25600 steps in 1/128 microstep mode, but 200 × 16 = 3200 steps in 1/16 microstep mode.

## Related commands and settings {#related}

<!-- osc-related: drive_mode -->
<!-- generated:begin osc-related drive_mode -->
**Related commands**

| Command | Arguments | Description |
| --- | --- | --- |
| [`/setVoltageMode`](../reference/voltage-and-current-mode-settings.md#setvoltagemode) | (int)motorID | Switches the specified motor to the voltage drive mode. |
| [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval) | (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)decKVAL | Sets the four KVALs together. |
| [`/getKval`](../reference/voltage-and-current-mode-settings.md#getkval) | (int)motorID | Get the four KVALs together. |
| [`/setBemfParam`](../reference/voltage-and-current-mode-settings.md#setbemfparam) | (int)motorID (int)INT_SPEED (int)ST_SLP (int)FN_SLP_ACC (int)FN_SLP_DEC | Sets BEMF compensation parameter register. |
| [`/getBemfParam`](../reference/voltage-and-current-mode-settings.md#getbemfparam) | (int)motorID | Get register values for the BEMF parameter. |
| [`/setHoldKval`](../reference/voltage-and-current-mode-settings.md#setholdkval) | (int)motorID (int)holdKVAL | Sets only the hold KVAL value. |
| [`/setRunKval`](../reference/voltage-and-current-mode-settings.md#setrunkval) | (int)motorID (int)runKVAL | Sets only the run KVAL value. |
| [`/setAccKval`](../reference/voltage-and-current-mode-settings.md#setacckval) | (int)motorID (int)accKVAL | Sets only the acceleration KVAL value. |
| [`/setDecKval`](../reference/voltage-and-current-mode-settings.md#setdeckval) | (int)motorID (int)decKVAL | Sets only the deceleration KVAL value. |
| [`/setCurrentMode`](../reference/voltage-and-current-mode-settings.md#setcurrentmode) | (int)motorID | Switches the specified motor to the current drive mode. |
| [`/setTval`](../reference/voltage-and-current-mode-settings.md#settval) | (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL | Sets the four TVALs together. |
| [`/getTval`](../reference/voltage-and-current-mode-settings.md#gettval) | (int)motorID | Get the four TVAL types together. |
| [`/getTval_mA`](../reference/voltage-and-current-mode-settings.md#gettval_ma) | (int)motorID | Get the four TVAL types together. |
| [`/setDecayModeParam`](../reference/voltage-and-current-mode-settings.md#setdecaymodeparam) | (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN | Sets registers for the current control algorithm parameters. |
| [`/getDecayModeParam`](../reference/voltage-and-current-mode-settings.md#getdecaymodeparam) | (int)motorID | Retrieves the register values for the current control algorithm parameters. |
| [`/setHoldTval`](../reference/voltage-and-current-mode-settings.md#setholdtval) | (int)motorID (int)holdTVAL | Sets only the hold TVAL value. |
| [`/setRunTval`](../reference/voltage-and-current-mode-settings.md#setruntval) | (int)motorID (int)runTVAL | Sets only the run TVAL value. |
| [`/setAccTval`](../reference/voltage-and-current-mode-settings.md#setacctval) | (int)motorID (int)accTVAL | Sets only the acceleration TVAL value. |
| [`/setDecTval`](../reference/voltage-and-current-mode-settings.md#setdectval) | (int)motorID (int)decTVAL | Sets only the deceleration TVAL value. |
<!-- generated:end osc-related drive_mode -->

<!-- osc-settings: driverSettings.isCurrentMode, voltageMode, currentMode -->
<!-- generated:begin osc-settings driverSettings.isCurrentMode, voltageMode, currentMode -->
**Related configuration items**

| Key | Name | Commands |
| --- | --- | --- |
| [`driverSettings.isCurrentMode`](../connections/configuration-items.md#driversettings-iscurrentmode) | Current mode | `/setVoltageMode`, `/setCurrentMode` |
| [`voltageMode.KVAL_HOLD`](../connections/configuration-items.md#voltagemode-kval_hold) | KVAL_HOLD | `/setKval`, `/setHoldKval` |
| [`voltageMode.KVAL_RUN`](../connections/configuration-items.md#voltagemode-kval_run) | KVAL_RUN | `/setKval`, `/setRunKval` |
| [`voltageMode.KVAL_ACC`](../connections/configuration-items.md#voltagemode-kval_acc) | KVAL_ACC | `/setKval`, `/setAccKval` |
| [`voltageMode.KVAL_DEC`](../connections/configuration-items.md#voltagemode-kval_dec) | KVAL_DEC | `/setKval`, `/setDecKval` |
| [`voltageMode.INT_SPEED`](../connections/configuration-items.md#voltagemode-int_speed) | INT_SPEED | `/setBemfParam` |
| [`voltageMode.ST_SLP`](../connections/configuration-items.md#voltagemode-st_slp) | ST_SLP | `/setBemfParam` |
| [`voltageMode.FN_SLP_ACC`](../connections/configuration-items.md#voltagemode-fn_slp_acc) | FN_SLP_ACC | `/setBemfParam` |
| [`voltageMode.FN_SLP_DEC`](../connections/configuration-items.md#voltagemode-fn_slp_dec) | FN_SLP_DEC | `/setBemfParam` |
| [`voltageMode.STALL_TH`](../connections/configuration-items.md#voltagemode-stall_th) | STALL_TH | `/setStallThreshold` |
| [`voltageMode.lowSpeedOptimizeEnable`](../connections/configuration-items.md#voltagemode-lowspeedoptimizeenable) | Low speed optimize enable | `/enableLowSpeedOptimize` |
| [`voltageMode.lowSpeedOptimize`](../connections/configuration-items.md#voltagemode-lowspeedoptimize) | lowSpeedOptimize | `/setLowSpeedOptimizeThreshold` |
| [`currentMode.TVAL_HOLD`](../connections/configuration-items.md#currentmode-tval_hold) | TVAL_HOLD | `/setTval`, `/setHoldTval` |
| [`currentMode.TVAL_RUN`](../connections/configuration-items.md#currentmode-tval_run) | TVAL_RUN | `/setTval`, `/setRunTval` |
| [`currentMode.TVAL_ACC`](../connections/configuration-items.md#currentmode-tval_acc) | TVAL_ACC | `/setTval`, `/setAccTval` |
| [`currentMode.TVAL_DEC`](../connections/configuration-items.md#currentmode-tval_dec) | TVAL_DEC | `/setTval`, `/setDecTval` |
| [`currentMode.T_FAST`](../connections/configuration-items.md#currentmode-t_fast) | T_FAST | `/setDecayModeParam` |
| [`currentMode.TON_MIN`](../connections/configuration-items.md#currentmode-ton_min) | TON_MIN | `/setDecayModeParam` |
| [`currentMode.TOFF_MIN`](../connections/configuration-items.md#currentmode-toff_min) | TOFF_MIN | `/setDecayModeParam` |
<!-- generated:end osc-settings driverSettings.isCurrentMode, voltageMode, currentMode -->
