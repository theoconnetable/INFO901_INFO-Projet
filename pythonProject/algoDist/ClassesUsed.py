
class AbstractMessage:
    """
    Classe abstraite de messages génériques
    """
    def __init__(self, payload, timestamp, sender, receiver):
        """
        :param payload: Le contenu du message
        :param timestamp: l'horloge de Lamport
        :param sender: Le protocole qui envoi le message
        :param receiver: Le protocole de destination du message
        """
        self.payload = payload
        self.timestamp = timestamp
        self.sender = sender
        self.receiver = receiver

    ## LES FONCTION DE RECUPERATION DES DONNEES
    def get_payload(self):
        return self.payload
    def get_timestamp(self):
        return self.timestamp
    def get_sender(self):
        return self.sender
    def get_receiver(self):
        return self.receiver

class Mailbox:
    """
        Classe de la boite aux lettres de messages
    """
    def __init__(self):
        self.mailbox = []

    def is_empty(self):
        """
        Vérifie si la boite aux lettres est vide
        :return: un Booléen
        """
        return len(self.mailbox) == 0

    def add_message(self, message):
        """
        Ajoute un message dans la boite aux lettres
        :param message: un AbstractMessage
        :return: none
        """
        self.mailbox.append(message)

    def get_message(self):
        """
        Dépile le premier message de la boite aux lettres
        :return: un message (AbstractMessage)
        """
        message = self.mailbox.pop(0)
        return message

class Token:
    """
    Classe qui gère le token
    """
    def __init__(self):
        self.active = True

class MessageToken:
    """Classe qui gère les messages de token"""
    def __init__(self, token, receiver):
        self.token = token
        self.receiver = receiver
