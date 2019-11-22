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

    def _run(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600, write_timeout = 1.0) # Establish the connection on a specific port#
        while True:
            self.send_loop()

    def send_loop(self):
        """Parses and sends movement instructions from other areas of the
        program

        All movements are expected to be in the form of a tuple, where the 
        first element is the instruction type and all other entries are helper
        data.
        """
        #movement = self.get_messages("movement")
        #if len(movement) == 0:
        #    return
        #else:
        #    movement = movement[-1]
        #
        #msg = {}
        #if movement.message == "reset":
        #    msg = self.get_reset()
        #elif movement.message == "move":
        #    msg = self.get_moves(movement)
        #elif movement.message == "track":
        #    msg = self.get_offset(movement)
        #elif movement.message == "colour":
        #    msg = self.get_colour(movement)

        msg = {
            "instr":1,
            "pattern":0
        }
        print(msg)
        ser_msg = json.dumps(msg).encode()
        self.ser.write(ser_msg)

        msg = {
            "instr":1,
            "pattern":0
        }
        print(msg)
        ser_msg = json.dumps(msg).encode()
        self.ser.write(ser_msg)

        print("func end")


    def get_moves(self, movement):
        return {
            "instr":1,
            "moves": [movement[1], movement[2]]
            }

    def get_offset(self, movement):
        return {
            "instr":2,
            "offset": [movement[1], movement[2]]
            }

    def get_colour(self, movement):
        return {
            "instr":3,
            "colour": movement[1]
        }

    def get_reset(self):
        return {"instr":0}


