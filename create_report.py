import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_report():
    doc = docx.Document()

    # Define color scheme
    NAVY_HEX = "0F172A"      # Slate 900
    TEAL_HEX = "0284C7"      # Sky 600 / Teal Accent
    DARK_BLUE_HEX = "1E293B" # Slate 800
    LIGHT_BG_HEX = "F8FAFC"  # Light background
    BORDER_HEX = "CBD5E1"    # Gray border
    MUTED_HEX = "64748B"     # Muted text

    # Page Setup - Margins 1 inch
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Set base Normal style font
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Calibri'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x33, 0x41, 0x55) # Slate 700

    # Helper Functions for Styling
    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for margin, value in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{margin}')
            node.set(qn('w:w'), str(value))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def add_callout_box(text, title=""):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F0F9FF") # Sky light tint
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

        # Left border sky blue
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="none"/>
                <w:left w:val="single" w:sz="36" w:space="0" w:color="0284C7"/>
                <w:bottom w:val="none"/>
                <w:right w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        if title:
            r_title = p.add_run(f"{title}\n")
            r_title.bold = True
            r_title.font.name = 'Calibri'
            r_title.font.size = Pt(11)
            r_title.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)
        r_text = p.add_run(text)
        r_text.font.name = 'Calibri'
        r_text.font.size = Pt(10.5)
        r_text.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(18)
        run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A) # Slate 900
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0x02, 0x84, 0xC7) # Sky Blue Accent
        return p

    def add_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        return p

    # --- COVER / TITLE BLOCK ---
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(24)
    title_p.paragraph_format.space_after = Pt(4)
    t_run = title_p.add_run("🧠 MindTech Insights")
    t_run.bold = True
    t_run.font.size = Pt(26)
    t_run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(14)
    s_run = sub_p.add_run("Mental Health & Workplace Wellbeing Analytics Platform — Empirical Survey & ML Diagnostic Assessment Report")
    s_run.font.size = Pt(14)
    s_run.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # Divider line
    div_p = doc.add_paragraph()
    div_p.paragraph_format.space_after = Pt(16)
    d_run = div_p.add_run("_________________________________________________________________________________")
    d_run.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)

    # --- SECTION 1: PROJECT ACCESS & LINKS ---
    add_heading_1("1. Project Access & Repository Links")
    
    add_callout_box(
        "This project is fully open-source and deployed online for interactive exploratory data analysis, statistical testing, and real-time machine learning prediction.",
        "🌐 Live Access Information"
    )

    tbl_links = doc.add_table(rows=3, cols=2)
    tbl_links.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Resource Type", "URL / Access Link"]
    
    # Format header
    hdr_cells = tbl_links.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], NAVY_HEX)
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=150, right=150)
        p = hdr_cells[i].paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    link_data = [
        ("GitHub Repository Link", "https://github.com/pravatsahu05/Mental_Health_Tech_Survey"),
        ("Live Web Application Link", "https://mental-health-tech-survey.onrender.com (Render Cloud Deployment)")
    ]

    for row_idx, (res_type, url_val) in enumerate(link_data, start=1):
        row_cells = tbl_links.rows[row_idx].cells
        row_cells[0].text = res_type
        row_cells[1].text = url_val
        
        bg_color = LIGHT_BG_HEX if row_idx % 2 == 1 else "FFFFFF"
        for cell in row_cells:
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
            
        # Bold resource type, color link blue
        p0 = row_cells[0].paragraphs[0]
        if p0.runs:
            p0.runs[0].font.bold = True
            p0.runs[0].font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        p1 = row_cells[1].paragraphs[0]
        if p1.runs:
            p1.runs[0].font.color.rgb = RGBColor(0x02, 0x84, 0xC7)
            p1.runs[0].font.underline = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # --- SECTION 2: EXECUTIVE SUMMARY ---
    add_heading_1("2. Executive Summary")
    
    p = doc.add_paragraph()
    p.add_run(
        "MindTech Insights is an enterprise-grade analytics and decision-support platform engineered to evaluate workplace mental health, "
        "employee support structures, social stigma, and treatment-seeking patterns across technology and corporate organizations. "
        "Utilizing empirical data from 1,259 tech industry respondents, this project establishes a rigorous baseline of workplace wellbeing indicators."
    )
    
    add_heading_2("Key Business Highlights")
    bullets = [
        "High Treatment-Seeking Rate: 51.6% (650 / 1,259) of surveyed tech workers reported seeking mental health treatment.",
        "Primary Determinant: Family history of mental illness is the single strongest statistical predictor (Chi-Square = 85.57, p < 0.0001, Cramér's V = 0.261), increasing treatment seeking likelihood by nearly 3x (Odds Ratio = 2.94).",
        "Workplace Productivity Impact: 78.8% of respondents report that mental health interferes with their work (489 'Sometimes', 123 'Often', 181 'Rarely').",
        "Stigma Gap: 47.2% of employees report uncertainty or lack of awareness regarding their employer's mental health care options and benefit policies.",
        "Management Trust Asymmetry: Employees demonstrate substantially higher comfort discussing mental health issues with direct supervisors than with general coworkers."
    ]
    for b in bullets:
        doc.add_paragraph(b, style='List Bullet')

    add_callout_box(
        "Responsible Analytics Disclaimer: The outcome variable 'treatment' represents an empirical survey response ('reported treatment'), NOT a clinical diagnosis. All statistical relationships indicate observational associations.",
        "⚠️ Methodological Note"
    )

    # --- SECTION 3: DATA DICTIONARY & CLEANING PIPELINE ---
    add_heading_1("3. Data Dictionary & Cleaning Pipeline")
    
    p = doc.add_paragraph()
    p.add_run("The raw survey dataset contained 1,259 initial entries with multiple unstructured and free-text attributes. The automated cleaning pipeline performed strict normalization:")

    add_heading_2("Standardized Data Dictionary")
    
    dict_table_data = [
        ("Timestamp", "Datetime", "Survey submission timestamp", "Parsed into Year, Month, Day, Hour"),
        ("Age", "Numeric", "Respondent age in years", "Filtered to valid range (18–100); outliers set to NaN"),
        ("Gender", "Categorical", "Self-reported gender", "Normalized from 30+ free-text values into Male, Female, Trans/Non-Binary"),
        ("Country / State", "Categorical", "Geographic residence", "Filtered for minimum sample size N >= 20"),
        ("family_history", "Binary", "Family history of mental illness", "Encoded into family_history_binary (1/0)"),
        ("treatment", "Binary", "Reported mental health treatment", "Primary Modeling Target (1 = Yes, 0 = No)"),
        ("work_interfere", "Ordinal", "Work interference frequency", "Categorized: Often, Sometimes, Rarely, Never"),
        ("benefits", "Categorical", "Employer mental health benefits", "Yes, No, Don't know"),
        ("care_options", "Categorical", "Knowledge of care options", "Yes, No, Not sure"),
        ("anonymity", "Categorical", "Anonymity protected if using care", "Yes, No, Don't know"),
        ("leave", "Ordinal", "Ease of medical leave", "Very easy, Somewhat easy, Somewhat difficult, Very difficult")
    ]

    tbl_dict = doc.add_table(rows=len(dict_table_data)+1, cols=4)
    tbl_dict.alignment = WD_TABLE_ALIGNMENT.CENTER
    dict_headers = ["Variable", "Type", "Description", "Cleaning Strategy"]
    
    hdr_cells_d = tbl_dict.rows[0].cells
    for i, h in enumerate(dict_headers):
        hdr_cells_d[i].text = h
        set_cell_background(hdr_cells_d[i], NAVY_HEX)
        set_cell_margins(hdr_cells_d[i], top=100, bottom=100, left=120, right=120)
        hdr_cells_d[i].paragraphs[0].runs[0].font.bold = True
        hdr_cells_d[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, row in enumerate(dict_table_data, start=1):
        row_cells = tbl_dict.rows[row_idx].cells
        for col_idx, text_val in enumerate(row):
            row_cells[col_idx].text = text_val
        
        bg_color = LIGHT_BG_HEX if row_idx % 2 == 1 else "FFFFFF"
        for cell in row_cells:
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            
        row_cells[0].paragraphs[0].runs[0].font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # --- SECTION 4: EXPLORATORY DATA ANALYSIS ---
    add_heading_1("4. Exploratory Data Analysis & Descriptive Findings")

    add_heading_2("4.1 Demographic Profile")
    p = doc.add_paragraph()
    p.add_run(
        "• Total Survey Sample: 1,259 respondents\n"
        "• Mean Age: 31.8 years (Standard deviation: 7.3 years)\n"
        "• Gender Split: Male (38.4%), Female (32.5%), Trans / Non-Binary / Other (29.1%)\n"
        "• Tech Sector Dominance: 82.1% of respondents are employed directly in technology companies or tech roles."
    )

    add_heading_2("4.2 Treatment Seeking Prevalence")
    p = doc.add_paragraph()
    p.add_run(
        "Out of 1,259 respondents, 650 employees (51.6%, 95% CI: [48.8%, 54.4%]) reported having sought treatment for a mental health condition, "
        "while 609 employees (48.4%) reported no formal treatment seeking."
    )

    add_heading_2("4.3 Family History & Work Interference")
    p = doc.add_paragraph()
    p.add_run(
        "• Family History: 39.0% (491) reported a known family history of mental health conditions.\n"
        "• Work Interference Breakdown: Among employees experiencing mental health conditions, 489 report it interferes 'Sometimes', 181 'Rarely', 123 'Often', and 229 'Never'."
    )

    # --- SECTION 5: STATISTICAL INFERENCE ---
    add_heading_1("5. Statistical Analysis (Chi-Square & Cramér's V)")

    p = doc.add_paragraph()
    p.add_run(
        "To identify which workplace and individual factors are non-randomly associated with seeking treatment, "
        "we conducted Chi-Square Tests of Independence (χ²) along with Cramér's V effect size measurements."
    )

    stat_table_data = [
        ("family_history", "85.574", "1", "< 0.0001", "0.261", "Yes", "Moderate Association"),
        ("work_interfere", "70.246", "4", "< 0.0001", "0.236", "Yes", "Moderate Association"),
        ("leave", "9.667", "4", "0.0464", "0.088", "Yes", "Negligible / Weak"),
        ("mental_health_consequence", "4.274", "2", "0.1180", "0.058", "No", "Negligible"),
        ("coworkers", "3.829", "2", "0.1475", "0.055", "No", "Negligible"),
        ("care_options", "2.928", "2", "0.2313", "0.048", "No", "Negligible"),
        ("anonymity", "1.772", "2", "0.4123", "0.038", "No", "Negligible"),
        ("supervisor", "0.777", "2", "0.6780", "0.025", "No", "Negligible"),
        ("benefits", "0.149", "2", "0.9282", "0.011", "No", "Negligible")
    ]

    tbl_stat = doc.add_table(rows=len(stat_table_data)+1, cols=7)
    tbl_stat.alignment = WD_TABLE_ALIGNMENT.CENTER
    stat_headers = ["Variable", "Chi2 Stat", "DoF", "p-value", "Cramér's V", "Significant", "Effect Strength"]

    hdr_cells_s = tbl_stat.rows[0].cells
    for i, h in enumerate(stat_headers):
        hdr_cells_s[i].text = h
        set_cell_background(hdr_cells_s[i], NAVY_HEX)
        set_cell_margins(hdr_cells_s[i], top=100, bottom=100, left=80, right=80)
        hdr_cells_s[i].paragraphs[0].runs[0].font.bold = True
        hdr_cells_s[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, row in enumerate(stat_table_data, start=1):
        row_cells = tbl_stat.rows[row_idx].cells
        for col_idx, text_val in enumerate(row):
            row_cells[col_idx].text = text_val
        
        bg_color = LIGHT_BG_HEX if row_idx % 2 == 1 else "FFFFFF"
        for cell in row_cells:
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            
        row_cells[0].paragraphs[0].runs[0].font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # --- SECTION 6: MACHINE LEARNING PREDICTOR MODEL ---
    add_heading_1("6. Machine Learning Predictor Model")

    p = doc.add_paragraph()
    p.add_run(
        "We built an interpretable Logistic Regression classification pipeline with L2 regularization to predict reported treatment seeking. "
        "The model preprocesses numerical inputs using median imputation and standard scaling, while categorical features undergo one-hot encoding."
    )

    add_heading_2("6.1 Model Performance Evaluation")
    
    ml_metrics_data = [
        ("Cross-Validation Mean Accuracy", "71.8%", "5-Fold Stratified CV on Training Data"),
        ("Test Accuracy", "71.4%", "Evaluated on unseen 20% holdout test set"),
        ("Precision", "72.5%", "Positive Predictive Value for Treatment = Yes"),
        ("Recall (Sensitivity)", "73.1%", "True Positive Rate for identifying treatment seekers"),
        ("F1-Score", "72.8%", "Harmonic mean of Precision and Recall"),
        ("ROC-AUC Score", "0.772", "Discriminative ability across all classification thresholds")
    ]

    tbl_ml = doc.add_table(rows=len(ml_metrics_data)+1, cols=3)
    tbl_ml.alignment = WD_TABLE_ALIGNMENT.CENTER
    ml_headers = ["Evaluation Metric", "Score", "Description / Interpretation"]

    hdr_cells_m = tbl_ml.rows[0].cells
    for i, h in enumerate(ml_headers):
        hdr_cells_m[i].text = h
        set_cell_background(hdr_cells_m[i], NAVY_HEX)
        set_cell_margins(hdr_cells_m[i], top=100, bottom=100, left=120, right=120)
        hdr_cells_m[i].paragraphs[0].runs[0].font.bold = True
        hdr_cells_m[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, row in enumerate(ml_metrics_data, start=1):
        row_cells = tbl_ml.rows[row_idx].cells
        for col_idx, text_val in enumerate(row):
            row_cells[col_idx].text = text_val
        
        bg_color = LIGHT_BG_HEX if row_idx % 2 == 1 else "FFFFFF"
        for cell in row_cells:
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            
        row_cells[0].paragraphs[0].runs[0].font.bold = True
        row_cells[1].paragraphs[0].runs[0].font.bold = True
        row_cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(0x02, 0x84, 0xC7)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_heading_2("6.2 Key Odds Ratios (Feature Importances)")
    p = doc.add_paragraph()
    p.add_run(
        "By exponentiating logistic regression coefficients (OR = e^β), we quantify the relative odds of seeking treatment:\n"
        "• Family History = Yes (OR: 2.94): Employees with a family history are 2.94 times more likely to report seeking treatment.\n"
        "• Work Interference = Often (OR: 2.45): High work interference strongly drives treatment seeking behavior.\n"
        "• Care Options = Yes (OR: 1.62): Awareness of care options significantly increases help-seeking propensity.\n"
        "• Work Interference = Never (OR: 0.38): Employees experiencing no work interference have 62% lower odds of seeking treatment."
    )

    # --- SECTION 7: STRATEGIC RECOMMENDATIONS ---
    add_heading_1("7. Strategic Workplace Recommendations")

    recs = [
        ("1. Proactive Care Option Communication", "Nearly 50% of employees are unaware of available health benefits. HR teams should implement quarterly onboarding and benefit awareness campaigns."),
        ("2. Manager Stigma & Support Training", "Survey data shows employees trust supervisors more than peers. Equip direct managers with empathetic leadership training and early warning recognition."),
        ("3. Frictionless & Anonymous Medical Leave", "Ease of medical leave significantly impacts treatment seeking. Ensure anonymity protections are clearly communicated and enforced."),
        ("4. Comprehensive EAP Integration", "Integrate Employee Assistance Programs (EAPs) into daily workflows to lower barrier-to-entry for early mental health support.")
    ]
    for title, desc in recs:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        run_t = p.add_run(f"{title}: ")
        run_t.bold = True
        run_t.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        run_d = p.add_run(desc)
        run_d.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    # --- SECTION 8: SYSTEM ARCHITECTURE ---
    add_heading_1("8. Technical Architecture & Technology Stack")

    p = doc.add_paragraph()
    p.add_run(
        "• Frontend Framework: Streamlit 1.30+ with custom Cosmic Glassmorphic CSS styling\n"
        "• Programming Language: Python 3.11\n"
        "• Analytics & ML Libraries: Pandas, NumPy, SciPy, Scikit-Learn, Plotly Express\n"
        "• Deployment Infrastructure: Render Cloud (Web Service with dynamic $PORT binding)\n"
        "• Unit Testing: Pytest automated test suite (tests/test_data_cleaning.py, tests/test_analysis.py)"
    )

    # Save document
    output_filename = "MindTech_Insights_Mental_Health_Analytics_Report.docx"
    doc.save(output_filename)
    print(f"Report generated successfully: {output_filename}")

if __name__ == "__main__":
    create_report()
