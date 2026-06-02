"""
Invoice Tool
"""

import uuid

from datetime import datetime


class InvoiceTool:

    @staticmethod
    def generate_invoice_number():

        return (
            "INV-"
            + uuid.uuid4()
            .hex[:10]
            .upper()
        )

    @staticmethod
    def calculate_tax(
        subtotal: float,
        tax_rate: float = 18
    ):

        return (
            subtotal *
            tax_rate /
            100
        )

    @staticmethod
    def calculate_total(
        subtotal: float,
        tax_amount: float
    ):

        return (
            subtotal +
            tax_amount
        )

    @staticmethod
    def build_invoice_data(
        customer_name: str,
        subtotal: float,
        tax_amount: float
    ):

        return {
            "invoice_number":
            InvoiceTool
            .generate_invoice_number(),

            "customer_name":
            customer_name,

            "subtotal":
            subtotal,

            "tax_amount":
            tax_amount,

            "total_amount":
            subtotal +
            tax_amount,

            "generated_at":
            datetime.utcnow()
            .isoformat()
        }