## DIP switch settings
<img src="https://ponoor.com/cms/wp-content/uploads/2020/10/step400-dipSw.jpg" width="600" />

The DIP switch specifies the ID that is used to reply to OSC messages and is also reflected in the local IP address and expected server port number. 
The ID is set in binary digits. For more information on setting the DIP switches in binary digits, click here.
[Channel setting with DIP switches](https://www.soundhouse.co.jp/howto/light/dmx-dip/)

## Network settings
### Initial settings
| Item | Initial value |
| ---- | ---- |
| IP address | 10.0.0.100+ID |
| MAC address | 0x60, 0x95, 0xCE, 0x10, 0x02, 0x00+ID |
| Server (or Destination) IP address | 10.0.0.10 |
| Local (or OSC incoming) port | 50000 |
| Server (or OSC outgoing) port | 50100+ID |

### IP Address and OSC Message Port
In its initial state, an ID will be added to IP address's final octet and the server (OSC outgoing) port.
With this mechanism, you are able to operate multiple devices with the same firmware and settings file. On the server, if you are able to retrieve the IP address of the device, you can configure the device to not add its ID to the expected server port.

This feature can be disabled via the microSD card configuration.

### MAC address
A unique MAC address is assigned to the device; however, its initial value is set as seen in the table above. The unique MAC address is printed on the sticker on the bottom of the device beneath another sticker that should contain the device's serial number. 

![](https://ponoor.com/cms/wp-content/uploads/2020/10/step400-solderside-mac-800x533.jpg)

To use the assigned MAC address, please generate the settings file from the [configTool](https://ponoor.com/docs/en/step-series/settings/setup-with-a-microsd-card/) and load it onto the microSD card.


### Initializing with microSD card
You can export the network settings and other initial values from the Configuration Tool, store them in a microSD card, and load them into STEP400. For details, see [Setup with a microSD card](https://ponoor.com/en/docs/step-series/settings/setup-with-a-microsd-card/).