from src.agents.base.base_agent import BaseAgent

from src.agents.base.agent_state import AgentState

from src.agents.concierge.intent_classifier import (
    IntentClassifier
)

from src.agents.concierge.router import AgentRouter


class ConciergeAgent(BaseAgent):

    def __init__(self):

        super().__init__("ConciergeAgent")

        self.classifier = IntentClassifier()

        self.router = AgentRouter()

    def execute(
        self,
        state: AgentState
    ) -> AgentState:

        query = state["user_query"]

        intent = self.classifier.classify(query)

        state["intent"] = intent

        self.log(f"Intent: {intent}")

        agent = self.router.get_agent(intent)

        if not agent:

            state["error"] = (
                "Unable to determine request"
            )

            return state

        return agent.execute(state)