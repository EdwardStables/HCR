#include <Servo.h>
#include <Stewart.h>
//#include <string>

// Array of pins to connect to servos
int pins[] = {9, 10, 11, 12, 14, 15};
// Create stewart platform object
Stewart Platform = Stewart(pins);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("<Arduino is ready>");
  // Zero Platform
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    String inData;
    inData = Serial.readStringUntil('\n');
    Serial.println("data: " + inData);
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, inData);
    state(doc["state"]);
    String instr = doc["instr"];
    switch (instr) {
      case "move pattern";
        movePattern(doc);
        break;

      case "move offset";
        moveOffset(doc);
        break;

      default:
        reset();
    }
  }
  
  // Set up vectors for platform translation and rotation
  static Vector Trans;
  static Vector Rotat;
  // Move Platform
  Platform.applyTranslationAndRotation(Trans, Rotat);

  // Increment translation.z to make platform move in z direction
  Trans.z += 0.1;

  // Limit z movement so program doesn't move platform to endpoint then stop
  if(Trans.z > 50)
    Trans.z = -50;

  // Wait to move slower
  delay(5);

}

void stateChange(String state) {
  
}

void reset() {
  
}

static movePattern() {
  float moves[][] = doc["moves"];
}
