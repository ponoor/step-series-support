---
title: Diagnosis via USB serial port
---

# Diagnosis via USB serial port

You can connect a computer to the USB connector of the board to check its status and settings. This is practical for troubleshooting, for example when you cannot reach the board over the Ethernet network. The USB serial port also takes the commands that the [browser configuration tool](../connections/browser-config-tool.md) uses.

> The examples of the output on this page were made from the source code of firmware v2.2.0, not copied from a board. The values are examples.

## Connection {#connection}

Connect the board and the computer with a USB Type-C cable. USB powers only the MCU and its peripheral circuits. In this state the driver ICs are not powered, so the board cannot talk to them. Supply the motor power as well.

If you connect the USB cable first and the motor power later, the driver ICs are not initialized: the board initializes them only when it starts. Turn on the motor power first and then connect USB, or push the RESET button after you turn on the motor power. You can also send [`/resetMotorDriver`](../reference/motor-driver-settings.md#resetmotordriver) for all the motors (255).

When the USB cable is pulled out while the Ethernet cable is connected, the STEP400 (R1 board) can restart. This is a hardware problem; stop the motors before you pull out the cable. See [STEP400](../hardware/step400.md#usb-unplug).

## Serial monitor {#serial-monitor}

The board is seen by the computer as an Arduino Zero and is a virtual serial port. As an example, this is how to use the serial monitor of the Arduino IDE. You can use any software that can send and receive text on a serial port.

### Selecting the port {#port}

From "Tools" -> "Port", choose "Arduino Zero (Native USB Port)".

![file](https://ponoor.com/cms/wp-content/uploads/2021/03/image-1616473811329.png)

### Opening the serial monitor {#open-monitor}

Click the magnifying glass icon. The window of the serial monitor opens.

[![](https://ponoor.com/cms/wp-content/uploads/2021/03/openserialmonitor-486x525.png)](https://ponoor.com/cms/wp-content/uploads/2021/03/openserialmonitor.png)

### Showing the menu {#menu}

Type `m` in the text box at the top and press the Send button (or the Return key). If the connection works, the menu of the diagnosis is shown.

![file](https://ponoor.com/cms/wp-content/uploads/2021/03/image-1616474112646.png)

The menu of firmware v2.2.0 is:

```
============== Diagnosis menu ==============
s: show status
c: show config
t: test motion
G: print config as JSON
T: print status as JSON
{: receive config JSON
F<filename>: set save filename
R: reboot board
p: print timing stats [us] and reset them
```

The commands are explained below. The board also prints `Ethernet link up` and `Ethernet link down` when the link of the Ethernet changes, and a message when it pauses or resumes the sends to a destination that does not answer.

## Status (`s`) {#status}

`s` shows the status of the hardware and of the firmware.

### Firmware {#status-firmware}

```
============== Current Status ==============
-------------- Firmware --------------
Firmware name : STEP400_R1_UNIVERSAL
Firmware version : 2.2.0
Compile date : Oct 20 2026, 10:00:00
Applicable config version : 1.2
Loaded config version : 1.2 [CONFIG_VERSION_APPLICABLE]
Config and product match : Yes
```

This part is about the firmware on the board. `Firmware name` depends on the product.

`Loaded config version` is the version of the configuration file that was read from the microSD card. You get one of these messages, depending on the versions of the configuration and of the firmware:

| Message | Description |
| --- | --- |
| CONFIG_VERSION_UNDEFINED | The version of the configuration is undefined |
| CONFIG_VERSION_NOTLOADED | No configuration was read from the microSD card |
| CONFIG_VERSION_OLD | The version of the configuration is old |
| CONFIG_VERSION_APPLICABLE | The versions of the configuration and of the firmware match |
| CONFIG_VERSION_NEW | The version of the configuration is newer than the firmware (the firmware is old) |

`Config and product match` is `No` when the product in the configuration file (`information.targetProduct`) is not the product of the board.

### DIP switch {#status-dip-switch}

```
-------------- DIP Switch --------------
BIN : 0000 0001
DEC : 1
```

The ID that the board reads from the DIP switch.

- `BIN`: the switches as 0 and 1. The lowest digit is on the right in this output, but on the left on the board (DIPSW1 of the STEP400).
- `DEC`: the ID as a decimal number.

### Ethernet {#status-ethernet}

```
-------------- Ethernet --------------
Ethernet hardware status: 3 -EthernetW5500
Ethernet link status: 1 -LinkON
isDestIpSet : Yes
Destination Ip : 10.0.0.10
Current My Ip : 10.0.0.101
Current MAC address : 60:95:CE:10:06:01
Destination MAC address : AA:BB:CC:DD:EE:FF
Current outPort : 50101
```

- `Ethernet hardware status`: the state of the Ethernet controller W5500. It is `EthernetW5500` when it works. `EthernetNoHardware` means that the board cannot talk to the W5500.
- `Ethernet link status`: `LinkON` (linked), `LinkOff` (not linked) or `Unknown` (the status cannot be read).
- `isDestIpSet`: `Yes` when the destination is set, that is, when [`/setDestIp`](../reference/system-settings.md#setdestip) was received (or the board may send before it) and the board can send OSC messages.
- `Destination Ip`, `Current My Ip`, `Current MAC address`, `Current outPort`: the destination, and the IP address, the MAC address and the sending port that the board uses now, with the ID added.
- `Destination MAC address`: the MAC address that the last send went to. It is `FF:FF:FF:FF:FF:FF` when the last send was a broadcast.

### microSD {#status-microsd}

```
-------------- microSD --------------
SD library initialize succeeded : Yes
SD config file open succeeded : Yes
SD config JSON parse succeeded : Yes
```

- `SD library initialize succeeded`: `No` when no card is inserted (or the card is exFAT).
- `SD config file open succeeded`: whether the configuration file on the card was opened.
- `SD config JSON parse succeeded`: whether the content of the file (JSON) was parsed. A file that was not accepted is not applied; see [Configuration with a microSD card](../connections/microsd-card.md#order).

### Motor driver {#status-motor-driver}

```
-------------- Motor Driver --------------
Motor driver SPI connection established : Yes
Driver ID#1
	ABS_POS: 0x00 (0step)
	EL_POS: 0x00 (Fullstep:0, Microstep:0)
	...
	OCD_TH: 0x0F (5000.0mA)
	STALL_TH: 0x1F (10000.0mA)
	...
	STATUS: 0xE603
	  High impedance state : Yes
	  BUSY : No
	  Motor direction : Reverse
	  Motor status : Stopped
	  UVLO (Undervoltage lock out) : No
	  UVLO_ADC (ADCIN undervoltage) : No
	  Thermal status : Normal
	  OCD (Overcurrent detection) : No
	  Stalled : No
	  SW_F: 0 -HOME sensor input open.
```

- `Motor driver SPI connection established`: `No` means that the board cannot talk to the driver ICs. The motor power may be off.
- The details of every driver are listed only when the connection works: the registers (position, speed, KVAL, thresholds, the alarm enable, the CONFIG register and its fields) and the STATUS register. The currents of `OCD_TH` and `STALL_TH` are calculated for the driver of the board. The driver ICs are listed for motors 1 to 4 (STEP400) or 1 to 8 (STEP800). On the STEP400 the line `UVLO_ADC` is shown too; a pressed LIMIT switch pulls ADCIN to GND and makes it `Yes`.
- The STATUS flags are read without clearing the latched flags.

### Modes {#status-modes}

```
-------------- Modes --------------
Servo Mode :  No, No, No, No
Current Mode :  No, No, No, No
Electromagnetic Brake Enable :  No, No, No, No
Brake status :
#1 : 0 ENGAGED
#2 : 0 ENGAGED
#3 : 0 ENGAGED
#4 : 0 ENGAGED
Homing status : 0, 0, 0, 0
```

- `Brake status` shows the state of the brake of each motor with its number: 0 ENGAGED, 1 RELEASING, 2 RELEASED, 3 STOPPING, 4 ENGAGING, 5 FREE. See [States of the brake](../guides/electromagnetic-brake.md#states). `Current Mode` is for the boards that have the current mode (the STEP400), and the brake lines for the boards that have the brake output.
- `Homing status`: the numbers of [`/homingStatus`](../reference/automatically-sent-messages.md#homingstatus).

## Configuration (`c`) {#config}

`c` shows the current running settings. This is not the content of the configuration file: it is what the board uses now, with the DIP switch and the changes that were made with OSC messages after the start. For example, the beginning when the board starts without a card is:

```
============== Configurations ==============
-------------- Config file --------------
SD config file open succeeded : No
SD config file parse succeeded : No
configTargetProduct : ---
Config and product match : No
configName : Default
config version : -1.0 [CONFIG_VERSION_NOTLOADED]
-------------- Network --------------
My Ip from Config : 10.0.0.100
isMyIpAddId : Yes
Dest Ip : 10.0.0.10
...
```

The items that are listed are the items of the configuration file; see [Configuration items](../connections/configuration-items.md). The addresses and the port that are shown with "from Config" are the values before the ID is added.

## Test motion (`t`) {#test-motion}

`t` makes all the motors rotate 25600 steps forward: one rotation for a 200-step motor at 1/128 microsteps. A motor that cannot start now (for example a motor with the brake enabled and the transition not done, or a motor in the servo mode) is skipped.

## Commands for the settings {#commands}

These commands are used by the [browser configuration tool](../connections/browser-config-tool.md). You can also send them from any serial terminal.

| Command | Description |
| --- | --- |
| `G` | Prints the running settings as one line of JSON |
| `T` | Prints the status of the board and the motors as one line of JSON |
| `{...}` | Applies a configuration JSON object and saves it to the card |
| `F<path>` | Sets the file that the next saves go to, until the next restart |
| `R` | Restarts the board |
| `p` | Prints the timing statistics and resets them |

- **`G`**: `board` (the product, the number of motors, the firmware version and the configuration file name) and the sections of the configuration.
- **`T`**: `board` has the product, the MCU (`mcu`), the reset cause (`resetCause`, and `resetCauseRaw` of the MCU), the firmware version, the IP address, the ID, the link, the destination MAC address (`destMac`, 6 numbers; 255 x 6 after a broadcast), `arpPending` (the MAC address of the destination is being resolved), and the state of the card and the configuration. Each element of `motors` has the position, speed, state, switch states and so on. `ocd` and `stall` are always false; use the OSC messages for them. The meaning of `resetCause` is in [`/booted`](../reference/automatically-sent-messages.md#booted).
- **`{...}`**: the board applies the settings, writes them to the card, and replies `{"result":"ok", ...}` or an error. **Stop the motors before you send it**: the board does not process anything while it saves (see [How the settings work](../connections/how-settings-work.md#saving)). When it takes effect: [When a change takes effect](../connections/how-settings-work.md#when).
- **`F<path>`**: see [The name set by `F<path>`](../connections/microsd-card.md#f-path) for the rules, and for the file names that the board does not read at the start.
- **`R`**: replies `{"result":"ok","message":"Rebooting..."}` first. The board waits at least 50 ms, stops the turning motors that have the brake enabled and not engaged, engages their brakes and waits for the transition duration (at most 1 s), and then restarts. See [Restart, watchdog and CPU fault](../guides/electromagnetic-brake.md#restart).
- **`p`**: the times of the loop and of the processing (maximum, average and count, in microseconds), and the counters of the sends and of the resolution of the MAC address of the destination (`udpSendFailed`, `udpSendDropped`, `arpResolve`, `arpProbe` and others). See [Resolving the MAC address](../guides/communication-and-messages.md#arp).
