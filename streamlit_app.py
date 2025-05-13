import os
import sys
import streamlit as st
import requests
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import json
import pathlib

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import after path setup
from app.agent_router import route_query

# Constants
MAX_SEARCHES = 100
SEARCHES_FILE = "community_searches.json"

def get_user_location():
    """Get user's location based on IP address"""
    try:
        # Get client IP from Streamlit
        client_ip = st.experimental_get_query_params().get("client_ip", [None])[0]
        if not client_ip:
            return "Unknown Location"
            
        # Use ipinfo.io with API key from secrets
        headers = {
            "Authorization": f"Bearer {st.secrets['ipinfo']['token']}"
        }
        response = requests.get(f"https://ipinfo.io/{client_ip}/json", headers=headers)
        if response.status_code == 200:
            data = response.json()
            city = data.get('city', '')
            country = data.get('country', '')
            return f"{city}, {country}" if city else "Unknown Location"
    except Exception as e:
        st.error(f"Error getting location: {str(e)}")
    return "Unknown Location"

def load_community_searches():
    """Load community searches from file"""
    try:
        if os.path.exists(SEARCHES_FILE):
            with open(SEARCHES_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading community searches: {str(e)}")
    return []

def save_community_searches(searches):
    """Save community searches to file"""
    try:
        with open(SEARCHES_FILE, 'w') as f:
            json.dump(searches, f)
    except Exception as e:
        st.error(f"Error saving community searches: {str(e)}")

# Health check function
def send_alert_email(subject, message):
    sender_email = "skidad75@gmail.com"
    receiver_email = "skidad75@gmail.com"
    password = st.secrets["email"]["password"]

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
    except Exception as e:
        st.error(f"Failed to send alert email: {str(e)}")

def check_app_health():
    try:
        # Check if the app is responding
        response = requests.get("https://cybergrc-agent.streamlit.app/")
        if response.status_code != 200:
            send_alert_email(
                "🚨 App Health Check Failed",
                f"The app is not responding correctly. Status code: {response.status_code}\nTime: {datetime.now()}"
            )
    except Exception as e:
        send_alert_email(
            "🚨 App Health Check Failed",
            f"The app is not accessible. Error: {str(e)}\nTime: {datetime.now()}"
        )

def run_health_check():
    while True:
        check_app_health()
        time.sleep(st.secrets.get("monitoring", {}).get("check_interval", 30))

# Start health check in background thread if monitoring is enabled
if st.secrets.get("monitoring", {}).get("enabled", False):
    health_check_thread = threading.Thread(target=run_health_check, daemon=True)
    health_check_thread.start()

# Set up the Streamlit page
st.set_page_config(page_title="Cyber GRC Agentic AI", layout="wide")

st.title("🧠 Cyber GRC Agentic AI Assistant")
st.markdown("Ask a question related to cybersecurity or GRC.")

# Add Buy Me a Coffee link
st.markdown("""
<div style='text-align: center; margin: 20px 0;'>
    <a href="https://buymeacoffee.com/skidad75" target="_blank">
        <img src="https://img.shields.io/badge/☕%20Buy%20Me%20a%20Coffee-skidad75-yellow?style=for-the-badge" alt="Buy Me a Coffee">
    </a>
</div>
""", unsafe_allow_html=True)

# Initialize session state for community searches if it doesn't exist
if 'community_searches' not in st.session_state:
    st.session_state.community_searches = load_community_searches()
if 'last_query' not in st.session_state:
    st.session_state.last_query = ""

# Sidebar for community searches
with st.sidebar:
    st.subheader("🔍 Community Search History")
    if st.session_state.community_searches:
        for search in st.session_state.community_searches[:10]:  # Show first 10 searches (most recent)
            st.markdown(f"*{search['query']}*")
            st.markdown(f"📍 {search['location']}")
            st.markdown("---")
    else:
        st.info("No searches yet. Be the first to search!")

query = st.text_input("Enter your query here:")

if query:
    # Process the query
    with st.spinner("Thinking..."):
        result = route_query(query)
        st.success(f"Response from {result['agent'].upper()} Agent")
        st.markdown(result["response"])
    
    # Update community search history if it's a new query
    if query != st.session_state.last_query:
        # Add new search to the beginning of the list
        st.session_state.community_searches.insert(0, {
            'query': query,
            'location': get_user_location()
        })
        
        # Keep only the last MAX_SEARCHES entries
        if len(st.session_state.community_searches) > MAX_SEARCHES:
            st.session_state.community_searches = st.session_state.community_searches[:MAX_SEARCHES]
        
        # Save to file
        save_community_searches(st.session_state.community_searches)
        st.session_state.last_query = query
        # Force a rerun to update the sidebar
        st.rerun() 