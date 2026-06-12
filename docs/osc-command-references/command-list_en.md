---
title: Command list
slug: command-list
lang: en
parent: 886
menu_order: 21
---

# Command list

This page provides a quick reference of all OSC (Open Sound Control) commands. Click the command name to go to the detailed documentation. Commands marked with **v2.1.0** were added in firmware v2.1.0.

Direction: **→** = sent to the device, **←** = sent from the device.

## System & Network

| Command | Dir | Arguments | STEP400 | STEP800 |
|---------|:---:|-----------|:-------:|:-------:|
| [/setDestIp](system-settings.md) | → | — | ✓ | ✓ |
| [/getVersion](system-settings.md) | → | — | ✓ | ✓ |
| [/getConfigName](system-settings.md) | → | — | ✓ | ✓ |
| [/setConfigName](system-settings.md) | → | (Symbol)configName | ✓ | ✓ |
| [/saveConfig](system-settings.md) | → | — | ✓ | ✓ |
| [/reportError](system-settings.md) | → | (bool)enable | ✓ | ✓ |
| [/resetDevice](system-settings.md) | → | — | ✓ | ✓ |

## Configuration & Reporting

| Command | Dir | Arguments | STEP400 | STEP800 |
|---------|:---:|-----------|:-------:|:-------:|
| [/enableBusyReport](motor-driver-settings.md) | → | (int)motorID (bool)enable | ✓ | ✓ |
| [/enableHizReport](motor-driver-settings.md) | → | (int)motorID (bool)enable | ✓ | ✓ |
| [/enableDirReport](motor-driver-settings.md) | → | (int)motorID (bool)enable | ✓ | ✓ |
| [/enableMotorStatusReport](motor-driver-settings.md) | → | (int)motorID (bool)enable | ✓ | ✓ |
| [/enableHomeSwReport](home-and-limit-sensors.md) | → | (int)motorID (bool)enable | ✓ | ✓ |
| [/enableSwEventReport](home-and-limit-sensors.md) | → | (int)motorID (bool)enable | ✓ | ✓ |
| [/enableLimitSwReport](home-and-limit-sensors.md) | → | (int)motorID (bool)enable | ✓ | |
| [/setPositionReportInterval](motor-driver-settings.md) | → | (int)motorID (int)interval | ✓ | ✓ |
| [/setPositionListReportInterval](motor-driver-settings.md) | → | (int)interval | ✓ | ✓ |
| [/enableUvloReport](alarm-settings.md) | → | (int)motorID (bool)enable | ✓ | ✓ |
| [/enableThermalStatusReport](alarm-settings.md) | → | (int)motorID (bool)enable | ✓ | ✓ |
| [/enableOverCurrentReport](alarm-settings.md) | → | (int)motorID (bool)enable | ✓ | ✓ |
| [/enableStallReport](alarm-settings.md) | → | (int)motorID (bool)enable | ✓ | ✓ |

## Motor Driver Setup

