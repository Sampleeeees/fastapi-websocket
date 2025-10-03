"""Graceful shutdown handler for WebSocket connections."""
import asyncio
from datetime import datetime

from app.core.logging import logger
from app.core.settings import SHUTDOWN_TIMEOUT
from app.websockets.manager import ConnectionManager, manager


class GracefulShutdown:
    """Handle graceful shutdown of WebSocket connections."""

    def __init__(self, manager: ConnectionManager, timeout: int) -> None:
        """Initialize graceful shutdown handler."""
        self.manager: ConnectionManager = manager
        self.timeout: int = timeout
        self.shutdown_event: asyncio.Event = asyncio.Event()
        self.shutdown_start_time: datetime | None = None

    async def wait_for_connections_or_timeout(self) -> None:
        """Wait until all connections are closed or timeout is reached."""
        self.shutdown_start_time = datetime.now()
        logger.info("Graceful shutdown initiated", timeout=self.timeout)

        # record event loop time when shutdown started
        start_time: float = asyncio.get_event_loop().time()

        while True:
            # check number of active connections
            count: int = self.manager.get_connection_count()

            # elapsed time since shutdown started
            elapsed: float = asyncio.get_event_loop().time() - start_time
            remaining: float = self.timeout - elapsed

            # if all active clients disconnected then shutdown immediately
            if count == 0:
                logger.info("All connections closed. Processing with shutdown")
                break

            # if timeout reached then force close remaining connections
            if elapsed >= self.timeout:
                logger.warning("Timeout reached. Force closing connections", active=count)
                await self.manager.close_all()
                break

            # wait 1 second before checking again
            await asyncio.sleep(1)

    def trigger_shutdown(self) -> None:
        """Trigger shutdown event manually."""
        self.shutdown_event.set()


shutdown_handler = GracefulShutdown(manager=manager, timeout=SHUTDOWN_TIMEOUT)


