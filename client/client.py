#!/usr/bin/env python

# WS client example

import asyncio
import websockets


async def chat():
    async with websockets.connect("ws://localhost:8765/chat") as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")


asyncio.get_event_loop().run_until_complete(chat())
