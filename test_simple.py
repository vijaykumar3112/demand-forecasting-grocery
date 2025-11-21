#!/usr/bin/env python
"""Direct test of the predictor - no emojis"""

import sys
import traceback
import os

# Suppress LightGBM warnings
os.environ['PYTHONWARNINGS'] = 'ignore'

try:
    print("Step 1: Importing predictor...")
    from api.predictor import get_predictor
    
    print("Step 2: Loading predictor...")
    predictor = get_predictor()
    print("SUCCESS: Predictor loaded")
    
    print("\nStep 3: Attempting prediction...")
    print("  item_id=2, store_id=1, date=2025-11-22, on_promotion=False")
    
    result = predictor.predict(
        item_id=2,
        store_id=1,
        prediction_date="2025-11-22",
        on_promotion=False
    )
    
    print(f"\nSUCCESS: Prediction completed!")
    print(f"Predicted demand: {result[0]}")
    print(f"Confidence lower: {result[1]}")
    print(f"Confidence upper: {result[2]}")
    
except Exception as e:
    print(f"\nERROR occurred:")
    print(f"Type: {type(e).__name__}")
    print(f"Message: {str(e)}")
    print(f"\nTraceback:")
    traceback.print_exc()
    sys.exit(1)
