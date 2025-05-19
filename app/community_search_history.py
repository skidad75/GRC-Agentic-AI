import streamlit as st
import json
import os
from datetime import datetime

# Path to the community search log file
SEARCHES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../community_searches.json")

st.set_page_config(page_title="Community Search History", layout="wide")
st.title("🔍 Community Search History")

# Load community searches
searches = []
if os.path.exists(SEARCHES_FILE):
    with open(SEARCHES_FILE, 'r') as f:
        try:
            searches = json.load(f)
        except Exception as e:
            st.error(f"Error loading search history: {str(e)}")

if not searches:
    st.info("No community searches logged yet.")
else:
    for entry in searches[:100]:
        st.markdown(f"**Prompt:** {entry.get('query', '')}")
        st.markdown(f"**Timestamp:** {entry.get('timestamp', '')}")
        st.markdown(f"**Agent:** {entry.get('agent', '')}")
        st.markdown(f"**Knowledge Base:** {entry.get('kb_choice', '')}")
        st.markdown(f"**IP:** {entry.get('ip', '')}")
        st.markdown(f"**Location:** {entry.get('location', '')}")
        st.markdown(f"**Cookies:** {entry.get('cookies', '')}")
        st.markdown(f"**User Agent:** {entry.get('user_agent', '')}")
        st.markdown("---") 