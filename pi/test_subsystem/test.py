from hcrutils.subsystem import subsystem
from hcrutils.message import messagebody

from time import time

class test(subsystem):
    """A minimal subsystem to test messaging.

    Allows for ID and policy to be set when initialised.
    """

    def __init__(self, ID, policy):
        super().__init__(ID, policy)
       

    def _run(self, **kwargs):
        cp = consumer_producer(self, 1)
        cp.start()

class consumer_producer:

    def __init__(self, subsystem, period=1):
        self.period = period 
        self.ID = subsystem.ID
        self.pipe = subsystem.pipe

    def start(self):
        t = time()
        while True:
            while self.pipe.poll():
                m: messagebody = self.pipe.recv()
                print("{} recieved {} from {}".format(
                        self.ID,
                        m.message,
                        m.sender_id
                    ))

            if time() - t > self.period:
                message = messagebody(
                    target_id = 'test' + ('1' if '2' in self.ID else '2'),
                    sender_id = self.ID,
                    message = "Hi from {}".format(self.ID)
                )

                print("{} sent message to {}".format(
                        self.ID,
                        message.target_id
                    ))
                self.pipe.send(message)  
                t = time()
