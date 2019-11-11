from multiprocessing import Pipe, Process
from collections import deque
import sys
from time import sleep


class messagebody:
    """A template message format that can be used for simpler communication between processes."""

    def __init__(self, target_id, sender_id, message, ref):
        self.target_id = target_id
        self.sender_id = sender_id
        self.message = message
        self.ref = ref 

class mediator:
    """Handler for passing messages between multiple processes via pipes."""

    def __init__(self, processes):
        self.processes = processes
        self.greedy = [p for p, v in self.processes.items() if v['policy'] == 'greedy']
        self.pipes = [p['pipe'] for _, p in self.processes.items()]
        self.messageQueue = deque()
        self.status = "Starting"

    def start(self):
        i = 0
        self.status = "Looping"
        while True:
            i += 1
            self.add_messages()
            #self.send_greedy()
            self.send_messages() 

    def add_messages(self):
        for p in self.pipes:
            if p.poll():
                self.messageQueue.append(p.recv())

    def send_greedy(self):
        for greedy_process in self.greedy:
            pipe = self.processes[greedy_process]['pipe']
            for m in self.messageQueue:
                pipe.send(m)

    def send_messages(self):
        while len(self.messageQueue) > 0:
            message = self.messageQueue.pop()
            self.handle_message(message)

    def handle_message(self, message):
        target = message.target_id

        if target == "mediator":
            self.handle_self_message(message)

        elif target == "all":
            for p, v in self.processes.items():
                v["pipe"].send(message)
            self.handle_self_message(message)

        elif target in self.processes:
            self.processes[target]["pipe"].send(message)

        elif "status" in self.processes:
            address_error = messagebody(
                target_id = "status",
                sender_id = "mediator",
                ref = "error",
                message = '{} send a message to unknown id: "{}"'.format(
                    message.sender_id, 
                    message.target_id
                    ),
            )
            self.messageQueue.append(address_error)

    def handle_self_message(self, message: messagebody):
        ref = message.ref

        if ref == "get_all_status":
            reply = messagebody("status", "mediator", self.status, ref="get_all_status_reply")            
            self.messageQueue.append(reply)
        #elif ref == "stop":
        #    self.kill_all()

    #def kill_all(self):
    #    """Sends a message to call the stop function for each subprocess,
    #    once the function returns it is assumed it is safe to kill.
    #    """
    #    print("Trying to end...")
    #    m = messagebody(None, "mediator", None, "stop")
    #    for p, v in self.processes.items():
    #        print("Killing {}...".format(p))
    #        v["pipe"].send(m)
    #        sleep(1)
    #        v["process"].terminate()
    #        v["process"].join()
    #        print("Killed {}.".format(p))
    #    print("All processes joined")
    #    sys.exit()   

        