from fastapi import APIRouter

from src.agents.concierge.concierge_agent import (
    ConciergeAgent
)

router = APIRouter(
    prefix="/workflow",
    tags=["Workflow"]
)


@router.post("/execute")
async def execute_workflow(
    query: str
):

    state = {
        "user_query": query
    }

    agent = ConciergeAgent()

    result = agent.execute(state)

    return result