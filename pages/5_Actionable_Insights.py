"""
Page 5: Actionable Insights & Report Data Exporter
"""

import streamlit as st
import pandas as pd
from src.data_loader import load_raw_data
from src.data_cleaning import clean_survey_data
from components.sidebar import render_sidebar_filters
from components.insight_cards import render_insight_card, render_responsible_use_disclaimer
from src.utils import filter_dataset, convert_df_to_csv, inject_custom_theme
from src.insights import generate_executive_insights, generate_actionable_recommendations
from src.statistics import compute_all_chi_square_summary

st.set_page_config(page_title="Actionable Insights | MindTech Insights", page_icon="🧠", layout="wide")
inject_custom_theme()

df_raw = load_raw_data()
df_clean = clean_survey_data(df_raw)

filters = render_sidebar_filters(df_clean)
df_filtered = filter_dataset(
    df_clean,
    country=filters['country'],
    gender=filters['gender'],
    age_range=filters['age_range'],
    company_size=filters['company_size'],
    remote_work=filters['remote_work'],
    tech_company=filters['tech_company'],
    family_history=filters['family_history'],
    work_interfere=filters['work_interfere']
)

st.title("💡 Strategic Recommendations & Report Data Exporter")
st.caption("Synthesizing empirical findings, workplace support gaps, statistical associations, and actionable policy interventions.")

if len(df_filtered) == 0:
    st.warning("⚠️ No data available matching the selected filter criteria.")
    st.stop()

# 1. Strategic Workplace Recommendations
st.subheader("🎯 Actionable Workplace Policy Recommendations")
recs = generate_actionable_recommendations()

for rec in recs:
    st.markdown(
        f"""
        <div class="insight-card info" style="border-left: 4px solid #00F2FE;">
            <div style="font-weight: 700; color: #00F2FE; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;">
                CATEGORY: {rec['category']}
            </div>
            <div style="font-weight: 700; color: #FFFFFF; font-size: 1.1rem; margin-bottom: 6px;">
                {rec['action']}
            </div>
            <div style="color: #C9D1D9; font-size: 0.92rem; line-height: 1.55;">
                {rec['details']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# 2. Export Data & Reports Section
st.subheader("📥 Export Analytics & Report Data")
col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    st.markdown("#### Filtered Dataset Export")
    csv_filtered = convert_df_to_csv(df_filtered)
    st.download_button(
        label="⬇️ Download Filtered CSV Dataset",
        data=csv_filtered,
        file_name="mindtech_filtered_survey_data.csv",
        mime="text/csv"
    )

with col_exp2:
    st.markdown("#### Statistical Associations Export")
    candidate_vars = ['family_history', 'work_interfere', 'care_options', 'benefits', 'wellness_program', 'anonymity', 'Gender_clean']
    stat_summary = compute_all_chi_square_summary(df_filtered, candidate_vars)
    csv_stats = convert_df_to_csv(stat_summary)
    st.download_button(
        label="⬇️ Download Statistical Tests CSV Summary",
        data=csv_stats,
        file_name="mindtech_statistical_summary.csv",
        mime="text/csv"
    )

render_responsible_use_disclaimer()
