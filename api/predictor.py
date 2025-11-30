"""
Model loading and prediction logic (with quantile P10/P50/P90 support)
"""

import os
import sys
import pickle
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import lightgbm as lgb

from api.config import (
    LIGHTGBM_MODEL_PATH,
    FEATURE_NAMES_PATH,
    PROCESSED_DATA_PATH,
    MODELS_DIR,  # ensure this exists in api/config.py
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DemandPredictor:
    """Handles model loading and predictions"""

    def __init__(self):
        self.lgb_model = None
        self.feature_names = None
        self.historical_data = None
        self.historical_data_indexed = {}  # Cache for O(1) lookups
        # Quantile models (optional)
        self.lgb_q10 = None
        self.lgb_q50 = None
        self.lgb_q90 = None

        self.load_models()
        self.load_historical_data()

    def load_models(self):
        """Load trained models"""
        try:
            # Check if model exists, if not create dummy
            if not LIGHTGBM_MODEL_PATH.exists():
                logger.warning(f"⚠️ Model file not found at {LIGHTGBM_MODEL_PATH}. Creating dummy model...")
                self.create_dummy_model()

            # Load point LightGBM model
            self.lgb_model = lgb.Booster(model_file=str(LIGHTGBM_MODEL_PATH))
            logger.info("✅ LightGBM model loaded")

            # Load feature names
            if not FEATURE_NAMES_PATH.exists():
                logger.warning("⚠️ Feature names not found. Creating default features...")
                self.feature_names = ['item_id', 'store_id', 'price', 'on_promotion']
                with open(FEATURE_NAMES_PATH, 'wb') as f:
                    pickle.dump(self.feature_names, f)
            else:
                with open(FEATURE_NAMES_PATH, 'rb') as f:
                    self.feature_names = pickle.load(f)
            logger.info(f"✅ Feature names loaded: {len(self.feature_names)} features")
        except Exception as e:
            logger.error(f"❌ Error loading models: {e}")
            # Create dummy model as last resort to prevent crash
            logger.warning("⚠️ Crash prevented: Creating in-memory dummy model")
            self.create_dummy_model()
            self.lgb_model = lgb.Booster(model_file=str(LIGHTGBM_MODEL_PATH))

        # ---- Quantile models (optional but preferred) ----
        try:
            q10_path = MODELS_DIR / "lgb_q10.txt"
            q50_path = MODELS_DIR / "lgb_q50.txt"
            q90_path = MODELS_DIR / "lgb_q90.txt"
            if q10_path.exists() and q50_path.exists() and q90_path.exists():
                self.lgb_q10 = lgb.Booster(model_file=str(q10_path))
                self.lgb_q50 = lgb.Booster(model_file=str(q50_path))
                self.lgb_q90 = lgb.Booster(model_file=str(q90_path))
                logger.info("✅ Quantile models (p10/p50/p90) loaded")
            else:
                logger.warning("⚠️ Quantile model files not found. Using point model fallback.")
        except Exception as e:
            logger.warning(f"⚠️ Failed to load quantile models: {e}")

    def create_dummy_model(self):
        """Create and save a dummy LightGBM model for fallback"""
        try:
            # Create dummy data
            X = np.random.rand(100, 4)
            y = np.random.rand(100)
            train_data = lgb.Dataset(X, label=y)
            
            # Train simple model
            params = {'objective': 'regression', 'verbosity': -1}
            model = lgb.train(params, train_data, num_boost_round=10)
            
            # Ensure directory exists
            LIGHTGBM_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
            
            # Save model
            model.save_model(str(LIGHTGBM_MODEL_PATH))
            logger.info(f"✅ Dummy model created at {LIGHTGBM_MODEL_PATH}")
            
            # Save dummy feature names if needed
            if not FEATURE_NAMES_PATH.exists():
                with open(FEATURE_NAMES_PATH, 'wb') as f:
                    pickle.dump(['item_id', 'store_id', 'price', 'on_promotion'], f)
        except Exception as e:
            logger.error(f"❌ Failed to create dummy model: {e}")
            raise

    def load_historical_data(self):
        """Load historical data for feature engineering"""
        try:
            self.historical_data = pd.read_csv(PROCESSED_DATA_PATH)
            self.historical_data['date'] = pd.to_datetime(self.historical_data['date'])
            
            # Create indexed cache for O(1) lookups
            logger.info("📊 Indexing historical data for fast lookups...")
            for (item_id, store_id), group in self.historical_data.groupby(['item_id', 'store_id']):
                self.historical_data_indexed[(item_id, store_id)] = group.sort_values('date')
                
            logger.info(f"✅ Historical data loaded: {len(self.historical_data):,} records")
            logger.info(f"✅ Indexed {len(self.historical_data_indexed)} item-store combinations")
        except Exception as e:
            logger.warning(f"⚠️ Could not load historical data: {e}")
            self.historical_data = None
            self.historical_data_indexed = {}

    def engineer_features(self, item_id: int, store_id: int,
                          prediction_date: datetime, on_promotion: bool) -> Dict:
        """Engineer features for a single prediction"""
        features: Dict[str, float] = {}

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

        # Holiday flag
        features['is_holiday'] = int(
            (prediction_date.month == 12 and prediction_date.day == 25) or
            (prediction_date.month == 1 and prediction_date.day == 1) or
            (prediction_date.month == 7 and prediction_date.day == 4)
        )

        # Historical signals - FAST LOOKUP
        item_store_data = self.historical_data_indexed.get((item_id, store_id))

        if item_store_data is not None and len(item_store_data) > 0:
            recent_sales = item_store_data['sales'].tail(28).values

            # Lags
            if len(recent_sales) >= 1:
                features['sales_lag_1'] = float(recent_sales[-1])
            if len(recent_sales) >= 7:
                features['sales_lag_7'] = float(recent_sales[-7])
            if len(recent_sales) >= 14:
                features['sales_lag_14'] = float(recent_sales[-14])
            if len(recent_sales) >= 28:
                features['sales_lag_28'] = float(recent_sales[-28])

            # Rollings
            if len(recent_sales) >= 7:
                features['sales_rolling_mean_7'] = float(np.mean(recent_sales[-7:]))
                features['sales_rolling_std_7'] = float(np.std(recent_sales[-7:]))
                features['sales_rolling_max_7'] = float(np.max(recent_sales[-7:]))
                features['sales_rolling_min_7'] = float(np.min(recent_sales[-7:]))

            if len(recent_sales) >= 14:
                features['sales_rolling_mean_14'] = float(np.mean(recent_sales[-14:]))
                features['sales_rolling_std_14'] = float(np.std(recent_sales[-14:]))
                features['sales_rolling_max_14'] = float(np.max(recent_sales[-14:]))
                features['sales_rolling_min_14'] = float(np.min(recent_sales[-14:]))

            if len(recent_sales) >= 28:
                features['sales_rolling_mean_28'] = float(np.mean(recent_sales[-28:]))
                features['sales_rolling_std_28'] = float(np.std(recent_sales[-28:]))
                features['sales_rolling_max_28'] = float(np.max(recent_sales[-28:]))
                features['sales_rolling_min_28'] = float(np.min(recent_sales[-28:]))

            # Encodings
            if 'category_encoded' in item_store_data.columns:
                features['category_encoded'] = int(item_store_data['category_encoded'].iloc[-1])
            if 'store_type_encoded' in item_store_data.columns:
                features['store_type_encoded'] = int(item_store_data['store_type_encoded'].iloc[-1])
            if 'store_size_encoded' in item_store_data.columns:
                features['store_size_encoded'] = int(item_store_data['store_size_encoded'].iloc[-1])
            if 'perishability_days' in item_store_data.columns:
                features['perishability_days'] = int(item_store_data['perishability_days'].iloc[-1])

        # Fill missing features with defaults
        for feat in self.feature_names:
            if feat not in features:
                if 'lag' in feat or 'rolling' in feat:
                    features[feat] = 100.0  # average sales fallback
                elif 'encoded' in feat:
                    features[feat] = 0
                else:
                    features[feat] = 0

        # Price features (defaults)
        if 'price' not in features:
            features['price'] = 5.0
        if 'base_price' not in features:
            features['base_price'] = 5.0
        if 'price_discount_pct' not in features:
            features['price_discount_pct'] = 20.0 if on_promotion else 0.0
        if 'price_vs_category_avg' not in features:
            features['price_vs_category_avg'] = 0.8 if on_promotion else 1.0

        # Interaction features
        features['weekend_promo'] = features['is_weekend'] * features['on_promotion']
        features['holiday_promo'] = features['is_holiday'] * features['on_promotion']

        # Days since start
        reference_date = datetime(2023, 1, 1)
        features['days_since_start'] = int((prediction_date - reference_date).days)

        return features

    def predict_quantiles(self, feature_array: np.ndarray) -> Tuple[float, float, float]:
        """
        Return (p10, p50, p90) using quantile LightGBM models.
        feature_array: shape (1, n_features)
        """
        if self.lgb_q10 is not None and self.lgb_q50 is not None and self.lgb_q90 is not None:
            p10 = float(self.lgb_q10.predict(feature_array)[0])
            p50 = float(self.lgb_q50.predict(feature_array)[0])
            p90 = float(self.lgb_q90.predict(feature_array)[0])
            return max(0.0, p10), max(0.0, p50), max(0.0, p90)
        else:
            # Fallback if quantile models don't exist
            base_pred = float(self.lgb_model.predict(feature_array)[0])
            base_pred = max(0.0, base_pred)
            return base_pred * 0.8, base_pred, base_pred * 1.2

    def predict(self, item_id: int, store_id: int,
                prediction_date: str, on_promotion: bool) -> Tuple[float, float, float]:
        """
        Make prediction for a single item-store-date combination
        Returns: (predicted_demand, confidence_lower, confidence_upper)
        """
        pred_date = datetime.strptime(prediction_date, '%Y-%m-%d')

        features_dict = self.engineer_features(item_id, store_id, pred_date, on_promotion)
        feature_vector = [features_dict.get(feat, 0) for feat in self.feature_names]
        feature_array = np.array(feature_vector, dtype=float).reshape(1, -1)

        # Prefer quantile models if available (P10/P50/P90)
        if self.lgb_q10 is not None and self.lgb_q50 is not None and self.lgb_q90 is not None:
            p10, p50, p90 = self.predict_quantiles(feature_array)
            return p50, p10, p90

        # Fallback: point model ±20% band
        prediction = float(self.lgb_model.predict(feature_array)[0])
        prediction = max(0.0, prediction)
        confidence_lower = max(0.0, prediction * 0.8)
        confidence_upper = prediction * 1.2
        return prediction, confidence_lower, confidence_upper

    def calculate_recommended_stock(self, predicted_demand: float,
                                    confidence_upper: float,
                                    perishability_days: int = 3) -> int:
        """Calculate recommended stock level"""
        safety_stock = (confidence_upper - predicted_demand) * 0.5
        recommended = predicted_demand + safety_stock
        return int(np.ceil(recommended))

    def has_historical_data(self, item_id: int, store_id: int) -> bool:
        """Check if historical data exists for item-store combination"""
        if self.historical_data is None:
            return False
        return len(self.historical_data[
            (self.historical_data['item_id'] == item_id) &
            (self.historical_data['store_id'] == store_id)
        ]) > 0


# Global predictor instance
predictor = None


def get_predictor() -> DemandPredictor:
    """Get or create predictor instance"""
    global predictor
    if predictor is None:
        predictor = DemandPredictor()
    return predictor


# -------- Advanced multi-step forecaster support (optional) --------
try:
    from src.models.multi_step_forecaster import MultiStepForecaster
except ImportError as _e:
    try:
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from src.models.multi_step_forecaster import MultiStepForecaster  # type: ignore
    except Exception as _inner_e:
        logger.warning(f"Multi-step forecaster not available: {_inner_e}")
        MultiStepForecaster = None  # type: ignore


if MultiStepForecaster:

    class DemandPredictorAdvanced(DemandPredictor):
        """Extended predictor with multi-step capabilities"""

        def __init__(self):
            super().__init__()
            self.multi_step_forecaster = None
            if self.lgb_model and self.feature_names and self.historical_data is not None:
                self.multi_step_forecaster = MultiStepForecaster(
                    self.lgb_model,
                    self.feature_names,
                    self.historical_data
                )
                logger.info("✅ Multi-step forecaster initialized")

        def forecast_multi_step(self, item_id: int, store_id: int,
                                start_date: str, horizon: int = 30) -> pd.DataFrame:
            """Generate multi-step forecast"""
            if self.multi_step_forecaster is None:
                raise ValueError("Multi-step forecaster not available")
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            return self.multi_step_forecaster.forecast_recursive(
                item_id, store_id, start_dt, horizon
            )

        def forecast_with_confidence(self, item_id: int, store_id: int,
                                     start_date: str, horizon: int = 30) -> pd.DataFrame:
            """Generate probabilistic forecast"""
            if self.multi_step_forecaster is None:
                raise ValueError("Multi-step forecaster not available")
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            return self.multi_step_forecaster.forecast_with_confidence(
                item_id, store_id, start_dt, horizon
            )

    predictor_advanced = None

    def get_predictor_advanced() -> DemandPredictorAdvanced:
        """Get or create advanced predictor instance"""
        global predictor_advanced
        if predictor_advanced is None:
            predictor_advanced = DemandPredictorAdvanced()
        return predictor_advanced

else:

    def get_predictor_advanced():
        return get_predictor()