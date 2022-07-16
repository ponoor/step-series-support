## The difference between voltage control and current control
There are two types of stepping control methods: constant voltage control (**voltage mode**) and constant current control (**current mode**). Only the STEP400 can switch between both voltage and current modes. The difference between these modes is well-explained in [this presentation PDF](https://www.st.com/content/dam/AME/2019/developers-conference-2019/presentations/STDevCon19_3.6_Using%20Powerstep01.pdf) by STMicroelectronics.


The differences can be described as follows:

- Voltage mode is quiet and smooth, but is limited to lower speeds
- Current mode is noisy, but can reach higher speeds

## Test with the STEP400
To better illustrate this point, here is a demonstration video to show the differences between these two modes.

<div class="embed-video"><iframe width="560" height="315" src="https://www.youtube.com/embed/ydPHQfc22kQ" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

First, the motor runs under constant voltage mode. After around 800 steps/sec, the motor cannot run properly and starts to vibrate and stalls at about 1,400 steps/sec. Overall, the motor runs quietly until the vibration starts. A microphone is attached to the motor so that we can capture the smallest noises.

Next, the motor is switched to constant current mode. It is noisy, but can drive to a higher speed. In this mode, we were able to achieve more than 11,000 steps/sec before the motor started to vibrate and stall.

## KVAL and TVAL
**KVAL** register values are applied to control the drive voltage in voltage mode; likewise, **TVAL** registers are used to control the drive current in current mode. Both act as percentage multipliers to dictate what percentage of the power supply voltage or current is sent to the motors. Although they are the same registers internally in the driver, our firmware keeps them separated and rewrites them when the modes are changed.

## Voltage mode setting
In voltage mode, KVAL is used to set what percentage of the power supply voltage should be applied to the motor. If a high voltage power source is used, excessive current may flow when the motor is spinning at lower speeds. To compensate this current imbalance, there is a group of registers to lower the supplied drive voltage at low speeds and supply higher voltages at higher speeds. The calculation of these register values is described in [STMicroelectronics application note](https://www.st.com/resource/en/application_note/). In the STEP400, these registers can be set with [`/setBemfParam`](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setbemfparam_intmotorid_intint_speed_intst_slp_intfn_slp_acc_intfn_slp_dec) command or with the [Config Tool](http://ponoor.com/tools/step400-config/).

Additionally, we have calculated the register values for some motors based on our actual measurements and have made them available as [configuration files](https://ponoor.com/en/docs/step-series/settings/example-parameter-values-for-example-steppers/). We have only a small numbers of configuration files at the moment, but we are planning to add more in the future. If you have a motor that is not listed in the example files and have determined these configurations on your own, we would deeply appreciate you sharing your configurations with us and the community.

## Current mode setting
In current mode, which is only available on the STEP400, TVAL registers are used to set the target current value. The current can be set up to 5A in increments of 78mA on the STEP400. You'll need a high voltage power supply to deliver the target current when the motor is running at high speed. Although the powerSTEP01's actual current drive capability is 10A, the STEP400 has the upper rating limit of 5A due to the power rating limitation of the current sensing resistor. At 5A phase current, the torque is considerably strong, and the tiniest mistake may lead to great physical danger. In such situations we recommend to use use an industrial grade motor driver.

## Switching between the modes
Use the following commands to switch between the modes:
- [`/setVoltageMode`](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setvoltagemode_intmotorid) - switch to the voltage mode.
- [`/setCurrentMode`](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setcurrentmode_intmotorid) - switch to the current mode.

The motor must be in the high impedance (High Z) state before switching the mode. For example, if you are going to switch the Motor 1 to current mode, send these commands in the following order:

1. `/hardHiZ 1`
2. `/setCurrentMode 1`

Microstepping is limited to a minimum of 1/16 in current mode. Any lower value than 1/16 will be regarded as 1/16. When you change microstep value, the coordinate system will also change. For example, for one full shaft rotation of a 200 step motor in 1/128 microstepping mode, 200x128=25600 steps are made; but one rotation in 1/16 microstepping mode is 200x16=3200 steps.

