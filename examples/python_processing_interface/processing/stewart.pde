import peasy.*; //<>//
import controlP5.*;
import oscP5.*;
import netP5.*; //osc library
import processing.net.*;
import websockets.*;

float MAX_TRANSLATION = 50;
float MAX_ROTATION = PI/2;

ControlP5 cp5;
PeasyCam camera;
Platform mPlatform;

Client myClient;

OscP5 oscP5;
NetAddress mOscOut; // address of the pi connected to the motors

Slider PosX, PosY, PosZ, RotX, RotY, RotZ;

float posX=0, posY=0, posZ=0, rotX=0, rotY=0, rotZ=0;
boolean ctlPressed = false;

void setup() {
  size(2048, 1024, P3D);
  smooth();
  frameRate(60);
  textSize(15);

  myClient = new Client(this, "127.0.0.1", 50007);

  mOscOut = new NetAddress("192.168.0.24", 8888);

  camera = new PeasyCam(this, 400);
  camera.setRotations(-1.0, 0.0, 0.0);
  camera.lookAt(8.0, -50.0, 80.0);

  mPlatform = new Platform(1);
  mPlatform.applyTranslationAndRotation(new PVector(), new PVector());

  ControlFont cf0 = new ControlFont(createFont("Arial", 30));
  
  cp5 = new ControlP5(this);
  
  cp5.setFont(cf0);

  PosX = cp5.addSlider("posX")
    .setPosition(20, 20)
    .setSize(360, 60).setRange(-1, 1);
  PosY = cp5.addSlider("posY")
    .setPosition(20, 90)
    .setSize(360, 60).setRange(-1, 1);
  PosZ = cp5.addSlider("posZ")
    .setPosition(20, 160)
    .setSize(360, 60).setRange(-1, 1);

  RotX = cp5.addSlider("rotX")
    .setPosition(width-470, 20)
    .setSize(360, 60).setRange(-1, 1);
  RotY = cp5.addSlider("rotY")
    .setPosition(width-470, 90)
    .setSize(360, 60).setRange(-1, 1);
  RotZ = cp5.addSlider("rotZ")
    .setPosition(width-470, 160)
    .setSize(360, 60).setRange(-1, 1);
  
  
  cp5.setAutoDraw(false);
  camera.setActive(true);
}

void draw() {
  background(200);
  String[] vecs = {};
  if(myClient.available() > 0){
    String str = myClient.readString(); 
    vecs = split(str, ',');
  }
  if(vecs.length == 7){
    PosX.setValue(float(vecs[1]));
    PosY.setValue(float(vecs[2]));
    PosZ.setValue(float(vecs[3]));
    RotX.setValue(float(vecs[4]));
    RotY.setValue(float(vecs[5]));
    RotZ.setValue(float(vecs[6]));
  }else{
    println(vecs);
  }

  mPlatform.applyTranslationAndRotation(PVector.mult(new PVector(posX, posY, posZ), MAX_TRANSLATION), 
    PVector.mult(new PVector(rotX, rotY, rotZ), MAX_ROTATION));
  mPlatform.draw();

  hint(DISABLE_DEPTH_TEST);
  camera.beginHUD();
  cp5.draw();
  camera.endHUD();
  hint(ENABLE_DEPTH_TEST);
}

void controlEvent(ControlEvent theEvent) {
  camera.setActive(false);
}
void mouseReleased() {
  camera.setActive(true);
}

long lastTime = 0;

void sendOSC() {
  //after a UI event send a OSC packege
  float[] angles = mPlatform.getAlpha();

  for (float f : angles) {
    if (Float.isNaN(f)) {
      return;
    }
  }

  OscMessage myMessage = new OscMessage("/angles");
  myMessage.add(angles); /* add an int array to the osc message */

  oscP5.flush(myMessage, mOscOut);
  lastTime = millis();
}

void mouseDragged () {
  if (ctlPressed) {
    //posX = map(mouseX, 0, width, -1, 1);
    //posY = map(mouseY, 0, height, -1, 1);
  }
}


void keyPressed() {
  if (key == ' ') {
    camera.setRotations(-1.0, 0.0, 0.0);
    camera.lookAt(8.0, -50.0, 80.0);
    camera.setDistance(400);
    
    PosX.setValue(0);
    PosY.setValue(0);
    PosZ.setValue(0);
    
    RotX.setValue(0);
    RotY.setValue(0);
    RotZ.setValue(0);
    
    //mPlatform.applyTranslationAndRotation(PVector.mult(new PVector(0, posY, posZ), MAX_TRANSLATION), 
    //  PVector.mult(new PVector(rotX, rotY, rotZ), MAX_ROTATION));
    
    //mPlatform.draw();
    
  } else if (keyCode == CONTROL) {
    camera.setActive(false);
    ctlPressed = true;
  }
}

void keyReleased() {
  if (keyCode == CONTROL) {
    camera.setActive(true);
    ctlPressed = false;
  }
}
