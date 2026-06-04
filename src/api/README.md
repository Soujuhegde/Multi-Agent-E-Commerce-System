# FastAPI Backend

This directory contains the core REST API for the Multi-Agent E-Commerce Platform, built with FastAPI.

## Overview

The API layer manages the communication between the frontend (Streamlit) and the underlying multi-agent system. It handles user requests, orchestrates the LangGraph agents, interfaces with the LLMs (SarvamAI), and manages interactions with the database.

## Running the API

To run the FastAPI server for development:

```bash
# From the project root
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## Structure

The API is structured to separate concerns:
*   Routes are defined in the `api` module (or directly in `main.py` for simpler setups).
*   Business logic and agent orchestration are handled by `agents` and `graph`.
*   Data models and validation are defined in `schemas`.
