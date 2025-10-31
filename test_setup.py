# test_setup.py - Verify all libraries installed correctly

import sys
print("=" * 60)
print("🔍 INSTALLATION VERIFICATION")
print("=" * 60)
print(f"Python: {sys.version}")
print("-" * 60)

try:
    import pandas as pd
    print(f"✅ Pandas {pd.__version__}")
except ImportError as e:
    print(f"❌ Pandas - FAILED: {e}")

try:
    import numpy as np
    print(f"✅ NumPy {np.__version__}")
except ImportError as e:
    print(f"❌ NumPy - FAILED: {e}")

try:
    import matplotlib
    print(f"✅ Matplotlib {matplotlib.__version__}")
except ImportError as e:
    print(f"❌ Matplotlib - FAILED: {e}")

try:
    import seaborn as sns
    print(f"✅ Seaborn {sns.__version__}")
except ImportError as e:
    print(f"❌ Seaborn - FAILED: {e}")

try:
    import sklearn
    print(f"✅ Scikit-learn {sklearn.__version__}")
except ImportError as e:
    print(f"❌ Scikit-learn - FAILED: {e}")

try:
    import lightgbm as lgb
    print(f"✅ LightGBM {lgb.__version__}")
except ImportError as e:
    print(f"❌ LightGBM - FAILED: {e}")

try:
    import xgboost as xgb
    print(f"✅ XGBoost {xgb.__version__}")
except ImportError as e:
    print(f"❌ XGBoost - FAILED: {e}")

try:
    from prophet import Prophet
    print(f"✅ Prophet - INSTALLED")
except ImportError as e:
    print(f"❌ Prophet - FAILED: {e}")

try:
    import streamlit
    print(f"✅ Streamlit {streamlit.__version__}")
except ImportError as e:
    print(f"❌ Streamlit - FAILED: {e}")

try:
    import fastapi
    print(f"✅ FastAPI {fastapi.__version__}")
except ImportError as e:
    print(f"❌ FastAPI - FAILED: {e}")

try:
    import mlflow
    print(f"✅ MLflow {mlflow.__version__}")
except ImportError as e:
    print(f"❌ MLflow - FAILED: {e}")

print("=" * 60)
print("🎉 VERIFICATION COMPLETE!")
print("=" * 60)