from typing import TypedDict, Dict, Any, Optional


class AgentState(TypedDict, total=False):
    user_query: str
    intent: str
    current_agent: str
    workflow_status: str
    inventory_result: Dict[str, Any]
    invoice_result: Dict[str, Any]
    market_result: Dict[str, Any]
    final_response: Optional[str]
    error: Optional[str]