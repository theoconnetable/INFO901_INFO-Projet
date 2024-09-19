import threading
from AbstractMessage import AbstractMessage
from pyeventbus3.pyeventbus3 import *

class Com:
    def __init__(self):
        # Horloge de Lamport
        self.lamport_clock = 0
        # Sémaphore pour protéger l'accès à l'horloge
        self.semaphore = threading.Semaphore()

    def inc_clock(self):
        """Incrémente l'horloge de Lamport."""
        with self.semaphore:  # Accès protégé par un sémaphore
            self.lamport_clock += 1
            print(f"Horloge incrémentée : {self.lamport_clock}")

    def broadcast(self, o):
        self.inc_clock()
        message = AbstractMessage(o, self.lamport_clock)
        PyBus.Instance().post(message)


