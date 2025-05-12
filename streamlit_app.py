import os
import sys
import streamlit as st

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app.agent_router import route_query

st.set_page_config(page_title="Healthcare Organization Agentic AI", layout="wide")

st.title("🧠 Healthcare Organization Agentic AI Assistant")
st.markdown("Ask a question related to cybersecurity or GRC.")

query = st.text_input("Enter your query here:")

if query:
    with st.spinner("Thinking..."):
        result = route_query(query)
        st.success(f"Response from {result['agent'].upper()} Agent")
        st.markdown(result["response"]) 