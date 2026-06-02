from src.agents.base.base_agent import BaseAgent

from src.agents.base.agent_state import AgentState


class InvoiceAgent(BaseAgent):

    def __init__(self):

        super().__init__("InvoiceAgent")

    def execute(
        self,
        state: AgentState
    ) -> AgentState:

        self.log("Generating invoice")

        state["invoice_result"] = {
            "status": "success"
        }

        state["final_response"] = (
            "Invoice generated"
        )

        return state