from graph_state import GraphState

def route_decision(state: GraphState):
    decision = state["routing_decision"]
    if decision.get("route_to_article_search"):
        return "article_search"
    elif decision.get("route_to_case_law"):
        return "case_law"
    elif decision.get("route_to_historical_context"):
        return "historical_context"
    else:
        return "synthesizer"
