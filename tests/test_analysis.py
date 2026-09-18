"""
Unit Tests for Statistical Analysis & ML Model Pipeline
"""

import pandas as pd
import numpy as np
import pytest
from src.data_loader import load_raw_data
from src.data_cleaning import clean_survey_data
from src.statistics import run_chi_square_test, calculate_cramers_v
from src.modeling import build_and_evaluate_model


def test_chi_square_test():
    df_raw = load_raw_data()
    clean_df = clean_survey_data(df_raw)
    res = run_chi_square_test(clean_df, 'family_history')
    assert 'chi2' in res
    assert 'p_value' in res
    assert 'cramers_v' in res
    assert res['chi2'] >= 0
    assert 0 <= res['p_value'] <= 1.0


def test_cramers_v_calc():
    ct = np.array([[50, 10], [10, 50]])
    v = calculate_cramers_v(ct)
    assert 0 <= v <= 1.0


def test_ml_model_pipeline():
    df_raw = load_raw_data()
    clean_df = clean_survey_data(df_raw)
    model_results = build_and_evaluate_model(clean_df, test_size=0.2, random_state=42)
    assert 'pipeline' in model_results
    assert 'test_metrics' in model_results
    assert 'confusion_matrix' in model_results
    assert 'feature_importance_df' in model_results
    
    test_m = model_results['test_metrics']
    assert 0 <= test_m['accuracy'] <= 1.0
    assert 0 <= test_m['roc_auc'] <= 1.0
