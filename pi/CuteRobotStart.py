import sys
import os
import multiprocessing as mp

from hcrutils.subsystem import subsystem
from hcrutils.message import messagebody
from hcrutils.message import mediator

#Import each subsystem that needs to be launched
# from serial_interface_subsystem.serial_interface import serial_interface
from status_subsystem.status import status
from face_recog_subsystem.face_recog import face_recog
from ai_subsystem.ai import ai
from screen_subsystem.screen import screen

def main():
    ROOT = os.getcwd()

    #Define each subsystem
    subsystems = [
        status(),
        #face_recog(ROOT, 0, num_sub=["ai"], rel_sub=["screen"]),
        ai(),
        #screen(ROOT),
        #serial_interface()
    ]

    print("Subsystems instantiated.")
    
    #Only launch if all are of the correct type
    for ss in subsystems:
        assert isinstance(ss, subsystem)

    processes = {}

    for ss in subsystems:
        p, s, i = ss.start() 
        processes[i] = {
            "pipe" : p,
            "process" : s,
            "policy" : ss.policy,
        }

    print("Subsystems started.")

    process_mediator = mediator(processes)
    process_mediator.start()

    for ss in subsystems:
        ss.close()

    sys.exit()


if __name__ == "__main__":
    main()
