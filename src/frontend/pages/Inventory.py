import streamlit as st
import sys
from pathlib import Path

# Setup paths
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from components.sidebar import render_sidebar
from components.navbar import render_navbar, render_topnav
from services.api_client import APIClient
from utils.theme import apply_premium_theme, render_card, render_custom_alert

# Apply global premium styling
apply_premium_theme()
render_topnav("inventory")
render_sidebar()  # no-op

render_navbar(
    page_title="Inventory",
    subtitle="View and manage your product stock levels in real time."
)

# ─── Tabs ────────────────────────────────────────────
tab_stock, tab_add = st.tabs(["📦  Current Stock", "➕  Add New Product"])

# ═══════════════════════════════════════════════════
# TAB 1 — Current Stock
# ═══════════════════════════════════════════════════
with tab_stock:
    col_btn, col_empty = st.columns([1, 6])
    with col_btn:
        refresh = st.button("🔄  Refresh")

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    try:
        products = APIClient.get_products()

        if products:
            for item in products:
                qty          = item.get("stock_quantity", 0)
                price        = item.get("price", 0.0)
                category     = item.get("category", "General")
                product_name = item.get("product_name", "Unknown Item")

                # Status badge + accent colour
                if qty == 0:
                    status_html  = '<span style="background:#fef2f2; color:#dc2626; border:1px solid #fecaca; padding:3px 9px; border-radius:20px; font-size:11px; font-weight:600; letter-spacing:0.3px;">OUT OF STOCK</span>'
                    accent       = "#dc2626"
                elif qty < 20:
                    status_html  = '<span style="background:#fffbeb; color:#d97706; border:1px solid #fde68a; padding:3px 9px; border-radius:20px; font-size:11px; font-weight:600; letter-spacing:0.3px;">LOW STOCK</span>'
                    accent       = "#d97706"
                else:
                    status_html  = '<span style="background:#f0fdf4; color:#16a34a; border:1px solid #bbf7d0; padding:3px 9px; border-radius:20px; font-size:11px; font-weight:600; letter-spacing:0.3px;">IN STOCK</span>'
                    accent       = "#16a34a"

                render_card(
                    title=product_name,
                    body_html=f"""
                    <div style="display:flex; justify-content:space-between;
                                align-items:center; flex-wrap:wrap; gap:10px;">
                        <div style="display:flex; align-items:center; gap:12px;">
                            <span style="
                                font-size:11.5px; background:#f1f5f9; color:#475569;
                                padding:3px 9px; border-radius:6px; font-weight:500;
                                border:1px solid #e2e8f0;">
                                {category}
                            </span>
                            <span style="font-weight:700; color:#4f46e5; font-size:15px;">
                                ₹{price:,.2f}
                            </span>
                        </div>
                        <div style="display:flex; align-items:center; gap:14px;">
                            <span style="font-size:13px; color:#475569;">
                                Qty: <strong style="color:#0f172a;">{qty}</strong>
                            </span>
                            {status_html}
                        </div>
                    </div>
                    """,
                    border_color=accent,
                )

        else:
            render_custom_alert(
                "No products found. Add your first product using the 'Add New Product' tab.",
                "info",
            )

    except Exception as exc:
        render_custom_alert(
            f"Could not load products. Please check your connection. ({exc})", "error"
        )


# ═══════════════════════════════════════════════════
# TAB 2 — Add New Product
# ═══════════════════════════════════════════════════
with tab_add:
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(
            """
            <h3 style="margin:0 0 16px 0; font-size:14px; font-weight:700;
                       color:#0f172a; letter-spacing:-0.2px;">
                ➕ New Product Details
            </h3>
            """,
            unsafe_allow_html=True,
        )

        with st.form("new_product_form", clear_on_submit=True):
            new_name = st.text_input(
                "Product Name",
                placeholder="e.g. iPad Pro M4",
            )
            new_category = st.selectbox(
                "Category",
                ["Mobiles", "Laptops", "Accessories", "Tablets", "Audio", "Wearables"],
            )

            col_price, col_stock = st.columns(2, gap="medium")
            with col_price:
                new_price = st.number_input(
                    "Unit Price (₹)",
                    min_value=1.0,
                    value=25000.0,
                    step=500.0,
                    format="%.2f",
                )
            with col_stock:
                new_stock = st.number_input(
                    "Opening Stock Quantity",
                    min_value=1,
                    value=50,
                    step=5,
                )

            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            submit = st.form_submit_button("✅  Save Product")

            if submit:
                if not new_name.strip():
                    render_custom_alert("Product Name cannot be blank.", "error")
                else:
                    try:
                        res = APIClient.add_product(
                            product_name=new_name,
                            category=new_category,
                            price=new_price,
                            stock_quantity=new_stock,
                        )
                        if res.get("success"):
                            render_custom_alert(
                                f"✓ '{new_name}' has been added to your inventory!", "success"
                            )
                            st.balloons()
                            st.rerun()
                        else:
                            render_custom_alert(
                                "Could not save the product. Please try again.", "error"
                            )
                    except Exception as e:
                        render_custom_alert(
                            f"Connection error. Please check the server is running. ({e})",
                            "error",
                        )