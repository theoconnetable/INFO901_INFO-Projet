from typing import override


class Message:
    def __init__(self, payload):
        self.payload = payload
        self.clock = 0

    def increment_clock(self):
        self.clock += 1

    def update_clock(self, received_clock):
        self.clock = max(self.clock, received_clock) + 1

    def to_string(self):
        return "message: " + str(self.payload) + " ; clock: " + str(self.clock)

class BroadcastMessage:
    def __init__(self, payload, sender, clock):
        self.payload = payload
        self.sender = sender
        self.clock = clock

    def increment_clock(self):
        self.clock += 1

    def to_string(self):
        return "message: " + str(self.payload) + " ; de la part de: " + str(self.sender) + " ; clock: " + str(self.clock)

class MessageTo:
    def __init__(self, payload, receiver, clock):
        self.payload = payload
        self.receiver = receiver
        self.clock = clock

    def increment_clock(self):
        self.clock += 1

    def to_string(self):
        return "message: " + str(self.payload) + " ; à destination de: " + str(self.receiver) + " ; clock: " + str(self.clock)

class Token:
    def __init__(self):
        self.active = False
