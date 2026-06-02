class IntentClassifier:

    def classify(self, query: str) -> str:

        query = query.lower()

        if "stock" in query:
            return "inventory"

        if "inventory" in query:
            return "inventory"

        if "invoice" in query:
            return "invoice"

        if "bill" in query:
            return "invoice"

        if "market" in query:
            return "market"

        if "price" in query:
            return "market"

        return "unknown"