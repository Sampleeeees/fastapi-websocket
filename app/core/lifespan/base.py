"""
FastAPI lifespan context manager.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.lifespan.startup import on_startup
from app.core.lifespan.shutdown import on_shutdown


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """Application lifespan context manager."""
    await on_startup(app)
    try:
        yield
    finally:
        await on_shutdown(app)
