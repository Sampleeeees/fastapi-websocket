"""Logging configuration using structlog."""
import logging
from typing import Literal

import structlog

def setup_logging(environment: Literal["dev", "prod"] = "dev") -> structlog.stdlib.BoundLogger:
    """Configure structlog for logging."""
    # base configuration for stdlib logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )

    # common processors for structlog
    processors: list[structlog.types.Processor] = [
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    # renderer depending on environment
    if environment == "prod":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger("fastapi-websocket")

logger: structlog.stdlib.BoundLogger = setup_logging(environment="dev")