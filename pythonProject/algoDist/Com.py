from threading import Thread, Lock, Condition
from ClassesUsed import AbstractMessage
from algoDist.ClassesUsed import Mailbox, Token, MessageToken
from pyeventbus3.pyeventbus3 import *
from time import sleep


class Com:
    """La classe des communications"""
    def __init__(self, p_id, nb_process):
        ## Variables pour l'envoi de messages
        self.myId = p_id
        self.nb_process = nb_process
        PyBus.Instance().register(self, self)
        self.lamport_clock = 0
        self.semaphore = threading.Semaphore()
        self.mailbox = Mailbox()

        ## variable etat pour gérer la section critique
        self.state = "null"
        if self.myId == (self.nb_process -1):
            token = Token()
            next_processus = (self.myId + 1) % self.nb_process
            print("TOKEN ENVOYEE A " + str(next_processus))
            message = MessageToken(token, next_processus)
            PyBus.Instance().post(message)

        ## Variables pour la synchronisation
        self.condition = threading.Condition()
        self.received_messages = {}


    def inc_clock(self):
        """Incrémente l'horloge de Lamport à l'aide d'un semaphore"""
        with self.semaphore:
            self.lamport_clock += 1
            print("Horloge de " + str(self.myId) + " incrémentée: " + str(self.lamport_clock))

    def broadcast(self, o):
        """
        Broadcaste un message à tous les autres processus
        :param o: AbstractMessage
        """
        for i in range(0,self.nb_process):
            if i != self.myId:
                self.inc_clock()
                message = AbstractMessage(o, self.lamport_clock,self.myId,i)
                PyBus.Instance().post(message)

    def send_to(self,o,dest):
        """
        Envoie un message à un processus définit
        :param o: AbstractMessage
        :param dest: un Processus
        """
        self.inc_clock()
        message = AbstractMessage(o, self.lamport_clock,self.myId,dest)
        PyBus.Instance().post(message)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=AbstractMessage)
    def receive(self, o):
        """
        Reçoit un AbstractMessage et le stock dans la boite aux lettres de messages
        :param o: AbstractMessage
        """
        message_received = o
        if message_received.get_receiver() == self.myId:
            print(str(self.myId) + " a recu un message avec timestamp: " + str(message_received.get_timestamp()))
            with self.semaphore:
                self.lamport_clock = max(self.lamport_clock, message_received.timestamp)
                self.inc_clock()
                self.mailbox.add_message(message_received)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=MessageToken)
    def on_token(self, message_token):
        """
        Reçoit un MessageToken et effectue les différentes actions associées en fonction de
        l'État du processus. Si request : se met en section critique et attend d'être en état release pour transmettre
        le Token. Sinon transmet directement le token.
        :param message_token: MessageToken
        """
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
        """
        Change l'état du processus en request
        """
        self.state = "REQUEST"

    def release_sc(self):
        """
        Change l'état du processus en release
        """
        self.state = "RELEASE"

    def synchronize(self):
        """
        Attend que tous les processus aient invoqué cette méthode pour tous les débloquer.
        """
        print("TODO")

    def broadcastSync(self, o, from_id):
        """
        Diffuse un message à tous les autres processus de manière synchrone et attend leur confirmation de réception.
        :param o: AbstractMessage
        :param from_id: un Processus
        """
        if self.myId == from_id:
            for i in range(self.nb_process):
                if i != self.myId:
                    self.inc_clock()
                    message = AbstractMessage(o, self.lamport_clock, self.myId, i)
                    PyBus.Instance().post(message)

            with self.condition:
                while len(self.received_messages) < (self.nb_process - 1):
                    self.condition.wait()
        else:
            with self.condition:
                while from_id not in self.received_messages:
                    self.condition.wait()

    def sendToSync(self, o, dest):
        """
        Envoie un message de manière synchrone à un processus dest et attend la confirmation de réception.
        :param o: AbstractMessage
        :param dest: un Processus
        """
        if self.myId != dest:
            self.inc_clock()
            message = AbstractMessage(o, self.lamport_clock, self.myId, dest)
            PyBus.Instance().post(message)
            with self.condition:
                while dest not in self.received_messages:
                    self.condition.wait()

    def recvFromSync(self, from_id):
        """
        Bloque jusqu'à ce qu'un message soit reçu d'un processus spécifique.
        :param from_id: Un processus
        :return:
        """
        with self.condition:
            while from_id not in self.received_messages:
                self.condition.wait()