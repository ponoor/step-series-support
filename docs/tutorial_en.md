## Sample files for this tutorial
This device communicates over Open Sound Control (OSC) protocol. So prepare the host application (or program) that can send and receive OSC.

- [Max](https://github.com/ponoor/step-series-example-Max) Currently the Max sample file covers functions the most. Start from [downloading Max](https://cycling74.com/downloads) and install.

- [Processing](https://github.com/yuskegoto/STEP400_Processing)
Contribution of [@yuskegoto](https://github.com/yuskegoto)
- [openFrameworks](https://github.com/ponoor/step-series-example-openFrameworks)
Contribution of [@niimi](https://github.com/niimi)
- [Unity](https://github.com/ponoor/step-series-example-Unity)
Contribution of [@niimi](https://github.com/niimi)
- [Touch Designer](https://github.com/ponoor/step-series-example-TouchDesigner)
Contribution of [@loveandsheep](https://github.com/loveandsheep), [@yuskegoto](https://github.com/yuskegoto)
- [Node-RED](https://github.com/yuskegoto/STEP400_Node-RED)
Contribution of [@yuskegoto](https://github.com/yuskegoto)

## Connection
### Network
First, connect the PC and This device with a ethernet cable. If your PC does not have an ethernet port, you will need to use a USB-Ethernet converter.

To simplify this tutorial, we will assume that the PC and the board are connected peer to peer with an ethernet cable. You can off course connect over a network switch (NOT a router) instead. Routers may make things complicated when they have DHCP functionality, not recommended to get started.

### Stepper motor
The type of stepper motor that can be used with this device is a "bipolar" one. Power supply capacity and settings may vary depending on the specification of motor. A good example of easily available motor is MERCURY MOTOR's SM-42BYG011-25. It can be purchased from the following sources among others:
- [Sparkfun](https://www.sparkfun.com/products/9238)
- [Strawberry Linux](http://strawberry-linux.com/catalog/items?code=12026)
- [Akizuki Denshi](https://akizukidenshi.com/catalog/g/gP-05372/)

![](http://ponoor.com/manage/wp-content/uploads/2020/10/09238-01.jpg)

Here, we will use this motor as an example for specific setting values.
Click [here](https://ponoor.com/en/docs/step-series/settings/power-supply-and-motor/#i-5) for information about how to connect the board to a motor and to a power supply.

The data sheet of this stepper can be found [here](https://www.sparkfun.com/datasheets/Robotics/SM-42BYG011-25.pdf).
From this diagram, we can see that the wiring pairs are Red - Green and Yellow - Blue.

[![](https://ponoor.com/cms/wp-content/uploads/2020/08/motor-wiring-diagram-sample.png)](https://ponoor.com/cms/wp-content/uploads/2020/08/motor-wiring-diagram-sample.png)

We need to pair two wires from same coil, so the connection order to the terminal block should look like this.

[![](https://ponoor.com/cms/wp-content/uploads/2020/08/SM-42BYG-wiring-700x525.jpg)](https://ponoor.com/cms/wp-content/uploads/2020/08/SM-42BYG-wiring.jpg)

### Power supply
If you want to run a single motor in the example above, the AC adapter’s capacity of 24V1A is sufficient. The power supply must have DC barrel plug with 5.5mm outer diameter / 2.1mm inner diameter / center positive.

<img src="https://ponoor.com/cms/wp-content/uploads/2020/08/image-1609563897700.png" width="600" />

Supplying from the DC barrel jack is sufficient for this size of motor, but if you need to drive much larger motor with high voltage , high current capacity, use the screw terminal block next to the DC jack.
Do not connect the power supply before configuring the following DIP switches.

## Network settings
### Configuration Tool
You can change your network settings using the [Configuration Tool](http://ponoor.com/tools/step400-config/)  (HTML+JavaScript) to generate a configuration file, which can then be written onto a microSD card. In this tutorial however, we will use the default settings, so you can just leave the microSD slot empty.

### Board side
The DIP switch on the board must be set to 1. That is, only the digit 1 is ON, and all other digits are OFF. In this state, the board has the following network settings:

| item | assigned value |
| ---- | ---- |
| IP address | 10.0.0.101 |
| Reply address | 10.0.0.10 |
| OSC incoming port | 50000 |
| OSC outgoing port | 50101 |

<img src="http://ponoor.com/manage/wp-content/uploads/2020/10/IMG_0704.jpg" width="600" />

Now you can turn on the power. On the rear side of this device PCB, there are several pins where the power supply voltage is applied, so either attach spacers to the holes on the board or place the board on a non-conductive material.

### PC side
Set the static IP address for the Ethernet port that this device is connected to. Set it as follows:

| Item | Assign value |
| ---- | ---- |
| IP address| 10.0.0.10 |
| Subnet mask | 255.255.255.0 |

Setting the static IP address varies dending on your OS.
- [Windows10](https://support.microsoft.com/en-us/windows/change-tcp-ip-settings-bd0a07af-15f5-cd6a-363f-ca2b6f391ace)
- [Mac](https://support.apple.com/en-us/HT202480)

Provided that you don’t encounter problems with these settings, you should be able to check the connection with commands such as `ping 10.0.0.101` from Terminal on Mac, or Command Prompt on Windows computers.

## Check the connection
From here on, the actual operations will vary depending on your environment, but we will focus on describing the actual Open Sound Control messages that are sent and received.

First, the command`/setDestIp`has to be sent to this device to tell where the response messages have to be send back to. The destination address is `10.0.0.101`, and the outgoing port is `50000`. Until this command is received by the this device, the controller will not send any OSC messages. This is because the operation may become unstable if this device continues to send OSC messages to a non-existent destination.
If `/setDestIp` is received without problems, you should get the following response. The incoming port is `50101`.

```
/destIp (int)destIp[0] (int)destIp[1] (int)destIp[2] (int)destIp[3] (bool)isNewDestIp
```

- `destIp[0-3]` : Each bytes of destIp
- `isNewDestIp` : Indicates whether or not destIp has been changed. 1 if it has been changed, or 0 if the same address has already been set.

Now we're ready to exchange messages.

## Get the motor running
Let's send a command to run the motor. `/run (int)motorID (float)speed` command sets the motor to rotate at the specified speed.

The `motorID` specifies which motor to run (the number is printed on the this device board). Possible ID values are 1-4 for STEP400, 1-8 for STEP800, and 255. If you set the ID to `255`, you can send the command to all motors. This applies to almost all commands that need to specify motor ID.

The `speed` command specifies the speed and the direction of the motor. The range you can set is from -15625.0 to 15625.0 step/s. If you're using a motor with 200 steps per revolution, you can specify `200.0` to make one revolution per second. If you set a negative value, the motor will go backwards.

For example, to make one revolution per second for a motor connected to connector number 1, the OSC message should look like this:

```
/run 1 200.
```

Did it work? If something went wrong with the motor and you want to stop it, set speed to `0.0`, or send the message
`/hardHiZ 255`
to stop all motors.

In many cases, the motor might not be running smoothly at this point. We will need to make further set up.

## KVAL setting
In most cases, the reason for lacking motion smoothness is insufficient (or sometimes excessive) drive voltage. This can be adjusted with the KVAL register. The KVAL register sets the voltage to drive the motor in the scale of 0 to 255, where 0 means 0V (cannot turn) and 255 means that the motor drive voltage is almost the same as the power supply voltage. For example, if you are using a 24V power supply and you specify 128 for the KVAL, the motor will be driven at about 12V.

There are four types of KVAL:

| KVAL name | function | initial value at this device |
| --- | --- | --- |
| KVAL_HOLD | Holding KVAL | 0 |
| KVAL_RUN | Constant speed KVAL | 16 |
| KVAL_ACC | Acceleration KVAL | 16 |
| KVAL_DEC | Deceleration KVAL | 16 |

Let's adjust KVAL_RUN while rotating the motor at a constant speed.
Send following message to rotate the motor:

```
/run 1 200.
```
You can set individual KVALs, for example with `/setRunKval` for `KVAL_RUN`, but we are going to try following command which can set all KVALs at once.

```
/setKval (int)motorID (int)holdKVAL (int)runKVAL (int)accKVAL (int)setDecKVAL
```

Where `motorID` is `1-4, 255` for STEP400, `1-8, 255` for STEP800. Possible value for each KVAL ranges from 0 to 255. Let's set KVAL to `0` for stopping, and gradually increase the value for acceleration and deceleration to the same value as KVAL for constant speed.

```
/setKval 1 0 24 24 24
```

This message specifies the first motor KVAL for holding as 0, and the rest of them as 24 (approximately 9% of the power supply voltage).

Gradually increase the numbers as follows, and from some point the motor should begin to turn quietly.

```
/setKval 1 0 32 32 32
```

As you increase the KVALs, the torque will also increase, but the motor will generate more heat as well as the vibration, so make sure to set appropriate adjustments to suit the load.


