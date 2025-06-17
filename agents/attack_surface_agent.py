from openai import OpenAI, OpenAIError
import os
import streamlit as st

def handle_attack_surface_query(query: str, context: dict = None) -> str:
    """
    Handle queries related to attack surface management using OpenAI API.
    Args:
        query (str): The user query.
        context (dict, optional): Additional context for the query.
    Returns:
        str: The agent's response.
    """
    try:
        client = OpenAI(api_key=st.secrets["openai"]["api_key"])
        if not api_key:
            raise ValueError("OpenAI API key not found in Streamlit secrets")

        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in attack surface management."},
                {"role": "user", "content": query}
            ]
        )

        return response.choices[0].message.content

    except OpenAIError as e:
        return f"An OpenAI error occurred while processing your request: {str(e)}"
    except Exception:
        return "This is the Attack Surface Management Agent. I can help with questions about asset discovery, external exposure, and attack surface reduction."