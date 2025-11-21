
import sys
import os
sys.path.append(os.getcwd())
import logging

logging.basicConfig(level=logging.INFO)

try:
    print("Attempting to import get_predictor...")
    from api.predictor import get_predictor
    print("Import successful. Attempting to call get_predictor()...")
    predictor = get_predictor()
    print("get_predictor() successful.")
    if predictor.lgb_model:
        print("Model loaded.")
    else:
        print("Model NOT loaded.")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
