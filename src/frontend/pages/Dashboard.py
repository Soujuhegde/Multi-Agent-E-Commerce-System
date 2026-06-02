import streamlit as st
import sys
import textwrap
from pathlib import Path

# Setup paths
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from components.sidebar import render_sidebar
from components.navbar import render_navbar
from utils.theme import apply_premium_theme, render_card

# Apply global premium styling & sidebar
apply_premium_theme()
render_sidebar()
render_navbar(page_title="Platform Diagnostics")

st.markdown(
    textwrap.dedent(
        """
        <p style="color: #4b5563; margin-bottom: 2rem; font-size: 1rem;">
            Real-time health monitoring of the autonomous Multi-Agent orchestration engine.
        </p>
        """
    ),
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    render_card(
        title="🔋 System Performance",
        body_html=textwrap.dedent(
            """
            <div style="display: flex; flex-direction: column; gap: 15px;">
                <div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.85rem; color: #111827;">
                        <span>CPU Allocation</span><span style="color: #4f46e5; font-weight: 600;">14%</span>
                    </div>
                    <div style="background: #e5e7eb; height: 6px; border-radius: 3px;">
                        <div style="background: #4f46e5; width: 14%; height: 100%; border-radius: 3px;"></div>
                    </div>
                </div>
                <div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.85rem; color: #111827;">
                        <span>LLM Context Usage</span><span style="color: #0d9488; font-weight: 600;">2.4k / 32k tokens</span>
                    </div>
                    <div style="background: #e5e7eb; height: 6px; border-radius: 3px;">
                        <div style="background: #0d9488; width: 8%; height: 100%; border-radius: 3px;"></div>
                    </div>
                </div>
                <div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.85rem; color: #111827;">
                        <span>Database Connection Pool</span><span style="color: #15803d; font-weight: 600;">99.8% Available</span>
                    </div>
                    <div style="background: #e5e7eb; height: 6px; border-radius: 3px;">
                        <div style="background: #15803d; width: 99.8%; height: 100%; border-radius: 3px;"></div>
                    </div>
                </div>
            </div>
            """
        ),
        border_color="#4f46e5"
    )

with col2:
    render_card(
        title="🌐 API Connectivity Gateway",
        body_html=textwrap.dedent(
            """
            <div style="font-size: 0.85rem; line-height: 1.8; color: #111827;">
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #e5e7eb; padding-bottom: 6px; margin-bottom: 6px;">
                    <strong>FastAPI Gateway</strong><span style="color: #15803d; font-weight: 600;">ONLINE (Port 8000)</span>
                </div>
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #e5e7eb; padding-bottom: 6px; margin-bottom: 6px;">
                    <strong>Sarvam AI Connection</strong><span style="color: #15803d; font-weight: 600;">ONLINE (240ms Latency)</span>
                </div>
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #e5e7eb; padding-bottom: 6px; margin-bottom: 6px;">
                    <strong>Vector Store Cache</strong><span style="color: #15803d; font-weight: 600;">CONNECTED (1.2k Embeddings)</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <strong>SMTP Dispatcher</strong><span style="color: #4b5563;">STANDBY (Invoices Ready)</span>
                </div>
            </div>
            """
        ),
        border_color="#0d9488"
    )

st.subheader("📋 System Events Log")
st.code(
    """
[2026-06-02 18:35:48] [INFO] Database initialized successfully
[2026-06-02 18:35:55] [INFO] Starting Multi-Agent E-Commerce Platform...
[2026-06-02 18:36:02] [INFO] Aether LangGraph Router loaded and verified.
[2026-06-02 18:36:10] [INFO] Concierge Agent connected to routing pipeline.
[2026-06-02 18:37:34] [INFO] Inventory Database seeded with 5 core products.
[2026-06-02 18:38:02] [INFO] Streamlit Frontend Control Center successfully initiated.
[2026-06-02 18:39:15] [INFO] Awaiting Agent requests...
    """,
    language="bash"
)