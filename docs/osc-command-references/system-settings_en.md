## System settings
### `/setDestIp`
#### Argument
None

#### Executable timing
Always

#### Description
Sets the destination IP address (`destIp`) to where the device should send messages to, when it replies to a query or report internal state changes, etc.
The board sets the `destIp` to the sender of this message .

Also, until `destIp` is set, no OSC messages will be sent from the device, so send this command first. One single exception is the `/booted` message.

From the Config Tool, you can set the board to start sending out the OSC message without waiting the `destIp` to be set.

#### Response
```
/destIp (int)destIp[0] (int)destIp[1] (int)destIp[2] (int)destIp[3] (bool)isNewDestIp
```
| Argument | Range | Description |
| --- | --- | --- |
| destIp[0-3] | 0-255 | Each byte of destIp |
| isNewDestIp | 0-1 | Indicates if destIp has been changed. 1 if it has been changed, or 0 if the same address has already been set. |

#### Initial value
10.0.0.10

### `/getVersion`
#### Argument
None

#### Executable timing
Always

#### Description
Returns the firmware version burnt on the chip.

#### Response

```
/version (Symbol)firmwareName (Symbol)firmwareVersion (Symbol)compileDate
```
| Argument | Description |
| --- | --- |
| firmwareName | Name of the firmware |
| firmwareVersion | Firmware version |
| compileDate | Compile date of the firmware |

### `/getConfigName`
#### Argument
None

#### Executable timing
Always

#### Description
Returns the name of the configuration file read from the micro SD card on system boot.

#### Response

```
/configName (Symbol)configName (bool)sdInitializeSucceeded (bool)configFileOpenSucceeded (bool)configFileParseSucceeded
```
| Argument | Description |
| --- | --- |
| configName | The name of the configuration |
| sdInitializeSucceeded | If the reading from microSD card was successful. |
| configFileOpenSucceeded | If the device could open the configuration file successfully. |
| configFileParseSucceeded | If the config Json data could be parsed successfully. |

### `/reportError (bool)enable`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| enable | 0-1 | 1 for enabled, 0 for disabled |

#### Executable timing
Always

#### Description
Enables or disables the automatic message notification for [`/error/command`](https://ponoor.com/en/docs/step-series/https://ponoor.com/en/docs/step-series/osc-command-reference/automatically-sent-messages-from-step-400/#errorcommand) and [`/error/osc`](https://ponoor.com/en/docs/step-series/osc-command-reference/automatically-sent-messages-from-step-400/#errorosc).

#### Initial value
1 (Enabled)