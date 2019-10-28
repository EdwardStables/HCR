from hcrutils.subsystem import subsystem
from hcrutils.message import messagebody
from stateMachine import StateMachine
from flags import Flag
from time import sleep, time

class ai(subsystem):
    """Main statemachine ai process"""

    def __init__(self, default_state_subs, loop_time=0.5):
        self.default_state_subs = default_state_subs
        self.loop_time = loop_time
        super().__init__()

    def _run(self):
        self.robot = StateMachine()
        t1 = time()
        self.status = "Looping"
        self.last_state = "Idle()"
        while True:
            slp = self.loop_time - (time() - t1)
            if slp > 0:
                sleep(slp)
            t1 = time()
            self.update_flags()
            self.robot.event()
            new_state = self.robot.state
            if self.last_state != new_state:
                self.last_state = new_state
                self.send_state_update(new_state)

    def update_flags(self):
        #Receive most recent number of faces in frame
        num_faces = self.get_messages(ref="num_faces")[-1]
        self.robot.flags.person = bool(num_faces)

        #Add processing for the rest of the flags here...

    def send_state_update(self, state):
        for s in self.default_state_subs:
            self.send_message(s, "ai_state_update", state)
       