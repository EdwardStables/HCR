# states.py

from .flags import Flag
from .misc import *

# Set up the flags
flag = Flag()

class State(object):
    """
    Generic state class that can run code and move into the next state.
    """
    def run(self):
        raise NotImplementedError
    def __str__(self):
        return self.state_string
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
        self.state_string = "Idle"
        flag.talking = False
        flag.processing = False
        flag.listening = False
        flag.timeout = 5
        flag.lastNonTimeOut = Idle()
        if flag.emotion[1] == 0:
            flag.emotion[0] = "content"
        elif flag.emotion[1] > 0:
            flag.emotion[1] -= 1

    def event(self, event):

        if flag.person == True:
            greetPerson()
            flag.greeting = 3 # length for greeting
            return WatchingGreeting()
        
        return self


class TimingOut(State):
    def run(self):
        self.state_string = "TimingOut"
        flag.timeout = flag.timeout - 1

    def event(self, event):
        
        if flag.timeout == 0:
            # Person didn't return after 5 cycles
            return Idle()

        if flag.person == True:
            # Refound person
            flag.timeout = 5
            return flag.lastNonTimeOut
        
        return self


class WatchingGreeting(State):
    """
    WatchingGreeting State

    - Robot watches person.
    - The robot welcomes them and moves into the WatchingWaiting state.
    - If the person leaves then return to Idle state.
    - Otherwise remain in this state.
    """
    def run(self): 
        self.state_string = "WatchingGreeting"
        flag.talking = True
        flag.listen = False
        flag.lastNonTimeOut = WatchingGreeting()
        if flag.emotion[1] == 0:
            flag.emotion[0] = "happy"
        elif flag.emotion[1] > 0:
            flag.emotion[1] -= 1
        flag.greeting -= 1

    def event(self, event):
        
        if flag.person == True and flag.greeting == 0:
            return WatchingWaiting()
        
        elif flag.person == False:
            return TimingOut()
        
        return self


class WatchingWaiting(State):
    """
    WatchingWaiting State

    - If the processing flag is set then move to WatchingProcessing state.
    - If the person leaves then return to Idle state.
    - Otherwise remain in this state.   
    """
    def run(self): 
        self.state_string = "WatchingWaiting"
        flag.listening = False
        flag.talking = False
        flag.lastNonTimeOut = WatchingWaiting()
        if flag.emotion[1] == 0:
            flag.emotion[0] = "content"
        elif flag.emotion[1] > 0:
            flag.emotion[1] -= 1

    def event(self, event):
        
        if flag.person == True and flag.question != -1:
            flag.processing == True
            flag.emotion = makeQuestion(flag.emotion[0])
            return WatchingAskingQuestion()
        
        if flag.person == False:
            return TimingOut()
        
        return self


class WatchingAskingQuestion(State):
    """
    WatchingAskingQuestion State

    - Presents a question to be answered by the person
    - If person answers question go back to watching waiting
    - If the person leaves go to the timeout state.
    - Otherwise remain in this state.
    """
    def run(self): 
        self.state_string = "WatchingAskingQuestion"
        flag.listening = True
        flag.lastNonTimeOut = WatchingAskingQuestion()
        if flag.emotion[1] == 0:
            flag.emotion[0] = "thinking"
        elif flag.emotion[1] > 0:
            flag.emotion[1] -= 1
        
    def event(self, event):
        
        if flag.person == True and flag.processing == False:
            flag.question == -1
            return WatchingWaiting()
        
        if flag.person == False:
            return TimingOut()
        
        return self