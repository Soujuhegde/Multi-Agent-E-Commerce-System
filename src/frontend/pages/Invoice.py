import streamlit as st
import sys
import textwrap
from pathlib import Path
import uuid
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
render_navbar(page_title="Intelligent Billing & Invoice Core")

st.markdown(
    textwrap.dedent(
        """
        <p style="color: #4b5563; margin-bottom: 2rem; font-size: 1rem;">
            Generate compliant tax invoices, calculate GST schedules, and update warehouse stocks automatically on billing.
        </p>
        """
    ),
    unsafe_allow_html=True
)

# Initialize Session State for billing cart
if "invoice_cart" not in st.session_state:
    st.session_state.invoice_cart = []
if "invoice_success_data" not in st.session_state:
    st.session_state.invoice_success_data = None

col_builder, col_cart = st.columns([2, 3])

with col_builder:
    with st.container(border=True):
        st.markdown("<h3 style='margin:0; font-size:1.15rem; font-weight:700; color:#4f46e5;'>📋 Customer & Cart Items</h3>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        customer_name = st.text_input("Customer Full Name", placeholder="e.g. Aditi Sharma", key="billing_customer")
        
        st.markdown("<hr style='border-color: #e5e7eb; margin: 15px 0;'>", unsafe_allow_html=True)
        
        try:
            products = APIClient.get_products()
            if products:
                product_options = {p["product_name"]: p for p in products if p.get("stock_quantity", 0) > 0}
                
                if product_options:
                    selected_prod_name = st.selectbox("Select Product", list(product_options.keys()))
                    prod_data = product_options[selected_prod_name]
                    
                    max_qty = prod_data.get("stock_quantity", 1)
                    st.markdown(f"<p style='color: #0d9488; font-size: 0.8rem; margin: -5px 0 10px 0;'>In Stock: <strong>{max_qty}</strong> | Price: <strong>₹{prod_data['price']:,.2f}</strong></p>", unsafe_allow_html=True)
                    
                    selected_qty = st.number_input("Billing Quantity", min_value=1, max_value=max_qty, value=1)
                    
                    add_item = st.button("➕ Append to Cart")
                    
                    if add_item:
                        existing = [item for item in st.session_state.invoice_cart if item["product_id"] == prod_data["id"]]
                        if existing:
                            existing[0]["quantity"] = min(existing[0]["quantity"] + selected_qty, max_qty)
                        else:
                            st.session_state.invoice_cart.append({
                                "product_id": prod_data["id"],
                                "product_name": prod_data["product_name"],
                                "price": prod_data["price"],
                                "quantity": selected_qty
                            })
                        st.success(f"Added {selected_qty}x '{prod_data['product_name']}' to cart.")
                else:
                    st.warning("All products are currently out of stock.")
            else:
                st.warning("No products available in stock database. Please seed inventory first.")
        except Exception as e:
            render_custom_alert(f"Failed to fetch stock items from database: {e}", "error")

with col_cart:
    with st.container(border=True):
        st.markdown("<h3 style='margin:0; font-size:1.15rem; font-weight:700; color:#0d9488;'>🛒 Active Shopping Cart</h3>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.session_state.invoice_cart:
            table_rows = ""
            subtotal = 0.0
            
            for idx, item in enumerate(st.session_state.invoice_cart):
                row_total = item["price"] * item["quantity"]
                subtotal += row_total
                table_rows += f"""
                <tr style="border-bottom: 1px solid #e5e7eb; font-size: 0.85rem;">
                    <td style="padding: 10px 0; color: #111827;">{item['product_name']}</td>
                    <td style="padding: 10px 0; text-align: center; color: #4b5563;">{item['quantity']}</td>
                    <td style="padding: 10px 0; text-align: right; color: #4b5563;">₹{item['price']:,.2f}</td>
                    <td style="padding: 10px 0; text-align: right; color: #4f46e5; font-weight: 600;">₹{row_total:,.2f}</td>
                </tr>
                """
                
            gst_amount = subtotal * 0.18
            grand_total = subtotal + gst_amount
            
            st.markdown(
                f"""
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 1.5rem;">
                    <thead>
                        <tr style="border-bottom: 2px solid #e5e7eb; font-size: 0.8rem; text-transform: uppercase; color: #111827; text-align: left;">
                            <th style="padding-bottom: 8px;">Product</th>
                            <th style="padding-bottom: 8px; text-align: center;">Qty</th>
                            <th style="padding-bottom: 8px; text-align: right;">Unit Price</th>
                            <th style="padding-bottom: 8px; text-align: right;">Line Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
                
                <div style="background: #f9fafb; border-radius: 8px; padding: 15px; border: 1px dashed #e5e7eb;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 6px; color: #4b5563;">
                        <span>Subtotal:</span>
                        <span>₹{subtotal:,.2f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 6px; color: #4b5563;">
                        <span>GST Schedule (18%):</span>
                        <span>₹{gst_amount:,.2f}</span>
                    </div>
                    <hr style="border-color: #e5e7eb; margin: 8px 0;">
                    <div style="display: flex; justify-content: space-between; font-size: 1.1rem; font-weight: 700; color: #15803d;">
                        <span>Grand Total:</span>
                        <span>₹{grand_total:,.2f}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            col_clear, col_gen = st.columns(2)
            with col_clear:
                clear_cart = st.button("🗑️ Reset Cart")
                if clear_cart:
                    st.session_state.invoice_cart = []
                    st.session_state.invoice_success_data = None
                    st.rerun()
                    
            with col_gen:
                gen_invoice = st.button("⚡ Finalize Billing & Print")
                
                if gen_invoice:
                    if not customer_name.strip():
                        render_custom_alert("Customer Name is required to generate legal tax invoice.", "error")
                    else:
                        try:
                            import requests
                            payload = {
                                "customer_name": customer_name,
                                "items": [
                                    {"product_id": item["product_id"], "quantity": item["quantity"]} 
                                    for item in st.session_state.invoice_cart
                                ]
                            }
                            
                            invoice_id = f"INV-{uuid.uuid4().hex[:8].upper()}"
                            success_data = {
                                "invoice_number": invoice_id,
                                "customer_name": customer_name,
                                "subtotal": subtotal,
                                "gst": gst_amount,
                                "total": grand_total,
                                "date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                                "items": st.session_state.invoice_cart
                            }
                            
                            for item in st.session_state.invoice_cart:
                                requests.put(
                                    f"http://localhost:8000/inventory/update-stock/{item['product_id']}",
                                    params={"quantity": item["quantity"]}
                                )
                                
                            st.session_state.invoice_success_data = success_data
                            st.session_state.invoice_cart = [] # Clear cart
                            st.balloons()
                            st.rerun()
                        except Exception as e:
                            render_custom_alert(f"Failed to submit invoice to backend repository: {e}", "error")
        else:
            st.markdown(
                textwrap.dedent(
                    """
                    <div style="text-align: center; padding: 4rem 0; color: #4b5563;">
                        <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">🛒</div>
                        <p style="margin: 0; font-size: 0.95rem; font-weight: 500;">Your active shopping cart is empty.</p>
                        <p style="margin: 5px 0 0 0; font-size: 0.8rem; color: #4b5563;">Add items from the product builder console on the left.</p>
                    </div>
                    """
                ),
                unsafe_allow_html=True
            )

# Render premium receipt container if generated
if st.session_state.invoice_success_data:
    data = st.session_state.invoice_success_data
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        textwrap.dedent(
            f"""
            <div class="premium-card" style="border-top: 3px solid #15803d !important; max-width: 600px; margin: 0 auto; background: #ffffff;">
                <div style="text-align: center; margin-bottom: 1.5rem;">
                    <span style="font-size: 1.8rem; background: #f0fdf4; padding: 8px 12px; border-radius: 50%; border: 1.5px solid #15803d; color: #15803d;">✓</span>
                    <h3 style="color: #15803d; margin: 15px 0 5px 0; font-weight: 700;">TAX INVOICE GENERATED</h3>
                    <p style="color: #4b5563; font-size: 0.8rem; margin: 0;">Aether Autonomous E-Commerce Network</p>
                </div>
                
                <div style="font-size: 0.85rem; line-height: 1.8; margin-bottom: 1.5rem; color: #111827;">
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #e5e7eb; padding-bottom: 5px; margin-bottom: 5px;">
                        <span style="color: #4b5563;">Invoice ID:</span>
                        <strong style="color: #111827;">{data['invoice_number']}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #e5e7eb; padding-bottom: 5px; margin-bottom: 5px;">
                        <span style="color: #4b5563;">Timestamp:</span>
                        <span style="color: #111827;">{data['date']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #e5e7eb; padding-bottom: 5px; margin-bottom: 5px;">
                        <span style="color: #4b5563;">Client Name:</span>
                        <span style="color: #111827;">{data['customer_name']}</span>
                    </div>
                </div>
                
                <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; margin-bottom: 1.5rem;">
                    <thead>
                        <tr style="border-bottom: 1.5px solid #e5e7eb; color: #111827; text-align: left;">
                            <th style="padding-bottom: 6px;">Product</th>
                            <th style="padding-bottom: 6px; text-align: center;">Qty</th>
                            <th style="padding-bottom: 6px; text-align: right;">Unit Price</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join(f'<tr style="border-bottom: 1px solid #e5e7eb;"><td style="padding: 6px 0; color: #111827;">{item["product_name"]}</td><td style="padding: 6px 0; text-align: center; color: #4b5563;">{item["quantity"]}</td><td style="padding: 6px 0; text-align: right; color: #111827;">₹{item["price"]:,.2f}</td></tr>' for item in data['items'])}
                    </tbody>
                </table>
                
                <div style="background: #f0fdf4; border-radius: 8px; padding: 15px; border: 1px dashed #bbf7d0;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 4px; color: #4b5563;">
                        <span>Subtotal:</span>
                        <span style="color: #111827;">₹{data['subtotal']:,.2f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 4px; color: #4b5563;">
                        <span>GST (18%):</span>
                        <span style="color: #111827;">₹{data['gst']:,.2f}</span>
                    </div>
                    <hr style="border-color: #bbf7d0; margin: 6px 0;">
                    <div style="display: flex; justify-content: space-between; font-size: 1.05rem; font-weight: 700; color: #15803d;">
                        <span>Grand Total:</span>
                        <span style="color: #15803d;">₹{data['total']:,.2f}</span>
                    </div>
                </div>
                
                <p style="text-align: center; font-size: 0.75rem; color: #4b5563; margin-top: 1.5rem; letter-spacing: 0.5px;">
                    ✓ Electronically generated. No physical signature required.
                </p>
            </div>
            """
        ),
        unsafe_allow_html=True
    )
    
    if st.button("🔄 Create New Billing Invoice"):
        st.session_state.invoice_success_data = None
        st.rerun()