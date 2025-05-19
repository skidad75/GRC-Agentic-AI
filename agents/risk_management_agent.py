import openai
from openai import OpenAIError
import os
import streamlit as st

def handle_risk_management_query(query: str, context: dict = None) -> str:
    """
    Handle queries related to risk management. Uses OpenAI API if available, otherwise returns a fallback response.
    Args:
        query (str): The user query.
        context (dict, optional): Additional context for the query.
    Returns:
        str: The agent's response.
    """
    try:
        api_key = st.secrets["openai"]["api_key"]
        if not api_key:
            raise ValueError("OpenAI API key not found in Streamlit secrets")
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a risk management expert."},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return "This is the Risk Management Agent. I can help with questions about risk assessment, mitigation, and risk frameworks." 