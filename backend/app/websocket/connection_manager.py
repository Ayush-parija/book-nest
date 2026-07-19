from fastapi import WebSocket
from typing import Dict, List
import asyncio


# Manages all active WebSocket connections
class ConnectionManager:
    def __init__(self):
        # Store active WebSocket connections for each user
        self.active_connections: Dict[int, List[WebSocket]] = {}

        # Store the running event loop for background tasks
        self._loop = None

    # Accept and register a new WebSocket connection
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()

        # Create a connection list for the user if it doesn't exist
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []

        # Add the new WebSocket connection
        self.active_connections[user_id].append(websocket)

        # Save the current event loop
        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            pass

        print(f"✅ User {user_id} connected. Total users connected: {len(self.active_connections)}")

    # Remove a disconnected WebSocket connection
    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)

            # Remove the user entry if no active connections remain
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

        print(f"❌ User {user_id} disconnected. Total users connected: {len(self.active_connections)}")

    # Send a message to a specific WebSocket connection
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    # Send a message to all active connections of a user
    async def send_to_user(self, user_id: int, message: str):
        if user_id in self.active_connections:
            disconnected = []

            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(message)
                except Exception as e:
                    print(f"Error sending to user {user_id}:", e)
                    disconnected.append(connection)

            # Remove connections that are no longer active
            for connection in disconnected:
                self.disconnect(connection, user_id)

    # Send a message to a user from synchronous code
    def send_to_user_sync(self, user_id: int, message: str):
        if user_id not in self.active_connections:
            return

        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self.send_to_user(user_id, message))
        except RuntimeError:
            if self._loop:
                asyncio.run_coroutine_threadsafe(self.send_to_user(user_id, message), self._loop)
            else:
                print("No event loop available to send message.")

    # Broadcast a message to all connected users
    async def broadcast(self, message: str):
        print(f"📢 Broadcasting to all clients")

        for user_id in list(self.active_connections.keys()):
            await self.send_to_user(user_id, message)

    # Broadcast a message from synchronous code
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


# Global WebSocket connection manager instance
manager = ConnectionManager()