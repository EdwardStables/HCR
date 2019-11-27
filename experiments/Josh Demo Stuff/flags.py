# flags.py

class Flag(object):
    """
    Class containing flags that are used for moving around the state machine as well as a function for printing them.
    """
    
    def __init__(self):
        self.currentState = "Idle()"
        self.person = False
        self.listening = False
        self.processing = False
        self.talking = True
        self.question = -1
        self.timeout = 5
    
    def printFlags(self):
        print("\nperson:", self.person, 
            "\nlistening:", self.listening, 
            "\nprocessing:", self.processing,
            "\ntalking:", self.talking, 
            "\nquestion:", self.question, "(-1: invalid question, 0: cancel question, 1+: all other questions)",
            )

