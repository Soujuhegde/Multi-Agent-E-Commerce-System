"""
Common Helper Functions
"""

from datetime import datetime
from typing import Any
from typing import Dict


class Helpers:

    @staticmethod
    def success_response(
        message: str,
        data: Dict[str, Any] = None
    ) -> Dict[str, Any]:

        return {
            "success": True,
            "message": message,
            "data": data or {},
            "timestamp": datetime.utcnow().isoformat()
        }

    @staticmethod
    def error_response(
        message: str
    ) -> Dict[str, Any]:

        return {
            "success": False,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }

    @staticmethod
    def format_currency(
        amount: float
    ) -> str:

        return f"₹{amount:,.2f}"

    @staticmethod
    def generate_workflow_id():

        import uuid

        return str(uuid.uuid4())