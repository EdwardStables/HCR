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
        flag.name = "unknown"
        flag.timeout = 5
        flag.lastNonTimeOut = Idle()
        
    def event(self, event):
        
        if flag.person == True:
            return WatchingGreeting()
        
        return self


class TimingOut(State):
    def run(self):
        self.state_string = "TimingOut"
        flag.timeout = flag.timeout - 1
    def event(self, event):
        
        if flag.timeout == 0:
            return Idle()

        if flag.person == True:
            flag.timeout = 5
            return flag.lastNonTimeOut
        
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
        
    def event(self, event):
        
        if flag.person == True and flag.name != "unknown":
            #say(("Hello " + flag.name))
            return WatchingWaiting()
        
        elif flag.person == True and flag.name == "unknown":
            #say("I don't know you, what is your name?")
            return WatchingGetName()
        
        elif flag.person == False:
            return TimingOut()
        return self


class WatchingGetName(State):
    """
    WatchingGetName State

    - If the name is updated from unknown then move to WatchingGreeting state.
    - If the person leaves then return to Idle state.
    - Otherwise remain in this state.
    """
    def run(self): 
        self.state_string = "Idle"
        flag.talking = False
        flag.listening = True
        flag.lastNonTimeOut = WatchingGetName()
        
    def event(self, event):
        
        if flag.person == True: # and flag.name != "unknown":
            flag.name = "getName()"
            return WatchingGreeting()
        
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
        flag.processing = False
        flag.listening = True
        flag.talking = False
        flag.lastNonTimeOut = WatchingWaiting()
        
    def event(self, event):
        
        if flag.person == True and flag.processing == True:
            #say("What is your question?")
            return WatchingProcessing()
        
        if flag.person == False:
            return TimingOut()
        
        return self


class WatchingTalking(State):
    """
    WatchingTalking State

    - If the person is still present and the robot isn't talking go to the WatchingWaiting state.
    - If the person is leaves and the robot isn't talking go to the Idle state.
    - Otherwise remain in this state.   
    """
    def run(self): 
        self.state_string = "WatchingTalking"
        flag.lastNonTimeOut = WatchingTalking()
        
    def event(self, event):        
        
        if flag.person == True and flag.talking == False and flag.question == -1:
            #say("Invalid question, please ask a valid question.")
            return WatchingProcessing()

        if flag.person == True and flag.talking == False and flag.question == 0:
            #say("Okay.")
            return WatchingWaiting()

        if flag.person == True and flag.talking == False and flag.question > 0:
            # answerQuestion(flag.question - 1) # Subtract 1 because index 0 is the nevermind question
            return WatchingWaiting()
        
        if flag.person == False and flag.talking == False:
            return TimingOut()
        
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
        self.state_string = "WatchingProcessing"
        flag.listening = False
        flag.lastNonTimeOut = WatchingProcessing()
        
    def event(self, event):
        
        if flag.person == True:
            #flag.question = getQuestion()
            return WatchingTalking()
        
        if flag.person == False:
            return TimingOut()
        
        return self