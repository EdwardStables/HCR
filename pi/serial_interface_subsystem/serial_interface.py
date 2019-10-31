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
        self.serial = serial.SerialBase()
        sleep(1)
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
        if len(movement) > 0:
            #Send the most recent instruction only
            movement = movement[-1]
        
        msg = {}
        if movement[0] == "reset":
            msg = self.get_reset()
        elif movement[0] == "position":
            msg = self.get_position(movement)
        elif movement[0] == "track":
            msg = self.get_track(movement)
        elif movement[0] == "dance":
            msg = self.get_dance(movement)
        
    def get_reset(self):
        return {"instr":0}

    def get_track(self, movement):
        return {
            "instr":3,
            "offset": [movement[1], movement[2]],
            }

    def get_track(self, movement):
        return {
            "instr":2,
            "offset": [movement[1], movement[2]],
            }

    def get_dance(self, movement):
        return {"instr":1}


