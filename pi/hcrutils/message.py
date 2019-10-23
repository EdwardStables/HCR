from multiprocessing import Pipe, Process
from collections import deque


class messagebody:
    """A template message format that can be used for simpler communication between processes."""

    def __init__(self, target_id, sender_id, message, ref=None):
        self.target_id = target_id
        self.sender_id = sender_id
        self.message = message
        self.ref = None

class mediator:
    """Handler for passing messages between multiple processes via pipes."""

    def __init__(self, processes):
        self.processes = subprocesses
        self.messageQueue = deque()
        self.greedy = [p for p in self.processes if p['policy'] == 'greedy']

    def start(self):
        while True:
            self.add_messages()
            self.send_greedy()
            self.send_messages() 

    def add_messages(self):
        for p in pipes:
            self.messageQueue.append(p.recv())

    def send_greedy(self):
        for p in greedy:
            pipe = p['pipe']
            for m in self.messageQueue:
                pipe.send(m)

    def send_messages(self):
        while self.messageQueue.count > 0:
            m = self.messageQueue.pop()
            target = m.target_id
            if target == 'mediator':
                handle_self_messages(m)
            elif target in self.processes:
                processes[target]['pipe'].send(m)
            elif 'status' in self.processes:
                address_error = messagebody(
                    target_id = 'status',
                    sender_id = 'mediator',
                    message = '{} send a message to unknown id: "{}"'.format(m.sender_id, m.target_id),
                )
                self.messageQueue.append(address_error)

    def handle_self_messages(self, message):
        pass