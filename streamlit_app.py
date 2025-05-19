import os
import sys
import streamlit as st
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Set up the Streamlit page - MUST be the first Streamlit command
#st.set_page_config(page_title="Cyber GRC Agentic AI", layout="wide")

# Modern professional styling
st.markdown(
    '''<style>
    /* Modern color scheme and base styles */
    :root {
        --primary-color: #1E3A8A;
        --secondary-color: #2563EB;
        --accent-color: #3B82F6;
        --text-color: #1F2937;
        --light-bg: #F3F4F6;
        --border-color: #E5E7EB;
    }
    
    /* Main container */
    .main .block-container { 
        padding: 1rem 2rem !important;
        max-width: 1400px !important;
    }
    
    /* Header styling */
    .main .block-container h1, .main .block-container h1:first-child {
        color: var(--primary-color) !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        font-family: 'Segoe UI', 'Arial', sans-serif !important;
        line-height: 1.2 !important;
        margin-bottom: 1rem !important;
        border-bottom: 2px solid var(--border-color) !important;
        padding-bottom: 0.5rem !important;
    }
    
    /* Subheaders */
    .stMarkdown h2, h2, .stMarkdown h3, h3, .stMarkdown h4, h4 {
        color: var(--primary-color) !important;
        font-family: 'Segoe UI', 'Arial', sans-serif !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        margin: 1rem 0 0.5rem 0 !important;
    }
    
    /* Form elements */
    .stRadio label, .stTextInput label, .stButton > button, .stMarkdown p, p {
        font-family: 'Segoe UI', 'Arial', sans-serif !important;
        font-size: 1rem !important;
        color: var(--text-color) !important;
    }
    
    /* Modern buttons */
    .stButton > button { 
        background-color: var(--secondary-color) !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: var(--primary-color) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    /* Modern text inputs */
    .stTextInput > div > div > input { 
        border: 1px solid var(--border-color) !important;
        border-radius: 4px !important;
        padding: 0.5rem !important;
        font-size: 1rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 2px rgba(59,130,246,0.1) !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background-color: var(--light-bg) !important;
        border-radius: 4px !important;
        padding: 0.5rem !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Sidebar */
    .stSidebar {
        background-color: var(--light-bg) !important;
    }
    .stSidebar .block-container { 
        padding: 1rem !important;
    }
    .stSidebar .stMarkdown {
        color: var(--text-color) !important;
    }
    
    /* Dividers */
    hr { 
        border: none !important;
        border-top: 1px solid var(--border-color) !important;
        margin: 1rem 0 !important;
    }
    
    /* Form containers */
    .stForm {
        background-color: white !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
    }
    
    /* Success/error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 4px !important;
        padding: 0.75rem !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Sample prompts section */
    .prompt-section {
        background-color: var(--light-bg) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
    }
    .prompt-button {
        background-color: white !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 4px !important;
        padding: 0.5rem !important;
        margin: 0.25rem !important;
        transition: all 0.2s ease !important;
    }
    .prompt-button:hover {
        background-color: var(--accent-color) !important;
        color: white !important;
        border-color: var(--accent-color) !important;
    }
    
    /* Footer */
    footer {
        text-align: center !important;
        padding: 1rem !important;
        color: var(--text-color) !important;
        border-top: 1px solid var(--border-color) !important;
    }
    </style>''',
    unsafe_allow_html=True
)

# Use inline HTML for the main header
st.markdown("""
<h1 style='color:#1E3A8A;font-size:2.2rem;font-weight:800;font-family:Segoe UI,Arial,sans-serif;line-height:1.2;margin-bottom:1rem;border-bottom:2px solid #E5E7EB;padding-bottom:0.5rem;'>🧠 Cyber GRC Agentic AI Assistant</h1>
""", unsafe_allow_html=True)

