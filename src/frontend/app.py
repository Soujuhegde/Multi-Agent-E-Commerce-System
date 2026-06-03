import streamlit as st
import sys
from pathlib import Path

# Setup sys.path inside main script to avoid import issues
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Page Config must be the first Streamlit command called on a page
st.set_page_config(
    page_title="Multi-Agent AI Control Center",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define custom page navigation structure
pages = [
    st.Page("pages/Overview.py", title="Dashboard", icon="📊", default=True),
    st.Page("pages/Agent_Workflow.py", title="AI Assistant", icon="💬"),
    st.Page("pages/Inventory.py", title="Inventory", icon="📦"),
    st.Page("pages/Invoice.py", title="Invoices & Billing", icon="📄"),
    st.Page("pages/Market_Intelligence.py", title="Market Insights", icon="📈")
]

# Create navigation and run the app
pg = st.navigation(pages)
pg.run()