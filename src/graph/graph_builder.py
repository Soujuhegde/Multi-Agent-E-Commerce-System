from langgraph.graph import StateGraph
from langgraph.graph import END

from src.graph.state import EcommerceState

from src.graph.nodes import (
    concierge_node,
    inventory_node,
    invoice_node,
    market_node,
)

from src.graph.edges import (
    route_by_intent
)


def build_graph():

    workflow = StateGraph(
        EcommerceState
    )

    workflow.add_node(
        "concierge",
        concierge_node
    )

    workflow.add_node(
        "inventory",
        inventory_node
    )

    workflow.add_node(
        "invoice",
        invoice_node
    )

    workflow.add_node(
        "market",
        market_node
    )

    workflow.set_entry_point(
        "concierge"
    )

    workflow.add_conditional_edges(
        "concierge",
        route_by_intent,
        {
            "inventory": "inventory",
            "invoice": "invoice",
            "market": "market",
            "end": END,
        },
    )

    workflow.add_edge(
        "inventory",
        END
    )

    workflow.add_edge(
        "invoice",
        END
    )

    workflow.add_edge(
        "market",
        END
    )

    return workflow.compile()