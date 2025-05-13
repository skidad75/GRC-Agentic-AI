from agents.cyber_agent import handle_cyber_query
from agents.grc_agent import handle_grc_query

def route_query(query: str) -> dict:
    # Simple keyword-based routing
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
