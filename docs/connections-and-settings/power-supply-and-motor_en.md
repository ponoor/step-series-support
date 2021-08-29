## Connecting a power supply

### Power supplies for STEP400
The power sections are different between STEP400 and STEP800 as following;

| Product | Voltage rating (Absolute maximum supply voltage) |
| --- | --- |
| STEP400 | 12V-76V |
| STEP800 | 9V-36V |


Supplied voltage will directly fed to the motor driver. It is also stepped down to 5V and 3.3V on the board for control power source. If a PC or another device is connected to the USB port, only the control power will be supplied to the board. The required power supply capacity depends on the type and number of motors as well as the drive voltage.

### Terminal for the power supply
There are 2 types of power input terminals on this device, a DC jack (4) and a screw terminal(5).
<img src="https://ponoor.com/cms/wp-content/uploads/2020/10/step400_connectors_numbering.jpg" width="600" />

| Number | Description |
| --- | --- |
| 1  | Connector for the electromagnetic brake (STEP400) |
| 2  | Ethernet |
| 3  | USB type-C  |
| 4  | DC Jack  |
| 5  | Screw terminal block for power supply |

The DC jack and screw terminal are connected parallel on the board. **Avoid supplying both at the same time, as it may cause short circuit.**

#### DC jack
- 5.5mm outer diameter
- 2.1mm inner diameter
- center positive
The rating of the DC jack are limited to 24V/5A. Use the screw terminal if you want to supply much higher voltage or larger current.

#### Screw terminal
If you see the connector from the edge of the board, left side is negative and right side is positive terminal. The screw diameter is M3. You can fasten the cupper wire directly, but you can also use a dedicated terminal for a more secure connection. Some compatible terminals are:

- NICHIFU TMEX1.25-3N

## Motor connection

### Motor Selection
This device can be used with bipolar stepper motors, and it's phase current is depended on the products;

| Product | Phase Current |
| --- | --- |
| STEP400 | 5A or less |
| STEP800 | 2A or less |


We have calculated register values for some motors based on our actual measurements and made them available in the form of configuration files. They can be found from following URL:

https://ponoor.com/en/docs/step-series/settings/example-parameter-values-for-example-steppers/

### Terminal for motors
<img src="https://ponoor.com/cms/wp-content/uploads/2020/10/image-1604122105179.png" width="600" />

A 3.81mm (0.150") pitch header (Euro-style terminal block) is provided on the board. Corresponding connectors include following:

- TE Connectivity AMP Connectors 284507-4
- Ningbo Kangnex Elec WJ15EDGK-3.81-4P

The bipolar stepping motors has two coils. To connect the motor to the STEP400, we need to figure out which of the four wires from the motor are wired to which coil. The combination of wire color and corresponding coil is described on the data sheet. If you have a multimeter by your side, you can determine which wires are connected to the same coil, as the resistance of the coil is very low.
Connect the wires from two coils as follows.

<img src="https://ponoor.com/cms/wp-content/uploads/2020/10/coil-wiring.png" width="600" />

It is not crucial which coil is the coil A  or B on this picture. It does also not matter how the wiring order is. It won't affect the motor itself if these wirings are inverted, however the rotation direction will change. For the practice it is recommended to have a common wiring rule.

## The Relationship Between Power Supply and Stepper Motor Ratings
### Inductance
The windings inside a stepper motor behave as an inductor. When voltage is applied to the inductance, the current does not start to flow immediately but rises gradually. In the case of stepper motor that repeats the ON/OFF cycle at each step, when the rotation speed rises, ON/OFF cycle will become shorter and less current will flow. Since the torque of a stepper motor is nearly proportional to the current, the maximum torque decreases as the motor rotates at higher speed.

### Power supply voltage
To overcome the inductance and let driving current into the motor, you need to use a power supply with high voltage as possible. If you look at the motor’s datasheet, you might see very low rating voltage, but when you drive the motor, it will not be able to deliver the required current at that voltage. In fact, you will need to supply voltage several times higher.

Following graph from ST's application note is an example that shows the relation between supplied voltage and current. Actual value may vary depending on the motors, but we can see that the driver cannot supply enough current as the rotation increases when using a power source with low voltage.
<img src="https://ponoor.com/cms/wp-content/uploads/2020/10/motor_current_example_graph-800x570.png" width="800" />

The required voltage varies greatly depending on the motor’s rating, required speed required, and the load. But in general, required voltage is roughly as follows:

- Until NEMA17 size : 24 V
- NEMA23 or bigger : 48 V or 72 V for high speed

This means that NEMA 23 size and larger may be difficult to drive with STEP800.
However, some motors can produce high torque even with a small form factor, while others can’t apply much current even with larger size, so it’s important to check the ratings.

STEP400 works from DC12V, however since it is the DC-DC converter's lower limit for the input voltage range, there are cases where slight voltage drop causes the STEP400 to reset, especially when the inrush motor current causes voltage drop in the wiring from power supply. Therefore we don't recommend using 12V power source unless you are driving a small motor at low torque.

<img src="https://ponoor.com/cms/wp-content/uploads/2020/10/update-48V-configuration-800x533.jpg" alt="STEP400 working with the 48 V configuration, series of two 24V power supplies." width="600" class="size-medium wp-image-949" /> 
STEP400 working with the 48 V, supplied from series of two 24V power sources.

### Current Capacity
The current supply capacity of the power source is another important factor. Large current may flow at the moment of stalling, and if there is not enough current capacity, overload protection may be activated on the power supply side, causing the power supply to shut down. You might need to supply only several amps when you are driving small motors at lower speed, however, if you are driving large motors or operating them in high speed, often you do need much larger power source capable to supply 10A or 20A, depending on the quantity of motors, mode of operation, as well as your circuit protection settings. So we recommend you to choose a power supply with with large enough capacity.