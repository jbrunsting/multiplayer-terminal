#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import signal
import sys

from chat.chatscreen import ChatScreen

chatScreen = ChatScreen()

def signal_handler(sig, frame):
    chatScreen.hide()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

async def chat():
    async with websockets.connect("ws://localhost:8765/chat") as websocket:
        name = input("Chat name: ")
        await websocket.send(name)
        print(f"> {name}")
        chatScreen.show()
        while True:
            chatScreen.add_message(await websocket.recv())


asyncio.get_event_loop().run_until_complete(chat())
