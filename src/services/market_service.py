"""
Market Intelligence Service
"""

from sqlalchemy.orm import Session

from src.database.models import (
    MarketInsight
)

from src.database.repository import (
    MarketRepository
)

from src.agents.market.pricing_engine import (
    PricingEngine
)

from src.agents.market.trend_analyzer import (
    TrendAnalyzer
)

from src.schemas.market import (
    MarketInsightCreate
)


class MarketService:

    @staticmethod
    def create_market_insight(
        db: Session,
        data: MarketInsightCreate
    ):

        insight = MarketInsight(
            product_name=
            data.product_name,
            competitor_price=
            data.competitor_price,
            trend_score=
            data.trend_score,
            demand_score=
            data.demand_score
        )

        return (
            MarketRepository
            .create(
                db,
                insight
            )
        )

    @staticmethod
    def get_all_insights(
        db: Session
    ):

        return (
            MarketRepository
            .get_all(db)
        )

    @staticmethod
    def generate_analysis(
        competitor_price: float
    ):

        trend = (
            TrendAnalyzer
            .analyze()
        )

        recommended_price = (
            PricingEngine
            .recommend_price(
                competitor_price
            )
        )

        return {
            "competitor_price":
            competitor_price,

            "recommended_price":
            recommended_price,

            "trend_score":
            trend["trend_score"]
        }