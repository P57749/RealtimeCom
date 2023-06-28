#
# from typing import Union
#
# from fastapi import FastAPI
# from pydantic import BaseModel
#
# app = FastAPI()
#
#
# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None
#
#
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
#
#
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
#
#
# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}
#
#
from typing import Union

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from item import Item
# from fastapi_websocket import WebSocket
from starlette.responses import HTMLResponse

app = FastAPI()

# Lista para almacenar las conexiones WebSocket activas
connections = []


def process_message(message):
    if message == "ping":
        response = "pong"
    elif message == "hello":
        response = "Hello, client!"
    else:
        response = "Unknown command"

    return response






html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket.accept()

    # Agregar la conexión WebSocket a la lista de conexiones activas
    connections.append(websocket)

    try:
        while True:
            # Recibir mensaje desde el cliente WebSocket
            message = await websocket.receive_text()

            # Procesar el mensaje recibido
            response = process_message(message)

            # Enviar respuesta al cliente WebSocket
            await websocket.send_text(response)

    except WebSocketDisconnect:
        # Remover la conexión WebSocket de la lista cuando se desconecta
        connections.remove(websocket)
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

