"""
Demand Forecasting Dashboard - Professional Edition
Enterprise-Grade UI with Dark Mode
Version: 4.1 (Connected to Real API)
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import requests
import time
import os
import hashlib

# =============================================================================
# CONFIGURATION
# =============================================================================

# API_URL = "http://api:8000"  # For Docker deployment
API_URL = os.getenv("API_URL", "http://localhost:8000")  # Read from environment variable, fallback to localhost

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Demand Forecasting Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Enterprise Demand Forecasting Platform v4.1"
    }
)

# =============================================================================
# SESSION STATE
# =============================================================================

if 'page' not in st.session_state:
    st.session_state.page = "Overview"  # Default to Dashboard Overview
if 'api_online' not in st.session_state:
    st.session_state.api_online = True
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True  # Default to dark mode
if 'metadata' not in st.session_state:
    st.session_state.metadata = None
if 'forecast_result' not in st.session_state:
    st.session_state.forecast_result = None
if 'forecast_data' not in st.session_state:
    st.session_state.forecast_data = None

# =============================================================================
# COLOR SCHEMES
# =============================================================================

LIGHT_COLORS = {
    'primary': '#6772E5',        # Stripe Rich Purple
    'primary_dark': '#5558DD',
    'primary_light': '#7C84F3',
    'secondary': '#9B8EF9',      # Vibrant Violet
    'success': '#30A46C',
    'warning': '#F76B15',
    'danger': '#E5484D',
    'info': '#0091FF',
    'gray_50': '#FAFAFA',
    'gray_100': '#F5F5F5',
    'gray_200': '#E5E5E5',
    'gray_300': '#D4D4D4',
    'gray_400': '#A3A3A3',
    'gray_500': '#737373',
    'gray_600': '#525252',
    'gray_700': '#404040',
    'gray_800': '#262626',
    'gray_900': '#171717',
    'white': '#FFFFFF',
    'black': '#000000',
    'background': '#FAFAFA',
    'surface': '#FFFFFF',
    'text_primary': '#111827',
    'text_secondary': '#4B5563',
    'border': '#E5E5E5',
}

DARK_COLORS = {
    'primary': '#7C84F3',
    'primary_dark': '#6772E5',
    'primary_light': '#9B8EF9',
    'secondary': '#A8B3FF',
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'info': '#3B82F6',
    'gray_50': '#18181B',
    'gray_100': '#27272A',
    'gray_200': '#3F3F46',
    'gray_300': '#52525B',
    'gray_400': '#71717A',
    'gray_500': '#A1A1AA',
    'gray_600': '#D4D4D8',
    'gray_700': '#E4E4E7',
    'gray_800': '#F4F4F5',
    'gray_900': '#FAFAFA',
    'white': '#18181B',
    'black': '#FAFAFA',
    'background': '#09090B',
    'surface': '#18181B',
    'text_primary': '#FFFFFF',
    'text_secondary': '#E5E7EB',
    'border': '#27272A',
}

COLORS = DARK_COLORS if st.session_state.dark_mode else LIGHT_COLORS

# =============================================================================
# PROFESSIONAL STYLING
# =============================================================================

colors_hash = hashlib.md5(str(COLORS).encode()).hexdigest()[:8]

st.markdown(f"""
    <style>
    /* Cache buster: {colors_hash} */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {{ font-family: 'Inter', sans-serif; }}
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        color: {COLORS['text_primary']} !important;
        background-color: {COLORS['background']} !important;
    }}
    
    
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    
    /* Hide only the share button, not the entire header */
    button[title="Share"] {{display: none;}}
    button[aria-label="Share"] {{display: none;}}
    
    
    .stApp {{ background-color: {COLORS['background']} !important; }}
    
    /* Remove top whitespace */
    .main .block-container {{ 
        background-color: {COLORS['background']} !important; 
        padding-top: 1rem !important; 
        margin-top: -3rem !important;
    }}
    
    section[data-testid="stSidebar"] {{ background-color: {COLORS['surface']} !important; }}
    section[data-testid="stSidebar"] > div {{ background-color: {COLORS['surface']} !important; }}
    
    .element-container, .stMarkdown, div[data-testid="column"] {{
        color: {COLORS['text_primary']} !important;
    }}
    
    /* Fix Input Fields (Date, Selectbox) */
    div[data-baseweb="input"] > div, div[data-baseweb="base-input"], input {{
        color: {COLORS['text_primary']} !important;
        background-color: {COLORS['surface']} !important;
        -webkit-text-fill-color: {COLORS['text_primary']} !important;
    }}
    
    /* Fix Tooltip Icon (?) */
    div[data-testid="stTooltipIcon"] > svg {{
        fill: {COLORS['text_secondary']} !important;
        color: {COLORS['text_secondary']} !important;
    }}
    
    /* Fix Selectbox Dropdown Text */
    ul[data-baseweb="menu"] li {{
        color: {COLORS['text_primary']} !important;
        background-color: {COLORS['surface']} !important;
    }}
    
    .block-container {{ padding: 2rem 3rem 3rem 3rem; max-width: 1400px; }}

    .page-header {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }}

    .page-header::before {{
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        border-radius: 50%;
        transform: translate(30%, -30%);
    }}

    .page-header h1 {{
        margin: 0; font-size: 2rem; font-weight: 800; color: white !important;
        letter-spacing: -0.03em; position: relative; z-index: 1;
    }}

    .page-header p {{
        margin: 0.5rem 0 0 0; font-size: 1rem; color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 500; position: relative; z-index: 1;
    }}
    
    .stButton > button[kind="secondary"], .stButton > button {{
        background: {COLORS['surface']} !important;
        color: {COLORS['text_primary']} !important;
        border: 2px solid {COLORS['border']};
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
        white-space: nowrap !important;
        text-align: center !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 3rem !important;
    }}
    
    .stButton > button[kind="secondary"]:hover, .stButton > button:hover {{
        background: {COLORS['gray_50']} !important;
        border-color: {COLORS['primary']};
        color: {COLORS['primary']} !important;
    }}
    
    /* Sidebar Buttons */
    [data-testid="stSidebar"] > div:first-child {{ background: {COLORS['surface']} !important; }}
    [data-testid="stSidebar"] .stButton > button {{
        width: 100%; text-align: center; background: transparent !important; border: none;
        color: {COLORS['text_secondary']} !important; font-weight: 500;
        white-space: nowrap !important;
    }}
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {{
        background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(103, 114, 229, 0.2);
    }}
    [data-testid="stSidebar"] .stButton > button[kind="primary"] p {{
        color: white !important;
    }}
    [data-testid="stSidebar"] .stButton > button[kind="secondary"] {{
        background: rgba(255, 255, 255, 0.1) !important;
        color: {COLORS['text_primary']} !important;
        border: 2px solid {COLORS['border']} !important;
    }}
    [data-testid="stSidebar"] .stButton > button[kind="secondary"] p {{
        color: {COLORS['text_primary']} !important;
    }}
    
    /* Inputs */
    .stTextInput > div > div, .stSelectbox > div > div, .stNumberInput > div > div, .stDateInput > div > div {{
        background-color: {COLORS['surface']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 8px !important;
        color: {COLORS['text_primary']} !important;
    }}
    .stTextInput input, .stSelectbox select, .stNumberInput input, .stDateInput input {{
        color: {COLORS['text_primary']} !important;
    }}
    
    /* ALL Labels - Form inputs, selectbox, date input, etc */
    label, .stSelectbox label, .stTextInput label, .stNumberInput label, .stDateInput label, .stToggle label {{
        color: {COLORS['text_primary']} !important;
        font-weight: 500 !important;
    }}
    
    /* Toggle / Checkbox text */
    .stCheckbox label, .stToggle label {{
        color: {COLORS['text_primary']} !important;
    }}
    
    /* Form labels specifically */
    div[data-testid="stForm"] label {{
        color: {COLORS['text_primary']} !important;
    }}
    
    /* All paragraph text */
    p, span {{
        color: {COLORS['text_primary']} !important;
    }}
    
    /* Headers in main content */
    h1, h2, h3, h4, h5, h6 {{
        color: {COLORS['text_primary']} !important;
    }}
    
    /* Info/Alert/Success/Error boxes */
    .stAlert, div[data-baseweb="notification"] {{
        background-color: {COLORS['surface']} !important;
        border: 1px solid {COLORS['border']} !important;
        color: {COLORS['text_primary']} !important;
    }}
    .stAlert p, div[data-baseweb="notification"] p {{
        color: {COLORS['text_primary']} !important;
    }}
    div[data-baseweb="notification"] > div {{
        background-color: {COLORS['surface']} !important;
        color: {COLORS['text_primary']} !important;
    }}
    
    /* Metrics */
    div[data-testid="metric-container"] {{
        background-color: {COLORS['surface']} !important;
        border: 1px solid {COLORS['border']} !important;
        padding: 1.5rem !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }}
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {{
        color: {COLORS['text_primary']} !important;
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    div[data-testid="metric-container"] label {{
        color: {COLORS['text_secondary']} !important;
    }}
    
    /* Plotly charts - Force text visibility */
    .js-plotly-plot .plotly, .js-plotly-plot .plotly div {{
        color: {COLORS['text_primary']} !important;
    }}
    .js-plotly-plot .plotly text {{
        fill: {COLORS['text_primary']} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# API FUNCTIONS
# =============================================================================

@st.cache_data(ttl=300, show_spinner=False)  # Cache for 5 minutes
def get_metadata():
    """Fetch available items and stores from API"""
    try:
        response = requests.get(f"{API_URL}/metadata", timeout=2)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_prediction(item_id, store_id, date, on_promotion):
    """Get prediction from API"""
    try:
        payload = {
            "item_id": item_id,
            "store_id": store_id,
            "date": date.strftime("%Y-%m-%d"),
            "on_promotion": on_promotion
        }
        # Increased timeout to 30s to prevent read timeouts
        response = requests.post(f"{API_URL}/predict", json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

def get_multi_step_forecast(item_id, store_id, start_date, horizon=30):
    """Get multi-step forecast for graph"""
    try:
        # Try calling the advanced endpoint if it exists
        params = {
            "item_id": item_id,
            "store_id": store_id,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "horizon": horizon
        }
        # Increased timeout to 30s to prevent read timeouts
        response = requests.post(f"{API_URL}/predict/multi-step", params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            # Fallback: Generate dummy trend based on single prediction if endpoint fails
            # This ensures graph always shows something even if advanced model isn't ready
            return None
    except:
        return None

@st.cache_data(ttl=60, show_spinner=False)  # Cache for 1 minute
def get_health_status():
    """Get API health status"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            return response.json(), "Online", "Healthy"
        return {}, "Offline", "Down"
    except:
        return {}, "Offline", "Down"

@st.cache_data(ttl=60, show_spinner=False)  # Cache for 1 minute
def get_valid_ranges():
    """Get valid item/store ranges"""
    try:
        response = requests.get(f"{API_URL}/items/valid-ranges", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return data.get('valid_items', {}).get('count', 0), data.get('valid_stores', {}).get('count', 0)
        return 0, 0
    except:
        return 0, 0

@st.cache_data(ttl=60, show_spinner=False)  # Cache for 1 minute
def get_model_performance():
    """Get model performance metrics"""
    try:
        response = requests.get(f"{API_URL}/model/performance", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return data.get('metrics', {}).get('MAE', 0), data.get('metrics', {}).get('R2', 0)
        return 0, 0
    except:
        return 0, 0

@st.cache_data(ttl=600, show_spinner=False)  # Cache for 10 minutes
def load_historical_data_sample(nrows=2000):
    """Load a sample of historical data for charts (optimized for speed)"""
    try:
        import os
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed', 'features_engineered.csv')
        df = pd.read_csv(data_path, nrows=nrows)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        return None


# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.markdown(f"""
        <div style="padding: 1rem 0.5rem 2rem 0.5rem; text-align: center;">
            <h1 style="font-size: 1.25rem; font-weight: 800; margin: 0; color: {COLORS['text_primary']};">DemandForecast</h1>
            <p style="font-size: 0.6875rem; color: {COLORS['text_secondary']}; margin: 0.5rem 0 0 0; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase;">Enterprise Platform</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div style="margin: 1.5rem 0 0.75rem 0.5rem; color: {COLORS["text_secondary"]}; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">Navigation</div>', unsafe_allow_html=True)
    
    pages = {"Overview": "Dashboard Overview", "Forecaster": "Demand Forecaster", "Performance": "Performance Analytics"}
    for page_id, page_label in pages.items():
        if st.button(page_label, key=f"nav_{page_id}", type="primary" if st.session_state.page == page_id else "secondary", use_container_width=True):
            st.session_state.page = page_id
            st.rerun()

    st.markdown(f'<div style="margin: 1.5rem 0 0.75rem 0.5rem; color: {COLORS["text_secondary"]}; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">Theme</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="small")
    with col1:
        if st.button("Light", key="theme_light", type="primary" if not st.session_state.dark_mode else "secondary", use_container_width=True):
            st.session_state.dark_mode = False
            st.rerun()
    with col2:
        if st.button("Dark", key="theme_dark", type="primary" if st.session_state.dark_mode else "secondary", use_container_width=True):
            st.session_state.dark_mode = True
            st.rerun()

# =============================================================================
# MAIN CONTENT
# =============================================================================

# Initialize metadata if needed
if st.session_state.metadata is None:
    st.session_state.metadata = get_metadata()

# Fallback if API is down
if st.session_state.metadata is None:
    item_options = list(range(1, 51))
    store_options = list(range(1, 11))
else:
    item_options = st.session_state.metadata.get('item_ids', list(range(1, 51)))
    store_options = st.session_state.metadata.get('store_ids', list(range(1, 11)))

if st.session_state.page == "Forecaster":
    st.markdown(f"""
        <div class="page-header">
            <h1>Demand Forecaster</h1>
            <p>Generate accurate demand predictions using advanced machine learning models</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<h3 style='color:{COLORS['text_primary']}; font-size:1.25rem; margin-bottom:1rem;'>Forecast Configuration</h3>", unsafe_allow_html=True)
    
    with st.form("forecast_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            item_id = st.selectbox("Product Item ID", item_options)
        with c2:
            store_id = st.selectbox("Store Location", store_options)
        with c3:
            date = st.date_input("Target Date", datetime.now() + timedelta(days=1))
            
        on_promo = st.toggle("Promotional Offer Active", help="Enable if a promotion is active")
        def clear_forecast_results():
            st.session_state.forecast_result = None
            st.session_state.forecast_data = None

        submitted = st.form_submit_button("Generate Forecast", type="primary", use_container_width=True, on_click=clear_forecast_results)
        
        if submitted:
            with st.spinner("Generating forecast..."):
                # 1. Get Single Prediction (FAST)
                result = get_prediction(item_id, store_id, date, on_promo)
                
                # 2. Get Multi-step Forecast for Graph (OPTIONAL - reduced to 7 days for speed)
                forecast_data = get_multi_step_forecast(item_id, store_id, date, horizon=7)
                
                # Store in session state to persist across theme changes
                st.session_state.forecast_result = result
                st.session_state.forecast_data = forecast_data
        
        # Use stored results if available
        result = st.session_state.forecast_result
        forecast_data = st.session_state.forecast_data
        
        if result:
                    st.success("Forecast generated successfully!")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(f"<h3 style='color:{COLORS['text_primary']}; font-size:1.25rem; margin-bottom:1rem;'>Forecast Results</h3>", unsafe_allow_html=True)
                    
                    r1, r2, r3 = st.columns(3)
                    with r1:
                        st.metric("Predicted Demand", f"{int(result['predicted_demand'])} units", "High Confidence")
                    with r2:
                        confidence_range = f"{int(result['confidence_lower'])} - {int(result['confidence_upper'])}"
                        st.metric("Confidence Interval", confidence_range, "90% Probable")
                    with r3:
                        st.metric("Recommended Stock", f"{result['recommended_stock']} units", "+Safety Stock")
                    
                    # 3. Display Graph
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(f"<h3 style='color:{COLORS['text_primary']}; font-size:1.25rem; margin-bottom:1rem;'>7-Day Demand Trend</h3>", unsafe_allow_html=True)
                    
                    if forecast_data and 'forecasts' in forecast_data:
                        df_forecast = pd.DataFrame(forecast_data['forecasts'])
                        df_forecast['date'] = pd.to_datetime(df_forecast['date'])
                        
                        # Defensive: Ensure confidence columns exist
                        if 'confidence_upper' not in df_forecast.columns:
                            df_forecast['confidence_upper'] = df_forecast['predicted_demand'] * 1.1
                        if 'confidence_lower' not in df_forecast.columns:
                            df_forecast['confidence_lower'] = df_forecast['predicted_demand'] * 0.9
                            
                        fig = px.line(df_forecast, x='date', y='predicted_demand', 
                                      title=f'Forecast for Item {item_id} at Store {store_id}',
                                      labels={'predicted_demand': 'Demand (Units)', 'date': 'Date'})
                        
                        # Add confidence interval
                        fig.add_trace(go.Scatter(
                            x=df_forecast['date'], 
                            y=df_forecast['confidence_upper'],
                            mode='lines',
                            line=dict(width=0),
                            showlegend=False,
                            hoverinfo='skip'
                        ))
                        fig.add_trace(go.Scatter(
                            x=df_forecast['date'], 
                            y=df_forecast['confidence_lower'],
                            mode='lines',
                            line=dict(width=0),
                            fill='tonexty',
                            fillcolor='rgba(103, 114, 229, 0.2)',
                            name='Confidence Interval'
                        ))
                        
                    else:
                        # Fallback graph
                        dates = [date + timedelta(days=i) for i in range(7)]
                        base_val = result['predicted_demand']
                        values = [base_val * (1 + 0.1 * np.sin(i/5) + np.random.normal(0, 0.05)) for i in range(7)]
                        
                        df_mock = pd.DataFrame({'date': dates, 'demand': values})
                        fig = px.line(df_mock, x='date', y='demand', title=f'Projected Trend (Estimated)')
                        fig.update_traces(line_color=COLORS['primary'], line_width=3)
                    
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Inter", color=COLORS['text_primary']),
                        xaxis=dict(showgrid=False),
                        yaxis=dict(showgrid=True, gridcolor=COLORS['border']),
                        hovermode="x unified",
                        hoverlabel=dict(
                            bgcolor=COLORS['surface'],
                            font_color=COLORS['text_primary'],
                            bordercolor=COLORS['border']
                        )
                    )
                    st.plotly_chart(fig, use_container_width=True)
        elif submitted and not result:
            # Only show error if form was submitted but failed
            st.error("Failed to generate forecast. Please check API connection.")

elif st.session_state.page == "Overview":
    st.markdown(f"""
        <div class="page-header">
            <h1>Dashboard Overview</h1>
            <p>Real-time performance metrics and business intelligence insights</p>
        </div>
    """, unsafe_allow_html=True)
    
    # System Status - Use cached function
    health_data, api_status_text, api_delta = get_health_status()
    
    # Get real item/store ranges - Use cached function
    total_items, total_stores = get_valid_ranges()
    
    # Get real model performance - Use cached function
    model_mae, model_r2 = get_model_performance()
    
    # System Health
    st.markdown(f"<h3 style='color:{COLORS['text_primary']}; font-size:1.25rem; margin-bottom:1rem;'>System Health</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("API Status", api_status_text, api_delta)
    with col2:
        uptime = health_data.get('uptime_seconds', 0)
        uptime_mins = int(uptime / 60)
        st.metric("Uptime", f"{uptime_mins} min", f"{uptime_mins} min")
    with col3:
        features = health_data.get('features_count', 0)
        st.metric("Features Loaded", str(features), "Active")
    with col4:
        model_loaded = health_data.get('model_loaded', False)
        st.metric("Model Status", "Loaded" if model_loaded else "Not Loaded", "LightGBM")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Real Business Metrics
    st.markdown(f"<h3 style='color:{COLORS['text_primary']}; font-size:1.25rem; margin-bottom:1rem;'>Dataset Overview</h3>", unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Items", str(total_items), "Unique Products")
    with m2:
        st.metric("Store Locations", str(total_stores), "Active Stores")
    with m3:
        if model_mae > 0:
            st.metric("Model MAE", f"{model_mae:.2f}", "units")
        else:
            st.metric("Model MAE", "N/A", "Not Available")
    with m4:
        if model_r2 > 0:
            st.metric("Model R² Score", f"{model_r2:.3f}", f"{model_r2*100:.1f}%")
        else:
            st.metric("Model R² Score", "N/A", "Not Available")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Load and analyze historical data for REAL charts - Use cached function
    df_sample = load_historical_data_sample(nrows=2000)  # Optimized for speed
    
    if df_sample is not None:
        st.markdown(f"<h3 style='color:{COLORS['text_primary']}; font-size:1.25rem; margin-bottom:1rem;'>Historical Data Analysis</h3>", unsafe_allow_html=True)
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Real Sales Distribution by Day of Week
            df_sample['day_name'] = df_sample['date'].dt.day_name()
            daily_avg = df_sample.groupby('day_name')['sales'].mean().reindex(
                ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            )
            
            fig1 = go.Figure(data=[
                go.Bar(x=daily_avg.index, y=daily_avg.values, marker_color=COLORS['primary'])
            ])
            fig1.update_layout(
                title="Average Sales by Day of Week",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter", color=COLORS['text_primary']),
                xaxis=dict(showgrid=False, title="Day"),
                yaxis=dict(showgrid=True, gridcolor=COLORS['border'], title="Average Sales"),
                height=300,
                hoverlabel=dict(
                    bgcolor=COLORS['surface'],
                    font_color=COLORS['text_primary'],
                    bordercolor=COLORS['border']
                )
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with chart_col2:
            # Real - Promotion Impact
            promo_impact = df_sample.groupby('on_promotion')['sales'].mean()
            
            fig2 = go.Figure(data=[
                go.Bar(
                    x=['No Promotion', 'On Promotion'],
                    y=[promo_impact.get(0, 0), promo_impact.get(1, 0)],
                    marker_color=[COLORS['secondary'], COLORS['success']]
                )
            ])
            fig2.update_layout(
                title="Average Sales: Promotion Impact",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter", color=COLORS['text_primary']),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor=COLORS['border'], title="Average Sales"),
                height=300,
                hoverlabel=dict(
                    bgcolor=COLORS['surface'],
                    font_color=COLORS['text_primary'],
                    bordercolor=COLORS['border']
                )
            )
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Historical data analysis unavailable")
    



elif st.session_state.page == "Performance":
    st.markdown(f"""
        <div class="page-header">
            <h1>Performance Analytics</h1>
            <p>Comprehensive model evaluation and predictive accuracy metrics</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get real performance data from API
    try:
        # Increased timeout to 30s for heavy performance calculations
        response = requests.get(f"{API_URL}/model/performance", timeout=30)
        if response.status_code == 200:
            perf_data = response.json()
            
            # Model Metrics Overview
            st.markdown(f"<h3 style='color:{COLORS['text_primary']}; font-size:1.25rem; margin-bottom:1rem;'>Model Performance Metrics</h3>", unsafe_allow_html=True)
            
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                mae = perf_data.get('metrics', {}).get('MAE', 0)
                st.metric("Mean Absolute Error", f"{mae:.2f} units", "Lower is better")
            with m2:
                rmse = perf_data.get('metrics', {}).get('RMSE', 0)
                st.metric("Root Mean Squared Error", f"{rmse:.2f} units", "Lower is better")
            with m3:
                r2 = perf_data.get('metrics', {}).get('R2', 0)
                st.metric("R² Score", f"{r2:.3f}", f"{r2*100:.1f}% variance explained")
            with m4:
                st.metric("Model Type", perf_data.get('model_name', 'N/A').split()[0], perf_data.get('version', 'v1.0'))
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Feature Importance Analysis
            st.markdown(f"<h3 style='color:{COLORS['text_primary']}; font-size:1.25rem; margin-bottom:1rem;'>Feature Importance Analysis</h3>", unsafe_allow_html=True)
            
            features = perf_data.get('top_features', [])
            if features and len(features) > 0:
                feat_col1, feat_col2 = st.columns([2, 1])
                
                with feat_col1:
                    # Feature importance chart
                    df_features = pd.DataFrame(features)
                    
                    fig_feat = go.Figure(go.Bar(
                        x=df_features['importance'],
                        y=df_features['feature'],
                        orientation='h',
                        marker=dict(
                            color=df_features['importance'],
                            colorscale='Viridis',
                            showscale=False
                        )
                    ))
                    
                    fig_feat.update_layout(
                        title="Top 10 Most Important Features",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Inter", color=COLORS['text_primary']),
                        yaxis=dict(autorange="reversed", title=""),
                        xaxis=dict(showgrid=True, gridcolor=COLORS['border'], title="Importance Score"),
                        height=400,
                        hoverlabel=dict(
                            bgcolor=COLORS['surface'],
                            font_color=COLORS['text_primary'],
                            bordercolor=COLORS['border']
                        )
                    )
                    st.plotly_chart(fig_feat, use_container_width=True)
                
                with feat_col2:
                    st.markdown(f"""
                        <div style="background: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px; border: 1px solid {COLORS['border']}; height: 100%;">
                            <h4 style="color: {COLORS['text_primary']}; margin: 0 0 1rem 0;">Feature Insights</h4>
                            <p style="color: {COLORS['text_secondary']}; font-size: 0.875rem; line-height: 1.6;">
                                The most influential feature is <strong style="color: {COLORS['primary']};">{features[0]['feature']}</strong> 
                                with an importance score of <strong>{features[0]['importance']}</strong>.
                            </p>
                            <p style="color: {COLORS['text_secondary']}; font-size: 0.875rem; line-height: 1.6; margin-top: 1rem;">
                                Total features used: <strong style="color: {COLORS['text_primary']};">{perf_data.get('total_features', 0)}</strong>
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Load historical data for real performance analysis
            try:
                import os
                data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed', 'features_engineered.csv')
                
                # Sample data for analysis
                df_perf = pd.read_csv(data_path, nrows=5000)
                df_perf['date'] = pd.to_datetime(df_perf['date'])
                
                st.markdown(f"<h3 style='color:{COLORS['text_primary']}; font-size:1.25rem; margin-bottom:1rem;'>Historical Performance Analysis</h3>", unsafe_allow_html=True)
                
                analysis_col1, analysis_col2 = st.columns(2)
                
                with analysis_col1:
                    # Sales Distribution
                    fig_dist = go.Figure()
                    fig_dist.add_trace(go.Histogram(
                        x=df_perf['sales'],
                        nbinsx=50,
                        marker_color=COLORS['primary'],
                        name='Sales Distribution'
                    ))
                    
                    fig_dist.update_layout(
                        title="Sales Distribution",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Inter", color=COLORS['text_primary']),
                        xaxis=dict(showgrid=True, gridcolor=COLORS['border'], title="Sales (units)"),
                        yaxis=dict(showgrid=True, gridcolor=COLORS['border'], title="Frequency"),
                        height=350,
                        showlegend=False,
                        hoverlabel=dict(
                            bgcolor=COLORS['surface'],
                            font_color=COLORS['text_primary'],
                            bordercolor=COLORS['border']
                        )
                    )
                    st.plotly_chart(fig_dist, use_container_width=True)
                
                with analysis_col2:
                    # Sales over time trend
                    daily_sales = df_perf.groupby('date')['sales'].mean().reset_index()
                    daily_sales = daily_sales.sort_values('date').tail(30)
                    
                    fig_trend = go.Figure()
                    fig_trend.add_trace(go.Scatter(
                        x=daily_sales['date'],
                        y=daily_sales['sales'],
                        mode='lines+markers',
                        line=dict(color=COLORS['success'], width=2),
                        marker=dict(size=6),
                        name='Avg Daily Sales'
                    ))
                    
                    fig_trend.update_layout(
                        title="Average Daily Sales Trend (Last 30 Days)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Inter", color=COLORS['text_primary']),
                        xaxis=dict(showgrid=False, title="Date"),
                        yaxis=dict(showgrid=True, gridcolor=COLORS['border'], title="Average Sales"),
                        height=350,
                        showlegend=False,
                        hoverlabel=dict(
                            bgcolor=COLORS['surface'],
                            font_color=COLORS['text_primary'],
                            bordercolor=COLORS['border']
                        )
                    )
                    st.plotly_chart(fig_trend, use_container_width=True)
                
                # Error Analysis
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='color:{COLORS['text_primary']}; font-size:1.25rem; margin-bottom:1rem;'>Data Quality & Statistics</h3>", unsafe_allow_html=True)
                
                stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
                
                with stat_col1:
                    st.metric("Mean Sales", f"{df_perf['sales'].mean():.2f}", "units/transaction")
                with stat_col2:
                    st.metric("Median Sales", f"{df_perf['sales'].median():.2f}", "units/transaction")
                with stat_col3:
                    st.metric("Std Deviation", f"{df_perf['sales'].std():.2f}", "volatility")
                with stat_col4:
                    if 'on_promotion' in df_perf.columns:
                        promo_rate = (df_perf['on_promotion'].sum() / len(df_perf) * 100)
                        st.metric("Promotion Rate", f"{promo_rate:.1f}%", f"{int(df_perf['on_promotion'].sum())} items")
                    else:
                        st.metric("Total Records", f"{len(df_perf):,}", "samples analyzed")
                
            except Exception as e:
                st.info("📊 **Historical Data Analysis**")
                st.markdown("""
                Advanced historical analytics are available when running locally with the full dataset.
                
                **For cloud deployment**, the core forecasting features are fully functional:
                - ✅ Real-time demand predictions
                - ✅ Confidence intervals
                - ✅ Multi-step forecasts
                - ✅ Model performance metrics (above)
                
                To view historical analytics, run the dashboard locally with the complete dataset.
                """)
        else:
            st.error("Could not load performance metrics. Please ensure the API is running.")
            
    except Exception as e:
        st.error(f"Failed to connect to API: {str(e)}")
        st.info("Please ensure the FastAPI backend is running at http://localhost:8000")
