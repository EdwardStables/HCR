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
        'List all active subsystems and their last reported status.'
        self.op.print_status()

    def do_EOF(self, arg):
        input()
        #print("EOF:", arg)
    
class operator:
    """Performs the operations specified by the interface, should be passed a subsystem inherited object"""
    def __init__(self, subsystem: status):
        self.subsystem = subsystem
        self.ID = self.subsystem.ID
        self.pipe = self.subsystem.pipe
        self.reciever = self.subsystem.pipe_reciever
        self.messages = {}

    def set_status(self, status):
        self.subsystem.status = status

    def print_status(self):
        get_status_msg = messagebody("mediator", self.ID, None, "get_all_status")
        self.pipe.send(get_status_msg)

        #Requested method returns a dict of all subsystems and their current status
        msg = self.reciever("get_all_status").message

        print(msg)




