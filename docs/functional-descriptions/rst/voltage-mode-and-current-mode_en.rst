The difference between voltage control and current control
----------------------------------------------------------

There are two types of stepping motor control methods: constant voltage
control (**voltage mode**) and constant current control (**current
mode**). STEP800 can be used in voltage mode, while STEP400 can switch
between both voltage and current modes. The difference between these
modes is well-explained in `this presentation PDF`_ by
STMicroelectronics.

The differences for the users can be described as follows;

-  Voltage mode is quiet and smooth, but can only drive at low speed.
-  Current mode is noisy, but can drive to higher speed.

Test with the STEP400
---------------------

Here is a video about: - The difference between constant voltage control
and constant current control - The difference between full-step and
micro-stepping drive

.. container:: embed-video

   .. raw:: html

      <iframe width="560" height="315" src="https://www.youtube.com/embed/ydPHQfc22kQ" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>

   .. raw:: html

      </iframe>

First, the motor runs under constant voltage control (hereinafter
referred to as “**voltage mode**”). After around 800 step/sec, the motor
cannot run properly and starts to vibrate, then it stalls at about 1,400
step/sec and stops completely. The motor runs quietly until the
vibration starts, but in this video, a microphone is attached to the
motor so that we can capture the smallest noise.

Next, the motor is switched to constant current control (hereinafter
referred to as “**current mode**”). It is noisy, but it can drive to
higher speed. In this setting, we were able to achieve more than 11,000
steps/sec.

KVAL and TVAL
-------------

**KVAL** register values are applied to control the drive voltage in the
voltage mode, and **TVAL** registers are used to control the drive
current in the current mode. Although they are actually same registers
in the driver, our firmware keeps them separated, rewrites them when
mode changes to avoid unintended values to be set.

Voltage mode setting
--------------------

In the voltage mode of the STEP400 or STEP800, registers called KVAL is
used to set what percentage of the power supply voltage should be
applied to the motor. Also if a high voltage power source is used,
excessive current may flow when the motor is spinning at lower speed. To
compensate this current imbalance, there is a group of registers to
lower the drive voltage at low speed and supply higher voltage at higher
speed. The calculation of these register values is described in the
`STMicroelectronics application note`_. In STEP400, these registers can
be set with ```/setBemfParam```_ command, and from the `Config Tool`_ as
well.

We have calculated the register values for some motors based on our
actual measurements and have made them available as `configuration
files`_. We have only a small numbers of configuration files at the
moment, but we are planning to add more in the future.

Current mode setting
--------------------

In the current mode which available in STEP400, the TVAL registers are
used to set the target current value. The current can be set up to 5A in
increments of 78mA in the STEP400. Yo need a high voltage power supply
to deliver the target current when the motor is running at high speed.
Although the PowerSTEP01’s actual current drive capability is 10A, the
STEP400 has the upper rating limit of 5A due to the power rating
limitation of the current sensing resistor. At 5A phase current, the
torque is considerably strong, and the tiniest mistake may lead to great
physical danger. In such situations we recommend to use use an
industrial grade motor drivers.

Switching modes
---------------

These commands are available for switching between modes; -
```/setVoltageMode```_ - switch to the voltage mode. -
```/setCurrentMode```_ - switch to the current mode.

The motor must be in the high impedance (High Z) state before switching
the mode. For example, if you are going to switch the Motor 1 to current
mode, the command sequence is in the following order; 1. ``/hardHiZ 1``
2. ``/setCurrentMode 1``

The microstepping is limited to minimum 1/16 in current mode. Any lower
value than 1/16 will be regarded as 1/16. When you change the
microstepping mode, the coordinate system will also change. For example
one rotation in 1/128 microstepping mode is 200x128=25600 steps for a
200steps/round motor, but one rotation in 1/16 microstepping mode is
200x16=3200 steps.

.. _this presentation PDF: https://www.st.com/content/dam/AME/2019/developers-conference-2019/presentations/STDevCon19_3.6_Using%20Powerstep01.pdf
.. _STMicroelectronics application note: https://www.st.com/resource/en/application_note/dm00061093-voltage-mode-control-operation-and-parameter-optimization-stmicroelectronics.pdf
.. _``/setBemfParam``: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setbemfparam_intmotorid_intint_speed_intst_slp_intfn_slp_acc_intfn_slp_dec
.. _Config Tool: http://ponoor.com/tools/step400-config/
.. _configuration files: https://ponoor.com/en/docs/step-series/settings/example-parameter-values-for-example-steppers/
.. _``/setVoltageMode``: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setvoltagemode_intmotorid
.. _``/setCurrentMode``: https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setcurrentmode_intmotorid
