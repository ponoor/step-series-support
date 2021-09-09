# STEP400/800 Config Generator
This python script generate config files for STEP400 and STEP800. Only `voltageMode` and `currentMode` values are generated and rest of them are same as the template files.

`motor_list.json` is generated from this [spreadsheet](https://docs.google.com/spreadsheets/d/1B9prXANUKMmz7NMaXzELaq7gCRYSPkStu4m9uLBT8zM/edit?usp=sharing).

# Example parameters
The file name should be `config.txt` for a microSD card, but file names are different here to identify.  Please rename them when you copy to your microSD, or copy the content of the Json files to your config.txt file.

Please check [the documents](https://ponoor.com/en/docs/step-series/settings/setup-with-a-microsd-card/) for more details.

We are currently testing the following motors:

### MERCURY MOTOR
|MPN|Size|Resistance|Inductance|Phase Current|Voltage|Holding Torque|Ke|
|:----|:----|:----|:----|:----|:----|:----|:----|
|SM-42BYG011-25|NEMA17|34ohm|46mH|0.33A|12V|0.23Nm|0.0763|
|ST-42BYH1004-5013|NEMA17|5.0ohm|11.5mH|1.0A|5V|4.4Kgf.cm|-|
|ST-42BYH1684-1612|NEMA17|1.65ohm|4.1mh|1.68A|2.8V|4.4Kgf.cm|0.0151|
|ST-57BYG076-0604|NEMA23|20ohm|55mH|0.6A|12V|13Kgf.cm|0.248|
|ST-57BYG076-3004D|NEMA23|1ohm|3.5mH|3A|3V|18Kgf.cm|0.2985|


### Orientalmotor
|MPN|Size|Resistance|Inductance|Phase Current|Voltage|Holding Torque|Ke|
|:----|:----|:----|:----|:----|:----|:----|:----|
|PKP213D05|NEMA8|8.5ohm|4.1mH|0.5A|4.25V|0.02Nm|0.0049|
|PKP223D15|NEMA11|1.18ohm|0.96mH|1.5A|1.77V|0.095Nm|0.0067|
|PKP243D23|NEMA17|0.78ohm|1.4mH|2.3A|1.8V|0.35Nm|0.0148|
|PKP246D23|NEMA17|1.4ohm|3.3mH|2.3A|3.2V|0.99Nm|0.0431|


### Usongshine
|MPN|Size|Resistance|Inductance|Phase Current|Voltage|Holding Torque|Ke|
|:----|:----|:----|:----|:----|:----|:----|:----|
|17HS2408S|NEMA17|8.0ohm|10mH|0.6A|4.8V|12N.cm|0.0405|
|17HS3401S|NEMA17|2.4ohm|2.8mH|1.3A| |28N.cm|0.02753|
|17HS4023|NEMA17|4.0ohm|3.2mH|0.7A|12V|14N.cm|0.00981|
|17HS4401S|NEMA17|1.5ohm|2.8mH|1.7A| |40N.cm|0.02753|
|23HS5628|NEMA23|0.9ohm|2.5mH|2.8A|-|126N.cm|0.0473|


### STEPPER ONLINE
|MPN|Size|Resistance|Inductance|Phase Current|Voltage|Holding Torque|Ke|
|:----|:----|:----|:----|:----|:----|:----|:----|
|17HS08-1004S|NEMA17|3.7ohm|4.5mH|1.0A|3.7V|16N.cm|0.01645|



### 多摩川精機 / Tamagawa
|MPN|Size|Resistance|Inductance|Phase Current|Voltage|Holding Torque|Ke|
|:----|:----|:----|:----|:----|:----|:----|:----|
|TS3692N65|NEMA8|8.5ohm|3.4mH|0.35A|3.0V|0.017Nm|0.00495|

