# states.py

from misc import *
from flags import Flag

# Set up the flags
flag = Flag()

class State(object):
    """
    Generic state class that can run code and move into the next state.
    """
    def run(self):
        assert 0, "run not implemented"
    def event(self, event):
        pass

class Idle(State):
    """
    Idle State

    - Robot will idle.
    - If the person flag is set then move to the WatchingGreeting state.
    - Otherwise remain in this state.
    """
    def run(self):
        print("IDLE STATE")
        flag.talking = False
        flag.processing = False
        flag.listening = False
        flag.name = "unknown"
        # flag.printFlags()
    def event(self, event):
        if flag.person == True:
            return WatchingGreeting()
        return self

class WatchingGreeting(State):
    """
    WatchingGreeting State

    - Robot watches person.
    - If the person is known, then the robot welcomes them and moves into the WatchingWaiting state.
    - If the person is unknown, tell them they are unknown and move into the WatchingGetName state.
    - If the person leaves then return to Idle state.
    - Otherwise remain in this state.
    """
    def run(self): 
        print("GREETING STATE")
        flag.talking = True
        flag.listen = False
        # flag.printFlags()
    def event(self, event):
        if flag.person == True and flag.name != "unknown":
            say(("Hello" + flag.name))
            return WatchingWaiting()
        elif flag.person == True and flag.name == "unknown":
            say("I don't know you, what is your name?")
            flag.name = getName()
            return WatchingGetName()
        elif flag.person == False:
            return Idle()
        return self

class WatchingGetName(State):
    """
    WatchingGetName State

    - If the name is updated from unknown then move to WatchingGreeting state.
    - If the person leaves then return to Idle state.
    - Otherwise remain in this state.
    """
    def run(self): 
        print("GETTING NAME STATE")
        flag.talking = False
        flag.listening = True
        # flag.printFlags()
        # Wait for name to switch from "unknown" to something new
    def event(self, event):
        if flag.person == True and flag.name != "unknown":
            return WatchingGreeting()
        elif flag.person == False:
            return Idle()
        return self

class WatchingWaiting(State):
    """
    WatchingWaiting State

    - If the processing flag is set then move to WatchingProcessing state.
    - If the person leaves then return to Idle state.
    - Otherwise remain in this state.   
    """
    def run(self): 
        print("WATCHING STATE")
        flag.processing = False
        flag.listening = True
        flag.talking = False
        # flag.printFlags()
    def event(self, event):
        if flag.person == True and flag.processing == True:
            return WatchingProcessing()
        if flag.person == False:
            return Idle()
        return self

class WatchingTalking(State):
    """
    WatchingTalking State

    - If the person is still present and the robot isn't talking go to the WatchingWaiting state.
    - If the person is leaves and the robot isn't talking go to the Idle state.
    - Otherwise remain in this state.   
    """
    def run(self): 
        print("TALKING STATE")
        # flag.printFlags()
    def event(self, event):
        if flag.person == True and flag.talking == False:
            return WatchingWaiting()
        if flag.person == False and flag.talking == False:
            return Idle()
        return self

class WatchingProcessing(State):
    """
    WatchingProcessing State

    - If the person is still present go to the WatchingTalking state.
    - If the person leabes go to the IDle state.
    - Otherwise remain in this state.
    """
    def run(self): 
        print("PROCESSING STATE")
        flag.listening = False
        # flag.printFlags()
    def event(self, event):
        if flag.person == True:
            return WatchingTalking()
        if flag.person == False:
            return Idle()
        return self