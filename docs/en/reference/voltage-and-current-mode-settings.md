---
title: Voltage and current mode settings
---

# Voltage and current mode settings

For how to decide the KVAL and TVAL values, see [Voltage and current mode](../guides/voltage-and-current-mode.md).

## Voltage mode

<!-- osc: /setVoltageMode -->
<!-- generated:begin osc /setVoltageMode -->
### `/setVoltageMode` (int)motorID {#setvoltagemode}

Available on STEP400 only.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

High Z state

#### Description

Switches the specified motor to the voltage drive mode.

Note: This command is only available in STEP400.  
STEP800 is always in this voltage mode and cannot change.

#### Changes

- **v2.2.0**: The outputs must be HiZ; otherwise `/error/command MotorNotHiZ` is replied and nothing is applied.
- **v2.2.0**: The mode is changed only if the driver took it (STEP_MODE is read back); otherwise `/error/command CommandIgnored`. Before, the stored mode was changed while the driver kept the old one, so [`/setKval`](voltage-and-current-mode-settings.md#setkval) and [`/setTval`](voltage-and-current-mode-settings.md#settval) then wrote the wrong registers.

#### Errors

- `MotorNotHiZ`: The command writes a driver register that can be written only while the outputs are HiZ, and the motor is not HiZ. A motor holding its position is not HiZ: send `/softHiZ` or `/hardHiZ` first. Nothing is applied. Added in v2.2.0.
- `CommandIgnored`: The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`).

#### See also

[`/setCurrentMode`](voltage-and-current-mode-settings.md#setcurrentmode)
<!-- generated:end osc /setVoltageMode -->

<!-- osc: /setKval -->
<!-- generated:begin osc /setKval -->
### `/setKval` (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)decKVAL {#setkval}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| holdKVAL | int | 0-255 | KVAL when stopped |
| runKVAL | int | 0-255 | KVAL in constant speed operation |
| accKVAL | int | 0-255 | KVAL during acceleration |
| decKVAL | int | 0-255 | KVAL during deceleration |

#### Executable timing

Always

#### Description

Sets the four KVALs together.

A value outside 0-255 is not rejected: it is limited to 0-255.

On STEP400 in the current mode only the stored setting changes; [`/setVoltageMode`](voltage-and-current-mode-settings.md#setvoltagemode) writes it to the registers.

#### Initial value

- `holdKVAL`: 0 ([voltageMode.KVAL_HOLD](../connections/configuration-items.md#voltagemode-kval_hold))
- `runKVAL`: 16 ([voltageMode.KVAL_RUN](../connections/configuration-items.md#voltagemode-kval_run))
- `accKVAL`: 16 ([voltageMode.KVAL_ACC](../connections/configuration-items.md#voltagemode-kval_acc))
- `decKVAL`: 16 ([voltageMode.KVAL_DEC](../connections/configuration-items.md#voltagemode-kval_dec))

#### See also

[`/getKval`](voltage-and-current-mode-settings.md#getkval), [`/setHoldKval`](voltage-and-current-mode-settings.md#setholdkval), [`/setRunKval`](voltage-and-current-mode-settings.md#setrunkval), [`/setAccKval`](voltage-and-current-mode-settings.md#setacckval), [`/setDecKval`](voltage-and-current-mode-settings.md#setdeckval)
<!-- generated:end osc /setKval -->

<!-- osc: /getKval -->
<!-- generated:begin osc /getKval -->
### `/getKval` (int)motorID {#getkval}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Get the four KVALs together.

With the electromagnetic brake enabled and the voltage mode, KVAL_HOLD is raised to at least half of KVAL_RUN whenever the motor is energized again (from engaged, engaging or after [`/free`](brake.md#free)), and this command returns the raised value. In the current mode TVAL_HOLD is raised instead.

#### Changes

- **v2.2.0**: Returns the settings (what [`/setKval`](voltage-and-current-mode-settings.md#setkval) sets and `/saveConfig` saves) instead of the driver registers. In the current mode the KVAL registers keep the value from before; in the voltage mode they are the registers. KVAL_HOLD raised for a motor with the electromagnetic brake is returned too. STEP800: the reply is the same as before.

#### Response

```
/kval (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)decKVAL
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| holdKVAL | int | 0-255 | KVAL when stopped |
| runKVAL | int | 0-255 | KVAL in constant speed operation |
| accKVAL | int | 0-255 | KVAL during acceleration |
| decKVAL | int | 0-255 | KVAL during deceleration |
<!-- generated:end osc /getKval -->

<!-- osc: /setBemfParam -->
<!-- generated:begin osc /setBemfParam -->
### `/setBemfParam` (int)motorID (int)INT_SPEED (int)ST_SLP (int)FN_SLP_ACC (int)FN_SLP_DEC {#setbemfparam}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| INT_SPEED | int | 0-16383 | INT_SPEED register value |
| ST_SLP | int | 0-255 | ST_SLP register value |
| FN_SLP_ACC | int | 0-255 | FN_SLP_ACC register value |
| FN_SLP_DEC | int | 0-255 | FN_SLP_DEC register value |

#### Executable timing

High Z state

#### Description

Sets BEMF compensation parameter register. For the values for each parameter, refer voltage mode and current mode.

The outputs must be HiZ; otherwise `MotorNotHiZ` is replied and nothing is applied.

A value outside the range is not rejected: INT_SPEED is limited to 0-16383 and the other parameters to 0-255.

#### Changes

- **v2.2.0**: The outputs must be HiZ (INT_SPEED, ST_SLP, FN_SLP_ACC and FN_SLP_DEC are writable only in HiZ); otherwise `/error/command MotorNotHiZ` and nothing is applied.

#### Errors

- `MotorNotHiZ`: The command writes a driver register that can be written only while the outputs are HiZ, and the motor is not HiZ. A motor holding its position is not HiZ: send `/softHiZ` or `/hardHiZ` first. Nothing is applied. Added in v2.2.0.

#### Initial value

- `INT_SPEED`: 1032 ([voltageMode.INT_SPEED](../connections/configuration-items.md#voltagemode-int_speed))
- `ST_SLP`: 25 ([voltageMode.ST_SLP](../connections/configuration-items.md#voltagemode-st_slp))
- `FN_SLP_ACC`: 41 ([voltageMode.FN_SLP_ACC](../connections/configuration-items.md#voltagemode-fn_slp_acc))
- `FN_SLP_DEC`: 41 ([voltageMode.FN_SLP_DEC](../connections/configuration-items.md#voltagemode-fn_slp_dec))

#### See also

[`/getBemfParam`](voltage-and-current-mode-settings.md#getbemfparam)
<!-- generated:end osc /setBemfParam -->

<!-- osc: /getBemfParam -->
<!-- generated:begin osc /getBemfParam -->
### `/getBemfParam` (int)motorID {#getbemfparam}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Get register values for the BEMF parameter.

#### Response

```
/bemfParam (int)motorID (int)INT_SPEED (int)ST_SLP (int)FN_SLP_ACC (int)FN_SLP_DEC
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| INT_SPEED | int | 0-16383 | INT_SPEED register value |
| ST_SLP | int | 0-255 | ST_SLP register value |
| FN_SLP_ACC | int | 0-255 | FN_SLP_ACC register value |
| FN_SLP_DEC | int | 0-255 | FN_SLP_DEC register value |
<!-- generated:end osc /getBemfParam -->

<!-- osc: /setHoldKval -->
<!-- generated:begin osc /setHoldKval -->
### `/setHoldKval` (int)motorID (int)holdKVAL {#setholdkval}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| holdKVAL | int | 0-255 | KVAL when stopped |

#### Executable timing

Always

#### Description

Sets only the hold KVAL value.

A value outside 0-255 is not rejected: it is limited to 0-255.

On STEP400 in the current mode only the stored setting changes; [`/setVoltageMode`](voltage-and-current-mode-settings.md#setvoltagemode) writes it to the registers.

#### Initial value

- `holdKVAL`: 0 ([voltageMode.KVAL_HOLD](../connections/configuration-items.md#voltagemode-kval_hold))

#### See also

[`/setKval`](voltage-and-current-mode-settings.md#setkval)
<!-- generated:end osc /setHoldKval -->

<!-- osc: /setRunKval -->
<!-- generated:begin osc /setRunKval -->
### `/setRunKval` (int)motorID (int)runKVAL {#setrunkval}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| runKVAL | int | 0-255 | KVAL in constant speed operation |

#### Executable timing

Always

#### Description

Sets only the run KVAL value.

A value outside 0-255 is not rejected: it is limited to 0-255.

On STEP400 in the current mode only the stored setting changes; [`/setVoltageMode`](voltage-and-current-mode-settings.md#setvoltagemode) writes it to the registers.

#### Initial value

- `runKVAL`: 16 ([voltageMode.KVAL_RUN](../connections/configuration-items.md#voltagemode-kval_run))

#### See also

[`/setKval`](voltage-and-current-mode-settings.md#setkval)
<!-- generated:end osc /setRunKval -->

<!-- osc: /setAccKval -->
<!-- generated:begin osc /setAccKval -->
### `/setAccKval` (int)motorID (int)accKVAL {#setacckval}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| accKVAL | int | 0-255 | KVAL during acceleration |

#### Executable timing

Always

#### Description

Sets only the acceleration KVAL value.

A value outside 0-255 is not rejected: it is limited to 0-255.

On STEP400 in the current mode only the stored setting changes; [`/setVoltageMode`](voltage-and-current-mode-settings.md#setvoltagemode) writes it to the registers.

#### Initial value

- `accKVAL`: 16 ([voltageMode.KVAL_ACC](../connections/configuration-items.md#voltagemode-kval_acc))

#### See also

[`/setKval`](voltage-and-current-mode-settings.md#setkval)
<!-- generated:end osc /setAccKval -->

<!-- osc: /setDecKval -->
<!-- generated:begin osc /setDecKval -->
### `/setDecKval` (int)motorID (int)decKVAL {#setdeckval}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| decKVAL | int | 0-255 | KVAL during deceleration |

#### Executable timing

Always

#### Description

Sets only the deceleration KVAL value.

A value outside 0-255 is not rejected: it is limited to 0-255.

On STEP400 in the current mode only the stored setting changes; [`/setVoltageMode`](voltage-and-current-mode-settings.md#setvoltagemode) writes it to the registers.

#### Initial value

- `decKVAL`: 16 ([voltageMode.KVAL_DEC](../connections/configuration-items.md#voltagemode-kval_dec))

#### See also

[`/setKval`](voltage-and-current-mode-settings.md#setkval)
<!-- generated:end osc /setDecKval -->

## Current mode

<!-- osc: /setCurrentMode -->
<!-- generated:begin osc /setCurrentMode -->
### `/setCurrentMode` (int)motorID {#setcurrentmode}

Available on STEP400 only.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

High Z state

#### Description

Switches the specified motor to the current drive mode.

The PowerSTEP01 current mode goes up to 1/16 microsteps: a finer microstep mode is lowered to 1/16, and the stored setting ([`/setMicrostepMode`](motor-driver-settings.md#setmicrostepmode), `driverSettings.stepMode`) is changed with it.

#### Changes

- **v2.2.0**: The outputs must be HiZ; otherwise `/error/command MotorNotHiZ` is replied and nothing is applied.
- **v2.2.0**: The mode is changed only if the driver took it (STEP_MODE is read back); otherwise `/error/command CommandIgnored`. Before, the stored mode was changed while the driver kept the old one, so [`/setKval`](voltage-and-current-mode-settings.md#setkval) and [`/setTval`](voltage-and-current-mode-settings.md#settval) then wrote the wrong registers.

#### Errors

- `MotorNotHiZ`: The command writes a driver register that can be written only while the outputs are HiZ, and the motor is not HiZ. A motor holding its position is not HiZ: send `/softHiZ` or `/hardHiZ` first. Nothing is applied. Added in v2.2.0.
- `CommandIgnored`: The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`).

#### See also

[`/setVoltageMode`](voltage-and-current-mode-settings.md#setvoltagemode), [`/setMicrostepMode`](motor-driver-settings.md#setmicrostepmode)
<!-- generated:end osc /setCurrentMode -->

<!-- osc: /setTval -->
<!-- generated:begin osc /setTval -->
### `/setTval` (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL {#settval}

Available on STEP400 only.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| holdTVAL | int | 0-64 | TVAL when stopped |
| runTVAL | int | 0-64 | TVAL in constant speed operation |
| accTVAL | int | 0-64 | TVAL during acceleration |
| decTVAL | int | 0-64 | TVAL during deceleration |

#### Executable timing

Always

#### Description

Sets the four TVALs together.  
In STEP400, the TVAL is as follows.

A value outside 0-64 is not rejected: it is limited to 0-64. The upper limit 64 (about 5 A) is a safety limit of the firmware.

In the voltage mode only the stored setting changes; [`/setCurrentMode`](voltage-and-current-mode-settings.md#setcurrentmode) writes it to the registers.

#### Initial value

- `holdTVAL`: 0 (78.125mA) ([currentMode.TVAL_HOLD](../connections/configuration-items.md#currentmode-tval_hold))
- `runTVAL`: 16 (1.328125A) ([currentMode.TVAL_RUN](../connections/configuration-items.md#currentmode-tval_run))
- `accTVAL`: 16 (1.328125A) ([currentMode.TVAL_ACC](../connections/configuration-items.md#currentmode-tval_acc))
- `decTVAL`: 16 (1.328125A) ([currentMode.TVAL_DEC](../connections/configuration-items.md#currentmode-tval_dec))

| TVAL | Setting value[mA] |
| --- | --- |
| 0 | 78mA |
| 1 | 156mA |
| ... | ... |
| 127 | 9,984mA |

#### See also

[`/getTval`](voltage-and-current-mode-settings.md#gettval), [`/getTval_mA`](voltage-and-current-mode-settings.md#gettval_ma), [`/setHoldTval`](voltage-and-current-mode-settings.md#setholdtval), [`/setRunTval`](voltage-and-current-mode-settings.md#setruntval), [`/setAccTval`](voltage-and-current-mode-settings.md#setacctval), [`/setDecTval`](voltage-and-current-mode-settings.md#setdectval)
<!-- generated:end osc /setTval -->

<!-- osc: /getTval -->
<!-- generated:begin osc /getTval -->
### `/getTval` (int)motorID {#gettval}

Available on STEP400 only.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Get the four TVAL types together.

With the electromagnetic brake enabled and the current mode, TVAL_HOLD is raised to at least half of TVAL_RUN whenever the motor is energized again (from engaged, engaging or after [`/free`](brake.md#free)), and this command returns the raised value. In the voltage mode KVAL_HOLD is raised instead.

#### Changes

- **v2.2.0**: Returns the settings (what [`/setTval`](voltage-and-current-mode-settings.md#settval) sets and `/saveConfig` saves) instead of the driver registers. In the voltage mode the TVAL registers keep the value from before. TVAL_HOLD raised for a motor with the electromagnetic brake is returned too.

#### Response

Available on STEP400 only.

```
/tval (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| holdTVAL | int | 0-64 | TVAL when stopped |
| runTVAL | int | 0-64 | TVAL in constant speed operation |
| accTVAL | int | 0-64 | TVAL during acceleration |
| decTVAL | int | 0-64 | TVAL during deceleration |

#### See also

[`/getTval_mA`](voltage-and-current-mode-settings.md#gettval_ma)
<!-- generated:end osc /getTval -->

<!-- osc: /getTval_mA -->
<!-- generated:begin osc /getTval_mA -->
### `/getTval_mA` (int)motorID {#gettval_ma}

Available on STEP400 only.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Get the four TVAL types together. Not in register values but in the actual current values in [mA].

#### Changes

- **v2.2.0**: Returns the settings (what [`/setTval`](voltage-and-current-mode-settings.md#settval) sets and `/saveConfig` saves) instead of the driver registers. In the voltage mode the TVAL registers keep the value from before. TVAL_HOLD raised for a motor with the electromagnetic brake is returned too.

#### Response

Available on STEP400 only.

```
/tval_mA (int)motorID (float)holdTVAL_mA (float)runTVAL_mA (float)accTVAL_mA (float)decTVAL_mA
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| holdTVAL_mA | float | 78.125-5078.12 mA | TVAL when stopped |
| runTVAL_mA | float | 78.125-5078.12 mA | TVAL in constant speed operation |
| accTVAL_mA | float | 78.125-5078.12 mA | TVAL during acceleration |
| decTVAL_mA | float | 78.125-5078.12 mA | TVAL during deceleration |

#### See also

[`/getTval`](voltage-and-current-mode-settings.md#gettval)
<!-- generated:end osc /getTval_mA -->

<!-- osc: /setDecayModeParam -->
<!-- generated:begin osc /setDecayModeParam -->
### `/setDecayModeParam` (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN {#setdecaymodeparam}

Available on STEP400 only.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| T_FAST | int | 0-255 | T_FAST register value |
| TON_MIN | int | 0-127 | TON_MIN register value |
| TOFF_MIN | int | 0-127 | TOFF_MIN register value |

#### Executable timing

High Z state

#### Description

Sets registers for the current control algorithm parameters. For the each register values, refer the datasheet of the PowerSTEP01.

The outputs must be HiZ; otherwise `MotorNotHiZ` is replied and nothing is applied.

TON_MIN and TOFF_MIN are 7 bit (0-127): a value outside it replies `CommandIgnored` and nothing is applied. A T_FAST outside 0-255 is limited to 0-255.

#### Changes

- **v2.2.0**: TON_MIN and TOFF_MIN are 0-127 (7 bit); a value outside it replies `/error/command CommandIgnored` and nothing is applied. Before, 128-255 were taken modulo 128 by the driver while the saved value stayed 128-255. T_FAST is 0-255 as before.
- **v2.2.0**: The outputs must be HiZ; otherwise `/error/command MotorNotHiZ` and nothing is applied.

#### Errors

- `MotorNotHiZ`: The command writes a driver register that can be written only while the outputs are HiZ, and the motor is not HiZ. A motor holding its position is not HiZ: send `/softHiZ` or `/hardHiZ` first. Nothing is applied. Added in v2.2.0.
- `CommandIgnored`: The command is currently not executable. Also refer Timing section. Also sent when a value is outside the range of the command; nothing is applied (the motor ID is 255 for `/setPositionListReportInterval`).

#### Initial value

- `T_FAST`: 25 ([currentMode.T_FAST](../connections/configuration-items.md#currentmode-t_fast))
- `TON_MIN`: 41 ([currentMode.TON_MIN](../connections/configuration-items.md#currentmode-ton_min))
- `TOFF_MIN`: 41 ([currentMode.TOFF_MIN](../connections/configuration-items.md#currentmode-toff_min))

#### See also

[`/getDecayModeParam`](voltage-and-current-mode-settings.md#getdecaymodeparam)
<!-- generated:end osc /setDecayModeParam -->

<!-- osc: /getDecayModeParam -->
<!-- generated:begin osc /getDecayModeParam -->
### `/getDecayModeParam` (int)motorID {#getdecaymodeparam}

Available on STEP400 only.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Retrieves the register values for the current control algorithm parameters.

#### Response

Available on STEP400 only.

```
/decayModeParam (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| T_FAST | int | 0-255 | T_FAST register value |
| TON_MIN | int | 0-127 | TON_MIN register value |
| TOFF_MIN | int | 0-127 | TOFF_MIN register value |
<!-- generated:end osc /getDecayModeParam -->

<!-- osc: /setHoldTval -->
<!-- generated:begin osc /setHoldTval -->
### `/setHoldTval` (int)motorID (int)holdTVAL {#setholdtval}

Available on STEP400 only.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| holdTVAL | int | 0-64 | TVAL when stopped |

#### Executable timing

Always

#### Description

Sets only the hold TVAL value.

A value outside 0-64 is not rejected: it is limited to 0-64. The upper limit 64 (about 5 A) is a safety limit of the firmware.

In the voltage mode only the stored setting changes; [`/setCurrentMode`](voltage-and-current-mode-settings.md#setcurrentmode) writes it to the registers.

#### Initial value

- `holdTVAL`: 0 (78.125mA) ([currentMode.TVAL_HOLD](../connections/configuration-items.md#currentmode-tval_hold))

#### See also

[`/setTval`](voltage-and-current-mode-settings.md#settval)
<!-- generated:end osc /setHoldTval -->

<!-- osc: /setRunTval -->
<!-- generated:begin osc /setRunTval -->
### `/setRunTval` (int)motorID (int)runTVAL {#setruntval}

Available on STEP400 only.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| runTVAL | int | 0-64 | TVAL in constant speed operation |

#### Executable timing

Always

#### Description

Sets only the run TVAL value.

A value outside 0-64 is not rejected: it is limited to 0-64. The upper limit 64 (about 5 A) is a safety limit of the firmware.

In the voltage mode only the stored setting changes; [`/setCurrentMode`](voltage-and-current-mode-settings.md#setcurrentmode) writes it to the registers.

#### Initial value

- `runTVAL`: 16 (1.328125A) ([currentMode.TVAL_RUN](../connections/configuration-items.md#currentmode-tval_run))

#### See also

[`/setTval`](voltage-and-current-mode-settings.md#settval)
<!-- generated:end osc /setRunTval -->

<!-- osc: /setAccTval -->
<!-- generated:begin osc /setAccTval -->
### `/setAccTval` (int)motorID (int)accTVAL {#setacctval}

Available on STEP400 only.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| accTVAL | int | 0-64 | TVAL during acceleration |

#### Executable timing

Always

#### Description

Sets only the acceleration TVAL value.

A value outside 0-64 is not rejected: it is limited to 0-64. The upper limit 64 (about 5 A) is a safety limit of the firmware.

In the voltage mode only the stored setting changes; [`/setCurrentMode`](voltage-and-current-mode-settings.md#setcurrentmode) writes it to the registers.

#### Initial value

- `accTVAL`: 16 (1.328125A) ([currentMode.TVAL_ACC](../connections/configuration-items.md#currentmode-tval_acc))

#### See also

[`/setTval`](voltage-and-current-mode-settings.md#settval)
<!-- generated:end osc /setAccTval -->

<!-- osc: /setDecTval -->
<!-- generated:begin osc /setDecTval -->
### `/setDecTval` (int)motorID (int)decTVAL {#setdectval}

Available on STEP400 only.

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| decTVAL | int | 0-64 | TVAL during deceleration |

#### Executable timing

Always

#### Description

Sets only the deceleration TVAL value.

A value outside 0-64 is not rejected: it is limited to 0-64. The upper limit 64 (about 5 A) is a safety limit of the firmware.

In the voltage mode only the stored setting changes; [`/setCurrentMode`](voltage-and-current-mode-settings.md#setcurrentmode) writes it to the registers.

#### Initial value

- `decTVAL`: 16 (1.328125A) ([currentMode.TVAL_DEC](../connections/configuration-items.md#currentmode-tval_dec))

#### See also

[`/setTval`](voltage-and-current-mode-settings.md#settval)
<!-- generated:end osc /setDecTval -->
