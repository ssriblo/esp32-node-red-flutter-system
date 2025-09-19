// https://chatgpt.com/share/68973fed-ed10-8009-a376-cbbb0546b16c

#include <WiFi.h>
#include <PubSubClient.h>
#include <Arduino.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#include "tempFilter.h" 

// #define DEBUG_PRINT


const char* ssid = "ENAiKOON-Technik";
const char* password = "EN2020ik";
const char* mqtt_server = "130.61.123.45";
const char* nodeRedUrl = "http://130.61.123.45:1880/esp32_params";

WiFiClient espClient;
PubSubClient client(espClient);


HeaterModel model;
float heater_val = 0.0;

void callback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (int i = 0; i < length; i++) message += (char)payload[i];

#ifdef DEBUG_PRINT    
  Serial.printf(">>>>> topic: %s, message: %s\n", topic, message.c_str());
#endif

  if (String(topic) == "esp32/alarm") {
    if (message == "ON") {
      digitalWrite(2, HIGH); // LED ON
      Serial.println("Alarm ON: LED is ON");
    } else {
      digitalWrite(2, LOW); // LED OFF
      Serial.println("Alarm OFF: LED is OFF");
    }
  }

  if (String(topic) == "esp32/heater") {
    heater_val = message.toFloat();
#ifdef DEBUG_PRINT    
    Serial.println("Heater value set to: " + String(heater_val));
#endif
  }
}

void reconnect() {
  Serial.println("[reconnect-1]\n");
  while (!client.connected()) {
    Serial.println("[reconnect-2]\n");
    if (client.connect("ESP32Client")) {
      Serial.printf("Connected to MQTT broker at %s\n", mqtt_server);
      client.subscribe("esp32/alarm");
      client.subscribe("esp32/heater");
    } else {
      delay(2000);
    }
  }
}

bool paramsParsing(HeaterModel* m, String payload) {
/* Node-RED function node to send initial parameters
msg.payload = {
    "HeatCapasity": Math.floor(100),
    "HeatLossCoeff": Math.floor(1),
    "Alpha": Math.floor(20),
    "tAbient": Math.floor(20),
    "delayTime": Math.floor(5),
    "stepSecound": Math.floor(1),
    "tRoom": Math.floor(20),
    "tSensor": Math.floor(20)
};
return msg;
*/
  DynamicJsonDocument doc(1024);
  DeserializationError error = deserializeJson(doc, payload);
  bool ret = false;

  if (!error) {
    m->Cp = doc["HeatCapasity"] | 100.0;
    m->U = doc["HeatLossCoeff"] | 1.0;
    m->alpha = doc["Alpha"] | 20.0;
    m->Tamb = doc["tAbient"] | 20.0;
    m->tau = doc["delayTime"] | 5.0;
    m->dt = doc["stepSecound"] | 1.0;
    m->T = doc["tRoom"] | 20.0;
    m->Ts = doc["tSensor"] | 20.0;
    
    Serial.println("========================");
    Serial.println("Parameters updated from Node-RED:");
    Serial.printf("HeatCapasity: %2.1f\n", m->Cp);
    Serial.printf("HeatLossCoeff: %2.1f\n", m->U);
    Serial.printf("Alpha: %2.1f\n", m->alpha);
    Serial.printf("tAbient: %2.1f\n", m->Tamb);
    Serial.printf("delayTime: %2.1f\n", m->tau);
    Serial.printf("stepSecound: %2.1f\n", m->dt);
    Serial.printf("tRoom: %2.1f\n", m->T);
    Serial.printf("tSensor: %2.1f\n", m->Ts);
    Serial.println("========================");
    ret = true;
  } else {
    Serial.println("JSON parsing error: " + String(error.c_str()));
  }


  return ret;
}
void setup() {
  Serial.begin(115200);
  pinMode(GPIO_NUM_0, INPUT_PULLUP);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);
  Serial.printf("Connected to WiFi: %s\n", ssid);
  Serial.printf("IP address: %s\n", WiFi.localIP().toString().c_str());

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);


  HTTPClient http;
  http.begin(nodeRedUrl);

  int httpCode = -1;
  while(1) {
    httpCode = http.GET();
    if (http.GET() == HTTP_CODE_OK){
      String payload = http.getString();
      Serial.println("Received parameters: " + payload);
      bool ret = paramsParsing(&model,payload);
      if (!ret)  {
        Serial.println("Parameter parsing error!");
      } else {
        http.end();
        break;
      }
    } else {
      Serial.printf("Waiting for Node-RED server... %d\n", httpCode);
      delay(2000);
      continue;
    }
  }

  // float dt = 1.0;
  // init_model(&model,
  //             100.0,   // Cp
  //             1.0,     // U
  //             20.0,    // alpha
  //             20.0,    // Tamb
  //             5.0,     // tau
  //             dt,
  //             20.0,    // initail room temperature
  //             20.0);   // initial sensor temperature
  // heater_model_unit_test();


}

void loop() {
  if (!client.connected()) reconnect();
  bool state = client.loop();
  static bool sendToMQTT = true;
  static int num = 0;

#ifdef DEBUG_PRINT    
  Serial.printf("Loop state: %d heater_val: %2.1f\n", state, heater_val);
#endif

  int pinState = digitalRead(GPIO_NUM_0);
  if (pinState == LOW) {
    sendToMQTT = sendToMQTT ? false : true;
    Serial.printf("[PUSH] Pin state: %d sendToMQTT: %d\n", pinState, sendToMQTT);
    delay(2000); // debounce
  } 
  // Serial.printf("Pin state: %d sendToMQTT: %d\n", pinState, sendToMQTT);

  if (sendToMQTT) {
    step_model(&model, heater_val * 10);
    float temp = model.Ts;

    String payload = "{\"temp\":" + String(temp) + ",\"num\":" + String(num++) + "}";
    state = client.publish("esp32/sensors", payload.c_str());

    // payload = "{\"kp\":" + String(0.2) + \
    //   ",\"ki\":" + String(0.03) + \
    //    ",\"kd\":" + String(0.1) + \ 
    //    "}";
    // state = client.publish("esp32/pid_parameters", payload.c_str());
    // Serial.printf("pid_parameters: payload: %s\n", payload.c_str());


  #ifdef DEBUG_PRINT    
    Serial.printf("Publish state: %d payload: %s\n", state, payload.c_str());
  #endif
    delay(500);
  }
}
