"""
MindTech Insights — Data Cleaning Pipeline
Standardizes data types, normalizes free-text gender responses, validates age entries,
extracts timestamp features, and generates analysis-ready binary variables.
"""

import numpy as np
import pandas as pd
import streamlit as st


def normalize_gender(gender_str: str) -> str:
    """
    Normalizes messy free-text gender responses into standard analysis buckets
    while preserving non-binary and transgender visibility.
    """
    if pd.isna(gender_str):
        return "Other / Unspecified"
    
    g = str(gender_str).strip().lower()
    
    # Exact / pattern matching
    if g in ['m', 'male', 'male-ish', 'maile', 'cis male', 'mal', 'male (cis)', 'make', 
            'male ', 'man', 'msle', 'mail', 'malr', 'cis man', 'guy (-ish) ^_^']:
        return "Male"
    
    if g in ['f', 'female', 'female ', 'femake', 'cis female', 'woman', 'female (cis)', 
            'femail', 'cis-female/femme', 'woman']:
        return "Female"
    
    if any(k in g for k in ['trans', 'non-binary', 'enby', 'queer', 'fluid', 'genderqueer', 'androgyne', 'agender', 'neuter']):
        return "Trans / Non-Binary"
    
    if 'male' in g and 'female' not in g and 'trans' not in g:
        return "Male"
    if 'female' in g and 'trans' not in g:
        return "Female"

    return "Other / Unspecified"


@st.cache_data(show_spinner=False)
def clean_survey_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs data cleaning pipeline on the survey DataFrame:
    1. Preserves raw fields (Age_raw, Gender_raw).
    2. Cleans Age (valid range: 18 - 100). Invalid ages become NaN.
    3. Normalizes Gender into standard categories.
    4. Parses Timestamp into year, month, day, day_name, and hour.
    5. Fills missing categorical values intelligently ('Unspecified' or 'Don't know').
    6. Constructs binary flags for modeling and statistical analysis.

    Returns:
        pd.DataFrame: Cleaned and enriched dataset.
    """
    cleaned = df.copy()
    
    # 1. Retain raw columns
    cleaned['Age_raw'] = cleaned['Age']
    cleaned['Gender_raw'] = cleaned['Gender']
    
    # 2. Age Cleaning (Valid workforce age range: 18 - 100)
    cleaned['Age_clean'] = pd.to_numeric(cleaned['Age'], errors='coerce')
    cleaned['Age_is_invalid'] = (cleaned['Age_clean'] < 18) | (cleaned['Age_clean'] > 100)
    cleaned.loc[cleaned['Age_is_invalid'], 'Age_clean'] = np.nan
    
    # Age Groups
    age_bins = [17, 25, 35, 45, 55, 100]
    age_labels = ['18-25', '26-35', '36-45', '46-55', '56+']
    cleaned['Age_group'] = pd.cut(cleaned['Age_clean'], bins=age_bins, labels=age_labels)
    
    # 3. Gender Normalization
    cleaned['Gender_clean'] = cleaned['Gender_raw'].apply(normalize_gender)
    
    # 4. Timestamp Feature Extraction
    if 'Timestamp' in cleaned.columns:
        cleaned['Timestamp_dt'] = pd.to_datetime(cleaned['Timestamp'], errors='coerce')
        cleaned['Year'] = cleaned['Timestamp_dt'].dt.year
        cleaned['Month'] = cleaned['Timestamp_dt'].dt.month_name()
        cleaned['Day_of_Week'] = cleaned['Timestamp_dt'].dt.day_name()
        cleaned['Hour'] = cleaned['Timestamp_dt'].dt.hour
    
    # 5. Categorical Cleanup & Missing Value Handling
    if 'self_employed' in cleaned.columns:
        cleaned['self_employed'] = cleaned['self_employed'].fillna('No')
    if 'work_interfere' in cleaned.columns:
        cleaned['work_interfere'] = cleaned['work_interfere'].fillna('Unknown')
    if 'state' in cleaned.columns:
        cleaned['state'] = cleaned['state'].fillna('Not Applicable')
    if 'comments' in cleaned.columns:
        cleaned['comments_present'] = cleaned['comments'].notnull() & (cleaned['comments'] != '')
    else:
        cleaned['comments_present'] = False
    
    # Normalize string columns (strip trailing whitespace)
    str_cols = cleaned.select_dtypes(include='object').columns
    for c in str_cols:
        cleaned[c] = cleaned[c].astype(str).str.strip()
    
    # 6. Binary Variables (Yes=1, No=0, Other=0)
    target_binaries = [
        ('treatment', 'treatment_binary'),
        ('family_history', 'family_history_binary'),
        ('remote_work', 'remote_work_binary'),
        ('tech_company', 'tech_company_binary'),
        ('self_employed', 'self_employed_binary'),
        ('benefits', 'benefits_binary'),
        ('care_options', 'care_options_binary'),
        ('wellness_program', 'wellness_program_binary'),
        ('seek_help', 'seek_help_binary'),
        ('anonymity', 'anonymity_binary'),
        ('obs_consequence', 'obs_consequence_binary')
    ]
    
    for src_col, target_col in target_binaries:
        if src_col in cleaned.columns:
            cleaned[target_col] = (cleaned[src_col] == 'Yes').astype(int)
        else:
            cleaned[target_col] = 0
    
    return cleaned
