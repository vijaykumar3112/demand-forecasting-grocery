# src/models/multi_step_forecaster.py
"""
Multi-Step Demand Forecasting
Like Walmart/Amazon - predict multiple days ahead
"""

import numpy as np
import pandas as pd
import lightgbm as lgb
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MultiStepForecaster:
    """
    Advanced multi-step forecasting
    - Recursive strategy: Use predictions as features
    - Direct strategy: Separate model for each horizon
    - Hybrid strategy: Ensemble of both
    """
    
    def __init__(self, lgb_model, feature_names, historical_data):
        self.lgb_model = lgb_model
        self.feature_names = feature_names
        self.historical_data = historical_data
        
    def forecast_recursive(self, item_id: int, store_id: int, 
                          start_date: datetime, horizon: int = 30) -> pd.DataFrame:
        """
        Recursive multi-step forecasting
        Use each prediction as input for next step
        """
        forecasts = []
        current_date = start_date
        
        # Get historical data for this item-store
        # OPTIMIZATION: Only keep last 60 days (sufficient for max lag of 28)
        # This prevents pd.concat from being slow on large dataframes
        full_item_data = self.historical_data[
            (self.historical_data['item_id'] == item_id) &
            (self.historical_data['store_id'] == store_id)
        ].sort_values('date')
        
        item_data = full_item_data.tail(60).copy()
        
        for day in range(horizon):
            # Engineer features for current day
            features = self._engineer_features_recursive(
                item_id, store_id, current_date, item_data
            )
            
            # Make prediction
            prediction = self._predict_single(features)
            
            # Store forecast
            forecasts.append({
                'date': current_date,
                'item_id': item_id,
                'store_id': store_id,
                'predicted_demand': max(0, prediction),
                'forecast_horizon': day + 1
            })
            
            # Update historical data with prediction (for next step)
            new_row = {
                'date': current_date,
                'item_id': item_id,
                'store_id': store_id,
                'sales': prediction,
                **features
            }
            item_data = pd.concat([
                item_data,
                pd.DataFrame([new_row])
            ], ignore_index=True)
            
            # Keep item_data small for next iteration
            if len(item_data) > 60:
                item_data = item_data.tail(60)
            
            # Move to next day
            current_date += timedelta(days=1)
        
        return pd.DataFrame(forecasts)
    
    def forecast_with_confidence(self, item_id: int, store_id: int,
                                 start_date: datetime, horizon: int = 30,
                                 n_simulations: int = 100) -> pd.DataFrame:
        """
        Probabilistic forecasting with Monte Carlo simulation
        Returns point forecast + confidence intervals
        """
        all_simulations = []
        
        for sim in range(n_simulations):
            # Add noise to features (simulate uncertainty)
            forecast = self.forecast_recursive(item_id, store_id, start_date, horizon)
            
            # Add random noise proportional to forecast horizon
            noise_factor = 1 + np.random.normal(0, 0.05 * (np.arange(horizon) + 1) / horizon)
            forecast['simulated_demand'] = forecast['predicted_demand'] * noise_factor
            forecast['simulation'] = sim
            
            all_simulations.append(forecast)
        
        # Combine all simulations
        all_sims_df = pd.concat(all_simulations, ignore_index=True)
        
        # Calculate statistics
        results = all_sims_df.groupby('date').agg({
            'simulated_demand': ['mean', 'std', 
                                 lambda x: np.percentile(x, 10),
                                 lambda x: np.percentile(x, 90)]
        }).reset_index()
        
        results.columns = ['date', 'predicted_demand', 'std_dev', 
                          'confidence_lower', 'confidence_upper']
        
        results['item_id'] = item_id
        results['store_id'] = store_id
        
        return results
    
    def forecast_with_scenarios(self, item_id: int, store_id: int,
                                start_date: datetime, horizon: int = 30,
                                scenarios: Dict[str, Dict] = None) -> Dict[str, pd.DataFrame]:
        """
        Scenario-based forecasting
        - Base case
        - Promotion scenario
        - High demand scenario
        - Low demand scenario
        """
        if scenarios is None:
            scenarios = {
                'base_case': {},
                'with_promotion': {'on_promotion': True, 'demand_multiplier': 1.6},
                'high_demand': {'demand_multiplier': 1.3},
                'low_demand': {'demand_multiplier': 0.7}
            }
        
        results = {}
        
        for scenario_name, scenario_params in scenarios.items():
            forecast = self.forecast_recursive(item_id, store_id, start_date, horizon)
            
            # Apply scenario adjustments
            if 'demand_multiplier' in scenario_params:
                forecast['predicted_demand'] *= scenario_params['demand_multiplier']
            
            forecast['scenario'] = scenario_name
            results[scenario_name] = forecast
        
        return results
    
    def _engineer_features_recursive(self, item_id: int, store_id: int,
                                    prediction_date: datetime, 
                                    item_data: pd.DataFrame) -> Dict:
        """Engineer features using recursive predictions"""
        features = {}
        
        # Date features
        features['year'] = prediction_date.year
        features['month'] = prediction_date.month
        features['day'] = prediction_date.day
        features['day_of_week'] = prediction_date.weekday()
        features['week_of_year'] = prediction_date.isocalendar()[1]
        features['quarter'] = (prediction_date.month - 1) // 3 + 1
        features['is_weekend'] = int(prediction_date.weekday() >= 5)
        features['is_month_start'] = int(prediction_date.day == 1)
        features['is_month_end'] = int(prediction_date.day >= 28)
        
        # Cyclical encoding
        features['month_sin'] = np.sin(2 * np.pi * prediction_date.month / 12)
        features['month_cos'] = np.cos(2 * np.pi * prediction_date.month / 12)
        features['dow_sin'] = np.sin(2 * np.pi * prediction_date.weekday() / 7)
        features['dow_cos'] = np.cos(2 * np.pi * prediction_date.weekday() / 7)
        
        # Holiday flag
        features['is_holiday'] = int(
            (prediction_date.month == 12 and prediction_date.day == 25) or
            (prediction_date.month == 1 and prediction_date.day == 1) or
            (prediction_date.month == 7 and prediction_date.day == 4)
        )
        
        # Get recent sales (including predictions)
        recent_sales = item_data.sort_values('date')['sales'].tail(28).values
        
        # Lag features
        if len(recent_sales) >= 1:
            features['sales_lag_1'] = recent_sales[-1]
        if len(recent_sales) >= 7:
            features['sales_lag_7'] = recent_sales[-7]
        if len(recent_sales) >= 14:
            features['sales_lag_14'] = recent_sales[-14]
        if len(recent_sales) >= 28:
            features['sales_lag_28'] = recent_sales[-28]
        
        # Rolling features
        if len(recent_sales) >= 7:
            features['sales_rolling_mean_7'] = np.mean(recent_sales[-7:])
            features['sales_rolling_std_7'] = np.std(recent_sales[-7:])
            features['sales_rolling_max_7'] = np.max(recent_sales[-7:])
            features['sales_rolling_min_7'] = np.min(recent_sales[-7:])
        
        if len(recent_sales) >= 14:
            features['sales_rolling_mean_14'] = np.mean(recent_sales[-14:])
            features['sales_rolling_std_14'] = np.std(recent_sales[-14:])
            features['sales_rolling_max_14'] = np.max(recent_sales[-14:])
            features['sales_rolling_min_14'] = np.min(recent_sales[-14:])
        
        if len(recent_sales) >= 28:
            features['sales_rolling_mean_28'] = np.mean(recent_sales[-28:])
            features['sales_rolling_std_28'] = np.std(recent_sales[-28:])
            features['sales_rolling_max_28'] = np.max(recent_sales[-28:])
            features['sales_rolling_min_28'] = np.min(recent_sales[-28:])
        
        # Fill missing with defaults
        for feat in self.feature_names:
            if feat not in features:
                if 'lag' in feat or 'rolling' in feat:
                    features[feat] = 100.0
                else:
                    features[feat] = 0
        
        # Add other required features
        features['item_id'] = item_id
        features['store_id'] = store_id
        features['on_promotion'] = 0
        features['price'] = 5.0
        features['base_price'] = 5.0
        features['price_discount_pct'] = 0.0
        features['price_vs_category_avg'] = 1.0
        features['weekend_promo'] = 0
        features['holiday_promo'] = 0
        features['days_since_start'] = (prediction_date - datetime(2023, 1, 1)).days
        
        if 'category_encoded' not in features:
            features['category_encoded'] = 0
        if 'store_type_encoded' not in features:
            features['store_type_encoded'] = 0
        if 'store_size_encoded' not in features:
            features['store_size_encoded'] = 0
        if 'perishability_days' not in features:
            features['perishability_days'] = 3
        
        return features
    
    def _predict_single(self, features: Dict) -> float:
        """Make single prediction using LightGBM model"""
        feature_vector = [features.get(feat, 0) for feat in self.feature_names]
        feature_array = np.array(feature_vector).reshape(1, -1)
        prediction = self.lgb_model.predict(feature_array)[0]
        return max(0, prediction)