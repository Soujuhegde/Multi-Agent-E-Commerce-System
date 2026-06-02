"""
Sarvam AI Client
"""

from typing import Optional

import requests

from src.config.settings import settings

from src.config.logging_config import (
    get_logger
)

logger = get_logger()


class SarvamClient:

    BASE_URL = (
        "https://api.sarvam.ai/v1/chat/completions"
    )

    def __init__(self):

        self.api_key = (
            settings.SARVAM_API_KEY
        )

        self.model = (
            settings.SARVAM_MODEL
        )

    def generate(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 500
    ) -> Optional[str]:

        try:

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            headers = {
                "Authorization":
                f"Bearer {self.api_key}",
                "Content-Type":
                "application/json"
            }

            response = requests.post(
                self.BASE_URL,
                json=payload,
                headers=headers,
                timeout=60
            )

            response.raise_for_status()

            data = response.json()

            return (
                data["choices"][0]
                ["message"]["content"]
            )

        except Exception as e:

            logger.error(
                f"Sarvam Error: {str(e)}"
            )

            return None