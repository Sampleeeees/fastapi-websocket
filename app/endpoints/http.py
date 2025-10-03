"""HTTP endpoints for status checks and broadcasting."""
from datetime import datetime

from fastapi import APIRouter
from starlette.responses import HTMLResponse

from app.websockets.manager import manager

http_router = APIRouter()

@http_router.get("/")
async def get_index():
    """Return demo WebSocket HTML client."""
    with open("app/templates/index.html") as f:
        return HTMLResponse(content=f.read())


@http_router.get("/status")
async def get_status():
    """Return server status and number of active WebSocket connections."""
    return {
        "status": "running",
        "connections": manager.get_connection_count(),
        "timestamp": datetime.now().isoformat(),
    }


@http_router.post("/broadcast")
async def broadcast_message(message: str):
    """Broadcast a custom message to all active WebSocket clients."""
    await manager.broadcast(f"Manual broadcast: {message}")
    return {
        "status": "sent",
        "message": message,
        "recipients": manager.get_connection_count(),
    }