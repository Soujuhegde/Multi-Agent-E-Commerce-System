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
render_navbar(page_title="LangGraph Multi-Agent Orchestration Portal")

st.markdown(
    textwrap.dedent(
        """
        <p style="color: #4b5563; margin-bottom: 2rem; font-size: 1rem;">
            Interact with the central AI orchestrator. Watch autonomous agents collaborate, dynamically route intents, and construct solutions.
        </p>
        """
    ),
    unsafe_allow_html=True
)

# Suggested queries for quick interaction
st.markdown("<p style='font-size:0.85rem; color:#4f46e5; font-weight:600; margin-bottom:8px;'>💡 Suggested Scenarios</p>", unsafe_allow_html=True)
c_sug1, c_sug2, c_sug3 = st.columns(3)
with c_sug1:
    sug1 = st.button("📦 'Check stock for iPhone 15'")
with c_sug2:
    sug2 = st.button("📈 'Analyze competitor price for Samsung S24'")
with c_sug3:
    sug3 = st.button("📄 'Draft invoice for Rohan Malhotra'")

# Determine query input value
query_val = ""
if sug1:
    query_val = "Check the stock of iPhone 15"
elif sug2:
    query_val = "Analyze competitor price for Samsung S24"
elif sug3:
    query_val = "Generate an invoice for Rohan Malhotra for Sony WH-1000XM5"

st.markdown("<br>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown(
        """
        <h3 style="margin-top:0; color: #4f46e5; font-weight: 700; font-size: 1.2rem; margin-bottom: 1.2rem;">💬 Prompt Orchestration Terminal</h3>
        """,
        unsafe_allow_html=True
    )
    
    # Render textarea
    query_input = st.text_area("User Request Query", value=query_val, placeholder="Ask something like: 'Generate a sales bill for Aditi' or 'What is the stock level of MacBook Air M3?'", key="workflow_query_input")
    
    st.markdown("<br>", unsafe_allow_html=True)
    col_run, col_clear = st.columns([1, 4])
    with col_run:
        run_workflow = st.button("⚡ Execute Workflow")

if run_workflow and query_input.strip():
    with st.spinner("🧠 Orchestrating Agents (Traversing LangGraph State Node Graph)..."):
        try:
            # Execute actual workflow against backend FastAPI
            response = APIClient.execute_workflow(query_input)
            
            if response:
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader("🛠️ LangGraph Telemetry Pathway")
                
                # Render a gorgeous flowchart showing agent pathing
                intent = response.get("intent", "unknown")
                error = response.get("error", None)
                
                if intent == "inventory":
                    routing_step = "📦 Inventory Agent Active"
                    target_color = "#0d9488"
                    agent_badge = "Inventory Core"
                elif intent == "invoice":
                    routing_step = "📄 Invoice Agent Active"
                    target_color = "#15803d"
                    agent_badge = "Billing Core"
                elif intent == "market":
                    routing_step = "📈 Market Intel Agent Active"
                    target_color = "#b91c1c"
                    agent_badge = "Pricing Core"
                else:
                    routing_step = "⚠️ Unknown Intent"
                    target_color = "#b45309"
                    agent_badge = "Fallback Core"
                    
                st.markdown(
                    textwrap.dedent(
                        f"""
                        <div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin: 2rem 0; flex-wrap: wrap; color: #111827;">
                            <div style="background: #eeebff; border: 1.5px solid #4f46e5; border-radius: 8px; padding: 10px 20px; font-weight: 700; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                                🤵 Concierge Agent<br><span style="font-size:0.75rem; color:#4b5563; font-weight:400;">Classified Intent</span>
                            </div>
                            <div style="font-size: 1.5rem; color: #4f46e5;">➔</div>
                            <div style="background: #ffffff; border: 1.5px solid {target_color}; border-radius: 8px; padding: 10px 20px; font-weight: 700; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                                {routing_step}<br><span style="font-size:0.75rem; color:#4b5563; font-weight:400;">Processed Request</span>
                            </div>
                            <div style="font-size: 1.5rem; color: #4f46e5;">➔</div>
                            <div style="background: #f0fdf4; border: 1.5px solid #15803d; border-radius: 8px; padding: 10px 20px; font-weight: 700; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                                🏁 Process Ended<br><span style="font-size:0.75rem; color:#4b5563; font-weight:400;">State Returned</span>
                            </div>
                        </div>
                        """
                    ),
                    unsafe_allow_html=True
                )
                
                # Check for errors in state
                if error:
                    render_custom_alert(f"Workflow Exception: {error}", "error")
                else:
                    final_resp = response.get("final_response", "Operation successfully processed by agent network.")
                    
                    st.markdown(
                        f"""
                        <div class="premium-card" style="border-top: 3px solid #15803d !important; background: #ffffff;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                                <h3 style="margin: 0; color: #15803d; font-weight: 700;">🔮 Central Agent Orchestrator Response</h3>
                                <span style="background: #f0fdf4; color: #15803d; padding: 4px 10px; border-radius: 20px; border: 1px solid #bbf7d0; font-weight: 600; font-size: 0.75rem;">{agent_badge}</span>
                            </div>
                            <p style="color: #111827; font-size: 1.05rem; line-height: 1.8; margin-bottom: 0;">
                                "{final_resp}"
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    with st.expander("🔍 View Raw Agent State Telemetry"):
                        st.json(response)
                        
        except Exception as err:
            render_custom_alert(f"Failed to communicate with the central agent router: {err}. Please verify the FastAPI backend is running on port 8000.", "error")
elif run_workflow:
    render_custom_alert("Please enter a valid user request query.", "error")