# src/data/generate_data.py
"""
Generate realistic grocery sales data for demand forecasting
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

print("🛒 Generating Grocery Sales Data...")
print("=" * 60)

np.random.seed(42)

NUM_ITEMS = 50
NUM_STORES = 5
NUM_DAYS = 730
START_DATE = datetime(2023, 1, 1)

CATEGORIES = {
    'Fruits': {'perishability': 3, 'base_demand': 80, 'price_range': (2, 8)},
    'Vegetables': {'perishability': 3, 'base_demand': 90, 'price_range': (1, 6)},
    'Dairy': {'perishability': 7, 'base_demand': 100, 'price_range': (3, 10)},
    'Bakery': {'perishability': 2, 'base_demand': 70, 'price_range': (2, 7)},
    'Meat': {'perishability': 5, 'base_demand': 60, 'price_range': (5, 20)}
}

STORE_TYPES = ['Urban', 'Suburban', 'Rural']

dates = [START_DATE + timedelta(days=x) for x in range(NUM_DAYS)]
all_data = []

print(f"📅 Date Range: {dates[0].date()} to {dates[-1].date()}")
print(f"🏪 Stores: {NUM_STORES}")
print(f"📦 Products: {NUM_ITEMS}")
print(f"📊 Total Records: {NUM_ITEMS * NUM_STORES * NUM_DAYS:,}")
print("=" * 60)

for item_id in range(1, NUM_ITEMS + 1):
    category = np.random.choice(list(CATEGORIES.keys()))
    category_info = CATEGORIES[category]
    base_price = np.random.uniform(*category_info['price_range'])
    product_name = f"{category[:-1]}_{item_id}"
    
    for store_id in range(1, NUM_STORES + 1):
        store_type = np.random.choice(STORE_TYPES)
        store_size = np.random.choice(['Small', 'Medium', 'Large'])
        
        location_multiplier = 1.3 if store_type == 'Urban' else (1.0 if store_type == 'Suburban' else 0.7)
        
        for date in dates:
            base_demand = category_info['base_demand']
            day_of_week = date.weekday()
            
            dow_multiplier = 1.4 if day_of_week >= 5 else (1.2 if day_of_week == 4 else 1.0)
            
            month = date.month
            month_multiplier = 1.5 if month in [11, 12] else (1.2 if month in [6, 7, 8] else 1.0)
            
            days_since_start = (date - START_DATE).days
            trend = 1 + (days_since_start / NUM_DAYS) * 0.1
            
            on_promotion = np.random.random() < 0.10
            promo_multiplier = 1.6 if on_promotion else 1.0
            
            demand = (base_demand * location_multiplier * dow_multiplier * 
                     month_multiplier * trend * promo_multiplier)
            demand = demand * np.random.uniform(0.8, 1.2)
            sales = max(0, int(np.random.poisson(demand)))
            
            price = base_price * (0.80 if on_promotion else 1.0)
            revenue = sales * price
            
            is_holiday = (
                (date.month == 1 and date.day == 1) or
                (date.month == 7 and date.day == 4) or
                (date.month == 11 and date.day in [22, 23, 24, 25]) or
                (date.month == 12 and date.day == 25)
            )
            
            all_data.append({
                'date': date.date(),
                'year': date.year,
                'month': date.month,
                'day': date.day,
                'day_of_week': day_of_week,
                'day_name': date.strftime('%A'),
                'is_weekend': int(day_of_week >= 5),
                'is_holiday': int(is_holiday),
                'store_id': store_id,
                'store_type': store_type,
                'store_size': store_size,
                'item_id': item_id,
                'product_name': product_name,
                'category': category,
                'perishability_days': category_info['perishability'],
                'base_price': round(base_price, 2),
                'price': round(price, 2),
                'on_promotion': int(on_promotion),
                'sales': sales,
                'revenue': round(revenue, 2)
            })

print("📊 Creating DataFrame...")
df = pd.DataFrame(all_data)

os.makedirs('data/raw', exist_ok=True)
output_path = 'data/raw/grocery_sales.csv'
df.to_csv(output_path, index=False)

print("=" * 60)
print("✅ DATA GENERATION COMPLETE!")
print("=" * 60)
print(f"📁 File: {output_path}")
print(f"📊 Records: {len(df):,}")
print(f"💾 Size: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
print("=" * 60)
print("\nFirst 10 rows:")
print(df.head(10))
print("\nSales by Category:")
print(df.groupby('category')['sales'].describe())