| Command | Dir | Arguments | STEP400 | STEP800 |
|---------|:---:|-----------|:-------:|:-------:|
| [/setMicrostepMode](motor-driver-settings.md) | → | (int)motorID (int)STEP_SEL | ✓ | ✓ |
| [/getMicrostepMode](motor-driver-settings.md) | → | (int)motorID | ✓ | ✓ |
| [/enableLowSpeedOptimize](motor-driver-settings.md) | → | (int)motorID (bool)enable | ✓ | ✓ |
| [/setLowSpeedOptimizeThreshold](motor-driver-settings.md) | → | (int)motorID (float)threshold | ✓ | ✓ |
| [/getLowSpeedOptimizeThreshold](motor-driver-settings.md) | → | (int)motorID | ✓ | ✓ |
| [/setBemfParam](voltage-and-current-mode-settings.md) | → | (int)motorID (int)INT_SPEED (int)ST_SLP (int)FN_SLP_ACC (int)FN_SLP_DEC | ✓ | ✓ |
| [/getBemfParam](voltage-and-current-mode-settings.md) | → | (int)motorID | ✓ | ✓ |
| [/setDecayModeParam](voltage-and-current-mode-settings.md) | → | (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN | ✓ | |
| [/getDecayModeParam](voltage-and-current-mode-settings.md) | → | (int)motorID | ✓ | |
| [/resetMotorDriver](motor-driver-settings.md) | → | (int)motorID | ✓ | ✓ |

## Voltage / Current Mode

| Command | Dir | Arguments | STEP400 | STEP800 |
|---------|:---:|-----------|:-------:|:-------:|
| [/setVoltageMode](voltage-and-current-mode-settings.md) | → | (int)motorID | ✓ | |
| [/setCurrentMode](voltage-and-current-mode-settings.md) | → | (int)motorID | ✓ | |
| [/setKval](voltage-and-current-mode-settings.md) | → | (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)decKVAL | ✓ | ✓ |
| [/setHoldKval](voltage-and-current-mode-settings.md) | → | (int)motorID (int)holdKVAL | ✓ | ✓ |
| [/setRunKval](voltage-and-current-mode-settings.md) | → | (int)motorID (int)runKVAL | ✓ | ✓ |
| [/setAccKval](voltage-and-current-mode-settings.md) | → | (int)motorID (int)accKVAL | ✓ | ✓ |
| [/setDecKval](voltage-and-current-mode-settings.md) | → | (int)motorID (int)decKVAL | ✓ | ✓ |
| [/getKval](voltage-and-current-mode-settings.md) | → | (int)motorID | ✓ | ✓ |
| [/setTval](voltage-and-current-mode-settings.md) | → | (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL | ✓ | |
| [/setHoldTval](voltage-and-current-mode-settings.md) | → | (int)motorID (int)holdTVAL | ✓ | |
| [/setRunTval](voltage-and-current-mode-settings.md) | → | (int)motorID (int)runTVAL | ✓ | |
| [/setAccTval](voltage-and-current-mode-settings.md) | → | (int)motorID (int)accTVAL | ✓ | |
| [/setDecTval](voltage-and-current-mode-settings.md) | → | (int)motorID (int)decTVAL | ✓ | |
| [/getTval](voltage-and-current-mode-settings.md) | → | (int)motorID | ✓ | |
| [/getTval_mA](voltage-and-current-mode-settings.md) | → | (int)motorID | ✓ | |

## Speed & Acceleration

| Command | Dir | Arguments | STEP400 | STEP800 |
|---------|:---:|-----------|:-------:|:-------:|
| [/setSpeedProfile](speed-profile.md) | → | (int)motorID (float)acc (float)dec (float)maxSpeed | ✓ | ✓ |
| [/getSpeedProfile](speed-profile.md) | → | (int)motorID | ✓ | ✓ |
| [/setMaxSpeed](speed-profile.md) | → | (int)motorID (float)maxSpeed | ✓ | ✓ |
| [/setMinSpeed](speed-profile.md) | → | (int)motorID (float)minSpeed | ✓ | ✓ |
| [/getMinSpeed](speed-profile.md) | → | (int)motorID | ✓ | ✓ |
| [/setFullstepSpeed](speed-profile.md) | → | (int)motorID (float)fullstepSpeed | ✓ | ✓ |
| [/getFullstepSpeed](speed-profile.md) | → | (int)motorID | ✓ | ✓ |
| [/setAcc](speed-profile.md) | → | (int)motorID (float)acc | ✓ | ✓ |
| [/setDec](speed-profile.md) | → | (int)motorID (float)dec | ✓ | ✓ |
| [/getSpeed](speed-profile.md) | → | (int)motorID | ✓ | ✓ |
| [/setSpeedProfileRaw](speed-profile.md) | → | (int)motorID (int)acc (int)dec (int)maxSpeed | ✓ | ✓ |
| [/getSpeedProfileRaw](speed-profile.md) | → | (int)motorID | ✓ | ✓ |
| [/setMaxSpeedRaw](speed-profile.md) | → | (int)motorID (int)maxSpeed | ✓ | ✓ |
| [/setMinSpeedRaw](speed-profile.md) | → | (int)motorID (int)minSpeed | ✓ | ✓ |
| [/setFullstepSpeedRaw](speed-profile.md) | → | (int)motorID (int)fullstepSpeed | ✓ | ✓ |
| [/setAccRaw](speed-profile.md) | → | (int)motorID (int)acc | ✓ | ✓ |
| [/setDecRaw](speed-profile.md) | → | (int)motorID (int)dec | ✓ | ✓ |

## Motion Commands

| Command | Dir | Arguments | STEP400 | STEP800 |
|---------|:---:|-----------|:-------:|:-------:|
| [/run](motor-control.md) | → | (int)motorID (float)speed | ✓ | ✓ |
| [/move](motor-control.md) | → | (int)motorID (int)step | ✓ | ✓ |
| [/goTo](motor-control.md) | → | (int)motorID (int)position | ✓ | ✓ |
| [/goToDir](motor-control.md) | → | (int)motorID (bool)DIR (int)position | ✓ | ✓ |
| [/goHome](position-management.md) | → | (int)motorID | ✓ | ✓ |
| [/goMark](position-management.md) | → | (int)motorID | ✓ | ✓ |
| [/softStop](motor-control.md) | → | (int)motorID | ✓ | ✓ |
| [/hardStop](motor-control.md) | → | (int)motorID | ✓ | ✓ |
| [/softHiZ](motor-control.md) | → | (int)motorID | ✓ | ✓ |
| [/hardHiZ](motor-control.md) | → | (int)motorID | ✓ | ✓ |
| [/runRaw](motor-control.md) | → | (int)motorID (int)speed | ✓ | ✓ |
| [/goUntilRaw](motor-control.md) | → | (int)motorID (bool)ACT (int)speed | ✓ | ✓ |

## Combined (Multi-Motor)

| Command | Dir | Arguments | STEP400 | STEP800 |
|---------|:---:|-----------|:-------:|:-------:|
| [/combinedRun](motor-control.md) | → | (float)speed1 ... speedN | ✓ | ✓ |
| [/combinedMove](motor-control.md) | → | (int)step1 ... stepN | ✓ | ✓ |
| [/combinedGoTo](motor-control.md) | → | (int)position1 ... positionN | ✓ | ✓ |
| [/combinedGoToDir](motor-control.md) | → | (bool)DIR1 (int)pos1 ... | ✓ | ✓ |
| [/combinedSoftStop](motor-control.md) | → | — | ✓ | ✓ |
| [/combinedHardStop](motor-control.md) | → | — | ✓ | ✓ |
| [/combinedSoftHiZ](motor-control.md) | → | — | ✓ | ✓ |
| [/combinedHardHiZ](motor-control.md) | → | — | ✓ | ✓ |
| [/combinedRunRaw](motor-control.md) | → | (int)speed1 ... speedN | ✓ | ✓ |

## Homing & Switches

| Command | Dir | Arguments | STEP400 | STEP800 |
|---------|:---:|-----------|:-------:|:-------:|
| [/homing](homing.md) | → | (int)motorID | ✓ | ✓ |
| [/getHomingStatus](homing.md) | → | (int)motorID | ✓ | ✓ |
| [/setHomingDirection](homing.md) | → | (int)motorID (bool)direction | ✓ | ✓ |
| [/getHomingDirection](homing.md) | → | (int)motorID | ✓ | ✓ |
| [/setHomingSpeed](homing.md) | → | (int)motorID (float)speed | ✓ | ✓ |
| [/getHomingSpeed](homing.md) | → | (int)motorID | ✓ | ✓ |
| [/goUntil](homing.md) | → | (int)motorID (bool)ACT (float)speed | ✓ | ✓ |
| [/releaseSw](homing.md) | → | (int)motorID (bool)ACT (bool)DIR | ✓ | ✓ |
| [/setGoUntilTimeout](homing.md) | → | (int)motorID (int)timeOut | ✓ | ✓ |
| [/getGoUntilTimeout](homing.md) | → | (int)motorID | ✓ | ✓ |
| [/setReleaseSwTimeout](homing.md) | → | (int)motorID (int)timeOut | ✓ | ✓ |
| [/getHomeSw](home-and-limit-sensors.md) | → | (int)motorID | ✓ | ✓ |
| [/getLimitSw](home-and-limit-sensors.md) | → | (int)motorID | ✓ | |
| [/setHomeSwMode](home-and-limit-sensors.md) | → | (int)motorID (bool)SW_MODE | ✓ | ✓ |
| [/getHomeSwMode](home-and-limit-sensors.md) | → | (int)motorID | ✓ | ✓ |
| [/setLimitSwMode](home-and-limit-sensors.md) | → | (int)motorID (bool)SW_MODE | ✓ | |
| [/getLimitSwMode](home-and-limit-sensors.md) | → | (int)motorID | ✓ | |
| [/setProhibitMotionOnHomeSw](alarm-settings.md) | → | (int)motorID (bool)enable | ✓ | ✓ |
| [/getProhibitMotionOnHomeSw](alarm-settings.md) | → | (int)motorID | ✓ | ✓ |
| [/setProhibitMotionOnLimitSw](alarm-settings.md) | → | (int)motorID (bool)enable | ✓ | |
| [/getProhibitMotionOnLimitSw](alarm-settings.md) | → | (int)motorID | ✓ | |

## Position

| Command | Dir | Arguments | STEP400 | STEP800 |
|---------|:---:|-----------|:-------:|:-------:|
| [/getPosition](position-management.md) | → | (int)motorID | ✓ | ✓ |
| [/getPositionList](position-management.md) | → | — | ✓ | ✓ |
| [/setPosition](position-management.md) | → | (int)motorID (int)newPosition | ✓ | ✓ |
| [/resetPos](position-management.md) | → | (int)motorID | ✓ | ✓ |
| [/setElPos](position-management.md) | → | (int)motorID (int)newFullstep (int)newMicrostep | ✓ | ✓ |
| [/getElPos](position-management.md) | → | (int)motorID | ✓ | ✓ |
| [/setMark](position-management.md) | → | (int)motorID (int)MARK | ✓ | ✓ |
| [/getMark](position-management.md) | → | (int)motorID | ✓ | ✓ |

## Servo Mode

| Command | Dir | Arguments | STEP400 | STEP800 |
|---------|:---:|-----------|:-------:|:-------:|
| [/enableServoMode](servo-mode_reference.md) | → | (int)motorID (bool)enable | ✓ | ✓ |
| [/setServoParam](servo-mode_reference.md) | → | (int)motorID (float)kP (float)kI (float)kD | ✓ | ✓ |
| [/getServoParam](servo-mode_reference.md) | → | (int)motorID | ✓ | ✓ |
| [/setTargetPosition](servo-mode_reference.md) | → | (int)motorID (int)position | ✓ | ✓ |
| [/setTargetPositionList](servo-mode_reference.md) | → | (int)position1 ... positionN | ✓ | ✓ |

## Electromagnetic Brake

| Command | Dir | Arguments | STEP400 | STEP800 |
|---------|:---:|-----------|:-------:|:-------:|
| [/enableElectromagnetBrake](brake.md) | → | (int)motorID (bool)enable | ✓ | ✓ |
| [/activate](brake.md) | → | (int)motorID (bool)state | ✓ | ✓ |
| [/free](brake.md) | → | (int)motorID | ✓ | ✓ |
| [/setBrakeTransitionDuration](brake.md) | → | (int)motorID (int)duration | ✓ | ✓ |
| [/getBrakeTransitionDuration](brake.md) | → | (int)motorID | ✓ | ✓ |

## Alarm Settings

| Command | Dir | Arguments | STEP400 | STEP800 |
|---------|:---:|-----------|:-------:|:-------:|
| [/setOverCurrentThreshold](alarm-settings.md) | → | (int)motorID (int)OCD_TH | ✓ | ✓ |
| [/getOverCurrentThreshold](alarm-settings.md) | → | (int)motorID | ✓ | ✓ |
| [/setStallThreshold](alarm-settings.md) | → | (int)motorID (int)STALL_TH | ✓ | ✓ |
| [/getStallThreshold](alarm-settings.md) | → | (int)motorID | ✓ | ✓ |

## Status Queries

| Command | Dir | Arguments | STEP400 | STEP800 |
|---------|:---:|-----------|:-------:|:-------:|
| [/getBusy](motor-driver-settings.md) | → | (int)motorID | ✓ | ✓ |
| [/getHiZ](motor-driver-settings.md) | → | (int)motorID | ✓ | ✓ |
| [/getDir](motor-driver-settings.md) | → | (int)motorID | ✓ | ✓ |
| [/getMotorStatus](motor-driver-settings.md) | → | (int)motorID | ✓ | ✓ |
| [/getUvlo](alarm-settings.md) | → | (int)motorID | ✓ | ✓ |
| [/getThermalStatus](alarm-settings.md) | → | (int)motorID | ✓ | ✓ |
| [/getStatus](motor-driver-settings.md) | → | (int)motorID | ✓ | ✓ |
| [/getStatusList](motor-driver-settings.md) | → | — | ✓ | ✓ |
| [/getConfigRegister](motor-driver-settings.md) | → | (int)motorID | ✓ | ✓ |
| [/getAdcVal](motor-driver-settings.md) | → | (int)motorID | ✓ | |

## Automatically Sent Messages

| Message | Dir | Arguments | STEP400 | STEP800 |
|---------|:---:|-----------|:-------:|:-------:|
| [/booted](automatically-sent-messages-from-step-400.md) | ← | (int)deviceID | ✓ | ✓ |
| [/error/osc](automatically-sent-messages-from-step-400.md) | ← | (Symbol)errorText | ✓ | ✓ |
| [/error/command](automatically-sent-messages-from-step-400.md) | ← | (Symbol)ErrorText (int)motorID | ✓ | ✓ |
| [/busy](automatically-sent-messages-from-step-400.md) | ← | (int)motorID (bool)state | ✓ | ✓ |
| [/HiZ](automatically-sent-messages-from-step-400.md) | ← | (int)motorID (bool)state | ✓ | ✓ |
| [/dir](automatically-sent-messages-from-step-400.md) | ← | (int)motorID (bool)direction | ✓ | ✓ |
| [/motorStatus](automatically-sent-messages-from-step-400.md) | ← | (int)motorID (int)MOT_STATUS | ✓ | ✓ |
| [/homingStatus](automatically-sent-messages-from-step-400.md) | ← | (int)motorID (int)homingStatus | ✓ | ✓ |
| [/position](automatically-sent-messages-from-step-400.md) | ← | (int)motorID (int)ABS_POS | ✓ | ✓ |
| [/positionList](automatically-sent-messages-from-step-400.md) | ← | (int)pos1 ... posN | ✓ | ✓ |
| [/uvlo](automatically-sent-messages-from-step-400.md) | ← | (int)motorID | ✓ | ✓ |
| [/thermalStatus](automatically-sent-messages-from-step-400.md) | ← | (int)motorID (int)thermalStatus | ✓ | ✓ |
| [/overCurrent](automatically-sent-messages-from-step-400.md) | ← | (int)motorID | ✓ | ✓ |
| [/stall](automatically-sent-messages-from-step-400.md) | ← | (int)motorID | ✓ | ✓ |
| [/swEvent](home-and-limit-sensors.md) | ← | (int)motorID | ✓ | ✓ |
