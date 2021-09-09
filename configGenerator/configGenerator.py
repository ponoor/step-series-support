#import numpy as np
import json
from collections import OrderedDict
import pprint
import math
import os
path = os.path.dirname(__file__)

num_of_motor_axis_step400 = 4
num_of_motor_axis_step800 = 8
targetVoltage_step400 = [24.0, 48.0, 72.0]
targetVoltage_step800 = [12.0, 24.0, 32.0]
currentOverdrive = 1.0

f = open(path + "/motor_list.json", "r")
motor_dict = json.load(f, object_pairs_hook=OrderedDict)
motor = motor_dict["motors"]
f.close()
#pprint.pprint(motor_dict, width=40)

f = open(path + "/configTemplate_step400.json")
templateConfig_400 = json.load(f, object_pairs_hook=OrderedDict)
f.close()

f = open(path + "/configTemplate_step800.json")
templateConfig_800 = json.load(f, object_pairs_hook=OrderedDict)
f.close()

#pprint.pprint(motor[5])
#print(len(motor))

def get_kval(target_current, voltage, resistance):
    t = (target_current * currentOverdrive * resistance) / voltage
    t *= 255.0
    t = round(t)
    return t

def get_int_spd(resistance, inductance):
    t = 4.0 * resistance / (3.14159265 * 2.0 * inductance)
    t /= 0.0596
    t = round(t)
    return t

def get_StSlp(ke, voltage):
    t = ( ke/4.0) / voltage
    t /= 0.000015
    t = round(t)
    return t

def getFnSlp(inductance, current, ke, voltage):
    t = ((2.0 * math.pi * inductance * current * currentOverdrive + ke) / 4.0) / voltage
    t *= 65536.0
    t = round(t)
    return t

def getTval(targetCurrent):
    t = (targetCurrent * currentOverdrive * 1000.0) / 78.125
    t += 1
    t = round(t)
    if t > 127: # STEP400 current limit
        t = 127
    return t

# Load motor parameters
for i in motor:
    MPN = i["MPN"]
    r = i["Resistance"]
    l = i["Inductance"] / 1000.0 # [mH] to [H]
    current = i["PhaseCurrent"]
    ke = i["Ke"]
    # Generate parameters for each motors
    for v in targetVoltage_step400:
        kval = get_kval(current, v, r)
        kval_hold = round(kval / 2)
        int_spd = get_int_spd(r, l)
        st_slp = get_StSlp(ke, v)
        fn_slp = getFnSlp(l, current, ke, v)
        tval = getTval(current)
        tval_hold = round(tval/2)

        #print(MPN, current)
        information = templateConfig_400["information"]
        information['configName'] = MPN + '_' + str(int(v))+'V'
        voltageMode = templateConfig_400['voltageMode']
        currentMode = templateConfig_400['currentMode']
        for j in range(num_of_motor_axis_step400):
            voltageMode['KVAL_HOLD'][j] = kval_hold
            voltageMode['KVAL_RUN'][j] = kval
            voltageMode['KVAL_ACC'][j] = kval
            voltageMode['KVAL_DEC'][j] = kval
            voltageMode['INT_SPEED'][j] = int_spd
            voltageMode['ST_SLP'][j] = st_slp
            voltageMode['FN_SLP_ACC'][j] = fn_slp
            voltageMode['FN_SLP_DEC'][j] = fn_slp
            currentMode['TVAL_HOLD'] = tval_hold
            currentMode['TVAL_RUN'] = tval
            currentMode['TVAL_ACC'] = tval
            currentMode['TVAL_DEC'] = tval
        filename = '/step400-configs/STEP400_' + information['configName'] + '.json'
        with open(path + filename, "w") as f:
            json.dump(templateConfig_400, f, indent=4)
        f.close()
        print('Wrote:'+filename)
    
    for v in targetVoltage_step800:
        if current > 2.0:
            break
        kval = get_kval(current, v, r)
        kval_hold = round(kval / 2)
        int_spd = get_int_spd(r, l)
        st_slp = get_StSlp(ke, v)
        fn_slp = getFnSlp(l, current, ke, v)

        #print(MPN, current)
        information = templateConfig_800["information"]
        information['configName'] = MPN + '_' + str(int(v))+'V'
        voltageMode = templateConfig_800['voltageMode']
        for j in range(num_of_motor_axis_step800):
            voltageMode['KVAL_HOLD'][j] = kval_hold
            voltageMode['KVAL_RUN'][j] = kval
            voltageMode['KVAL_ACC'][j] = kval
            voltageMode['KVAL_DEC'][j] = kval
            voltageMode['INT_SPEED'][j] = int_spd
            voltageMode['ST_SLP'][j] = st_slp
            voltageMode['FN_SLP_ACC'][j] = fn_slp
            voltageMode['FN_SLP_DEC'][j] = fn_slp
        filename = '/step800-configs/STEP800_' + information['configName'] + '.json'
        with open(path + filename, "w") as f:
            json.dump(templateConfig_800, f, indent=4)
        f.close()
        print('Wrote:'+filename)
