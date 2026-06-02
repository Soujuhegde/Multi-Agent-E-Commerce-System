from fastapi import APIRouter

from src.agents.market.trend_analyzer import (
    TrendAnalyzer
)

from src.agents.market.pricing_engine import (
    PricingEngine
)

router = APIRouter(
    prefix="/market",
    tags=["Market Intelligence"]
)


@router.get("/trend")
async def market_trend():

    return TrendAnalyzer.analyze()


@router.get("/price-recommendation")
async def recommend_price(
    current_price: float
):

    price = (
        PricingEngine
        .recommend_price(current_price)
    )

    return {
        "recommended_price": price
    }


@router.get("/insights")
async def market_insights():

    return {
        "trend_score": 87,
        "competitor_price": 950,
        "demand_score": 80
    }