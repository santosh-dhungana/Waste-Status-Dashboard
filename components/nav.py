import streamlit as st

def navigation():
    st.sidebar.markdown("""
        <style>
        .nav-title {
            font-weight: 700;
            font-size: 16px;
            color: #1c4e80;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
            margin-bottom: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar.expander("📊 Dashboard", expanded=True):
        st.markdown('<div class="nav-title">Dashboard</div>', unsafe_allow_html=True)
        page = st.radio("", ["Main Page", "Province Page"], key="dashboard_nav")

    with st.sidebar.expander("🗺️ Story Maps", expanded=False):
        st.markdown('<div class="nav-title">Story Maps</div>', unsafe_allow_html=True)
        st.radio("", ["Story Maps"], key="storymap_nav")

    # Routing logic (simplified)
    selected = st.session_state.get("dashboard_nav") or st.session_state.get("storymap_nav")
    st.write(f"👉 You selected: {selected}")
    return selected