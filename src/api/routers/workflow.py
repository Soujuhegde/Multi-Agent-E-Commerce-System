from fastapi import APIRouter

from src.services.workflow_service import WorkflowService

router = APIRouter(
    prefix="/workflow",
    tags=["Workflow"]
)


@router.post("/execute")
async def execute_workflow(
    query: str
):

    return WorkflowService.execute(query)