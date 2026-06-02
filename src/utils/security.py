"""
Security Utilities
"""

import hashlib
import secrets


class SecurityUtils:

    @staticmethod
    def hash_text(
        text: str
    ) -> str:

        return hashlib.sha256(
            text.encode()
        ).hexdigest()

    @staticmethod
    def generate_token():

        return secrets.token_hex(
            32
        )

    @staticmethod
    def verify_hash(
        text: str,
        hashed_text: str
    ):

        return (
            SecurityUtils.hash_text(
                text
            )
            == hashed_text
        )