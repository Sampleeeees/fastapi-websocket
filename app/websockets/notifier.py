"""Background task that periodically sends notifications to all active clients."""
import asyncio
from datetime import datetime

from app.core.logging import logger
from app.websockets.manager import manager


async def periodic_notifications(interval: int = 10) -> None:
    """Send periodic notifications to connected clients."""
    counter: int = 0

    try:
        while True:
            # wait for the configured interval
            await asyncio.sleep(interval)

            # only broadcast if there are active connections
            if manager.get_connection_count() > 0:
                counter += 1
                msg: str = f"Notification #{counter} at {datetime.now().isoformat()}"
                await manager.broadcast(msg)
                logger.info("Notification sent", message=msg)
    except asyncio.CancelledError:
        logger.info("Periodic notifications stopped")