"""
Test feature generation to see what's missing
"""
import pickle
import numpy as np
from datetime import datetime

# Load feature names
with open('models/feature_names.pkl', 'rb') as f:
    expected_features = pickle.load(f)

print(f"Model expects {len(expected_features)} features:")
for i, feat in enumerate(expected_features, 1):
    print(f"  {i:2d}. {feat}")

# Simulate what engineer_features creates
features = {}
prediction_date = datetime(2024, 12, 1)
on_promotion = False
item_id = 1
store_id = 1

# Basic features
features['item_id'] = int(item_id)
features['store_id'] = int(store_id)
features['on_promotion'] = int(on_promotion)

# Date features
features['year'] = int(prediction_date.year)
features['month'] = int(prediction_date.month)
features['day'] = int(prediction_date.day)
features['day_of_week'] = int(prediction_date.weekday())
features['week_of_year'] = int(prediction_date.isocalendar()[1])
features['quarter'] = int((prediction_date.month - 1) // 3 + 1)
features['day_of_month'] = int(prediction_date.day)
features['is_weekend'] = int(prediction_date.weekday() >= 5)
features['is_month_start'] = int(prediction_date.day == 1)
features['is_month_end'] = int(prediction_date.day >= 28)

# Cyclical features
features['month_sin'] = float(np.sin(2 * np.pi * prediction_date.month / 12))
features['month_cos'] = float(np.cos(2 * np.pi * prediction_date.month / 12))
features['dow_sin'] = float(np.sin(2 * np.pi * prediction_date.weekday() / 7))
features['dow_cos'] = float(np.cos(2 * np.pi * prediction_date.weekday() / 7))

# Holiday
features['is_holiday'] = 0

# Default values for missing features
for feat in expected_features:
    if feat not in features:
        if 'lag' in feat or 'rolling' in feat:
            features[feat] = 100.0
        elif 'encoded' in feat:
            features[feat] = 0
        else:
            features[feat] = 0

# Price features
features['price'] = 5.0
features['base_price'] = 5.0
features['price_discount_pct'] = 0.0
features['price_vs_category_avg'] = 1.0

# Interactions
features['weekend_promo'] = features['is_weekend'] * features['on_promotion']
features['holiday_promo'] = features['is_holiday'] * features['on_promotion']

# Days since start
reference_date = datetime(2023, 1, 1)
features['days_since_start'] = int((prediction_date - reference_date).days)

print(f"\nGenerated {len(features)} features")
print(f"\nMissing from generated: {set(expected_features) - set(features.keys())}")
print(f"\nExtra in generated: {set(features.keys()) - set(expected_features)}")
