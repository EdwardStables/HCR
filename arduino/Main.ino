// ArduinoJson - arduinojson.org
// Copyright Benoit Blanchon 2014-2019
// MIT License
//
// This example shows how to deserialize a JSON document with ArduinoJson.
//
// https://arduinojson.org/v6/example/parser/

#include <ArduinoJson.h>
#include <Servo.h>
#include <Stewart.h>

void state(int state);
void makeMoves(float moves[50][3]);
void applyOffset(int offset[2]);
void reset();

int pins[] = {9, 10, 11, 12, 14, 15};

Stewart Platform = Stewart(pins);

void setup() {
  // Initialize serial port
  Serial.begin(9600);
  while (!Serial) continue;

  //const char* sensor = doc["sensor"];
  //long time = doc["time"];
  //double latitude = doc["data"][0];
  //double longitude = doc["data"][1];
}

void loop() {
  
  StaticJsonDocument<200> doc;
  String inData;
  char json[50];
  float moves[50][6];
  int offset[2];

  while (Serial.available() > 0) {
    char received = Serial.read();
    inData += received;
  }

  inData.toCharArray(json, 50);
  
  // Deserialize the JSON document
  DeserializationError error = deserializeJson(doc, json);

  // Test if parsing succeeds.
  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.c_str());
    return;
  }

  int state = doc["state"];
  changeState(state);
  
  int instr = doc["instr"];
  switch (instr) {

    case 1:
    moves[50][6] = doc["moves"];
    makeMoves(moves);
    break;

    case 2:
    offset[2] = doc["offset"];
    applyOffset(offset);

    default:
    reset();
    break;
    
  }
}

void changeState(int state) {
  
}

void makeMoves(float moves[50][6]) {
  static Vector trans;
  static Vector rotat;
  for (int i = 0; i < 50; i++) {
    trans.x = moves[i][0];
    trans.y = moves[i][1];
    trans.z = moves[i][2];
    rotat.x = moves[i][3];
    rotat.x = moves[i][4];
    rotat.x = moves[i][5];
    
    Platform.applyTranslationAndRotation(trans, rotat);
    if (Serial.available() > 0) {
      loop();
    }
  }
  loop();
}

void applyOffset(int offset[2]) {
  int tx, ty, tz, rx, ry, rz;
  // convert offset to xyz xyz
  static Vector trans;
  static Vector rotat;
  trans.x = tx;
  trans.y = ty;
  trans.z = tz;
  rotat.x = rx;
  rotat.y = ry;
  rotat.z = rz;
  Platform.applyTranslationAndRotation(trans, rotat);
}

void reset() {
  static Vector trans;
  static Vector rotat;
  trans.x = 0;
  trans.y = 0;
  trans.z = 0;
  rotat.x = 0;
  rotat.y = 0;
  rotat.z = 0;
  Platform.applyTranslationAndRotation(trans, rotat);
}
