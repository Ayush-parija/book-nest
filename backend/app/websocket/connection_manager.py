from fastapi import WebSocket
from typing import List
import asyncio


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self._loop = None

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            pass
        print(f"✅ Client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

        print(f"❌ Client disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(
        self,
        message: str,
        websocket: WebSocket,
    ):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        print(f"📢 Broadcasting to {len(self.active_connections)} clients")
        print(f"📨 Message: {message}")

        disconnected = []

        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print("Broadcast Error:", e)
                disconnected.append(connection)

        for connection in disconnected:
            self.disconnect(connection)

    def broadcast_sync(self, message: str):
        if not self.active_connections:
            return
            
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self.broadcast(message))
        except RuntimeError:
            if self._loop:
                asyncio.run_coroutine_threadsafe(self.broadcast(message), self._loop)
            else:
                print("No event loop available for broadcast.")


manager = ConnectionManager()
print("Connection Manager ID:", id(manager))