"""
Embedding Service
"""

from typing import List

import hashlib


class EmbeddingService:

    @staticmethod
    def generate_embedding(
        text: str
    ) -> List[float]:

        hash_value = hashlib.md5(
            text.encode()
        ).hexdigest()

        embedding = []

        for char in hash_value[:32]:

            embedding.append(
                float(ord(char))
            )

        return embedding