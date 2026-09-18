"""
MindTech Insights — KPI Cards Component
Renders styled glassmorphism KPI cards for Streamlit pages.
"""

from typing import Dict
import streamlit as st


def render_kpi_card(title: str, value: str, subtitle: str = ""):
    """
    Renders a glassmorphic metric card using HTML/CSS.
    """
    html_code = f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        {"<div class='kpi-subtitle'>" + subtitle + "</div>" if subtitle else ""}
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)


def render_executive_kpis(metrics: Dict[str, str]):
    """
    Renders 6 executive overview KPI cards across two columns.
    """
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        render_kpi_card("Respondents", metrics.get('total_respondents', '0'))
    with col2:
        render_kpi_card("Treatment %", metrics.get('treatment_pct', '0.0%'))
    with col3:
        render_kpi_card("Family History", metrics.get('family_history_pct', '0.0%'))
    with col4:
        render_kpi_card("Benefits Available", metrics.get('benefits_pct', '0.0%'))
    with col5:
        render_kpi_card("Remote Work", metrics.get('remote_work_pct', '0.0%'))
    with col6:
        render_kpi_card("Work Interference", metrics.get('work_interfere_pct', '0.0%'))
