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
render_topnav("invoice")
render_sidebar()  # no-op

render_navbar(
    page_title="Invoices & Billing",
    subtitle="Build invoices, calculate taxes, and update stock levels — all in one place."
)

# ─── Session state ────────────────────────────────
if "invoice_cart" not in st.session_state:
    st.session_state.invoice_cart = []
if "invoice_success_data" not in st.session_state:
    st.session_state.invoice_success_data = None

# ═══════════════════════════════════════════════
# Layout: Builder (left) | Cart (right)
# ═══════════════════════════════════════════════
col_builder, col_cart = st.columns([2, 3], gap="large")

# ─── LEFT: Product selector ───────────────────
with col_builder:
    with st.container(border=True):
        st.markdown(
            """
            <h3 style="margin:0 0 16px 0; font-size:14px; font-weight:700;
                       color:#0f172a;">
                📋 Customer &amp; Products
            </h3>
            """,
            unsafe_allow_html=True,
        )

        customer_name = st.text_input(
            "Customer Name",
            placeholder="e.g. Aditi Sharma",
            key="billing_customer",
        )

        st.markdown(
            "<hr style='border:none; border-top:1px solid #e2e8f0; margin:14px 0;'>",
            unsafe_allow_html=True,
        )

        try:
            products = APIClient.get_products()
            if products:
                in_stock = {p["product_name"]: p for p in products if p.get("stock_quantity", 0) > 0}

                if in_stock:
                    selected_name = st.selectbox("Select Product", list(in_stock.keys()))
                    prod = in_stock[selected_name]
                    max_qty = prod.get("stock_quantity", 1)

                    st.markdown(
                        f"""
                        <p style="font-size:12px; color:#0d9488; margin:-2px 0 10px 0; font-weight:500;">
                            In Stock: <strong>{max_qty}</strong>
                            &nbsp;·&nbsp;
                            Price: <strong>₹{prod['price']:,.2f}</strong>
                        </p>
                        """,
                        unsafe_allow_html=True,
                    )

                    selected_qty = st.number_input(
                        "Quantity",
                        min_value=1,
                        max_value=max_qty,
                        value=1,
                    )

                    if st.button("➕  Add to Cart"):
                        existing = [
                            i for i in st.session_state.invoice_cart
                            if i["product_id"] == prod["id"]
                        ]
                        if existing:
                            existing[0]["quantity"] = min(
                                existing[0]["quantity"] + selected_qty, max_qty
                            )
                        else:
                            st.session_state.invoice_cart.append({
                                "product_id":   prod["id"],
                                "product_name": prod["product_name"],
                                "price":        prod["price"],
                                "quantity":     selected_qty,
                            })
                        st.success(f"Added {selected_qty}× '{prod['product_name']}' to cart.")

                else:
                    render_custom_alert("All products are currently out of stock.", "info")
            else:
                render_custom_alert(
                    "No products are available right now. Please add stock first.", "info"
                )
        except Exception as e:
            render_custom_alert(
                f"Could not load products. Please check your connection. ({e})", "error"
            )

