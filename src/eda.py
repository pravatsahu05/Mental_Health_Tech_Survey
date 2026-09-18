"""
MindTech Insights — Exploratory Data Analysis (EDA) Module
Generates modern, interactive analytical charts for Demographics, Mental Health,
Workplace Support, Workplace Culture, and Stigma patterns.
"""

from typing import Dict, Any, Optional
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import config


# ==========================================
# 1. DEMOGRAPHICS EDA
# ==========================================

def plot_age_distribution(df: pd.DataFrame) -> go.Figure:
    """Age histogram with KDE density marginal plot and custom hover template."""
    df_valid = df.dropna(subset=['Age_clean'])
    fig = px.histogram(
        df_valid,
        x='Age_clean',
        nbins=25,
        title="<b>Respondent Age Distribution</b>",
        color_discrete_sequence=['#00F2FE'],
        marginal="box",
        labels={'Age_clean': 'Age (Years)'}
    )
    fig.update_traces(hovertemplate="<b>Age Range:</b> %{x} yrs<br><b>Count:</b> %{y}<extra></extra>")
    fig.update_layout(**config.PLOTLY_THEME_CONFIG, height=420)
    return fig


def plot_gender_distribution(df: pd.DataFrame) -> go.Figure:
    """Gender category distribution donut chart with neon color palette."""
    counts = df['Gender_clean'].value_counts().reset_index()
    counts.columns = ['Gender', 'Count']
    
    fig = px.pie(
        counts,
        names='Gender',
        values='Count',
        title="<b>Gender Distribution (Normalized)</b>",
        hole=0.55,
        color='Gender',
        color_discrete_map={
            'Male': '#4FACFE',
            'Female': '#00F2FE',
            'Trans / Non-Binary': '#7F00FF',
            'Other / Unspecified': '#8B949E'
        }
    )
    fig.update_traces(
        textinfo='percent+label',
        hoverinfo='label+value+percent',
        hovertemplate="<b>%{label}</b><br>Respondents: %{value}<br>Share: %{percent}<extra></extra>",
        marker=dict(line=dict(color='#030712', width=2))
    )
    fig.update_layout(**config.PLOTLY_THEME_CONFIG, height=380)
    return fig


def plot_company_size_distribution(df: pd.DataFrame) -> go.Figure:
    """Company size distribution horizontal bar chart with cyan-blue gradient."""
    size_order = ['1-5', '6-25', '26-100', '100-500', '500-1000', 'More than 1000']
    counts = df['no_employees'].value_counts().reindex(size_order).fillna(0).reset_index()
    counts.columns = ['Company_Size', 'Count']
    
    fig = px.bar(
        counts,
        y='Company_Size',
        x='Count',
        orientation='h',
        text='Count',
        title="<b>Respondent Distribution by Company Size</b>",
        color='Count',
        color_continuous_scale=['#4FACFE', '#00F2FE'],
        labels={'Company_Size': 'Number of Employees', 'Count': 'Respondents'}
    )
    fig.update_traces(
        textposition='outside',
        hovertemplate="<b>Company Size:</b> %{y}<br><b>Respondents:</b> %{x}<extra></extra>"
    )
    fig.update_layout(**config.PLOTLY_THEME_CONFIG, height=380, coloraxis_showscale=False)
    return fig


def plot_tech_and_remote(df: pd.DataFrame) -> go.Figure:
    """Side-by-side comparison of Tech Company vs Remote Work status."""
    tech_cnt = df['tech_company'].value_counts(normalize=True).mul(100).round(1)
    remote_cnt = df['remote_work'].value_counts(normalize=True).mul(100).round(1)
    
    data = pd.DataFrame([
        {'Category': 'Tech Company', 'Status': 'Yes', 'Percentage': tech_cnt.get('Yes', 0)},
        {'Category': 'Tech Company', 'Status': 'No', 'Percentage': tech_cnt.get('No', 0)},
        {'Category': 'Remote Work', 'Status': 'Yes', 'Percentage': remote_cnt.get('Yes', 0)},
        {'Category': 'Remote Work', 'Status': 'No', 'Percentage': remote_cnt.get('No', 0)}
    ])
    
    fig = px.bar(
        data,
        x='Category',
        y='Percentage',
        color='Status',
        barmode='group',
        text='Percentage',
        title="<b>Tech Employment & Remote Work Prevalence (%)</b>",
        color_discrete_map={'Yes': '#00F2FE', 'No': '#FF5252'}
    )
    fig.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside',
        hovertemplate="<b>%{x}</b> (%{fullData.name}): %{y:.1f}%<extra></extra>"
    )
    fig.update_layout(**config.PLOTLY_THEME_CONFIG, height=380, yaxis_range=[0, 110])
    return fig


# ==========================================
# 2. MENTAL HEALTH & TREATMENT EDA
# ==========================================

