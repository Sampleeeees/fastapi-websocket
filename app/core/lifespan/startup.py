"""
Startup logic for FastAPI.
"""

import asyncio
from fastapi import FastAPI

from app.core.logging import logger
from app.core.settings import NOTIFICATION_INTERVAL
from app.websockets.notifier import periodic_notifications


async def on_startup(app: FastAPI) -> None:
    """Run startup tasks."""
    logger.info("Starting FastAPI WebSocket server")

    # background task for notifications
    app.state.notification_task = asyncio.create_task(
        periodic_notifications(interval=NOTIFICATION_INTERVAL),
        name="periodic_notifications"
    )
