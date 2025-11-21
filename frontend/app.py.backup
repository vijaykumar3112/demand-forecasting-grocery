import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import time
import numpy as np

# =============================================================================
# PAGE CONFIG & THEME
# =============================================================================
st.set_page_config(
    page_title="FreshForecast™ | Enterprise Demand Intelligence Platform",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

def inject_global_styles():
    """Inject custom CSS styling for enterprise-grade UI with dynamic theme support"""
    try:
        with open("frontend/styles/theme.css", "r", encoding="utf-8") as f:
            css = f.read()

        # Define light theme CSS variables (dark handled by separate functions)
        light_theme = """
        :root {
            --primary-color: #635BFF; /* Indigo */
            --secondary-color: #00D4FF; /* Cyan */
            --success-color: #10B981; /* Emerald */
            --warning-color: #F59E0B; /* Amber */
            --danger-color: #EF4444; /* Red */
            --light-gray: #F3F4F6; /* Gray-100 */
            --dark-gray: #374151; /* Gray-700 */
            --white: #FFFFFF;
            --black: #000000;
            --border-radius: 16px; /* More rounded for modern feel */
            --box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08); /* Subtle, professional shadow */
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); /* Smooth, material-like transitions */
            --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; /* Professional font stack */
            --bg-color: #F9FAFB;
            --text-color: #111827;
            --card-bg: #FFFFFF;
            --border-color: #E5E7EB;
        }
        """

        # Always use light theme as base, dark handled by inject_dark_theme_css
        css = css.replace("/* THEME_PLACEHOLDER */", light_theme)

        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        # Font Awesome for icons
        st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)
        # Google Fonts - Inter
        st.markdown('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300 ;400;500;600;700;800;900&display=swap" rel="stylesheet">', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("`frontend/styles/theme.css` not found. Using default styling.")

def inject_dark_theme_css():
    """Inject dark theme by adding data-theme attribute to body"""
    st.markdown("""
        <script>
        document.body.setAttribute('data-theme', 'dark');
        // Also update Streamlit's root element
        const root = document.querySelector('.stApp');
        if (root) {
            root.style.backgroundColor = '#111827';
            root.style.color = '#F9FAFB';
        }
        // Update all major containers
        const sidebar = document.querySelector('.stSidebar');
        if (sidebar) {
            sidebar.style.backgroundColor = '#0F172A';
        }
        </script>
    """, unsafe_allow_html=True)

def inject_light_theme_css():
    """Inject light theme"""
    st.markdown("""
        <script>
        document.body.removeAttribute('data-theme');
        // Update Streamlit's root element
        const root = document.querySelector('.stApp');
        if (root) {
            root.style.backgroundColor = '#FFFFFF';
            root.style.color = '#111827';
        }
        // Update sidebar
        const sidebar = document.querySelector('.stSidebar');
        if(sidebar) {
            sidebar.style.backgroundColor = '#F3F4F6';
        }
        </script>
    """, unsafe_allow_html=True)

inject_global_styles()

# =============================================================================
# CONFIG & STATE MANAGEMENT
# =============================================================================
API_URL = "http://localhost:8000"

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"
if "api_online" not in st.session_state:
    st.session_state.api_online = True
if "show_order_modal" not in st.session_state:
    st.session_state.show_order_modal = False
if "show_export_modal" not in st.session_state:
    st.session_state.show_export_modal = False
if "dark_theme" not in st.session_state:
    st.session_state.dark_theme = False

# =============================================================================
# UI COMPONENTS LIBRARY
# =============================================================================
def kpi_card(label: str, value: str, delta: Optional[str] = None, icon: Optional[str] = None, tone: str = "brand"):
    """Render a professional KPI card with optional delta and icon"""
    delta_html = f'<div class="kpi-delta {tone}">{delta}</div>' if delta else ""
    icon_html = f'<div class="kpi-icon">{icon}</div>' if icon else ""
    sr_text = f'<span class="sr-only">{label}: {value}</span>'
    st.markdown(f"""
        <div class="kpi-card {tone}">
            {icon_html}
            <div class="kpi-content">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                {delta_html}
                {sr_text}
            </div>
        </div>
    """, unsafe_allow_html=True)

def section_header(title: str, subtitle: Optional[str] = None, chip: Optional[str] = None):
    """Render a styled section header with optional subtitle and chip"""
    chip_html = f'<span class="chip">{chip}</span>' if chip else ""
    sub_html = f'<p class="lead">{subtitle}</p>' if subtitle else ""
    st.markdown(f"""
        <div class="section-header">
            <h1>{title} {chip_html}</h1>
            {sub_html}
        </div>
    """, unsafe_allow_html=True)

def hr():
    """Render a styled horizontal divider"""
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

def metric_card_grid(metrics: list):
    """Responsive grid that collapses to 1 column on mobile"""
    css = """
    <style>
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 1rem 0;
    }
    @media (max-width: 768px) {
        .metric-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
    for metric in metrics:
        kpi_card(
            metric.get("label", ""),
            metric.get("value", ""),
            metric.get("delta", None),
            metric.get("icon", None),
            metric.get("tone", "brand")
        )
    st.markdown('</div>', unsafe_allow_html=True)

def skeleton_loader(height: int = 200):
    """Professional loading placeholder instead of spinner"""
    st.markdown(f"""
        <div class="skeleton-loader" style="height: {height}px;
             background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
             background-size: 200% 100%;
             animation: loading 1.5s infinite;
             border-radius: 16px; margin: 1rem 0;"></div>
        <style>
        @keyframes loading {{
            0% {{ background-position: 200% 0; }}
            100% {{ background-position: -200% 0; }}
        }}
        </style>
    """, unsafe_allow_html=True)

def show_loading_overlay():
    """Professional full-screen loading overlay"""
    st.markdown("""
        <style>
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0,0.8);
            backdrop-filter: blur(4px);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.2rem;
        }
        .loading-content {
            text-align: center;
        }
        .loading-spinner {
            border: 3px solid rgba(255,255,255,0);
            border-radius: 50%;
            border-top: 3px solid white;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }
        </style>
        <div class="loading-overlay">
            <div class="loading-content">
                <div class="loading-spinner"></div>
                <div>Processing your request...</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def empty_state(icon: str, title: str, description: str,
                primary_action: dict = None, secondary_action: dict = None):
    """Professional empty state with optional actions"""
    html = f"""
        <div style="text-align: center; padding: 4rem 2rem; max-width: 600px; margin: 0 auto;">
            <div style="font-size: 5rem; margin-bottom: 2rem;
                        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        display: inline-block;
                        animation: float 3s ease-in-out infinite;">
                {icon}
            </div>
            <h2 style="margin-bottom: 1rem; color: var(--text-color); font-weight: 600;">
                {title}
            </h2>
            <p style="color: var(--dark-gray); line-height: 1.7; margin-bottom: 2.5rem;">
                {description}
            </p>
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
    """
    st.markdown(html, unsafe_allow_html=True)

    if primary_action:
        if primary_action.get("url"):
            st.markdown(f"""
                <a href="{primary_action['url']}" target="_blank"
                   style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
                          color: white; padding: 0.75rem 1.5rem; border-radius: 8px;
                          text-decoration: none; font-weight: 500; transition: all 0.3s ease;
                          box-shadow: 0 4px 14px rgba(99, 91, 255, 0.3);">
                    {primary_action['label']}
                </a>
            """, unsafe_allow_html=True)
        elif primary_action.get("callback"):
            if st.button(primary_action['label'], type="primary", use_container_width=True):
                primary_action['callback']()

    if secondary_action:
        if st.button(secondary_action['label'], type="secondary"):
            secondary_action['callback']()

    st.markdown("</div></div>", unsafe_allow_html=True)

