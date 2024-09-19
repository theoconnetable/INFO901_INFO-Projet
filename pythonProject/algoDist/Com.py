import threading
from ClassesUsed import AbstractMessage
from algoDist.ClassesUsed import Mailbox
from pyeventbus3.pyeventbus3 import *


class Com:

    nb_process_created = 0

    def __init__(self, np_process):

        ## Definition nombre de processus
        self.np_process = np_process
        self.myId = Com.nb_process_created
        Com.nb_process_created += 1

        # Horloge de Lamport et Sémaphore pour protéger son accès
        self.lamport_clock = 0
        self.semaphore = threading.Semaphore()
        self.mailbox = Mailbox()

    def inc_clock(self):
        """Incrémente l'horloge de Lamport."""
        with self.semaphore:  # Accès protégé par un sémaphore
            self.lamport_clock += 1
            print(f"Horloge incrémentée : {self.lamport_clock}")

    def broadcast(self, o):
        for i in range(0,Com.nb_process_created):
            if i != self.myId:
                self.inc_clock()
                message = AbstractMessage(o, self.lamport_clock,self.myId,i)
                PyBus.Instance().post(message)

    def send_to(self,o,dest):
        self.inc_clock()
        message = AbstractMessage(o, self.lamport_clock,self.myId,dest)
        PyBus.Instance().post(message)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=AbstractMessage)
    def receive(self, o):
        message_received = o


