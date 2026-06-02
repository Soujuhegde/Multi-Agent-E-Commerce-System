from src.agents.concierge.concierge_agent import (
    ConciergeAgent
)

from src.agents.inventory.inventory_agent import (
    InventoryAgent
)

from src.agents.invoice.invoice_agent import (
    InvoiceAgent
)

from src.agents.market.market_agent import (
    MarketAgent
)

from src.graph.state import EcommerceState


def concierge_node(
    state: EcommerceState
):

    agent = ConciergeAgent()

    return agent.execute(state)


def inventory_node(
    state: EcommerceState
):

    agent = InventoryAgent()

    return agent.execute(state)


def invoice_node(
    state: EcommerceState
):

    agent = InvoiceAgent()

    return agent.execute(state)


def market_node(
    state: EcommerceState
):

    agent = MarketAgent()

    return agent.execute(state)