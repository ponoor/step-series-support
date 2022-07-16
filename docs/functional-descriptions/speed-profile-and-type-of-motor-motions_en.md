## Speed profile
### Overview
Speed profile sets the acceleration (acc), deceleration (dec), and maximum speed (maxSpeed) values of the motor prior to the motor moving.
These values depend on the following:

- Motor Specifications
- Power supply voltage
- Load
- Voltage mode or current mode

While we provide some example defaults, you need to set these values according to your actual environment. This requires some trial and error on your part.

### Setting the Profile
Use [`/setSpeedProfile`](https://ponoor.com/en/docs/step400/osc-command-reference/speed-profile/#setspeedprofile_intmotorid_floatacc_floatdec_floatmaxspeed) to set the above three values. Acc and dec
cannot be set unless the motor is stopped; however, maxSpeed can be set at any time.

You can also set the minimum speed (minSpeed) with `/setMinSpeed`. It is unlikely to be used for any actual application, but this speed will be used for `/releaseSw` speed as a part of the homing procedure.

## Type of motor operation
### Constant speed
The [`/run`](https://ponoor.com/en/docs/step400/osc-command-reference/motor-control/#run_intmotorid_floatspeed) command is used to drive the motor at a constant speed. The acceleration, deceleration, and maximum speed curves set by [`/setSpeedProfile`](https://ponoor.com/en/docs/step400/osc-command-reference/speed-profile/#setspeedprofile_intmotorid_floatacc_floatdec_floatmaxspeed) are adhered to by this command. The motor runs perpetually until speed 0 (`/run 0`) or a stop command is sent. The motor will not run faster than the maximum speed set in the speed profile. Sending a speed to run faster than this profile setting will cause the motor's speed to be truncated to that setting. The motor will be kept in the BUSY state during the acceleration and deceleration.

[`/goUntil`](https://ponoor.com/en/docs/step400/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed) and [`/releaseSw`](https://ponoor.com/en/docs/step400/osc-command-reference/homing/#releasesw_intmotorid_boolact_booldir) are also considered constant speed commands.

### Positioning
The trapezoidal drive towards the specified position is performed according to the speed profile. In other words, it accelerates according to the acceleration rate of the speed profile, then drives at constant speed when it reaches the maximum speed, and then decelerates at specified deceleration rate at the timing calculated backwards to stop at the specified position. It may start decelerating before it reaches the maximum speed, especially when you want to accelerate / decelerate at a relatively slow rate. It remains in the BUSY state until the motor stops. It's not possible to interrupt the current positioning motion with another positioning motion.

Typical commands for positioning operation are `/goTo` and `/move`. Other commands include `/goHome`, `/goMark`, and `/goToDir`.

NOTE: With [STEP-series Universal Firmware](https://github.com/ponoor/step-series-universal-firmware), positioning motions (except /move) can interrupt another positioning motions.

### Servo mode
This is not a function of the motor driver, but a mode of driving implemented in the firmware. It constantly updates the constant speed operation to follow a given target position. This mode is similar to a radio controlled servo motor. No other motor motion commands can be sent while the motor is operating in this mode.

### Types of stops
There are two options with a total of four different commands, as follows:

-  Decelerating according to the speed profile or stop instantly
-  Keeping magnetized/excited or entering a high impedance (High Z) state after stopping

| State after stop | Deceleration stop | Immediate stop |
| --- | --- | --- |
| Excited | SoftStop | HardStop |
| HiZ | SoftHiZ | HardHiZ |

The excited state is the state in which voltage or current (torque) is maintained to hold the motor's position according to `KVAL_HOLD` or `TVAL_HOLD`, respectively. The high impedance (HiZ) state is when the current is cut off and no holding torque is maintained. **Any loads the motor is moving may fall or lose their positioning during HiZ.**
