"""
Market Tool
"""

import random


class MarketTool:

    @staticmethod
    def get_competitor_price(
        product_name: str
    ):

        mock_prices = {
            "iPhone 15": 78500,
            "Samsung S24": 67000,
            "MacBook Air M3": 120000,
        }

        return mock_prices.get(
            product_name,
            random.randint(
                500,
                5000
            )
        )

    @staticmethod
    def get_demand_score(
        product_name: str
    ):

        return random.randint(
            50,
            100
        )

    @staticmethod
    def get_market_trend():

        score = random.randint(
            50,
            100
        )

        if score > 80:
            return "Rising"

        if score > 60:
            return "Stable"

        return "Declining"