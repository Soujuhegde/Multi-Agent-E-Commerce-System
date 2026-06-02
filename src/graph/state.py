from typing import TypedDict
from typing import Dict
from typing import Any
from typing import Optional


class EcommerceState(TypedDict, total=False):

    user_query: str

    intent: str

    current_agent: str

    workflow_status: str

    inventory_result: Dict[str, Any]

    invoice_result: Dict[str, Any]

    market_result: Dict[str, Any]

    final_response: Optional[str]

    error: Optional[str]