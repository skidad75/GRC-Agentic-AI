
from agents.cyber_agent import handle_cyber_query
from agents.grc_agent import handle_grc_query

def determine_agent(query: str) -> str:
    cyber_keywords = ["vulnerability", "attack", "incident", "penetration test", "firewall", "zero-day", "SIEM"]
    grc_keywords = ["policy", "compliance", "audit", "HIPAA", "risk", "governance", "framework", "NIST", "SOC 2"]

    query_lower = query.lower()

    if any(word in query_lower for word in cyber_keywords):
        return "cyber"
    elif any(word in query_lower for word in grc_keywords):
        return "grc"
    else:
        return "grc"

def route_query(query: str, context: dict = None) -> dict:
    selected_agent = determine_agent(query)

    if selected_agent == "cyber":
        response = handle_cyber_query(query, context)
    else:
        response = handle_grc_query(query, context)

    return {
        "agent": selected_agent,
        "response": response
    }