def plot_bivariate_treatment(
    df: pd.DataFrame, 
    group_col: str, 
    title: str, 
    x_label: str,
    category_orders: Optional[Dict[str, list]] = None
) -> go.Figure:
    """
    Modern interactive 100% normalized stacked bar chart or grouped percentage bar chart
    comparing any survey variable against treatment response with custom hover templates.
    """
    ct = pd.crosstab(df[group_col], df['treatment'], normalize='index').mul(100).round(1).reset_index()
    counts = pd.crosstab(df[group_col], df['treatment']).reset_index()
    
    ct_melt = ct.melt(id_vars=group_col, value_vars=['Yes', 'No'], var_name='Treatment', value_name='Percentage')
    counts_melt = counts.melt(id_vars=group_col, value_vars=['Yes', 'No'], var_name='Treatment', value_name='Count')
    
    merged = pd.merge(ct_melt, counts_melt, on=[group_col, 'Treatment'])
    
    fig = px.bar(
        merged,
        x=group_col,
        y='Percentage',
        color='Treatment',
        barmode='group',
        text='Percentage',
        title=f"<b>{title}</b>",
        labels={group_col: x_label, 'Percentage': 'Treatment Response %'},
        color_discrete_map={'Yes': '#00F2FE', 'No': '#8B949E'},
        category_orders=category_orders,
        custom_data=['Count']
    )
    fig.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside',
        hovertemplate="<b>%{x}</b><br>Treatment (%{fullData.name}): <b>%{y:.1f}%</b><br>Sample Count: N=%{customdata[0]}<extra></extra>"
    )
    fig.update_layout(**config.PLOTLY_THEME_CONFIG, height=400, yaxis_range=[0, 115])
    return fig


# ==========================================
# 3. WORKPLACE SUPPORT INDEX
# ==========================================

def calculate_workplace_support_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates composite Workplace Support Index (0 - 100).
    Components:
    - benefits == 'Yes' (+20)
    - care_options == 'Yes' (+20)
    - wellness_program == 'Yes' (+20)
    - seek_help == 'Yes' (+20)
    - anonymity == 'Yes' (+20)
    """
    df_out = df.copy()
    b_score = (df_out['benefits'] == 'Yes').astype(int) * 20
    c_score = (df_out['care_options'] == 'Yes').astype(int) * 20
    w_score = (df_out['wellness_program'] == 'Yes').astype(int) * 20
    s_score = (df_out['seek_help'] == 'Yes').astype(int) * 20
    a_score = (df_out['anonymity'] == 'Yes').astype(int) * 20
    
    df_out['support_index'] = b_score + c_score + w_score + s_score + a_score
    return df_out


def plot_support_index_distribution(df_with_index: pd.DataFrame) -> go.Figure:
    """Histogram & Boxplot of Workplace Support Index."""
    fig = px.histogram(
        df_with_index,
        x='support_index',
        nbins=10,
        title="<b>Workplace Support Index Distribution (Score 0 - 100)</b>",
        color_discrete_sequence=['#00E676'],
        marginal="box",
        labels={'support_index': 'Workplace Support Index'}
    )
    fig.update_traces(hovertemplate="<b>Index Score:</b> %{x}<br><b>Employees:</b> %{y}<extra></extra>")
    fig.update_layout(**config.PLOTLY_THEME_CONFIG, height=400)
    return fig


# ==========================================
# 4. WORKPLACE CULTURE & STIGMA EDA
# ==========================================

def plot_culture_comparison(df: pd.DataFrame) -> go.Figure:
    """
    Perception Comparison: Discussion Comfort with Coworkers vs Supervisor vs Interview.
    """
    coworkers = df['coworkers'].value_counts(normalize=True).mul(100).round(1)
    supervisor = df['supervisor'].value_counts(normalize=True).mul(100).round(1)
    
    comp_df = pd.DataFrame([
        {'Target': 'Coworkers', 'Response': 'Yes', 'Percentage': coworkers.get('Yes', 0)},
        {'Target': 'Coworkers', 'Response': 'Some of them', 'Percentage': coworkers.get('Some of them', 0)},
        {'Target': 'Coworkers', 'Response': 'No', 'Percentage': coworkers.get('No', 0)},
        {'Target': 'Supervisor', 'Response': 'Yes', 'Percentage': supervisor.get('Yes', 0)},
        {'Target': 'Supervisor', 'Response': 'Some of them', 'Percentage': supervisor.get('Some of them', 0)},
        {'Target': 'Supervisor', 'Response': 'No', 'Percentage': supervisor.get('No', 0)}
    ])
    
    fig = px.bar(
        comp_df,
        x='Target',
        y='Percentage',
        color='Response',
        barmode='group',
        text='Percentage',
        title="<b>Comfort Level Discussing Mental Health Issues</b>",
        color_discrete_map={'Yes': '#00E676', 'Some of them': '#FFD600', 'No': '#FF5252'}
    )
    fig.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside',
        hovertemplate="<b>Target: %{x}</b><br>Response (%{fullData.name}): <b>%{y:.1f}%</b><extra></extra>"
    )
    fig.update_layout(**config.PLOTLY_THEME_CONFIG, height=400, yaxis_range=[0, 110])
    return fig


def plot_mental_vs_physical_perceptions(df: pd.DataFrame) -> go.Figure:
    """
    Compares whether mental health is perceived as taken as seriously as physical health.
    """
    mvsp = df['mental_vs_physical'].value_counts().reset_index()
    mvsp.columns = ['Perception', 'Count']
    
    fig = px.bar(
        mvsp,
        x='Perception',
        y='Count',
        text='Count',
        title="<b>Does Employer Take Mental Health as Seriously as Physical Health?</b>",
        color='Perception',
        color_discrete_map={'Yes': '#00E676', 'No': '#FF5252', "Don't know": '#8B949E'},
        labels={'Perception': 'Perception', 'Count': 'Respondents'}
    )
    fig.update_traces(
        textposition='outside',
        hovertemplate="<b>Perception: %{x}</b><br>Respondents: %{y}<extra></extra>"
    )
    fig.update_layout(**config.PLOTLY_THEME_CONFIG, height=380)
    return fig
