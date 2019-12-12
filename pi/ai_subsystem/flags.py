# flags.py

class Flag(object):
    """
    Class containing flags that are used for moving around the state machine as well as a function for printing them.
    """
    
    def __init__(self):
        self.currentState = "Idle"
        self.person = False # Is there a face in view
        self.listening = False # Is the robot listening
        self.processing = [False, False, -1] # question asked, bool set for one cycle for messaging screen subsystem, question
        self.talking = True # Is the robot talking (if we had it...)
        self.question = -1 # -1 = Null question, 0+ = valid question
        self.timeout = 20 # Timeout and its length in cycles
        self.emotion = ("", 0) # Emotion and its persistence in cycles
        self.greeting = 0 
        self.interactivity = 2 # 0 = no interactivity, 1 = no movement, 2 = all interactiity
        self.greetingLength = 3 # Greet for three cycles
        self.questionAnswered = True
    
    def printFlags(self):
        print("\ntimeout:", self.timeout,
              "\ncurrentstate:", self.currentState,
	      "\nperson:", self.person, 
              "\nlistening:", self.listening, 
              "\nprocessing:", self.processing,
              "\ntalking:", self.talking, 
              "\nquestion:", self.question,
              "\ninteractivity:", self.interactivity,
              "\nemotion:", self.emotion[0], 
              "\nemotionLock:", self.emotion[1],
              "\ngreeting:", self.greeting,
              "\ngreeting length:", self.greetingLength
              )

