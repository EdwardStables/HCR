# states.py
from .flags import Flag

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
        print("Robot emotion: Idling. \nSend LIGHT GREEN colour information. \nSend CONTENT eyes to screen. \nSend DANCING movement information")
        
    def event(self, event):

        if flag.person == True:
            print("**Person appears**")
            print("Call function to greet user.")
            return WatchingGreeting()
        
        # doing shit all
        return self


class TimingOut(State):
    def run(self):
        self.state_string = "TimingOut"
        flag.timeout = flag.timeout - 1
        print("DO NOT CHANGE INFORMATION SENT TO SUBSYSTEMS")
    def event(self, event):
        
        if flag.timeout == 0:
            print("**Person didn't return after 5 cycles**")
            return Idle()

        if flag.person == True:
            print("**Refound person**")
            flag.timeout = 5
            return flag.lastNonTimeOut
        
        print("**Person disappeared for", 5 - flag.timeout, "cycles**")
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
        print("Robot emotion: Happy. \nSend YELLOW colour information. \nSend HAPPY eyes to screen. \nSend WATCHING movement information")
        
    def event(self, event):
        
        if flag.person == True:
            print("**Robot greets person**")
            return WatchingWaiting()
        
        elif flag.person == False:
            print("**Lost person**")
            return TimingOut()
        
        # still greeting
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
        print("Robot emotion: Content. \nSend LIGHT GREEN colour information. \nSend CONTENT eyes to screen. \nSend WATCHING movement information")
        
    def event(self, event):
        
        if flag.person == True and flag.question != -1:
            flag.processing == True
            print("**call function that displays question and sets processing flag to False after question answered**")
            return WatchingAskingQuestion()
        
        if flag.person == False:
            print("**Lost person**")
            return TimingOut()
        
        # nothing has happened
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
        
    def event(self, event):
        
        if flag.person == True and flag.processing == False:
            flag.question == -1
            return WatchingWaiting()
        
        if flag.person == False:
            return TimingOut()
        
        return self