#include <Adafruit_NeoPixel.h>
#include <ArduinoJson.h>
#include <Servo.h>
#include <Stewart.h>

#define LED_PIN 6
 
#define LED_COUNT 9

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

int pins[] = {14, 15, 9, 10, 11, 12};

Stewart Platform = Stewart(pins);

int speed_set = 20;

float position[6] = {0, 0, 0, 0, 0, 0};

int loop_no = 0;

void setup() {
  reset();
  strip.begin();
  for (int i = 0; i < 9; i++) {
    strip.setPixelColor(i, 0, 0, 0);
  }
  strip.show();

  pinMode(13, OUTPUT);
  // Initialize serial port
  Serial.begin(9600);
  Serial.println("Serial connection established");
  while (!Serial) continue;
}

void loop() {
  if (loop_no % 5 == 0) {
    digitalWrite(13, HIGH);
  } else {
    digitalWrite(13, LOW);
  }
  loop_no++;
  
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

    int last_instr = inData.lastIndexOf('{');
    String newInput = inData.substring(last_instr, inData.length());
    char json[newInput.length() + 1];
    newInput.toCharArray(json, inData.length() + 1);
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
    int x, colour;
    switch (instr) {

      case 1:
        Serial.print("Move pattern: ");
        x = doc["pattern"];
        Serial.println(x);
        movePattern(doc["pattern"]);
        break;

      case 2:
        Serial.print("Idle");
        idle_state();
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
        colour = doc["colour"];
        Serial.println(colour);
        changeColour(colour);
        break;
      
      default:
        reset();
    
    }
  }
}

void movePattern(int pattern) {

  float pattern0[][6] = {{0,0,-8,0,0,0},{0,0,8,0,0,0}};
  float pattern1[][6] = {{0,0,5,0,0,0},{0,0,-5,0,0,0}};
  float pattern2[][6] = {{0,10,0,0,0,0},{0,-10,0,0,0,0}};
  float pattern3[][6] = {{15,0,0,0,0,0},{-15,0,0,0,0,0}};
  
  switch (pattern) {
    case 0:
      iterateMoves(pattern0, 2);
      break;

    case 1:
      iterateMoves(pattern1, 2);
      break;

    case 2:
      iterateMoves(pattern2, 2);
      break;

    case 3:
      iterateMoves(pattern3, 2);
      break;

    default:
      Serial.println("Unknown pattern");
      break;
  }
}

void iterateMoves(float moves[][6], int arraySize) {
  static Vector trans;
  static Vector rotat;
  // Loops through moves Array and applies moves

  for (int i = 0; i < arraySize; i++) {
    for (int j = 0; j < speed_set; j++) {
      trans.x = position[0] + (moves[i][0] - position[0]) * j / speed_set;
      trans.y = position[1] + (moves[i][1] - position[1]) * j / speed_set;
      trans.z = position[2] + (moves[i][2] - position[2]) * j / speed_set;
      rotat.x = radians(position[3] + (moves[i][3] - position[3]) * j / speed_set);
      rotat.y = radians(position[4] + (moves[i][4] - position[4]) * j / speed_set);
      rotat.z = radians(position[5] + (moves[i][5] - position[5]) * j / speed_set);
    
      Platform.applyTranslationAndRotation(trans, rotat);

      if (Serial.available() > 0) {
        for (int k = 0; k < 6; k++) {
          position[k] = position[k] + (moves[i][k] - position[k]) * j / speed_set;
        }
        return;
      }
    }
    for (int k = 0; k < 6; k++) {
      position[k] = moves[i][k];
    }
    delay(200);
  }
}

void idle_state() {
  while (Serial.available() <= 0) {
    movePattern(3);
  }
  reset();
}

void applyOffset(float offset[]) {
  if (offset[0] == 0 && offset[1] == 0) {
    return;
  }
  static Vector trans;
  static Vector rotat;
  float rx_adjust, rz_adjust;
  rx_adjust = offset[1] * -8;
  rz_adjust = offset[0] * -24;

  rx_adjust = position[3] + rx_adjust;
  rz_adjust = position[5] + rz_adjust;
  
  if (rz_adjust > 24) {
    rz_adjust = 24;
  }
  if (rz_adjust < -24) {
    rz_adjust = -24;
  }
  if (rx_adjust > 8) {
    rx_adjust = 8;
  }
  if (rx_adjust < -8) {
    rx_adjust = -8;
  }

  Serial.println(rz_adjust);
  Serial.println(rx_adjust);
    
  for (int i = 1; i <= 35; i++) {
    trans.x = 0;
    trans.y = 0;
    trans.z = 0;
    rotat.x = radians(position[3] + (rx_adjust - position[3]) * i / 35);
    rotat.y = 0;
    rotat.z = radians(position[5] + (rz_adjust - position[5]) * i / 35);
    Platform.applyTranslationAndRotation(trans, rotat);

    if (Serial.available() > 0) {
      position[3] = position[3] + (rx_adjust - position[3]) * i / 35;
      position[5] = position[5] + (rz_adjust - position[5]) * i / 35;
      return;
    }
  }

  position[5] = rz_adjust;
  position[3] = rx_adjust;
  Serial.println(position[5]);
  Serial.println(position[3]);
  
  // Offset needs converting to xyz xyz
  Serial.println("Offset applied (conversion still needed)");
}

void changeColour(int colour) {
  int r, g, b;
  switch (colour) {
    case 0:
      r = 255; g = 255; b = 0;
      break;
      
    case 1:
      r = 255; g = 100; b = 0;
      break;
      
    case 2:
      r = 0; g = 0; b = 255;
      break;
      
    case 3: 
      r = 255; g = 255; b = 255;
      break;
      
    default: 
      r, g, b = 0;
  }
  for (int i = 0; i < 9; i++) {
    strip.setPixelColor(i, r, g, b);
  }
  strip.show();
  Serial.print("Colour changed to: ");
  Serial.println(colour);
}

void reset() {
  static Vector trans;
  static Vector rotat;

  for (int i = 1; i <= speed_set; i++) {
    trans.x = position[0] - position[0] * i / speed_set;
    trans.y = position[1] - position[1] * i / speed_set;
    trans.z = position[2] - position[2] * i / speed_set;
    rotat.x = radians(position[3] - position[3] * i / speed_set);
    rotat.y = radians(position[4] - position[4] * i / speed_set);
    rotat.z = radians(position[5] - position[5] * i / speed_set);
    Platform.applyTranslationAndRotation(trans, rotat);
  }
  for (int i = 0; i < 6; i++) {
    position[i] = 0;
  }
  Serial.println("Reset completed");
}
