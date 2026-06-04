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
        max_tokens: int = 2000
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
                timeout=120
            )

            response.raise_for_status()

            data = response.json()
            
            message = data["choices"][0]["message"]
            content = message.get("content")
            
            if not content and "reasoning_content" in message:
                content = message["reasoning_content"]

            return content

        except requests.exceptions.HTTPError as e:
            print(f"DEBUG Sarvam HTTP Error: {str(e)} - {e.response.text}")
            logger.error(f"Sarvam HTTP Error: {str(e)} - {e.response.text}")
            return None
        except Exception as e:
            import traceback
            print(f"DEBUG Sarvam Error: {str(e)}\n{traceback.format_exc()}")
            logger.error(f"Sarvam Error: {str(e)}\n{traceback.format_exc()}")
            return None