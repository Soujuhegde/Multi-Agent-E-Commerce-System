import os
import streamlit as st
import textwrap


def apply_premium_theme():
    """
    Reads the custom styles.css file and injects it directly into the Streamlit app.
    Called once at the top of every page before any other rendering.
    """
    css_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "assets",
        "styles.css",
    )
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        # Minimal fallback
        st.markdown(
            "<style>.stApp { background:#f8fafc; color:#0f172a; }</style>",
            unsafe_allow_html=True,
        )


def render_card(title: str, body_html: str, border_color: str = "#e2e8f0"):
    """
    Renders a premium card with a coloured top-border accent.

    Args:
        title:        Card heading text (plain string, may include emoji).
        body_html:    Inner HTML for the card body.
        border_color: CSS colour for the 3px top accent strip.
    """
    cleaned = "\n".join(line.strip() for line in body_html.strip().splitlines())
    html = f"""
<div class="premium-card" style="border-top:3px solid {border_color} !important;">
    <h3 style="margin:0 0 14px 0; font-size:14px; font-weight:700;
               color:#0f172a; letter-spacing:-0.2px;">
        {title}
    </h3>
    <div style="color:#475569; line-height:1.65; font-size:13.5px;">
        {cleaned}
    </div>
</div>"""
    st.markdown(html, unsafe_allow_html=True)


def render_custom_alert(message: str, alert_type: str = "success"):
    """
    Renders a contextual alert banner.

    Args:
        message:    Plain-text or minimal HTML message.
        alert_type: One of 'success', 'error', 'info'.
    """
    icon_map = {"success": "✓", "error": "⚠", "info": "ℹ"}
    icon = icon_map.get(alert_type, "ℹ")
    html = f"""
<div class="custom-alert custom-alert-{alert_type}">
    <span style="font-size:15px; flex-shrink:0;">{icon}</span>
    <span>{message}</span>
</div>"""
    st.markdown(html, unsafe_allow_html=True)


# ── Legacy — kept for import compatibility ───────────
def render_header(title: str, subtitle: str = ""):
    """Deprecated. Use render_navbar() from components.navbar instead."""
    sub = (
        f'<p style="color:#475569; font-size:13.5px; margin:2px 0 16px 0;">{subtitle}</p>'
        if subtitle else ""
    )
    st.markdown(
        f'<div style="margin-bottom:20px; border-bottom:1px solid #e2e8f0; padding-bottom:16px;">'
        f'<h1 style="margin:0; font-size:18px; font-weight:700; color:#0f172a;">{title}</h1>'
        f'{sub}</div>',
        unsafe_allow_html=True,
    )
