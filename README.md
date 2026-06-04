# Multi-Agent E-Commerce Platform

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-Integration-orange.svg)
![SarvamAI](https://img.shields.io/badge/SarvamAI-Supported-purple.svg)

A sophisticated Multi-Agent E-Commerce Platform leveraging the power of Large Language Models (LLMs) to enhance customer experience, streamline operations, and provide intelligent assistance. The system uses LangGraph and LangChain to orchestrate multiple specialized agents.

## 🌟 Features

*   **Intelligent Assistant:** AI-powered chatbot for customer inquiries and product discovery.
*   **Multi-Agent Architecture:** Specialized agents for different tasks (e.g., catalog search, order management, customer support) built with LangGraph.
*   **RAG (Retrieval-Augmented Generation):** Enhances AI responses with accurate, up-to-date product information from the database.
*   **Modern Tech Stack:**
    *   **Backend:** FastAPI for high-performance, asynchronous REST APIs.
    *   **Frontend:** Streamlit for an interactive, conversational user interface.
    *   **AI/LLM:** LangChain, LangGraph, and SarvamAI integration.
    *   **Database:** SQLAlchemy and Alembic for robust data management.

## 📁 Project Structure

```
├── .github/          # GitHub Actions and workflows
├── data/             # Sample data and static files
├── docs/             # Project documentation
├── scripts/          # Utility scripts
├── src/              # Main source code
│   ├── agents/       # LangGraph agent definitions
│   ├── api/          # FastAPI routes and endpoints
│   ├── config/       # Application configuration and settings
│   ├── database/     # Database models and session management
│   ├── frontend/     # Streamlit application UI
│   ├── graph/        # Agent orchestration logic
│   ├── llm/          # LLM client wrappers (e.g., Sarvam client)
│   ├── rag/          # Document loaders and vector store logic
│   ├── schemas/      # Pydantic models for data validation
│   ├── services/     # Core business logic
│   ├── tools/        # Tools available to the agents
│   ├── utils/        # Helper functions
│   └── main.py       # FastAPI application entry point
├── .env.example      # Example environment variables
├── docker-compose.yml# Docker compose configuration
├── Dockerfile        # Docker image definition
├── Makefile          # Useful Make commands
├── pyproject.toml    # Python project metadata
└── requirements.txt  # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

*   Python 3.11+
*   Docker and Docker Compose (optional, for containerized deployment)

### Local Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Multi-Agent-E-Commerce-System.git
    cd Multi-Agent-E-Commerce-System
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    # On Windows:
    .venv\Scripts\activate
    # On Linux/macOS:
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables:**
    Copy the example environment file and configure your keys (e.g., Sarvam API key):
    ```bash
    cp .env.example .env
    ```

5.  **Run the Backend (FastAPI):**
    ```bash
    uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
    ```

6.  **Run the Frontend (Streamlit):**
    In a new terminal, activate the virtual environment and run:
    ```bash
    streamlit run src/frontend/app.py
    ```

## 🐳 Docker Deployment

You can run the entire stack using Docker Compose:

```bash
docker-compose up --build
```

## 🛠️ Development

*   **Linting & Formatting:** The project uses `black`, `ruff`, and `mypy` to maintain code quality.
*   **Testing:** Run tests using `pytest`:
    ```bash
    pytest
    ```

## Author 
Soujanya S P
