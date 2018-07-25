import asyncio
import websockets
from chat.main import connect as connectToChat, sendMessage as sendChatMessage


async def main(websocket, path):
    pathComponents = path.split('/')

    if len(pathComponents) == 1:
        return

    root = pathComponents[1]
    if root == "chat":
        chatName = await websocket.recv()
        await connectToChat(websocket, chatName)
        while True:
            message = await websocket.recv()
            await sendChatMessage(chatName, message)


start_server = websockets.serve(main, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
