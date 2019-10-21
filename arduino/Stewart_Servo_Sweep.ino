/* Sweep
 by BARRAGAN <http://barraganstudio.com> 
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://arduino.cc/en/Tutorial/Sweep
*/ 

#include <Servo.h> 
 
Servo Servos[6];  // create servo object to control a servo 
                // twelve servo objects can be created on most boards
 
int pos = 0;    // variable to store the servo position 

bool ledState = HIGH;
 
void setup() 
{ 
  Servos[0].attach(9);  
  Servos[1].attach(10);
  Servos[2].attach(11);
  Servos[3].attach(12);
  Servos[4].attach(14);
  Servos[5].attach(15);
  
  pinMode(13, OUTPUT);
} 
 
void loop() 
{ 
  for(pos = 0; pos <= 180; pos += 1) // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    for(int i = 0; i < 6; i++)
    {
      if(i%2 == 0)
        Servos[i].write(pos);
      else
        Servos[i].write(180-pos);
    }                                // tell servo to go to position in variable 'pos' 
    delay(5);                       // waits 15ms for the servo to reach the position 
  } 
  for(pos = 180; pos>=0; pos-=1)     // goes from 180 degrees to 0 degrees 
  {                                
    for(int i = 0; i < 6; i++)
    {
      if(i%2 == 0)
        Servos[i].write(pos);
      else
        Servos[i].write(180-pos);
    }                                 // tell servo to go to position in variable 'pos' 
    delay(5);                       // waits 15ms for the servo to reach the position 
  } 

  digitalWrite(13, ledState);
  ledState = !ledState;
} 
