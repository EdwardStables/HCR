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
        flag.currentState = "Idle()"
        flag.talking = False
        flag.processing = False
        flag.listening = False
        flag.name = "unknown"
        
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
        flag.currentState = "WatchingGreeting()"
        flag.talking = True
        flag.listen = False
        
    def event(self, event):
        
        if flag.person == True and flag.name != "unknown":
            say(("Hello " + flag.name))
            return WatchingWaiting()
        
        elif flag.person == True and flag.name == "unknown":
            say("I don't know you, what is your name?")
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
        flag.currentState = "WatchingGetName()"
        flag.talking = False
        flag.listening = True
        
    def event(self, event):
        
        if flag.person == True: # and flag.name != "unknown":
            flag.name = getName()
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
        flag.currentState = "WatchingWaiting()"
        flag.processing = False
        flag.listening = True
        flag.talking = False
        
    def event(self, event):
        
        if flag.person == True and flag.processing == True:
            say("What is your question?")
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
        flag.currentState = "WatchingTalking()"
        
    def event(self, event):        
        
        if flag.person == True and flag.talking == False and flag.question == -1:
            say("Invalid question, please ask a valid question.")
            return WatchingProcessing()

        if flag.person == True and flag.talking == False and flag.question == 0:
            say("Okay.")
            return WatchingWaiting()

        if flag.person == True and flag.talking == False and flag.question > 0:
            answerQuestion(flag.question - 1) # Subtract 1 because index 0 is the nevermind question
            return WatchingWaiting()
        
        if flag.person == False and flag.talking == False:
            return Idle()
        
        return self


class WatchingProcessing(State):
    """
    WatchingProcessing State

    - Listens to question asked by person.
    - If the person is still present go to the WatchingTalking state.
    - If the person leabes go to the Idle state.
    - Otherwise remain in this state.
    """
    def run(self): 
        flag.currentState = "WatchingProcessing()"
        flag.listening = False
        
    def event(self, event):
        
        if flag.person == True:
            flag.question = getQuestion()
            return WatchingTalking()
        
        if flag.person == False:
            return Idle()
        
        return self