"""
Workflow Schemas
"""

from typing import Dict
from typing import Any
from typing import Optional

from pydantic import BaseModel


class WorkflowRequest(
    BaseModel
):

    query: str


class WorkflowResponse(
    BaseModel
):

    success: bool

    intent: Optional[str] = None

    workflow_status: Optional[str] = None

    inventory_result: Optional[
        Dict[str, Any]
    ] = None

    invoice_result: Optional[
        Dict[str, Any]
    ] = None

    market_result: Optional[
        Dict[str, Any]
    ] = None

    final_response: Optional[
        str
    ] = None

    error: Optional[
        str
    ] = None