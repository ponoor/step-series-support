### `/homing (int)motorID`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |

#### Executable timing
Always

#### Description
Start the homing movement. Move towards origin direction, stop when the HOME switch is activated. Then the motor reverses the direction and move slowly, halts when the HOME sensor is not active anymore, then reset location to zero at the current point.

This is equivalent to the following actions of executing [`/goUntil`](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed) command, and after the motor stops on HOME sensor activation, execute [`/releaseSW`](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#releasesw_intmotorid_boolact_booldir) command.

The `homingDirection` and the `homingSpeed` can be set by [`/setHomingDirection`](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#sethomingdirection_intmotorid_booldirection)and [`/setHomingSpeed`](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#sethomingspeed_intmotorid_floatspeed) commands, as well as configuring from the configTool.

Time-out can be set for each of the `/goUntil` and `/releaseSw` commands. The controller halts the motor movement if the sensor state have not changed during this time frame. The time-out values can be set from [`/setGoUntilTimeout`](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#setgountiltimeout_intmotorid_inttimeout) and from [`setReleaseSwTimeout`](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#setreleaseswtimeout_intmotorid_inttimeout) command.

Depending on the state change on the homing movement, following response will be sent.

#### Response
```
/homingStatus (int)motorID (int)homingStatus
```

| Argument | Range | Description |
|---|---|---|
| motorID | 1-4/1-8, 255 | Motor ID |
| homingStatus | 0-4 | Homing Status |

##### Homing Status
| homingStatus | Homing Status | Description |
| --- | --- | --- |
| 0 | HOMING_UNDEFINED | Not yet executing homing movement |
| 1 | HOMING_GOUNTIL | Executing `/goUntil` |
| 2 | HOMING_RELEASESW | Executing `/releaseSw` |
| 3 | HOMIMG_COMPLETED | Homing done |
| 4 | HOMING_TIMEOUT | The movement did not complete during specified time frame. |

### `/getHomingStatus (int)motorID`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |

#### Executable timing
Always

#### Description
Returns current state of homing movement.

#### Response
Same as [`/homing`](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#homing_intmotorid) command.

### `/setHomingDirection (int)motorID (bool)direction`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |
| direction | 0-1 | 1:Forward, 0:Reverse |

#### Executable timing
Always

#### Description
Sets the `homingDirection` for the [`/homing`](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#homing_intmotorid) command. It can be also configured from the configTool.

#### Description
0 (Reverse)

### `/getHomingDirection (int)motorID`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |

#### Executable timing
Always

#### Description
Returns `homingDirection` parameter.

#### Response
```
/homingDirection (int)motorID (bool)homingDirection
```

| Argument | Range | Description |
|---|---|---|
|motorID|1-4/1-8|Motor ID|
| homingDirection | 0-1 | 1:Forward, 0:Reverse |

### `/setHomingSpeed (int)motorID (float)speed`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |
| speed | 0.0-15625.0[step/s] | homingSpeed |

#### Executable timing
Always

#### Description
Sets the `homingSpeed` when executing the command [`/homing`](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#homing_intmotorid). It can be configured from the configTool.

#### Initial value
100.0[step/s]

### `/getHomingSpeed (int)motorID`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |

#### Executable timing
Always

#### Description.
Returns `homingSpeed` parameter.

#### Response
```
/homingSpeed (int)motorID (float)homingSpeed
```

| Argument | Range | Description |
|---|---|---|
|motorID|1-4/1-8|Motor ID|
| homingSpeed | 0.0-15625.0[step/s] | Homing Speed |

### `/goUntil (int)motorID (bool)ACT (float)speed`
#### Argument
| Argument | Range | Description |
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|ACT|0-1| Refer to the table below |
|speed|-15625 - 15625 [step/s]||

| ACT | Description |
| --- | --- |
| 0 | Reset the ABS_POS register |
| 1 | Copy the value of the ASB_POS register to the MARK register |

#### Executable timing
Always

#### Description
Move the motor at specified speed and direction. When the HOME switch turns on (the HOME switch terminal is closed), process ABS_POS register according to the ACT value.
The motor will softStop afterwards, but if the SW_MODE is set to 0 in the `/setSwMode` command, it will be a hardStop instead. This command will keep the motor to the BUSY state until it stops.

#### Response
None

### `/setGoUntilTimeout (int)motorID (int)timeOut`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |
| timeOut | 0-65535[ms] | Time-out duration |

#### Executable timing
Always

#### Description
Sets the time-out duration when executing [`/goUntil`](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed) command. If the sensor did not detect during this time frame, the controller will regard time-out and halts the movement. Specify 0 to disable the timeout. It can also be configured from the configTool.

#### Description
10000[ms]

### `/getGoUntilTimeout (int)motorID`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |

#### Executable timing
Always

#### Description
Returns the time-out duration when executing [`/goUntil`](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed) command.

#### Response
```
/goUntilTimeout (int)motorID (int)timeout
```

#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |
| timeout | 0-65535[ms] | Time-out duration |


### `/releaseSw (int)motorID (bool)ACT (bool)DIR`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|ACT|0-1| Refer to the table below |
|DIR|0-1| Refer to the table below |

| ACT | Description |
| --- | --- |
| 0 | Reset the ABS_POS register |
| 1 | Copy the value of the ASB_POS register to the MARK register |

| DIR | Motor direction |
| --- | --- |
| 1 | Forward |
| 0 | Reverse |

#### Executable timing
Always

#### Description
Move at minimum speed (5[step/s] by default) in the specified direction until the HOME switch pin becomes open. Then it will process the ABS_POS register according to the value of ACT. The process of the ACT is same as the [`/goUntil`](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed) command. Then halt the motor with hardStop.

#### Response
None

### `/setReleaseSwTimeout (int)motorID (int)timeOut`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |
| timeOut | 0-65535[ms] | Time-out duration |

#### Executable timing
Always

#### Description
Sets the time-out duration when executing [`/releaseSw`](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#releasesw_intmotorid_boolact_booldir) command. If the sensor cannot be released during this time frame, halt the movement as time-out. Specify 0 to disable the timeout. It can be configured from the configTool.

#### Initial value
5000[ms]

#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |

#### Executable timing
Always

#### Description
Returns the time-out duration when executing [`/releaseSw`](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#releasesw_intmotorid_boolact_booldir) command.

#### Response
```
/releaseSwTimeout (int)motorID (int)timeout
```

#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |
| timeout | 0-10000[ms] | Time-out duration |