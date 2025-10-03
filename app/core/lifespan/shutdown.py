"""
Shutdown logic for FastAPI.
"""

import asyncio
from typing import Optional
from fastapi import FastAPI

from app.core.logging import logger
from app.core.settings import SHUTDOWN_TIMEOUT
from app.websockets.manager import manager
from app.websockets.shutdown import shutdown_handler


async def on_shutdown(app: FastAPI) -> None:
    """Run shutdown tasks."""
    logger.info("Shutting down FastAPI WebSocket server")

    # cancel background notifier
    await _cancel_task(getattr(app.state, "notification_task", None))

    # wait for graceful shutdown with timeout
    try:
        await asyncio.wait_for(
            shutdown_handler.wait_for_connections_or_timeout(),
            timeout=SHUTDOWN_TIMEOUT,
        )
    except asyncio.TimeoutError:
        logger.error("Shutdown timeout exceeded, forcing exit", connections=manager.get_connection_count())
    else:
        logger.info("Shutdown complete", connections=manager.get_connection_count())


async def _cancel_task(task: Optional[asyncio.Task]) -> None:
    """Cancel background task if running."""
    if not task:
        return
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        logger.info("Background task cancelled", task=task.get_name())
