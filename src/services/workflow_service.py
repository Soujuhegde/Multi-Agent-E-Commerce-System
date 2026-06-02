"""
Workflow Service
"""

from src.graph.workflow import (
    WorkflowExecutor
)


class WorkflowService:

    @staticmethod
    def execute(
        query: str
    ):

        return (
            WorkflowExecutor
            .execute(query)
        )