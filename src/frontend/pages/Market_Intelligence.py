import streamlit as st
import sys
import textwrap
from pathlib import Path
from datetime import datetime

# Setup paths
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from components.sidebar import render_sidebar
from components.navbar import render_navbar, render_topnav
from services.api_client import APIClient
from utils.theme import apply_premium_theme, render_card, render_custom_alert

# Apply global premium styling
apply_premium_theme()
render_topnav("market")
render_sidebar()  # no-op

render_navbar(
    page_title="Market Insights",
    subtitle="Compare your prices against competitors, track demand trends, and get smart pricing recommendations."
)

# ─── Two-column layout ────────────────────────────
col_controls, col_results = st.columns([2, 3], gap="large")

# ═══════════════════════════════════════════════
# LEFT: Controls
# ═══════════════════════════════════════════════
with col_controls:
    with st.container(border=True):
        st.markdown(
            """
            <h3 style="margin:0 0 16px 0; font-size:14px; font-weight:700;
                       color:#0f172a;">
                🎯 Analysis Controls
            </h3>
            """,
            unsafe_allow_html=True,
        )

        try:
            products = APIClient.get_products()
            if products:
                product_list     = [p["product_name"] for p in products]
                selected_product = st.selectbox("Select Product", product_list)

                st.markdown(
                    "<hr style='border:none; border-top:1px solid #e2e8f0; margin:14px 0;'>",
                    unsafe_allow_html=True,
                )

                competitor_source = st.selectbox(
                    "Compare Against",
                    ["Amazon.in", "Flipkart", "Croma", "Vijay Sales"],
                )

                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
                analyse_btn = st.button("🚀  Analyse Prices")

                if analyse_btn:
                    target_p      = next(p for p in products if p["product_name"] == selected_product)
                    current_price = target_p["price"]
                    try:
                        res = APIClient.market_insights(selected_product)
                        st.session_state.market_results = {
                            "product_name":      selected_product,
                            "current_price":     current_price,
                            "competitor_price":  res.get("competitor_price", current_price),
                            "recommended_price": res.get("recommended_price", current_price),
                            "demand_score":      res.get("demand_score", 75),
                            "trend_score":       res.get("trend_score", 70),
                            "source":            competitor_source,
                            "timestamp":         datetime.utcnow().strftime("%H:%M UTC"),
                        }
                        st.success("Analysis complete!")
                    except Exception as exc:
                        render_custom_alert(f"Could not fetch market data. ({exc})", "error")
            else:
                render_custom_alert(
                    "No products found. Please add products to your inventory first.", "info"
                )

        except Exception as e:
            render_custom_alert(
                f"Could not load products. Please check your connection. ({e})", "error"
            )

# ═══════════════════════════════════════════════
# RIGHT: Results
# ═══════════════════════════════════════════════
with col_results:
    if "market_results" in st.session_state and st.session_state.market_results:
        res = st.session_state.market_results

        with st.container(border=True):
            # Header row with timestamp
            col_h, col_t = st.columns([3, 1])
            with col_h:
                st.markdown(
                    f"""
                    <h3 style="margin:0; font-size:14px; font-weight:700; color:#0f172a;">
                        📊 {res['product_name']}
                    </h3>
                    """,
                    unsafe_allow_html=True,
                )
            with col_t:
                st.markdown(
                    f"""
                    <span style="font-size:11px; background:#eff6ff; color:#2563eb;
                                 padding:3px 8px; border-radius:20px; font-weight:600;
                                 float:right; border:1px solid #bfdbfe;">
                        {res['timestamp']}
                    </span>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

            # Price comparison cards
            pc1, pc2 = st.columns(2, gap="small")
            with pc1:
                st.markdown(
                    f"""
                    <div style="background:#f8fafc; border:1px solid #e2e8f0;
                                border-radius:10px; padding:14px; margin-bottom:12px;">
                        <div style="font-size:11px; color:#475569; font-weight:600;
                                    text-transform:uppercase; letter-spacing:0.6px;
                                    margin-bottom:6px;">Your Price</div>
                        <div style="font-size:1.5rem; font-weight:700; color:#0f172a;">
                            ₹{res['current_price']:,.2f}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with pc2:
                st.markdown(
                    f"""
                    <div style="background:#f8fafc; border:1px solid #e2e8f0;
                                border-radius:10px; padding:14px; margin-bottom:12px;">
                        <div style="font-size:11px; color:#475569; font-weight:600;
                                    text-transform:uppercase; letter-spacing:0.6px;
                                    margin-bottom:6px;">
                            {res['source']}
                        </div>
                        <div style="font-size:1.5rem; font-weight:700; color:#dc2626;">
                            ₹{res['competitor_price']:,.2f}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Recommended price highlight
            st.markdown(
                f"""
                <div style="background:#f0fdf4; border:1px solid #bbf7d0;
                            border-radius:12px; padding:16px; margin-bottom:16px;
                            text-align:center;">
                    <div style="font-size:11px; color:#16a34a; font-weight:700;
                                text-transform:uppercase; letter-spacing:0.6px;
                                margin-bottom:6px;">
                        💰 Recommended Price
                    </div>
                    <div style="font-size:1.7rem; font-weight:700; color:#0f172a;">
                        ₹{res['recommended_price']:,.2f}
                    </div>
                    <p style="margin:6px 0 0 0; font-size:12px; color:#475569;">
                        Balances profit margin with competitive positioning
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Demand & trend gauges
            render_card(
                title="📈 Market Gauges",
                body_html=f"""
                <div style="display:flex; flex-direction:column; gap:14px; color:#0f172a;">
                    <div>
                        <div style="display:flex; justify-content:space-between;
                                    margin-bottom:5px; font-size:13px;">
                            <span>Market Demand</span>
                            <span style="color:#0d9488; font-weight:600;">{res['demand_score']}%</span>
                        </div>
                        <div style="background:#e2e8f0; height:5px; border-radius:99px;">
                            <div style="background:#0d9488; width:{res['demand_score']}%;
                                        height:100%; border-radius:99px;
                                        transition:width 0.5s ease;"></div>
                        </div>
                    </div>
                    <div>
                        <div style="display:flex; justify-content:space-between;
                                    margin-bottom:5px; font-size:13px;">
                            <span>Price Trend</span>
                            <span style="color:#4f46e5; font-weight:600;">{res['trend_score']}%</span>
                        </div>
                        <div style="background:#e2e8f0; height:5px; border-radius:99px;">
                            <div style="background:#4f46e5; width:{res['trend_score']}%;
                                        height:100%; border-radius:99px;
                                        transition:width 0.5s ease;"></div>
                        </div>
                    </div>
                </div>
                """,
                border_color="#16a34a",
            )

    else:
        # Empty state
        with st.container(border=True):
            st.markdown(
                """
                <div style="text-align:center; padding:60px 20px; color:#94a3b8;">
                    <div style="font-size:2.8rem; margin-bottom:14px;">📈</div>
                    <p style="margin:0; font-size:14px; font-weight:600; color:#475569;">
                        Ready for analysis
                    </p>
                    <p style="margin:8px 0 0 0; font-size:13px; color:#94a3b8;">
                        Select a product and click 'Analyse Prices' to see results here
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )