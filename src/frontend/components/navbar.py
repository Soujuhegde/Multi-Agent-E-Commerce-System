import streamlit as st
from utils.theme import render_header

def render_navbar(page_title: str = "Multi-Agent AI Control Center"):
    """
    Renders a unified premium header/navbar for the current active page.
    """
    render_header(
        title=f"🛒 {page_title}",
        subtitle="Powered by FastAPI + LangGraph Orchestrator + Sarvam AI Core"
    )