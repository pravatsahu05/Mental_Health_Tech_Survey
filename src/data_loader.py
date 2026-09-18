"""
MindTech Insights — Data Loader Module
Handles secure loading and caching of raw survey data.
"""

import os
import pandas as pd
import streamlit as st
import config


@st.cache_data(show_spinner=False)
def load_raw_data(file_path: str = config.DATASET_PATH) -> pd.DataFrame:
    """
    Loads raw CSV data from the specified file path.
    Uses Streamlit caching to prevent re-reading on re-renders.

    Returns:
        pd.DataFrame: Raw survey DataFrame.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found at: {file_path}")
    
    df = pd.read_csv(file_path)
    return df
