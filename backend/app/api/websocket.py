from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.websocket.connection_manager import manager
from app.core.security import decode_token

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(None)):
    if not token:
        await websocket.close(code=1008)
        return
        
    payload = decode_token(token)
    if not payload or not payload.get("sub"):
        await websocket.close(code=1008)
        return
        
    user_id = int(payload.get("sub"))
    
    await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(
                f"You said: {data}",
                websocket,
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)