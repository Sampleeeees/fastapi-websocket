"""WebSocket endpoints for FastAPI."""
from datetime import datetime

from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.core.logging import logger
from app.websockets.manager import manager

websocket_router = APIRouter()

@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication."""
    # register client connection
    await manager.connect(websocket)

    try:
        # send welcome message
        await websocket.send_text(f"Connected at {datetime.now().isoformat()}")

        # receive and process messages
        while True:
            data = await websocket.receive_text()
            logger.info("Message receiver", message=data)
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error("WebSocket error", error=str(e))
    finally:
        # ensure client is removed from manager
        await manager.disconnect(websocket)