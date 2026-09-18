"""
MindTech Insights — Machine Learning Predictor Engine
Builds interpretable Logistic Regression classification pipeline predicting reported treatment.
Extracts Odds Ratios, Feature Coefficients, Permutation Importances, ROC-AUC, and Confusion Matrices.
Includes graceful fallback if scikit-learn is absent.
"""

from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import config

# Graceful import of scikit-learn
try:
    from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        roc_auc_score, confusion_matrix, roc_curve
    )
    from sklearn.inspection import permutation_importance
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


# Candidate predictors available in survey.csv
PREDICTOR_CANDIDATES = [
    'Age_clean', 'Gender_clean', 'self_employed', 'family_history',
    'work_interfere', 'no_employees', 'remote_work', 'tech_company',
    'benefits', 'care_options', 'wellness_program', 'seek_help',
    'anonymity', 'leave', 'mental_health_consequence', 'phys_health_consequence',
    'coworkers', 'supervisor', 'mental_health_interview', 'phys_health_interview',
    'mental_vs_physical', 'obs_consequence'
]


def format_readable_feature_name(feature_name: str) -> str:
    """Formats technical pipeline column names into clean, readable labels."""
    clean = feature_name.replace('cat__', '').replace('num__', '')
    parts = clean.split('_')
    if len(parts) > 1:
        val = parts[-1]
        col_name = " ".join(parts[:-1]).title()
        return f"{col_name} = {val}"
    return clean.replace('_', ' ').title()


def build_and_evaluate_model(
    df: pd.DataFrame,
    feature_cols: List[str] = PREDICTOR_CANDIDATES,
    test_size: float = config.MODEL_TEST_SIZE,
    random_state: int = config.MODEL_RANDOM_STATE,
    C_param: float = 1.0
) -> Dict[str, Any]:
    """
    Trains Logistic Regression model on survey predictor variables.
    Reports separate Training, Validation (CV), and Test metrics.

    Returns:
        Dict: Model object, test metrics, confusion matrix, ROC data, feature importances.
    """
    if not HAS_SKLEARN:
        return {
            'error': 'scikit-learn is not installed in the active environment. Please install using: pip install scikit-learn',
            'pipeline': None,
            'train_metrics': {'accuracy': 0, 'precision': 0, 'recall': 0, 'f1': 0},
            'test_metrics': {'accuracy': 0, 'precision': 0, 'recall': 0, 'f1': 0, 'roc_auc': 0, 'cv_mean_accuracy': 0, 'cv_std_accuracy': 0},
            'confusion_matrix': np.zeros((2, 2)),
            'roc_df': pd.DataFrame({'fpr': [0, 1], 'tpr': [0, 1]}),
            'feature_importance_df': pd.DataFrame(),
            'permutation_importance_df': pd.DataFrame(),
            'sample_sizes': {'train': 0, 'test': 0}
        }

    # 1. Dataset Preparation
    valid_cols = [c for c in feature_cols if c in df.columns]
    data = df.dropna(subset=['treatment']).copy()
    
    X = data[valid_cols]
    y = (data['treatment'] == 'Yes').astype(int)
    
    # Identify numeric and categorical columns
    num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Preprocessing Pipelines
    num_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    cat_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(transformers=[
        ('num', num_transformer, num_cols),
        ('cat', cat_transformer, cat_cols)
    ])
    
    model = LogisticRegression(C=C_param, max_iter=1000, random_state=random_state)
    
    clf = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])
    
    # Train / Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Train Model
    clf.fit(X_train, y_train)
    
    # Predictions
    y_train_pred = clf.predict(X_train)
    y_test_pred = clf.predict(X_test)
    y_test_proba = clf.predict_proba(X_test)[:, 1]
    
    # 5-Fold Cross Validation Score on Training Data
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
    cv_scores = cross_val_score(clf, X_train, y_train, cv=cv, scoring='accuracy')
    
    # Metrics Calculation
    train_metrics = {
        'accuracy': accuracy_score(y_train, y_train_pred),
        'precision': precision_score(y_train, y_train_pred, zero_division=0),
        'recall': recall_score(y_train, y_train_pred, zero_division=0),
        'f1': f1_score(y_train, y_train_pred, zero_division=0)
    }
    
    test_metrics = {
        'accuracy': accuracy_score(y_test, y_test_pred),
        'precision': precision_score(y_test, y_test_pred, zero_division=0),
        'recall': recall_score(y_test, y_test_pred, zero_division=0),
        'f1': f1_score(y_test, y_test_pred, zero_division=0),
        'roc_auc': roc_auc_score(y_test, y_test_proba),
        'cv_mean_accuracy': cv_scores.mean(),
        'cv_std_accuracy': cv_scores.std()
    }
    
    # Feature Importances & Odds Ratios
    cat_encoder = clf.named_steps['preprocessor'].named_transformers_['cat'].named_steps['encoder']
    encoded_cat_names = cat_encoder.get_feature_names_out(cat_cols).tolist() if cat_cols else []
    all_feature_names = num_cols + encoded_cat_names
    
    coefficients = clf.named_steps['classifier'].coef_[0]
    odds_ratios = np.exp(coefficients)
    
    feature_imp_df = pd.DataFrame({
        'raw_feature': all_feature_names,
        'readable_feature': [format_readable_feature_name(f) for f in all_feature_names],
        'coefficient': coefficients,
        'odds_ratio': odds_ratios,
        'abs_coef': np.abs(coefficients)
    }).sort_values(by='abs_coef', ascending=False)
    
    # Permutation Importance
    perm_imp = permutation_importance(clf, X_test, y_test, n_repeats=5, random_state=random_state)
    perm_df = pd.DataFrame({
        'feature': X.columns,
        'importance_mean': perm_imp.importances_mean,
        'importance_std': perm_imp.importances_std
    }).sort_values(by='importance_mean', ascending=False)
    
    # ROC Curve Data
    fpr, tpr, thresholds = roc_curve(y_test, y_test_proba)
    roc_df = pd.DataFrame({'fpr': fpr, 'tpr': tpr})
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_test_pred)
    
    return {
        'pipeline': clf,
        'train_metrics': train_metrics,
        'test_metrics': test_metrics,
        'confusion_matrix': cm,
        'roc_df': roc_df,
        'feature_importance_df': feature_imp_df,
        'permutation_importance_df': perm_df,
        'sample_sizes': {'train': len(X_train), 'test': len(X_test)}
    }


