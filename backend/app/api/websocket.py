from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query

# WebSocket connection manager
from app.websocket.connection_manager import manager

# JWT token decoder
from app.core.security import decode_token

# Router for WebSocket endpoint
router = APIRouter()


# WebSocket endpoint for real-time communication
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(None)):
    
    # Close the connection if no token is provided
    if not token:
        await websocket.close(code=1008)
        return
        
    # Validate the JWT token
    payload = decode_token(token)

    # Reject the connection if the token is invalid
    if not payload or not payload.get("sub"):
        await websocket.close(code=1008)
        return
        
    # Extract the user ID from the token
    user_id = int(payload.get("sub"))
    
    # Register the user with the connection manager
    await manager.connect(websocket, user_id)

    try:
        # Keep listening for messages while the client is connected
        while True:
            data = await websocket.receive_text()

            # Send the received message back to the same user
            await manager.send_personal_message(
                f"You said: {data}",
                websocket,
            )

    # Remove the connection when the client disconnects
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)