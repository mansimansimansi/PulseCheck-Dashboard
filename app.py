import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="PulseCheck | Customer Health", layout="wide")

# --- 2. CLEANING & SCORING LOGIC ---
def clean_and_score(df):
    # Strip any invisible spaces from column headers
    df.columns = df.columns.str.strip()
    
    # Standardize column names for the UI logic
    rename_map = {
        'Total Spend': 'Monthly_Spend',
        'CustomerID': 'Customer_ID',
        'Usage Frequency': 'Usage_Frequency',
        'Support Calls': 'Support_Calls',
        'Payment Delay': 'Payment_Delay'
    }
    df = df.rename(columns=rename_map)
    
    # Handle Numeric Conversion (Safety for Total Spend)
    df['Monthly_Spend'] = pd.to_numeric(df['Monthly_Spend'], errors='coerce')
    df = df.fillna(0) 

    # --- CUSTOM HEALTH SCORING ALGORITHM ---
    # We define 'Risk' as: High Late Payments + High Support Needs - Tenure
    max_delay = df['Payment_Delay'].max() if df['Payment_Delay'].max() > 0 else 1
    max_calls = df['Support_Calls'].max() if df['Support_Calls'].max() > 0 else 1
    
    df['Risk_Score'] = (
        (df['Payment_Delay'] / max_delay * 40) +    # 40% Weight: Financial Risk
        (df['Support_Calls'] / max_calls * 30) +    # 30% Weight: Resource Drain
        (100 - (df['Tenure'].clip(0, 12) * 2.5)))