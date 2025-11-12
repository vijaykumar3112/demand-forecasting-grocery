# api/__init__.py
"""
Demand Forecasting API Package

A production-ready REST API for grocery demand forecasting using ML models.
"""

__version__ = "1.0.0"
__author__ = "Vijaykumar & Sanket"
__description__ = "ML-powered demand forecasting API for perishable grocery items"

# Package-level imports (optional)
from api.app import app
from api.predictor import get_predictor
from api.config import API_VERSION

__all__ = [
    "app",
    "get_predictor",
    "API_VERSION"
]