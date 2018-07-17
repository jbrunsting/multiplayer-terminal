import asyncio
import websockets

async def connect(websocket, path):
    await websocket.send("connected to chat")
