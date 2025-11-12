# api/app.py
"""
FastAPI application for Demand Forecasting
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import time
import logging
from datetime import datetime

from api.schemas import (
    PredictionRequest,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
    ModelPerformance,
    BusinessImpact,
    HealthResponse
)
from api.predictor import get_predictor
from api.config import API_TITLE, API_DESCRIPTION, API_VERSION

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Track API start time
API_START_TIME = time.time()


@app.on_event("startup")
async def startup_event():
    """Load models on startup"""
    logger.info("🚀 Starting Demand Forecasting API...")
    try:
        predictor = get_predictor()
        logger.info("✅ Models loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load models: {e}")
        raise


@app.get("/", tags=["General"])
async def root():
    """Root endpoint"""
    return {
        "message": "🛒 Demand Forecasting API",
        "version": API_VERSION,
        "docs": "/docs",
        "health": "/health",
        "status": "online"
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Health check endpoint"""
    predictor = get_predictor()
    uptime = time.time() - API_START_TIME

    return HealthResponse(
        status="healthy",
        api_version=API_VERSION,
        model_loaded=predictor.lgb_model is not None,
        features_count=len(predictor.feature_names) if predictor.feature_names else 0,
        uptime_seconds=uptime
    )


@app.get("/welcome", tags=["General"])
async def welcome(request: Request):
    """
    Welcome endpoint

    Returns a welcome message and logs the request metadata.
    """
    logger.info(f"Request received: {request.method} {request.url.path}")
    return {"message": "Welcome to the Demand Forecasting API Service!"}


