from hcrutils.subsystem import subsystem
from hcrutils.message import messagebody
from cmd import Cmd
import sys

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
        operator_class = operator(self)
        interface(operator_class).cmdloop()         

class interface(Cmd):
    """Supplies a commandline interface for the program"""
    intro = "HCR Cute Robot project commandline interface :) \n"
    prompt = '> '

    def __init__(self, operator):
        self.op = operator
        self.op.set_status("Executing CLI")
        super().__init__()

    def do_status(self, arg):
        """List all active subsystems and their last reported status."""
        self.op.print_status()

    def do_stop(self, arg):
        """Safely shut down all subsystems and exit"""
        self.op.stop(arg)
        
    
class operator:
    """Performs the operations specified by the interface, should be passed a subsystem inherited object"""
    def __init__(self, subsystem: status):
        self.subsystem = subsystem
        self.ID = self.subsystem.ID
        self.pipe = self.subsystem.pipe
        self.set_status = self.subsystem.set_status
        self.messages = {}

    def print_status(self):
        """Send a request for all subsystem status values to mediator"""
        self.subsystem.send_message("all", "get_all_status", None)
        #Requested method returns a dict of all subsystems and their current status
        msg = self.subsystem.get_messages(timeout=1, ref="get_all_status_reply")

        print(msg)

    def stop(self, arg):
        """Send an exit signal to all subsystems."""
        if arg == '':
            self.subsystem.send_message("all", "stop", None)
        else:
            ss = list(set(arg.split())) #cast to set to ensure no repeats
            if "status" in ss:
                #ensures status is the last thing to be sent stop
                ss.remove("status")
                ss.append("status")
            for s in ss:
                self.subsystem.send_message(s, "stop", None)
