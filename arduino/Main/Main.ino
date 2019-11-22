#include <ArduinoJson.h>
#include <Servo.h>
#include <Stewart.h>

int pins[] = {9, 10, 11, 12, 14, 15};
bool once;

Stewart Platform = Stewart(pins);

void setup() {
  // Initialize serial port
  Serial.begin(9600);
  while (!Serial) continue;
  once = true;
}

void loop() {
  // Setup JSON input, 1024 bytes
  StaticJsonDocument<1024> doc;
  String inData;
  float offset[2];
  float move[6];
  
  if (Serial.available() > 0) {
    once = false;
    
    while (Serial.available() > 0) {
      char received = Serial.read();
      inData += received;
    }
    
    Serial.println(inData);
    char json[inData.length()];
    inData.toCharArray(json, inData.length());
    //char json[] = "{\"instr\":1,\"state\":0,\"moves\":[[0,0,40,0,0,0],[0,0,-30,0,0,0]]}";
    // Deserialize the JSON document
    Serial.println(json);
    DeserializationError error = deserializeJson(doc, json);

    // Test if parsing succeeds.
    if (error) {
      Serial.print(F("deserializeJson() failed: "));
      Serial.println(error.c_str());
      return;
    }
  
    int instr = doc["instr"];
    switch (instr) {

      case 1:
      movePattern(doc["pattern"]);
      break;

      case 2:
      move[6] = doc["move"];
      makeMove(move);
      break;

      case 3:
      offset[2] = doc["offset"];
      applyOffset(offset);
      break;

      case 4:
      changeColour(doc["colour"]);
      break;
      
      default:
      reset();
      break;
    
    }
  }
}

void movePattern(int pattern) {

  switch (pattern) {

    case 0:
    float moves[][6] = {{0,0,-30,0,0,0}};
    iterateMoves(moves, sizeof(moves));
    break;

    case 1:
    float moves[][6] = {{0,0,-30,0,0,0},{0,0,40,0,0,0}};
    iterateMoves(moves, sizeof(moves));
    break; 

    default:
    break;
    
  }
}

void iterateMoves(float moves[][6], int arraySize) {
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
    Serial.println(trans.x);
    Serial.println(trans.y);
    Serial.println(trans.z);
    Serial.println(rotat.x);
    Serial.println(rotat.y);
    Serial.println(rotat.z);
    
    Platform.applyTranslationAndRotation(trans, rotat);
    delay(500);
    
    // Checks if new instruction is available IE interrupts
    if (Serial.available() > 0) {
      loop();
    }
  }
}

void makeMove(float move[]) {
  static Vector trans;
  static Vector rotat;
  trans.x = move[0];
  trans.y = move[1];
  trans.z = move[2];
  rotat.x = move[3];
  rotat.y = move[4];
  rotat.z = move[5];
  
  Platform.applyTranslationAndRotation(trans, rotat);
  delay(500);
}

void applyOffset(float offset[2]) {
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
  delay(500);
}

void changeColour(String colour) {
  // some colour change thing
  Serial.print("Colour changed to: ");
  Serial.println(colour);
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
  delay(500);
}
