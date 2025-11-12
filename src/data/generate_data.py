# src/data/generate_data.py
#cspell:words mult dow rng promo perishability
"""
Generate realistic grocery sales data for demand forecasting.

Columns:
date, year, month, day, day_of_week, day_name, is_weekend, is_holiday,
store_id, store_type, store_size, item_id, product_name, category,
perishability_days, base_price, price, on_promotion, sales, revenue
"""

from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import pandas as pd


def singularize(name: str) -> str:
    # Make simple singular names like Vegetables -> Vegetable (leave others unchanged)
    return name[:-1] if name.endswith("s") else name


def main():
    # Config (adjust if you like)
    NUM_ITEMS = 50
    NUM_STORES = 5
    NUM_DAYS = 730
    START_DATE = datetime(2023, 1, 1)
    PROMO_RATE = 0.10
    RNG_SEED = 42

    CATEGORIES = {
        "Fruits":     {"perishability": 3, "base_demand": 80,  "price_range": (2, 8)},
        "Vegetables": {"perishability": 3, "base_demand": 90,  "price_range": (1, 6)},
        "Dairy":      {"perishability": 7, "base_demand": 100, "price_range": (3, 10)},
        "Bakery":     {"perishability": 2, "base_demand": 70,  "price_range": (2, 7)},
        "Meat":       {"perishability": 5, "base_demand": 60,  "price_range": (5, 20)},
    }
    STORE_TYPES = ["Urban", "Suburban", "Rural"]

    rng = np.random.default_rng(RNG_SEED)
    dates = [START_DATE + timedelta(days=i) for i in range(NUM_DAYS)]
    rows = []

    print("Generating Grocery Sales Data")
    print("=" * 60)
    print(f"Date Range: {dates[0].date()} to {dates[-1].date()}")
    print(f"Stores:     {NUM_STORES}")
    print(f"Products:   {NUM_ITEMS}")
    print(f"Total rows: {NUM_ITEMS * NUM_STORES * NUM_DAYS:,}")
    print("=" * 60)

    for item_id in range(1, NUM_ITEMS + 1):
        category = rng.choice(list(CATEGORIES.keys()))
        info = CATEGORIES[category]
        base_price = rng.uniform(*info["price_range"])
        product_name = f"{singularize(category)}_{item_id}"

        for store_id in range(1, NUM_STORES + 1):
            store_type = rng.choice(STORE_TYPES)
            store_size = rng.choice(["Small", "Medium", "Large"])
            loc_mult = 1.3 if store_type == "Urban" else (1.0 if store_type == "Suburban" else 0.7)

            for d in dates:
                base_demand = info["base_demand"]
                dow = d.weekday()

                # Weekly pattern
                dow_mult = 1.4 if dow >= 5 else (1.2 if dow == 4 else 1.0)

                # Seasonality
                month = d.month
                month_mult = 1.5 if month in (11, 12) else (1.2 if month in (6, 7, 8) else 1.0)

                # Trend (+10% over the period)
                days_since_start = (d - START_DATE).days
                trend = 1.0 + (days_since_start / max(1, NUM_DAYS)) * 0.10

                # Promotions
                on_promotion = rng.random() < PROMO_RATE
                promo_mult = 1.6 if on_promotion else 1.0

                # Demand and realized sales
                demand = base_demand * loc_mult * dow_mult * month_mult * trend * promo_mult
                demand *= rng.uniform(0.8, 1.2)  # multiplicative noise
                sales = max(0, int(rng.poisson(demand)))

                # Price and revenue (WARNING: don't use revenue as a training feature for sales)
                price = base_price * (0.80 if on_promotion else 1.00)
                revenue = round(sales * price, 2)

                # Simple holiday flags
                is_holiday = (
                    (d.month == 1 and d.day == 1) or
                    (d.month == 7 and d.day == 4) or
                    (d.month == 12 and d.day == 25) or
                    (d.month == 11 and d.day in (22, 23, 24, 25))
                )

                rows.append({
                    "date": d.date(),
                    "year": d.year,
                    "month": d.month,
                    "day": d.day,
                    "day_of_week": dow,
                    "day_name": d.strftime("%A"),
                    "is_weekend": int(dow >= 5),
                    "is_holiday": int(is_holiday),
                    "store_id": store_id,
                    "store_type": store_type,
                    "store_size": store_size,
                    "item_id": item_id,
                    "product_name": product_name,
                    "category": category,
                    "perishability_days": info["perishability"],
                    "base_price": round(base_price, 2),
                    "price": round(price, 2),
                    "on_promotion": int(on_promotion),
                    "sales": sales,
                    "revenue": revenue,
                })

    df = pd.DataFrame(rows)

    # Robust output path: repo_root/data/raw/grocery_sales.csv
    base_dir = Path(__file__).resolve().parents[2]
    out_dir = base_dir / "data" / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "grocery_sales.csv"

    df.to_csv(out_path, index=False, encoding="utf-8")
    print("=" * 60)
    print("DATA GENERATION COMPLETE")
    print("=" * 60)
    print(f"File:    {out_path}")
    print(f"Records: {len(df):,}")
    try:
        size_mb = out_path.stat().st_size / 1024 / 1024
        print(f"Size:    {size_mb:.2f} MB")
    except Exception:
        pass

    # Preview
    with pd.option_context("display.max_columns", 0):
        print("\nFirst 10 rows:")
        print(df.head(10))
    print("\nSales by Category:")
    print(df.groupby("category")["sales"].describe())


if __name__ == "__main__":
    main()