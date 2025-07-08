import streamlit as st

def navbar():
    st.markdown("""
        <style>
        .nav-container {
            position: fixed;
            top: 0;
            right: 0;
            background-color: #f9f9f9;
            padding: 10px 30px;
            z-index: 9999;
            border-radius: 0 0 0 12px;
            box-shadow: -2px 2px 5px rgba(0,0,0,0.1);
        }
        .nav-link {
            margin-left: 20px;
            font-size: 16px;
            color: #1c4e80;
            text-decoration: none;
            font-weight: bold;
        }
        .nav-link:hover {
            text-decoration: underline;
            color: #034694;
        }
        </style>
        <div class="nav-container">
            <a class="nav-link" href="/?page=Turkey_main">Turkey_main</a>
            <a class="nav-link" href="/?page=Provinces_main">Provinces_main</a>
            <a class="nav-link" href="/?page=storymaps">storymaps</a>
        </div>
    """, unsafe_allow_html=True)
