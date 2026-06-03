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
async def market_insights(
    product_name: str = "iPhone 15"
):

    from src.tools.market_tool import MarketTool
    from src.agents.market.pricing_engine import PricingEngine

    comp_price = MarketTool.get_competitor_price(product_name)
    demand_score = MarketTool.get_demand_score(product_name)
    trend_name = MarketTool.get_market_trend()
    trend_score = 90 if trend_name == "Rising" else (70 if trend_name == "Stable" else 50)
    rec_price = PricingEngine.recommend_price(comp_price)

    return {
        "product_name": product_name,
        "competitor_price": comp_price,
        "demand_score": demand_score,
        "trend_score": trend_score,
        "recommended_price": rec_price
    }