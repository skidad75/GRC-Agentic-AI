import openai
from openai import OpenAIError
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Fallback responses
CYBER_FALLBACK_RESPONSES = {
    "vulnerability": "A vulnerability is a weakness in a system that can be exploited by attackers to gain unauthorized access or cause harm.",
    "firewall": "A firewall is a network security device that monitors and filters incoming and outgoing network traffic based on predetermined security rules.",
    "siem": "SIEM (Security Information and Event Management) is a security solution that helps organizations detect, analyze, and respond to security threats.",
    "incident": "A security incident is any event that could lead to the loss of, or damage to, an organization's assets, data, or reputation.",
    "default": "I understand you're asking about cybersecurity. While I'm currently unable to provide a detailed response due to API limitations, cybersecurity involves protecting systems, networks, and programs from digital attacks."
}

def handle_cyber_query(query: str, context: dict = None) -> str:
    try:
        # Retrieve OpenAI API key directly from environment variable
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
            
        response = openai.ChatCompletion.create(
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
            for key, response in CYBER_FALLBACK_RESPONSES.items():
                if key in query_lower:
                    return response
            return CYBER_FALLBACK_RESPONSES["default"]
        else:
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"