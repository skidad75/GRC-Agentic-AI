import os
import sys
import json
import streamlit as st
from datetime import datetime

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# File to store shared search history
SEARCH_HISTORY_FILE = "shared_search_history.json"

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_shared_history():
    try:
        if os.path.exists(SEARCH_HISTORY_FILE):
            with open(SEARCH_HISTORY_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception:
        return []

def save_shared_history(history):
    try:
        with open(SEARCH_HISTORY_FILE, 'w') as f:
            json.dump(history, f)
    except Exception:
        pass  # Silently fail if we can't save

# Initialize shared search history
if 'shared_history' not in st.session_state:
    st.session_state.shared_history = load_shared_history()

# Display shared search history
st.subheader("🔍 Recent Community Searches")
if st.session_state.shared_history:
    for search in reversed(st.session_state.shared_history[-5:]):  # Show last 5 searches
        st.markdown(f"*{search['query']}* - {search['timestamp']}")
else:
    st.info("No recent community searches yet. Your search will appear here when you make one!")

# Import and run the main app
from app.main import *

# Update shared history after each query
if 'query' in st.session_state and st.session_state.query:
    current_history = st.session_state.shared_history
    new_entry = {
        'query': st.session_state.query,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Add new search if it's not the same as the last one
    if not current_history or current_history[-1]['query'] != st.session_state.query:
        current_history.append(new_entry)
        # Keep only the last 10 searches
        if len(current_history) > 10:
            current_history.pop(0)
        st.session_state.shared_history = current_history
        save_shared_history(current_history) 