"""
Page 1: Executive Overview & Top Findings
"""

import streamlit as st
import pandas as pd
from src.data_loader import load_raw_data
from src.data_cleaning import clean_survey_data
from components.sidebar import render_sidebar_filters
from components.kpi_cards import render_executive_kpis
from components.insight_cards import render_insight_card, render_responsible_use_disclaimer, render_chart_insight
from src.utils import filter_dataset, format_pct, inject_custom_theme
from src.eda import plot_bivariate_treatment, plot_age_distribution, plot_gender_distribution
from src.insights import generate_executive_insights

st.set_page_config(page_title="Executive Overview | MindTech Insights", page_icon="🧠", layout="wide")
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

st.title("📊 Executive Overview & Key Findings")
st.caption("High-level summary of survey respondents, reported treatment rates, core workplace indicators, and dynamic key findings.")

if len(df_filtered) == 0:
    st.warning("⚠️ No data available matching the selected filter criteria. Please adjust filters.")
    st.stop()

total_n = len(df_filtered)
treatment_pct = (df_filtered['treatment'] == 'Yes').mean() * 100
family_history_pct = (df_filtered['family_history'] == 'Yes').mean() * 100
benefits_pct = (df_filtered['benefits'] == 'Yes').mean() * 100
remote_work_pct = (df_filtered['remote_work'] == 'Yes').mean() * 100
work_interfere_pct = (df_filtered['work_interfere'].isin(['Often', 'Sometimes'])).mean() * 100

metrics = {
    'total_respondents': f"{total_n:,}",
    'treatment_pct': format_pct(treatment_pct),
    'family_history_pct': format_pct(family_history_pct),
    'benefits_pct': format_pct(benefits_pct),
    'remote_work_pct': format_pct(remote_work_pct),
    'work_interfere_pct': format_pct(work_interfere_pct)
}

render_executive_kpis(metrics)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    fig_fh = plot_bivariate_treatment(
        df_filtered, 'family_history',
        "Reported Treatment vs Family History of Mental Illness",
        "Family History"
    )
    st.plotly_chart(fig_fh, use_container_width=True)
    render_chart_insight("Respondents reporting a family history of mental illness show a substantially higher treatment rate.")

with col2:
    fig_wi = plot_bivariate_treatment(
        df_filtered, 'work_interfere',
        "Reported Treatment vs Work Interference Frequency",
        "Work Interference Frequency",
        category_orders={'work_interfere': ['Often', 'Sometimes', 'Rarely', 'Never', 'Unknown']}
    )
    st.plotly_chart(fig_wi, use_container_width=True)
    render_chart_insight("Respondents experiencing frequent work interference report significantly higher rates of seeking treatment.")

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    fig_age = plot_age_distribution(df_filtered)
    st.plotly_chart(fig_age, use_container_width=True)
    render_chart_insight("The survey sample is concentrated primarily among early to mid-career tech workforce respondents (25 - 40 years).")

with col4:
    fig_gen = plot_gender_distribution(df_filtered)
    st.plotly_chart(fig_gen, use_container_width=True)
    render_chart_insight("Normalized gender categories preserve transgender and non-binary representation alongside male and female respondents.")

st.markdown("---")

st.subheader("💡 Key Empirical Findings")
insights = generate_executive_insights(df_filtered)
for ins in insights:
    render_insight_card(
        finding=ins['finding'],
        evidence=ins['evidence'],
        interpretation=ins['interpretation'],
        card_type=ins['card_type']
    )

render_responsible_use_disclaimer()
