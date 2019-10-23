import sys
import multiprocessing as mp

from hcrutils.subsystem import subsystem
from hcrutils.message import messagebody
from hcrutils.message import mediator

#Import each subsystem that needs to be launched
from status_subsystem.status import status

def main(args):

    #Define each subsystem
    subsystems = [
        status_process = status(),
    ]
    
    #Only launch if all are of the correct type
    for ss in subsystems:
        assert isinstance(ss, subsystem)

    pipes = {} 
    subprocesses = {}

    for ss in subsystems:
        p, s, i = ss.start() 
        pipes[i] = p 
        subprocesses[i] = s 

    mediator = mediator(pipes, subprocesses)
    mediator.start()

    for ss in subsystems:
        ss.close()

    sys.exit()


if __name__ == "__main__":
    args = arg_parser(sys.argv[1:])
    main(args)