from agents.cyber_agent import handle_cyber_query
from agents.grc_agent import handle_grc_query

def route_query(query: str, force_agent: str = None) -> dict:
    # If an agent is forced, use it directly
    if force_agent:
        if force_agent.lower() == 'cyber':
            return {
                "agent": "cyber",
                "response": handle_cyber_query(query)
            }
        elif force_agent.lower() == 'grc':
            return {
                "agent": "grc",
                "response": handle_grc_query(query)
            }
        else:
            raise ValueError(f"Invalid agent specified: {force_agent}. Must be 'cyber' or 'grc'.")

    # Simple keyword-based routing for auto-selection
    cyber_keywords = ['cyber', 'security', 'threat', 'vulnerability', 'attack', 'firewall', 'siem']
    grc_keywords = ['compliance', 'policy', 'risk', 'governance', 'audit', 'hipaa', 'nist', 'hitrust']
    
    query_lower = query.lower()
    
    # Check for cyber security keywords
    if any(keyword in query_lower for keyword in cyber_keywords):
        return {
            "agent": "cyber",
            "response": handle_cyber_query(query)
        }
    
    # Check for GRC keywords
    elif any(keyword in query_lower for keyword in grc_keywords):
        return {
            "agent": "grc",
            "response": handle_grc_query(query)
        }
    
    # Default to GRC if no specific keywords are found
    else:
        return {
            "agent": "grc",
            "response": handle_grc_query(query)
        }
