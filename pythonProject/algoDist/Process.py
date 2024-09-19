#from EventBus import EventBus
#from Message import *
#from pyeventbus3.pyeventbus3 import *
#-----------------------------------------------
from threading import Lock, Thread
from time import sleep
from Com import Com

class Process(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.com = Com()
        self.nbProcess = self.com.get_nb_process()
        self.setName(name)
        self.alive = True
        self.start()

    def run(self):
        loop = 0
        while self.alive:
            print(self.getName() + " Loop: " + str(loop))
            sleep(1)

            if self.getName() == "P0":
                print(self.getName() + " envoie un message")
                self.com.send_to("j'appelle 2 et je te recontacte après", 1)

    def waitStopped(self):
        self.join()

    def stop(self):
        self.alive = False
        self.join()