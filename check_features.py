import pickle
import pandas as pd
from pathlib import Path

# Check model features
feature_names_path = Path("models/feature_names.pkl")
with open(feature_names_path, 'rb') as f:
    feature_names = pickle.load(f)

print(f"📊 Model expects {len(feature_names)} features")
print(f"\n🔍 Feature names:")
for i, feat in enumerate(feature_names, 1):
    print(f"  {i:2d}. {feat}")

# Check processed data features
try:
    data = pd.read_csv("data/processed/features_engineered.csv")
    print(f"\n📁 Processed data has {len(data.columns)} columns")
    print(f"\n📋 Processed data columns:")
    for i, col in enumerate(data.columns, 1):
        print(f"  {i:2d}. {col}")
    
    # Find missing features
    missing_in_model = set(data.columns) - set(feature_names)
    missing_in_data = set(feature_names) - set(data.columns)
    
    if missing_in_model:
        print(f"\n⚠️ Features in data but NOT in model: {missing_in_model}")
    if missing_in_data:
        print(f"\n⚠️ Features in model but NOT in data: {missing_in_data}")
        
except Exception as e:
    print(f"\n❌ Error loading data: {e}")
