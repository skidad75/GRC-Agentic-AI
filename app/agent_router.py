from agents.cyber_agent import handle_cyber_query
from agents.grc_agent import handle_grc_query
from agents.attack_surface_agent import handle_attack_surface_query
from agents.risk_management_agent import handle_risk_management_query
from openai import OpenAI
import httpx

from openai import OpenAI
import streamlit as st

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
        elif force_agent.lower() == 'attack_surface':
            return {
                "agent": "attack_surface",
                "response": handle_attack_surface_query(query)
            }
        elif force_agent.lower() == 'risk_management':
            return {
                "agent": "risk_management",
                "response": handle_risk_management_query(query)
            }
        else:
            raise ValueError(f"Invalid agent specified: {force_agent}. Must be 'cyber', 'grc', 'attack_surface', or 'risk_management'.")

    # Simple keyword-based routing for auto-selection
    cyber_keywords = ['cyber', 'security', 'threat', 'vulnerability', 'attack', 'firewall', 'siem']
    grc_keywords = ['compliance', 'policy', 'risk', 'governance', 'audit', 'hipaa', 'nist', 'hitrust']
    attack_surface_keywords = ['attack surface', 'asset discovery', 'external exposure', 'surface management', 'external asset']
    risk_management_keywords = ['risk management', 'risk assessment', 'mitigation', 'risk framework', 'risk register', 'risk appetite']

    query_lower = query.lower()

    # Check for attack surface management keywords
    if any(keyword in query_lower for keyword in attack_surface_keywords):
        return {
            "agent": "attack_surface",
            "response": handle_attack_surface_query(query)
        }
    # Check for risk management keywords
    elif any(keyword in query_lower for keyword in risk_management_keywords):
        return {
            "agent": "risk_management",
            "response": handle_risk_management_query(query)
        }
    # Check for cyber security keywords
    elif any(keyword in query_lower for keyword in cyber_keywords):
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
