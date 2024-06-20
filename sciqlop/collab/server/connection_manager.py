#
#


from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str, websocket: WebSocket):
        del self.active_connections[client_id]

    async def send(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_shared(self, message: str, client_ids: set[str]):
        for client_id in client_ids:
            await self.active_connections[client_id].send_text(message)

    async def broadcast(self, message: str):
        for websocket in self.active_connections.values():
            await websocket.send_text(message)
