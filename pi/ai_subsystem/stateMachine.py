# stateMachine.py

from .states import *
from .flags import Flag

class StateMachine(object):
    """ 
    A simple state machine.
    """

    def __init__(self):
        """ Initialize the components."""
        self.state = Idle()
        self.state.run()
        self.flags = flag

    def event(self, event=""):
        """
        Incoming events are delegated to the given states which then handle the event. 
        The result is then assigned as the new state.
        """
        #print(event, '\n')

        # The next state will be the result of the on_event function.
        self.state = self.state.event(event)
        self.state.run()
    