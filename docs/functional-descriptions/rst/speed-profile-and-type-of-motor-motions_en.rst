Speed profile
-------------

Overview
~~~~~~~~

The speed profile sets the acceleration, deceleration, and maximum speed
values of the motion prior to the motor operation in advance. This
depends on the following:

-  Motor Specifications
-  Power supply voltage
-  Load
-  Voltage control or current control

You need to set these values according to your actual environment.

Values to be set
~~~~~~~~~~~~~~~~

The three values, Acceleration(acc),deceleration(dec), and maxSpeed need
to be set. You can also set the minimum speed (minSpeed) as a function
of the motor driver, but it is fixed at 0 on the firmware because it is
unlikely to be used for the actual application.

Setting command
~~~~~~~~~~~~~~~

With ```/setSpeedProfile```_ command you can set above three values. The
acc and dec cannot be set unless the motor is stopped, the maxSpeed
parameter can be set at anytime.

Type of motor operation
-----------------------

Constant speed
~~~~~~~~~~~~~~

This is the command to drive the the motor with the
acceleration/deceleration rate set by the speed profile, then maintains
constant speed. It continues to rotate until speed 0 is set, or stop
command is sent. The range of speed that can be set is limited to the
maximum speed of the speed profile. It will keep BUSY state during the
acceleration and deceleration. A representative command for the constant
spped drive is ```/run```_. There are also ```/goUntil```_ and
```/releaseSw```_ commands are available.

Positioning
~~~~~~~~~~~

The trapezoidal drive towards the specified position is performed
according to the speed profile. In other words, it accelerates according
to the acceleration rate of the speed profile, then drives at constant
speed when it reaches the maximum speed, and then decelerates at
specified deceleration rate at the timing calculated backwards to stop
at the specified position. It may start decelrating before it reaches
the maximum speed, especially when you want to accelerate / decelerate
relatively slow rate. It remains in the BUSY state until the motor
stops. It’s not possbile to interrupt the current positioning motion
with another positioning motion.

Servo mode
~~~~~~~~~~

This is not a function of the motor driver, but a mode of driving
implemented in the firmware. It constantly updates the constant speed
operation to follow a given target position. This mode is similar to tje
radio controlled servo motor. No other motor motion commands can be sent
while the motor is operating in this mode.

Types of stops
~~~~~~~~~~~~~~

There are two options with a total of four different commands, as
follows;

-  Decelerate according to the speed profile or stop instantly.
-  Keep magnetized / excited or goes to the high impedance(High Z) state
   after stop.

================ ================= ==============
State after stop Deceleration stop Immediate stop
================ ================= ==============
Excitation       SoftStop          HardStop
HiZ              SoftHiZ           HardHiZ
================ ================= ==============

The excited state is the state in which the torque is applied to hold
the motor position according to ``KVAL_HOLD``\ voltage, or current set
by the ``TVAL_HOLD`` value. The high impedance state is the state where
the current is cut off and there is no holding torque.

.. _``/setSpeedProfile``: https://ponoor.com/en/docs/step400/osc-command-reference/speed-profile/#setspeedprofile_intmotorid_floatacc_floatdec_floatmaxspeed
.. _``/run``: https://ponoor.com/en/docs/step400/osc-command-reference/motor-control/#run_intmotorid_floatspeed
.. _``/goUntil``: https://ponoor.com/en/docs/step400/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed
.. _``/releaseSw``: https://ponoor.com/en/docs/step400/osc-command-reference/homing/#releasesw_intmotorid_boolact_booldir
