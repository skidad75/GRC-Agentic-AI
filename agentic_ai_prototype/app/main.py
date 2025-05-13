import streamlit as st
import tempfile
import os
import json
from datetime import datetime
from .agent_router import route_query

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

# Initialize session state for search history if it doesn't exist
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Try importing voice-related packages, but don't fail if they're not available
try:
    import speech_recognition as sr
    from gtts import gTTS
    VOICE_FEATURES_AVAILABLE = True
except ImportError:
    VOICE_FEATURES_AVAILABLE = False

st.set_page_config(page_title="Healthcare Organization Agentic AI", layout="wide")

st.title("🧠 Healthcare Organization Agentic AI Assistant")
st.markdown("Ask a question related to cybersecurity or GRC.")

# Display shared search history
st.subheader("🔍 Recent Community Searches")
shared_history = load_shared_history()

if shared_history:
    # Display searches in a more visible way
    for search in reversed(shared_history[-5:]):  # Show last 5 searches
        st.markdown(f"*{search['query']}* - {search['timestamp']}")
else:
    st.info("No recent community searches yet. Your search will appear here when you make one!")

# Sample prompts section
st.subheader("📝 Sample Prompts")
sample_prompts = [
    "What are the key requirements for HIPAA compliance?",
    "How should we handle a data breach incident?",
    "What are the best practices for access control?",
    "Explain the NIST cybersecurity framework",
    "What are the requirements for incident response planning?"
]

# Display sample prompts as buttons
cols = st.columns(3)
for i, prompt in enumerate(sample_prompts):
    if cols[i % 3].button(prompt, key=f"prompt_{i}"):
        st.session_state.query = prompt

# Voice input section (only show if voice features are available)
if VOICE_FEATURES_AVAILABLE:
    st.subheader("🎤 Voice Input")
    if st.button("Start Recording"):
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                st.info("Listening... Speak now!")
                try:
                    audio = recognizer.listen(source, timeout=5)
                    text = recognizer.recognize_google(audio)
                    st.session_state.query = text
                    st.success(f"Recognized: {text}")
                except sr.WaitTimeoutError:
                    st.warning("No speech detected within timeout period.")
                except sr.UnknownValueError:
                    st.warning("Could not understand audio. Please try again.")
                except sr.RequestError as e:
                    st.error(f"Could not request results; {str(e)}")
                except Exception as e:
                    st.error(f"Error during voice recognition: {str(e)}")
        except Exception as e:
            st.warning("Voice input is not available in this environment. Please use text input instead.")
            st.info("Voice features are only available when running the app locally with a microphone.")
else:
    st.info("ℹ️ Voice input is not available in this environment. Please use text input instead.")

# Text input section
query = st.text_input("Enter your query here:", value=st.session_state.get("query", ""))

if query:
    # Add query to shared history
    current_history = load_shared_history()
    new_entry = {
        'query': query,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Add new search if it's not the same as the last one
    if not current_history or current_history[-1]['query'] != query:
        current_history.append(new_entry)
        # Keep only the last 10 searches
        if len(current_history) > 10:
            current_history.pop(0)
        save_shared_history(current_history)
            
    with st.spinner("Thinking..."):
        result = route_query(query)
        st.success(f"Response from {result['agent'].upper()} Agent")
        st.markdown(result["response"])
        
        # Text-to-speech for the response (only if available)
        if VOICE_FEATURES_AVAILABLE:
            if st.button("🔊 Read Response"):
                try:
                    tts = gTTS(text=result["response"], lang='en')
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                        tts.save(fp.name)
                        st.audio(fp.name, format='audio/mp3')
                        os.unlink(fp.name)  # Clean up the temporary file
                except Exception as e:
                    st.warning("Text-to-speech is not available in this environment.")
        else:
            st.info("ℹ️ Text-to-speech is not available in this environment.")