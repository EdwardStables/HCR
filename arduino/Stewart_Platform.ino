#include <Servo.h>

const float pi = 3.14159,
            //theta_r = angle between attachment points
            theta_r = radians(48.0),
            //theta_p = angle between rotation points
            theta_p = radians(23.2),
            //theta_s = orientation of the servos
            theta_s[] = { -pi / 3, 2 * pi / 3, pi, 0, pi / 3, -2 * pi / 3},
            //RD = distance to end effector attachment points
            RD = 2.395,
            //PD = distance to servo rotation points
            PD = 3.3,
            //L1 = servo arm length
            L1 = 1.0,
            //L2 = connecting arm length
            L2 = 4.72,
            //z_home = default z height with servo arms horizontal
            z_home = 4.25,
            //servo_min = lower limit for servo arm angle
            servo_min = 700,
            //servo_max = upper limit for servo arm angle
            servo_max = 2300,
            //servo_mult = multiplier to convert to milliseconds
            servo_mult = 1,
            //p = location of servo rotation points in base frame [x/y][1-6]
            p[2][6] = {{
                PD * cos(pi / 6 + theta_p), PD * cos(pi / 6 - theta_p), PD * cos(-(pi / 2 - theta_p)),
                -PD * cos(-(pi / 2 - theta_p)), -PD * cos(pi / 6 - theta_p), -PD * cos(pi / 6 + theta_p)
              },
              { PD * sin(pi / 6 + theta_p), PD * sin(pi / 6 - theta_p), PD * sin(-(pi / 2 - theta_p)),
                PD * sin(-(pi / 2 - theta_p)), PD * sin(pi / 6 - theta_p), PD * sin(pi / 6 + theta_p)
              }
            },
            //re = location of attachment points in end eector frame [x/y][1-6]
            re[2][6] = {{
                RD * cos(pi / 6 + theta_r), RD * cos(pi / 6 - theta_r), RD * cos(-(pi / 2 - theta_r)),
                -RD * cos(-(pi / 2 - theta_r)), -RD * cos(pi / 6 - theta_r), -RD * cos(pi / 6 + theta_r)
              },
              { RD * sin(pi / 6 + theta_r), RD * sin(pi / 6 - theta_r), RD * sin(-(pi / 2 - theta_r)),
                RD * sin(-(pi / 2 - theta_r)), RD * sin(pi / 6 - theta_r), RD * sin(pi / 6 + theta_r)
              }
            };

//servo_pin = servo pin assignments,
const int servo_pin[] = {9, 10, 11, 12, 14, 15},
            //servo_zero = zero angles for each servo (horizontal)
            servo_zero[6] = {1710, 1280, 1700, 1300, 1680, 1300};

Servo servo[6];
/*
  Servos 0, 2, 4: reversed (+ = down, - = up)
  Servos 1, 3, 5: normal (+ = up, - = down)
*/

void setup()
{
  Serial.begin(9600);
  for (int i = 0; i < 6; i++)
  {
    servo[i].attach(servo_pin[i]);
    servo[i].writeMicroseconds(servo_zero[i]);
  }
  delay(1000);
}
void loop()
{
  
  static float pe[6] = {0, 0, 0, radians(0), radians(0), radians(0)}, 
               theta_a[6], 
               servo_pos[6],
               q[3][6], 
               r[3][6], 
               dl[3][6], 
               dl2[6];
  /*
    pe = location and orientation of end eector frame relative to the base frame [sway, surge,
    heave, pitch, roll, yaw)
    theta_a = angle of the servo arm
    servo_pos = value written to each servo
    q = position of lower mounting point of connecting link [x,y,z][1-6]
    r = position of upper mounting point of connecting link
    dl = dierence between x,y,z coordinates of q and r
    dl2 = distance between q and r
  */
  for (int i = 0; i < 6; i++)
  {
    q[0][i] = L1 * cos(-theta_a[i]) * cos(theta_s[i]) + p[0][i];
    q[1][i] = L1 * cos(-theta_a[i]) * sin(theta_s[i]) + p[1][i];
    q[2][i] = -L1 * sin(-theta_a[i]);
    r[0][i] = re[0][i] * cos(pe[4]) * cos(pe[5]) + re[1][i] * (sin(pe[3]) * sin(pe[4]) * cos(pe[5]) -
              cos(pe[3]) * sin(pe[5])) + pe[0];
    r[1][i] = re[0][i] * cos(pe[4]) * sin(pe[5]) + re[1][i] * (cos(pe[3]) * cos(pe[5]) +
              sin(pe[3]) * sin(pe[4]) * sin(pe[5])) + pe[1];
    r[2][i] = -re[0][i] * sin(pe[4]) + re[1][i] * sin(pe[3]) * cos(pe[4]) + z_home + pe[2];
    dl[0][i] = q[0][i] - r[0][i];
    dl[1][i] = q[1][i] - r[1][i];
    dl[2][i] = q[2][i] - r[2][i];
    dl2[i] = sqrt(dl[0][i] * dl[0][i] + dl[1][i] * dl[1][i] + dl[2][i] * dl[2][i]) - L2;
    theta_a[i] += dl2[i];
    theta_a[i] = constrain(theta_a[i], servo_min, servo_max);
    if (i % 2 == 1)
      servo_pos[i] = servo_zero[i] + theta_a[i] * servo_mult;
    else
      servo_pos[i] = servo_zero[i] - theta_a[i] * servo_mult;
  }
  for (int i = 0; i < 6; i++)
  {
    servo[i].writeMicroseconds(servo_pos[i]);
  }

  pe[5] = pe[5] + 0.1;

  Serial.println("pe:");
  for(int i = 0; i < 6; i++)
  {
      Serial.print(pe[i], DEC);
      Serial.print("\t");
  }
  Serial.println();

  Serial.println("dl2:");
  for(int i = 0; i < 6; i++)
  {
      Serial.print(dl2[i], DEC);
      Serial.print("\t");
  }
  Serial.println();


  Serial.println("servo pos:");
  for(int i = 0; i < 6; i++)
  {
      Serial.print(servo_pos[i], DEC);
      Serial.print("\t");
  }
  Serial.println();

  delay(5);
}
