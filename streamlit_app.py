import os
import sys
import streamlit as st

# Set up the Streamlit page - MUST be the first Streamlit command
st.set_page_config(page_title="Cyber GRC Agentic AI", layout="wide")

import requests
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import json
import pathlib
import streamlit.components.v1 as components
import subprocess

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Constants
SEARCHES_FILE = os.path.join(project_root, "community_searches.json")
MAX_SEARCHES = 100

# Import after path setup
from app.agent_router import route_query

# Initialize RAG functionality with fallback
RAG_AVAILABLE = False
try:
    # LlamaIndex imports
    from llama_index.core import VectorStoreIndex
    from llama_index.readers.file import SimpleDirectoryReader
    from llama_index.llms.openai import OpenAI
    
    # Build the RAG indices with feedback
    st.info("Loading RAG documents...")
    cyber_docs = SimpleDirectoryReader("rag_docs/cyber").load_data()
    grc_docs = SimpleDirectoryReader("rag_docs/grc").load_data()
    
    # Show document loading status
    st.success(f"✅ Loaded {len(cyber_docs)} Cyber documents and {len(grc_docs)} GRC documents")
    
    # Build indices
    with st.spinner("Building vector indices..."):
        cyber_index = VectorStoreIndex.from_documents(cyber_docs)
        grc_index = VectorStoreIndex.from_documents(grc_docs)
        cyber_query_engine = cyber_index.as_query_engine()
        grc_query_engine = grc_index.as_query_engine()
    
    st.success("✅ Vector indices built successfully")
    RAG_AVAILABLE = True
except ImportError:
    # Silently handle missing llama_index module
    RAG_AVAILABLE = False
except Exception as e:
    # Handle other potential errors silently
    RAG_AVAILABLE = False

# Add a tag to indicate which approach is being used
if RAG_AVAILABLE:
    st.sidebar.markdown("🔍 Using RAG-based search")
else:
    st.sidebar.markdown("🤖 Using agent-based search")

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text
    except:
        return None

