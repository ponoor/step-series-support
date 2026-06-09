---
title: Example parameter values for example steppers
wp_id: 871
slug: example-parameter-values-for-example-steppers
lang: en
link: "https://ponoor.com/en/docs/step-series/settings/example-parameter-values-for-example-steppers/"
date: "2020-10-31T14:33:09"
modified: "2021-12-09T17:21:27"
parent: 867
menu_order: 58
---

# Example parameter values for example steppers

## Motor parameters examples

We'd like to post here the parameters we have actually tested and figured out for the motor we have in our lab. The parameters will be provided as a configuration file.  
<https://github.com/ponoor/step-series-support/tree/main/configGenerator>

### Set parameters

#### config name

Config file names are set to `Type_Voltage`.

#### Voltage mode

- Each KVAL values (KVAL\_HOLD is set to half of the KVAL\_RUN)
- BEMF compensate parameter. Refer [this article](https://ponoor.com/en/docs/step-series/functional-description/voltage-mode-and-current-mode/) for the calculation.

#### Current mode

- Each TVAL values (TVAL\_HOLD is set to half of the TVAL\_RUN)

#### Speed profile

The maximum motor speed and acceleration, deceleration vary greatly depending on the weight of load, size, mounting method. Therefore these values are set to default. Configure them with`/setSpeedProfile` and other commands while actuating loads.

### File name

To differentiate the files on the link, their names are formatted to`Type_Voltage.json`. However the name must be changed to `config.txt` when copying to microSD. For the detail please refer [Set up with a miroSD card](https://ponoor.com/en/docs/step-series/settings/setup-with-a-microsd-card/).
