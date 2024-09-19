import mailbox


class AbstractMessage:
    def __init__(self, payload, timestamp, sender, receiver):
        self.payload = payload
        self.timestamp = timestamp
        self.sender = sender
        self.receiver = receiver

        def

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

