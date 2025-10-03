"""Connection manager for active WebSocket clients."""
import asyncio

from starlette.websockets import WebSocket

from app.core.logging import logger


class ConnectionManager:
    """Manages active WebSocket connections."""

    def __init__(self) -> None:
        """Initialize connection manager."""
        self.active_connections: list[WebSocket] = []
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> None:
        """Accept and register new WebSocket client."""
        await websocket.accept()

        async with self._lock:
            self.active_connections.append(websocket)

        logger.info("Client connected", total=len(self.active_connections))

    async def disconnect(self, websocket: WebSocket) -> None:
        """Remove a disconnected WebSocket client."""
        async with self._lock:
            self.active_connections.remove(websocket)

        logger.info("Client disconnected", total=len(self.active_connections))

    async def broadcast(self, message: str) -> None:
        """Send a message to all active WebSocket clients."""
        if not self.active_connections:
            return

        # prepare set of disconnected clients
        disconnected: set = set()
        async with self._lock:
            connections: list[WebSocket] = self.active_connections.copy()

        for connection in connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Failed to send message", error=str(e))
                disconnected.add(connection)

        if disconnected:
            async with self._lock:
                self.active_connections -= disconnected

    def get_connection_count(self) -> int:
        """Return the number of active WebSocket clients."""
        return len(self.active_connections)

    async def close_all(self) -> None:
        """Close all active WebSocket connections."""
        async with self._lock:
            connections: list[WebSocket] = self.active_connections.copy()
            self.active_connections.clear()

        for connection in connections:
            try:
                await connection.close(code=1001, reason="Server shutting down")
            except Exception as e:
                logger.error("Error closing connection", error=str(e))


manager = ConnectionManager()