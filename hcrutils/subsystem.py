import multiprocessing as mp


class subsystem:
    """Contains all methods for setting up and communicating with any subsystem.

    All subsystems should contain this class and use its run() method for launching code,
    as well as its signal methods for communicating with the rest of the program.

    The only methods that should be called externally are '_start()' and '_SIGNAL_METHOD_'
    to preserve the multiprocessing interface.
    """

    def __init__(self, ID):
        self.ID = ID

    def _run(self, **kwargs):
        """Launch all subsystem functionality from this function.
        
        Must be implemented on a per-subsystem basis as all are different.
        """
        raise NotImplementedError

    def start(self, **kwargs):
        """Sets up multiprocessing interface and returns subsystem's pipe.

        Passes all kwargs to _run().

        Should not be overridden unless you know what you're doing. 
        """
        q = mp.Queue() 
        kwargs['queue'] = q
        p = mp.Process(target=_run, kwargs=kwargs)
        p.start()
        return q