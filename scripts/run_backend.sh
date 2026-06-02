#!/bin/bash

echo "Starting FastAPI Backend..."

uvicorn src.main:app \
--host 0.0.0.0 \
--port 8000 \
--reload