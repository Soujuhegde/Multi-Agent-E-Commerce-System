import streamlit as st

# Setup sys.path inside main script to avoid import issues
import sys
import textwrap
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from components.sidebar import render_sidebar
from components.navbar import render_navbar
from components.metrics import render_metrics
from components.charts import inventory_chart
from utils.theme import apply_premium_theme, render_card

# Page Config must be the first Streamlit command called on a page
st.set_page_config(
    page_title="Multi-Agent AI Control Center",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global premium styling
apply_premium_theme()

# Render custom sidebar
render_sidebar()

# Render custom header navbar
render_navbar(page_title="Dashboard")

# Render metrics
render_metrics()

# Create two columns for charts & system description
col1, col2 = st.columns([2, 1])

with col1:
    inventory_chart()

with col2:
    render_card(
        title="⚡ System Overview",
        body_html=textwrap.dedent(
            """
            <p style="color: #4b5563; line-height: 1.6; font-size: 0.9rem; margin-top: 0; margin-bottom: 0;">
                Aether is an autonomous multi-agent platform orchestrating specialized AI nodes using a <strong>LangGraph routing state-flow</strong> to execute inventory auditing, billing cycles, and competitive pricing analytics.
            </p>
            """
        ),
        border_color="#4f46e5"
    )