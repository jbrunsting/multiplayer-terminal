import threading
import asyncio
from datetime import datetime

MAX_MESSAGES = 100


class ChatRoom:
    def __init__(self, name):
        self.lastUpdated = datetime.now()
        self.name = name
        self.messages = []
        self.participants = []
        self.nextListenerId = 1
        self.messageListeners = {}
        self.lock = threading.Lock()

    def getMessages(self):
        return self.messages

    def addMessage(self, message):
        with self.lock:
            self.lastUpdated = datetime.now()
            self.messages.append(message)
            if len(self.messages) > MAX_MESSAGES:
                del self.messages[:len(self.messages) - MAX_MESSAGES]

            futures = []
            for listenerId, callback in self.messageListeners.items():
                futures.append(asyncio.Task(callback(listenerId, message)))
            asyncio.wait(futures, return_when=asyncio.ALL_COMPLETED)

    def addMessageListener(self, listener):
        with self.lock:
            listenerId = self.nextListenerId
            self.nextListenerId += 1
            self.messageListeners[listenerId] = listener

    def removeMessageListener(self, listenerId):
        with self.lock:
            del self.messageListeners[listenerId]
