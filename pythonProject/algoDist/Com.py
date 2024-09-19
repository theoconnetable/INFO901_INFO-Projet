import threading
from ClassesUsed import AbstractMessage
from algoDist.ClassesUsed import Mailbox
from pyeventbus3.pyeventbus3 import *


class Com:

    nb_process_created = 0

    def __init__(self):
        ## Definition nombre de processus
        #self.np_process = np_process TODO: supprime ce comment
        self.myId = Com.nb_process_created
        Com.nb_process_created += 1

        # Horloge de Lamport et Sémaphore pour protéger son accès
        self.lamport_clock = 0
        self.semaphore = threading.Semaphore()
        self.mailbox = Mailbox()

    def get_nb_process(self):
        return self.nb_process_created
    def get_my_id(self):
        return self.myId


    def inc_clock(self):
        """Incrémente l'horloge de Lamport."""
        with self.semaphore:  # Accès protégé par un sémaphore
            self.lamport_clock += 1
            print("Horloge de " + str(self.myId) + " incrémentée: " + str(self.lamport_clock))

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
        self.lamport_clock = max(self.lamport_clock, message_received.timestamp)
        self.inc_clock()
        self.mailbox.add_message(message_received)
        print(str(self.myId) + "a recu un message!")


