import uuid


class InvoiceGenerator:

    @staticmethod
    def generate_invoice_number():

        return (
            "INV-"
            + str(uuid.uuid4())[:8]
        )