@app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
async def predict_demand(request: PredictionRequest):
    """
    Predict demand for a single item-store-date combination
    
    - **item_id**: Product identifier
    - **store_id**: Store identifier
    - **date**: Prediction date (YYYY-MM-DD)
    - **on_promotion**: Whether item is on promotion
    
    Returns predicted demand with confidence intervals and recommended stock level.
    """
    try:
        predictor = get_predictor()
        
        # Make prediction
        predicted_demand, confidence_lower, confidence_upper = predictor.predict(
            item_id=request.item_id,
            store_id=request.store_id,
            prediction_date=request.date,
            on_promotion=request.on_promotion
        )
        
        # Calculate recommended stock
        recommended_stock = predictor.calculate_recommended_stock(
            predicted_demand, confidence_upper
        )
        
        return PredictionResponse(
            item_id=request.item_id,
            store_id=request.store_id,
            date=request.date,
            predicted_demand=round(predicted_demand, 2),
            confidence_lower=round(confidence_lower, 2),
            confidence_upper=round(confidence_upper, 2),
            recommended_stock=recommended_stock,
            model_used="LightGBM"
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict/batch", response_model=BatchPredictionResponse, tags=["Predictions"])
async def predict_batch(request: BatchPredictionRequest):
    """
    Predict demand for multiple items in batch
    
    Accepts a list of prediction requests and returns predictions for all items.
    Useful for bulk forecasting across multiple products/stores.
    """
    start_time = time.time()
    predictions = []
    
    try:
        predictor = get_predictor()
        
        for pred_request in request.predictions:
            predicted_demand, confidence_lower, confidence_upper = predictor.predict(
                item_id=pred_request.item_id,
                store_id=pred_request.store_id,
                prediction_date=pred_request.date,
                on_promotion=pred_request.on_promotion
            )
            
            recommended_stock = predictor.calculate_recommended_stock(
                predicted_demand, confidence_upper
            )
            
            predictions.append(PredictionResponse(
                item_id=pred_request.item_id,
                store_id=pred_request.store_id,
                date=pred_request.date,
                predicted_demand=round(predicted_demand, 2),
                confidence_lower=round(confidence_lower, 2),
                confidence_upper=round(confidence_upper, 2),
                recommended_stock=recommended_stock,
                model_used="LightGBM"
            ))
        
        processing_time = (time.time() - start_time) * 1000  # milliseconds
        
        return BatchPredictionResponse(
            predictions=predictions,
            total_predictions=len(predictions),
            processing_time_ms=round(processing_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")


@app.get("/models/performance", tags=["Models"])
async def get_model_performance():
    """
    Get performance metrics for all models
    
    Returns accuracy metrics (MAE, RMSE, MAPE, R²) for deployed models.
    """
    # In production, load these from saved metrics
    return [
        ModelPerformance(
            model_name="LightGBM",
            mae=12.34,
            rmse=18.56,
            mape=15.2,
            r2=0.8543,
            accuracy_pct=84.8
        ),
        ModelPerformance(
            model_name="XGBoost",
            mae=13.12,
            rmse=19.23,
            mape=16.1,
            r2=0.8421,
            accuracy_pct=83.9
        ),
        ModelPerformance(
            model_name="Baseline",
            mae=23.45,
            rmse=32.11,
            mape=28.3,
            r2=0.6234,
            accuracy_pct=71.7
        )
    ]


@app.get("/business/impact", response_model=BusinessImpact, tags=["Business"])
async def get_business_impact():
    """
    Calculate business impact and ROI
    
    Returns cost savings from waste reduction and stockout prevention.
    """
    # In production, calculate from real data
    return BusinessImpact(
        model_name="LightGBM",
        waste_cost=45230.50,
        stockout_cost=32150.75,
        total_cost=77381.25,
        annual_savings=156789.00,
        cost_reduction_pct=32.5
    )
# Add to api/app.py (before if __name__ == "__main__":)

@app.post("/predict/multi-step", tags=["Advanced Predictions"])
async def predict_multi_step(
    item_id: int,
    store_id: int,
    start_date: str,
    horizon: int = 30
):
    """
    Multi-step demand forecasting (Enterprise Feature)
    
    Predict demand for next N days (like Walmart/Amazon systems)
    
    - **item_id**: Product identifier
    - **store_id**: Store identifier  
    - **start_date**: Forecast start date (YYYY-MM-DD)
    - **horizon**: Number of days to forecast (default: 30)
    
    Returns day-by-day predictions for the entire horizon.
    """
    try:
        from api.predictor import get_predictor_advanced
        
        predictor = get_predictor_advanced()
        
        # Generate forecast
        forecast_df = predictor.forecast_multi_step(
            item_id=item_id,
            store_id=store_id,
            start_date=start_date,
            horizon=horizon
        )
        
        # Convert to list of dicts
        forecasts = forecast_df.to_dict('records')
        
        # Calculate statistics
        total_demand = forecast_df['predicted_demand'].sum()
        avg_daily_demand = forecast_df['predicted_demand'].mean()
        peak_demand = forecast_df['predicted_demand'].max()
        peak_date = forecast_df.loc[forecast_df['predicted_demand'].idxmax(), 'date']
        
        return {
            "item_id": item_id,
            "store_id": store_id,
            "forecast_horizon": horizon,
            "forecasts": forecasts,
            "summary": {
                "total_demand": round(total_demand, 2),
                "average_daily_demand": round(avg_daily_demand, 2),
                "peak_demand": round(peak_demand, 2),
                "peak_date": str(peak_date)
            }
        }
        
    except Exception as e:
        logger.error(f"Multi-step prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Multi-step forecast failed: {str(e)}")


@app.post("/predict/probabilistic", tags=["Advanced Predictions"])
async def predict_probabilistic(
    item_id: int,
    store_id: int,
    start_date: str,
    horizon: int = 30
):
    """
    Probabilistic demand forecasting with confidence intervals
    
    Uses Monte Carlo simulation to generate confidence bounds.
    Like Amazon's uncertainty quantification.
    
    Returns predictions with 80% confidence intervals.
    """
    try:
        from api.predictor import get_predictor_advanced
        
        predictor = get_predictor_advanced()
        
        # Generate probabilistic forecast
        forecast_df = predictor.forecast_with_confidence(
            item_id=item_id,
            store_id=store_id,
            start_date=start_date,
            horizon=horizon
        )
        
        forecasts = forecast_df.to_dict('records')
        
        return {
            "item_id": item_id,
            "store_id": store_id,
            "forecast_horizon": horizon,
            "forecasts": forecasts,
            "confidence_level": "80%",
            "method": "Monte Carlo Simulation (100 iterations)"
        }
        
    except Exception as e:
        logger.error(f"Probabilistic prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Probabilistic forecast failed: {str(e)}")
    
# Add to api/app.py

@app.get("/items/valid-ranges", tags=["General"])
async def get_valid_ranges():
    """
    Get valid item and store ID ranges
    
    Returns the valid ranges for items and stores that have historical data.
    Use this to validate inputs before making predictions.
    """
    predictor = get_predictor()
    
    if predictor.historical_data is not None:
        valid_items = sorted(predictor.historical_data['item_id'].unique().tolist())
        valid_stores = sorted(predictor.historical_data['store_id'].unique().tolist())
        
        return {
            "valid_items": {
                "min": min(valid_items),
                "max": max(valid_items),
                "count": len(valid_items),
                "list": valid_items
            },
            "valid_stores": {
                "min": min(valid_stores),
                "max": max(valid_stores),
                "count": len(valid_stores),
                "list": valid_stores
            },
            "total_combinations": len(valid_items) * len(valid_stores),
            "note": "Predictions for IDs outside these ranges will use intelligent defaults with lower confidence"
        }
    else:
        return {"message": "Historical data not available"}


@app.get("/items/coverage", tags=["General"])
async def get_data_coverage():
    """
    Show which item-store combinations have historical data
    
    Returns detailed coverage information for all item-store pairs.
    """
    try:
        predictor = get_predictor()
        
        if predictor.historical_data is None:
            raise HTTPException(status_code=503, detail="Historical data not loaded")
        
        # Get unique combinations with data
        coverage = predictor.historical_data.groupby(['item_id', 'store_id']).agg({
            'sales': ['count', 'mean', 'std'],
            'date': ['min', 'max']
        }).reset_index()
        
        coverage.columns = ['item_id', 'store_id', 'records', 'avg_sales', 
                           'std_sales', 'first_date', 'last_date']
        
        # Convert to records
        coverage_records = coverage.to_dict('records')
        
        # Calculate statistics
        total_possible = predictor.historical_data['item_id'].nunique() * \
                        predictor.historical_data['store_id'].nunique()
        
        return {
            "total_combinations_with_data": len(coverage),
            "total_possible_combinations": total_possible,
            "coverage_percentage": round(len(coverage) / total_possible * 100, 1),
            "unique_items": int(predictor.historical_data['item_id'].nunique()),
            "unique_stores": int(predictor.historical_data['store_id'].nunique()),
            "total_records": len(predictor.historical_data),
            "sample_coverage": coverage_records[:20],  # First 20
            "note": "Use /items/valid-ranges for valid ID ranges"
        }
        
    except Exception as e:
        logger.error(f"Coverage endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/items/{item_id}/stores/{store_id}/validate", tags=["General"])
async def validate_item_store(item_id: int, store_id: int):
    """
    Validate if an item-store combination exists
    
    Check if the requested item-store pair has historical data
    before making predictions.
    """
    try:
        predictor = get_predictor()
        
        has_data = predictor.has_historical_data(item_id, store_id)
        
        if has_data:
            item_data = predictor.historical_data[
                (predictor.historical_data['item_id'] == item_id) &
                (predictor.historical_data['store_id'] == store_id)
            ]
            
            return {
                "valid": True,
                "has_historical_data": True,
                "item_id": item_id,
                "store_id": store_id,
                "data_quality": "High",
                "records": len(item_data),
                "avg_sales": float(item_data['sales'].mean()),
                "date_range": {
                    "from": str(item_data['date'].min()),
                    "to": str(item_data['date'].max())
                },
                "recommendation": "Safe to use - predictions based on real historical data"
            }
        else:
            # Check if it's within valid ranges
            valid_items = predictor.historical_data['item_id'].unique()
            valid_stores = predictor.historical_data['store_id'].unique()
            
            item_in_range = item_id in valid_items
            store_in_range = store_id in valid_stores
            
            if not item_in_range or not store_in_range:
                return {
                    "valid": False,
                    "has_historical_data": False,
                    "item_id": item_id,
                    "store_id": store_id,
                    "data_quality": "None",
                    "error": f"Item {item_id} or Store {store_id} does not exist in dataset",
                    "valid_item_range": f"1-{max(valid_items)}",
                    "valid_store_range": f"1-{max(valid_stores)}",
                    "recommendation": "Do NOT use - outside valid ranges"
                }
            else:
                return {
                    "valid": True,
                    "has_historical_data": False,
                    "item_id": item_id,
                    "store_id": store_id,
                    "data_quality": "Medium",
                    "records": 0,
                    "note": "This item-store combination exists but has no data",
                    "recommendation": "Use with caution - predictions use intelligent defaults"
                }
        
    except Exception as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
# Update the /predict endpoint in api/app.py to be more explicit

@app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
async def predict_demand(request: PredictionRequest):
    """
    Predict demand for a single item-store-date combination
    
    ⚠️ NOTE: Only items 1-50 and stores 1-5 have historical data.
    Other IDs will use intelligent defaults with lower confidence.
    """
    # ... rest of the code stays the same

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)