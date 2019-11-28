#include <ArduinoJson.h>
#include <Servo.h>
#include <Stewart.h>

int pins[] = {9, 10, 11, 12, 14, 15};

Stewart Platform = Stewart(pins);

void setup() {
  // Initialize serial port
  Serial.begin(9600);
  Serial.println("Serial connection established");
  while (!Serial) continue;
}

void loop() {
  // Setup JSON input, 1024 bytes
  StaticJsonDocument<1024> doc;
  String inData;
  float offset[2];
  float move[6];
  
  if (Serial.available() > 0) {
    
    while (Serial.available() > 0) {
      char received = Serial.read();
      inData += received;
    }
    
    char json[inData.length() + 1];
    inData.toCharArray(json, inData.length() + 1);
    Serial.println(json);
    
    // Deserialize the JSON document
    DeserializationError error = deserializeJson(doc, json);

    // Test if parsing succeeds.
    if (error) {
      Serial.print(F("deserializeJson() failed: "));
      Serial.println(error.c_str());
      return;
    }
  
    int instr = doc["instr"];
    int x;
    String colour = "";
    switch (instr) {

      case 1:
        Serial.print("Move pattern: ");
        x = doc["pattern"];
        Serial.println(x);
        movePattern(doc["pattern"]);
        break;

      case 2:
        Serial.print("Make move: ");
        for (int i = 0; i < 6; i++) {
          move[i] = doc["move"][i];
          Serial.print(move[i]);
          Serial.print(" ");
        }
        Serial.println();
        makeMove(move);
        break;

      case 3:
        Serial.print("Apply offset: ");
        for (int i = 0; i < 2; i++) {
          offset[i] = doc["offset"][i];
          Serial.print(offset[i]);
          Serial.print(" ");
        }
        Serial.println();
        applyOffset(offset);
        break;

      case 4:
        Serial.print("Change colour: ");
        colour = doc["colour"].as<String>();
        Serial.println(colour);
        changeColour(doc["colour"]);
        break;
      
      default:
        reset();
    
    }
  }
}

void movePattern(int pattern) {

  float pattern0[][6] = {{0,0,-30,0,0,0},{0,0,20,0,0,0}};
  float pattern1[][6] = {{0,0,-30,0,0,0},{0,0,40,0,0,0},{0,0,20,0,0,0}};
  
  switch (pattern) {
    case 0:
      iterateMoves(pattern0, 2);
      break;

    case 1:
      iterateMoves(pattern1, 3);
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
