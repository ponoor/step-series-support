## Sensor/switch connections
Each axis of the STEP400 and STEP800 has a `HOME` connector which allows for you to plug-in some form of limit switch or equivalent sensor. Additionally, the STEP400 has `LIMIT` inputs for each axis in addition to the `HOME` inputs.

### HOME
Since the stepper motor cannot track its own position, a dedicated sensor is required to return to the home position on boot-up. It is directly connected to the motor driver IC and can be used for position management. The pin is pulled up to 3v3 (3.3V) inside the driver IC.

### LIMIT
`STEP400 Only`

As stated above, the STEP400 has an additional `LIMIT` switch input that can be used to limit the operational range of each motor. You can configure these inputs to halt the motor, or to be used as another input for another purpose. Like the `HOME` input, this input is also pulled up to 3v3.

### Connection Terminals
We use the XA series connectors from JST (J.S.T.MFG.CO., LTD.). For compatible connectors, please refer to the following:

| Product name | Model number | Remarks
| ---- | ---- | ---- |
| (Reference) PCB Post | B03B-XASK-1 (LF)(SN) | Header mounted on the PCB |
| Housing | XAP-03V-1 | Plastic housing |
| Contact | BXA-001T-P0.6 | Crimp contact inserted into the housing |

### Pin assignments
The pin assignments for both inputs are the same. The pin number is printed on the housing.

| Pin number | Function |
| ---- | ---- |
| 1 | GND |
| 2 | Sensor/switch input |
| 3 | 5V output |

The driver responds when the input falls from `HIGH (3v3)` to `LOW (0V)`. Therefore, the switch must behave as "normally open".

For more information, please refer to [Homing and Position Management](https://ponoor.com/en/docs/step-series/functional-description/homing-and-position-management/).