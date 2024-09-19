from threading import Lock, Thread

from time import sleep

#from geeteventbus.subscriber import subscriber
#from geeteventbus.eventbus import eventbus
#from geeteventbus.event import event

#from EventBus import EventBus
from Message import *

from pyeventbus3.pyeventbus3 import *

class Process(Thread):
    nbProcessCreated = 0

    def __init__(self, name, npProcess):
        Thread.__init__(self)

        self.npProcess = npProcess
        self.myId = Process.nbProcessCreated
        Process.nbProcessCreated +=1
        self.setName(name)
        self.message = Message("")  # Chaque processus a un message
        self.etat = "RELEASE"
        self.mytoken = Token()
        PyBus.Instance().register(self, self)
        self.alive = True
        self.start()

    @subscribe(threadMode = Mode.PARALLEL, onEvent=Message)
    def process(self, event):        
        received_message = event
        print("Message recu: " + received_message.to_string())
        self.message.update_clock(received_message.clock)
        self.message.payload = received_message.payload
        print(self.getName() + " est désormais: " + self.message.to_string())

    def run(self):
        loop = 0
        while self.alive:
            print(self.getName() + " Loop: " + str(loop))
            sleep(1)

            if self.getName() == "P1":
                self.message.payload = "ga"
                print(self.getName() + " a pour valeurs: " + self.message.to_string())
                self.message.increment_clock()
                PyBus.Instance().post(self.message)
                self.broadcast("go")
                self.sendTo("gi", "P0")

            if self.npProcess == self.nbProcessCreated and loop == 0 :
                self.mytoken.active = True
                next_p = (self.npProcess + 1) % self.nbProcessCreated
                self.sendTo(self.mytoken, next_p)

            if self.getName() == "P2":
                self.request()
                print(self.getName() + " en section critique")
                sleep(5)
                self.release()

            loop+=1
        print(self.getName() + " stopped")

    def stop(self):
        self.alive = False

    def waitStopped(self):
        self.join()

    def broadcast(self, o):
        broadcast_message = BroadcastMessage(o,self.getName(), self.message.clock)
        broadcast_message.increment_clock()
        ##TODO: degage increment de la classe BroadcastMessage
        PyBus.Instance().post(broadcast_message)

    def sendTo(self, o, receiver):
        message_to = MessageTo(o, receiver, self.message.clock)
        message_to.increment_clock()
        PyBus.Instance().post(message_to)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=BroadcastMessage)
    def onBroadcast(self, m):
        received_message = m
        if self.getName() != received_message.sender:
            print("Message recu: " + received_message.to_string())
            self.message.update_clock(received_message.clock)
            self.message.payload = received_message.payload
            print(self.getName() + " est désormais: " + self.message.to_string())

    @subscribe(threadMode=Mode.PARALLEL, onEvent=MessageTo)
    def onReceive(self, m):
        received_message = m
        if type(received_message.payload) == Token and self.alive == True:
            self.onToken(received_message.payload)
        if self.getName() == received_message.receiver:
            print("Message recu: " + received_message.to_string())
            self.message.update_clock(received_message.clock)
            self.message.payload = received_message.payload
            print(self.getName() + " est désormais: " + self.message.to_string())

    def onToken(self, token):
        next_p = (self.npProcess + 1) % self.nbProcessCreated
        if token.active:
            print(str(self.getName()) + " a recu le Token")
            if self.etat == "REQUEST":
                self.mytoken = token
                self.etat = "SC"
            elif self.etat == "SC":
                print(str(self.getName()) + "Déjà en posséssion du token")
                self.sendTo(token, next_p)
            else :
                print(str(self.getName()) + " a rendu le Token")
                self.sendTo(token, next_p)
                self.mytoken.token = False




    def request(self):
        self.etat = "REQUEST"
        while self.etat != "SC":
            sleep(1)

    def release(self):
        self.etat = "RELEASE"
        self.onToken(self.mytoken)

