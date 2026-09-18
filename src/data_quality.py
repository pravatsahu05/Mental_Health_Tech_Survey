"""
MindTech Insights — Data Quality Analysis Module
Generates comprehensive data quality audit metrics, missing value analyses,
and outlier diagnostics.
"""

from typing import Dict, Any
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import config


def generate_data_quality_report(df_raw: pd.DataFrame, df_clean: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes data quality statistics comparing raw vs cleaned datasets.
    """
    total_rows = len(df_raw)
    total_cols = len(df_raw.columns)
    total_cells = total_rows * total_cols
    
    duplicate_count = df_raw.duplicated().sum()
    missing_cells = df_raw.isnull().sum().sum()
    missing_pct = (missing_cells / total_cells) * 100
    
    missing_by_col = df_raw.isnull().sum()
    missing_pct_by_col = (missing_by_col / total_rows * 100).round(2)
    
    col_quality = pd.DataFrame({
        'Column': df_raw.columns,
        'Dtype': df_raw.dtypes.astype(str),
        'Missing_Count': missing_by_col.values,
        'Missing_Pct': missing_pct_by_col.values,
        'Unique_Values': [df_raw[c].nunique(dropna=True) for c in df_raw.columns]
    }).sort_values(by='Missing_Pct', ascending=False)
    
    # Suspicious numerical values
    invalid_ages = df_clean['Age_is_invalid'].sum()
    
    return {
        'total_rows': total_rows,
        'total_cols': total_cols,
        'total_cells': total_cells,
        'duplicate_count': int(duplicate_count),
        'missing_cells': int(missing_cells),
        'missing_pct': float(round(missing_pct, 2)),
        'col_quality': col_quality,
        'invalid_ages_count': int(invalid_ages),
        'high_missing_cols': col_quality[col_quality['Missing_Pct'] > 10]['Column'].tolist()
    }


def plot_missing_bar(col_quality_df: pd.DataFrame) -> go.Figure:
    """
    Creates a Plotly bar chart showing missing value percentage per column.
    """
    df_missing = col_quality_df[col_quality_df['Missing_Pct'] > 0].copy()
    if df_missing.empty:
        fig = go.Figure()
        fig.add_annotation(text="No missing values in dataset", showarrow=False, font=dict(size=16, color="#00E676"))
        fig.update_layout(**config.PLOTLY_THEME_CONFIG)
        return fig

    fig = px.bar(
        df_missing,
        x='Column',
        y='Missing_Pct',
        text='Missing_Pct',
        title="Missing Values Percentage by Variable (%)",
        color='Missing_Pct',
        color_continuous_scale=['#4FACFE', '#FF5252'],
        labels={'Missing_Pct': 'Missing %', 'Column': 'Survey Column'}
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        **config.PLOTLY_THEME_CONFIG,
        height=380,
        xaxis_tickangle=-45,
        coloraxis_showscale=False
    )
    return fig


def plot_data_types_pie(col_quality_df: pd.DataFrame) -> go.Figure:
    """
    Creates a donut chart of data types present in dataset.
    """
    dtype_counts = col_quality_df['Dtype'].value_counts().reset_index()
    dtype_counts.columns = ['Dtype', 'Count']
    
    fig = px.pie(
        dtype_counts,
        names='Dtype',
        values='Count',
        title="Data Type Distribution",
        hole=0.4,
        color_discrete_sequence=['#00F2FE', '#4FACFE', '#7F00FF']
    )
    fig.update_layout(**config.PLOTLY_THEME_CONFIG, height=350)
    return fig
