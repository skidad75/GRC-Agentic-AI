
def query_vector_db(query, namespace="grc", top_k=4):
    return [
        "NIST CSF control ID PR.AC-1 requires identity management...",
        "Providence GRC policy 2023.4 indicates a risk scoring threshold of..."
    ]

def format_rag_prompt(query, docs, persona="You are an expert..."):
    context = "\n\n".join(docs)
    return f"""{persona}

Use the following documents to answer the query:
{context}

Question: {query}

Answer:"""
