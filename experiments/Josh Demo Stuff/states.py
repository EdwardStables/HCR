# states.py
from flags import Flag
import time

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
    - If the person is known, then the robot welcomes them and moves into the WatchingWaiting state.
    - If the person is unknown, tell them they are unknown and move into the WatchingGetName state.
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
        flag.processing = False
        flag.listening = True
        flag.talking = False
        flag.lastNonTimeOut = WatchingWaiting()
        print("Robot emotion: Content. \nSend LIGHT GREEN colour information. \nSend CONTENT eyes to screen. \nSend WATCHING movement information")
        
    def event(self, event):
        
        if flag.person == True and flag.processing == True:
            print("**Person finishes asking question**")
            return WatchingProcessing()
        
        if flag.person == False:
            print("**Lost person**")
            return TimingOut()
        
        # nothing has happened
        return self

class ValidQuestion(State):
    
    def run(self): 
        self.state_string = "ValidQuestion"
        flag.lastNonTimeOut = ValidQuestion()
        print("Robot emotion: Happy. \nSend YELLOW colour information. \nSend HAPPY eyes to screen. \nSend WATCHING movement information")
        print("Call function to answer question, after this is run talking flag == 0.")
        flag.talking = False # remove in final code

    def event(self, event):

        if flag.person == True and flag.talking == False:
            return WatchingWaiting()
        
        if flag.person == False:
            print("**Lost person**")
            return TimingOut()
        
        # still talking
        return self

class InvalidQuestion(State):
   
    def run(self): 
        self.state_string = "InvalidQuestion"
        flag.lastNonTimeOut = InvalidQuestion()
        print("Robot emotion: Sad. \nSend BLUE colour information. \nSend SAD eyes to screen. \nSend WATCHING movement information")
        print("Call function to say question was invalid, after this is run talking flag == 0.")
        flag.talking = False # remove in final code

    def event(self, event):

        if flag.person == True and flag.talking == False:
            return WatchingWaiting()
        
        if flag.person == False:
            print("**Lost person**")
            return TimingOut()
        
        # still talking
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
        print("Robot emotion: Thinking. \nSend GREY colour information. \nSend THOUGHTFUL eyes to screen. \nSend WATCHING movement information")
        self.state_string = "WatchingProcessing"
        flag.listening = False
        flag.lastNonTimeOut = WatchingProcessing()
        
    def event(self, event):
        
        if flag.person == True and flag.processing == False and flag.question > 0:
            print("**Question processed, it was valid**")
            return ValidQuestion()

        if flag.person == True and flag.processing == False and flag.question == -1:
            print("**Question processed, it was invalid**")
            return InvalidQuestion()
        
        if flag.person == True and flag.talking == False and flag.question == 0:
            print("**User has canceled question**")
            print("Call function to cancel the question and set flags.")
            return WatchingWaiting()
        
        if flag.person == False:
            print("**Lost person**")
            return TimingOut()
        
        return self