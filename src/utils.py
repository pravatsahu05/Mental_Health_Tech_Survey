"""
MindTech Insights — Dynamic Helper Utilities
Filtering, formatting, data exporting, sample size safety helpers, and CSS theme injection.
"""

import os
from typing import Dict, Any, List
import pandas as pd
import streamlit as st
import config


def inject_custom_theme():
    """
    Injects cosmic glassmorphism style.css into the active Streamlit page.
    Ensures seamless application-wide visual styling including the sidebar navbar.
    """
    if os.path.exists(config.STYLE_CSS_PATH):
        with open(config.STYLE_CSS_PATH, 'r', encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def filter_dataset(
    df: pd.DataFrame,
    country: List[str] = None,
    gender: List[str] = None,
    age_range: tuple = (18, 100),
    company_size: List[str] = None,
    remote_work: List[str] = None,
    tech_company: List[str] = None,
    family_history: List[str] = None,
    treatment: List[str] = None,
    work_interfere: List[str] = None
) -> pd.DataFrame:
    """
    Applies global sidebar filter criteria dynamically to the cleaned dataset.
    """
    filtered = df.copy()
    
    if country and len(country) > 0 and 'All' not in country:
        filtered = filtered[filtered['Country'].isin(country)]
        
    if gender and len(gender) > 0 and 'All' not in gender:
        filtered = filtered[filtered['Gender_clean'].isin(gender)]
        
    if age_range and len(age_range) == 2:
        min_age, max_age = age_range
        filtered = filtered[
            (filtered['Age_clean'] >= min_age) & (filtered['Age_clean'] <= max_age) | (filtered['Age_clean'].isna())
        ]
        
    if company_size and len(company_size) > 0 and 'All' not in company_size:
        filtered = filtered[filtered['no_employees'].isin(company_size)]
        
    if remote_work and len(remote_work) > 0 and 'All' not in remote_work:
        filtered = filtered[filtered['remote_work'].isin(remote_work)]
        
    if tech_company and len(tech_company) > 0 and 'All' not in tech_company:
        filtered = filtered[filtered['tech_company'].isin(tech_company)]
        
    if family_history and len(family_history) > 0 and 'All' not in family_history:
        filtered = filtered[filtered['family_history'].isin(family_history)]
        
    if treatment and len(treatment) > 0 and 'All' not in treatment:
        filtered = filtered[filtered['treatment'].isin(treatment)]
        
    if work_interfere and len(work_interfere) > 0 and 'All' not in work_interfere:
        filtered = filtered[filtered['work_interfere'].isin(work_interfere)]
        
    return filtered


def format_pct(val: float) -> str:
    """Formats float to 1-decimal percentage string."""
    return f"{val:.1f}%"


def check_sample_size_warning(n: int, min_threshold: int = 20) -> str:
    """Returns sample size warning text if below threshold."""
    if n < min_threshold:
        return f"⚠️ **Small sample warning (N={n})**: Interpret metrics with extreme caution."
    return ""


def convert_df_to_csv(df: pd.DataFrame) -> bytes:
    """Converts DataFrame to UTF-8 CSV bytes for Streamlit download button."""
    return df.to_csv(index=False).encode('utf-8')
