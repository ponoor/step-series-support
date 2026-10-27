---
title: Communication and messages
---

# Communication and messages

This page explains how the board exchanges OSC (Open Sound Control) messages with your computer: how it learns where to send them, what it sends by itself, and what it does with the arguments it receives.

## Overview {#overview}

The board receives OSC messages as UDP packets. It sends two kinds of messages back: the **replies** to the commands that ask for something (such as [`/getVersion`](../reference/system-settings.md#getversion)), and the messages that it sends **by itself** when something happens or at a fixed interval (such as [`/busy`](../reference/automatically-sent-messages.md#busy) or [`/position`](../reference/automatically-sent-messages.md#position)). Both go to the **destination**, the IP address and port that the board keeps for this purpose.

For how to set the IP address of the board, the port numbers and the DIP switch, see [Network and DIP switch](../connections/network-and-dip-switch.md). They are not repeated here.

## The destination and `/setDestIp` {#setdestip}

### When to send `/setDestIp` {#when}

The board does not know where to send messages until it receives [`/setDestIp`](../reference/system-settings.md#setdestip): it takes the sender of this message as the destination. Until then it sends nothing, except the broadcast [`/booted`](../reference/automatically-sent-messages.md#booted). (With [`network.canSendMsgBeforeDestIp`](../connections/configuration-items.md#network-cansendmsgbeforedestip) set, the board sends to [`network.destIp`](../connections/configuration-items.md#network-destip) from the start.)

Send `/setDestIp`:

- at the start of the connection, and
- when the network or the computer changes: another computer or network adapter with the same IP address, or a switch between Wi-Fi and wired. When you replace the computer, wait at least 1.5 s after the last message that the old one sent.

Without it, the board keeps sending to the MAC address of the old computer. Your commands still work, but no reply and no report reaches you. (When the computer is connected directly and the link goes down and up again, the board recovers by itself; through a switch it does not.)

### Resolving the MAC address {#arp}

When the destination is set (or changes) by a `/setDestIp` that is from a new address, or comes 1.5 s or more after the last packet from the destination (a `/setDestIp` sent every second as a heartbeat does not start it), the board has to find the MAC address of the destination. It sends one byte of UDP to port 9 (discard) of the broadcast address, then one byte to port 9 of the destination at once and every 150 ms, until the destination answers the ARP request or a few seconds have passed. The computer may answer each of these packets with an ICMP port unreachable message, which is harmless; it can show up in the log of a firewall.

The reply [`/destIp`](../reference/system-settings.md#setdestip) of the `/setDestIp` that starts this resolution is sent when the resolution is done. On a wired network it comes a few ms after the command; **when the computer is on Wi-Fi it can take up to a few seconds**. If [`/destIp`](../reference/system-settings.md#setdestip) does not come, send `/setDestIp` again.

While the MAC address is being resolved (after such a `/setDestIp`, and after the link comes up again; also after the board starts, when it sends before `/setDestIp`), the messages to the destination are **dropped**, not sent later: no replies and no reports arrive. The broadcast `/booted` is still sent.

While the board waits for a destination that does not answer the ARP request, it cannot process OSC messages: each probe that fails stops the processing for up to about 41 ms, and the probes come every 150 ms. A wired computer answers the first probe at once; a computer on Wi-Fi often needs several, so the processing stops repeatedly during the resolution. This disturbs the monitoring of the electromagnetic brake and the servo mode. **We recommend that you send `/setDestIp` while the motors are stopped.**

A send to a destination that has never answered ARP (for example a wrong destination address) fails. The board then pauses all the sends to that destination for 1 s and drops the messages in that time; after that it tries again with the next message. A packet that arrives from the destination resumes the sends at once.

### Checking the connection {#keepalive}

To check that the board is alive, send a command that has a reply, such as `/getVersion`. Do not use `/setDestIp` for this.

## Replies and messages that the board sends by itself {#messages}

- **Replies.** A command that asks for a value (`/get...`) is answered with a message, and so are some set commands. What a command returns is written in its reference.
- **Notifications of changes.** The board reads the state of the drivers every 5 ms and sends a message when the state changes: [`/busy`](../reference/automatically-sent-messages.md#busy), [`/HiZ`](../reference/automatically-sent-messages.md#hiz), [`/dir`](../reference/automatically-sent-messages.md#dir), [`/motorStatus`](../reference/automatically-sent-messages.md#motorstatus), [`/homeSw`](../reference/automatically-sent-messages.md#homesw), [`/limitSw`](../reference/automatically-sent-messages.md#limitsw), [`/swEvent`](../reference/automatically-sent-messages.md#swevent), [`/uvlo`](../reference/automatically-sent-messages.md#uvlo), [`/thermalStatus`](../reference/automatically-sent-messages.md#thermalstatus), [`/overCurrent`](../reference/automatically-sent-messages.md#overcurrent), [`/stall`](../reference/automatically-sent-messages.md#stall) and so on. Each of them is turned on and off with its own `/enable...Report` command, and the settings of the board decide which of them are on at the start. A state is sent only when it changes. For the alarms see [Alarms and protection](alarms-and-protection.md#timing).
- **Reports at a fixed interval.** [`/setPositionReportInterval`](../reference/motor-driver-settings.md#setpositionreportinterval) makes the board send [`/position`](../reference/automatically-sent-messages.md#position) of a motor at an interval, and [`/setPositionListReportInterval`](../reference/motor-driver-settings.md#setpositionlistreportinterval) makes it send the positions of all the motors in a single message, [`/positionList`](../reference/automatically-sent-messages.md#positionlist). To get the positions of all the motors at short intervals, use the list report: it needs much less of the CPU of the board than one report per motor.
- **[`/booted`](../reference/automatically-sent-messages.md#booted)** is broadcast when the board starts. It contains the reason of the reset.

The full list is in [Automatically sent messages](../reference/automatically-sent-messages.md).

## The arguments that the board receives {#arguments}

The board checks the arguments of a command before it applies the command. When a check fails, **nothing is applied**.

| Case | Message |
| --- | --- |
| Fewer arguments than the command needs | [`/error/osc`](../reference/automatically-sent-messages.md#error-osc) `MissingArgument` |
| An argument of the wrong type (a string where a number is needed, NaN or infinity, or a non-string for `/setConfigName`) | `/error/osc` `WrongDataType` |
| A motor ID that the board does not have (not a motor of the board, and not 255), or outside 0-255 | [`/error/command`](../reference/automatically-sent-messages.md#error-command) `MotorIdNotMatch`, with the motor ID that was sent |
| A value outside the range of the command | `/error/command` `CommandIgnored` |
| A packet larger than 512 bytes, or more than 16 arguments | `/error/osc` `OscSyntaxError` |

Before v2.2.0, missing arguments and arguments of the wrong type were applied as 0. For example `/setKval 1` set every KVAL of the motor to 0.

- Arguments beyond the ones that a command needs are ignored.
- Some commands do not reject a value outside the range but limit it or wrap it around. The reference of each command says which; see also the [common rules](../reference/index.md#messages-to-the-board).
- An integer and a floating-point number are converted into each other. **Send a logical value as the integer 0 or 1** (type tag `i`); that is how the STEP Series defines it, and the board always sends logical values this way. The board also accepts a number (an integer greater than 0, or a float of 1.0 or more, is true) and the OSC values True and False.
- OSC bundles are not supported.

## Errors {#errors}

Two messages report errors:

- [`/error/osc`](../reference/automatically-sent-messages.md#error-osc): the message itself could not be used: a missing argument, a wrong type, a syntax error, or an address that the board does not know (`MessageNotMatch`).
- [`/error/command`](../reference/automatically-sent-messages.md#error-command): the message was understood, but the command could not be executed or was not applied: the state of the motor does not allow it (`MotorNotHiZ`, `BrakeEngaged`, `InServoMode`, ...), a value was out of the range, a motor ID did not exist, a timeout elapsed.

With [`/reportError`](../reference/system-settings.md#reporterror) set to 0, the board sends neither of them. The list of the errors is in [Automatically sent messages](../reference/automatically-sent-messages.md#error-command), and the errors of a command are listed in its reference.

## Diagnosis {#diagnosis}

The USB serial port shows the MAC address of the destination and more about the connection. See [USB serial diagnosis](../maintenance/usb-serial-diagnosis.md).

## Related commands and settings {#related}

<!-- osc-related: system, /setPositionReportInterval, /setPositionListReportInterval -->
<!-- generated:begin osc-related system, /setPositionReportInterval, /setPositionListReportInterval -->
**Related commands**

| Command | Arguments | Description |
| --- | --- | --- |
| [`/setDestIp`](../reference/system-settings.md#setdestip) | - | Sets the destination IP address (`destIp`) to where the device should send messages to, when it replies to a query or report internal state changes, etc. |
| [`/getVersion`](../reference/system-settings.md#getversion) | - | Returns the firmware version burnt on the chip. |
| [`/getConfigName`](../reference/system-settings.md#getconfigname) | - | Returns `/configName`: the configuration name, whether the microSD card could be used, whether a configuration file was opened and parsed, and the path of the file. |
| [`/reportError`](../reference/system-settings.md#reporterror) | (bool)enable | Enables or disables the automatic message notification for `/error/command` and `/error/osc`. |
| [`/setConfigName`](../reference/system-settings.md#setconfigname) | (string)configName | Sets the configuration name stored in the device. |
| [`/saveConfig`](../reference/system-settings.md#saveconfig) | - | Saves the current running configuration to the microSD card as a JSON file. |
| [`/resetDevice`](../reference/system-settings.md#resetdevice) | - | Resets the entire device. |
| [`/setPositionReportInterval`](../reference/motor-driver-settings.md#setpositionreportinterval) | (int)motorID (int)interval | Send the current position (`ABS_POS`) of the specified motor with the specified interval. |
| [`/setPositionListReportInterval`](../reference/motor-driver-settings.md#setpositionlistreportinterval) | (int)interval | Send a single message with a list of the current position (`ABS_POS`) of all motors with the specified interval. |
<!-- generated:end osc-related system, /setPositionReportInterval, /setPositionListReportInterval -->

<!-- osc-settings: network -->
<!-- generated:begin osc-settings network -->
**Related configuration items**

| Key | Name | Commands |
| --- | --- | --- |
| [`network.myIp`](../connections/configuration-items.md#network-myip) | My IP address |  |
| [`network.isMyIpAddId`](../connections/configuration-items.md#network-ismyipaddid) | ID adds to my IP |  |
| [`network.destIp`](../connections/configuration-items.md#network-destip) | Destination IP | `/setDestIp` |
| [`network.dns`](../connections/configuration-items.md#network-dns) | DNS |  |
| [`network.gateway`](../connections/configuration-items.md#network-gateway) | Gateway |  |
| [`network.subnet`](../connections/configuration-items.md#network-subnet) | Subnet mask |  |
| [`network.inPort`](../connections/configuration-items.md#network-inport) | Incoming port |  |
| [`network.outPort`](../connections/configuration-items.md#network-outport) | Outgoing port |  |
| [`network.isOutPortAddId`](../connections/configuration-items.md#network-isoutportaddid) | ID adds to Outgoing port |  |
| [`network.mac`](../connections/configuration-items.md#network-mac) | MAC address |  |
| [`network.isMacAddId`](../connections/configuration-items.md#network-ismacaddid) | ID adds to MAC address |  |
| [`network.bootedMsgEnable`](../connections/configuration-items.md#network-bootedmsgenable) | Booted message enable |  |
| [`network.canSendMsgBeforeDestIp`](../connections/configuration-items.md#network-cansendmsgbeforedestip) | Allow OSC reply before /setDestIp |  |
| [`network.reportError`](../connections/configuration-items.md#network-reporterror) | Report errors | `/reportError` |
<!-- generated:end osc-settings network -->
