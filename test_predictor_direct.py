import sys
sys.path.insert(0, '.')

from api.predictor import get_predictor
import traceback

try:
    print("Initializing predictor...")
    predictor = get_predictor()
    
    print(f"\n✅ Predictor initialized!")
    print(f"Model features: {len(predictor.feature_names)}")
    print(f"\nFeature list:")
    for i, feat in enumerate(predictor.feature_names, 1):
        print(f"  {i:2d}. {feat}")
    
    # Try a prediction
    print("\n\nTesting prediction...")
    result = predictor.predict(
        item_id=1,
        store_id=1,
        prediction_date="2024-12-01",
        on_promotion=False
    )
    print(f"✅ Prediction successful: {result}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"\nFull traceback:")
    traceback.print_exc()