def plot_coefficients_bar(feature_imp_df: pd.DataFrame, top_n: int = 12) -> go.Figure:
    """Plots top positive and negative coefficient odds ratios."""
    if feature_imp_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No model feature importances available", showarrow=False)
        fig.update_layout(**config.PLOTLY_THEME_CONFIG)
        return fig

    top_df = feature_imp_df.head(top_n).sort_values(by='coefficient', ascending=True)
    
    fig = px.bar(
        top_df,
        x='coefficient',
        y='readable_feature',
        orientation='h',
        text='odds_ratio',
        title=f"Top {top_n} Predictor Coefficients (Logistic Regression)",
        labels={'coefficient': 'Coefficient Value (Beta)', 'readable_feature': 'Predictor Variable'},
        color='coefficient',
        color_continuous_scale=['#FF5252', '#00E676'],
        hover_data=['odds_ratio']
    )
    fig.update_traces(texttemplate='OR: %{text:.2f}', textposition='outside')
    fig.update_layout(**config.PLOTLY_THEME_CONFIG, height=450, coloraxis_showscale=False)
    return fig


def plot_roc_curve(roc_df: pd.DataFrame, auc_score: float) -> go.Figure:
    """Plots Receiver Operating Characteristic (ROC) Curve."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=roc_df['fpr'], y=roc_df['tpr'], mode='lines', name=f'ROC Curve (AUC = {auc_score:.3f})', line=dict(color='#00F2FE', width=3)))
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Random Classifier', line=dict(color='#8B949E', dash='dash')))
    fig.update_layout(
        title="Receiver Operating Characteristic (ROC) Curve",
        xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate",
        **config.PLOTLY_THEME_CONFIG,
        height=380
    )
    return fig


def plot_confusion_matrix(cm: np.ndarray) -> go.Figure:
    """Plots heatmap visualization of Confusion Matrix."""
    labels = ['No Treatment (0)', 'Reported Treatment (1)']
    fig = px.imshow(
        cm,
        x=labels,
        y=labels,
        text_auto=True,
        color_continuous_scale=['#161B22', '#00F2FE'],
        title="Confusion Matrix (Test Evaluation)"
    )
    fig.update_layout(**config.PLOTLY_THEME_CONFIG, height=360, coloraxis_showscale=False)
    return fig
