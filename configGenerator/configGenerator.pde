// Load the motor list json test
JSONObject json, configTemplate;
float targetVoltage[] = {24.0, 48.0, 72.0};
float currentOverdrive = 1.0;
int NUM_OF_MOTOR = 4;
String configLinkPath = "https://github.com/ponoor/STEP400/blob/develop/configTool/sample-setups/";

void setup() {
  size(640, 360);
  loadMotorData();
}

void draw() {
  //
  background(255);  
}
int getKval(float targetCurrent, float voltage, float resistance) {
  float t = (targetCurrent * currentOverdrive * resistance) / voltage;
  t *= 255.0;
  t = round(t);
  t = constrain(t, 0, 255);
  return int(t);
}

int getIntSpd(float resistance, float inductance) {
  float t = 4.0*resistance / (PI*2.0*inductance);
  t /= 0.0596;
  t = round(t);
  t = constrain(t, 0, 16383);
  return int(t);
}

int getStSlp(float ke, float voltage) {
  float t = (ke/4.0) / voltage;
  t /= 0.000015;
  t = round(t);
  t = constrain(t, 0, 255);
  return int(t);
}

int getFnSlp(float inductance, float current, float ke, float voltage) {
  float t = ((2.0 * PI * inductance * current * currentOverdrive + ke) / 4.0) / voltage;
  t *= 65536.0; // need to test
  t = round(t);
  t = constrain(t, 0, 255);
  return int(t);
}

int getTval(float targetCurrent) {
  float t = (targetCurrent * currentOverdrive * 1000.0) / 78.125;
  t += 1;
  t = round(t);
  t = constrain(t, 0, 127);
  return int(t);
}

void loadMotorData() {
  // Motor data list
  json = loadJSONObject("motor_list.json");
  JSONArray motorData = json.getJSONArray("motors");

  // template config json
  configTemplate = loadJSONObject("configTemplate.json");

  // Generate a config for each motors
  for (int i = 0; i < motorData.size(); i++) {
    JSONObject motor = motorData.getJSONObject(i);
    int motorNum = motor.getInt("num");
    String MPN = motor.getString("MPN");
    String manufacture = motor.getString("Manufacture");
    String motorSize = motor.getString("Size");
    float r = motor.getFloat("Resistance");
    float l = motor.getFloat("Inductance"); // in [mH]
    l /= 1000.0; // [H]
    float current = motor.getFloat("PhaseCurrent");
    float ke = motor.getFloat("Ke");

    // set to the template
    JSONObject information = configTemplate.getJSONObject("information");
    
    JSONObject voltageMode = configTemplate.getJSONObject("voltageMode");
    JSONArray kvalHoldArray = voltageMode.getJSONArray("KVAL_HOLD");
    JSONArray kvalRunArray = voltageMode.getJSONArray("KVAL_RUN");
    JSONArray kvalAccArray = voltageMode.getJSONArray("KVAL_ACC");
    JSONArray kvalDecArray = voltageMode.getJSONArray("KVAL_DEC");
    JSONArray intSpeedArray = voltageMode.getJSONArray("INT_SPEED");
    JSONArray stSlpArray = voltageMode.getJSONArray("ST_SLP");
    JSONArray fnSlpAccArray = voltageMode.getJSONArray("FN_SLP_ACC");
    JSONArray fnSlpDecArray = voltageMode.getJSONArray("FN_SLP_DEC");

    JSONObject currentMode = configTemplate.getJSONObject("currentMode");
    JSONArray tvalHoldArray = currentMode.getJSONArray("TVAL_HOLD");
    JSONArray tvalRunArray = currentMode.getJSONArray("TVAL_RUN");
    JSONArray tvalAccArray = currentMode.getJSONArray("TVAL_ACC");
    JSONArray tvalDecArray = currentMode.getJSONArray("TVAL_DEC"); 
    for (int j=0; j<3; j++) {
      String configName = MPN + "_" + str(int(targetVoltage[j])) + "V";
      information.setString("configName", configName);

      int kval = getKval(current, targetVoltage[j], r);
      int int_spd = getIntSpd(r,l);
      int st_slp = getStSlp(ke, targetVoltage[j]);
      int fn_slp = getFnSlp(l, current, ke, targetVoltage[j]);
      int tval = getTval(current);
      println("motorNum: " + motorNum + ", " + MPN);
      println("\tKVAL: " + kval);
      println("\tINT_SPD: " + int_spd);
      println("\tST_SLP: " + st_slp);
      println("\tFN_SLP: " + fn_slp);
      println("\tTVAL: " + tval);
      for (int k=0; k<NUM_OF_MOTOR; k++) {
        kvalHoldArray.setInt(k, kval/2);
        kvalRunArray.setInt(k, kval);
        kvalAccArray.setInt(k, kval);
        kvalDecArray.setInt(k, kval);
        intSpeedArray.setInt(k, int_spd);
        stSlpArray.setInt(k, st_slp);
        fnSlpAccArray.setInt(k, fn_slp);
        fnSlpDecArray.setInt(k, fn_slp);
        tvalHoldArray.setInt(k, tval/2);
        tvalRunArray.setInt(k, tval);
        tvalAccArray.setInt(k, tval);
        tvalDecArray.setInt(k, tval);
      }
      String fileName = "./config/" + configName + ".json";
      println("\t"+fileName);
      saveJSONObject(configTemplate, fileName, "indent=4");
    }
  }  

}

