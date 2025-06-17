from openai import OpenAI, OpenAIError
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

CYBER_FALLBACK_RESPONSES = {
    "vulnerability": "A vulnerability is a weakness in a system that can be exploited by attackers to gain unauthorized access or cause harm.",
    "firewall": "A firewall is a network security device that monitors and filters incoming and outgoing network traffic based on predetermined security rules.",
    "siem": "SIEM (Security Information and Event Management) is a security solution that helps organizations detect, analyze, and respond to security threats.",
    "incident": "A security incident is any event that could lead to the loss of, or damage to, an organization's assets, data, or reputation.",
    "default": "Cybersecurity involves protecting systems, networks, and programs from digital attacks."
}

def handle_cyber_query(query: str, context: dict = None) -> str:
    try:
        # Use Streamlit secrets or environment variable
        api_key = st.secrets["openai"]["api_key"]
        if not api_key:
            raise ValueError("OpenAI API key not found")

        # Instantiate new OpenAI client
        client = OpenAI(api_key=api_key)

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
            query_lower = query.lower()
            for key, fallback in CYBER_FALLBACK_RESPONSES.items():
                if key in query_lower:
                    return fallback
            return CYBER_FALLBACK_RESPONSES["default"]
        else:
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"