from src.agents.base.base_agent import BaseAgent

from src.agents.base.agent_state import AgentState


class MarketAgent(BaseAgent):

    def __init__(self):

        super().__init__("MarketAgent")

    def execute(
        self,
        state: AgentState
    ) -> AgentState:

        self.log(
            "Analyzing market intelligence"
        )

        state["market_result"] = {
            "trend_score": 87,
            "competitor_price": 1000
        }

        state["final_response"] = (
            "Market analysis completed"
        )

        return state