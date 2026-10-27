---
title: Electromagnetic brake wiring
---

# Electromagnetic brake wiring

How to wire an electromagnetic brake to the STEP400 and the STEP800. The firmware controls the brakes of both boards in the same way; what a brake does and how its state changes is explained in [Electromagnetic brake](../guides/electromagnetic-brake.md).

## Overview {#overview}

Both boards have an output for the brakes, one per motor. The output is a 3.3 V logic signal and cannot drive a brake directly. A driving circuit that switches the power of the brake is needed.

- **STEP400**: use the EMB-STEP400, the brake board for the STEP400. It has the driving circuit for 4 brakes. See [EMB-STEP400](../hardware/emb-step400.md) for its specifications.
- **STEP800**: the brake output (J2) is on the board, but there is no official driving board. Make a driving circuit with transistors, MOSFETs, relays or similar parts.

The pin assignment of the output connectors is in [STEP400](../hardware/step400.md#brake-output) and [STEP800](../hardware/step800.md#brake-output).

To use a brake, enable it for the motor with [`electromagnetBrakeEnable`](configuration-items.md#driversettings-electromagnetbrakeenable) (`/enableElectromagnetBrake`), and set the transition duration ([`brakeTransitionDuration`](configuration-items.md#driversettings-braketransitionduration); how to decide it: [Transition duration](../guides/electromagnetic-brake.md#transition-duration)).

### Output level {#logic}

**HIGH releases the brake and LOW engages it.** This is the same on both boards. The STEP400 drives the output from a pin of the MCU, and the STEP800 drives it through a shift register (74HC595). The driving circuit must engage the brake when its input is LOW.

## STEP400 with the EMB-STEP400 {#step400}

### Power for the brake {#brake-power}

Supply the voltage that the electromagnetic brake needs to the EMB-STEP400. Many brakes use 24 V; check the datasheet of your motor. **Use the same power supply as for the motor** (see [Usage notes](../guides/electromagnetic-brake.md#usage) for the reason).

The board has two power terminals, a DC barrel jack and a Euro-style terminal block. They are connected in parallel on the board, so **never supply power to both at the same time.**

#### DC barrel jack {#brake-dc-jack}

- 5.5 mm outer diameter
- 2.1 mm inner diameter
- Center positive

#### Euro-style terminal block {#brake-terminal-block}

The terminal block is a 3.81 mm pitch, 2 pin block. Connect the polarity as printed on the board.

[![](https://ponoor.com/cms/wp-content/uploads/2021/03/brake-power-700x525.jpg)](https://ponoor.com/cms/wp-content/uploads/2021/03/brake-power.jpg)

### Connecting the brake {#connecting-brake}

Connect the wires of the electromagnetic brake to the brake terminals. The terminals of the brake board are numbered like the motors of the STEP400. Connect each brake to the terminal with the same number as its motor.

Most electromagnetic brakes have a polarity. Connect them as the signs on the board show.

### Connecting the STEP400 {#connecting-step400}

Connect the STEP400 and the EMB-STEP400 with the supplied 6-pin ribbon cable.

[![](https://ponoor.com/cms/wp-content/uploads/2021/03/brake-riboncable-700x525.jpg)](https://ponoor.com/cms/wp-content/uploads/2021/03/brake-riboncable.jpg)

## STEP800 {#step800}

The brake output (J2) of the STEP800 has one signal for each of the 8 motors, 3.3 V and GND. Connect each signal to the input of a driving circuit that you make. There is no official driving board.

## The output at power-on and at a reset {#power-on}

The output is not under the control of the firmware from the power-on or the reset until the firmware starts. Take this into account in the driving circuit, because a load that hangs on the motor can fall. The firmware cannot prevent this; see [When the load is not held](../guides/electromagnetic-brake.md#unsupported).

- **STEP400**: the pins of the output are in a high impedance state until the firmware starts (nothing is connected to them). Pull down the input of the driving circuit, so that the brake engages while the output floats. The EMB-STEP400 does this with a resistor on each input.
- **STEP800**: the shift register is not defined at power-on, and all the outputs can be on the releasing side. It is about 250 ms after the power is applied, mostly the time of the bootloader. After a reset (the reset button or a drop of the supply voltage), the outputs also keep the released state for about 0.5 s until the firmware starts.

Countermeasures for the STEP800:

- Supply the power of the brake after the board has sent [`/booted`](../reference/automatically-sent-messages.md#booted).
- Or make the driving circuit so that it does not release the brake for a while after the power is applied.

## Notes {#notes}

- **Disconnect the electromagnetic brake while you write the firmware.** While the firmware is written, the firmware does not run, and the brake output of the STEP800 can be on the releasing side. See [Compiling the firmware](../maintenance/compile-the-arduino-sketch.md#uploading).
- **Use the same power supply for the brake and the motor.** See [Usage notes](../guides/electromagnetic-brake.md#usage).
- Restart, watchdog and CPU fault: the board engages the brakes before it restarts. See [Restart, watchdog and CPU fault](../guides/electromagnetic-brake.md#restart).

## Related commands and settings {#related}

<!-- osc-related: /enableElectromagnetBrake -->
<!-- generated:begin osc-related /enableElectromagnetBrake -->
**Related commands**

| Command | Arguments | Description |
| --- | --- | --- |
| [`/enableElectromagnetBrake`](../reference/brake.md#enableelectromagnetbrake) | (int)motorID (bool)enable | Enables / disables electromagnetic brake mode. |
<!-- generated:end osc-related /enableElectromagnetBrake -->

<!-- osc-settings: driverSettings.electromagnetBrakeEnable, driverSettings.brakeTransitionDuration -->
<!-- generated:begin osc-settings driverSettings.electromagnetBrakeEnable, driverSettings.brakeTransitionDuration -->
**Related configuration items**

| Key | Name | Commands |
| --- | --- | --- |
| [`driverSettings.electromagnetBrakeEnable`](configuration-items.md#driversettings-electromagnetbrakeenable) | Electromagnetic brake enable | `/enableElectromagnetBrake` |
| [`driverSettings.brakeTransitionDuration`](configuration-items.md#driversettings-braketransitionduration) | Brake transition duration | `/setBrakeTransitionDuration` |
<!-- generated:end osc-settings driverSettings.electromagnetBrakeEnable, driverSettings.brakeTransitionDuration -->
