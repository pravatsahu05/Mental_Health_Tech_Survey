"""
Page 4: Advanced Analytics & Machine Learning Model
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_loader import load_raw_data
from src.data_cleaning import clean_survey_data
from components.sidebar import render_sidebar_filters
from components.insight_cards import render_insight_card, render_responsible_use_disclaimer, render_chart_insight
from src.utils import filter_dataset, inject_custom_theme
from src.statistics import compute_all_chi_square_summary, run_chi_square_test
from src.modeling import (
    build_and_evaluate_model, plot_coefficients_bar,
    plot_roc_curve, plot_confusion_matrix, PREDICTOR_CANDIDATES
)
import config

st.set_page_config(page_title="Analytics & ML | MindTech Insights", page_icon="🧠", layout="wide")
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

st.title("🤖 Advanced Statistical Analytics & Machine Learning")
st.caption("Combining Chi-Square Independence tests, Cramér's V association matrices, and an interpretable Logistic Regression classification pipeline.")

if len(df_filtered) < 50:
    st.warning("⚠️ Insufficient sample size (< 50 records) in current filter selection to run advanced statistical tests and train ML model. Please relax filters.")
    st.stop()

# --- PART A: STATISTICAL TESTING ---
st.subheader("📐 Association Strength Summary (Cramér's V Matrix)")
CANDIDATE_VARS = [
    'family_history', 'work_interfere', 'care_options', 'benefits',
    'wellness_program', 'seek_help', 'anonymity', 'leave',
    'mental_health_consequence', 'phys_health_consequence',
    'coworkers', 'supervisor', 'mental_vs_physical', 'obs_consequence',
    'Gender_clean', 'no_employees', 'remote_work', 'tech_company'
]

summary_df = compute_all_chi_square_summary(df_filtered, CANDIDATE_VARS)
st.dataframe(summary_df, use_container_width=True, hide_index=True)

fig_v = px.bar(
    summary_df,
    x='Cramer\'s V',
    y='Variable',
    orientation='h',
    text='Cramer\'s V',
    title="<b>Categorical Predictor Association Strength (Cramér's V)</b>",
    color='Cramer\'s V',
    color_continuous_scale=['#4FACFE', '#00F2FE'],
    hover_data=['P-Value', 'Significant (p < 0.05)']
)
fig_v.update_traces(texttemplate='%{text:.3f}', textposition='outside')
fig_v.update_layout(**config.PLOTLY_THEME_CONFIG, height=420, coloraxis_showscale=False)
st.plotly_chart(fig_v, use_container_width=True)

st.markdown("---")

# --- PART B: MACHINE LEARNING PREDICTOR MODEL ---
st.subheader("🤖 Machine Learning — Treatment Predictor Model")
st.markdown("### 🎛️ Model Hyperparameters & Setup")

col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
with col_ctrl1:
    test_size_input = st.slider("Test Split Ratio", min_value=0.15, max_value=0.35, value=0.20, step=0.05)
with col_ctrl2:
    c_param_input = st.select_slider("Regularization Parameter (C)", options=[0.01, 0.1, 1.0, 10.0], value=1.0)
with col_ctrl3:
    random_state_input = st.number_input("Random Seed", value=42, step=1)

model_results = build_and_evaluate_model(
    df_filtered,
    feature_cols=PREDICTOR_CANDIDATES,
    test_size=test_size_input,
    random_state=int(random_state_input),
    C_param=float(c_param_input)
)

test_m = model_results['test_metrics']
train_m = model_results['train_metrics']

st.markdown("#### 📈 Model Performance Metrics")
m_col1, m_col2, m_col3, m_col4, m_col5, m_col6 = st.columns(6)
m_col1.metric("Test Accuracy", f"{test_m['accuracy']*100:.1f}%", f"Train: {train_m['accuracy']*100:.1f}%")
m_col2.metric("5-Fold CV Accuracy", f"{test_m['cv_mean_accuracy']*100:.1f}%", f"±{test_m['cv_std_accuracy']*100:.1f}%")
m_col3.metric("Precision", f"{test_m['precision']*100:.1f}%")
m_col4.metric("Recall", f"{test_m['recall']*100:.1f}%")
m_col5.metric("F1-Score", f"{test_m['f1']*100:.1f}%")
m_col6.metric("ROC-AUC", f"{test_m['roc_auc']:.3f}")

st.markdown("---")

col_diag1, col_diag2 = st.columns(2)

with col_diag1:
    fig_cm = plot_confusion_matrix(model_results['confusion_matrix'])
    st.plotly_chart(fig_cm, use_container_width=True)
    render_chart_insight("Confusion matrix illustrates true positive vs false positive treatment predictions on test data.")

with col_diag2:
    fig_roc = plot_roc_curve(model_results['roc_df'], test_m['roc_auc'])
    st.plotly_chart(fig_roc, use_container_width=True)
    render_chart_insight(f"ROC Curve demonstrates classifier discrimination power with an AUC of {test_m['roc_auc']:.3f}.")

st.markdown("---")

st.subheader("🔍 Model Interpretability & Odds Ratios")
fig_coef = plot_coefficients_bar(model_results['feature_importance_df'], top_n=14)
st.plotly_chart(fig_coef, use_container_width=True)

st.markdown("#### Full Feature Odds Ratios & Coefficients Table")
st.dataframe(
    model_results['feature_importance_df'][['readable_feature', 'coefficient', 'odds_ratio']],
    use_container_width=True,
    hide_index=True
)

render_responsible_use_disclaimer()
