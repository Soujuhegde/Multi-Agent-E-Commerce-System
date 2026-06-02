"""
Market Intelligence Schemas
"""

from datetime import datetime

from pydantic import BaseModel


class MarketInsightCreate(BaseModel):

    product_name: str

    competitor_price: float

    trend_score: float

    demand_score: float


class MarketInsightResponse(
    MarketInsightCreate
):

    id: int

    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class MarketAnalysisRequest(
    BaseModel
):

    product_name: str


class MarketAnalysisResponse(
    BaseModel
):

    product_name: str

    competitor_price: float

    recommended_price: float

    trend_score: float

    demand_score: float

    summary: str