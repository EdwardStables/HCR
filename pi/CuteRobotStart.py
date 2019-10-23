import sys
import multiprocessing as mp

from hcrutils.subsystem import subsystem
from hcrutils.message import messagebody
from hcrutils.message import mediator

#Import each subsystem that needs to be launched
from status_subsystem.status import status

def main():
    #Define each subsystem
    subsystems = [
        status(),
    ]
    
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

    process_mediator = mediator(processes)
    process_mediator.start()

    for ss in subsystems:
        ss.close()

    sys.exit()


if __name__ == "__main__":
    main()