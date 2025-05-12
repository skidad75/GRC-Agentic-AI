import openai
from openai import OpenAIError
import os
from dotenv import load_dotenv
from agents.shared_tools import query_vector_db, format_rag_prompt
import streamlit as st

load_dotenv()

# Fallback responses for when API is unavailable
CYBER_FALLBACK_RESPONSES = {
    "vulnerability": "A vulnerability is a weakness in a system that can be exploited by attackers to gain unauthorized access or cause harm.",
    "firewall": "A firewall is a network security device that monitors and filters incoming and outgoing network traffic based on predetermined security rules.",
    "siem": "SIEM (Security Information and Event Management) is a security solution that helps organizations detect, analyze, and respond to security threats.",
    "incident": "A security incident is any event that could lead to the loss of, or damage to, an organization's assets, data, or reputation.",
    "default": "I understand you're asking about cybersecurity. While I'm currently unable to provide a detailed response due to API limitations, I can tell you that cybersecurity involves protecting systems, networks, and programs from digital attacks."
}

def handle_cyber_query(query: str, context: dict = None) -> str:
    try:
        client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Cybersecurity expert assistant."},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        if "insufficient_quota" in str(e):
            # Try to match query with fallback responses
            query_lower = query.lower()
            for key, response in CYBER_FALLBACK_RESPONSES.items():
                if key in query_lower:
                    return response
            return CYBER_FALLBACK_RESPONSES["default"]
        else:
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
