"""
Database Engine Configuration
"""

from sqlalchemy import create_engine

from src.config.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=settings.DEBUG,
)