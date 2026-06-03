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
render_topnav("ai_assistant")
render_sidebar()  # no-op

render_navbar(
    page_title="AI Assistant",
    subtitle="Ask anything about your inventory, orders, or pricing. Our AI handles the rest."
)

# ─── Quick Example Chips ────────────────────────────
st.markdown(
    """
    <p style="font-size:12px; color:#475569; font-weight:600;
       text-transform:uppercase; letter-spacing:0.6px; margin-bottom:10px;">
        💡 Try an example
    </p>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3, gap="small")
with c1:
    sug1 = st.button("📦 Check stock for iPhone 15")
with c2:
    sug2 = st.button("📈 Competitor price: Samsung S24")
with c3:
    sug3 = st.button("📄 Draft invoice for Rohan Malhotra")

# Populate textarea if a suggestion was clicked
query_val = ""
if sug1:
    query_val = "Check the stock of iPhone 15"
elif sug2:
    query_val = "Analyze competitor price for Samsung S24"
elif sug3:
    query_val = "Generate an invoice for Rohan Malhotra for Sony WH-1000XM5"

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ─── Input Box ──────────────────────────────────────
with st.container(border=True):
    st.markdown(
        """
        <h3 style="margin:0 0 12px 0; color:#4f46e5; font-size:14px;
                   font-weight:700; letter-spacing:-0.2px;">
            💬 Ask the AI
        </h3>
        """,
        unsafe_allow_html=True,
    )

    query_input = st.text_area(
        "Your question",
        value=query_val,
        placeholder="e.g. 'Create a bill for Aditi' or 'How many MacBook Air M3 are in stock?'",
        key="workflow_query_input",
        height=100,
        label_visibility="collapsed",
    )

    col_run, col_hint = st.columns([1, 5])
    with col_run:
        run_workflow = st.button("▶  Run")
    with col_hint:
        st.markdown(
            "<p style='font-size:12px; color:#94a3b8; margin:8px 0 0 4px;'>"
            "Press Run or hit Ctrl+Enter</p>",
            unsafe_allow_html=True,
        )

# ─── Response ───────────────────────────────────────
if run_workflow and query_input.strip():
    with st.spinner("Processing your request…"):
        try:
            response = APIClient.execute_workflow(query_input)

            if response:
                intent = response.get("intent", "unknown")
                error  = response.get("error", None)

                badge_map = {
                    "inventory": ("Inventory",  "#0d9488", "#f0fdfa", "#99f6e4"),
                    "invoice":   ("Billing",    "#16a34a", "#f0fdf4", "#bbf7d0"),
                    "market":    ("Pricing",    "#7c3aed", "#faf5ff", "#e9d5ff"),
                }
                badge_label, badge_color, badge_bg, badge_border = badge_map.get(
                    intent, ("General", "#475569", "#f8fafc", "#e2e8f0")
                )

                if error:
                    render_custom_alert(f"Something went wrong: {error}", "error")
                else:
                    final_resp = response.get(
                        "final_response",
                        "Your request has been processed successfully."
                    )

                    st.markdown(
                        f"""
                        <div style="
                            background: {badge_bg};
                            border: 1px solid {badge_border};
                            border-left: 4px solid {badge_color};
                            border-radius: 12px;
                            padding: 20px;
                            margin-top: 16px;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
                        ">
                            <div style="display:flex; justify-content:space-between;
                                        align-items:center; margin-bottom:14px;
                                        border-bottom: 1px solid {badge_border};
                                        padding-bottom: 10px;">
                                <div style="display:flex; align-items:center; gap:8px;">
                                    <span style="font-size:16px;">✨</span>
                                    <span style="font-size:13.5px; font-weight:700;
                                                 color:#0f172a; font-family:Inter,sans-serif;">AI Assistant Response</span>
                                </div>
                                <span style="
                                    background:#ffffff; color:{badge_color};
                                    padding:3px 10px; border-radius:20px;
                                    border:1px solid {badge_border};
                                    font-weight:600; font-size:11px;
                                    letter-spacing:0.3px;
                                    font-family:Inter,sans-serif;">
                                    {badge_label} Mode
                                </span>
                            </div>
                            <div style="color:#1e293b; font-size:14px;
                                      line-height:1.8; margin:0; font-family:Inter,sans-serif;
                                      white-space: pre-wrap;">{final_resp}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        except Exception as err:
            render_custom_alert(
                f"Could not process your request. Please try again. ({err})", "error"
            )

elif run_workflow:
    render_custom_alert("Please enter a question or request before running.", "error")