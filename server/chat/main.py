import asyncio
import websockets

chats = {}

async def connect(websocket, path):
    chatName = await websocket.recv()
    if chatName in chats:
        await websocket.send("connected to chat " + chatName)
    else:
        chats[chatName] = "temp"
        await websocket.send("created new chat " + chatName)
