from abc import ABC, abstractmethod

from src.agents.base.agent_state import AgentState

from loguru import logger


class BaseAgent(ABC):

    def __init__(self, agent_name: str):
        self.agent_name = agent_name

    def log(self, message: str):

        logger.info(
            f"[{self.agent_name}] {message}"
        )

    @abstractmethod
    def execute(
        self,
        state: AgentState
    ) -> AgentState:
        pass