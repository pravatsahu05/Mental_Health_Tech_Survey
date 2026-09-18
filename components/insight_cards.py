"""
MindTech Insights — Insight Cards Component
Renders styled business insight callout cards and disclaimers.
"""

import streamlit as st


def render_insight_card(finding: str, evidence: str = "", interpretation: str = "", card_type: str = "info"):
    """
    Renders styled callout card for evidence-backed findings.
    """
    badge_map = {
        'info': '💡 INSIGHT',
        'warning': '⚠️ ATTENTION',
        'danger': '🚨 ALERT',
        'success': '✅ POSITIVE'
    }
    badge = badge_map.get(card_type, '💡 INSIGHT')
    
    html_code = f"""
    <div class="insight-card {card_type}">
        <div class="insight-title">{badge}: {finding}</div>
        {"<div class='insight-body'><b>Evidence:</b> " + evidence + "</div>" if evidence else ""}
        {"<div class='insight-body' style='margin-top:4px;'><b>Interpretation:</b> " + interpretation + "</div>" if interpretation else ""}
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)


def render_chart_insight(insight_text: str):
    """
    Renders standard chart business insight block below visual charts.
    """
    st.markdown(
        f"""
        <div style="background: rgba(22, 27, 34, 0.6); border-left: 3px solid #00F2FE; padding: 10px 14px; border-radius: 6px; font-size: 0.88rem; color: #C9D1D9; margin-top: 8px;">
            <b>💡 Business Insight:</b> {insight_text}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_responsible_use_disclaimer():
    """
    Renders responsible analytics & medical disclaimer.
    """
    st.markdown(
        """
        <div class="responsible-banner">
            <b>⚖️ Responsible Analytics & Use Notice:</b><br>
            • This application displays self-reported survey data from tech industry respondents.<br>
            • <code>treatment</code> indicates survey participation in mental health care; it is <b>not a clinical diagnosis</b>.<br>
            • All identified statistical relationships are observational <b>associations</b> and do not prove direct causation.<br>
            • Insights should be used solely for workplace wellbeing policy improvements, never for discriminatory HR practices.
        </div>
        """,
        unsafe_allow_html=True
    )
