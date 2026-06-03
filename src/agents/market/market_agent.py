from src.agents.base.base_agent import BaseAgent
from src.agents.base.agent_state import AgentState
from src.tools.market_tool import MarketTool
from src.agents.market.pricing_engine import PricingEngine
from src.database.session import SessionLocal
from src.database.models import Product, MarketInsight
from src.llm.sarvam_client import SarvamClient
from src.llm.prompts import PromptTemplates


class MarketAgent(BaseAgent):

    def __init__(self):
        super().__init__("MarketAgent")
        self.llm = SarvamClient()

    def execute(
        self,
        state: AgentState
    ) -> AgentState:

        self.log("Evaluating competitor prices and demand indexing")

        query = state.get("user_query", "")

        db = SessionLocal()

        try:
            # 1. Match query with target product in our database
            products = db.query(Product).all()
            target_product = None

            for p in products:
                if p.product_name.lower() in query.lower():
                    target_product = p
                    break

            if not target_product:
                # Default fallback if no specific product was found
                target_product = db.query(Product).first()
                if not target_product:
                    state["error"] = "No products found in the catalog to analyze"
                    return state

            product_name = target_product.product_name
            current_price = target_product.price

            # 2. Query market statistics using tools
            comp_price = MarketTool.get_competitor_price(product_name)
            demand_score = MarketTool.get_demand_score(product_name)
            trend_name = MarketTool.get_market_trend()
            trend_score = (
                90 if trend_name == "Rising"
                else (70 if trend_name == "Stable" else 50)
            )

            # 3. Compute optimized price recommendation
            rec_price = PricingEngine.recommend_price(comp_price)

            # 4. Save insight to database
            insight = MarketInsight(
                product_name=product_name,
                competitor_price=comp_price,
                trend_score=float(trend_score),
                demand_score=float(demand_score)
            )

            db.add(insight)
            db.commit()

            # 5. Ask the LLM to write analysis report
            prompt = PromptTemplates.MARKET_AGENT.format(
                product_name=product_name,
                competitor_price=comp_price,
                demand_score=demand_score
            )

            llm_response = self.llm.generate(prompt)

            # 6. Store market insight telemetry in state
            state["market_result"] = {
                "product_name": product_name,
                "current_price": current_price,
                "competitor_price": comp_price,
                "recommended_price": rec_price,
                "demand_score": demand_score,
                "trend_score": trend_score,
                "source": "Competitor Crawl Agent",
                "insight_id": insight.id
            }

            if llm_response:
                state["final_response"] = llm_response.strip()
            else:
                state["final_response"] = (
                    f"Market Analysis for {product_name} finished. "
                    f"Our Price: ₹{current_price:,.2f}, Competitor Price: ₹{comp_price:,.2f}, "
                    f"Recommended Price: ₹{rec_price:,.2f}."
                )

        except Exception as exc:
            db.rollback()
            self.log(f"Error evaluating market insights: {exc}")
            state["error"] = str(exc)

        finally:
            db.close()

        return state