---
title: Network and the DIP switch
---

# Network and the DIP switch

The DIP switch sets the ID of the board. This page explains how the ID is used, the initial network settings, and the MAC address.

## DIP switch settings {#dip-switch}

![](https://ponoor.com/cms/wp-content/uploads/2020/10/step400-dipSw.jpg)

The DIP switch on the board sets the ID. The ID is used in the replies to the OSC (Open Sound Control) messages, and it is added to the IP address, the destination port and the MAC address (see below).

The ID is a binary number of 8 digits, so it is from 0 to 255. A switch in the ON position counts as 1. On the STEP400, DIPSW1 is the lowest digit (1) and DIPSW8 is the highest digit (128). The STEP400 reads the 8 switches directly; the STEP800 reads them through a shift register. For how to set binary numbers with a DIP switch, see [Channel setting with DIP switches](https://www.soundhouse.co.jp/howto/light/dmx-dip/) (in Japanese).

The board reads the DIP switch not only at the start. If you change the ID while the board is running, it sets up the network again with the new ID. The USB serial command `s` shows the ID that the board reads; see [Diagnosis via USB serial port](../maintenance/usb-serial-diagnosis.md#status).

## Network settings {#network-settings}

### Initial settings {#initial}

The board uses these values when there is no configuration file or when the file does not have the key. "firmware" is the value in the firmware, and "template" is the value in the template files of the configuration tool; they are shown when they differ.

<!-- osc-settings-values: network -->
<!-- generated:begin osc-settings-values network -->
| Key | Name | Initial value | Range / Unit |
| --- | --- | --- | --- |
| [`network.myIp`](configuration-items.md#network-myip) | My IP address | 10.0.0.100 |  |
| [`network.isMyIpAddId`](configuration-items.md#network-ismyipaddid) | ID adds to my IP | true |  |
| [`network.destIp`](configuration-items.md#network-destip) | Destination IP | 10.0.0.10 |  |
| [`network.dns`](configuration-items.md#network-dns) | DNS | 10.0.0.1 |  |
| [`network.gateway`](configuration-items.md#network-gateway) | Gateway | 10.0.0.1 |  |
| [`network.subnet`](configuration-items.md#network-subnet) | Subnet mask | 255.255.255.0 |  |
| [`network.inPort`](configuration-items.md#network-inport) | Incoming port | 50000 |  |
| [`network.outPort`](configuration-items.md#network-outport) | Outgoing port | 50100 |  |
| [`network.isOutPortAddId`](configuration-items.md#network-isoutportaddid) | ID adds to Outgoing port | true |  |
| [`network.mac`](configuration-items.md#network-mac) | MAC address | STEP400: 60:95:CE:10:06:00 (firmware) / 60:95:CE:10:02:00 (template); STEP800: 60:95:CE:10:06:00 (firmware) / 60:95:CE:10:03:00 (template) |  |
| [`network.isMacAddId`](configuration-items.md#network-ismacaddid) | ID adds to MAC address | true |  |
| [`network.bootedMsgEnable`](configuration-items.md#network-bootedmsgenable) | Booted message enable | true |  |
| [`network.canSendMsgBeforeDestIp`](configuration-items.md#network-cansendmsgbeforedestip) | Allow OSC reply before /setDestIp | false |  |
| [`network.reportError`](configuration-items.md#network-reporterror) | Report errors | true |  |
<!-- generated:end osc-settings-values network -->

### Adding the ID to the IP address and the port {#adding-id}

In the initial state, the ID is added to the last number of the IP address, to the destination (OSC outgoing) port and to the MAC address. With this, you can use many boards with the same firmware and the same configuration file. If the receiving side can get the IP address of the sender of a message, you can switch off the addition to the port, and let all the boards send to the same port.

Each addition can be switched off in the settings: [`isMyIpAddId`](configuration-items.md#network-ismyipaddid), [`isOutPortAddId`](configuration-items.md#network-isoutportaddid) and [`isMacAddId`](configuration-items.md#network-ismacaddid).

The result must stay in the range:

- The last number of the IP address (`myIp`) plus the ID cannot exceed 254.
- The destination port (`outPort`) plus the ID cannot exceed 65535.

If it would, the board does not add the ID, uses the configured value as it is, and prints a warning on the USB serial port. Choose the IP address and the port so that the largest ID that you use stays in the range.

### MAC address {#mac-address}

Each board has its own MAC address, but the initial value is not that address: it is a MAC address of ours for tests. The MAC address of the board is printed on the sticker on the back of the board, under the sticker with the serial number. The number that starts with P is the serial number, and the 12 hexadecimal digits under it are the MAC address.

![](https://ponoor.com/cms/wp-content/uploads/2020/10/step400-solderside-mac-800x533.jpg)

To use it, set it as the MAC address in the configuration file or with the [browser configuration tool](browser-config-tool.md), save the configuration, and restart the board. See [How the settings work](how-settings-work.md). You can also change the initial value in the source of the firmware and build it; see [Compiling the firmware](../maintenance/compile-the-arduino-sketch.md).

### Destination {#destination}

The board sends its replies and messages to the destination IP address. Send [`/setDestIp`](../reference/system-settings.md#setdestip) to the board to set it. When to send it, and what happens in the network, are explained in [Communication and messages](../guides/communication-and-messages.md#setdestip).

### When the settings take effect {#when}

The IP address, the ports and the MAC address that you save in the configuration take effect after the board is restarted; the running values do not change. See [How the settings work](how-settings-work.md#when).

## Related commands {#related}

<!-- osc-related: /setDestIp -->
<!-- generated:begin osc-related /setDestIp -->
**Related commands**

| Command | Arguments | Description |
| --- | --- | --- |
| [`/setDestIp`](../reference/system-settings.md#setdestip) | - | Sets the destination IP address (`destIp`) to where the device should send messages to, when it replies to a query or report internal state changes, etc. |
<!-- generated:end osc-related /setDestIp -->
