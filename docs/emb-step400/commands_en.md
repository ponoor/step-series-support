## Electromagnet brake mode
To use the electromagnetic brake, brake mode must first be activated. To do this, send the command [`/enableElectromagnetBrake`](https://ponoor.com/en/docs/step400/osc-command-reference/brake/#enableelectromagnetbrake_intmotorid_boolenable) or from the config tool under `Electromagnetic brake enable`.

If the mode is enabled, the brake will be controlled according to the motors' excitation state.

## Switching States

With the command [`/activate`](https://ponoor.com/en/docs/step400/osc-command-reference/brake/#activate_intmotorid_boolstate), you can switch the excitation state of the motor. The brake will be released when the motor is excited and engage when the motor is not excited.

The overlapping time `Brake Transition Duration` can be set from [`/setBrakeTransitionDuration`](https://ponoor.com/en/docs/step400/osc-command-reference/brake/#setbraketransitionduration_intmotorid_intduration) or from the config tool under `Brake transition duration`.

## Releasing the Hold

Any load will be releasing when the holding torque on it is lost. However, there are cases where this behavior is desired. To do this, the command [`/free`](https://ponoor.com/en/docs/step400/osc-command-reference/brake/#free_intmotorid_boolstate) can be sent.

WARNING: Be very careful when sending this command. It is dangerous while any load is still attached to the motor! Ensure the load is safed before sending this command!

## Command Behaviors

While the EM brake is engaged, the motion commands [`/run`](https://ponoor.com/en/docs/step400/osc-command-reference/motor-control/#run_intmotorid_floatspeed), [`/goTo`](https://ponoor.com/en/docs/step400/osc-command-reference/motor-control/#goto_intmotorid_intposition), and [`/move`](https://ponoor.com/en/docs/step400/osc-command-reference/motor-control/#move_intmotorid_intstep) are not executed. Instead, the error [`ERROR_BRAKE_ENGAGED`](https://ponoor.com/en/docs/step400/osc-command-reference/automatically-sent-messages-from-step-400/#errorcommand) message will be raised.


Commands that put the motor into a non-excited state (torque hold released) will behave as follows:

- [`/softHiZ`](https://ponoor.com/en/docs/step400/osc-command-reference/motor-control/#softhiz_intmotorid): Decelerate the motor to a stop, engage the brake, then release the motor (HiZ state).
- [`/hardHiz`](https://ponoor.com/en/docs/step400/osc-command-reference/motor-control/#hardhiz_intmotorid): Stop the motor immediately, engage the brake, then release the motor (HiZ state).

[`/softStop`](https://ponoor.com/en/docs/step400/osc-command-reference/motor-control/#softstop_intmotorid) and [`/hardStop`](https://ponoor.com/en/docs/step400/osc-command-reference/motor-control/#hardstop_intmotorid) have no change in behavior and will operate like normal. The brake is not engaged when these commands are sent and the motor is kept excited.