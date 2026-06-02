from src.graph.state import EcommerceState


def route_by_intent(
    state: EcommerceState
):

    intent = state.get(
        "intent",
        "unknown"
    )

    if intent == "inventory":
        return "inventory"

    if intent == "invoice":
        return "invoice"

    if intent == "market":
        return "market"

    return "end"