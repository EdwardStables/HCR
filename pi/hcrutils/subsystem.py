import multiprocessing as mp 

class subsystem:
    """Contains all methods for setting up and communicating with any subsystem.

    All subsystems should contain this class and use its run() method for launching code,
    as well as its signal methods for communicating with the rest of the program.
    """

    def __init__(self, ID, policy):
        """Set subsystem information.

        ID: the identifier of this subsystem used for status and communication

        policy: the policy for recieving information. 'greedy' subsystems will accept
        information from all available sources. 'id_only' subsystems will accept data
        only addressed to them. 
        """
        self.ID = ID
        if policy not in ('greedy', 'id_only'):
            raise ValueError("Policy must be either 'greedy' or 'id_only'.")
        self.policy = policy
        self.pipe = None
        self.status = "Starting"
        self.messages

    def get_status(self):
        return "{} {}".format(self.ID, self.status)

    def pipe_reciever(self, ref):
        """Manages retrieving data from the queue. If the message with the desired response is not
        already stored in self.messages, the pipe will be polled for up to a second to find the message.
        Extra messages will be stored in self.messages"""
        while poll(1) or ref not in messages::
            msg = self.pipe.recv()
            self.messages[msg.ref] = msg

        return messages.pop(ref)

    def _run(self, **kwargs):
        """Launch all subsystem functionality from this function.
        
        Must be implemented on a per-subsystem basis as all are different.
        """
        raise NotImplementedError

    def start(self, **kwargs):
        """Sets up multiprocessing interface and returns subsystem's pipe.

        Passes all kwargs to _run().

        Should not be overridden unless you know what you're doing. 

        returns the process's input pipe, and the process object itself.  
        """
        pipe_a, pipe_b = mp.Pipe() 
        self.pipe = pipe_a
        p = mp.Process(target=_run, kwargs=kwargs)
        p.start()
        self.status = "Started"
        return pipe_b, p, self.ID

    def close(self):
        assert False