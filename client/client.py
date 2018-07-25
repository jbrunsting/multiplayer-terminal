#!/usr/bin/env python

# WS client example

import websocket
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
    chat(chatScreen)

def chat(chatScreen):
    ws = websocket.create_connection("ws://localhost:8765/chat")
    def on_input(message):
        chatScreen.set_prompt("...")
        ws.send(message)
        chatScreen.set_prompt("> ")
    chatScreen.accept_input("Chat name: ", on_input)
    while True:
        message = ws.recv()
        chatScreen.add_message(message)
    ws.close()

curses.wrapper(main)
