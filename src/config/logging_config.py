"""
Central logging configuration.
"""

import sys
from pathlib import Path

from loguru import logger

from src.config.settings import settings


# =====================================================
# CREATE LOG DIRECTORY
# =====================================================

Path("logs").mkdir(
    parents=True,
    exist_ok=True
)

# =====================================================
# REMOVE DEFAULT LOGGER
# =====================================================

logger.remove()

# =====================================================
# CONSOLE LOGGER
# =====================================================

logger.add(
    sys.stdout,
    level=settings.LOG_LEVEL,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level}</level> | "
        "<cyan>{name}</cyan>:"
        "<cyan>{function}</cyan>:"
        "<cyan>{line}</cyan> | "
        "{message}"
    ),
    colorize=True
)

# =====================================================
# APPLICATION LOG
# =====================================================

logger.add(
    "logs/app.log",
    level="INFO",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    enqueue=True
)

# =====================================================
# ERROR LOG
# =====================================================

logger.add(
    "logs/errors.log",
    level="ERROR",
    rotation="10 MB",
    retention="60 days",
    compression="zip",
    enqueue=True,
    backtrace=True,
    diagnose=True
)

# =====================================================
# AGENT LOG
# =====================================================

logger.add(
    "logs/agents.log",
    level="INFO",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    enqueue=True,
    filter=lambda record: "Agent" in record["message"]
)


def get_logger():
    return logger