import serial
import json
from time import sleep, time
from hcrutils.subsystem import subsystem
from hcrutils.message import messagebody

class serial_interface(subsystem):
    """Supplies commands to the connected arduino for movement
    via serial.
    """

    def __init__(self):
        super().__init__("serial_interface", "id_only")
        self.last_time = time()
        self.FOLLOW = False

    def _run(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600, write_timeout = 1) # Establish the connection on a specific port#
        while True:
            self.send_loop()

    def send_loop(self):
        """Parses and sends movement instructions from other areas of the
        program

        All movements are expected to be in the form of a tuple, where the 
        first element is the instruction type and all other entries are helper
        data.
        """
        movement = self.get_messages("movement")
        if len(movement) == 0:
            return
        else:
            movement = movement[-1]

        message = movement.message[0]
        
        msg = {}
        if message == "reset":
            msg = self.get_reset()
        elif message == "set_following":
            self.FOLLOW = True
        elif message == "idle":
            self.FOLLOW = False
            msg = self.get_idle(movement)
        elif self.FOLLOW and message == "offset":
            msg = self.get_offset(movement)
        elif message == "colour":
            msg = self.get_colour(movement)


        ser_msg = json.dumps(msg).encode()
        try:
            self.ser.write(ser_msg)
        except serial.serialutil.SerialTimeoutException as e:
            print("Serial restarting")
            self.ser = serial.Serial('/dev/ttyACM0', 9600, write_timeout = 1) # Establish the connection on a specific port#

        
        #while self.ser.inWaiting():
        #    print(self.ser.readline())

    def get_idle(self, movement):
        return { "instr":2 }

    def get_offset(self, movement):
        return {
            "instr":3,
            "offset": [movement.message[1], movement.message[2]]
            }

    def get_colour(self, movement):
        return {
            "instr":4,
            "colour": movement[1]
        }

    def get_reset(self):
        return {"instr":0}


