# STUART

This repository contains the code for STUART, a robot designed to evaluate the effects of robot interactivity on ratings given for facilities or services. The code is in two parts, Pi and Arduino.

## Pi

The Pi folder contains Python 3.7 code designed to be run on a Raspberry Pi 4. An earlier Raspberry Pi will struggle with running every subsystem, especially facial recognition. It should also be compatible with any Linux distribution, but the subprocess spawning mechanism is not compatible with Windows. 

The code is launched by running the file `CuteRobotStart.py` (named from the initial working name of the robot). This will launch each of the subsystems in their own process and transition to a mediator to transfer messages between them. 

The mediator code and subsystem base class are contained in the `hcrutils` folder. Any new subsystems should extend from the base shown here, and be included in `CuteRobotStart.py`. If it is desirable to not start a subsystem, their inclusion in the subsystems array can be commented out, this can be useful if testing without an install of OpenCV, or a serial connection.

The level of interactivity of the robot can be changed by setting the `self.interactivity` option in `pi/ai_subsystem/flags.py`, the three levels vary from no interactivity, to the full amount allowed by the robot's systems. 

Any selection on the vote screen will be saved to a csv file in the pi directory, showing the given rating, a timestamp, and the level of interactivity at the time. 

## Arduino

This code was written to run on a Teensy microcontroller. The main sketch `main.ino` requires the Stewart Platform library also included. The library handles inverse kinematics for the dimensions of this particular platform. CAD files for the design are available upon request, if needed. 


