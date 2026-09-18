"""
MindTech Insights — Statistical Analysis Module
Provides Chi-Square tests, Cramér's V effect sizes, correlation analysis,
and proportion confidence intervals with clear business interpretation.
Includes pure-Python fallback calculations if scipy is absent.
"""

from typing import Dict, Any, Tuple, List
import math
import numpy as np
import pandas as pd

# Graceful import of scipy.stats with pure-Python fallback
try:
    from scipy import stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


def pure_python_chi2_contingency(obs: np.ndarray) -> Tuple[float, float, int]:
    """
    Pure Python calculation of Chi-Square statistic, approximate p-value, and degrees of freedom.
    """
    row_sums = obs.sum(axis=1)
    col_sums = obs.sum(axis=0)
    total = obs.sum()
    
    r, c = obs.shape
    dof = (r - 1) * (c - 1)
    
    chi2 = 0.0
    for i in range(r):
        for j in range(c):
            expected = (row_sums[i] * col_sums[j]) / total
            if expected > 0:
                chi2 += ((obs[i, j] - expected) ** 2) / expected
                
    # Approximate p-value for dof=1 using normal approximation z = sqrt(2*chi2) - sqrt(2*dof - 1)
    if dof > 0:
        z = math.sqrt(2 * chi2) - math.sqrt(2 * dof - 1)
        p_val = 0.5 * math.erfc(z / math.sqrt(2))
        p_val = max(0.0, min(1.0, p_val))
    else:
        p_val = 1.0
        
    return float(chi2), float(p_val), int(dof)


def calculate_cramers_v(contingency_table: np.ndarray) -> float:
    """
    Calculates Cramér's V statistic for categorical-categorical association.
    Formula: V = sqrt(chi2 / (n * min(r-1, c-1)))
    """
    n = contingency_table.sum()
    if n == 0:
        return 0.0
    r, c = contingency_table.shape
    min_dim = min(r - 1, c - 1)
    if min_dim == 0:
        return 0.0

    if HAS_SCIPY:
        chi2 = stats.chi2_contingency(contingency_table)[0]
    else:
        chi2 = pure_python_chi2_contingency(contingency_table)[0]
        
    return float(np.sqrt(chi2 / (n * min_dim)))


def interpret_cramers_v(v: float) -> str:
    """Returns qualitative strength interpretation of Cramér's V."""
    if v < 0.10:
        return "Negligible association"
    elif v < 0.20:
        return "Weak association"
    elif v < 0.30:
        return "Moderate association"
    else:
        return "Strong association"


def run_chi_square_test(df: pd.DataFrame, feature_col: str, target_col: str = 'treatment') -> Dict[str, Any]:
    """
    Performs Chi-Square Test of Independence between a categorical feature and treatment response.

    Returns:
        Dict: Test name, variables, chi2 statistic, p-value, df, Cramér's V, and interpretation.
    """
    valid_df = df.dropna(subset=[feature_col, target_col])
    contingency_table = pd.crosstab(valid_df[feature_col], valid_df[target_col])
    
    if contingency_table.empty or contingency_table.shape[0] < 2 or contingency_table.shape[1] < 2:
        return {
            'feature': feature_col,
            'target': target_col,
            'chi2': 0.0,
            'p_value': 1.0,
            'dof': 0,
            'cramers_v': 0.0,
            'is_significant': False,
            'effect_interpretation': 'Insufficient valid categories',
            'business_summary': 'Not enough data across groups to evaluate relationship.',
            'contingency_table': contingency_table
        }

    if HAS_SCIPY:
        chi2, p_val, dof, _ = stats.chi2_contingency(contingency_table)
    else:
        chi2, p_val, dof = pure_python_chi2_contingency(contingency_table.values)

    v = calculate_cramers_v(contingency_table.values)
    is_sig = p_val < 0.05
    effect_str = interpret_cramers_v(v)
    
    if is_sig:
        summary = (
            f"Statistically significant relationship detected (p = {p_val:.4f}). "
            f"Effect size is {effect_str} (Cramér's V = {v:.3f}). "
            f"Treatment response rates vary across '{feature_col}' groups in a non-random pattern."
        )
    else:
        summary = (
            f"No statistically significant relationship detected (p = {p_val:.4f}). "
            f"Observed variations across '{feature_col}' may be due to sample variance."
        )

    return {
        'feature': feature_col,
        'target': target_col,
        'chi2': float(round(chi2, 3)),
        'p_value': float(round(p_val, 4)),
        'dof': int(dof),
        'cramers_v': float(round(v, 3)),
        'is_significant': bool(is_sig),
        'effect_interpretation': effect_str,
        'business_summary': summary,
        'contingency_table': contingency_table
    }


def calculate_proportion_confidence_interval(count: int, nobs: int, alpha: float = 0.05) -> Tuple[float, float, float]:
    """
    Calculates Wilson score 95% confidence interval for proportions.
    Returns: (proportion, ci_lower, ci_upper)
    """
    if nobs == 0:
        return 0.0, 0.0, 0.0
    p = count / nobs
    
    if HAS_SCIPY:
        z = stats.norm.ppf(1 - alpha / 2)
    else:
        z = 1.95996  # 95% CI z-score approximation
        
    denom = 1 + z**2 / nobs
    centre_adjusted_p = (p + z**2 / (2 * nobs)) / denom
    adjusted_std_dev = math.sqrt((p * (1 - p) + z**2 / (4 * nobs)) / nobs) / denom
    
    ci_lower = max(0.0, centre_adjusted_p - z * adjusted_std_dev)
    ci_upper = min(1.0, centre_adjusted_p + z * adjusted_std_dev)
    
    return float(round(p * 100, 1)), float(round(ci_lower * 100, 1)), float(round(ci_upper * 100, 1))


def compute_all_chi_square_summary(df: pd.DataFrame, candidate_cols: List[str]) -> pd.DataFrame:
    """
    Runs Chi-Square tests across all candidate survey variables against 'treatment'
    and returns a sorted summary DataFrame.
    """
    results = []
    for col in candidate_cols:
        if col in df.columns and col != 'treatment':
            res = run_chi_square_test(df, col)
            results.append({
                'Variable': col,
                'Chi2 Statistic': res['chi2'],
                'Degrees of Freedom': res['dof'],
                'P-Value': res['p_value'],
                'Cramer\'s V': res['cramers_v'],
                'Significant (p < 0.05)': 'Yes' if res['is_significant'] else 'No',
                'Effect Strength': res['effect_interpretation']
            })
    
    res_df = pd.DataFrame(results).sort_values(by='Cramer\'s V', ascending=False)
    return res_df
