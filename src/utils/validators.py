"""
Validation Utilities
"""

import re


class Validators:

    @staticmethod
    def validate_product_name(
        name: str
    ) -> bool:

        return (
            len(name.strip()) >= 2
        )

    @staticmethod
    def validate_price(
        price: float
    ) -> bool:

        return price > 0

    @staticmethod
    def validate_stock(
        quantity: int
    ) -> bool:

        return quantity >= 0

    @staticmethod
    def validate_customer_name(
        name: str
    ) -> bool:

        return (
            len(name.strip()) >= 3
        )

    @staticmethod
    def validate_email(
        email: str
    ) -> bool:

        pattern = (
            r"^[a-zA-Z0-9._%+-]+"
            r"@[a-zA-Z0-9.-]+"
            r"\.[a-zA-Z]{2,}$"
        )

        return bool(
            re.match(
                pattern,
                email
            )
        )