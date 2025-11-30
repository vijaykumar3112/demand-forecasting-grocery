# api/config.py
"""
Configuration for the Demand Forecasting API
"""

import os
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Model paths
MODELS_DIR = BASE_DIR / "models"
LIGHTGBM_MODEL_PATH = MODELS_DIR / "model_lgb.txt"
XGBOOST_MODEL_PATH = MODELS_DIR / "xgboost_model.pkl"
FEATURE_NAMES_PATH = MODELS_DIR / "feature_names.pkl"

# Data paths
DATA_DIR = BASE_DIR / "data"
PROCESSED_DATA_PATH = DATA_DIR / "processed" / "features_engineered.csv"

# API Configuration
API_TITLE = "🛒 Demand Forecasting API"
API_DESCRIPTION = """
Production-ready ML API for grocery demand forecasting.

## Features
* **Real-time predictions** for any item-store combination
* **Batch predictions** for multiple items
* **Model performance** metrics and comparison
* **Business impact** calculator (ROI, waste, stockout costs)
* **SHAP explanations** for model interpretability

## Use Cases
* Inventory optimization
* Supply chain planning
* Promotion planning
* Waste reduction
"""
API_VERSION = "1.0.0"

# Business parameters
COST_PER_WASTED_ITEM = 5.0  # Average cost of wasted perishable item
COST_OF_STOCKOUT = 8.0  # Lost profit + customer dissatisfaction
PROFIT_MARGIN = 0.30  # 30% profit margin