## Sensor/switch connections
Each axis of STEP400/STEP800 has HOME connector which can connect sensors or switches. STEP400 has LIMIT sensor inputs in addition to HOME inputs.

The roles of each connectors are the following:

### HOME
Input connector terminal for home position detection. Since the stepper motor cannot detect its own position, a dedicated sensor is required to return to the home position on boot. It is directly connected to the motor driver IC and can be used for position management for the driver. The input pin is pulled up to 3.3 V inside the driver IC.

### LIMIT
Only available in STEP400.

Other than the HOME connector, there is a LIMIT connector that can be used to limit mechanical operating range for each motor. You can configure these pins to halt the corresponding motor, but it can be used for another purpose as well. The input terminal is pulled up to 3.3V.

### Connection Terminals
We use XA series connectors from JST (J.S.T.MFG.CO.,LTD.) . For compatible connectors, please refer to the following:

| Product name | Model number | Remarks
| ---- | ---- | ---- |
| (Reference) PCB Post | B03B-XASK-1 (LF)(SN) | Parts mounted on the PCB.|
| Housing | XAP-03V-1 | Main body of the connector. |
| Contact | BXA-001T-P0.6 | Crimp part to be inserted into housing. |

### Pin assignment
The pin assignments are the same for HOME and LIMIT.

| Pin number | Function |
| ---- | ---- |
| 1 | GND |
| 2 | Sensor/switch input |
| 3 | 5V output |

The driver responds when the input level falls from High (3.3v) to Low (0V). Therefore, the mechanism and sensor (or switch) must be combined in such a way that the contacts are open under normal state (normal open).

For more information, please refer to [Homing and Position Management](https://ponoor.com/en/docs/step-series/functional-description/homing-and-position-management/).