def get_last_hop_city_region_country():
    try:
        # Run traceroute to a public IP (e.g., 8.8.8.8)
        result = subprocess.run(
            ["traceroute", "-n", "8.8.8.8"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        lines = result.stdout.strip().split('\n')
        if len(lines) < 2:
            st.info("Traceroute output too short:")
            st.code(result.stdout)
            return "Somewhere in the multiverse..."
        # Get the last hop IP address
        last_hop_line = lines[-1]
        parts = last_hop_line.split()
        last_hop_ip = None
        for part in parts:
            if part.count('.') == 3:
                last_hop_ip = part
                break
        if not last_hop_ip:
            st.info(f"No valid IP found in last hop line: {last_hop_line}")
            return "Somewhere in the multiverse..."
        # Use full IPinfo API to get city, region, country
        token = st.secrets["ipinfo"]["token"]
        response = requests.get(f"https://ipinfo.io/{last_hop_ip}/json?token={token}")
        if response.status_code == 200:
            data = response.json()
            city = data.get('city', '')
            region = data.get('region', '')
            country = data.get('country', '')
            # Format: City, Region, Country (only include what is available)
            location_parts = [part for part in [city, region, country] if part]
            if location_parts:
                return ", ".join(location_parts)
            else:
                st.info(f"No city/region/country found for IP {last_hop_ip}: {data}")
        else:
            st.info(f"IPinfo request failed for {last_hop_ip}: {response.status_code} {response.text}")
        return "Somewhere in the multiverse..."
    except Exception as e:
        st.info(f"Error tracing route: {str(e)}")
        return "Somewhere in the multiverse..."

def get_client_location():
    try:
        client_ip = get_public_ip()
        if not client_ip:
            return "Somewhere in the multiverse..."
        token = st.secrets["ipinfo"]["token"]
        response = requests.get(f"https://ipinfo.io/{client_ip}/json?token={token}")
        if response.status_code == 200:
            data = response.json()
            city = data.get('city', '')
            region = data.get('region', '')
            country = data.get('country', '')
            location_parts = [part for part in [city, region, country] if part]
            if location_parts:
                return ", ".join(location_parts)
            else:
                st.info(f"No city/region/country found for IP {client_ip}: {data}")
        else:
            st.info(f"IPinfo request failed for {client_ip}: {response.status_code} {response.text}")
        return "Somewhere in the multiverse..."
    except Exception as e:
        st.info(f"Error getting client location: {str(e)}")
        return "Somewhere in the multiverse..."

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

# Add Test Prompts Section
st.subheader("📋 Sample Prompts")
st.markdown("Click any prompt below to quickly get started:")

# Create three columns for the prompts
col1, col2, col3 = st.columns(3)

# Define the prompts
test_prompts = [
    "Evaluate whether this cloud-hosted patient portal is HIPAA-compliant.",
    "Perform a NIST CSF gap analysis for the uploaded system architecture.",
    "Which controls from HITRUST apply to a mobile health application?",
    "Assess the risk posture of an IoT-connected blood pressure monitor.",
    "Generate a summary of technical safeguards based on HIPAA §164.312.",
    "Analyze this architecture for attack vectors under MITRE ATT&CK.",
    "Is role-based access control (RBAC) configured according to Providence policies?",
    "Identify any AI-specific risks in this ML-based clinical decision support tool.",
    "What GRC implications arise from using public cloud for PHI storage?",
    "Provide an audit checklist for SOC 2 Type II compliance.",
    "How would an internal red team test this external-facing API?",
    "Flag any gaps between this solution and OWASP Top 10 requirements.",
    "Review this vendor's service for third-party risk classification.",
    "Map this deployment to ISO 27001 Annex A control categories.",
    "Does this solution architecture align with Providence's AI governance framework?"
]

# Distribute prompts across columns
prompts_per_column = len(test_prompts) // 3
for i, prompt in enumerate(test_prompts):
    col = col1 if i < prompts_per_column else (col2 if i < 2 * prompts_per_column else col3)
    if col.button(prompt, key=f"prompt_{i}", use_container_width=True):
        st.session_state.last_query = prompt
        st.rerun()

st.markdown("---")

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
            # Get agent info with better fallback handling
            agent_info = search.get('agent', 'Unknown')
            if agent_info == 'Unknown' and 'kb_choice' in search:
                agent_info = f"{search['kb_choice']} RAG"
            st.markdown(f"🤖 Agent: {agent_info}")
            st.markdown(f"📍 {search['location']}")
            st.markdown("---")
    else:
        st.info("No searches yet. Be the first to search!")

st.subheader("Ask the Cyber or GRC Knowledge Base")

# Agent selection with auto-select option
agent_mode = st.radio(
    "Choose how to handle your query:",
    ["Auto-select Agent", "Use Specific Agent"],
    horizontal=True
)

if agent_mode == "Use Specific Agent":
    kb_choice = st.radio("Choose a knowledge base:", ["Cyber", "GRC"])
else:
    kb_choice = None

user_query = st.text_input("Enter your question:")

if user_query:
    if agent_mode == "Auto-select Agent":
        # Let the agent router decide
        with st.spinner("Thinking..."):
            result = route_query(user_query)
            agent_used = result['agent']
            st.success(f"Response from {agent_used.upper()} Agent")
            st.markdown(result["response"])
    else:
        # Use specific agent based on selection
        if RAG_AVAILABLE:
            with st.spinner("Retrieving answer from curated docs..."):
                try:
                    if kb_choice == "Cyber":
                        st.info("🔍 Searching Cyber knowledge base...")
                        response = cyber_query_engine.query(user_query)
                        agent_used = "Cyber RAG"
                    else:
                        st.info("🔍 Searching GRC knowledge base...")
                        response = grc_query_engine.query(user_query)
                        agent_used = "GRC RAG"
                    st.success("✅ Found relevant information in knowledge base")
                    st.write(response.response)
                except Exception as e:
                    st.warning(f"RAG search failed: {str(e)}")
                    st.warning("Falling back to agent-based search...")
                    # Force the specific agent
                    result = route_query(user_query, force_agent=kb_choice.lower())
                    agent_used = result['agent']
                    st.success(f"Response from {agent_used.upper()} Agent")
                    st.markdown(result["response"])
        else:
            # Use agent-based search with forced agent
            with st.spinner("Thinking..."):
                result = route_query(user_query, force_agent=kb_choice.lower())
                agent_used = result['agent']
                st.success(f"Response from {agent_used.upper()} Agent")
                st.markdown(result["response"])

    # Update community search history if it's a new query
    if user_query != st.session_state.last_query:
        # Add new search to the beginning of the list
        search_entry = {
            'query': user_query,
            'location': get_client_location(),
            'agent': agent_used,
            'kb_choice': kb_choice if kb_choice else 'Auto-selected'
        }
        st.session_state.community_searches.insert(0, search_entry)
        
        # Keep only the last MAX_SEARCHES entries
        if len(st.session_state.community_searches) > MAX_SEARCHES:
            st.session_state.community_searches = st.session_state.community_searches[:MAX_SEARCHES]
        
        # Save to file
        save_community_searches(st.session_state.community_searches)
        st.session_state.last_query = user_query
        # Force a rerun to update the sidebar
        st.rerun() 