# Auto-collapse the sidebar on page load (unofficial JS hack)
st.components.v1.html(
    '''<script>
    window.addEventListener('DOMContentLoaded', function() {
        const sidebar = window.parent.document.querySelector('section[data-testid="stSidebar"]');
        const collapseButton = window.parent.document.querySelector('button[title="Collapse sidebar"]');
        if (sidebar && collapseButton && !sidebar.classList.contains('collapsed')) {
            collapseButton.click();
        }
    });
    </script>''',
    height=0,
    width=0
)

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

def get_public_ip():
    """
    Retrieve the public IP address of the client machine using an external API.
    Returns:
        str or None: The public IP address as a string, or None if retrieval fails.
    """
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text
    except:
        return None

def get_last_hop_city_region_country():
    """
    Perform a traceroute to 8.8.8.8 and return the city, region, and country of the last hop IP address.
    Uses the IPinfo API for geolocation. Returns a fallback string if any step fails.
    Returns:
        str: Location in the format 'City, Region, Country' or a fallback string if unavailable.
    """
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
    """
    Retrieve the city, region, and country of the client based on their public IP address.
    Uses the IPinfo API for geolocation. Returns a fallback string if any step fails.
    Returns:
        str: Location in the format 'City, Region, Country' or a fallback string if unavailable.
    """
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
    """
    Load the community search history from the JSON file defined by SEARCHES_FILE.
    Returns:
        list: A list of previous community searches, or an empty list if loading fails.
    """
    try:
        if os.path.exists(SEARCHES_FILE):
            with open(SEARCHES_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading community searches: {str(e)}")
    return []

def save_community_searches(searches):
    """
    Save the community search history to the JSON file defined by SEARCHES_FILE.
    Args:
        searches (list): The list of community searches to save.
    """
    try:
        with open(SEARCHES_FILE, 'w') as f:
            json.dump(searches, f)
    except Exception as e:
        st.error(f"Error saving community searches: {str(e)}")

# Health check function
def send_alert_email(subject, message):
    """
    Send an alert email using Gmail SMTP with the given subject and message.
    Args:
        subject (str): The subject of the email.
        message (str): The body of the email.
    """
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
    """
    Check if the Streamlit app is healthy by sending a request to its public URL.
    If the app is not healthy, send an alert email.
    """
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

# Initialize session state for community searches if it doesn't exist
if 'community_searches' not in st.session_state:
    st.session_state['community_searches'] = load_community_searches()
if 'last_query' not in st.session_state:
    st.session_state['last_query'] = ""
if 'user_query' not in st.session_state:
    st.session_state['user_query'] = ""

# Inject JS to capture user agent and store in Streamlit session state (no visible input)
if 'user_agent' not in st.session_state or not st.session_state['user_agent']:
    st.components.v1.html(
        '''<script>
        const userAgent = navigator.userAgent;
        window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'user_agent', value: userAgent}, '*');
        </script>''',
        height=0,
        width=0
    )
    # Fallback: set to empty string if not set by JS
    if 'user_agent' not in st.session_state:
        st.session_state['user_agent'] = ''

# Create a two-column layout for the main content
col1, col2 = st.columns([2, 1])

with col1:
    # Agent selection with auto-select option
    st.markdown("### Query Configuration")
    agent_mode = st.radio(
        "Choose how to handle your query:",
        ["Auto-select Agent", "Use Specific Agent"],
        horizontal=True
    )

    if agent_mode == "Use Specific Agent":
        kb_choice = st.radio("Choose a knowledge base:", ["Cyber", "GRC", "Attack Surface", "Risk Management"])
    else:
        kb_choice = None

    # Query input form
    with st.form("query_form", clear_on_submit=False):
        user_query = st.text_input("Enter your question:", key="user_query_input")
        submitted = st.form_submit_button("Submit")

    # Determine which query to use
    query_to_use = None
    if st.session_state.get('user_query'):
        query_to_use = st.session_state['user_query']
        st.session_state['user_query'] = ""  # Clear after use
    elif submitted and st.session_state.get('user_query_input'):
        query_to_use = st.session_state['user_query_input']

    if query_to_use:
        user_query = query_to_use
        if agent_mode == "Auto-select Agent":
            with st.spinner("Thinking..."):
                result = route_query(user_query)
                agent_used = result['agent']
                st.success(f"Response from {agent_used.upper()} Agent")
                st.markdown(result["response"])
        else:
            force_agent = None
            if kb_choice == "Cyber":
                force_agent = "cyber"
            elif kb_choice == "GRC":
                force_agent = "grc"
            elif kb_choice == "Attack Surface":
                force_agent = "attack_surface"
            elif kb_choice == "Risk Management":
                force_agent = "risk_management"
            with st.spinner("Thinking..."):
                result = route_query(user_query, force_agent=force_agent)
                agent_used = result['agent']
                st.success(f"Response from {agent_used.upper()} Agent")
                st.markdown(result["response"])

        # Update community search history if it's a new query
        if user_query != st.session_state['last_query']:
            # Add new search to the beginning of the list
            search_entry = {
                'query': user_query,
                'timestamp': datetime.now().isoformat(),
                'ip': get_public_ip(),
                'location': get_client_location(),
                'agent': agent_used,
                'kb_choice': kb_choice if kb_choice else 'Auto-selected',
                'cookies': st.experimental_get_query_params().get('cookies', ''),
                'user_agent': st.session_state.get('user_agent', '')
            }
            st.session_state['community_searches'].insert(0, search_entry)
            # Keep only the last MAX_SEARCHES entries
            if len(st.session_state['community_searches']) > MAX_SEARCHES:
                st.session_state['community_searches'] = st.session_state['community_searches'][:MAX_SEARCHES]
            # Save to file
            save_community_searches(st.session_state['community_searches'])
            st.session_state['last_query'] = user_query
            st.session_state['user_query_input'] = ""
            st.rerun()

with col2:
    st.markdown("### Sample Prompts")
    st.markdown("Click a prompt to get started:")
    
    # Define prompts for each discipline
    cyber_prompts = [
        "What is a SIEM and how does it work?",
        "List common types of cyber attacks on healthcare systems.",
        "How do you secure a cloud-based application?",
        "Explain the principle of least privilege in cybersecurity.",
        "What are the steps in incident response for a ransomware attack?",
    ]
    grc_prompts = [
        "What is the purpose of a risk register in GRC?",
        "How do you perform a NIST CSF gap analysis?",
        "What are the main components of HIPAA compliance?",
        "Describe the process of a GRC audit.",
        "How do you map controls to ISO 27001 Annex A?",
    ]
    attack_surface_prompts = [
        "How do you discover external assets for attack surface management?",
        "What tools are used for attack surface monitoring?",
        "Explain the importance of reducing digital footprint.",
        "How do you identify shadow IT in an organization?",
        "What is continuous attack surface management?",
    ]
    risk_management_prompts = [
        "How do you perform a qualitative risk assessment?",
        "What is risk appetite and how is it defined?",
        "Describe the process of risk mitigation planning.",
        "How do you use a risk matrix in decision making?",
        "What are the key steps in a risk management lifecycle?",
    ]

    # Display prompts in a compact grid
    for label, prompts in [
        ("Cyber", cyber_prompts),
        ("GRC", grc_prompts),
        ("Attack Surface", attack_surface_prompts),
        ("Risk Management", risk_management_prompts),
    ]:
        st.markdown(f"**{label}**")
        for prompt in prompts:
            if st.button(prompt, key=f"prompt_{label}_{prompt}", use_container_width=True):
                st.session_state['user_query'] = prompt
                st.session_state['last_query'] = prompt
                st.rerun()

# Add footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; margin: 20px 0;'>
    <a href="https://buymeacoffee.com/skidad75" target="_blank">
        <img src="https://img.shields.io/badge/☕%20Buy%20Me%20a%20Coffee-skidad75-yellow?style=for-the-badge" alt="Buy Me a Coffee">
    </a>
    <br/>
    <a href="https://github.com/skidad75/grc-agentic-ai" target="_blank">
        <img src="https://img.shields.io/badge/GitHub-Source%20Code-blue?style=for-the-badge&logo=github" alt="GitHub">
    </a>
</div>
""", unsafe_allow_html=True) 