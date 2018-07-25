import asyncio
import websockets

from chat.chatroom import ChatRoom

chats = {}


async def connect(websocket, chatName):
    if chatName in chats:
        await websocket.send("connected to chat " + chatName)
    else:
        chats[chatName] = ChatRoom(chatName)
        await websocket.send("created new chat " + chatName)

    chat = chats[chatName]
    for message in chat.getMessages():
        await websocket.send(message)

    chat.addMessageListener(getMessageCallback(websocket, chat))


async def sendMessage(chatName, message):
    chats[chatName].addMessage(message)


def getMessageCallback(websocket, chat):
    async def messageCallback(callbackId, message):
        try:
            await websocket.send(message)
        except Exception as e:
            print(e)
            chat.removeMessageListener(callbackId)

    return messageCallback
