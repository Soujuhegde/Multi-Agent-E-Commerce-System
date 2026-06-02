from src.agents.inventory.inventory_agent import InventoryAgent

from src.agents.invoice.invoice_agent import InvoiceAgent

from src.agents.market.market_agent import MarketAgent


class AgentRouter:

    def get_agent(self, intent: str):

        if intent == "inventory":
            return InventoryAgent()

        if intent == "invoice":
            return InvoiceAgent()

        if intent == "market":
            return MarketAgent()

        return None