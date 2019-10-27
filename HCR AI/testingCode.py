# testingCode.py

from stateMachine import StateMachine
import time
from states import *
from flags import Flag
import keyboard
import os

def printControlPanel(cycle):
    """
    Prints the AMAZING ROBOT CONSOLE.
    """
    def fp(b):
        if b == True:
            return "True "
        else:
            return "False"

    def s(state):
        if state == "Idle()":
            return "Idling            "
        elif state == "WatchingTalking()":
            return "WatchingTalking   "
        elif state == "WatchingGreeting()":
            return "WatchingGreeting  "
        elif state == "WatchingProcessing()":
            return "WatchingProcessing"
        elif state == "WatchingGetName()":
            return "WatchingGetName   "
        elif state == "WatchingWaiting()":
            return "WatchingWaiting   "

    def printCycle(cycle):
        if cycle < 0:
            return "---- "
        if cycle < 10:
            t = (str(cycle) + "    ")
            return t
        elif cycle < 100:
            t = (str(cycle) + "   ")
            return t
        elif cycle < 1000:
            t = (str(cycle) + "  ")
            return t
        elif cycle < 10000:
            t = (str(cycle) + " ")
            return t
        elif cycle < 100000:
            return str(cycle)
        else:
            return "error"
    
    os.system('clear')
    print(" ",
          "\n  AMAZING ROBOT CONSOLE V1.0",
          "\n",
          "\n  Cycle:", printCycle(cycle),
          "\n",
          "\n  Current State:", s(flag.currentState),"   Log:",
          "\n                                      ", printCycle(cycle - 7), ": ",  s(log[cycle]),
          "\n  Flags:                              ", printCycle(cycle - 6), ": ",  s(log[cycle + 1]),
          "\n   person     = ", fp(flag.person), "               ", printCycle(cycle - 5), ": ",  s(log[cycle + 2]),
          "\n   listening  = ", fp(flag.listening), "               ", printCycle(cycle - 4), ": ",  s(log[cycle + 3]),
          "\n   processing = ", fp(flag.processing), "               ", printCycle(cycle - 3), ": ",  s(log[cycle + 4]),
          "\n   talking    = ", fp(flag.talking), "               ", printCycle(cycle - 2), ": ",  s(log[cycle + 5]), 
          "\n                                      ", printCycle(cycle - 1), ": ",  s(log[cycle + 6]), 
          "\n   name       = ", flag.name,
          "\n   question   = ", flag.question,
          end="")

cuteRobot = StateMachine()

# Keep track of states
log = [
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " "
    ]

for i in range(3000):
    
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

    log.append(flag.currentState)

    printControlPanel(i)
