"""
Custom styles for Deadlock & Banker's Algorithm Dashboard
"""
import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    /* Make numeric cells and matrix values easier to read */
    [data-testid="stDataFrame"] [role="gridcell"] { font-size: 19px !important; }
    [data-testid="stDataFrame"] [role="columnheader"] { font-size: 16px !important; }
    [data-testid="stMetricValue"] { font-size: 30px !important; }
    .big-number { font-size: 24px; font-weight: 750; letter-spacing: .3px; }
    .sim-card { border: 1px solid rgba(128,128,128,.35); border-radius: 12px; padding: 12px; margin-bottom: 8px; }
    .sim-title { font-size: 16px; font-weight: 700; }
    .sim-sub { font-size: 13px; opacity: .8; }
    </style>
    """, unsafe_allow_html=True)
