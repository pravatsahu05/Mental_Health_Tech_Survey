"""
MindTech Insights — Advanced Interactive Chart Engine
Renders modern, interactive Plotly charts with custom hover templates,
glowing cyan/purple gradients, Sankey flow diagrams, Radar/Spider charts, and Violin distributions.
"""

from typing import Dict, Any, Optional, List
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import config


# ==========================================
# 1. SANKEY FLOW DIAGRAM
# ==========================================

def plot_sankey_treatment_flow(df: pd.DataFrame) -> go.Figure:
    """
    Renders a multi-stage Sankey Flow Diagram:
    Family History -> Work Interference -> Reported Treatment
    """
    valid = df.dropna(subset=['family_history', 'work_interfere', 'treatment']).copy()
    
    # Stage 1: Family History -> Work Interference
    g1 = valid.groupby(['family_history', 'work_interfere']).size().reset_index(name='count')
    
    # Stage 2: Work Interference -> Treatment
    g2 = valid.groupby(['work_interfere', 'treatment']).size().reset_index(name='count')
    
    # Unique nodes
    nodes = (
        [f"Family History: {v}" for v in valid['family_history'].unique()] +
        [f"Interference: {v}" for v in valid['work_interfere'].unique()] +
        [f"Treatment: {v}" for v in valid['treatment'].unique()]
    )
    node_dict = {name: idx for idx, name in enumerate(nodes)}
    
    source = []
    target = []
    value = []
    
    for _, row in g1.iterrows():
        source.append(node_dict[f"Family History: {row['family_history']}"])
        target.append(node_dict[f"Interference: {row['work_interfere']}"])
        value.append(row['count'])
        
    for _, row in g2.iterrows():
        source.append(node_dict[f"Interference: {row['work_interfere']}"])
        target.append(node_dict[f"Treatment: {row['treatment']}"])
        value.append(row['count'])
        
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=18,
            thickness=20,
            line=dict(color="rgba(0, 242, 254, 0.8)", width=1),
            label=nodes,
            color=["#00F2FE", "#4FACFE", "#7F00FF", "#00E676", "#FFD600", "#FF5252", "#8B949E", "#9C27B0", "#FF9800"][:len(nodes)]
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color="rgba(0, 242, 254, 0.2)"
        )
    )])
    
    fig.update_layout(
        title="<b>Sankey Behavioral Flow:</b> Family History ➔ Work Interference ➔ Reported Treatment",
        **config.PLOTLY_THEME_CONFIG,
        height=450
    )
    return fig


# ==========================================
# 2. WORKPLACE SUPPORT RADAR / SPIDER CHART
# ==========================================

def plot_workplace_support_radar(df: pd.DataFrame) -> go.Figure:
    """
    Renders a Radar / Spider Chart evaluating 5 Workplace Support Dimensions (%).
    """
    categories = ['Benefits Coverage', 'Care Options', 'Wellness Program', 'Seek Help Support', 'Anonymity Protected']
    
    pct_yes = [
        (df['benefits'] == 'Yes').mean() * 100,
        (df['care_options'] == 'Yes').mean() * 100,
        (df['wellness_program'] == 'Yes').mean() * 100,
        (df['seek_help'] == 'Yes').mean() * 100,
        (df['anonymity'] == 'Yes').mean() * 100
    ]
    
    # Close polygon
    categories_closed = categories + [categories[0]]
    pct_yes_closed = pct_yes + [pct_yes[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=pct_yes_closed,
        theta=categories_closed,
        fill='toself',
        name='Positive Support (%)',
        fillcolor='rgba(0, 242, 254, 0.25)',
        line=dict(color='#00F2FE', width=3),
        hovertemplate="<b>%{theta}</b>: %{r:.1f}%<extra></extra>"
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#8B949E")),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#F0F6FC", size=11)),
            bgcolor="rgba(0,0,0,0)"
        ),
        title="<b>Workplace Support Dimensions (Radar Analysis)</b>",
        **config.PLOTLY_THEME_CONFIG,
        height=420
    )

    return fig


# ==========================================
# 3. AGE VIOLIN DISTRIBUTION
# ==========================================

def plot_age_violin_by_treatment(df: pd.DataFrame) -> go.Figure:
    """
    Renders Violin plot comparing Age distribution curves split by Treatment response.
    """
    valid = df.dropna(subset=['Age_clean', 'treatment']).copy()
    
    fig = px.violin(
        valid,
        x='treatment',
        y='Age_clean',
        color='treatment',
        box=True,
        points="all",
        title="<b>Age Distribution & Density Curves by Reported Treatment</b>",
        labels={'treatment': 'Reported Treatment', 'Age_clean': 'Age (Years)'},
        color_discrete_map={'Yes': '#00F2FE', 'No': '#7F00FF'}
    )
    
    fig.update_traces(meanline_visible=True, jitter=0.35, pointpos=-1.8, marker=dict(size=4, opacity=0.6))
    fig.update_layout(**config.PLOTLY_THEME_CONFIG, height=420)
    return fig


# ==========================================
# 4. INTERACTIVE TREEMAP (COMPANY SIZE X TECH X TREATMENT)
# ==========================================

def plot_company_treemap(df: pd.DataFrame) -> go.Figure:
    """
    Renders an Interactive Treemap showing Company Size -> Tech Company -> Treatment Response.
    """
    valid = df.dropna(subset=['no_employees', 'tech_company', 'treatment']).copy()
    valid['Tech_Label'] = valid['tech_company'].apply(lambda x: 'Tech Company' if x == 'Yes' else 'Non-Tech Company')
    valid['Treatment_Label'] = valid['treatment'].apply(lambda x: 'Treatment: Yes' if x == 'Yes' else 'Treatment: No')
    
    fig = px.treemap(
        valid,
        path=['no_employees', 'Tech_Label', 'Treatment_Label'],
        title="<b>Hierarchical Treemap: Company Size ➔ Tech Sector ➔ Treatment</b>",
        color='treatment',
        color_discrete_map={'Yes': '#00F2FE', 'No': '#4FACFE', '(undefined)': '#161B22'}
    )
    
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Respondents: %{value}<br>Share: %{percentParent:.1%}<extra></extra>",
        marker=dict(cornerradius=5)
    )
    fig.update_layout(**config.PLOTLY_THEME_CONFIG, height=450)
    return fig
