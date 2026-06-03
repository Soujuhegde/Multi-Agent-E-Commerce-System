import requests

BASE_URL = "http://localhost:8000"


class APIClient:

    @staticmethod
    def health():
        return requests.get(
            f"{BASE_URL}/health"
        ).json()

    @staticmethod
    def get_products():
        return requests.get(
            f"{BASE_URL}/inventory/products"
        ).json()

    @staticmethod
    def add_product(
        product_name: str,
        category: str,
        price: float,
        stock_quantity: int
    ):
        return requests.post(
            f"{BASE_URL}/inventory/add",
            params={
                "product_name": product_name,
                "category": category,
                "price": price,
                "stock_quantity": stock_quantity
            }
        ).json()

    @staticmethod
    def generate_invoice(
        customer_name: str,
        items: list
    ):
        payload = {
            "customer_name": customer_name,
            "items": items
        }
        response = requests.post(
            f"{BASE_URL}/invoice/generate",
            json=payload
        )
        # Check response code first to raise appropriate HTTPException logs in UI
        response.raise_for_status()
        return response.json()

    @staticmethod
    def market_insights(
        product_name: str
    ):
        return requests.get(
            f"{BASE_URL}/market/insights",
            params={"product_name": product_name}
        ).json()

    @staticmethod
    def execute_workflow(
        query: str
    ):
        return requests.post(
            f"{BASE_URL}/workflow/execute",
            params={"query": query}
        ).json()