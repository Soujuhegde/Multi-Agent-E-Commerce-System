import streamlit as st

def render_metrics():
    """
    Renders highly customized glassmorphic metric cards with clean borders and high contrast.
    """
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="premium-card" style="border-top: 3px solid #4f46e5 !important; padding: 1rem !important; margin-bottom: 0 !important; text-align: center; background: #ffffff;">
                <div style="font-size: 1.5rem; margin-bottom: 3px;">📦</div>
                <div style="font-size: 0.8rem; text-transform: uppercase; color: #4b5563; letter-spacing: 0.5px; font-weight: 600;">Active Products</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #111827; margin-top: 2px;">120</div>
                <div style="font-size: 0.75rem; color: #15803d; margin-top: 2px; font-weight: 500;">✓ Synced</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="premium-card" style="border-top: 3px solid #0d9488 !important; padding: 1rem !important; margin-bottom: 0 !important; text-align: center; background: #ffffff;">
                <div style="font-size: 1.5rem; margin-bottom: 3px;">📄</div>
                <div style="font-size: 0.8rem; text-transform: uppercase; color: #4b5563; letter-spacing: 0.5px; font-weight: 600;">Invoices</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #111827; margin-top: 2px;">54</div>
                <div style="font-size: 0.75rem; color: #15803d; margin-top: 2px; font-weight: 500;">↑ 12% Weekly</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="premium-card" style="border-top: 3px solid #15803d !important; padding: 1rem !important; margin-bottom: 0 !important; text-align: center; background: #ffffff;">
                <div style="font-size: 1.5rem; margin-bottom: 3px;">₹</div>
                <div style="font-size: 0.8rem; text-transform: uppercase; color: #4b5563; letter-spacing: 0.5px; font-weight: 600;">Stock Value</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #111827; margin-top: 2px;">8.5L</div>
                <div style="font-size: 0.75rem; color: #0d9488; margin-top: 2px; font-weight: 500;">Optimal stock limits</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            """
            <div class="premium-card" style="border-top: 3px solid #b91c1c !important; padding: 1rem !important; margin-bottom: 0 !important; text-align: center; background: #ffffff;">
                <div style="font-size: 1.5rem; margin-bottom: 3px;">📈</div>
                <div style="font-size: 0.8rem; text-transform: uppercase; color: #4b5563; letter-spacing: 0.5px; font-weight: 600;">Market Score</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #111827; margin-top: 2px;">87<span style="font-size: 1.1rem; color: #4b5563;">/100</span></div>
                <div style="font-size: 0.75rem; color: #15803d; margin-top: 2px; font-weight: 500;">★ High Demand</div>
            </div>
            """,
            unsafe_allow_html=True
        )