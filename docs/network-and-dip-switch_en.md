## DIP switch settings
<img src="https://ponoor.com/cms/wp-content/uploads/2020/10/step400-dipSw.jpg" width="600" />

The DIP switch specifies the STEP400 ID that is used to reply to OSC messages, and is also reflected in the IP address and send port number.
The ID is set in binary digits. For more information on setting the DIP switches in binary digits, click here.
[Channel setting with DIP switches](https://www.soundhouse.co.jp/howto/light/dmx-dip/)

## Network settings
### Initial settings
| Item | Initial value |
| ---- | ---- |
| IP address | 10.0.0.100+ID |
| MAC address | 0x60, 0x95, 0xCE, 0x10, 0x02, 0x00+ID |
| Destination address | 10.0.0.10 |
| OSC incoming port | 50000 |
| OSC outgoing port | 50100+ID |

### IP Address and OSC Message Port
In it's initial state, an ID will be added to the IP Address's final byte and the OSC message port. With this mechanism, you can operate multiple devices with same firmware and settings file. For the OSC message port, in case you can retrieve the IP address of the sender, you can set to send the messages to the same port number without adding its ID.

This feature can be turned off with initial setup from the microSD card.

### MAC address
An individual mac address is assigned to the device, however the initial value is set as above. This is one of the MAC addresses we acquired and used for the test in the company.

Every device has individual MAC address assigned and it can be found on the sticker on the rear side.
![](https://ponoor.com/cms/wp-content/uploads/2020/10/step400-solderside-mac-800x533.jpg)

Above number which starts from P, is the serial number. And the lower 12 hex number is the MAC address. 
To use the assigned mac address, please generate setting file from [configTool](https://ponoor.com/docs/en/step-series/settings/setup-with-a-microsd-card/), load it to the microSD card. You can also hard-code the address directly into their firmware, compile and upload to the controller.

### Initializing with microSD card
You can export the network settings and other initial values from the Configuration Tool, store them in a microSD card, and load them into STEP400. For details, see [Setup with a microSD card](https://ponoor.com/en/docs/step-series/settings/setup-with-a-microsd-card/).