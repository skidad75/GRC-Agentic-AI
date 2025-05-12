import openai
from openai import OpenAIError
import os
from dotenv import load_dotenv
from agents.shared_tools import query_vector_db, format_rag_prompt

load_dotenv()

# Fallback responses for when API is unavailable
GRC_FALLBACK_RESPONSES = {
    "policy": "A policy is a formal statement of principles and rules that guide an organization's operations and decision-making processes.",
    "compliance": "Compliance refers to adhering to laws, regulations, standards, and ethical practices that apply to an organization's operations.",
    "risk": "Risk management involves identifying, assessing, and controlling threats to an organization's capital and earnings.",
    "audit": "An audit is a systematic examination of records, statements, or other evidence to verify compliance with established standards.",
    "default": "I understand you're asking about GRC (Governance, Risk, and Compliance). While I'm currently unable to provide a detailed response due to API limitations, I can tell you that GRC is a framework that helps organizations align their IT activities with business goals, manage risks effectively, and meet regulatory requirements."
}

def handle_grc_query(query: str, context: dict = None) -> str:
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a GRC (Governance, Risk, and Compliance) expert assistant."},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        if "insufficient_quota" in str(e):
            # Try to match query with fallback responses
            query_lower = query.lower()
            for key, response in GRC_FALLBACK_RESPONSES.items():
                if key in query_lower:
                    return response
            return GRC_FALLBACK_RESPONSES["default"]
        else:
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
