## Overview
If you insert the microSD card with a configuration file written into the device, you can initialize the controller with the settings written in the file.
The configuration files can be exported using the Config Tool.

If you boot without a microSD card inserted, the default values written in the firmware will be used.

## Preparing the microSD card
Only microSD or microSDHC cards can be used, and they must be formatted with FAT16 or FAT32. The file name is limited to 8 characters and the extension is limited to 3 characters.

Refer the [Arduino SD Library reference](https://www.arduino.cc/en/Reference/SD) for the detail of the limitation of file name length.

## Configuration tool (Config Tool)
The configuration tool is written by HTML and JavaScript and available from here. It works both online and offline.

| MOdel | URL | Source (Github) |
| --- | --- | --- |
| STEP400 | http://ponoor.com/tools/step400-config/ | [/configTool](https://github.com/ponoor/STEP400/tree/master/configTool) |
| STEP800 | http://ponoor.com/tools/step800-config/ | [/configTool](https://github.com/ponoor/STEP800/tree/master/configTool) |


 You can use it via following URL:
http://ponoor.com/tools/step400-config/

Or, you can download it from here:
https://github.com/kanta/STEP400_prototype/tree/master/rev4/configTool

At the top of the page, you can load previous configuration files.
Click the "Export" button at the bottom of the page to download the configuration. The file name is `config.txt`. Although the file format is JSON, the file extension is changed to `.txt` instead of `.json` because it can only contain three characters for the extension.

Copy this file to the top level of the microSD card and insert it into the device. Then boot or reset the device. The settings are only loaded at startup.

Most of the items can be set from OSC message. The corresponding messages are listed below. [This spreadsheet](https://docs.google.com/spreadsheets/d/1EAUpzARE69ip6_LolZAv3crpmXGsESjCOz6EqVY1lUo/edit?usp=sharing) contains the list of corresponding JSON file items and parameters in the Arduino sketch.

## Config Tool items
### `Information`
| Parameter | OSC command | Default |
|-----------|-------------|---------|
| Configuration name | - | "Default" |
| Configuration version | - | 1.0 |
| Target product | - | "STEP400" or "STEP800"|

#### Configuration name
Configuration file name. Can be set freely.
#### Configuration version 
Version number of the Config Tool. Unable to modify.
#### Target product
Name of the target product for the config file. Unable to modify.

### `Network`

| Parameter | OSC command | Default |
|-----------|-------------|---------|
| My IP address |-| 10.0.0.100 |
| ID adds to my IP |-| TRUE |
| Destination IP | [/setDestIp](https://ponoor.com/en/docs/step-series/osc-command-reference/system-settings/#setdestip) | 10.0.0.10 |
| Gateway |-| 10.0.0.1 |
| DNS |-| 10.0.0.1 |
| Subnet mask |-| 255.255.255.0 |
| Incoming port |-| 50000 |
| Outgoing port |-| 50100 |
| ID adds to Outgoing port |-| TRUE |
| MAC address |-| 0x60, 0x95, 0xCE, 0x10, 0x02, 0x00 |
| ID adds to MAC address |-| TRUE |
| Booted message enable |-| TRUE |
| Allow OSC reply before /setDestIp |-| FALSE |
| Report errors | [/reportError](https://ponoor.com/en/docs/step-series/osc-command-reference/system-settings/#reporterror_boolenable) | TRUE |

#### My IP address
Set the IP address. if `ID adds to my IP` is checked, ID value added to this address becomes the actual IP address. For example if the IP address is set to `10.0.0.100` and ID switch is set to 1, `10.0.0.101` will be the actual address. Be cautious not the added value to exceed 254.

#### Incoming port
The port number that the device receives OSC messages.

#### Outgoing port
The port number that the device send out OSC message. If `ID adds to Outgoing port` check box is checked, the ID value will be added to the port number.
#### MAC address
You can switch decimal and hexadecimal display by clicking the check box `Hex`.

#### ID adds to MAC address
When this check box is checked, the ID value will be added to the lowest byte of the MAC address.

#### Booted message enable
Enables or disables the auto message [`/booted`](https://ponoor.com/en/docs/step-series/osc-command-reference/automatically-sent-messages-from-step-400/#booted) on ethernet link establishment on start.

#### Allow OSC reply before /setDestIp
In initial state, the controller does not send OSC response until receiving `/setDestIp`. However if this check box is checked, the controller will sends out OSC message immediately after boot up.

### `Alarm and Report`
| Parameter | OSC command | Default |
|-----------|-------------|---------|
| Report BUSY | [/enableBusyReport](https://ponoor.com/en/docs/step-series/osc-command-reference/motordriver-settings/#enablebusyreport_intmotorid_boolenable) | FALSE |
| Report HiZ | [/enableHizReport](https://ponoor.com/en/docs/step-series/osc-command-reference/motordriver-settings/#enablehizreport_intmotorid_boolenable) | FALSE |
| Report HOME switch status | [/enableHomeSwReport](https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#enablehomeswreport_intmotorid_boolenable) | FALSE |
| Report motor direction | /enableDirReport | FALSE |
| Report Motor Status | [/enableMotorStatusReport](https://ponoor.com/en/docs/step-series/osc-command-reference/motordriver-settings/#enablemotorstatusreport_intmotorid_boolenable) | FALSE |
| Report HOME switch event | [/enableSwEventReport](https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#enablesweventreport_intmotorid_boolenable) | FALSE |
| Report undervoltage lockout | [/enableUvloReport](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#enableuvloreport_intmotorid_boolenable) | TRUE |
| Report thermal status of driver chip | [/enableThermalStatusReport](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#enablethermalstatusreport_intmotorid_boolenable) | TRUE |
| Report motor stall detection | [/enableStallReport](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#enablestallreport_intmotorid_boolenable) | FALSE |
| Report LIMIT switch status *STEP400 ONLY | [/enableLimitSwReport](https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#enablelimitswreport_intmotorid_boolenable) | FALSE |
| Overcurrent threshold | [/setOverCurrentThreshold](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setovercurrentthreshold_intmotorid_intocd_th) | 15 |

### `Driver Settings`
| Parameter | OSC command | Default |
|-----------|-------------|---------|
| Homing when the system starts | ([/homing](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#homing_intmotorid)) | FALSE |
| Homing Direction | [/setHomingDirection](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#sethomingdirection_intmotorid_booldirection) | Reverse |
| Homing Speed | [/setHomingSpeed](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#sethomingspeed_intmotorid_floatspeed) | 50 |
| Home switch won't cause HardStop | [/setHomeSwMode](https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#sethomeswmode_intmotorid_boolsw_mode) | SW_USER |
| Prohibit motions on HomeSw | [/setProhibitMotionOnHomeSw](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setprohibitmotiononhomesw_intmotorid_boolenable) | FALSE |
| Limit switch won't cause HardStop *STEP400 ONLY | [/setLimitSwMode](https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#setlimitswmode_intmotorid_boolsw_mode) | SW_USER |
| Prohibit motions on LimitSw *STEP400 ONLY | [/setProhibitMotionOnLimitSw](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setprohibitmotiononlimitsw_intmotorid_boolenable) | FALSE |
| goUntil timeout duration | [/setGoUntilTimeout](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#setgountiltimeout_intmotorid_inttimeout) | 10000 |
| releaseSw timeout duration | [/setReleaseSwTimeout](https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#setreleaseswtimeout_intmotorid_inttimeout) | 10000 |
| Microstepping mode | [/setMicrostepMode](https://ponoor.com/en/docs/step-series/osc-command-reference/motordriver-settings/#setmicrostepmode_intmotorid_intstep_sel) | STEP_FS_128 |
| Current mode *STEP400 ONLY | [/setVoltageMode](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setvoltagemode_intmotorid), [/setCurrentMode](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setcurrentmode_intmotorid) | FALSE |
| Slew rate | - | SR_980V_us |
| Electromagnetic brake enable | [/enableElectromagnetBrake](https://ponoor.com/en/docs/step-series/osc-command-reference/brake/#enableelectromagnetbrake_intmotorid_boolenable) | FALSE |
| Brake transition duration | [/setBrakeTransitionDuration](https://ponoor.com/en/docs/step-series/osc-command-reference/brake/#setbraketransitionduration_intmotorid_intduration) | 100 |

#### Homing when the system starts
Proceed to homing movement soon after boot when this check box is checked.

#### Slew rate
Set the slew rate (steepness of rising) of motor control current from a motor driver in 6 steps for STEP400, 3 steps for STEP800.

| Slew rate number | STEP400 | STEP800 |
| --- | --- | --- |
| 0 | 114V/us | 180V/us |
| 1 | 220V/us | 290V/us |
| 2 | 400V/us | 530V/us |
| 3 | 520V/us | - |
| 4 | 790V/us | - |
| 5 | 980V/us | - |

### `Speed Profile`
| Parameter | OSC command | Default |
|-----------|-------------|---------|
| Acceleration | [/setSpeedProfile](https://ponoor.com/en/docs/step-series/osc-command-reference/speed-profile/#setspeedprofile_intmotorid_floatacc_floatdec_floatmaxspeed) | 2000 |
| Decceleration | [/setSpeedProfile](https://ponoor.com/en/docs/step-series/osc-command-reference/speed-profile/#setspeedprofile_intmotorid_floatacc_floatdec_floatmaxspeed) | 2000 |
| Max speed | [/setSpeedProfile](https://ponoor.com/en/docs/step-series/osc-command-reference/speed-profile/#setspeedprofile_intmotorid_floatacc_floatdec_floatmaxspeed) | 620 |
| Transit to fullstep threshold speed | [/setFullstepSpeed](https://ponoor.com/en/docs/step-series/osc-command-reference/speed-profile/#setfullstepspeed_intmotorid_floatfullstepspeed) | 15625 |

### `Voltage Mode`
| Parameter | OSC command | Default |
|-----------|-------------|---------|
| KVAL_HOLD | [/setKval](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setkval_intmotorid_intholdkval_intrunkval_intacckval_intsetdeckval) | 16 |
| KVAL_RUN | [/setKval](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setkval_intmotorid_intholdkval_intrunkval_intacckval_intsetdeckval) | 16 |
| KVAL_ACC | [/setKval](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setkval_intmotorid_intholdkval_intrunkval_intacckval_intsetdeckval) | 16 |
| KVAL_DEC | [/setKval](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setkval_intmotorid_intholdkval_intrunkval_intacckval_intsetdeckval) | 16 |
| INT_SPEED | [/setBemfParam](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setbemfparam_intmotorid_intint_speed_intst_slp_intfn_slp_acc_intfn_slp_dec) | 1032 |
| ST_SLP | [/setBemfParam](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setbemfparam_intmotorid_intint_speed_intst_slp_intfn_slp_acc_intfn_slp_dec) | 25 |
| FN_SLP_ACC | [/setBemfParam](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setbemfparam_intmotorid_intint_speed_intst_slp_intfn_slp_acc_intfn_slp_dec) | 41 |
| FN_SLP_DEC | [/setBemfParam](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setbemfparam_intmotorid_intint_speed_intst_slp_intfn_slp_acc_intfn_slp_dec) | 41 |
| STALL_TH | [/setStallThreshold](https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setstallthreshold_intmotorid_intstall_th) | 31 |
| lowSpeedOptimize | [/setLowSpeedOptimizeThreshold](https://ponoor.com/en/docs/step-series/osc-command-reference/motordriver-settings/#setlowspeedoptimizethreshold_intmotorid_floatlowspeedoptimizationthreshold) | 20 |

### `Current Mode *STEP400 ONLY`
| Parameter | OSC command | Default |
|-----------|-------------|---------|
| TVAL_HOLD | [/setTval](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#settval_intmotorid_intholdtval_intruntval_intacctval_intsetdectval) | 16 |
| TVAL_RUN | [/setTval](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#settval_intmotorid_intholdtval_intruntval_intacctval_intsetdectval) | 16 |
| TVAL_ACC | [/setTval](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#settval_intmotorid_intholdtval_intruntval_intacctval_intsetdectval) | 16 |
| TVAL_DEC | [/setTval](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#settval_intmotorid_intholdtval_intruntval_intacctval_intsetdectval) | 16 |
| T_FAST | [/setDecayModeParam](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setdecaymodeparam_intmotorid_intt_fast_intton_min_inttoff_min) | 25 |
| TON_MIN | [/setDecayModeParam](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setdecaymodeparam_intmotorid_intt_fast_intton_min_inttoff_min) | 41 |
| TOFF_MIN | [/setDecayModeParam](https://ponoor.com/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/#setdecaymodeparam_intmotorid_intt_fast_intton_min_inttoff_min) | 41 |

### `Servo Mode`
| Parameter | OSC command | Default |
|-----------|-------------|---------|
| kP | [/setServoParam](https://ponoor.com/en/docs/step-series/osc-command-reference/servo-mode/#setservoparam_intmotorid_floatkp_floatki_floatkd) | 0.06 |
| kI | [/setServoParam](https://ponoor.com/en/docs/step-series/osc-command-reference/servo-mode/#setservoparam_intmotorid_floatkp_floatki_floatkd) | 0 |
| kD | [/setServoParam](https://ponoor.com/en/docs/step-series/osc-command-reference/servo-mode/#setservoparam_intmotorid_floatkp_floatki_floatkd) | 0 |
