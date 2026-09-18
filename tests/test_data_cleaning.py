"""
Unit Tests for Data Cleaning & Normalization Pipeline
"""

import numpy as np
import pandas as pd
import pytest
from src.data_cleaning import normalize_gender, clean_survey_data


def test_normalize_gender():
    assert normalize_gender('Male') == 'Male'
    assert normalize_gender('m') == 'Male'
    assert normalize_gender('cis male') == 'Male'
    assert normalize_gender('Female') == 'Female'
    assert normalize_gender('f') == 'Female'
    assert normalize_gender('cis female') == 'Female'
    assert normalize_gender('Trans-female') == 'Trans / Non-Binary'
    assert normalize_gender('non-binary') == 'Trans / Non-Binary'
    assert normalize_gender('fluid') == 'Trans / Non-Binary'
    assert normalize_gender(None) == 'Other / Unspecified'


def test_age_cleaning():
    df_raw = pd.DataFrame({
        'Timestamp': ['2014-08-27 11:29:31', '2014-08-27 11:29:37', '2014-08-27 11:29:44'],
        'Age': [37, -29, 99999999999],
        'Gender': ['Female', 'M', 'Male'],
        'Country': ['United States', 'United States', 'Canada'],
        'self_employed': [None, None, 'No'],
        'family_history': ['No', 'No', 'No'],
        'treatment': ['Yes', 'No', 'No'],
        'work_interfere': ['Often', 'Rarely', 'Rarely'],
        'no_employees': ['6-25', 'More than 1000', '6-25'],
        'remote_work': ['No', 'No', 'No'],
        'tech_company': ['Yes', 'No', 'Yes'],
        'benefits': ['Yes', "Don't know", 'No'],
        'care_options': ['Not sure', 'No', 'No'],
        'wellness_program': ['No', "Don't know", 'No'],
        'seek_help': ['Yes', "Don't know", 'No'],
        'anonymity': ['Yes', "Don't know", "Don't know"],
        'leave': ['Somewhat easy', "Don't know", 'Somewhat difficult'],
        'mental_health_consequence': ['No', 'Maybe', 'No'],
        'phys_health_consequence': ['No', 'No', 'No'],
        'coworkers': ['Some of them', 'No', 'Yes'],
        'supervisor': ['Yes', 'No', 'Yes'],
        'mental_health_interview': ['No', 'No', 'Yes'],
        'phys_health_interview': ['Maybe', 'No', 'Yes'],
        'mental_vs_physical': ['Yes', "Don't know", 'No'],
        'obs_consequence': ['No', 'No', 'No'],
        'comments': [None, None, None]
    })
    
    df_clean = clean_survey_data(df_raw)
    
    # Check valid age preserved
    assert df_clean.loc[0, 'Age_clean'] == 37
    # Check invalid ages converted to NaN
    assert pd.isna(df_clean.loc[1, 'Age_clean'])
    assert pd.isna(df_clean.loc[2, 'Age_clean'])
    
    # Check binary flags
    assert df_clean.loc[0, 'treatment_binary'] == 1
    assert df_clean.loc[1, 'treatment_binary'] == 0
