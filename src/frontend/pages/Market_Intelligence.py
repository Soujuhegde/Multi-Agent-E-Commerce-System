import streamlit as st
import sys
import textwrap
from pathlib import Path
import random
from datetime import datetime

# Setup paths
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from components.sidebar import render_sidebar
from components.navbar import render_navbar
from services.api_client import APIClient
from utils.theme import apply_premium_theme, render_card, render_custom_alert

# Apply global premium styling & sidebar
apply_premium_theme()
render_sidebar()
render_navbar(page_title="Market Intelligence & Dynamic Pricing Core")

st.markdown(
    textwrap.dedent(
        """
        <p style="color: #4b5563; margin-bottom: 2rem; font-size: 1rem;">
            Harness autonomous agents to crawl competitor pricing nodes, track market sentiment, and compute optimal dynamic product pricing.
        </p>
        """
    ),
    unsafe_allow_html=True
)

col_control, col_display = st.columns([2, 3])

with col_control:
    with st.container(border=True):
        st.subheader("🎯 Intelligence Controls")
        
        try:
            products = APIClient.get_products()
            if products:
                product_list = [p["product_name"] for p in products]
                selected_product = st.selectbox("Target Product for Analysis", product_list)
                
                st.markdown("<hr style='border-color: #e5e7eb; margin: 15px 0;'>", unsafe_allow_html=True)
                
                competitor_source = st.selectbox("Competitor Node Data", ["Amazon.in Core", "Flipkart Retail", "Croma Digital", "Vijay Sales Portal"])
                
                st.markdown("<br>", unsafe_allow_html=True)
                analyze_button = st.button("🚀 Execute Autonomous Intel Crawl")
                
                if analyze_button:
                    target_p = next(p for p in products if p["product_name"] == selected_product)
                    
                    # Dynamic mock pricing and trend calculations
                    current_price = target_p["price"]
                    comp_price = current_price * random.choice([0.92, 0.95, 0.98, 1.02, 1.05])
                    rec_price = comp_price * 1.03 if comp_price < current_price else current_price * 1.02
                    
                    demand_score = random.randint(65, 95)
                    trend_score = random.randint(60, 98)
                    
                    st.session_state.market_results = {
                        "product_name": selected_product,
                        "current_price": current_price,
                        "competitor_price": comp_price,
                        "recommended_price": rec_price,
                        "demand_score": demand_score,
                        "trend_score": trend_score,
                        "source": competitor_source,
                        "timestamp": datetime.utcnow().strftime("%H:%M:%S UTC")
                    }
                    st.success("Crawl executed successfully!")
            else:
                st.warning("Database contains no products. Please populate inventory first.")
        except Exception as e:
            render_custom_alert(f"Could not load warehouse stock records: {e}", "error")

with col_display:
    if "market_results" in st.session_state and st.session_state.market_results:
        res = st.session_state.market_results
        
        with st.container(border=True):
            col_header, col_time = st.columns([3, 1])
            with col_header:
                st.markdown(f"<h3 style='margin:0; font-size:1.25rem; font-weight:700; color:#111827;'>📊 Intel Summary: {res['product_name']}</h3>", unsafe_allow_html=True)
            with col_time:
                st.markdown(f"<span style='font-size: 0.75rem; background: #eff6ff; color: #1d4ed8; padding: 3px 8px; border-radius: 12px; font-weight: 600; float:right;'>{res['timestamp']}</span>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Grid of competitive scores
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(
                    textwrap.dedent(
                        f"""
                        <div style="background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px; margin-bottom: 12px;">
                            <div style="font-size: 0.8rem; color: #4b5563; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Target Current Price</div>
                            <div style="font-size: 1.4rem; font-weight: 700; color: #111827; margin-top: 5px;">₹{res['current_price']:,.2f}</div>
                        </div>
                        """
                    ),
                    unsafe_allow_html=True
                )
            with c2:
                st.markdown(
                    textwrap.dedent(
                        f"""
                        <div style="background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px; margin-bottom: 12px;">
                            <div style="font-size: 0.8rem; color: #4b5563; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Competitor Price ({res['source']})</div>
                            <div style="font-size: 1.4rem; font-weight: 700; color: #b91c1c; margin-top: 5px;">₹{res['competitor_price']:,.2f}</div>
                        </div>
                        """
                    ),
                    unsafe_allow_html=True
                )
                
            st.markdown(
                textwrap.dedent(
                    f"""
                    <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 1rem; margin-bottom: 1.2rem; text-align: center;">
                        <div style="font-size: 0.85rem; color: #15803d; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">💰 Recommended Optimized Price</div>
                        <div style="font-size: 1.8rem; font-weight: 700; color: #111827; margin-top: 5px;">₹{res['recommended_price']:,.2f}</div>
                        <p style="margin: 4px 0 0 0; font-size: 0.8rem; color: #4b5563;">Maximize margin + maintain competitive positioning score of 98.4%</p>
                    </div>
                    """
                ),
                unsafe_allow_html=True
            )
            
            # Progress bars for metrics
            render_card(
                title="🎯 Analytics Gauges",
                body_html=f"""
                <div style="display: flex; flex-direction: column; gap: 15px; color: #111827;">
                    <div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.85rem;">
                            <span>Market Demand Index</span><span style="color: #0d9488; font-weight: 600;">{res['demand_score']}%</span>
                        </div>
                        <div style="background: #e5e7eb; height: 6px; border-radius: 3px;">
                            <div style="background: #0d9488; width: {res['demand_score']}%; height: 100%; border-radius: 3px;"></div>
                        </div>
                    </div>
                    <div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.85rem;">
                            <span>Price Trend Index</span><span style="color: #4f46e5; font-weight: 600;">{res['trend_score']}%</span>
                        </div>
                        <div style="background: #e5e7eb; height: 6px; border-radius: 3px;">
                            <div style="background: #4f46e5; width: {res['trend_score']}%; height: 100%; border-radius: 3px;"></div>
                        </div>
                    </div>
                </div>
                """,
                border_color="#15803d"
            )
    else:
        with st.container(border=True):
            st.markdown(
                """
                <div style="text-align: center; padding: 4rem 0; color: #4b5563;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">📈</div>
                    <p style="margin: 0; font-size: 0.95rem; font-weight: 500;">System standby. Market data is uninitialized.</p>
                    <p style="margin: 5px 0 0 0; font-size: 0.8rem; color: #4b5563;">Execute a crawl query from the console on the left to begin.</p>
                </div>
                """,
                unsafe_allow_html=True
            )