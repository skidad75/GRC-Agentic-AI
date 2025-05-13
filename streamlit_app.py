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

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import after path setup
from app.agent_router import route_query

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
    st.session_state.community_searches = []
if 'last_query' not in st.session_state:
    st.session_state.last_query = ""

# Sidebar for community searches
with st.sidebar:
    st.subheader("🔍 Community Search History")
    if st.session_state.community_searches:
        for search in reversed(st.session_state.community_searches[-10:]):  # Show last 10 searches
            st.markdown(f"**{search['timestamp']}**")
            st.markdown(f"*{search['query']}*")
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
        st.session_state.community_searches.append({
            'query': query,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.session_state.last_query = query
        # Force a rerun to update the sidebar
        st.rerun() 