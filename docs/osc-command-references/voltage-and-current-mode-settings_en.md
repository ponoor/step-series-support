## Voltage mode
### `/setVoltageMode (int)motorID`
**STEP400 only**
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4, 255|motor ID|

#### Executable timing
HiZ State

#### Description
Switches the specified motor to the voltage drive mode.

Note: This command is only available in STEP400.
STEP800 is always in this voltage mode and cannot change.

### `/setKval (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)setDecKVAL`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|holdKVAL|0-255|KVAL when stopped|
|runKVAL|0-255|KVAL in constant speed operation|
|accKVAL|0-255|KVAL during acceleration|
|setDecKVAL|0-255|KVAL during deceleration|

#### Executable timing
Always

#### Description
Sets the four KVALs together.

#### Initial value
16

### `/getKval (int)motorID`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|

#### Executable timing
Always

#### Description
Get the four KVALs together.

#### Response
```
/kval (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)setDecKVAL
```

|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|holdKVAL|0-255|KVAL when stopped|
|runKVAL|0-255|KVAL in constant speed operation|
|accKVAL|0-255|KVAL during acceleration|
|setDecKVAL|0-255|KVAL during deceleration|

### `/setBemfParam (int)motorID (int)INT_SPEED (int)ST_SLP (int)FN_SLP_ACC (int)FN_SLP_DEC`

#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |
| INT_SPEED | 0-16383(0x3FFF) | INT_SPEED register value |
| ST_SLP | 0-255(0xFF) | ST_SLP register value |
| FN_SLP_ACC | 0-255(0xFF) | FN_SLP_ACC register value |
| FN_SLP_DEC | 0-255(0xFF) | FN_SLP_DEC register value |


#### Executable timing
High Z state

#### Description
Sets BEMF compensation parameter register. For the values for each parameter, refer [voltage mode and current mode](https://ponoor.com/en/docs/step-series/functional-description/voltage-mode-and-current-mode/#i-2).

#### Initial value
| Argument | Initial value |
| --- | --- |
| INT_SPEED | 1032 (0x0402) |
| ST_SLP | 25 (0x19) |
| FN_SLP_ACC | 41 (0x29) |
| FN_SLP_DEC | 41 (0x29) |

### `/getBemfParam (int)motorID`
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4/1-8, 255 | Motor ID |

#### Executable timing
Always

#### Description
Get register values for the BEMF parameter.

#### Response
```
/bemfParam (int)motorID (int)INT_SPEED (int)ST_SLP (int)FN_SLP_ACC (int)FN_SLP_DEC
```
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4 | Motor ID |
| INT_SPEED | 0-16383(0x3FFF) | INT_SPEED register value |
| ST_SLP | 0-255(0xFF) | ST_SLP register value |
| FN_SLP_ACC | 0-255(0xFF) | FN_SLP_ACC register value |
| FN_SLP_DEC | 0-255(0xFF) | FN_SLP_DEC register value |

<!--

### `/setHoldKval (int)motorID (int)holdKVAL`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|holdKVAL|0-255|KVAL when stopped|

#### Executable timing
Always

#### Description
Sets only KVAL when stopped.

#### Initial value
16

### `/setRunKval (int)motorID (int)runKVAL`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|setRunKVAL|0-255|KVAL in constant speed operation|

#### Executable timing
Always

#### Description
Sets only KVAL in constant speed operation.

#### Initial value
16

### `/setAccKval (int)motorID (int)accKVAL`
- `motorID` : 1-4/1-8, 255
- `accKVAL` : 0-255

Timing: Always

Sets only KVAL during acceleration.

### `/setDecKval (int)motorID (int)decKVAL`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|decKVAL|0-255|KVAL during deceleration|

#### Executable timing
Always

#### Description
Sets only KVAL during deceleration.

#### Initial value
16

-->

## Current mode
### `/setCurrentMode (int)motorID`
**STEP400 only**
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4, 255|motor ID|

#### Executable timing
High Z State

#### Description
Switches the specified motor to the current drive mode.

### `/setTval (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)setDecTVAL`
**STEP400 only**
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4, 255|motor ID|
|holdTVAL|0-127|TVAL when stopped|
|runTVAL|0-127|TVAL in constant speed operation|
|accTVAL|0-127|TVAL during acceleration|
|setDecTVAL|0-127|TVAL during deceleration|

#### Executable timing
Always

#### Description
Sets the four TVALs together.
In STEP 400, the TVAL is as follows.

| TVAL | Setting value[mA] |
| --- | --- |
| 0 | 78mA |
| 1 | 156mA |
| ... | ... |
| 127 | 9,984mA |

#### Initial value
16 (1328.125mA)

### `/getTval (int)motorID`
**STEP400 only**
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4, 255|motor ID|

#### Executable timing
Always

#### Description
Get the four TVAL types together.

#### Response
```
/tval (int)motorID (int)holdTVAL (int)runTVAL (int)accTVAL (int)decTVAL
```

|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|holdTVAL|0-127|TVAL when stopped|
|runTVAL|0-127|TVAL in constant speed operation|
|accTVAL|0-127|TVAL during acceleration|
|setDecTVAL|0-127|TVAL during deceleration|

### `/setDecayModeParam (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN`
**STEP400 only**
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4, 255 | Motor ID |
| T_FAST | 0-255(0xFF) | T_FAST register value |
| TON_MIN | 0-255(0xFF) | TON_MIN register value |
| TOFF_MIN | 0-255(0xFF) | TOFF_MIN register value |


#### Executable timing
High Z state

#### Description
Sets registers for the current control algorithm parameters. For the each register values, refer the datasheet of the PowerSTEP01.

#### Initial value
| Argument | Initial value |
| --- | --- |
| T_FAST | 25 (0x19) |
| TON_MIN | 41 (0x29) |
| TOFF_MIN | 41 (0x29) |

### `/getDecayModeParam (int)motorID`
**STEP400 only**
#### Argument
| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4, 255 | Motor ID |

#### Executable timing
Always

#### Description
Retrieves the register values for the current control algorithm parameters.

#### Response
```
/decayModeParam (int)motorID (int)T_FAST (int)TON_MIN (int)TOFF_MIN
```

| Argument | Range | Description |
| --- | --- | --- |
| motorID | 1-4 | Motor ID |
| T_FAST | 0-255(0xFF) | T_FAST register value |
| TON_MIN | 0-255(0xFF) | TON_MIN register value |
| TOFF_MIN | 0-255(0xFF) | TOFF_MIN register value |

<!--

### `/setHoldTval (int)motorID (int)holdTVAL`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|holdTVAL|0-255|TVAL when stopped|

#### Executable timing
Always

#### Description
Sets only TVAL when stopped.

#### Initial value
16 (1328.125mA)

### `/setRunTval (int)motorID (int)runTVAL`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|setRunTVAL|0-255|TVAL in constant speed operation|

#### Executable timing
Always

#### Description
Sets only TVAL in constant speed operation.

#### Initial value
16 (1328.125mA)

### `/setAccTval (int)motorID (int)accTVAL`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|accTVAL|0-255|TVAL during acceleration|

#### Executable timing
Always

#### Description
Sets only TVAL during acceleration.

#### Initial value
16 (1328.125mA)

### `/setDecTval (int)motorID (int)decTVAL`
#### Argument
|Argument|Range|Description|
|---|---|---|
|motorID|1-4/1-8, 255|motor ID|
|decTVAL|0-255|TVAL during deceleration|

#### Executable timing
Always

#### Description
Sets only TVAL during deceleration.

#### Initial value
16 (1328.125mA)

-->