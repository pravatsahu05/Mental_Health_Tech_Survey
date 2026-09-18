"""
MindTech Insights — Configuration Module
Contains global application constants, file paths, visual theme palettes, and default hyper-parameters.
Cosmic Glassmorphism Dark Palette ("Astra Analytics" Theme).
"""

import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# File Paths
DATASET_PATH = os.path.join(DATA_DIR, "survey.csv")
STYLE_CSS_PATH = os.path.join(ASSETS_DIR, "style.css")

# Analytical Defaults
MIN_GEO_SAMPLE_SIZE = 20  # Default minimum respondents for geographic ranking
MODEL_RANDOM_STATE = 42
MODEL_TEST_SIZE = 0.2

# Theme Color Palette (Cosmic Glassmorphism Theme)
COLOR_PALETTE = {
    "background": "#030712",
    "card_bg": "rgba(11, 16, 29, 0.70)",
    "card_border": "rgba(0, 242, 254, 0.3)",
    "primary": "#00F2FE",      # Electric Cyan
    "secondary": "#4FACFE",    # Neon Blue
    "accent": "#7F00FF",       # Cosmic Purple
    "positive": "#00E676",     # Mint Green
    "warning": "#FFD600",      # Amber Glow
    "negative": "#FF5252",     # Radiant Coral
    "neutral": "#8B949E",      # Slate Gray
    "text": "#F0F6FC",
    "text_muted": "#8B949E",
    "grid": "rgba(255, 255, 255, 0.08)"
}

# Plotly Template Default Layout Config (Cosmic Glassmorphism)
PLOTLY_THEME_CONFIG = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"family": "Plus Jakarta Sans, Inter, sans-serif", "color": "#F0F6FC", "size": 12},
    "margin": dict(l=30, r=30, t=50, b=40),
    "hoverlabel": dict(bgcolor="#0B101D", font=dict(size=13, family="Plus Jakarta Sans, sans-serif")),
    "colorway": ["#00F2FE", "#4FACFE", "#00E676", "#FFD600", "#FF5252", "#9C27B0", "#FF9800"],
    "xaxis": dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.1)"),
    "yaxis": dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.1)")
}
