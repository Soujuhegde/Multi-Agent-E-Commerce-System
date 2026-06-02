import os
import streamlit as st
import textwrap

def apply_premium_theme():
    """
    Reads the custom styles.css file and injects it directly into the Streamlit app.
    """
    css_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "assets",
        "styles.css"
    )
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        # Fallback in case path resolution is tricky
        st.markdown(
            textwrap.dedent("""
            <style>
            .stApp {
                background-color: #ffffff !important;
                color: #111827 !important;
            }
            </style>
            """),
            unsafe_allow_html=True
        )

def render_header(title: str, subtitle: str = ""):
    """
    Renders an eye-catching premium header using custom dark high-contrast typography.
    """
    subtitle_html = f'<p class="caption-text" style="color: #4b5563 !important; font-size: 0.95rem; line-height: 1.6; margin-top: 4px; margin-bottom: 1.5rem;">{subtitle}</p>' if subtitle else ''
    html = f"""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="margin: 0; font-weight: 700; font-size: 2rem; color: #111827 !important;">{title}</h1>
        {subtitle_html}
    </div>
    """
    st.markdown(textwrap.dedent(html), unsafe_allow_html=True)

def render_card(title: str, body_html: str, border_color: str = "#e5e7eb"):
    """
    Generates a premium light glassmorphic container for display cards.
    """
    html = f"""
    <div class="premium-card" style="border-top: 3px solid {border_color} !important; background: #ffffff !important;">
        <h3 style="margin-top: 0; margin-bottom: 0.8rem; font-weight: 700; color: #111827 !important;">{title}</h3>
        <div style="color: #4b5563 !important; line-height: 1.6; font-size: 0.95rem;">
            {textwrap.dedent(body_html)}
        </div>
    </div>
    """
    st.markdown(textwrap.dedent(html), unsafe_allow_html=True)

def render_custom_alert(message: str, alert_type: str = "success"):
    """
    Renders custom styled high-contrast success, error, or info alerts.
    """
    icon_map = {
        "success": "✓",
        "error": "⚠️",
        "info": "ℹ"
    }
    icon = icon_map.get(alert_type, "ℹ")
    html = f"""
    <div class="custom-alert custom-alert-{alert_type}">
        <span style="font-size: 1.2rem; margin-right: 0.6rem; font-weight: 700;">{icon}</span>
        <span style="font-size: 0.95rem; font-weight: 500;">{message}</span>
    </div>
    """
    st.markdown(textwrap.dedent(html), unsafe_allow_html=True)
