---
title: Speed profile
---

# Speed profile

For how the speed profile and the motions work, see [Speed profile and motions](../guides/speed-profile-and-motions.md).

<!-- osc: /setSpeedProfile -->
<!-- generated:begin osc /setSpeedProfile -->
### `/setSpeedProfile` (int)motorID (float)acc (float)dec (float)maxSpeed {#setspeedprofile}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| acc | float | 14.55-59575 step/s/s | acceleration |
| dec | float | 14.55-59590 (STEP400), 14.55-59575 (STEP800) step/s/s | deceleration |
| maxSpeed | float | 15.25-15610 step/s | maximum speed |

#### Executable timing

When the motor is stopped

#### Description

Sets the acc, dec, and maxSpeed of the speed profile together.

The speed profile is the set of acceleration, deceleration and maximum speed held in the motor driver. It is not sent with each command: it applies to every motion after it is written ([`/run`](motor-control.md#run), [`/goTo`](motor-control.md#goto) and so on). The minimum speed is set separately with [`/setMinSpeed`](speed-profile.md#setminspeed).

ACC and DEC are rounded to the nearest register value, so the written value can differ by 1 LSB. MAX_SPEED alone is writable at any time, but nothing is written to a motor that replies with `MotorNotStopped`. A value outside the range is limited by the driver library. On STEP400, a maximum speed of 0 is written as 1 (the register value 0 is reserved).

#### Changes

- **v2.2.0**: The motor must be stopped or HiZ; a turning motor replies `/error/command MotorNotStopped` and keeps its old values.
- **v2.2.0**: `acc` and `dec` are rounded to the nearest register value, so the written value can differ by 1 LSB.
- **v2.2.0**: STEP400: a maximum speed of 0 is written as 1 (the register value 0 is reserved).

#### Errors

- `MotorNotStopped`: The command writes a driver register that can be written only while the motor is stopped or HiZ, and the motor is turning. Nothing is applied. Added in v2.2.0.

#### Initial value

- `acc`: 1000 (firmware) / 2000 (template) ([speedProfile.acc](../connections/configuration-items.md#speedprofile-acc))
- `dec`: 1000 (firmware) / 2000 (template) ([speedProfile.dec](../connections/configuration-items.md#speedprofile-dec))
- `maxSpeed`: 650 (firmware) / 620 (template) ([speedProfile.maxSpeed](../connections/configuration-items.md#speedprofile-maxspeed))

#### See also

[`/getSpeedProfile`](speed-profile.md#getspeedprofile), [`/setAcc`](speed-profile.md#setacc), [`/setDec`](speed-profile.md#setdec), [`/setMaxSpeed`](speed-profile.md#setmaxspeed)
<!-- generated:end osc /setSpeedProfile -->

<!-- osc: /getSpeedProfile -->
<!-- generated:begin osc /getSpeedProfile -->
### `/getSpeedProfile` (int)motorID {#getspeedprofile}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Gets the acc, dec, and maxSpeed of the speed profile together.

#### Changes

- **v2.2.0**: The acceleration and deceleration are reported about 4.9% smaller than before; they now match the datasheet (driver libraries v1.2.0).

#### Response

```
/speedProfile (int)motorID (float)acc (float)dec (float)maxSpeed
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| acc | float | 14.55-59590 step/s/s | acceleration |
| dec | float | 14.55-59590 step/s/s | deceleration |
| maxSpeed | float | 15.25-15610 step/s | maximum speed |
<!-- generated:end osc /getSpeedProfile -->

<!-- osc: /setFullstepSpeed -->
<!-- generated:begin osc /setFullstepSpeed -->
### `/setFullstepSpeed` (int)motorID (float)fullstepSpeed {#setfullstepspeed}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| fullstepSpeed | float | 7.63-15625 step/s | threshold |

#### Executable timing

Always

#### Description

Sets the threshold at which the microstepping mode automatically switches to full-step mode.

A value above the range is limited to 15625 step/s by the driver library. A value from 0 up to the lower end of the range is written as the lower end (7.63 step/s). A negative value below about -7.6 is not limited to the lower end: the driver library converts it to a huge unsigned number and limits that to the maximum, so it becomes 15625 step/s.

#### Initial value

- `fullstepSpeed`: 15610 (firmware) / 15625 (template) ([speedProfile.fullStepSpeed](../connections/configuration-items.md#speedprofile-fullstepspeed))

#### See also

[`/getFullstepSpeed`](speed-profile.md#getfullstepspeed)
<!-- generated:end osc /setFullstepSpeed -->

<!-- osc: /getFullstepSpeed -->
<!-- generated:begin osc /getFullstepSpeed -->
### `/getFullstepSpeed` (int)motorID {#getfullstepspeed}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Gets the threshold at which the microstepping mode automatically switches to full-step mode.

#### Response

```
/fullstepSpeed (int)motorID (float)fullstepSpeed
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| fullstepSpeed | float | 7.63-15625 step/s | Threshold |
<!-- generated:end osc /getFullstepSpeed -->

<!-- osc: /setMaxSpeed -->
<!-- generated:begin osc /setMaxSpeed -->
### `/setMaxSpeed` (int)motorID (float)maxSpeed {#setmaxspeed}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| maxSpeed | float | 15.25-15610 step/s | maximum speed |

#### Executable timing

Always

#### Description

Set the maximum speed of the speed profile

A value outside the range is limited by the driver library. On STEP400, a maximum speed of 0 is written as 1 (the register value 0 is reserved).

#### Changes

- **v2.2.0**: STEP400: a maximum speed of 0 is written as 1 (the register value 0 is reserved). STEP800 is unchanged.

#### Initial value

- `maxSpeed`: 650 (firmware) / 620 (template) ([speedProfile.maxSpeed](../connections/configuration-items.md#speedprofile-maxspeed))

#### See also

[`/setSpeedProfile`](speed-profile.md#setspeedprofile)
<!-- generated:end osc /setMaxSpeed -->

<!-- osc: /setAcc -->
<!-- generated:begin osc /setAcc -->
### `/setAcc` (int)motorID (float)acc {#setacc}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| acc | float | 14.55-59575 step/s/s | acceleration |

#### Executable timing

When the motor is stopped

#### Description

Sets the acceleration of the speed profile.

The value is rounded to the nearest register value, so the written value can differ by 1 LSB. A value outside the range is limited by the driver library.

The motor must be stopped or HiZ; a turning motor replies `MotorNotStopped` and keeps its old value.

#### Changes

- **v2.2.0**: The motor must be stopped or HiZ; a turning motor replies `/error/command MotorNotStopped` and keeps its old value.
- **v2.2.0**: Rounds to the nearest register value, so the written value can differ by 1 LSB.

#### Errors

- `MotorNotStopped`: The command writes a driver register that can be written only while the motor is stopped or HiZ, and the motor is turning. Nothing is applied. Added in v2.2.0.

#### Initial value

- `acc`: 1000 (firmware) / 2000 (template) ([speedProfile.acc](../connections/configuration-items.md#speedprofile-acc))

#### See also

[`/setSpeedProfile`](speed-profile.md#setspeedprofile)
<!-- generated:end osc /setAcc -->

<!-- osc: /setDec -->
<!-- generated:begin osc /setDec -->
### `/setDec` (int)motorID (float)dec {#setdec}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| dec | float | 14.55-59590 (STEP400), 14.55-59575 (STEP800) step/s/s | deceleration |

#### Executable timing

When the motor is stopped

#### Description

Sets the deceleration of the speed profile.

The value is rounded to the nearest register value, so the written value can differ by 1 LSB. A value outside the range is limited by the driver library.

The motor must be stopped or HiZ; a turning motor replies `MotorNotStopped` and keeps its old value.

#### Changes

- **v2.2.0**: The motor must be stopped or HiZ; a turning motor replies `/error/command MotorNotStopped` and keeps its old value.
- **v2.2.0**: Rounds to the nearest register value, so the written value can differ by 1 LSB.

#### Errors

- `MotorNotStopped`: The command writes a driver register that can be written only while the motor is stopped or HiZ, and the motor is turning. Nothing is applied. Added in v2.2.0.

#### Initial value

- `dec`: 1000 (firmware) / 2000 (template) ([speedProfile.dec](../connections/configuration-items.md#speedprofile-dec))

#### See also

[`/setSpeedProfile`](speed-profile.md#setspeedprofile)
<!-- generated:end osc /setDec -->

<!-- osc: /setMinSpeed -->
<!-- generated:begin osc /setMinSpeed -->
### `/setMinSpeed` (int)motorID (float)minSpeed {#setminspeed}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| minSpeed | float | 0-976.3 step/s | Minimum speed |

#### Executable timing

When the motor is stopped

#### Description

Set the speed profile minimum speed. This value is also used for the motor speed of [`/releaseSw`](homing.md#releasesw). When Low speed optimization ([`/enableLowSpeedOptimize`](motor-driver-settings.md#enablelowspeedoptimize)) is enabled, the minimum speed of the speed profile is set to zero.

While the low speed optimization is disabled, the motor must be stopped or HiZ; a turning motor replies `MotorNotStopped` and keeps its old value. While it is enabled, only the saved value changes and no error is sent.

A value above the range is limited to 976.3 step/s by the driver library. A negative value below about -0.24 is not limited to 0: the driver library converts it to a huge unsigned number and limits that to the maximum, so it becomes 976.3 step/s.

#### Changes

- **v2.2.0**: While the low speed optimization is disabled, the motor must be stopped or HiZ; a turning motor replies `/error/command MotorNotStopped` and keeps its old value.
- **v2.2.0**: `/setMinSpeed 255` (all motors) checks the low speed optimization setting of each motor. It read an invalid array element.

#### Errors

- `MotorNotStopped`: The command writes a driver register that can be written only while the motor is stopped or HiZ, and the motor is turning. Nothing is applied. Added in v2.2.0.

#### Initial value

- `minSpeed`: 0 ([speedProfile.minSpeed](../connections/configuration-items.md#speedprofile-minspeed))

#### See also

[`/getMinSpeed`](speed-profile.md#getminspeed)
<!-- generated:end osc /setMinSpeed -->

<!-- osc: /getMinSpeed -->
<!-- generated:begin osc /getMinSpeed -->
### `/getMinSpeed` (int)motorID {#getminspeed}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Return the speed profile minimum speed.

Returns 0.0 for a motor with the low speed optimization enabled: the MIN_SPEED register then holds the optimization threshold (read it with [`/getLowSpeedOptimizeThreshold`](motor-driver-settings.md#getlowspeedoptimizethreshold)) and the actual minimum speed is 0. For a motor with the optimization disabled, it returns the MIN_SPEED register value of the driver in step/s.

#### Changes

- **v2.2.0**: Returns 0.0 for a motor with the low speed optimization enabled. A single motor returned the MIN_SPEED register value (the threshold) and `255` (all motors) returned the stored minimum speed setting; both behave the same now.

#### Response

```
/minSpeed (int)motorID (float)minSpeed
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| minSpeed | float | 0-976.3 step/s | Minimum speed |
<!-- generated:end osc /getMinSpeed -->

<!-- osc: /getSpeed -->
<!-- generated:begin osc /getSpeed -->
### `/getSpeed` (int)motorID {#getspeed}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Returns the current motor speed.

#### Response

```
/speed (int)motorID (float)speed
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| speed | float | -15625-15625 step/s | Current speed |
<!-- generated:end osc /getSpeed -->

## Raw register value commands

The following commands set or get the parameters of the speed profile with the register values of the driver IC, without unit conversion. For most users the standard commands, which use physical units, are recommended. These are for advanced use where the registers are controlled directly.

<!-- osc: /setSpeedProfileRaw -->
<!-- generated:begin osc /setSpeedProfileRaw -->
### `/setSpeedProfileRaw` (int)motorID (int)acc (int)dec (int)maxSpeed {#setspeedprofileraw}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| acc | int | 0-4095 | acceleration (raw register value) |
| dec | int | 0-4095 | deceleration (raw register value) |
| maxSpeed | int | 0-1023 | maximum speed (raw register value) |

#### Executable timing

When the motor is stopped

#### Description

Sets the acc, dec, and maxSpeed of the speed profile using raw driver IC register values.

A value outside the range is not rejected: it is converted to 16 bits (70000 becomes 4464) and then masked to the width of the register by the driver. The motor must be stopped or HiZ; a turning motor replies `MotorNotStopped` and keeps its old value.

#### Changes

- **v2.2.0**: Also sets the acceleration, deceleration and maximum speed setting that `/saveConfig` saves and `/resetMotorDriver` applies again. Before, only the register was changed, so a reset or a saved configuration brought back the value from before.
- **v2.2.0**: The motor must be stopped or HiZ; a turning motor replies `/error/command MotorNotStopped` and keeps its old value.

#### Errors

- `MotorNotStopped`: The command writes a driver register that can be written only while the motor is stopped or HiZ, and the motor is turning. Nothing is applied. Added in v2.2.0.

#### See also

[`/getSpeedProfileRaw`](speed-profile.md#getspeedprofileraw), [`/setSpeedProfile`](speed-profile.md#setspeedprofile)
<!-- generated:end osc /setSpeedProfileRaw -->

<!-- osc: /getSpeedProfileRaw -->
<!-- generated:begin osc /getSpeedProfileRaw -->
### `/getSpeedProfileRaw` (int)motorID {#getspeedprofileraw}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |

#### Executable timing

Always

#### Description

Gets the acc, dec, and maxSpeed of the speed profile as raw driver IC register values.

#### Response

```
/speedProfileRaw (int)motorID (int)acc (int)dec (int)maxSpeed
```

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800) | Motor ID |
| acc | int | 0-4095 | acceleration (raw register value) |
| dec | int | 0-4095 | deceleration (raw register value) |
| maxSpeed | int | 0-1023 | maximum speed (raw register value) |
<!-- generated:end osc /getSpeedProfileRaw -->

<!-- osc: /setMaxSpeedRaw -->
<!-- generated:begin osc /setMaxSpeedRaw -->
### `/setMaxSpeedRaw` (int)motorID (int)maxSpeed {#setmaxspeedraw}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| maxSpeed | int | 0-1023 | maximum speed (raw register value) |

#### Executable timing

Always

#### Description

Sets the maximum speed of the speed profile using a raw register value.

A value outside the range is not rejected: it is converted to 16 bits (70000 becomes 4464) and then masked to the width of the register by the driver.

`/setMaxSpeedRaw 0` writes 0, also on STEP400.

#### Changes

- **v2.2.0**: Also sets the maximum speed setting that `/saveConfig` saves and `/resetMotorDriver` applies again. Before, only the register was changed, so a reset or a saved configuration brought back the value from before.

#### See also

[`/setMaxSpeed`](speed-profile.md#setmaxspeed)
<!-- generated:end osc /setMaxSpeedRaw -->

<!-- osc: /setMinSpeedRaw -->
<!-- generated:begin osc /setMinSpeedRaw -->
### `/setMinSpeedRaw` (int)motorID (int)minSpeed {#setminspeedraw}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| minSpeed | int | 0-4095 | minimum speed (raw register value) |

#### Executable timing

When the motor is stopped

#### Description

Sets the minimum speed of the speed profile using a raw register value.

A value outside the range is not rejected: it is converted to 16 bits (70000 becomes 4464) and then masked to the width of the register by the driver. While the low speed optimization is disabled, the motor must be stopped or HiZ; a turning motor replies `MotorNotStopped` and keeps its old value. While it is enabled, only the saved value changes and no error is sent.

#### Changes

- **v2.2.0**: Also sets the minimum speed setting that `/saveConfig` saves and `/resetMotorDriver` applies again. Before, only the register was changed, so a reset or a saved configuration brought back the value from before.
- **v2.2.0**: While the low speed optimization is disabled, the motor must be stopped or HiZ; a turning motor replies `/error/command MotorNotStopped` and keeps its old value.
- **v2.2.0**: Bit 12 is ignored (it switched the low speed optimization on without [`/enableLowSpeedOptimize`](motor-driver-settings.md#enablelowspeedoptimize)). While the optimization is on, the command only changes the saved value, as [`/setMinSpeed`](speed-profile.md#setminspeed) does.

#### Errors

- `MotorNotStopped`: The command writes a driver register that can be written only while the motor is stopped or HiZ, and the motor is turning. Nothing is applied. Added in v2.2.0.

#### See also

[`/setMinSpeed`](speed-profile.md#setminspeed)
<!-- generated:end osc /setMinSpeedRaw -->

<!-- osc: /setFullstepSpeedRaw -->
<!-- generated:begin osc /setFullstepSpeedRaw -->
### `/setFullstepSpeedRaw` (int)motorID (int)fullstepSpeed {#setfullstepspeedraw}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| fullstepSpeed | int | 0-1023 | full-step speed threshold (raw register value) |

#### Executable timing

Always

#### Description

Sets the full-step speed threshold using a raw register value.

A value outside the range is not rejected: it is converted to 16 bits (70000 becomes 4464) and then masked to the width of the register by the driver.

#### Changes

- **v2.2.0**: Also sets the full-step speed setting that `/saveConfig` saves and `/resetMotorDriver` applies again. Before, only the register was changed, so a reset or a saved configuration brought back the value from before.

#### See also

[`/setFullstepSpeed`](speed-profile.md#setfullstepspeed)
<!-- generated:end osc /setFullstepSpeedRaw -->

<!-- osc: /setAccRaw -->
<!-- generated:begin osc /setAccRaw -->
### `/setAccRaw` (int)motorID (int)acc {#setaccraw}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| acc | int | 0-4095 | acceleration (raw register value) |

#### Executable timing

When the motor is stopped

#### Description

Sets the acceleration of the speed profile using a raw register value.

A value outside the range is not rejected: it is converted to 16 bits (70000 becomes 4464) and then masked to the width of the register by the driver. The motor must be stopped or HiZ; a turning motor replies `MotorNotStopped` and keeps its old value.

#### Changes

- **v2.2.0**: Also sets the acceleration setting that `/saveConfig` saves and `/resetMotorDriver` applies again. Before, only the register was changed, so a reset or a saved configuration brought back the value from before.
- **v2.2.0**: The motor must be stopped or HiZ; a turning motor replies `/error/command MotorNotStopped` and keeps its old value.

#### Errors

- `MotorNotStopped`: The command writes a driver register that can be written only while the motor is stopped or HiZ, and the motor is turning. Nothing is applied. Added in v2.2.0.

#### See also

[`/setAcc`](speed-profile.md#setacc)
<!-- generated:end osc /setAccRaw -->

<!-- osc: /setDecRaw -->
<!-- generated:begin osc /setDecRaw -->
### `/setDecRaw` (int)motorID (int)dec {#setdecraw}

#### Argument

| Argument | Type | Range | Description |
| --- | --- | --- | --- |
| motorID | int | 1-4 (STEP400), 1-8 (STEP800), 255 (all motors) | Motor ID |
| dec | int | 0-4095 | deceleration (raw register value) |

#### Executable timing

When the motor is stopped

#### Description

Sets the deceleration of the speed profile using a raw register value.

A value outside the range is not rejected: it is converted to 16 bits (70000 becomes 4464) and then masked to the width of the register by the driver. The motor must be stopped or HiZ; a turning motor replies `MotorNotStopped` and keeps its old value.

#### Changes

- **v2.2.0**: Also sets the deceleration setting that `/saveConfig` saves and `/resetMotorDriver` applies again. Before, only the register was changed, so a reset or a saved configuration brought back the value from before.
- **v2.2.0**: The motor must be stopped or HiZ; a turning motor replies `/error/command MotorNotStopped` and keeps its old value.

#### Errors

- `MotorNotStopped`: The command writes a driver register that can be written only while the motor is stopped or HiZ, and the motor is turning. Nothing is applied. Added in v2.2.0.

#### See also

[`/setDec`](speed-profile.md#setdec)
<!-- generated:end osc /setDecRaw -->
