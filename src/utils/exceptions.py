"""
Custom Exceptions
"""


class EcommerceException(Exception):
    pass


class ProductNotFoundException(
    EcommerceException
):

    def __init__(
        self,
        product_id: int
    ):

        super().__init__(
            f"Product not found: {product_id}"
        )


class InsufficientStockException(
    EcommerceException
):

    def __init__(
        self,
        product_name: str
    ):

        super().__init__(
            f"Insufficient stock for {product_name}"
        )


class InvoiceGenerationException(
    EcommerceException
):

    def __init__(
        self,
        message: str
    ):

        super().__init__(message)


class MarketAnalysisException(
    EcommerceException
):

    def __init__(
        self,
        message: str
    ):

        super().__init__(message)


class AgentExecutionException(
    EcommerceException
):

    def __init__(
        self,
        agent_name: str
    ):

        super().__init__(
            f"{agent_name} execution failed"
        )