class AbstractMessage:
    def __init__(self, payload, timestamp, sender, receiver):
        self.payload = payload
        self.timestamp = timestamp
        self.sender = sender
        self.receiver = receiver

    def get_payload(self):
        return self.payload
    def get_timestamp(self):
        return self.timestamp
    def get_sender(self):
        return self.sender
    def get_receiver(self):
        return self.receiver

class Mailbox:
    def __init__(self):
        self.mailbox = []

    def is_empty(self):
        return len(self.mailbox) == 0

    def add_message(self, message):
        self.mailbox.append(message)

    def get_message(self):
        message = self.mailbox.pop(0)
        return message

