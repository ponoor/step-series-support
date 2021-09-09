# STEP400/800 Config Generator
This python script generate config files for STEP400 and STEP800. Only `voltageMode` and `currentMode` values are generated and rest of them are same as the template files.

`motor_list.json` is generated from this [spreadsheet](https://docs.google.com/spreadsheets/d/1B9prXANUKMmz7NMaXzELaq7gCRYSPkStu4m9uLBT8zM/edit?usp=sharing).

## How to use generated configs
Copy the target json file to a microSD card, and rename the file to `config.txt`. Then you can insert the card to your device(STEP400/STEP800) and turn it on.

Please check [the documents](https://ponoor.com/en/docs/step-series/settings/setup-with-a-microsd-card/) for more details.
