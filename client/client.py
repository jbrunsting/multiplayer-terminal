#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import signal
import sys
import curses

from chat.chatscreen import ChatScreen

def main(stdscr):
    curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    chatScreen = ChatScreen(stdscr)
    asyncio.get_event_loop().run_until_complete(chat(chatScreen))

async def chat(chatScreen):
    async with websockets.connect("ws://localhost:8765/chat") as websocket:
        name = await chatScreen.get_input("Chat name: ")
        await websocket.send(name)
        response = await websocket.recv()
        chatScreen.add_message(response)
        while True:
            inputFuture = asyncio.ensure_future(chatScreen.get_input("> "))
            messageFuture = asyncio.ensure_future(websocket.recv())
            finished, unfinished = await asyncio.wait([inputFuture, messageFuture], return_when=asyncio.FIRST_COMPLETED)
            if inputFuture in finished:
                await websocket.send(inputFuture.result())
            else:
                chatScreen.add_message(messageFuture.result())

curses.wrapper(main)
