"""
Output Parsing Utilities
"""

import json

from typing import Dict
from typing import Any


class OutputParser:

    @staticmethod
    def parse_json(
        response: str
    ) -> Dict[str, Any]:

        try:

            return json.loads(response)

        except Exception:

            return {
                "success": False,
                "raw_response": response
            }

    @staticmethod
    def parse_text(
        response: str
    ) -> str:

        if not response:
            return ""

        return response.strip()

    @staticmethod
    def parse_intent(
        response: str
    ) -> str:

        response = (
            response
            .lower()
            .strip()
        )

        allowed = [
            "inventory",
            "invoice",
            "market"
        ]

        if response in allowed:
            return response

        return "unknown"