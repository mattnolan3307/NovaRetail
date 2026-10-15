"""
NovaRetail Customer Intelligence Dashboard
Author: Senior Customer Intelligence & Business Analytics Specialist
Target: Sophia Martinez & Executive Leadership Team
"""

import os
import json
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# Page Configuration & Clean Business Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="NovaRetail | Customer Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .metric-card {
        background-color: #F8F9FA;
        border: 1px solid #E9ECEF;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: 0.82rem;
        color: #6C757D;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E293B;
        margin-top: 4px;
    }
    .metric-sub {
        font-size: 0.78rem;
        color: #475569;
        margin-top: 2px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 18px;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Data Ingestion & Preprocessing
# ---------------------------------------------------------
CATEGORY_MAPPING = {
    'Books': 'Books & Media',
    'Books & Magazines': 'Books & Media',
    'Clothing': 'Apparel & Fashion',
    'Fashion': 'Apparel & Fashion',
    'Fashion & Apparel': 'Apparel & Fashion',
    'Fashion Accessories': 'Apparel & Fashion',
    'Sportswear': 'Apparel & Fashion',
    "Children's Clothing": 'Apparel & Fashion',
    'Electronics': 'Electronics',
    'Gaming': 'Electronics',
    'Home Appliances': 'Home & Living',
    'Home Decor': 'Home & Living',
    'Home Improvement': 'Home & Living',
    'Furniture': 'Home & Living',
    'Furniture & Decor': 'Home & Living',
    'Home & Garden': 'Home & Living',
    'Gardening Tools': 'Home & Living',
    'Groceries': 'Groceries & Consumables',
    'Grocery': 'Groceries & Consumables',
    'Grocery Items': 'Groceries & Consumables',
    'Food & Beverages': 'Groceries & Consumables',
    'Health & Wellness': 'Health & Beauty',
    'Health & Beauty': 'Health & Beauty',
    'Health Supplements': 'Health & Beauty',
    'Beauty Products': 'Health & Beauty',
    'Beauty & Personal Care': 'Health & Beauty',
    'Cosmetics': 'Health & Beauty',
    'Sporting Goods': 'Sports & Outdoors',
    'Sports & Outdoors': 'Sports & Outdoors',
    'Sports Equipment': 'Sports & Outdoors',
    'Outdoor Equipment': 'Sports & Outdoors',
    'Toys': 'Toys & Games',
    'Toys & Games': 'Toys & Games',
    'Office Supplies': 'Office Supplies',
    'Automotive': 'Automotive'
}

@st.cache_data
def load_data(file_path="NR_dataset.xlsx"):
    if not os.path.exists(file_path):
        st.error(f"Dataset '{file_path}' was not found in the root directory. Please place 'NR_dataset.xlsx' next to app.py.")
        return None
    
    df = pd.read_excel(file_path, sheet_name=0)
    
    # 1. Clean column strings
    df.columns = [c.strip() for c in df.columns]
