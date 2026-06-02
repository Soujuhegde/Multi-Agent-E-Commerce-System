import streamlit as st
from utils.theme import apply_premium_theme

def render_sidebar():
    """
    Renders an extremely minimal, simple, and clean sidebar layout.
    Avoids clutter by letting Streamlit's native navigation take center stage.
    """
    # Apply global premium theme
    apply_premium_theme()

    with st.sidebar:
        # Minimal brand heading
        st.markdown(
            """
            <div style="padding: 1rem 0; margin-bottom: 0.5rem;">
                <h2 style="margin: 0; font-size: 1.3rem; font-weight: 700; color: #111827 !important; letter-spacing: -0.5px;">
                    🛒 Aether Platform
                </h2>
                <p style="margin: 2px 0 0 0; font-size: 0.75rem; color: #4b5563; font-weight: 500;">
                    v1.0.0 • Connected
                </p>
            </div>
            <hr style="border-color: #e5e7eb; margin: 10px 0 15px 0;">
            """, 
            unsafe_allow_html=True
        )
        
        # Streamlit will automatically list pages in the space below this.
        
        # Minimal status indicator placed at the very bottom
        st.markdown(
            """
            <div style="position: absolute; bottom: 20px; left: 0; width: 100%; padding: 0 1rem; box-sizing: border-box;">
                <div style="display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: #4b5563; font-weight: 500;">
                    <span style="background: #15803d; width: 8px; height: 8px; border-radius: 50%;"></span>
                    <span>System Online</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )