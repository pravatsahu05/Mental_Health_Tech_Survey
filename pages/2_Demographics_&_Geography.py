"""
Page 2: Demographics & Geographic Analysis
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
    plot_age_distribution, plot_gender_distribution,
    plot_company_size_distribution, plot_tech_and_remote
)
from components.charts import plot_company_treemap
from src.statistics import calculate_proportion_confidence_interval
import config

st.set_page_config(page_title="Demographics & Geography | MindTech Insights", page_icon="🧠", layout="wide")
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

st.title("👥 Demographics & Geographic Analytics")
st.caption("Detailed demographic profiling and regional analysis across age, gender, company size, tech sector status, countries, and US states.")

if len(df_filtered) == 0:
    st.warning("⚠️ No data available matching the selected filter criteria.")
    st.stop()

# --- PART A: DEMOGRAPHICS ---
st.subheader("📋 Demographic Breakdown")
col1, col2 = st.columns(2)

with col1:
    fig_age = plot_age_distribution(df_filtered)
    st.plotly_chart(fig_age, use_container_width=True)
    render_chart_insight("Age distribution centers around median age 31 years.")

with col2:
    fig_gen = plot_gender_distribution(df_filtered)
    st.plotly_chart(fig_gen, use_container_width=True)
    render_chart_insight("Standardized gender categories preserve diverse identity visibility.")

st.markdown("---")

st.subheader("🌳 Hierarchical Sector & Size Treemap")
fig_tree = plot_company_treemap(df_filtered)
st.plotly_chart(fig_tree, use_container_width=True)
render_chart_insight("Interactive treemap reveals respondent density across organization scale and tech vs non-tech sectors.")

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    fig_size = plot_company_size_distribution(df_filtered)
    st.plotly_chart(fig_size, use_container_width=True)
    render_chart_insight("Survey includes balanced representation across small startups to enterprise corporations.")

with col4:
    fig_tech = plot_tech_and_remote(df_filtered)
    st.plotly_chart(fig_tech, use_container_width=True)
    render_chart_insight("High concentration of technology company employees and remote work participants.")

st.markdown("---")

# --- PART B: GEOGRAPHIC ANALYSIS ---
st.subheader("🌍 Geographic Analytics")
st.markdown("### ⚙️ Geographic Sample Size Filter")
min_sample_size = st.slider(
    "Configurable Minimum Sample Size Threshold (N)",
    min_value=5,
    max_value=100,
    value=config.MIN_GEO_SAMPLE_SIZE,
    step=5,
    help="Countries or States with fewer respondents than this threshold will be filtered out to prevent statistical distortion."
)

country_grouped = df_filtered.groupby('Country').agg(
    Total_Respondents=('treatment', 'count'),
    Treatment_Yes=('treatment', lambda x: (x == 'Yes').sum())
).reset_index()

country_grouped['Treatment_Rate_%'] = (country_grouped['Treatment_Yes'] / country_grouped['Total_Respondents'] * 100).round(1)
valid_countries = country_grouped[country_grouped['Total_Respondents'] >= min_sample_size].sort_values(by='Treatment_Rate_%', ascending=False)

if len(valid_countries) == 0:
    st.info(f"No countries meet the minimum sample threshold of N >= {min_sample_size}. Try reducing the threshold slider.")
else:
    cis = [calculate_proportion_confidence_interval(row['Treatment_Yes'], row['Total_Respondents']) for _, row in valid_countries.iterrows()]
    valid_countries['CI_Lower_%'] = [ci[1] for ci in cis]
    valid_countries['CI_Upper_%'] = [ci[2] for ci in cis]

    col_c1, col_c2 = st.columns([3, 2])

    with col_c1:
        fig_country = px.bar(
            valid_countries,
            y='Country',
            x='Treatment_Rate_%',
            orientation='h',
            text='Treatment_Rate_%',
            title=f"<b>Ranked Country Treatment Rates (Min N >= {min_sample_size})</b>",
            labels={'Treatment_Rate_%': 'Reported Treatment %', 'Country': 'Country'},
            color='Treatment_Rate_%',
            color_continuous_scale=['#4FACFE', '#00F2FE'],
            hover_data=['Total_Respondents', 'CI_Lower_%', 'CI_Upper_%']
        )
        fig_country.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_country.update_layout(**config.PLOTLY_THEME_CONFIG, height=420, coloraxis_showscale=False)
        st.plotly_chart(fig_country, use_container_width=True)
        render_chart_insight("National healthcare policies and public insurance coverage strongly influence employer-provided benefit expectations.")

    with col_c2:
        st.markdown(f"#### 📊 Validated Country Summary Table (N >= {min_sample_size})")
        st.dataframe(
            valid_countries[['Country', 'Total_Respondents', 'Treatment_Rate_%', 'CI_Lower_%', 'CI_Upper_%']],
            use_container_width=True,
            hide_index=True
        )

st.markdown("---")

st.subheader("🇺🇸 US State Breakdown")
us_df = df_filtered[(df_filtered['Country'] == 'United States') & (df_filtered['state'] != 'Not Applicable')]

if len(us_df) > 0:
    state_grouped = us_df.groupby('state').agg(
        Total_Respondents=('treatment', 'count'),
        Treatment_Yes=('treatment', lambda x: (x == 'Yes').sum())
    ).reset_index()

    state_grouped['Treatment_Rate_%'] = (state_grouped['Treatment_Yes'] / state_grouped['Total_Respondents'] * 100).round(1)
    valid_states = state_grouped[state_grouped['Total_Respondents'] >= 5].sort_values(by='Treatment_Rate_%', ascending=False)
    
    col_s1, col_s2 = st.columns([3, 2])

    with col_s1:
        fig_state = px.bar(
            valid_states.head(15),
            x='state',
            y='Treatment_Rate_%',
            text='Treatment_Rate_%',
            title="<b>Top US States by Treatment Seeking Rate (Min N >= 5)</b>",
            labels={'state': 'US State Code', 'Treatment_Rate_%': 'Reported Treatment %'},
            color='Treatment_Rate_%',
            color_continuous_scale=['#4FACFE', '#00F2FE'],
            hover_data=['Total_Respondents']
        )
        fig_state.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_state.update_layout(**config.PLOTLY_THEME_CONFIG, height=400, coloraxis_showscale=False)
        st.plotly_chart(fig_state, use_container_width=True)
        render_chart_insight("State-level variations reflect local tech hub concentration and regional benefit practices.")

    with col_s2:
        st.markdown("#### 📊 US State Data Table")
        st.dataframe(
            valid_states[['state', 'Total_Respondents', 'Treatment_Rate_%']],
            use_container_width=True,
            hide_index=True
        )

render_responsible_use_disclaimer()
