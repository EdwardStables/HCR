from hcrutils.subsystem import subsystem
from hcrutils.message import messagebody
from cmd import Cmd
import sys
from time import sleep, time

class status(subsystem):
    """Provides an interface to show the current status of the code.

    Written as a subsystem as an example of setting one up.

    TODO: Basic implementation will print to stdout, later it should expose a 
    web display to show the status (and maybe control)
    """

    def __init__(self):
        super().__init__("status", "greedy")

    def _run(self):
        sys.stdin = open(0)
        interface(self).cmdloop()         

    def check_messages(self):
        """Status is a special case that doesn't check
        messages in a main loop.
        """
        pass

    def stop(self):
        print("changing stdin")
        print(sys.stdin)
        sys.stdin = sys.__stdin__
        print(sys.stdin)
        

    def status_command(self):
        """Send a request for all subsystem status values to mediator"""
        self.send_message("all", "get_all_status", None)
        #Requested method returns a dict of all subsystems and their current status
        msg = self.get_messages(timeout=1, ref="get_all_status_reply")

        for m in msg:
            print(m.sender_id, m.message)

    def face_count_command(self, wait):
        self.send_message("face_recog", "num_subscribe", None)
        end = time() + wait
        while time() < end:
            m = self.get_messages("num_faces")
            for i in m:
                print(i.message)
        self.send_message("face_recog", "num_unsubscribe", None)

    def face_pos_command(self, wait):
        self.send_message("face_recog", "pos_subscribe", None)
        end = time() + wait
        while time() < end:
            m = self.get_messages("pos_faces")
            for i in m:
                print(i.message)
        self.send_message("face_recog", "pos_unsubscribe", None)
    
    def face_rel_command(self, wait):
        self.send_message("face_recog", "rel_subscribe", None)
        end = time() + wait
        while time() < end:
            m = self.get_messages("rel_faces")
            for i in m:
                print(i.message)
        self.send_message("face_recog", "rel_unsubscribe", None)
        
    def ai_state_command(self, wait):
        self.send_message("ai", "state_update_subscribe", None)
        end = time() + wait
        while time() < end:
            m = self.get_messages("ai_state_update")
            for i in m:
                print(i.message)
        self.send_message("ai", "state_update_unsubscribe", None)


class interface(Cmd):
    """Supplies a commandline interface for the program"""
    intro = "HCR Cute Robot project commandline interface :) \n"
    prompt = '> '

    def __init__(self, operator):
        self.op = operator
        self.op.status = "Executing CLI"
        self.set_reciever = None
        self.default_prompt = '> '
        super().__init__()

    def cmdloop(self):
        super().cmdloop()

    def do_status(self, arg):
        """List all active subsystems and their last reported status."""
        self.op.status_command()

    def do_face_count(self, arg):
        """Start printing the number of faces seen in frame for arg seconds"""
        time = get_num_args(arg)
        time = time[0] if time else 5
        self.op.face_count_command(time)

    def do_face_pos(self, arg):
        """Start printing the number of faces seen in frame for arg seconds"""
        time = get_num_args(arg)
        time = int(time[0]) if time else 5
        self.op.face_pos_command(time)

    def do_face_rel(self, arg):
        """Start printing the relative position of the largest face in the frame"""
        time = get_num_args(arg)
        time = int(time[0]) if time else 5
        self.op.face_rel_command(time)

    def do_ai_state(self, arg):
        """Print the current state of the ai subsystem for arg seconds"""
        time = get_num_args(arg)
        time = int(time[0]) if time else 5
        self.op.ai_state_command(time)

    def do_message(self, arg):
        """Send a custom message to a subsystem. Number of args denotes operation:
        0: Reset the default target and clear prompt
        1: Set default target and set in prompt
        2: Send the default target message with ref arg[0] and body arg[1].
           (Raises error if used without a default being set)
        3: Send target arg[0] message with ref arg[1] and body arg[2]
        """
        args = get_num_args(arg)
        num = len(args)
        if num == 0:
            self.prompt = self.default_prompt
            self.set_reciever = None
            return
        elif num == 1:
            self.prompt = "(" + args[0] + ")>"
            self.set_reciever = [0]
            return
        elif num == 2:
            if self.set_reciever == None:
                print("Error in command: No receiver set")
                return
            self.op.send_message(self.set_reciever, args[0], args[1])
        if num == 3:
            self.op.send_message(args[0], args[1], args[2])


def get_num_args(arg):
    args = arg.split()
    vals = []
    for a in args:
        try:
            vals.append(a)
        except:
            continue
    return vals 

    

