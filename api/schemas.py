# api/schemas.py
"""
Pydantic models for request/response validation
WITH PRODUCTION-GRADE INPUT VALIDATION
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from datetime import date, datetime

# ============================================================================
# VALID RANGES (Based on generated data)
# ============================================================================

VALID_ITEM_IDS = list(range(1, 51))  # Items 1-50
VALID_STORE_IDS = list(range(1, 6))   # Stores 1-5

MIN_ITEM_ID = 1
MAX_ITEM_ID = 50
MIN_STORE_ID = 1
MAX_STORE_ID = 5


# ============================================================================
# REQUEST MODELS
# ============================================================================

class PredictionRequest(BaseModel):
    """Single item prediction request WITH VALIDATION"""
    item_id: int = Field(
        ..., 
        ge=MIN_ITEM_ID, 
        le=MAX_ITEM_ID,
        description=f"Product ID (must be between {MIN_ITEM_ID} and {MAX_ITEM_ID})", 
        example=1
    )
    store_id: int = Field(
        ..., 
        ge=MIN_STORE_ID, 
        le=MAX_STORE_ID,
        description=f"Store ID (must be between {MIN_STORE_ID} and {MAX_STORE_ID})", 
        example=1
    )
    date: str = Field(
        ..., 
        description="Prediction date (YYYY-MM-DD)", 
        example="2024-12-31"
    )
    on_promotion: bool = Field(
        False, 
        description="Is item on promotion?", 
        example=False
    )
    
    @validator('date')
    def validate_date(cls, v):
        """Validate date format"""
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
    
    class Config:
        schema_extra = {
            "example": {
                "item_id": 1,
                "store_id": 1,
                "date": "2024-12-31",
                "on_promotion": False
            }
        }


class BatchPredictionRequest(BaseModel):
    """Batch prediction request WITH VALIDATION"""
    predictions: List[PredictionRequest] = Field(
        ..., 
        description="List of prediction requests (max 100)",
        max_items=100
    )
    
    class Config:
        schema_extra = {
            "example": {
                "predictions": [
                    {"item_id": 1, "store_id": 1, "date": "2024-12-31", "on_promotion": False},
                    {"item_id": 2, "store_id": 1, "date": "2024-12-31", "on_promotion": True}
                ]
            }
        }


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class PredictionResponse(BaseModel):
    """Single prediction response"""
    item_id: int
    store_id: int
    date: str
    predicted_demand: float = Field(..., description="Predicted sales quantity")
    confidence_lower: float = Field(..., description="Lower confidence bound (80%)")
    confidence_upper: float = Field(..., description="Upper confidence bound (80%)")
    recommended_stock: int = Field(..., description="Recommended stock quantity")
    model_used: str = Field(..., description="Model used for prediction")


class BatchPredictionResponse(BaseModel):
    """Batch prediction response"""
    predictions: List[PredictionResponse]
    total_predictions: int
    processing_time_ms: float


class ModelPerformance(BaseModel):
    """Model performance metrics"""
    model_name: str
    mae: float = Field(..., description="Mean Absolute Error")
    rmse: float = Field(..., description="Root Mean Squared Error")
    mape: float = Field(..., description="Mean Absolute Percentage Error (%)")
    r2: float = Field(..., description="R² Score")
    accuracy_pct: float = Field(..., description="Accuracy percentage")


class BusinessImpact(BaseModel):
    """Business impact metrics"""
    model_name: str
    waste_cost: float = Field(..., description="Cost from overstocking")
    stockout_cost: float = Field(..., description="Cost from understocking")
    total_cost: float = Field(..., description="Total operational cost")
    annual_savings: float = Field(..., description="Projected annual savings")
    cost_reduction_pct: float = Field(..., description="Cost reduction percentage")


class HealthResponse(BaseModel):
    """API health check response"""
    status: str
    api_version: str
    model_loaded: bool
    features_count: int
    uptime_seconds: float


class ValidationResponse(BaseModel):
    """Validation response for item-store combinations"""
    valid: bool
    has_historical_data: bool
    item_id: int
    store_id: int
    data_quality: str
    records: Optional[int] = None
    avg_sales: Optional[float] = None
    date_range: Optional[Dict] = None
    recommendation: str
    error: Optional[str] = None
    valid_item_range: Optional[str] = None
    valid_store_range: Optional[str] = None