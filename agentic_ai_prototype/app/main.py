import streamlit as st
from app.agent_router import route_query

st.set_page_config(page_title="Providence Agentic AI", layout="wide")

st.title("🧠 Providence Agentic AI Assistant")
st.markdown("Ask a question related to cybersecurity or GRC.")

query = st.text_input("Enter your query here:")

if query:
    with st.spinner("Thinking..."):
        result = route_query(query)
        st.success(f"Response from {result['agent'].upper()} Agent")
        st.markdown(result["response"])
