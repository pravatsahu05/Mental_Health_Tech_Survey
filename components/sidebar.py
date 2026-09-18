"""
MindTech Insights — Sidebar UI Component
Renders interactive filter controls and populates Streamlit session state.
"""

from typing import Dict, Any
import pandas as pd
import streamlit as st


def render_sidebar_filters(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Renders the global sidebar filter UI with multi-selects and a reset button.

    Returns:
        Dict: Selected filter values.
    """
    st.sidebar.markdown("### 🎛️ Filter Controls")
    
    if st.sidebar.button("🔄 Reset Filters"):
        st.session_state.clear()
        st.rerun()

    # Country Multiselect
    all_countries = sorted(df['Country'].dropna().unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "Country",
        options=['All'] + all_countries,
        default=['All'],
        key='filter_country'
    )
    
    # Gender Multiselect
    all_genders = sorted(df['Gender_clean'].dropna().unique().tolist())
    selected_genders = st.sidebar.multiselect(
        "Gender Category",
        options=['All'] + all_genders,
        default=['All'],
        key='filter_gender'
    )
    
    # Age Range Slider
    min_age_val = int(df['Age_clean'].min()) if not pd.isna(df['Age_clean'].min()) else 18
    max_age_val = int(df['Age_clean'].max()) if not pd.isna(df['Age_clean'].max()) else 75
    selected_age = st.sidebar.slider(
        "Age Range",
        min_value=18,
        max_value=max(max_age_val, 75),
        value=(18, max(max_age_val, 75)),
        key='filter_age'
    )
    
    # Company Size Multiselect
    size_order = ['1-5', '6-25', '26-100', '100-500', '500-1000', 'More than 1000']
    all_sizes = [s for s in size_order if s in df['no_employees'].unique()]
    selected_sizes = st.sidebar.multiselect(
        "Company Size",
        options=['All'] + all_sizes,
        default=['All'],
        key='filter_size'
    )
    
    # Remote Work Multiselect
    selected_remote = st.sidebar.multiselect(
        "Remote Work",
        options=['All', 'Yes', 'No'],
        default=['All'],
        key='filter_remote'
    )
    
    # Tech Company Multiselect
    selected_tech = st.sidebar.multiselect(
        "Tech Company",
        options=['All', 'Yes', 'No'],
        default=['All'],
        key='filter_tech'
    )

    # Family History Multiselect
    selected_family = st.sidebar.multiselect(
        "Family History",
        options=['All', 'Yes', 'No'],
        default=['All'],
        key='filter_family'
    )

    # Work Interference Multiselect
    all_wi = sorted(df['work_interfere'].unique().tolist())
    selected_wi = st.sidebar.multiselect(
        "Work Interference",
        options=['All'] + all_wi,
        default=['All'],
        key='filter_wi'
    )

    return {
        'country': selected_countries,
        'gender': selected_genders,
        'age_range': selected_age,
        'company_size': selected_sizes,
        'remote_work': selected_remote,
        'tech_company': selected_tech,
        'family_history': selected_family,
        'work_interfere': selected_wi
    }
