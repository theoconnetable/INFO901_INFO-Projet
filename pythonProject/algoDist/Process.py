#from EventBus import EventBus
#from Message import *
#from pyeventbus3.pyeventbus3 import *
#-----------------------------------------------
from threading import Lock, Thread
from time import sleep
from Com import Com

class Process(Thread):
    nb_proccess = 3
    nbProcessCreated = 0

    def __init__(self, name):
        Thread.__init__(self)
        self.myId = Process.nbProcessCreated
        Process.nbProcessCreated += 1
        self.com = Com(self.myId, Process.nb_proccess)
        self.nbProcess = Process.nbProcessCreated
        self.setName(name)
        self.alive = True
        self.start()

    def run(self):
        loop = 0
        while self.alive:
            print(self.getName() + " Loop: " + str(loop))
            sleep(1)

            if self.getName() == "P0":
                print(self.getName() + " broadcast un message")
                self.com.send_to("bonjour à tous", 1)

            if self.getName() == "P1":
                print(self.getName() + " envoie un message")
                self.com.send_to("j'appelle 3 et je te recontacte après", 2)
            if self.getName() == "P2":
                self.com.request_sc()
                print(self.getName() + " en sec critique")
                self.com.release_sc()
        print(self.getName() + " stopped")

    def waitStopped(self):
        self.join()

    def stop(self):
        self.alive = False
        self.join()