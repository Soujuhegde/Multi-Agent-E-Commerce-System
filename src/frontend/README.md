# Streamlit Frontend

This directory contains the user interface for the Multi-Agent E-Commerce Platform, built with Streamlit.

## Overview

The frontend serves as the primary interaction point for customers. It provides a chat-like interface where users can converse with the AI assistant to search the catalog, inquire about products, and place orders.

## Running the Frontend

The Streamlit app is typically run in conjunction with the FastAPI backend. Make sure the backend is running before starting the frontend.

To run the frontend independently for development:

```bash
# From the project root
streamlit run src/frontend/app.py
```

## Structure

*   `app.py`: The main entry point for the Streamlit application.
