---
title: Servo mode
wp_id: 1119
slug: servo-mode
lang: en
link: "https://ponoor.com/en/docs/step-series/functional-description/servo-mode/"
date: "2020-08-21T14:37:02"
modified: "2022-07-16T21:43:36"
parent: 873
menu_order: 52
---

# Servo mode

## Servo Mode Explained

As stated before, servo mode is not a function native to the motor driver chip on the board. While seemingly similar to positional commands, servo mode commands allow you to define a new target position *while the motor is moving*. This is not possible with positional commands which require the position to be set in advance of the motor's movements. New positional targets are not updated until after the current target is reached. While this mode is active, other functional commands cannot be sent.

*Example Behavior of Servo Mode*

## Initializing steps for Servo Mode

### Toggling the Mode

The command [`/enableServoMode`](https://ponoor.com/en/docs/step-series/osc-command-reference/servo-mode/#enableservomode_intmotorid_boolenable) enables or disables Servo Mode. Upon starting Servo Mode, the driver must not be in the BUSY state.

### Updating the Target Position

The target position can be updated by the [`/setTargetPosition`](https://ponoor.com/en/docs/step-series/osc-command-reference/servo-mode/#settargetposition_intmotorid_intposition) command. When the firmware receives a new target position, it will compare the new position with the current one and change the rotation speed of the motor.  
Additionally, you can send target positions to all motors at the same time with [`/setTargetPositionList`](https://ponoor.com/en/docs/step-series/osc-command-reference/servo-mode/#settargetpositionlist_intposition1_intposition2_intposition3_intposition4).

## Types of Control Parameters

The motor's rotation speed is calculated by a technique called "PID Control". To better illustrate the purpose of PID, refer to the following graph:

![](https://python-step-series.readthedocs.io/en/documentation/_images/pid-control.jpg)

Please refer to this graph when the control parameters are discussed below. These parameters can be set with the command [`/setServoParam`](https://ponoor.com/en/docs/step-series/osc-command-reference/servo-mode/#setservoparam_intmotorid_floatkp_floatki_floatkd).

### Proportional Gain (kP)

PID control uses differences of current position and target position (deviation) for the control. That is, it approaches the target position by rotating faster when the deviation is large, and rotates slower when the deviation is small. The proportional gain defines how much influence to the speed will be given from the deviation. If the value is too small, it will take time to approach the target position, and if the value is too large, an "overshoot" may occur in which case the target position is passed.

### Integral Gain (kI)

If there is only the proportional control, the rotation speed will get slower and takes very long time to compensate the offset when approaching to the target position. In this case, adding the time integral of the deviation to the control value will effectively compensate the offset. By applying large integral gain, you could compensate the offset quickly; however, it may cause the overshoot, or even the continuous oscillation by trying to compensate the overshoot.

### Differential Gain (kD)

In case an overshoot or oscillation occurs, this parameter is used to eliminate steep changes in deviation — it acts like a damper that continually decreases each oscillation.

## Methods for Determining PID Parameters

### Step by Step Procedures

PID Control Parameters must be determined from the actual acceleration, deceleration, and the maximum rotation speed (speed profile). Determine the control parameters by following these steps:

1. Decide the KVAL (in case of current mode, TVAL) that is matched to the rated value and load.
2. Decide the operational acceleration, deceleration, and the maximum rotation speed (speed profile).
3. Adjust the PID control gains.

### The Decisions of PID Control Gain

There are multiple methods for deciding the optimal PID control gain. The best values depend on factors like the objective of movement and the frequency of target position changes. We recommend the following step-by-step approach with trial and error on the actual setup.

#### 1. kP

Set all kP, kI, kD, to 0.0 and gradually raise the kP until the motor starts to oscillate around its target position. When the target position changes only sometimes, we often set only kP while keeping other kI and kD values at 0.0.

#### 2. kI

When the target position changes only once every couple of seconds, raising the kI value makes the movement quicker and more responsive. However, when the target position is sent at 60fps, the acceleration towards each new target position may cause vibration and lose smooth transitions. The preferred value depends on whether quick response to the target position or smooth overall movement is the priority.

#### 3. kD

We gradually raise the kD if oscillation or overshoot is observed when approaching the target.
