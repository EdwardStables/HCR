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

    def status_command(self):
        """Send a request for all subsystem status values to mediator"""
        self.send_message("all", "get_all_status", None)
        #Requested method returns a dict of all subsystems and their current status
        msg = self.get_messages(timeout=1, ref="get_all_status_reply")

        for m in msg:
            print(m.sender_id, m.message)


    def stop_command(self, arg):
        """Send an exit signal to all subsystems."""
        if arg == '':
            self.send_message("all", "stop", None)
        else:
            ss = list(set(arg.split())) #cast to set to ensure no repeats
            if "status" in ss:
                #ensures status is the last thing to be sent stop
                ss.remove("status")
                ss.append("status")
            for s in ss:
                self.send_message(s, "stop", None)

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

class interface(Cmd):
    """Supplies a commandline interface for the program"""
    intro = "HCR Cute Robot project commandline interface :) \n"
    prompt = '> '

    def __init__(self, operator):
        self.op = operator
        self.op.status = "Executing CLI"
        super().__init__()

    def do_status(self, arg):
        """List all active subsystems and their last reported status."""
        self.op.status_command()

    def do_stop(self, arg):
        """Safely shut down all subsystems and exit"""
        self.op.stop_command(arg)

    def do_face_count(self, arg):
        """Start printing the number of faces seen in frame for arg seconds"""
        try:
            time = int(arg)
        except:
            return  
        self.op.face_count_command(time)

    def do_face_pos(self, arg):
        """Start printing the number of faces seen in frame for arg seconds"""
        try:
            time = int(arg)
        except:
            return  
        self.op.face_pos_command(time)
