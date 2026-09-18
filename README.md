# 🧠 MindTech Insights — Mental Health & Workplace Wellbeing Analytics

## 1. Project Overview
**MindTech Insights** is an advanced, production-quality Mental Health Analytics application built from scratch to explore patterns, workplace attitudes, support availability, stigma, and predictive indicators in technology workplace survey data.

The system is designed to provide data-driven insights for HR leaders, executives, people operations teams, and data scientists seeking to foster supportive workplace environments.

> [!IMPORTANT]
> **Responsible Analytics Disclaimer:** `treatment` in this dataset represents an empirical survey response ("reported treatment", "treatment response"), **NOT a clinical diagnosis**. All statistical relationships are observational associations and do not establish causality.

---

## 2. Key Business & Analytical Questions Answered
1. What are the demographic characteristics of workplace respondents?
2. How are treatment seeking responses distributed across age, gender, and sector?
3. How does family history relate to treatment response?
4. How does work interference frequency relate to treatment seeking behavior?
5. Do employees understand available care options and health benefits?
6. What is the overall **Workplace Support Index (0 - 100)** score across organizations?
7. Are employees comfortable discussing mental health with supervisors vs coworkers?
8. Do employees perceive mental health as being treated as seriously as physical health?
9. How do treatment responses vary geographically across countries and US states?
10. Which workplace factors are most strongly associated with treatment seeking in statistical tests ($\chi^2$, Cramér's V) and machine learning models (Odds Ratios)?

---

## 3. Data Dictionary Summary
| Variable Name | Description | Data Type | Cleaning Strategy |
| :--- | :--- | :--- | :--- |
| `Timestamp` | Survey submission date & time | Datetime | Parsed to Year, Month, Day, Hour |
| `Age` | Respondent age (years) | Numeric | Validated (18 - 100); invalid values converted to NaN |
| `Gender` | Self-reported gender | Free-text | Standardized into Male, Female, Trans/Non-Binary, Other |
| `Country` | Country of residence | Categorical | Filterable by configurable minimum sample size $N \ge 20$ |
| `state` | US State code | Categorical | Filtered for US respondents |
| `family_history` | Family history of mental illness | Binary (Yes/No) | Encoded into `family_history_binary` (1/0) |
| `treatment` | Sought treatment for mental health | Binary (Yes/No) | Primary Modeling Outcome (`treatment_binary`) |
| `work_interfere` | Frequency mental health interferes with work | Ordinal | Categories: Often, Sometimes, Rarely, Never |
| `benefits` | Employer provides mental health benefits | Categorical | Options: Yes, No, Don't know |
| `care_options` | Knowledge of available care options | Categorical | Options: Yes, No, Not sure |
| `anonymity` | Anonymity protected if using care | Categorical | Options: Yes, No, Don't know |
| `leave` | Ease of taking medical leave | Ordinal | Options: Very easy to Very difficult |

---

## 4. System Architecture
```text
Mental_Health_Tech_Survey_Project/
│
├── app.py                      # Main Streamlit Entry Application
├── config.py                   # Global configuration & color theme palette
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── data/
│   └── survey.csv              # Survey dataset
│
├── pages/                      # Multi-page Streamlit Application
│   ├── 1_Executive_Overview.py
│   ├── 2_Demographics.py
│   ├── 3_Mental_Health.py
│   ├── 4_Workplace_Support.py
│   ├── 5_Workplace_Culture.py
│   ├── 6_Geographic_Analysis.py
│   ├── 7_Statistical_Analysis.py
│   ├── 8_Predictor_Model.py
│   └── 9_Insights.py
│
├── src/                        # Modular Core Analytics Modules
│   ├── __init__.py
│   ├── data_loader.py          # Cached data loading
│   ├── data_cleaning.py        # Cleaning, age validation, gender normalization
│   ├── data_quality.py         # Data quality report & missingness heatmaps
│   ├── eda.py                  # Demographics, Mental Health & Workplace EDA
│   ├── statistics.py           # Chi-Square, Cramér's V, Wilson Confidence Intervals
│   ├── modeling.py             # Logistic Regression, Odds Ratios, ROC-AUC
│   ├── insights.py             # Dynamic Insight & Recommendation Engine
│   └── utils.py                # Filters, formatting, CSV exporters
│
├── components/                 # Reusable UI Components
│   ├── sidebar.py              # Interactive sidebar filter bar
│   ├── kpi_cards.py            # Glassmorphism metric cards
│   ├── charts.py               # Plotly theme configuration
│   └── insight_cards.py        # Styled callout cards & disclaimers
│
├── assets/
│   └── style.css               # Modern dark-theme glassmorphism CSS
│
└── tests/                      # Automated Unit Test Suite
    ├── test_data_cleaning.py   # Cleaning & age validation unit tests
    └── test_analysis.py        # Statistical & ML pipeline unit tests
```

---

## 5. Data Cleaning Pipeline (`src/data_cleaning.py`)
1. **Age Validation:** Outliers ($< 18$ or $> 100$) are filtered to `NaN` while preserving valid entries.
2. **Gender Normalization:** Over 30 messy free-text strings (e.g. `M`, `female`, `Cis Female`, `non-binary`, `fluid`) are standardized into:
   - `Male`
   - `Female`
   - `Trans / Non-Binary`
   - `Other / Unspecified`
   *(The raw `Gender_raw` string is preserved intact for transparency).*
3. **Timestamp Parsing:** Extracts `Year`, `Month`, `Day_of_Week`, and `Hour`.
4. **Binary Feature Flags:** Constructs analysis-ready $1/0$ binary flags (`treatment_binary`, `family_history_binary`, `remote_work_binary`, etc.).

---

## 6. Machine Learning Pipeline (`src/modeling.py`)
- **Outcome Variable:** `treatment` ($1 = \text{Yes}, 0 = \text{No}$)
- **Algorithm:** Logistic Regression with L2 Regularization & Feature Preprocessing (`OneHotEncoder`, `StandardScaler`, `SimpleImputer`).
- **Evaluation:** Separate Training, 5-Fold Cross Validation, and Test Split metrics:
  - Accuracy & Cross-Validation Mean Accuracy
  - Precision, Recall, F1-Score
  - ROC-AUC Score & ROC Curve Visualization
  - Confusion Matrix Heatmap
- **Interpretability:** Coefficients converted into **Odds Ratios** ($OR = e^\beta$) with human-readable feature labels (e.g. `Family History = Yes`).

---

## 7. Installation & Local Execution Instructions

### Prerequisites
- Python 3.10+ installed on Windows, macOS, or Linux.

### Setup Steps
1. **Clone / Navigate to Project Directory:**
   ```bash
   cd Mental_Health_Tech_Survey_Project
   ```

2. **Create and Activate Virtual Environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate  # macOS/Linux
   ```

3. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Unit Tests:**
   ```bash
   python -m pytest tests/
   ```

5. **Launch Streamlit Application:**
   ```bash
   streamlit run app.py
   ```
