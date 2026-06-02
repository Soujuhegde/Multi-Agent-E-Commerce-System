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
    def market_insights():

        return requests.get(
            f"{BASE_URL}/market/insights"
        ).json()

    @staticmethod
    def execute_workflow(
        query: str
    ):

        return requests.post(
            f"{BASE_URL}/workflow/execute",
            params={"query": query}
        ).json()