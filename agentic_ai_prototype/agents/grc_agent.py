import openai
from openai import OpenAIError
import os
from dotenv import load_dotenv
from agents.shared_tools import query_vector_db, format_rag_prompt

load_dotenv()

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
            return "I apologize, but I'm currently unable to process your request due to API quota limitations. Please check your OpenAI API billing and quota status. In the meantime, you can try:\n\n1. Checking your OpenAI account billing status\n2. Upgrading your API plan if needed\n3. Contacting OpenAI support for assistance"
        else:
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