# ─── RIGHT: Cart & checkout ───────────────────
with col_cart:
    with st.container(border=True):
        st.markdown(
            """
            <h3 style="margin:0 0 16px 0; font-size:14px; font-weight:700;
                       color:#0f172a;">
                🛒 Cart
            </h3>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.invoice_cart:
            # Build table rows
            table_rows = ""
            subtotal   = 0.0
            for item in st.session_state.invoice_cart:
                row_total  = item["price"] * item["quantity"]
                subtotal  += row_total
                table_rows += f"""
                <tr style="border-bottom:1px solid #f1f5f9;">
                    <td style="padding:9px 0; color:#0f172a; font-size:13px;">{item['product_name']}</td>
                    <td style="padding:9px 0; text-align:center; color:#475569; font-size:13px;">{item['quantity']}</td>
                    <td style="padding:9px 0; text-align:right; color:#475569; font-size:13px;">₹{item['price']:,.2f}</td>
                    <td style="padding:9px 0; text-align:right; color:#4f46e5; font-weight:600; font-size:13px;">₹{row_total:,.2f}</td>
                </tr>
                """

            gst_amount  = subtotal * 0.18
            grand_total = subtotal + gst_amount

            st.markdown(
                f"""
                <table style="width:100%; border-collapse:collapse; margin-bottom:16px;">
                    <thead>
                        <tr style="border-bottom:2px solid #e2e8f0;">
                            <th style="padding-bottom:8px; text-align:left; font-size:11px;
                                       text-transform:uppercase; letter-spacing:0.6px;
                                       color:#475569; font-weight:600;">Product</th>
                            <th style="padding-bottom:8px; text-align:center; font-size:11px;
                                       text-transform:uppercase; letter-spacing:0.6px;
                                       color:#475569; font-weight:600;">Qty</th>
                            <th style="padding-bottom:8px; text-align:right; font-size:11px;
                                       text-transform:uppercase; letter-spacing:0.6px;
                                       color:#475569; font-weight:600;">Unit Price</th>
                            <th style="padding-bottom:8px; text-align:right; font-size:11px;
                                       text-transform:uppercase; letter-spacing:0.6px;
                                       color:#475569; font-weight:600;">Total</th>
                        </tr>
                    </thead>
                    <tbody>{table_rows}</tbody>
                </table>
                <div style="background:#f8fafc; border-radius:10px; padding:14px 16px;
                            border:1px solid #e2e8f0;">
                    <div style="display:flex; justify-content:space-between;
                                font-size:13px; margin-bottom:6px; color:#475569;">
                        <span>Subtotal</span>
                        <span>₹{subtotal:,.2f}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between;
                                font-size:13px; margin-bottom:8px; color:#475569;">
                        <span>GST (18%)</span>
                        <span>₹{gst_amount:,.2f}</span>
                    </div>
                    <hr style="border:none; border-top:1px solid #e2e8f0; margin:8px 0;">
                    <div style="display:flex; justify-content:space-between;
                                font-size:15px; font-weight:700; color:#16a34a;">
                        <span>Grand Total</span>
                        <span>₹{grand_total:,.2f}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col_clear, col_gen = st.columns(2, gap="small")
            with col_clear:
                if st.button("🗑️  Clear Cart"):
                    st.session_state.invoice_cart       = []
                    st.session_state.invoice_success_data = None
                    st.rerun()

            with col_gen:
                if st.button("⚡  Generate Invoice"):
                    if not customer_name.strip():
                        render_custom_alert(
                            "Please enter the customer name to generate an invoice.", "error"
                        )
                    else:
                        try:
                            items_payload = [
                                {"product_id": i["product_id"], "quantity": i["quantity"]}
                                for i in st.session_state.invoice_cart
                            ]
                            res = APIClient.generate_invoice(
                                customer_name=customer_name, items=items_payload
                            )
                            cart_map = {
                                i["product_id"]: i["product_name"]
                                for i in st.session_state.invoice_cart
                            }
                            success_items = [
                                {
                                    "product_name": cart_map.get(
                                        it["product_id"], f"Product #{it['product_id']}"
                                    ),
                                    "quantity": it["quantity"],
                                    "price":    it["unit_price"],
                                }
                                for it in res.get("items", [])
                            ]
                            st.session_state.invoice_success_data = {
                                "invoice_number": res.get("invoice_number"),
                                "customer_name":  res.get("customer_name"),
                                "subtotal":       res.get("total_amount", 0) - res.get("tax_amount", 0),
                                "gst":            res.get("tax_amount", 0),
                                "total":          res.get("total_amount", 0),
                                "date":           datetime.utcnow().strftime("%d %b %Y, %H:%M UTC"),
                                "items":          success_items,
                            }
                            st.session_state.invoice_cart = []
                            st.balloons()
                            st.rerun()
                        except Exception as e:
                            render_custom_alert(
                                f"Could not generate invoice. Please try again. ({e})", "error"
                            )

        else:
            # Empty cart state
            st.markdown(
                """
                <div style="text-align:center; padding:48px 0; color:#94a3b8;">
                    <div style="font-size:2.5rem; margin-bottom:12px;">🛒</div>
                    <p style="margin:0; font-size:14px; font-weight:600; color:#475569;">
                        Your cart is empty
                    </p>
                    <p style="margin:6px 0 0 0; font-size:13px; color:#94a3b8;">
                        Select a product from the left panel to get started
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ═══════════════════════════════════════════════
# Invoice Receipt (after successful generation)
# ═══════════════════════════════════════════════
if st.session_state.invoice_success_data:
    data = st.session_state.invoice_success_data

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    item_rows = "".join(
        f"""
        <tr style="border-bottom:1px solid #f1f5f9;">
            <td style="padding:7px 0; color:#0f172a; font-size:13px;">{it['product_name']}</td>
            <td style="padding:7px 0; text-align:center; color:#475569; font-size:13px;">{it['quantity']}</td>
            <td style="padding:7px 0; text-align:right; color:#0f172a; font-size:13px;">₹{it['price']:,.2f}</td>
        </tr>
        """
        for it in data["items"]
    )

    st.markdown(
        f"""
        <div class="premium-card" style="
            border-top:3px solid #16a34a !important;
            max-width:580px; margin:0 auto; background:#ffffff;
        ">
            <!-- Header -->
            <div style="text-align:center; margin-bottom:24px;">
                <div style="
                    display:inline-flex; align-items:center; justify-content:center;
                    width:44px; height:44px; border-radius:50%;
                    background:#f0fdf4; border:1.5px solid #16a34a;
                    font-size:20px; margin-bottom:12px;">✓</div>
                <h2 style="color:#16a34a; margin:0 0 4px 0; font-size:16px; font-weight:700;">
                    Invoice Generated
                </h2>
                <p style="color:#475569; font-size:12.5px; margin:0;">Aether E-Commerce Platform</p>
            </div>
            <!-- Meta -->
            <div style="font-size:13px; margin-bottom:20px; color:#0f172a;">
                <div style="display:flex; justify-content:space-between;
                            border-bottom:1px solid #f1f5f9; padding-bottom:6px; margin-bottom:6px;">
                    <span style="color:#475569;">Invoice ID</span>
                    <strong>{data['invoice_number']}</strong>
                </div>
                <div style="display:flex; justify-content:space-between;
                            border-bottom:1px solid #f1f5f9; padding-bottom:6px; margin-bottom:6px;">
                    <span style="color:#475569;">Date</span>
                    <span>{data['date']}</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#475569;">Customer</span>
                    <span>{data['customer_name']}</span>
                </div>
            </div>
            <!-- Items table -->
            <table style="width:100%; border-collapse:collapse; margin-bottom:16px;">
                <thead>
                    <tr style="border-bottom:1.5px solid #e2e8f0;">
                        <th style="padding-bottom:7px; text-align:left; font-size:11px;
                                   text-transform:uppercase; letter-spacing:0.5px;
                                   color:#475569; font-weight:600;">Product</th>
                        <th style="padding-bottom:7px; text-align:center; font-size:11px;
                                   text-transform:uppercase; letter-spacing:0.5px;
                                   color:#475569; font-weight:600;">Qty</th>
                        <th style="padding-bottom:7px; text-align:right; font-size:11px;
                                   text-transform:uppercase; letter-spacing:0.5px;
                                   color:#475569; font-weight:600;">Unit Price</th>
                    </tr>
                </thead>
                <tbody>{item_rows}</tbody>
            </table>
            <!-- Totals -->
            <div style="background:#f0fdf4; border-radius:10px; padding:14px 16px;
                        border:1px solid #bbf7d0;">
                <div style="display:flex; justify-content:space-between;
                            font-size:13px; margin-bottom:5px; color:#475569;">
                    <span>Subtotal</span>
                    <span style="color:#0f172a;">₹{data['subtotal']:,.2f}</span>
                </div>
                <div style="display:flex; justify-content:space-between;
                            font-size:13px; margin-bottom:8px; color:#475569;">
                    <span>GST (18%)</span>
                    <span style="color:#0f172a;">₹{data['gst']:,.2f}</span>
                </div>
                <hr style="border:none; border-top:1px solid #bbf7d0; margin:8px 0;">
                <div style="display:flex; justify-content:space-between;
                            font-size:15px; font-weight:700; color:#16a34a;">
                    <span>Grand Total</span>
                    <span>₹{data['total']:,.2f}</span>
                </div>
            </div>
            <p style="text-align:center; font-size:11.5px; color:#94a3b8;
                      margin:16px 0 0 0; letter-spacing:0.3px;">
                ✓ Electronically generated. No physical signature required.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    col_c, col_new = st.columns([3, 1])
    with col_new:
        if st.button("🔄  New Invoice"):
            st.session_state.invoice_success_data = None
            st.rerun()