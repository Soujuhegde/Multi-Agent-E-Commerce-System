import streamlit as st

# ─── Page definitions ────────────────────────────────
_NAV = [
    ("dashboard",    "📊",  "Dashboard",       "/"),
    ("ai_assistant", "💬",  "AI Assistant",    "/Agent_Workflow"),
    ("inventory",    "📦",  "Inventory",       "/Inventory"),
    ("invoice",      "📄",  "Invoices",        "/Invoice"),
    ("market",       "📈",  "Market Insights", "/Market_Intelligence"),
]


def render_topnav(active_page: str = "dashboard"):
    """
    Renders a fixed premium top navigation bar.
    Logo on the left, nav links centred, avatar on the right.
    
    active_page: one of 'dashboard', 'ai_assistant', 'inventory', 'invoice', 'market'
    """
    links = ""
    for key, icon, label, path in _NAV:
        if key == active_page.lower():
            style = (
                "display:inline-flex;align-items:center;gap:5px;"
                "padding:6px 13px;border-radius:8px;text-decoration:none;"
                "font-size:13.5px;font-weight:600;"
                "color:#4f46e5;background:#eef2ff;"
                "border:1px solid rgba(79,70,229,0.2);"
                "white-space:nowrap;font-family:Inter,sans-serif;"
            )
        else:
            style = (
                "display:inline-flex;align-items:center;gap:5px;"
                "padding:6px 13px;border-radius:8px;text-decoration:none;"
                "font-size:13.5px;font-weight:500;"
                "color:#475569;background:transparent;"
                "border:1px solid transparent;"
                "white-space:nowrap;font-family:Inter,sans-serif;"
                "transition:color 0.15s,background 0.15s,border-color 0.15s;"
            )
        links += f'<a href="{path}" style="{style}" target="_self"><span style="font-size:13px">{icon}</span>{label}</a>'

    nav_html = (
        '<nav style="'
        'position:fixed;top:0;left:0;right:0;height:56px;'
        'background:#ffffff;border-bottom:1px solid #e2e8f0;'
        'box-shadow:0 1px 3px rgba(0,0,0,0.06);'
        'display:flex;align-items:center;justify-content:space-between;'
        'padding:0 24px;z-index:9999;box-sizing:border-box;'
        'font-family:Inter,-apple-system,BlinkMacSystemFont,sans-serif;">'
        
        # Brand
        '<a href="/" target="_self" style="'
        'display:flex;align-items:center;gap:8px;'
        'text-decoration:none;color:#0f172a;'
        'font-weight:700;font-size:15px;letter-spacing:-0.3px;'
        'flex-shrink:0;min-width:110px;">'
        '<span style="font-size:14px;line-height:1;">🛒</span>'
        '<span>Aether</span>'
        '</a>'
        
        # Nav links wrapper
        '<div style="display:flex;align-items:center;gap:2px;flex:1;justify-content:center;">'
        + links +
        '</div>'
        
        # Avatar
        '<div style="display:flex;align-items:center;flex-shrink:0;min-width:110px;justify-content:flex-end;">'
        '<span style="'
        'width:26px;height:26px;border-radius:50%;'
        'background:linear-gradient(135deg,#4f46e5 0%,#7c3aed 100%);'
        'display:inline-flex;align-items:center;justify-content:center;'
        'font-size:11px;font-weight:700;color:#fff;cursor:pointer;'
        'box-shadow:0 1px 4px rgba(79,70,229,0.35);'
        'flex-shrink:0;" title="Account">A</span>'
        '</div>'
        
        '</nav>'
    )
    st.markdown(nav_html, unsafe_allow_html=True)


def render_navbar(page_title: str = "Dashboard", subtitle: str = ""):
    """
    Renders the page section header (title + optional subtitle)
    placed directly below the fixed top navbar.
    """
    sub = (
        f'<p style="font-size:13.5px;color:#475569;margin:2px 0 0 0;'
        f'line-height:1.5;font-weight:400;font-family:Inter,sans-serif;">'
        f'{subtitle}</p>'
        if subtitle else ""
    )
    st.markdown(
        f'<div style="margin-top:0 !important;margin-bottom:12px;padding-bottom:10px;'
        f'border-bottom:1px solid #e2e8f0;">'
        f'<h1 style="margin:0 0 2px 0 !important;font-size:18px;font-weight:700;'
        f'color:#0f172a;letter-spacing:-0.4px;line-height:1.3;'
        f'font-family:Inter,sans-serif;">{page_title}</h1>'
        f'{sub}'
        f'</div>',
        unsafe_allow_html=True,
    )