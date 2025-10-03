"""Create main FastAPI instance."""
from fastapi import FastAPI

from app.core.lifespan.base import app_lifespan
from app.endpoints.http import http_router
from app.endpoints.websocket import websocket_router

app: FastAPI = FastAPI(
    title="Websocket FastAPI",
    lifespan=app_lifespan
)

# register routers
app.include_router(http_router)
app.include_router(websocket_router)