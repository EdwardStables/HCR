# testingCode.py

from stateMachine import StateMachine
import time
from states import *
from flags import Flag
import keyboard

cuteRobot = StateMachine()

for i in range(3000):
    print("Cycle:", i, end='')

    cuteRobot.event("")

    t_end = time.time() + 2

    while time.time() < t_end:
    
        if keyboard.is_pressed('1'):
            flag.person = not flag.person
        if keyboard.is_pressed('2'):
            flag.listening = not flag.listening
        if keyboard.is_pressed('3'):
            flag.processing = not flag.processing
        if keyboard.is_pressed('4'):
            flag.talking = not flag.talking

    flag.printFlags()


