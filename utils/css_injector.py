# utils/css_injector.py

import streamlit as st

def inject_global_css():
    st.markdown("""
    <style>
        /* Reduce outer padding around content */
        .block-container {
                padding: 1rem 2rem 1rem 2rem !important;
                max-width: 100% !important;
            }

        /* Hide sidebar if not in use */
        .css-1d391kg, .css-18e3th9 {
                visibility: hidden;
            }

        /* Make the main area use full viewport width */
        .main {
                padding-left: 0rem;
                padding-right: 0rem;
                margin-left: 0rem;
                margin-right: 0rem;
            }

        /* Optional: Force full width of text elements */
        .stMarkdown, .stDataFrame, .stPlotlyChart, .stAltairChart {
            width: 100% !important;
        }

        /* Optional: Prevent overflow clipping */
        html, body, .stApp {
            width: 100%;
            height: 100%;
            overflow-x: hidden;
        }

        /* Optional: Tweak titles for better spacing */
        h1, h2, h3 {
            margin-top: 0.2rem;
            margin-bottom: 0.8rem;
        }
       


        h1 {
            font-size: 24px !important;
            font-weight: 700 !important;
            color: #034694 !important;
            font-family: 'Segoe UI', sans-serif !important;
            margin-top: 0.5rem !important;
            margin-bottom: 1rem !important;
        }

        h2 {
            font-size: 20px !important;
            font-weight: 700 !important;
            color: #1c4e80 !important;
            font-family: 'Segoe UI', sans-serif !important;
            margin-top: 0rem !important;
            margin-bottom: 0rem !important;
        }

        .stMarkdown h2, .stHeading, .stSubheader {
            font-size: 20px !important;
            font-weight: 700 !important;
            color: #1c4e80 !important;
            font-family: 'Segoe UI', sans-serif !important;
        }

        .custom-subheader-icon {
            font-size: 20px;
            font-weight: 700;
            color: #1c4e80;
            font-family: 'Segoe UI', sans-serif;
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 0.3rem;
            margin-bottom: 0.8rem;
        }

        h3 {
            font-size: 20px !important;
            font-weight: 700;
            color: #333333;
            text-align:left;
        }
        </style>
    """, unsafe_allow_html=True)