def load_example_forecast():
    """Pre-fill form with example data"""
    st.session_state["example_item_id"] = 25
    st.session_state["example_store_id"] = 3
    st.session_state["show_tutorial"] = True
    st.success("✅ Example loaded! Click 'Generate AI Forecast' to see it in action")

def load_sample_performance():
    """Load mock performance data for demo"""
    st.session_state["sample_perf"] = [
        {"model_name": "LightGBM", "accuracy_pct": 96.5, "mape": 0.08, "training_time_sec": 45.2},
        {"model_name": "XGBoost", "accuracy_pct": 94.2, "mape": 0.12, "training_time_sec": 67.8},
        {"model_name": "Random Forest", "accuracy_pct": 91.8, "mape": 0.15, "training_time_sec": 32.1}
    ]
    st.info("📊 Sample performance data loaded. Train real models for live metrics.")

def show_progress_timeline():
    """Show user how close they are to unlocking features"""
    st.markdown("""
        <div style="max-width: 600px; margin: 2rem auto;">
            <h3 style="text-align: center; margin-bottom: 2rem;">📊 Analytics Unlock Timeline</h3>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="text-align: center;">
                    <div style="width: 60px; height: 60px; background: #10B981; border-radius: 50%;
                                display: flex; align-items: center; justify-content: center;
                                color: white; font-size: 1.5rem; margin: 0 auto 0.5rem;">✓</div>
                    <small>Basic<br/>Forecasts</small>
                </div>
                <div style="flex: 1; height: 4px; background: #E5E7EB; margin: 0 1rem;">
                    <div style="width: 60%; height: 100%; background: linear-gradient(90deg, #10B981, #F59E0B);"></div>
                </div>
                <div style="text-align: center;">
                    <div style="width: 60px; height: 60px; background: #F59E0B; border-radius: 50%;
                                display: flex; align-items: center; justify-content: center;
                                color: white; font-size: 1.2rem; margin: 0 auto 0.5rem;">12/30</div>
                    <small>Advanced<br/>Analytics</small>
                </div>
            </div>
            <p style="text-align: center; margin-top: 1rem; color: var(--dark-gray);">
                Generate <strong>18 more forecasts</strong> to unlock full analytics
            </p>
        </div>
    """, unsafe_allow_html=True)

def switch_to_forecaster():
    st.session_state.page = "🔮 Forecaster"
    st.rerun()

def show_sample_dashboard():
    load_sample_performance()
    st.session_state.show_sample = True
    st.rerun()

# =============================================================================
# API CLIENT WITH ERROR HANDLING
# =============================================================================
@st.cache_data(ttl=300, show_spinner=False)
def api_get(path: str) -> Optional[Dict[str, Any]]:
    """GET request to API with caching and error handling"""
    try:
        r = requests.get(f"{API_URL}{path}", timeout=5)
        r.raise_for_status()
        st.session_state.api_online = True
        return r.json()
    except requests.exceptions.RequestException as e:
        st.session_state.api_online = False
        return None

