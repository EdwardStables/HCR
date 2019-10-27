# flags.py

class Flag(object):
    """
    Class containing flags that are used for moving around the state machine as well as a function for printing them.
    """
    
    def __init__(self):
        self.currentState = "Initial State"
        self.person = False
        self.listening = False
        self.processing = False
        self.talking = True
        self.name = "unknown"
        self.question = "invalid question"
    
    def printFlags(self):
        print("current state:", self.currentState,
            "\nperson:", self.person, 
            "\nlistening:", self.listening, 
            "\nprocessing:", self.processing,
            "\ntalking:", self.talking, 
            "\nname:", self.name, 
            "\nquestion:", self.question,
            "\n\n#################\n" )

