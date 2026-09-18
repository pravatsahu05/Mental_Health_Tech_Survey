"""
🧠 MindTech Insights — Mental Health & Workplace Wellbeing Analytics
Main Streamlit Entry Application with Cosmic Glassmorphism UI Theme.
"""

import os
import streamlit as st
import config
from src.utils import inject_custom_theme

# 1. Page Configuration
st.set_page_config(
    page_title="MindTech Insights | Mental Health Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Cosmic Glassmorphism Theme
inject_custom_theme()

# 3. App Cosmic Header Hero Banner
st.markdown(
    """
    <div style="background: rgba(11, 16, 29, 0.70); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(0, 242, 254, 0.4); border-radius: 16px; padding: 28px 32px; margin-bottom: 24px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 0 20px rgba(0, 242, 254, 0.1);">
        <div style="font-size: 0.85rem; font-weight: 700; color: #00F2FE; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 6px;">
            ⚡ ASTRA ANALYTICS — WORKPLACE WELLBEING
        </div>
        <h1 style="margin: 0; color: #FFFFFF; font-size: 2.5rem; font-weight: 800; letter-spacing: -0.02em; display: flex; align-items: center; gap: 14px;">
            🧠 MindTech Insights
        </h1>
        <p style="margin: 8px 0 0 0; color: #8B949E; font-size: 1.1rem;">
            Advanced Mental Health & Workplace Wellbeing Analytics Platform
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    ### 🌌 Welcome to MindTech Insights
    Select an analytics module from the **Sidebar Navigation Bar** to explore:
    - **1. Executive Overview**: Key findings & executive KPIs.
    - **2. Demographics & Geography**: Age, Gender, Tech Status, Company Size, Countries & US States.
    - **3. Workplace Health & Culture**: Behavioral Flow, Treatment, Workplace Support Index & Stigma.
    - **4. Advanced Analytics & ML**: Chi-Square tests, Cramér's V & Logistic Regression Predictor Model.
    - **5. Actionable Insights**: Strategic workplace recommendations & report data exports.
    """
)

# Sidebar Navigation Header
st.sidebar.markdown("### 🧠 MindTech Insights")
st.sidebar.markdown("<div style='color: #00F2FE; font-weight:600; font-size:0.85rem; margin-bottom:12px;'>⚡ COSMIC ANALYTICS ENGINE</div>", unsafe_allow_html=True)