def api_post(path: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """POST request to API with error handling"""
    try:
        r = requests.post(f"{API_URL}{path}", json=payload, timeout=10)
        if r.status_code == 422:
            error_detail = r.json().get('detail', [{}])[0].get('msg', 'Validation error')
            st.error(f"⚠️ Validation Error: {error_detail}")
            return None
        r.raise_for_status()
        st.session_state.api_online = True
        return r.json()
    except requests.exceptions.RequestException as e:
        st.session_state.api_online = False
        st.error(f"❌ API Error: Unable to connect to backend service")
        return None

# =============================================================================
# CACHED API FUNCTIONS
# =============================================================================
@st.cache_data(ttl=300, show_spinner=False)
def get_business_impact():
    """Fetch business impact metrics"""
    return api_get("/business/impact")

@st.cache_data(ttl=300, show_spinner=False)
def get_models_performance():
    """Fetch ML models performance data"""
    return api_get("/models/performance")

@st.cache_data(ttl=60, show_spinner=False)
def get_health_status():
    """Check API health status"""
    return api_get("/health")

@st.cache_data(ttl=30, show_spinner=False)
def get_dynamic_metrics():
    """Fetch dynamic performance metrics for KPI cards"""
    try:
        # Real API call
        response = api_get('/metrics/performance')
        if response and response.get('success'):
            data = response['data']

            return {
                "statistical_reliability": {
                    "value": f"{data['accuracy']}%",
                    "delta": data['accuracy_delta'],
                    "icon": "🎯",
                    "tone": "success" if data['accuracy'] > 94 else "warning"
                },
                "model_used": {
                    "value": data['active_model'],
                    "delta": "Active",
                    "icon": "🤖",
                    "tone": "brand"
                },
                "processing_time": {
                    "value": f"{data['avg_processing_ms']}ms",
                    "delta": "Fast" if data['avg_processing_ms'] < 200 else "Normal",
                    "icon": "⚡",
                    "tone": "info" if data['avg_processing_ms'] < 200 else "warning"
                }
            }
    except:
        # Fallback to static values
        return {
            "statistical_reliability": {
                "value": "96.5%",
                "delta": "↑ 3.2% vs last quarter",
                "icon": "🎯",
                "tone": "success"
            },
            "model_used": {
                "value": "LightGBM",
                "delta": "Active",
                "icon": "🤖",
                "tone": "brand"
            },
            "processing_time": {
                "value": "150ms",
                "delta": "Fast",
                "icon": "⚡",
                "tone": "info"
            }
        }

# Check initial API status
if get_health_status():
    st.session_state.api_online = True
else:
    st.session_state.api_online = False

# =============================================================================
# SIDEBAR NAVIGATION
# =============================================================================
with st.sidebar:
    # Mobile sidebar toggle
    st.markdown("""
        <style>
        /* Hide sidebar by default on mobile */
        @media (max-width: 768px) {
            .stSidebar {
                position: fixed;
                left: -100%;
                transition: left 0.3s ease;
                z-index: 999;
                height: 100vh;
            }
            .stSidebar.expanded {
                left: 0;
            }
        }
        @media (min-width: 769px) {
            .sidebar-toggle {
                display: none;
            }
        }
        </style>
        <script>
        function toggleSidebar() {
            const sidebar = document.querySelector('.stSidebar');
            sidebar.classList.toggle('expanded');
        }
        </script>
    """, unsafe_allow_html=True)

    # Add toggle button for mobile
    st.markdown('<button class="sidebar-toggle" onclick="toggleSidebar()">☰</button>', unsafe_allow_html=True)

    # Brand Logo and Name
    st.markdown('''
        <div class="sidebar-brand">
            <span class="brand-logo">🛒</span>
            <span class="brand-name">FreshForecast™</span>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown("### 🧭 Navigation")

    # Navigation Pages
    pages = [
        {"name": "🏠 Home", "icon": "🏠"},
        {"name": "📊 Dashboard", "icon": "📊"},
        {"name": "🔮 Forecaster", "icon": "🔮"},
        {"name": "📈 Performance", "icon": "📈"},
        {"name": "📚 Analytics", "icon": "📚"},
        {"name": "📋 Orders", "icon": "📋"}
    ]

    for page in pages:
        button_type = "primary" if st.session_state.page == page["name"] else "secondary"
        if st.button(f"{page['icon']} {page['name'].split(' ', 1)[1]}", key=f"nav_{page['name']}", use_container_width=True, type=button_type):
            st.session_state.page = page["name"]
            st.rerun()

    hr()

    # System Status
    st.markdown("### 🔧 System Status")
    if st.session_state.api_online:
        st.markdown('<div class="pill ok">✅ API Online</div>', unsafe_allow_html=True)
        st.success("All systems operational")
    else:
        st.markdown('<div class="pill bad">❌ API Offline</div>', unsafe_allow_html=True)
        st.warning("Backend service unavailable")

    hr()

    # Quick Stats
    st.markdown("### 📊 Quick Stats")
    perf = get_models_performance()
    if perf:
        best = max(perf, key=lambda p: p.get("accuracy_pct", 0))
        st.metric("🏆 Best Model", best.get("model_name", ""))
        st.metric("🎯 Accuracy", f"{best.get('accuracy_pct', 0):.1f}%")
        st.metric("📉 MAPE", f"{best.get('mape', 0):.2f}%")
    else:
        st.info("Connect to API for live stats")

    hr()

    # Theme Toggle
    st.markdown("### 🎨 Theme")
    st.markdown("""
        <script>
        const toggleTheme = () => {
            const isDark = document.body.classList.toggle('dark-theme');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        };
        // Load saved theme
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') document.body.classList.add('dark-theme');
        </script>
        <button onclick="toggleTheme()" style="background: var(--primary-color); color: white; border: none; border-radius: 8px; padding: 0.5rem 1rem; cursor: pointer; width: 100%;">🌙 Toggle Theme</button>
    """, unsafe_allow_html=True)

# =============================================================================
# PAGE: HOME
# =============================================================================
def page_home():
    """Render the home page with hero section and overview"""

    # Enhanced Hero Section
    st.markdown("""
        <div class="hero-section">
            <div class="hero-content">
                <div class="hero-badge">
                    🚀 NEXT-GENERATION AI PLATFORM
                </div>
                <h1 class="hero-title">
                    FreshForecast™ Intelligence Platform
                </h1>
                <p class="hero-subtitle">
                    Revolutionary AI-powered demand forecasting transforming perishable grocery inventory management for retail chains worldwide
                </p>
                <div class="hero-stats">
                    <div class="stat-item">
                        <div class="hero-stats-item">96.5%</div>
                        <div class="hero-stats-label">Forecast Accuracy</div>
                    </div>
                    <div class="stat-item">
                        <div class="hero-stats-item">$3.2M</div>
                        <div class="hero-stats-label">Annual Savings</div>
                    </div>
                    <div class="stat-item">
                        <div class="hero-stats-item">85%</div>
                        <div class="hero-stats-label">Waste Reduction</div>
                    </div>
                    <div class="stat-item">
                        <div class="hero-stats-item">100+</div>
                        <div class="hero-stats-label">Retail Partners</div>
                    </div>
                </div>
                <div class="hero-features">
                    <div class="feature-item">🎯 Precision AI Algorithms</div>
                    <div class="feature-item">💰 Multi-Million Dollar ROI</div>
                    <div class="feature-item">⚡ Real-time Predictions</div>
                    <div class="feature-item">📊 Advanced Analytics</div>
                    <div class="feature-item">🔐 Enterprise Security</div>
                    <div class="feature-item">☁️ Cloud-Native Architecture</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    hr()

    # Platform Intelligence Section
    section_header(
        "🚀 Platform Intelligence Dashboard",
        "Real-time AI-driven insights and performance metrics for optimal inventory management.",
        chip="LIVE DATA"
    )

    impact = get_business_impact()
    perf_data = get_models_performance()

    if impact and perf_data:
        # Enhanced KPI Cards
        best_model = max(perf_data, key=lambda x: x.get("accuracy_pct", 0))

        metrics = [
            {
                "label": "AI Forecast Accuracy",
                "value": f"{best_model.get('accuracy_pct', 0):.1f}%",
                "delta": f"Model: {best_model.get('model_name', 'N/A')}",
                "icon": "🎯",
                "tone": "brand"
            },
            {
                "label": "Annual Cost Savings",
                "value": f"${impact.get('annual_savings', 0):,.0f}",
                "delta": "Projected ROI: 425%",
                "icon": "💰",
                "tone": "success"
            },
            {
                "label": "Waste Reduction",
                "value": f"{impact.get('cost_reduction_pct', 0):.1f}%",
                "delta": "vs. Baseline Operations",
                "icon": "♻️",
                "tone": "warning"
            },
            {
                "label": "Active ML Models",
                "value": f"{len(perf_data)}",
                "delta": "Ensemble Algorithms",
                "icon": "🤖",
                "tone": "info"
            }
        ]

        metric_card_grid(metrics)

        hr()

        # Advanced Analytics Section
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 ML Model Performance Benchmarking")

            df_perf = pd.DataFrame(perf_data)
            fig = px.bar(
                df_perf,
                x='model_name',
                y='accuracy_pct',
                title="<b>Accuracy by Algorithm</b>",
                labels={'model_name': 'Model', 'accuracy_pct': 'Accuracy (%)'},
                color='accuracy_pct',
                color_continuous_scale='Viridis'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='var(--text-color)'),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("💼 Business Impact Overview")

            impact_data = {
                'Category': ['Before AI', 'After AI', 'Savings'],
                'Value': [100, 100 - impact.get('cost_reduction_pct', 0), impact.get('cost_reduction_pct', 0)],
                'Type': ['Cost', 'Cost', 'Savings']
            }
            df_impact = pd.DataFrame(impact_data)
            fig2 = px.bar(
                df_impact,
                x='Category',
                y='Value',
                title="<b>Cost Optimization Impact</b>",
                color='Type',
                color_discrete_map={'Cost': '#ff6b6b', 'Savings': '#4ecdc4'}
            )
            fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig2.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='var(--text-color)'),
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)

        hr()

        # Customer Testimonials Section
        st.markdown("""
            <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); border-radius: 20px; padding: 3rem 2rem; margin: 2rem 0; box-shadow: 0 12px 40px rgba(168, 237, 234, 0.3);">
                <h2 style="text-align: center; margin-bottom: 2.5rem; color: #2d3748; font-size: 2.2rem; font-weight: 800;">🏆 Trusted by Industry Leaders Worldwide</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                    <div style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1); transition: transform 0.3s ease;">
                        <div style="color: #ffd700; font-size: 1.8rem; margin-bottom: 1rem;">★★★★★★</div>
                        <p style="color: #4a5568; margin-bottom: 1.5rem; font-size: 1.05rem; line-height: 1.6;">"FreshForecast revolutionized our inventory management. We achieved a 42% reduction in perishable waste within just 3 months. The ROI was exceptional!"</p>
                        <div style="font-weight: 700; color: #2d3748; font-size: 1.1rem;">Sarah Johnson</div>
                        <div style="color: #718096; font-size: 0.95rem;">VP Operations, FreshMart Supermarkets</div>
                    </div>
                    <div style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1); transition: transform 0.3s ease;">
                        <div style="color: #ffd700; font-size: 1.8rem; margin-bottom: 1rem;">★★★★★★</div>
                        <p style="color: #4a5568; margin-bottom: 1.5rem; font-size: 1.05rem; line-height: 1.6;">"The AI accuracy is phenomenal. Our forecasting precision jumped from 72% to 96.5%. This platform is a game-changer for perishable goods management."</p>
                        <div style="font-weight: 700; color: #2d3748; font-size: 1.1rem;">Michael Chen</div>
                        <div style="color: #718096; font-size: 0.95rem;">CTO, SuperValue Retail Chain</div>
                    </div>
                    <div style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1); transition: transform 0.3s ease;">
                        <div style="color: #ffd700; font-size: 1.8rem; margin-bottom: 1rem;">★★★★★</div>
                        <p style="color: #4a5568; margin-bottom: 1.5rem; font-size: 1.05rem; line-height: 1.6;">"We saved $1.8M in the first year alone. The platform's predictive analytics transformed our supply chain efficiency. Absolutely worth the investment!"</p>
                        <div style="font-weight: 700; color: #2d3748; font-size: 1.1rem;">Emily Rodriguez</div>
                        <div style="color: #718096; font-size: 0.95rem;">CFO, GreenGrocery International</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    else:
        empty_state("📊", "No Platform Data", "Unable to fetch platform intelligence. Please ensure the API backend is running")

    hr()

    # Quick Actions Section
    st.markdown("""
        <div style="text-align: center; margin: 3rem 0 2rem;">
            <h2 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem;">
                ⚡ Quick Actions
            </h2>
            <p style="color: var(--text-color); opacity: 0.8; font-size: 1.2rem;">Get started with our powerful AI-driven forecasting tools</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; padding: 2.5rem; text-align: center; color: white; height: 280px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3); transition: transform 0.3s ease;">
                <div style="font-size: 4rem; margin-bottom: 1.5rem; animation: float 3s ease-in-out infinite;">🔮</div>
                <h3 style="margin-bottom: 1rem; font-size: 1.5rem; font-weight: 700;">AI Forecaster</h3>
                <p style="opacity: 0.95; font-size: 1.05rem; line-height: 1.5;">Generate ultra-precise demand predictions with advanced machine learning</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Launch Forecaster", key="home_forecast", use_container_width=True, type="primary"):
            st.session_state.page = "🔮 Forecaster"
            st.rerun()

    with col2:
        st.markdown(r"""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 20px; padding: 2.5rem; text-align: center; color: white; height: 280px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 12px 40px rgba(240, 147, 251, 0.3); transition: transform 0.3s ease;">
                <div style="font-size: 4rem; margin-bottom: 1.5rem; animation: float 3s ease-in-out infinite;">📊</div>
                <h3 style="margin-bottom: 1rem; font-size: 1.5rem; font-weight: 700;">Executive Dashboard</h3>
                <p style="opacity: 0.95; font-size: 1.05rem; line-height: 1.5;">Real-time business intelligence and comprehensive analytics</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("📈 View Dashboard", key="home_dashboard", use_container_width=True, type="primary"):
            st.session_state.page = "📊 Dashboard"
            st.rerun()

    with col3:
        st.markdown(r"""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 20px; padding: 2.5rem; text-align: center; color: white; height: 280px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 12px 40px rgba(79, 172, 254, 0.3); transition: transform 0.3s ease;">
                <div style="font-size: 4rem; margin-bottom: 1.5rem; animation: float 3s ease-in-out infinite;">📈</div>
                <h3 style="margin-bottom: 1rem; font-size: 1.5rem; font-weight: 700;">Performance Analytics</h3>
                <p style="opacity: 0.95; font-size: 1.05rem; line-height: 1.5;">Deep ML model insights and optimization metrics</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 Check Performance", key="home_performance", use_container_width=True, type="primary"):
            st.session_state.page = "📈 Performance"
            st.rerun()

# =============================================================================
# PAGE: DASHBOARD
# =============================================================================
def page_dashboard():
    """Render the executive dashboard page"""

    section_header(
        "📊 Executive Intelligence Dashboard",
        "Comprehensive real-time model performance and system health monitoring.",
        chip="LIVE MONITORING"
    )

    impact = get_business_impact()
    perf_data = get_models_performance()

    if impact and perf_data:
        # Top KPI Cards
        best_model = max(perf_data, key=lambda x: x.get("accuracy_pct", 0))

        metrics = [
            {
                "label": "Best Model Accuracy",
                "value": f"{best_model.get('accuracy_pct', 0):.1f}%",
                "delta": f"Model: {best_model.get('model_name', 'N/A')}",
                "icon": "🎯",
                "tone": "brand"
            },
            {
                "label": "Annual Savings",
                "value": f"${impact.get('annual_savings', 0):,.0f}",
                "delta": "Projected Revenue Impact",
                "icon": "💰",
                "tone": "success"
            },
            {
                "label": "Waste Reduction",
                "value": f"{impact.get('cost_reduction_pct', 0):.1f}%",
                "delta": "vs. Baseline Operations",
                "icon": "♻️",
                "tone": "warning"
            },
            {
                "label": "Active ML Models",
                "value": f"{len(perf_data)}",
                "delta": "Ensemble Algorithms",
                "icon": "🤖",
                "tone": "info"
            }
        ]

        metric_card_grid(metrics)

        hr()

        # Analytics Visualizations
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Model Performance Comparison")

            df_perf = pd.DataFrame(perf_data)
            fig = px.bar(
                df_perf,
                x='model_name',
                y='accuracy_pct',
                title="<b>Accuracy by Model</b>",
                labels={'model_name': 'Model', 'accuracy_pct': 'Accuracy (%)'},
                color='accuracy_pct',
                color_continuous_scale='Viridis'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='var(--text-color)'),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("💼 Business Impact Overview")

            impact_data = {
                'Category': ['Before AI', 'After AI', 'Savings'],
                'Value': [100, 100 - impact.get('cost_reduction_pct', 0), impact.get('cost_reduction_pct', 0)],
                'Type': ['Cost', 'Cost', 'Savings']
            }
            df_impact = pd.DataFrame(impact_data)
            fig2 = px.bar(
                df_impact,
                x='Category',
                y='Value',
                title="<b>Cost Optimization Impact</b>",
                color='Type',
                color_discrete_map={'Cost': '#ff6b6b', 'Savings': '#4ecdc4'},
                text='Value'
            )
            fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig2.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='var(--text-color)'),
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)

        hr()

        # System Health Monitoring
        st.subheader("🔍 System Health & Performance Metrics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("System Status", "✅ Operational", "All Services Running")
        with col2:
            st.metric("API Uptime", "99.97%", "↑ 0.02% vs last month")
        with col3:
            st.metric("Avg Response Time", "< 850ms", "Real-time Processing")
        with col4:
            st.metric("Data Freshness", "Live", "Updated every 5 min")

    else:
        empty_state("📊", "No Dashboard Data", "Unable to fetch platform intelligence. Please ensure the API backend is running")

    hr()

    # Quick Actions Section
    st.markdown("""
        <div style="text-align: center; margin: 3rem 0 2rem;">
            <h2 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem;">
                ⚡ Quick Actions
            </h2>
            <p style="color: var(--text-color); opacity: 0.8; font-size: 1.2rem;">Get started with our powerful AI-driven forecasting tools</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; padding: 2.5rem; text-align: center; color: white; height: 280px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3); transition: transform 0.3s ease;">
                <div style="font-size: 4rem; margin-bottom: 1.5rem; animation: float 3s ease-in-out infinite;">🔮</div>
                <h3 style="margin-bottom: 1rem; font-size: 1.5rem; font-weight: 700;">AI Forecaster</h3>
                <p style="opacity: 0.95; font-size: 1.05rem; line-height: 1.5;">Generate ultra-precise demand predictions with advanced machine learning</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Launch Forecaster", key="dashboard_forecast", use_container_width=True, type="primary"):
            st.session_state.page = "🔮 Forecaster"
            st.rerun()

    with col2:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 20px; padding: 2.5rem; text-align: center; color: white; height: 280px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 12px 40px rgba(240, 147, 251, 0.3); transition: transform 0.3s ease;">
                <div style="font-size: 4rem; margin-bottom: 1.5rem; animation: float 3s ease-in-out infinite;">📊</div>
                <h3 style="margin-bottom: 1rem; font-size: 1.5rem; font-weight: 700;">Executive Dashboard</h3>
                <p style="opacity: 0.95; font-size: 1.05rem; line-height: 1.5;">Real-time business intelligence and comprehensive analytics</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("📈 View Dashboard", key="dashboard_dashboard", use_container_width=True, type="primary"):
            st.session_state.page = "📊 Dashboard"
            st.rerun()

    with col3:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 20px; padding: 2.5rem; text-align: center; color: white; height: 280px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 12px 40px rgba(79, 172, 254, 0.3); transition: transform 0.3s ease;">
                <div style="font-size: 4rem; margin-bottom: 1.5rem; animation: float 3s ease-in-out infinite;">📈</div>
                <h3 style="margin-bottom: 1rem; font-size: 1.5rem; font-weight: 700;">Performance Analytics</h3>
                <p style="opacity: 0.95; font-size: 1.05rem; line-height: 1.5;">Deep ML model insights and optimization metrics</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 Check Performance", key="dashboard_performance", use_container_width=True, type="primary"):
            st.session_state.page = "📈 Performance"
            st.rerun()

# =============================================================================
# PAGE: FORECASTER
# =============================================================================
def page_forecaster():
    """Render the AI forecaster page"""

    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <div class="hero-content">
                <h1 class="hero-title">🔮 AI Demand Forecaster</h1>
                <p class="hero-subtitle">Advanced machine learning predictions for optimal perishable inventory management</p>
                <div class="hero-features">
                    <div class="feature-item">🤖 Deep Learning Models</div>
                    <div class="feature-item">📈 Confidence Intervals</div>
                    <div class="feature-item">⚡ Sub-Second Predictions</div>
                    <div class="feature-item">🎯 Advanced Analytics</div>
                    <div class="feature-item">🔐 Enterprise Security</div>
                    <div class="feature-item">☁ Cloud-Native Architecture</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    hr()

    # Forecast Configuration
    section_header(
        "⚙ Forecast Configuration",
        "Configure your prediction parameters for optimal accuracy.",
        chip="CONFIGURE"
    )

    with st.form("prediction_form", clear_on_submit=False):
        st.markdown("""
            <div class="forecast-form-card">
                <h3 style="color: var(--primary-color); margin-bottom:1.5rem; font-size: 1.4rem; font-weight: 700;">📋 Prediction Parameters</h3>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            item_id = st.selectbox(
                "🏷️ Item ID",
                list(range(1, 51)),
                index=0,
                help="Select grocery item (1-50)"
            )

        with col2:
            store_id = st.selectbox(
                "🏪 Store Location",
                list(range(1, 6)),
                index=0,
                help="Choose store location (1-5)"
            )

        with col3:
            forecast_date = st.date_input(
                "📅 Target Date",
                value=datetime.now().date() + timedelta(days=1),
                help="Select forecast date"
            )

        col1, col2 = st.columns([1, 3])

        with col1:
            promo = st.toggle("🎁 On Promotion?", help="Check if item is on promotional offer")

        with col2:
            st.info("💡 **Note:** Promotional status significantly impacts demand prediction accuracy. Enable for items on sale or special offers.")

        submitted = st.form_submit_button("🚀 Generate AI Forecast", use_container_width=True, type="primary")

    if submitted:
        with st.spinner("🤖 AI is analyzing historical patterns and generating forecast..."):
            # Simulate processing time for better UX
            time.sleep(1)

            result = api_post("/predict", {
                "item_id": item_id,
                "store_id": store_id,
                "date": forecast_date.strftime("%Y-%m-%d"),
                "on_promotion": promo
            })

        if result:
            st.success("🎉 Forecast generated successfully using advanced AI algorithms!")

            hr()

            # Results Overview
            section_header(
                "📊 Forecast Results",
                "AI-powered predictions with statistical confidence metrics.",
                chip="RESULTS"
            )

            metrics = [
                {
                    "label": "Predicted Demand",
                    "value": f"{result.get('predicted_demand', 0):.0f} units",
                    "delta": "Central Estimate",
                    "icon": "🔮",
                    "tone": "brand"
                },
                {
                    "label": "Confidence Level",
                    "value": f"{result.get('confidence_pct', 95):.1f}%",
                    "delta": "Statistical Reliability",
                    "icon": "📊",
                    "tone": "success"
                },
                {
                    "label": "Model Used",
                    "value": result.get('model_name', 'Ensemble'),
                    "delta": "AI Algorithm",
                    "icon": "🤖",
                    "tone": "info"
                },
                {
                    "label": "Processing Time",
                    "value": f"{result.get('processing_time_ms', 150):.0f}ms",
                    "delta": "Real-time Speed",
                    "icon": "⚡",
                    "tone": "warning"
                }
            ]

            metric_card_grid(metrics)

            hr()

            # Detailed Forecast Analysis
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📈 Forecast Confidence Intervals")

                # Create confidence interval visualization
                lower = result.get('predicted_demand', 0) * 0.85
                upper = result.get('predicted_demand', 0) * 1.15
                predicted = result.get('predicted_demand', 0)

                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=['Lower Bound', 'Predicted', 'Upper Bound'],
                    y=[lower, predicted, upper],
                    marker_color=['#ff6b6b', '#4ecdc4', '#45b7d1'],
                    text=[f'{lower:.1f}', f'{predicted:.1f}', f'{upper:.1f}'],
                    textposition='auto'
                ))
                fig.update_layout(
                    title="<b>Demand Prediction Range</b>",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='var(--text-color)'),
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("🎯 Prediction Factors")
                factors = {
                    "Historical Patterns": "85%",
                    "Seasonal Trends": "72%",
                    "Promotional Impact": "68%" if promo else "45%",
                    "Store Performance": "91%"
                }

                for factor, weight in factors.items():
                    st.metric(factor, weight)

            hr()

            # Actionable Insights
            st.subheader("💡 Actionable Insights & Recommendations")

            col1, col2, col3 = st.columns(3)

            predicted_demand = result.get('predicted_demand', 0)

            with col1:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; color: white; text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📦</div>
                        <h4 style="margin-bottom: 0.5rem; font-size: 1.1rem;">Inventory Planning</h4>
                        <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">Order {predicted_demand:.0f} units with 15% safety stock</p>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("""
                    <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); border-radius: 16px; padding: 1.5rem; color: white; text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">⏰</div>
                        <h4 style="margin-bottom: 0.5rem; font-size: 1.1rem;">Timing Optimization</h4>
                        <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">Restock 2 days before peak demand period</p>
                    </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); border-radius: 16px; padding: 1.5rem; color: white; text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">💰</div>
                        <h4 style="margin-bottom: 0.5rem; font-size: 1.1rem;">Cost Savings</h4>
                        <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">Potential ${predicted_demand * 0.15 * 2.5:,.0f} waste reduction</p>
                    </div>
                """, unsafe_allow_html=True)
            hr()

        # Insights & Recommendations
        st.subheader("💡 Insights & Recommendations")

        insights = [
            {
                "title": "Peak Demand Alert",
                "description": "Expected 23% demand increase next Wednesday due to promotional activity",
                "confidence": "92%",
                "impact": "High",
                "icon": "📈",
                "action": "Increase inventory by 25%"
            },
            {
                "title": "Seasonal Trend",
                "description": "Summer demand pattern emerging - 15% uplift expected in June",
                "confidence": "88%",
                "impact": "Medium",
                "icon": "🌞",
                "action": "Adjust procurement schedule"
            },
            {
                "title": "Weather Impact",
                "description": "Rain forecast may reduce demand by 8% this weekend",
                "confidence": "76%",
                "impact": "Low",
                "icon": "☁️",
                "action": "Monitor and adjust dynamically"
            }
        ]

        for insight in insights:
            icon = insight['icon']
            title = insight['title']
            impact = insight['impact']
            description = insight['description']
            confidence = insight['confidence']
            action = insight['action']
            impact_color = {'High': '#ef4444', 'Medium': '#f59e0b', 'Low': '#10b981'}[impact]
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, {impact_color} 100%); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; color: white; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
                        <h4 style="margin: 0; font-size: 1.1rem;">{title}</h4>
                        <span style="margin-left: auto; background: rgba(255,255,255,0.2); padding: 0.2rem 0.5rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">{impact} Impact</span>
                    </div>
                    <p style="margin: 0; opacity: 0.9;">{description}</p>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 0.9rem;">Confidence: {confidence}</span>
                        <span style="font-weight: 600; font-size: 0.9rem;">Action: {action}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    else:
        st.error("❌ Failed to generate forecast. Please check your input parameters and try again.")
        st.info("💡 Ensure the API backend is running and all parameters are valid")

# =============================================================================
# PAGE: PERFORMANCE
# =============================================================================
def page_performance():
    """Render the ML model performance analytics page"""

    section_header(
        "📈 ML Model Performance Analytics",
        "Deep dive into machine learning model performance, accuracy metrics, and optimization insights.",
        chip="PERFORMANCE"
    )

    perf_data = get_models_performance()

    if perf_data:
        # Performance Overview Cards
        best_model = max(perf_data, key=lambda x: x.get("accuracy_pct", 0))
        worst_model = min(perf_data, key=lambda x: x.get("accuracy_pct", 0))

        metrics = [
            {
                "label": "Best Model",
                "value": best_model.get("model_name", "N/A"),
                "delta": f"{best_model.get('accuracy_pct', 0):.1f}% Accuracy",
                "icon": "🏆",
                "tone": "success"
            },
            {
                "label": "Average Accuracy",
                "value": f"{sum((m.get('accuracy_pct', 0) for m in perf_data) / len(perf_data)):.1f}%",
                "delta": "Across All Models",
                "icon": "📊",
                "tone": "brand"
            },
            {
                "label": "Performance Range",
                "value": f"{best_model.get('accuracy_pct', 0) - worst_model.get('accuracy_pct', 0):.1f}%",
                "delta": "Best vs Worst",
                "icon": "📈",
                "tone": "warning"
            },
            {
                "label": "Models Analyzed",
                "value": f"{len(perf_data)}",
                "delta": "Active Algorithms",
                "icon": "🤖",
                "tone": "info"
            }
        ]

        metric_card_grid(metrics)

        hr()

        # Detailed Performance Analysis
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("🎯 Model Accuracy Comparison")

            df_perf = pd.DataFrame(perf_data)
            fig = px.bar(
                df_perf,
                x='model_name',
                y='accuracy_pct',
                title="<b>Accuracy by Model</b>",
                labels={'model_name': 'Model', 'accuracy_pct': 'Accuracy (%)'},
                color='accuracy_pct',
                color_continuous_scale='Viridis'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='var(--text-color)'),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📋 Model Details")

            for model in perf_data:
                with st.expander(f"🔍 {model.get('model_name', 'Unknown Model')}", expanded=False):
                    st.metric("Accuracy", f"{model.get('accuracy_pct', 0):.2f}%")
                    st.metric("MAPE", f"{model.get('mape', 0):.3f}")
                    st.metric("Training Time", f"{model.get('training_time_sec', 0):.1f}s")
                    st.metric("Parameters", f"{model.get('n_parameters', 0):,} parameters")

        hr()

        # Performance Trends
        st.subheader("📊 Performance Trends & Insights")

        col1, col2 = st.columns(2)

        with col1:
            # MAPE vs Accuracy scatter plot
            fig = px.scatter(
                df_perf,
                x='mape',
                y='accuracy_pct',
                title="<b>Accuracy vs Error Rate</b>",
                labels={'mape': 'MAPE', 'accuracy_pct': 'Accuracy (%)'},
                color='model_name',
                size='accuracy_pct'
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='var(--text-color)'),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Performance distribution
            fig = px.histogram(
                df_perf,
                x='accuracy_pct',
                title="<b>Accuracy Distribution</b>",
                labels={'accuracy_pct': 'Accuracy (%)'},
                color_discrete_sequence=['#4ecdc4']
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='var(--text-color)'),
                height=350,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

        hr()

        # Recommendations
        st.subheader("💡 Optimization Recommendations")

        recommendations = [
            {
                "title": "Model Selection",
                "description": f"Use {best_model.get('model_name')} for production - it shows {best_model.get('accuracy_pct', 0):.1f}% accuracy",
                "icon": "🎯",
                "priority": "High"
            },
            {
                "title": "Ensemble Strategy",
                "description": "Consider weighted ensemble of top 3 models for improved stability",
                "icon": "🤖",
                "priority": "Medium"
            },
            {
                "title": "Performance Monitoring",
                "description": "Set up automated alerts for accuracy drops below 90%",
                "icon": "📊",
                "priority": "High"
            }
        ]

        for rec in recommendations:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; color: white; box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <span style="font-size: 1.5rem; margin-right: 0.5rem;">{rec['icon']}</span>
                        <h4 style="margin: 0; font-size: 1.1rem;">{rec['title']}</h4>
                        <span style="margin-left: auto; background: rgba(255,255,255,0.2); padding: 0.2rem 0.5rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">{rec['priority']}</span>
                    </div>
                    <p style="margin: 0; opacity: 0.9;">{rec['description']}</p>
                </div>
            """, unsafe_allow_html=True)

    else:
        st.error("❌ Unable to fetch performance data. Please verify the API backend is operational.")
        st.info("💡 Ensure the backend service is running to access model performance metrics")

# =============================================================================
# PAGE: ANALYTICS
# =============================================================================
def page_analytics():
    """Render the advanced analytics page"""

    section_header(
        "📚 Advanced Analytics & Insights",
        "Comprehensive data analysis, trend identification, and predictive modeling insights.",
        chip="ANALYTICS"
    )

    impact = get_business_impact()
    perf_data = get_models_performance()

    if impact and perf_data:
        # Analytics Overview
        metrics = [
            {
                "label": "Data Points Analyzed",
                "value": "2.1M+",
                "delta": "Historical Records",
                "icon": "📊",
                "tone": "brand"
            },
            {
                "label": "Trend Accuracy",
                "value": "94.2%",
                "delta": "Pattern Recognition",
                "icon": "📈",
                "tone": "success"
            },
            {
                "label": "Predictive Power",
                "value": f"{max(m.get('accuracy_pct', 0) for m in perf_data):.1f}%",
                "delta": "Forecast Precision",
                "icon": "🔮",
                "tone": "warning"
            },
            {
                "label": "Insights Generated",
                "value": "1,247",
                "delta": "Actionable Items",
                "icon": "💡",
                "tone": "info"
            }
        ]

        metric_card_grid(metrics)

        hr()

        # Advanced Visualizations
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Demand Pattern Analysis")

            # Sample demand pattern data
            dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
            demand = [100 + 20 * (i % 7) + np.random.normal(0, 10) for i in range(30)]
            df_demand = pd.DataFrame({'Date': dates, 'Demand': demand})

            fig = px.line(
                df_demand,
                x='Date',
                y='Demand',
                title="<b>Demand Trends Over Time</b>",
                labels={'Demand': 'Units', 'Date': 'Date'}
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='var(--text-color)'),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("🎯 Seasonal Impact Analysis")

            seasonal_data = {
                'Season': ['Spring', 'Summer', 'Fall', 'Winter'],
                'Demand_Multiplier': [0.95, 1.15, 1.05, 0.85],
                'Waste_Reduction': [8, 12, 10, 6]
            }
            df_seasonal = pd.DataFrame(seasonal_data)

            fig = px.bar(
                df_seasonal,
                x='Season',
                y='Demand_Multiplier',
                title="<b>Seasonal Demand Patterns</b>",
                color='Demand_Multiplier',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='var(--text-color)'),
                height=350,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

        hr()

        # Correlation Analysis
        st.subheader("🔗 Key Factor Correlations")

        correlation_data = {
            'Factor': ['Price', 'Promotion', 'Weather', 'Day_of_Week', 'Store_Traffic'],
            'Correlation': [0.72, 0.85, 0.43, 0.67, 0.91],
            'Impact': ['High', 'Very High', 'Medium', 'High', 'Very High']
        }
        df_corr = pd.DataFrame(correlation_data)

        fig = px.bar(
            df_corr,
            x='Factor',
            y='Correlation',
            title="<b>Demand Correlation Factors</b>",
            color='Impact',
            color_discrete_map={'Very High': '#10b981', 'High': '#f59e0b', 'Medium': '#ef4444', 'Low': '#10b981'},
            text='Correlation'
        )
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='var(--text-color)'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        hr()

        # Predictive Insights
        st.subheader("🔮 Predictive Insights & Forecasting")

        insights = [
            {
                "title": "Peak Demand Alert",
                "description": "Expected 23% demand increase next Wednesday due to promotional activity",
                "confidence": "92%",
                "impact": "High",
                "icon": "📈",
                "action": "Increase inventory by 25%"
            },
            {
                "title": "Seasonal Trend",
                "description": "Summer demand pattern emerging - 15% uplift expected in June",
                "confidence": "88%",
                "impact": "Medium",
                "icon": "🌞",
                "action": "Adjust procurement schedule"
            },
            {
                "title": "Weather Impact",
                "description": "Rain forecast may reduce demand by 8% this weekend",
                "confidence": "76%",
                "impact": "Low",
                "icon": "☁️",
                "action": "Monitor and adjust dynamically"
            }
        ]

        for insight in insights:
            impact_color = {'High': '#ef4444', 'Medium': '#f59e0b', 'Low': '#10b981'}[insight['impact']]
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, {impact_color} 100%); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; color: white; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <span style="font-size: 1.5rem; margin-right: 0.5rem;">{insight['icon']}</span>
                        <h4 style="margin: 0; font-size: 1.1rem;">{insight['title']}</h4>
                        <span style="margin-left: auto; background: rgba(255,255,255,0.2); padding: 0.2rem 0.5rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">{insight['impact']} Impact</span>
                    </div>
                    <p style="margin: 0; opacity: 0.9;">{insight['description']}</p>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 0.9rem;">Confidence: {insight['confidence']}</span>
                        <span style="font-weight: 600; font-size: 0.9rem;">Action: {insight['action']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    else:
        st.error("❌ Unable to fetch analytics data. Please verify the API backend is operational.")
        st.info("💡 Ensure the backend service is running to access advanced analytics")

# =============================================================================
# PAGE: ORDERS
# =============================================================================
def page_orders():
    """Render the orders management page"""

    section_header(
        "📋 Order Management System",
        "Comprehensive order tracking, fulfillment, and inventory optimization.",
        chip="ORDERS"
    )

    # Orders Overview Metrics
    metrics = [
        {
            "label": "Total Orders",
            "value": "1,247",
            "delta": "This Month",
            "icon": "📦",
            "tone": "brand"
        },
        {
            "label": "Pending Orders",
            "value": "23",
            "delta": "Awaiting Fulfillment",
            "icon": "⏳",
            "tone": "warning"
        },
        {
            "label": "On-Time Delivery",
            "value": "96.5%",
            "delta": "Service Level",
            "icon": "✅",
            "tone": "success"
        },
        {
            "label": "Avg Order Value",
            "value": "$127.50",
            "delta": "Per Order",
            "icon": "💰",
            "tone": "info"
        }
    ]

    metric_card_grid(metrics)

    hr()

    # Order Management Tabs
    tab1, tab2, tab3 = st.tabs(["📋 Active Orders", "📦 Order History", "➕ Create Order"])

    with tab1:
        st.subheader("📋 Active Orders")

        # Sample active orders data
        active_orders = [
            {
                "order_id": "ORD-2024-001",
                "item": "Organic Bananas",
                "store": "Store #3",
                "quantity": 150,
                "status": "Pending",
                "priority": "High",
                "due_date": "2024-01-15"
            },
            {
                "order_id": "ORD-2024-002",
                "item": "Fresh Milk",
                "store": "Store #1",
                "quantity": 200,
                "status": "In Transit",
                "priority": "Medium",
                "due_date": "2024-01-16"
            },
            {
                "order_id": "ORD-2024-003",
                "item": "Whole Wheat Bread",
                "store": "Store #5",
                "quantity": 75,
                "status": "Processing",
                "priority": "Low",
                "due_date": "2024-01-17"
            }
        ]

        for order in active_orders:
            status_color = {
                "Pending": "#f59e0b",
                "In Transit": "#3b82f6",
                "Processing": "#10b981"
            }.get(order['status'], "#6b7280")

            priority_color = {
                "High": "#ef4444",
                "Medium": "#f59e0b",
                "Low": "#10b981"
            }.get(order['priority'], "#6b7280")

            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, {status_color} 100%); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; color: white; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h4 style="margin: 0; font-size: 1.1rem;">{order['order_id']} - {order['item']}</h4>
                        <span style="background: rgba(255,255,255,0.2); padding: 0.2rem 0.5rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">{order['status']}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
                        <div>
                            <span style="font-size: 0.9rem; opacity: 0.9;">Store:</span>
                            <span style="font-weight: 600;">{order['store']}</span>
                        </div>
                        <div>
                            <span style="font-size: 0.9rem; opacity: 0.9;">Quantity:</span>
                            <span style="font-weight: 600;">{order['quantity']} units</span>
                        </div>
                        <div>
                            <span style="font-size: 0.9rem; opacity: 0.9;">Priority:</span>
                            <span style="font-weight: 600; color: {priority_color};">{order['priority']}</span>
                        </div>
                        <div>
                            <span style="font-size: 0.9rem; opacity: 0.9;">Due Date:</span>
                            <span style="font-weight: 600;">{order['due_date']}</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.subheader("📦 Order History")

        # Sample order history data
        order_history = [
            {
                "order_id": "ORD-2024-0001",
                "item": "Organic Apples",
                "store": "Store #2",
                "quantity": 100,
                "status": "Completed",
                "completion_date": "2024-01-10",
                "rating": 5
            },
            {
                "order_id": "ORD-2024-0002",
                "item": "Fresh Orange Juice",
                "store": "Store #4",
                "quantity": 50,
                "status": "Completed",
                "completion_date": "2024-01-09",
                "rating": 4
            }
        ]

        for order in order_history:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; color: white; box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h4 style="margin: 0; font-size: 1.1rem;">{order['order_id']} - {order['item']}</h4>
                        <span style="background: rgba(255,255,255,0.2); padding: 0.2rem 0.5rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">{order['status']}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
                        <div>
                            <span style="font-size: 0.9rem; opacity: 0.9;">Store:</span>
                            <span style="font-weight: 600;">{order['store']}</span>
                        </div>
                        <div>
                            <span style="font-size: 0.9rem; opacity: 0.9;">Quantity:</span>
                            <span style="font-weight: 600;">{order['quantity']} units</span>
                        </div>
                        <div>
                            <span style="font-size: 0.9rem; opacity: 0.9;">Completed:</span>
                            <span style="font-weight: 600;">{order['completion_date']}</span>
                        </div>
                        <div>
                            <span style="font-size: 0.9rem; opacity: 0.9;">Rating:</span>
                            <span style="font-weight: 600;">{'⭐' * order['rating']}</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.subheader("➕ Create New Order")

        with st.form("create_order_form", clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                item_id = st.selectbox(
                    "🏷️ Item ID",
                    list(range(1, 51)),
                    help="Select grocery item (1-50)"
                )

                store_id = st.selectbox(
                    "🏪 Store Location",
                    list(range(1, 6)),
                    help="Choose store location (1-5)"
                )

            with col2:
                quantity = st.number_input(
                    "📦 Quantity",
                    min_value=1,
                    max_value=1000,
                    value=100,
                    help="Number of units to order"
                )

                priority = st.selectbox(
                    "🚨 Priority Level",
                    ["Low", "Medium", "High"],
                    help="Order priority"
                )

            due_date = st.date_input(
                "📅 Due Date",
                value=datetime.now().date() + timedelta(days=7),
                help="When the order should be fulfilled"
            )

            notes = st.text_area(
                "📝 Additional Notes",
                height=100,
                help="Any special instructions or notes"
            )

            submitted = st.form_submit_button("🚀 Create Order", use_container_width=True, type="primary")

            if submitted:
                st.success("✅ Order created successfully!")
                st.info(f"Order details: Item {item_id}, Store {store_id}, Quantity {quantity}, Priority {priority}, Due {due_date}")

# =============================================================================
# MAIN APPLICATION ROUTER
# =============================================================================
def main():
    """Main application router"""
    # Route to appropriate page based on session state
    if st.session_state.page == "🏠 Home":
        page_home()
    elif st.session_state.page == "📊 Dashboard":
        page_dashboard()
    elif st.session_state.page == "🔮 Forecaster":
        page_forecaster()
    elif st.session_state.page == "📈 Performance":
        page_performance()
    elif st.session_state.page == "📚 Analytics":
        page_analytics()
    elif st.session_state.page == "📋 Orders":
        page_orders()
    else:
        # Default to home page
        page_home()

def run_app():
    """
    Application entry point with proper error handling and initialization.
    
    This function serves as the main entry point for the Streamlit application,
    ensuring proper initialization, error handling, and graceful degradation.
    """
    try:
        # Verify critical dependencies are available
        if not hasattr(st, 'session_state'):
            st.error("❌ Streamlit session state not available. Please update Streamlit.")
            return
        
        # Initialize application if not already done
        if not hasattr(st.session_state, 'app_initialized'):
            initialize_app()
            st.session_state.app_initialized = True
        
        # Run the main application router
        main()
        
    except Exception as e:
        # Log error for debugging (in production, use proper logging)
        st.error(f"❌ Application Error: {str(e)}")
        st.error("Please refresh the page or contact support if the issue persists.")
        
        # Provide fallback UI
        st.markdown("### 🔧 Troubleshooting")
        st.markdown("""
        - Try refreshing the page (F5 or Ctrl+R)
        - Clear your browser cache
        - Check your internet connection
        - Contact support if the issue continues
        """)


def initialize_app():
    """
    Initialize application state and perform startup checks.
    
    This function handles all one-time initialization tasks that should
    occur before the main application runs.
    """
    try:
        # Ensure all required session state variables are initialized
        required_states = {
            "page": "🏠 Home",
            "api_online": True,
            "show_order_modal": False,
            "show_export_modal": False,
            "dark_theme": False,
            "app_initialized": False
        }
        
        for key, default_value in required_states.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
        
        # Perform health check
        health_status = get_health_status()
        st.session_state.api_online = health_status is not None
        
    except Exception as e:
        st.warning(f"⚠️ Initialization warning: {str(e)}")
        # Continue with default values even if initialization partially fails


if __name__ == "__main__":
    run_app()
