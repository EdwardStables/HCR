from hcrutils.subsystem import subsystem
from hcrutils.message import messagebody
from .stateMachine import StateMachine
from .flags import Flag
from time import sleep, time
from datetime import datetime
from collections import deque

class ai(subsystem):
    """Main statemachine ai process"""

    def __init__(self, default_state_subs=[], loop_time=0.5):
        self.state_subs = default_state_subs
        self.loop_time = loop_time
        self.last_face_number = 0
        self.last_emotion_read = ""
        self.movement = ("", "")
        self.colour = ("", "blue")
        self.eyes = ("", "wide_open")
        self.greeting = False
        self.greetingLength = 0
        self.questionAnswered = True
        self.question = [0]
        super().__init__("ai", "id_only")

    def _run(self):
        self.robot = StateMachine()
        self.greetingLength = self.robot.flags.greetingLength
        t1 = time()
        self.status = "Idle()"
        self.last_state = "Idle()"
        i = 0
        while True:
            print(i)
            i+=1
            slp = self.loop_time - (time() - t1)
            if slp > 0:
                sleep(slp)
            t1 = time()


            # Get messages from other subsystems, do logic, then send messages to subsystems
            emotion, num_faces, answer, answered = self.check_messages()
            colour_data, eye_data, movement_data = self.create_message_data(emotion, num_faces, answer, answered)
            self.send_messages(colour_data, eye_data, movement_data)

            self.robot.event()
            new_state = self.robot.state
            if self.last_state != new_state:
                #print("state update:", new_state)
                self.last_state = new_state
                self.send_state_update(new_state)

            #self.robot.flags.printFlags()
            
    
    def check_messages(self):
        """
        Check for messages from other subsystems for ai
        """
        # Receive Emotion data
        emotion = self.get_messages(ref="speech_emotion")
        emotion = emotion[0] if len(emotion) else []

        # Receive Question Answers data
        answer = self.get_messages(ref="question_answer")
        answer = answer[0] if len(answer) else []

        # get whether question has been answered (bool)
        answered = self.get_messages(ref="question_answered")
        answered = answered[0] if len(answered) else []


        # Receive Number of faces data
        num_faces = self.get_messages(ref="num_faces")
        num_faces = num_faces[0] if len(num_faces) else []

        #Handle remaining messages
        messages = self.get_messages()

        #Subscriber updates
        for m in messages:
            if m.ref == "state_update_subscribe":
                self.state_subs.append(m.sender_id)
            if m.ref == "state_update_unsubscribe" and m.sender_id in self.state_subs:
                self.state_subs.remove(m.sender_id)

        return emotion, num_faces, answer, answered

    def create_message_data(self, emotion, num_faces, answer, answered):
        """
        Based on message information, work out what information needs to be sent to the other subsystems
        """
        # Initialise
        colour_data, eye_data, movement_data = [], [], []
        
        # Set internal last_eomtion_read
        if emotion and emotion != self.last_emotion_read:
            self.last_emotion_read = emotion.message
            # Set flags.emotion
            self.robot.flags.emotion = emotion.message

        # Set flags.person
        #self.robot.flags.person = bool(num_faces)
        if num_faces == []:
            self.robot.flags.person = False
        else:
            self.robot.flags.person = num_faces.message

        print(self.robot.flags.person)
        # Set internal last_face_number
        if num_faces and self.last_face_number != num_faces.message:
            self.last_face_number = num_faces.message

        # Log question and answer in csv file
        # If answered exists then the answer must have also been sent so we don't check for it's existence
        if answer: #and self.robot.flags.processing[0] == True: #and answered.message == True:
            self.robot.flags.stateLock = False
            self.questionAnswered = True
            log = "%s, %i, %i\n" % (datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), answer.message, self.robot.flags.interactivity)
            print("Log:", log)
            with open("question_log.csv", 'a+') as f:
                f.write(log)
                f.close()
            # Tell ai subsystem that processing is done so it will go back to WatchingWaiting()
            self.robot.flags.processing = [False, False, -1]
            # Make robot sad for 5 cycles if results bad
            if answer.message < 3:
                self.robot.flags.emotion = ("sad", 8)
            else:
                self.robot.flags.emotion = ("happy", 8)
        print(self.robot.flags.currentState)

        # prepare movement information
        if self.robot.flags.currentState == "Idle":
            movement_data = ["idle"] # 0 means idling
            self.movement = (self.movement[1], "idle")
        elif self.robot.flags.currentState == "WatchingWaiting":
            movement_data = ["set_following"] # 1 means following
            self.movement = (self.movement[1], "following")
        elif self.robot.flags.currentState == "WatchingGreeting":
            movement_data = ["set_following"]
            self.movement = (self.movement[1], "following")
        elif self.robot.flags.currentState == "WatchingAskingQuestion":
            movement_data = ["set_following"]
            self.movement = (self.movement[1], "following")
        elif self.robot.flags.currentState == "Timeout":
            movement_data = ["set_following"]
            self.movement = (self.movement[1], "following")

        # Prepare colour and eye information
        if self.robot.flags.emotion[0] == "happy":
            colour_data = ["colour", 0] # 0-3
            eye_data = [-0.5] # 1 top maximum, -1 bottom maximum
            self.colour = (self.colour[1], "yellow")
            self.eyes = (self.eyes[1], "bottom_covered")
        elif self.robot.flags.emotion[0] == "sad":
            colour_data = ["colour", 1]
            eye_data = [0.5]
            self.colour = (self.colour[1], "orange")
            self.eyes = (self.eyes[1], "top_covered")
        elif self.robot.flags.emotion[0] == "thinking":
            colour_data = ["colour", 3]
            eye_data = [0]
            self.colour = (self.colour[1], "grey")
            self.eyes = (self.eyes[1], "look_to_corner")
        elif self.robot.flags.emotion[0] == "content":
            colour_data = ["colour", 2]
            eye_data = [0]
            self.colour = (self.colour[1], "blue")
            self.eyes = (self.eyes[1], "wide_open")
        
        # Case for no interactivity
        if self.robot.flags.interactivity == 0:
            eye_data = [0] # 0

        return colour_data, eye_data, movement_data

    def send_messages(self, colour_data, eye_data, movement_data):
        print("colour:", colour_data)
        print("eye_data:", eye_data)
        print("selfcolour", self.colour)
        print("movement:", movement_data)
        """
        Send messages to other subsystems from ai
        """
        # Send messages as required
        if self.movement[0] != self.movement[1] and self.robot.flags.interactivity == 2:
            self.send_message("serial_interface", "movement", movement_data)

        if self.colour[0] != self.colour[1] and self.robot.flags.interactivity > 0:
            self.send_message("serial_interface", "movement", colour_data)

        if self.eyes[0] != self.eyes[1] and self.robot.flags.interactivity > 0:
            self.send_message("screen", "eyes", eye_data)
        
        # Sort out Greeting
        if self.robot.flags.greeting == 0:
            self.greeting = False
        elif self.robot.flags.greeting == self.greetingLength: # If we change the greeting length also change here
            self.greeting = True
            greetingMessage = ["initialise_greeting", self.greetingLength]
            self.send_message("screen", "greeting", greetingMessage)
            self.robot.flags.emotion = "happy",  self.greetingLength
            # Only make face happy, not movement

        # Send Question
        if (self.robot.flags.sendQuestion == [True, False]):
                self.robot.flags.sendQuestion = [True, True]
                self.send_message("screen", "askquestion", [])
                
    def send_state_update(self, state):
        self.status = state
        for s in self.state_subs:
            self.send_message(s, "ai_state_update", state)
       
