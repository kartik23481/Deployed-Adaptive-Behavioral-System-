# # services/ws_manager.py

# from fastapi import WebSocket
# import typing

# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: typing.List[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         if websocket in self.active_connections:
#             self.active_connections.remove(websocket)

#     async def broadcast(self, message: str):
#         # Send the log to every connected frontend terminal
#         for connection in self.active_connections:
#             try:
#                 await connection.send_text(message)
#             except:
#                 pass

# # Global instance to be imported by your scraper and main.py
# ws_manager = ConnectionManager()


# services/ws_manager.py
from fastapi import WebSocket
import typing

class ConnectionManager:
    def __init__(self):
        self.active_connections: typing.Dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    # ONLY delete if the disconnecting socket matches the active socket
    def disconnect(self, client_id: str, websocket: WebSocket):
        if client_id in self.active_connections and self.active_connections[client_id] == websocket:
            del self.active_connections[client_id]

    async def send_personal_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(message)
            except Exception:
                pass 
        else:
            print(f"⚠️ WS Drop: Client {client_id} not found in active connections.")

ws_manager = ConnectionManager()