
from agents.shared_tools import query_vector_db, format_rag_prompt
from openai import OpenAI

openai = OpenAI()

def handle_grc_query(query: str, context: dict = None) -> str:
    related_docs = query_vector_db(query, namespace="grc")
    prompt = format_rag_prompt(query, related_docs, persona="You are a GRC compliance expert...")
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()
