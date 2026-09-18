"""
Page 3: Workplace Health, Support & Culture Analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_loader import load_raw_data
from src.data_cleaning import clean_survey_data
from components.sidebar import render_sidebar_filters
from components.insight_cards import render_chart_insight, render_responsible_use_disclaimer
from src.utils import filter_dataset, inject_custom_theme
from src.eda import (
    plot_bivariate_treatment, calculate_workplace_support_index,
    plot_support_index_distribution, plot_culture_comparison,
    plot_mental_vs_physical_perceptions
)
from components.charts import (
    plot_sankey_treatment_flow, plot_workplace_support_radar,
    plot_age_violin_by_treatment
)
import config

st.set_page_config(page_title="Workplace Health & Culture | MindTech Insights", page_icon="🧠", layout="wide")
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

st.title("🩺 Workplace Health, Support & Culture")
st.caption("Comprehensive analysis of treatment patterns, employer support programs, benefit awareness, discussion comfort, and workplace stigma.")

if len(df_filtered) == 0:
    st.warning("⚠️ No data available matching the selected filter criteria.")
    st.stop()

# --- PART A: TREATMENT PATTERNS & BEHAVIORAL FLOW ---
st.subheader("🌊 Behavioral Flow & Treatment Indicators")
fig_sankey = plot_sankey_treatment_flow(df_filtered)
st.plotly_chart(fig_sankey, use_container_width=True)
render_chart_insight("Sankey flow diagram traces how family predisposition and daily work interference translate into reported treatment outcomes.")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    fig1 = plot_bivariate_treatment(
        df_filtered, 'family_history',
        "Treatment Rate by Family History of Mental Illness",
        "Family History"
    )
    st.plotly_chart(fig1, use_container_width=True)
    render_chart_insight("Family history shows a strong positive correlation with reported treatment seeking.")

with col2:
    fig2 = plot_bivariate_treatment(
        df_filtered, 'work_interfere',
        "Treatment Rate by Work Interference Frequency",
        "Work Interference Frequency",
        category_orders={'work_interfere': ['Often', 'Sometimes', 'Rarely', 'Never', 'Unknown']}
    )
    st.plotly_chart(fig2, use_container_width=True)
    render_chart_insight("Work interference frequency is a primary trigger associated with treatment intervention.")

st.markdown("---")

# --- PART B: WORKPLACE SUPPORT INDEX & RADAR ANALYSIS ---
st.subheader("📊 Composite Workplace Support Index & Radar Analysis")
st.markdown(
    """
    > **Index Methodology:**  
    > The **Workplace Support Index (0 - 100)** combines Benefits ($20$), Care Options ($20$), Wellness Programs ($20$), Seeking Help ($20$), and Anonymity ($20$).
    """
)

df_indexed = calculate_workplace_support_index(df_filtered)
avg_score = df_indexed['support_index'].mean()
st.metric("Average Workplace Support Index", f"{avg_score:.1f} / 100")

col_r1, col_r2 = st.columns(2)

with col_r1:
    fig_radar = plot_workplace_support_radar(df_filtered)
    st.plotly_chart(fig_radar, use_container_width=True)
    render_chart_insight("Radar chart highlights relative gaps across benefits, care options, wellness programs, help resources, and anonymity.")

with col_r2:
    fig_index = plot_support_index_distribution(df_indexed)
    st.plotly_chart(fig_index, use_container_width=True)
    render_chart_insight("Distribution of Workplace Support Index scores across respondents.")

st.markdown("---")

# --- PART C: WORKPLACE CULTURE & STIGMA ---
st.subheader("🏛️ Workplace Culture, Discussion Comfort & Stigma")
col_c1, col_c2 = st.columns(2)

with col_c1:
    fig_culture = plot_culture_comparison(df_filtered)
    st.plotly_chart(fig_culture, use_container_width=True)
    render_chart_insight("Respondents show greater willingness to disclose mental health with direct managers than generally with all colleagues.")

with col_c2:
    fig_parity = plot_mental_vs_physical_perceptions(df_filtered)
    st.plotly_chart(fig_parity, use_container_width=True)
    render_chart_insight("Significant proportion of employees feel mental health is not treated with equal seriousness as physical health.")

render_responsible_use_disclaimer()
