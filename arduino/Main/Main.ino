#include <Adafruit_NeoPixel.h>
#include <ArduinoJson.h>
#include <Servo.h>
#include <Stewart.h>

#define LED_PIN 6
 
#define LED_COUNT 9

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

int pins[] = {14, 15, 9, 10, 11, 12};

Stewart Platform = Stewart(pins);

float position[2] = {0, 0};

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
  float pattern1[][6] = {{0,0,8,0,0,0},{0,0,-8,0,0,0}};
  float pattern2[][6] = {{0,40,0,0,0,0},{0,-40,0,0,0,0}};
  float pattern3[][6] = {{40,0,0,0,0,0},{-40,0,0,0,0,0}};

  Serial.println("movePattern");
  
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
    trans.x = moves[i][0];
    trans.y = moves[i][1];
    trans.z = moves[i][2];
    rotat.x = moves[i][3];
    rotat.y = moves[i][4];
    rotat.z = moves[i][5];
    
    Platform.applyTranslationAndRotation(trans, rotat);
    delay(300);
  }
}

void idle_state() {
  while (Serial.available() <= 0) {
    movePattern(1);
    movePattern(2);
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
  float rz_adjust, rx_adjust, rz, rx;
  rz_adjust = offset[0] * -24;
  rx_adjust = offset[1] * -8;
  
  rz_adjust = position[0] + rz_adjust;
  rx_adjust = position[1] + rx_adjust;
  
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
    rotat.x = radians(position[1] + (rx_adjust - position[1]) * i / 35);
    rotat.y = 0;
    rotat.z = radians(position[0] + (rz_adjust - position[0]) * i / 35);
    Platform.applyTranslationAndRotation(trans, rotat);
    //Serial.print(i);
    //Serial.println(" / 8 movement");

    if (Serial.available() > 0) {
      position[0] = position[0] + (rz_adjust - position[0]) * i / 35;
      position[1] = position[1] + (rx_adjust - position[1]) * i / 35;
      return;
    }
    //delayMicroseconds(5000 / sqrt(offset[0] * offset[0] + offset[1] * offset[1]));
  }

  position[0] = rz_adjust;
  position[1] = rx_adjust;
  Serial.println(position[0]);
  Serial.println(position[1]);
  
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
  trans.x = 0;
  trans.y = 0;
  trans.z = 0;
  rotat.x = 0;
  rotat.y = 0;
  rotat.z = 0;
  position[0] = 0;
  position[1] = 0;
  Platform.applyTranslationAndRotation(trans, rotat);
  Serial.println("Reset completed");
  delay(500);
}
