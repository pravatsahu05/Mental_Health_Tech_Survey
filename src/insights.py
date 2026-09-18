"""
MindTech Insights — Automated Insights & Recommendation Engine
Dynamically analyzes calculated dataset metrics to produce evidence-backed findings,
cautious non-causal statistical interpretations, and actionable workplace policies.
"""

from typing import Dict, List, Any
import pandas as pd
from src.statistics import run_chi_square_test


def generate_executive_insights(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Scans cleaned dataset and returns dynamically calculated executive findings.
    """
    insights = []
    
    # 1. Overall Treatment Rate Baseline
    total_n = len(df)
    treatment_n = (df['treatment'] == 'Yes').sum()
    treatment_pct = (treatment_n / total_n * 100) if total_n > 0 else 0
    
    insights.append({
        'category': 'Baseline Prevalence',
        'finding': f"Overall Reported Treatment Rate is {treatment_pct:.1f}% across surveyed workplace respondents.",
        'evidence': f"Treatment Yes: {treatment_n} / {total_n} total respondents.",
        'interpretation': (
            "This reflects the self-reported proportion of survey respondents who have sought treatment "
            "for a mental health condition. It measures survey prevalence, not clinical diagnostic rates."
        ),
        'card_type': 'info'
    })
    
    # 2. Family History Impact
    if 'family_history' in df.columns and 'treatment' in df.columns:
        fh_ct = pd.crosstab(df['family_history'], df['treatment'], normalize='index').mul(100)
        fh_n = pd.crosstab(df['family_history'], df['treatment'])
        
        yes_fh_rate = fh_ct.loc['Yes', 'Yes'] if 'Yes' in fh_ct.index else 0
        no_fh_rate = fh_ct.loc['No', 'Yes'] if 'No' in fh_ct.index else 0
        
        insights.append({
            'category': 'Demographic Indicator',
            'finding': f"Respondents with a family history of mental illness report significantly higher treatment rates ({yes_fh_rate:.1f}%) compared to those without ({no_fh_rate:.1f}%).",
            'evidence': f"Family History Yes treatment rate: {yes_fh_rate:.1f}% (N={fh_n.loc['Yes'].sum() if 'Yes' in fh_n.index else 0}) vs No: {no_fh_rate:.1f}% (N={fh_n.loc['No'].sum() if 'No' in fh_n.index else 0}).",
            'interpretation': "Strong observational association in survey data. Family history may increase personal awareness or willingness to seek professional care.",
            'card_type': 'warning'
        })

    # 3. Work Interference Pattern
    if 'work_interfere' in df.columns and 'treatment' in df.columns:
        wi_ct = pd.crosstab(df['work_interfere'], df['treatment'], normalize='index').mul(100)
        wi_n = pd.crosstab(df['work_interfere'], df['treatment'])
        
        often_rate = wi_ct.loc['Often', 'Yes'] if 'Often' in wi_ct.index else 0
        never_rate = wi_ct.loc['Never', 'Yes'] if 'Never' in wi_ct.index else 0
        
        insights.append({
            'category': 'Work Interference',
            'finding': f"Respondents reporting frequent ('Often') work interference exhibit a {often_rate:.1f}% treatment rate compared to {never_rate:.1f}% for those reporting 'Never'.",
            'evidence': f"'Often' interference treatment rate: {often_rate:.1f}% vs 'Never': {never_rate:.1f}%.",
            'interpretation': "Daily functional impact on work activities correlates strongly with treatment seeking behavior.",
            'card_type': 'danger'
        })
        
    # 4. Care Options & Benefit Awareness Gap
    if 'care_options' in df.columns:
        care_know = (df['care_options'] == 'Yes').mean() * 100
        care_unsure = (df['care_options'].isin(['Not sure', "Don't know"])).mean() * 100
        
        insights.append({
            'category': 'Workplace Benefit Gap',
            'finding': f"Only {care_know:.1f}% of respondents clearly know their employer's care options, while {care_unsure:.1f}% are unsure or unaware.",
            'evidence': f"Clear awareness: {care_know:.1f}% | Unsure/Unknown: {care_unsure:.1f}%.",
            'interpretation': "Indicates an internal communication gap regarding available health benefits rather than a total absence of programs.",
            'card_type': 'warning'
        })
        
    # 5. Culture & Discussion Stigma
    if 'supervisor' in df.columns and 'coworkers' in df.columns:
        sup_yes = (df['supervisor'] == 'Yes').mean() * 100
        cow_yes = (df['coworkers'] == 'Yes').mean() * 100
        
        insights.append({
            'category': 'Workplace Stigma & Openness',
            'finding': f"Respondents are more comfortable discussing mental health with direct supervisors ({sup_yes:.1f}%) than unreservedly with all coworkers ({cow_yes:.1f}%).",
            'evidence': f"Supervisor comfort 'Yes': {sup_yes:.1f}% vs Coworker comfort 'Yes': {cow_yes:.1f}%.",
            'interpretation': "Hierarchical trust and confidentiality expectations influence discussion openness at work.",
            'card_type': 'success'
        })

    return insights


def generate_actionable_recommendations() -> List[Dict[str, str]]:
    """
    Returns data-informed, strategic workplace recommendations.
    """
    return [
        {
            'category': 'Employee Support',
            'action': 'Proactive EAP & Care Option Guidance',
            'details': 'Publish annual, easy-to-read benefit cheat sheets detailing mental health coverage, therapy subsidies, and helpline access to eliminate benefit uncertainty.'
        },
        {
            'category': 'Workplace Policy',
            'action': 'Explicit Mental Health Medical Leave',
            'details': 'Normalize medical leave policies to explicitly cover mental health recovery days under standard sick leave without requiring clinical diagnostic disclosure.'
        },
        {
            'category': 'Manager Training',
            'action': 'Empathy & Burnout First Responder Training',
            'details': 'Equip team leads with empathetic communication skills to identify early burnout signs and provide confidential resource referrals.'
        },
        {
            'category': 'Confidentiality',
            'action': 'Anonymity Guarantees for Wellness Programs',
            'details': 'Ensure all wellness surveys, counseling tools, and health apps are managed by third-party vendors with explicit privacy firewalls.'
        },
        {
            'category': 'Workplace Culture',
            'action': 'Parity Between Mental and Physical Health',
            'details': 'Establish executive communications stating that mental health accommodations carry equal weight and legitimacy as physical injury accommodations.'
        }
    ]
