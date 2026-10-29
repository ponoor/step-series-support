---
title: Quick start
---

# Quick start

This page takes a board just out of the box to a motor turning. You connect one board directly to your PC, turn one motor with an OSC (Open Sound Control) message, and adjust the drive voltage (KVAL) so that the motor turns smoothly. The pages that explain each step in detail are linked from the steps.

## What you need {#what-you-need}

- A STEP400 or a STEP800.
- A bipolar stepper motor with 4 wires. This page uses the Mercury Motor `SM-42BYG011-25`, which is easy to get and inexpensive. If you use another motor, some settings may need to be changed to match it.
- A power supply: an AC adapter of 24 V and 1 A is enough for one motor of this size.
- An Ethernet cable, and a PC with an Ethernet port (or a USB-Ethernet converter).
- Software that sends OSC messages. See [Software to send OSC](index.md#software).

You do not need a microSD card.

## Connecting {#connecting}

Do not turn on the power supply until the steps say so. You may connect the power supply, but make sure it is off.

### Ethernet {#ethernet}

Connect the board to your PC directly with the Ethernet cable (peer-to-peer). A network switch also works.

!!! warning "Do not connect the board to a router"
    A router, especially one with a DHCP server, behaves differently from a switch and can cause trouble. Connect the board directly to the PC, or to a real network switch.

### Motor {#motor}

Only bipolar stepper motors with 4 wires can be used. The `SM-42BYG011-25` can be bought, for example, from these (unaffiliated) shops:

- [SparkFun](https://www.sparkfun.com/products/9238)
- [Strawberry Linux](http://strawberry-linux.com/catalog/items?code=12026)
- [Akizuki Denshi](https://akizukidenshi.com/catalog/g/gP-05372/)

![](http://ponoor.com/manage/wp-content/uploads/2020/10/09238-01.jpg)

Connect the two wires of one coil to a pair of the terminals, and the two wires of the other coil to the other pair. The wiring diagram in the [datasheet](https://www.sparkfun.com/datasheets/Robotics/SM-42BYG011-25.pdf) of this motor shows that the pairs are `Red - Green` and `Yellow - Blue`.

[![](https://ponoor.com/cms/wp-content/uploads/2020/08/motor-wiring-diagram-sample.png)](https://ponoor.com/cms/wp-content/uploads/2020/08/motor-wiring-diagram-sample.png)

Connect the wires to the terminal block like this:

[![](https://ponoor.com/cms/wp-content/uploads/2020/08/SM-42BYG-wiring-700x525.jpg)](https://ponoor.com/cms/wp-content/uploads/2020/08/SM-42BYG-wiring.jpg)

How to find the pairs of another motor, and the terminal, are explained in [Motor terminals](../connections/power-supply-and-motor.md#motor-terminals).

### Power supply {#power-supply}

Connect the AC adapter to the DC barrel jack. The plug must be 5.5 mm in outer diameter and 2.1 mm in inner diameter, with the center positive. Make sure the power supply is off.

![](https://ponoor.com/cms/wp-content/uploads/2020/08/image-1609563897700.png)

The DC barrel jack is enough for a motor of this size. For a larger motor with a higher voltage or a higher current, use the screw terminal next to the jack. **Never connect a power supply to both of them.** See [Power terminals](../connections/power-supply-and-motor.md#power-terminals).

## Settings of the board {#board-settings}

This page uses the default settings, so leave the microSD card slot empty. When there is no card, the board starts with the initial values of the firmware ([At start](../connections/how-settings-work.md#at-start)). You can change the settings later, and save them: see [How the settings work](../connections/how-settings-work.md).

Set the DIP switch to 1: slide only the leftmost switch to the ON side, and the others to the OFF side. With the board turned so that the digits printed on the DIP switch can be read, the leftmost switch is the lowest digit. See [DIP switch settings](../connections/network-and-dip-switch.md#dip-switch).

![](https://ponoor.com/cms/wp-content/uploads/2020/10/step400-dipSw.jpg)

With the DIP switch at 1 and the initial settings, the network settings of the board are as follows. The ID is added to the IP address of the board and to the sending port.

<!-- quickstart-network:begin -->
| Item | Value |
| --- | --- |
| IP address of the board | 10.0.0.101 <!-- qs-network: boardIp --> |
| IP address of the PC (the destination of the board) | 10.0.0.10 <!-- qs-network: pcIp --> |
| Subnet mask | 255.255.255.0 <!-- qs-network: subnet --> |
| Port that the board receives on | 50000 <!-- qs-network: boardPort --> |
| Port that the PC receives on | 50101 <!-- qs-network: pcPort --> |
<!-- quickstart-network:end -->

These are the values for ID 1 with the initial values of the firmware. The list of the initial values and the way the ID is added are in [Initial settings](../connections/network-and-dip-switch.md#initial) and [Adding the ID](../connections/network-and-dip-switch.md#adding-id).

Turn on the power supply now. The back of the board has pins that carry the supply voltage and a large current. Put the board on an insulator, or attach spacers to the holes of the board, so that you do not damage the board or hurt yourself.

## Settings of the PC {#pc-settings}

The board sends its messages to the IP address of the PC, so set a fixed IP address to the Ethernet port that the board is connected to. Set the IPv4 address of the PC as follows:

| Item | Value |
| --- | --- |
| IP address | 10.0.0.10 |
| Subnet mask | 255.255.255.0 |

How to set a fixed IP address depends on the OS:

- [Windows](https://support.microsoft.com/en-us/windows/change-tcp-ip-settings-bd0a07af-15f5-cd6a-363f-ca2b6f391ace)
- [Mac](https://support.apple.com/en-us/HT202480)
- [Linux](https://www.youtube.com/watch?v=Yr6qI6v1QCY)

## Checking the connection {#checking}

Run `ping 10.0.0.101` in the Terminal (the Command Prompt on Windows). If the board answers, the connection is working.

From here on, how you send the commands depends on your environment, so this page shows the OSC messages themselves. Send them to the IP address of the board and the port that the board receives on, which are in the table above.

First, tell the board where to send its replies by sending [`/setDestIp`](../reference/system-settings.md#setdestip):

```
/setDestIp
```

With the initial settings, the board sends no OSC message except `/booted` until it receives this command. When the board has received the command, it replies [`/destIp`](../reference/system-settings.md#setdestip) to the port that the PC receives on.

Send `/setDestIp` again when you replace the PC or change the network. The board learns the MAC address of the PC at that time; the details are in [The destination and `/setDestIp`](../guides/communication-and-messages.md#setdestip).

If `/destIp` does not come, check the settings of the PC again, and, on Windows, whether the firewall allows the communication of your application. See [Replies and position reports do not arrive](../maintenance/troubleshooting.md#no-reply).

## Running the motor {#running}

Send [`/run`](../reference/motor-control.md#run) to turn the motor at a speed:

```
/run 1 200.
```

The first argument is the motor ID: the number printed on the board next to the connector that the motor is connected to. 255 means all the motors; see [Motor ID](../reference/index.md#motor-id). The second argument is the speed in steps per second, and a negative value turns the motor in the opposite direction. For a motor with 200 steps per revolution, such as the `SM-42BYG011-25`, `200.` is one revolution per second. The range of the speed is in the [`/run`](../reference/motor-control.md#run) reference.

Is the motor turning? To stop it, send `/run 1 0`, or stop all the motors with [`/softStop`](../reference/motor-control.md#softstop) (decelerates and stops) or [`/hardHiZ`](../reference/motor-control.md#hardhiz):

```
/softStop 255
```

After `/hardHiZ` the motor is not energized, so it does not hold its position.

!!! warning "Do not disconnect the motor while it is turning"
    Do not disconnect the motor while it is energized or turning. It damages the board.

If the motor does not move, see [The motor does not move](../maintenance/troubleshooting.md#motor-not-moving).

The motor may turn roughly: with a lot of vibration and noise. This is because the drive voltage does not suit the motor. You adjust it with KVAL in the next step.

## Adjusting KVAL {#kval}

The drive voltage of the motor in voltage mode is set with KVAL, as a fraction of the supply voltage. Too low or too high a value makes the motor turn roughly. KVAL has four values, for holding, running, accelerating and decelerating; see [KVAL and TVAL](../guides/voltage-and-current-mode.md#kval-tval). The initial values and the range are in the [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval) reference.

Turn the motor again:

```
/run 1 200.
```

While it is turning, set the four values of motor 1 at once with [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval). Set the holding value to 0, and the other three to the same value, which you raise little by little:

```
/setKval 1 0 24 24 24
```

The arguments are the motor ID, the holding value, the running value, the accelerating value and the decelerating value. With a 24 V power supply, 24 is about 9% of the supply voltage. Raise the values little by little, and the motor starts to turn quietly at some point:

```
/setKval 1 0 32 32 32
/setKval 1 0 40 40 40
```

A higher KVAL gives more torque, but the motor also gets hotter and may vibrate again. Set it to suit your load. The STEP400 can also drive the motor with a constant current (current mode); see [Current mode setting](../guides/voltage-and-current-mode.md#current-mode-setting).

We calculated the values for some motors and made configuration files of them. See [Example parameter values for example steppers](../connections/example-parameters.md).

## Next steps {#next-steps}

- Save the settings that you adjusted so that they are kept after the board restarts: [`/saveConfig`](../reference/system-settings.md#saveconfig) and [How the settings work](../connections/how-settings-work.md).
- Use more than one board: change the ID with the DIP switch. [Adding the ID to the IP address and the port](../connections/network-and-dip-switch.md#adding-id).
- Find the reference position of the motor: [Homing and position management](../guides/homing-and-position.md).
- Know how each function works: [Functional guides](../guides/index.md).
- Look up a command: [OSC reference](../reference/index.md).

## Related commands and settings {#related}

<!-- osc-related: /setDestIp, /run, /softStop, /hardHiZ, /setKval -->
<!-- generated:begin osc-related /setDestIp, /run, /softStop, /hardHiZ, /setKval -->
**Related commands**

| Command | Arguments | Description |
| --- | --- | --- |
| [`/setDestIp`](../reference/system-settings.md#setdestip) | - | Sets the destination IP address (`destIp`) to where the device should send messages to, when it replies to a query or report internal state changes, etc. |
| [`/run`](../reference/motor-control.md#run) | (int)motorID (float)speed | Rotates the motor at specified speed. |
| [`/softStop`](../reference/motor-control.md#softstop) | (int)motorID | After decelerating according to the speed profile, the motor stops while it is kept excited. |
| [`/hardHiZ`](../reference/motor-control.md#hardhiz) | (int)motorID | Immediately stops the motor and releases the stepper excitation. |
| [`/setKval`](../reference/voltage-and-current-mode-settings.md#setkval) | (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)decKVAL | Sets the four KVALs together. |
<!-- generated:end osc-related /setDestIp, /run, /softStop, /hardHiZ, /setKval -->
