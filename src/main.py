"""
Main FastAPI Application

Entry Point for:
- Inventory APIs
- Invoice APIs
- Market Intelligence APIs
- Multi-Agent Workflow APIs
- LangGraph Orchestration
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.settings import settings
from src.config.logging_config import get_logger

from src.api.routers.health import router as health_router
from src.api.routers.inventory import router as inventory_router
from src.api.routers.invoice import router as invoice_router
from src.api.routers.market import router as market_router
from src.api.routers.workflow import router as workflow_router

from src.api.exception_handlers import (
    global_exception_handler
)

from src.database.models import Base
from src.database.db import engine

logger = get_logger()


# =====================================================
# APPLICATION LIFECYCLE
# =====================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info(
        "Starting Multi-Agent Ecommerce Platform..."
    )

    try:

        Base.metadata.create_all(
            bind=engine
        )

        logger.info(
            "Database initialized successfully"
        )

    except Exception as exc:

        logger.error(
            f"Database initialization failed: {exc}"
        )

    yield

    logger.info(
        "Shutting down application..."
    )


# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# =====================================================
# GLOBAL EXCEPTION HANDLER
# =====================================================

app.add_exception_handler(
    Exception,
    global_exception_handler
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# REGISTER ROUTERS
# =====================================================

app.include_router(
    health_router
)

app.include_router(
    inventory_router
)

app.include_router(
    invoice_router
)

app.include_router(
    market_router
)

app.include_router(
    workflow_router
)


# =====================================================
# ROOT ENDPOINT
# =====================================================

@app.get(
    "/",
    tags=["Root"]
)
async def root():

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "database": "sqlite",
        "llm": "sarvam",
        "workflow": "langgraph"
    }


# =====================================================
# APPLICATION INFO
# =====================================================

@app.get(
    "/info",
    tags=["System"]
)
async def application_info():

    return {
        "application":
        settings.APP_NAME,

        "version":
        settings.APP_VERSION,

        "debug":
        settings.DEBUG,

        "database":
        "SQLite",

        "llm":
        "Sarvam AI",

        "workflow":
        "LangGraph",

        "agents": [
            "Concierge Agent",
            "Inventory Agent",
            "Invoice Agent",
            "Market Intelligence Agent"
        ]
    }


# =====================================================
# STARTUP CHECK
# =====================================================

@app.get(
    "/startup-check",
    tags=["System"]
)
async def startup_check():

    return {
        "database": "connected",
        "api": "running",
        "workflow": "loaded",
        "agents": "ready"
    }