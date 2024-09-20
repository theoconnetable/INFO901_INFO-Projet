from threading import Thread, Lock, Condition
from ClassesUsed import AbstractMessage
from algoDist.ClassesUsed import Mailbox, Token, MessageToken
from pyeventbus3.pyeventbus3 import *
from time import sleep


class Com:

    def __init__(self, p_id, nb_process):
        self.myId = p_id
        self.nb_process = nb_process
        self.state = "null"
        PyBus.Instance().register(self, self)
        self.lamport_clock = 0
        self.semaphore = threading.Semaphore()
        self.mailbox = Mailbox()
        if self.myId == (self.nb_process -1):
            token = Token()
            next_processus = (self.myId + 1) % self.nb_process
            print("TOKEN ENVOYEE A " + str(next_processus))
            message = MessageToken(token, next_processus)
            PyBus.Instance().post(message)



    def get_nb_process(self):
        return self.nb_process
    def get_my_id(self):
        return self.myId


    def inc_clock(self):
        """Incrémente l'horloge de Lamport."""
        with self.semaphore:
            self.lamport_clock += 1
            print("Horloge de " + str(self.myId) + " incrémentée: " + str(self.lamport_clock))

    def broadcast(self, o):
        for i in range(0,self.nb_process):
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
        if message_received.get_receiver() == self.myId:
            print(str(self.myId) + " a recu un message avec timestamp: " + str(message_received.get_timestamp()))
            with self.semaphore:
                self.lamport_clock = max(self.lamport_clock, message_received.timestamp)
                self.inc_clock()
                self.mailbox.add_message(message_received)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=MessageToken)
    def on_token(self, message_token):
        if message_token.receiver == self.myId:
            token = message_token.token
            next_process = (self.myId + 1) % self.nb_process
            if self.state == "REQUEST":
                self.state = "SC"
                while self.state != "RELEASE":
                    sleep(1)
                self.state = "null"
            message = MessageToken(token, next_process)
            PyBus.Instance().post(message)

    def request_sc(self):
        self.state = "REQUEST"

    def release_sc(self):
        self.state = "RELEASE"

    def synchronize(self):
        print("TODO")