import pandas as pd
import streamlit as st

def inventory_chart():
    """
    Renders inventory analytics within a custom accessible light-mode container.
    """
    with st.container(border=True):
        st.markdown(
            """
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem;">
                <h4 style="margin: 0; font-size: 1.1rem; font-weight: 700; color: #111827;">📊 Stock Distribution by Category</h4>
                <span style="font-size: 0.75rem; background: #f0fdf4; color: #15803d; padding: 3px 8px; border-radius: 20px; border: 1px solid #bbf7d0; font-weight: 600;">Updated Live</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Render actual data
        data = pd.DataFrame(
            {
                "Category": ["Mobiles", "Laptops", "Accessories", "Tablets"],
                "Stock Level": [120, 40, 200, 75]
            }
        )
        
        # Streamlit chart
        st.bar_chart(
            data.set_index("Category"),
            color="#4f46e5", # Royal Indigo matching --primary
            use_container_width=True
        )