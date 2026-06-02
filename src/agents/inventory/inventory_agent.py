from src.agents.base.base_agent import BaseAgent

from src.agents.base.agent_state import AgentState


class InventoryAgent(BaseAgent):

    def __init__(self):

        super().__init__("InventoryAgent")

    def execute(
        self,
        state: AgentState
    ) -> AgentState:

        self.log("Checking inventory")

        state["inventory_result"] = {
            "status": "success",
            "message": "Inventory checked"
        }

        state["final_response"] = (
            "Inventory information processed"
        )

        return state