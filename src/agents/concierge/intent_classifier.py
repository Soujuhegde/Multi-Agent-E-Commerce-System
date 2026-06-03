from src.llm.sarvam_client import SarvamClient
from src.llm.prompts import PromptTemplates
from loguru import logger


class IntentClassifier:

    def __init__(self):
        self.llm = SarvamClient()

    def classify(self, query: str) -> str:
        # 1. Attempt LLM classification
        try:
            prompt = PromptTemplates.INTENT_CLASSIFIER.format(query=query)
            llm_result = self.llm.generate(prompt)
            if llm_result:
                intent = llm_result.strip().lower()
                # Clean any punctuation if returned by the LLM
                intent = "".join(char for char in intent if char.isalnum())
                if intent in ["inventory", "invoice", "market"]:
                    return intent
        except Exception as exc:
            logger.warning(
                f"LLM classification failed: {exc}. Using fallback classifier."
            )

        # 2. Fallback keyword classifier
        query_lower = query.lower()

        if "stock" in query_lower or "inventory" in query_lower:
            return "inventory"

        if "invoice" in query_lower or "bill" in query_lower:
            return "invoice"

        if "market" in query_lower or "price" in query_lower:
            return "market"

        return "unknown"