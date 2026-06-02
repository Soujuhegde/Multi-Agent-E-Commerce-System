import streamlit as st
import sys
import textwrap
from pathlib import Path

# Setup paths
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from components.sidebar import render_sidebar
from components.navbar import render_navbar
from services.api_client import APIClient
from utils.theme import apply_premium_theme, render_card, render_custom_alert

# Apply global premium styling & sidebar
apply_premium_theme()
render_sidebar()
render_navbar(page_title="Warehouse Inventory Core")

st.markdown(
    textwrap.dedent(
        """
        <p style="color: #4b5563; margin-bottom: 2rem; font-size: 1rem;">
            Monitor real-time warehouse stocks, edit quantites, and provision new product segments using the Autonomous Inventory Agent.
        </p>
        """
    ),
    unsafe_allow_html=True
)

tab1, tab2 = st.tabs(["📦 Stock Registry", "➕ Provision Product"])

with tab1:
    col_refresh, col_empty = st.columns([1, 4])
    with col_refresh:
        refresh = st.button("🔄 Refresh Stock")
        
    try:
        # Load products automatically on startup
        products = APIClient.get_products()
        
        if products:
            # Custom styled product listing cards
            for item in products:
                # Stock status and formatting
                qty = item.get("stock_quantity", 0)
                price = item.get("price", 0.0)
                category = item.get("category", "General")
                product_name = item.get("product_name", "Unknown Item")
                
                if qty == 0:
                    status_badge = '<span style="background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">OUT OF STOCK</span>'
                    border = "#b91c1c"
                elif qty < 20:
                    status_badge = '<span style="background: #fffbeb; color: #b45309; border: 1px solid #fde68a; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">LOW STOCK</span>'
                    border = "#b45309"
                else:
                    status_badge = '<span style="background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">IN STOCK</span>'
                    border = "#15803d"
                    
                render_card(
                    title=product_name,
                    body_html=f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; color: #111827;">
                        <div>
                            <span style="font-size: 0.8rem; background: #f3f4f6; color: #4b5563; padding: 3px 8px; border-radius: 6px; border: 1px solid #e5e7eb; font-weight: 500;">{category}</span>
                            <span style="margin-left: 15px; font-weight: 700; color: #4f46e5; font-size: 1.1rem;">₹{price:,.2f}</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <span style="font-size: 0.9rem;">Qty: <strong>{qty}</strong></span>
                            {status_badge}
                        </div>
                    </div>
                    """,
                    border_color=border
                )
        else:
            render_custom_alert("Warehouse database is currently empty. Populate initial stocks using scripts.", "info")
    except Exception as exc:
        render_custom_alert(f"Failed to fetch stock registry from backend: {exc}. Please verify the FastAPI backend is running.", "error")

with tab2:
    st.subheader("➕ Provision New Product")
    
    with st.form("new_product_form", clear_on_submit=True):
        new_name = st.text_input("Product Name", placeholder="e.g. iPad Pro M4")
        new_category = st.selectbox("Category", ["Mobiles", "Laptops", "Accessories", "Tablets", "Audio", "Wearables"])
        col_price, col_stock = st.columns(2)
        with col_price:
            new_price = st.number_input("Unit Price (INR)", min_value=1.0, value=25000.0, step=500.0)
        with col_stock:
            new_stock = st.number_input("Initial Stock Quantity", min_value=1, value=50, step=5)
            
        submit = st.form_submit_button("🚀 Deploy to Stock Registry")
        
        if submit:
            if not new_name.strip():
                render_custom_alert("Product Name cannot be blank.", "error")
            else:
                try:
                    import requests
                    response = requests.post(
                        "http://localhost:8000/inventory/add",
                        params={
                            "product_name": new_name,
                            "category": new_category,
                            "price": new_price,
                            "stock_quantity": new_stock
                        }
                    )
                    if response.status_code == 200 and response.json().get("success"):
                        render_custom_alert(f"Successfully provisioned '{new_name}' into database!", "success")
                        st.balloons()
                    else:
                        render_custom_alert("Backend rejected database provisioning. Ensure FastAPI is running.", "error")
                except Exception as e:
                    render_custom_alert(f"Could not connect to backend gateway: {e}", "error")