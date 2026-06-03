import streamlit as st
import sys
from pathlib import Path

# Setup paths relative to pages/ directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from components.sidebar import render_sidebar
from components.navbar import render_navbar, render_topnav
from components.metrics import render_metrics
from components.charts import inventory_chart
from utils.theme import apply_premium_theme, render_card

# Apply global premium styling
apply_premium_theme()
render_topnav("dashboard")
render_sidebar()  # no-op

# Page header
render_navbar(
    page_title="Dashboard",
    subtitle="A real-time overview of your store — products, invoices, revenue, and market performance."
)

# Metrics row
render_metrics()

# Two-column layout: chart + info card
col1, col2 = st.columns([3, 1], gap="large")

with col1:
    inventory_chart()

with col2:
    render_card(
        title="⚡ About This Platform",
        body_html="""
        <p style="color: #475569; line-height: 1.65; font-size: 13px; margin: 0;">
            Aether is a smart e-commerce platform that uses
            <strong style="color:#0f172a;">AI agents</strong> to help you manage
            inventory, generate invoices, and monitor competitor pricing —
            all automatically.
        </p>
        <div style="margin-top:16px; display:flex; flex-direction:column; gap:8px;">
            <div style="display:flex; align-items:center; gap:8px; font-size:12.5px; color:#475569;">
                <span style="color:#16a34a; font-size:14px;">✓</span> Inventory tracking
            </div>
            <div style="display:flex; align-items:center; gap:8px; font-size:12.5px; color:#475569;">
                <span style="color:#16a34a; font-size:14px;">✓</span> Automated invoicing
            </div>
            <div style="display:flex; align-items:center; gap:8px; font-size:12.5px; color:#475569;">
                <span style="color:#16a34a; font-size:14px;">✓</span> Competitor price alerts
            </div>
        </div>
        """,
        border_color="#4f46e5"
    )
