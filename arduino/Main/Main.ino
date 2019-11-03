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

/*void state(int state);
void makeMoves(float moves[][6]);
void applyOffset(int offset[2]);
void reset();*/

int pins[] = {9, 10, 11, 12, 14, 15};

Stewart Platform = Stewart(pins);

void setup() {
  // Initialize serial port
  Serial.begin(9600);
  while (!Serial) continue;
}

void loop() {
  
  // Setup JSON input, 1024 bytes
  StaticJsonDocument<1024> doc;
  String inData;
  //char json[48];
  int offset[2];

  // Not tested but should read Serial data into a string
  /*while (Serial.available() > 0) {
    char received = Serial.read();
    inData += received;
  }

  // Convert Serial data to a char Array
  inData.toCharArray(json, 48);*/
  // Test JSON variable
  char json[] = "{\"instr\":1,\"moves\":[[0,1,2,3,4,5],[6,7,8,9,10,11]]}";
  // Deserialize the JSON document
  DeserializationError error = deserializeJson(doc, json);

  // Test if parsing succeeds
  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.c_str());
    return;
  }

  // Simple function call to handle state change (function not written yet)
  //int state = doc["state"];
  //changeState(state);
  
  // Switch statement for instruction type
  int instr = doc["instr"];
  switch (instr) {

    // Case 1 is a movement pattern, eg dancing
    case 1:
    int arraySize = doc["moves"].size();
    float moves[arraySize][6];
    // Loop to copy doc["moves"] array as it behaves strangely (data type cannot be inferred)
    for (int x = 0; x < arraySize; x++) {
      for (int y = 0; y < 6; y++) {
        moves[x][y] = doc["moves"][x][y];
      }
    }
    makeMoves(moves, arraySize);
    break;

    // Case 2 is the offset instruction
    case 2:
    float offset[2];
    // Loop to copy doc["offset"] array as it behaves strangely (data type cannot be inferred)
    for (int x = 0; x < 2; x++) {
        moves[x] = doc["offset"][x];
    }
    applyOffset(offset);

    // Default case resets position
    default:
    reset();
    break;
    
  }
}

void changeState(int state) {
  // Function to change LED to indicate current state (not written yet)
  Serial.print("State changed to state ");
  Serial.println(state);
}

void makeMoves(float moves[][6], int arraySize) {
  static Vector trans;
  static Vector rotat;
  // Loops through moves Array and applies moves
  for (int i = 0; i < arraySize; i++) {
    trans.x = moves[i][0];
    trans.y = moves[i][1];
    trans.z = moves[i][2];
    rotat.x = moves[i][3];
    rotat.y = moves[i][4];
    rotat.z = moves[i][5];
    
    // Jack may need to alter the library so that this single instruction executes the movement at the correct speed
    Platform.applyTranslationAndRotation(trans, rotat);
    // Checks if new instruction is available IE interrupts
    if (Serial.available() > 0) {
      loop();
    }
  }
  loop();
}

void applyOffset(int offset[2]) {
  int tx, ty, tz, rx, ry, rz;
  // Offset needs converting to xyz xyz
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
  // These values need calibrating I think
  trans.x = 0;
  trans.y = 0;
  trans.z = 0;
  rotat.x = pi / 4;
  rotat.y = pi / 4;
  rotat.z = pi / 4;
  Platform.applyTranslationAndRotation(trans, rotat);
}
