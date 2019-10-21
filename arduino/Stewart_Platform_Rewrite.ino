struct Vector
{
  float x = 0;
  float y = 0;
  float z = 0;
};

Vector translation, rotation, initialHeight;
Vector baseJoint[6], platformJoint[6], q[6], l[6], A[6];
float alpha[6];
float baseRadius, platformRadius, hornLength, legLength;

// base angles
float baseAngles[] = {
  314.9, 345.1, 74.9, 105.1, 194.9, 225.1};

// platform angles
float platformAngles[] = {
  322.9, 337.1, 82.9, 97.1, 202.9, 217.1};

// Angles between servo horns and x axis
float beta[] = {
  -8*PI/3, PI/3, 0, -PI, -4*PI/3, -7*PI/3};
  
// Platform Measurements
const float SCALE_INITIAL_HEIGHT = 120;
const float SCALE_BASE_RADIUS = 70;
const float SCALE_PLATFORM_RADIUS = 70;
const float SCALE_HORN_LENGTH = 36;
const float SCALE_LEG_LENGTH = 125;

void setup() {
  // put your setup code here, to run once:

  initialHeight.z = SCALE_INITIAL_HEIGHT;
  baseRadius = SCALE_BASE_RADIUS;
  platformRadius = SCALE_PLATFORM_RADIUS;
  hornLength = SCALE_HORN_LENGTH;
  legLength = SCALE_LEG_LENGTH;

  for (int i=0; i<6; i++) {
      float mx = baseRadius*cos(radians(baseAngles[i]));
      float my = baseRadius*sin(radians(baseAngles[i]));
      baseJoint[i].x = mx;
      baseJoint[i].y = my;
  }

  for (int i=0; i<6; i++) {
     float mx = platformRadius*cos(radians(platformAngles[i]));
     float my = platformRadius*sin(radians(platformAngles[i]));

     platformJoint[i].x = mx;
     platformJoint[i].y = my;

  }
  calcQ();

}

void loop() {
  // put your main code here, to run repeatedly:
  
  static Vector Translation;
  static Vector Rotation;

  applyTranslationAndRotation(Translation,Rotation);

  // Debug 
  Serial.print(Translation.x, DEC);
  Serial.print(" Alpha: \t");
  for(int i = 0; i < 6; i++)
  {
    Serial.print(alpha[i], DEC);
    Serial.print(", ");
  }
  Serial.print("\n");

  Translation.x = (Translation.x + 1);

  if(Translation.x > 100)
    Translation.x = -100;

}

void applyTranslationAndRotation(Vector t, Vector r)
{
  translation.x = t.x;
  translation.y = t.y;
  translation.z = t.z;

  rotation.x = r.x;
  rotation.y = r.y;
  rotation.z = r.z;

  calcQ();
  calcAlpha();
}

void calcQ()
{

  for(int i = 0; i < 6; i++)
  {
    // rotation
    q[i].x = cos(rotation.z)*cos(rotation.y)*platformJoint[i].x +
        (-sin(rotation.z)*cos(rotation.x)+cos(rotation.z)*sin(rotation.y)*sin(rotation.x))*platformJoint[i].y +
        (sin(rotation.z)*sin(rotation.x)+cos(rotation.z)*sin(rotation.y)*cos(rotation.x))*platformJoint[i].z;
    
    q[i].y = sin(rotation.z)*cos(rotation.y)*platformJoint[i].x +
        (cos(rotation.z)*cos(rotation.x)+sin(rotation.z)*sin(rotation.y)*sin(rotation.x))*platformJoint[i].y +
        (-cos(rotation.z)*sin(rotation.x)+sin(rotation.z)*sin(rotation.y)*cos(rotation.x))*platformJoint[i].z;

    q[i].z = -sin(rotation.y)*platformJoint[i].x +
        cos(rotation.y)*sin(rotation.x)*platformJoint[i].y +
        cos(rotation.y)*cos(rotation.x)*platformJoint[i].z;
    
    // translation
    q[i].x += translation.x + initialHeight.x;
    q[i].y += translation.y + initialHeight.y;
    q[i].z += translation.z + initialHeight.z;

    l[i].x = q[i].x - baseJoint[i].x;
    l[i].y = q[i].y - baseJoint[i].y;
    l[i].z = q[i].z - baseJoint[i].z;
  }
  
}

void calcAlpha()
{
  for (int i=0; i<6; i++) {

      float magSqL = (l[i].x*l[i].x) + (l[i].y*l[i].y) + (l[i].z*l[i].z);
      
      float L = magSqL-(legLength*legLength)+(hornLength*hornLength);
      float M = 2*hornLength*(q[i].z-baseJoint[i].z);
      float N = 2*hornLength*(cos(beta[i])*(q[i].x-baseJoint[i].x) + sin(beta[i])*(q[i].y-baseJoint[i].y));
      alpha[i] = asin(L/sqrt(M*M+N*N)) - atan2(N, M);

      A[i].x = hornLength*cos(alpha[i])*cos(beta[i]) + baseJoint[i].x; 
      A[i].y = hornLength*cos(alpha[i])*sin(beta[i]) + baseJoint[i].y; 
      A[i].z = hornLength*sin(alpha[i]) + baseJoint[i].z;

      float xqxb = (q[i].x-baseJoint[i].x);
      float yqyb = (q[i].y-baseJoint[i].y);
      float h0 = sqrt((legLength*legLength)+(hornLength*hornLength)-(xqxb*xqxb)-(yqyb*yqyb)) - q[i].z;

      float L0 = 2*hornLength*hornLength;
      float M0 = 2*hornLength*(h0+q[i].z);
      float a0 = asin(L0/sqrt(M0*M0+N*N)) - atan2(N, M0);

      //println(i+":"+alpha[i]+"  h0:"+h0+"  a0:"+a0);
  }
}
