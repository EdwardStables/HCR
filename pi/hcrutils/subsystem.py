from .message import messagebody

import multiprocessing as mp 
import threading as th
from collections import defaultdict
from time import sleep, time

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
        self.messages = defaultdict(list)
        self.message_lock = mp.Lock()
        self.pipe_lock = mp.Lock()

    def message_receiver(self):
        """Threaded function to handle all received messages. 

        Stores specific messages in self.messages.
        Executes general messages (stop, status, etc.)
        """
        while True:
            sleep(0.1) #only run every few seconds.
            with self.message_lock, self.pipe_lock: #Lock while writing 
                while self.pipe.poll(): #while there are messages in the pipe
                    msg = self.pipe.recv()
                    self.messages[msg.ref].append(msg)

            remove_ref = []
            #Checking for components inside should be threadsafe
            if 'stop' in self.messages:
                remove_ref.append('stop')
                self.stop()
            if 'get_all_status' in self.messages:
                remove_ref.append('get_all_status')
                self.send_message('status', 'get_all_status_reply', self.status)
            #Add further global functions here.
            """
            if 'ref' in self.messages:
                remove_ref.append('ref')
                do thing...
            """

            with self.message_lock:
                for r in remove_ref:
                    self.messages.pop(r)

    def get_messages(self, ref = None, timeout = 0):
        """Returns messages from self.messages that match the passed reference,
        or (if no reference given), all messages.

        Passed messages are removed from self.messages.
    
        Returns an empty list if nothing is in place, takes an optional timeout to wait.
        """
        sleep(timeout)
        with self.message_lock:
            if ref == None:
                ret = []
                for _, v in self.messages.items():
                    ret += v
                self.messages = defaultdict(list)
            else:
                ret = self.messages[ref]
                self.messages.pop(ref)
        
        return ret

    def send_message(self, target, ref, message):
        msg = messagebody(target_id = target, sender_id = self.ID, ref = ref, message = message)
        with self.pipe_lock:
            self.pipe.send(msg)

    def _run(self):
        """Launch all subsystem functionality from this function.
        
        Must be implemented on a per-subsystem basis as all are different.
        """
        raise NotImplementedError

    def setup_threading(self, **kwargs):
        """Itermediate step for subprocess, required to properly fork threading"""
        self.receiver_thread = th.Thread(target=self.message_receiver, args=())
        self.receiver_thread.daemon = True
        self.receiver_thread.start()

        self._run()

    def start(self):
        """Sets up multiprocessing interface and returns subsystem's pipe.

        Passes all kwargs to _run().

        Should not be overridden unless you know what you're doing. 

        returns the process's input pipe, and the process object itself.  
        """
        pipe_a, pipe_b = mp.Pipe() 
        self.pipe = pipe_a
        p = mp.Process(target=self.setup_threading)
        p.start()
        self.status = "Started"
        return pipe_b, p, self.ID

    def stop(self):
        print("Stop:", self.ID)
