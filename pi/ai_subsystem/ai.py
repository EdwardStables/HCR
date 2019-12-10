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
        self.last_movement = "reset"
        self.current_movement = "reset"
        self.last_colour = ""
        self.current_colour = ""
        super().__init__("ai", "id_only")


    def _run(self):
        self.robot = StateMachine()
        t1 = time()
        self.status = "Idle()"
        self.last_state = "Idle()"
        while True:
            slp = self.loop_time - (time() - t1)
            if slp > 0:
                sleep(slp)
            t1 = time()
            self.check_messages()
            self.robot.event()
            new_state = self.robot.state
            if self.last_state != new_state:
                #print("state update:", new_state)
                self.last_state = new_state
                self.send_state_update(new_state)

    def check_messages(self):
        #Receive most recent number of faces in frame.
        num_faces = self.get_messages(ref="num_faces")
        num_faces = num_faces[0] if len(num_faces) else []

        if num_faces and self.last_face_number != num_faces.message:
            self.last_face_number = num_faces.message
        # Set flags.person
        self.robot.flags.person = bool(num_faces)

        # Recieve emotion data
        emotion = self.get_messages(ref="speech_emotion")
        emotion = emotion[0] if len(emotion) else []

        if emotion and emotion != self.last_emotion_read:
            self.last_emotion_read = emotion.message
        # Set flags.emotion
        self.robot.flags.emotion = emotion.message

        # Recieve question answers
        answer = self.get_messages(ref="question_answer")
        answer = answer[0] if len(answer) else []

        # Log question and answer
        if self.robot.flags.processing == True:
            log = "%i, %i, %i" % (datetime.now(), self.robot.flags.question, answer)
            try:
                f = open("log.csv", 'w')
                f.write(log)
            finally:
                f.close()
            # Tell ai subsystem that processing is done so it will go back to WatchingWaiting()
            self.robot.flags.processing = False

        
        
        #Add processing for the rest of the flags here...

        #Handle remaining messages
        messages = self.get_messages()
        #Subscriber updates
        for m in messages:
            if m.ref == "state_update_subscribe":
                self.state_subs.append(m.sender_id)
            if m.ref == "state_update_unsubscribe" and m.sender_id in self.state_subs:
                self.state_subs.remove(m.sender_id)

    def send_state_update(self, state):
        self.status = state
        for s in self.state_subs:
            self.send_message(s, "ai_state_update", state)
       