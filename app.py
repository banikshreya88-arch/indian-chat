import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Indian GPT", page_icon="🇮🇳", layout="wide")

# Custom CSS for clean UI
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stSidebar { background-color: #f7f7f8; }
    </style>
""", unsafe_allow_html=True)

# Securely load API key from Streamlit Secrets (Hidden from everyone)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    api_key = None

# Sidebar Controls
with st.sidebar:
    st.subheader("🇮🇳 Indian GPT Control")
    
    if st.button("➕ New Chat", use_container_width=True):
        new_chat_name = "New Chat"
        counter = 1
        while new_chat_name in st.session_state.get("chat_sessions", {}):
            new_chat_name = f"New Chat {counter}"
            counter += 1
        
        st.session_state.chat_sessions[new_chat_name] = [{"role": "assistant", "content": "Namaste! Ami Indian GPT. Amake jekono question korte paro!"}]
        st.session_state.current_chat = new_chat_name
        st.rerun()

    st.markdown("---")
    st.subheader("💬 Chat History")
    
    if "chat_sessions" in st.session_state:
        for chat_name in list(st.session_state.chat_sessions.keys()):
            if st.button(chat_name, use_container_width=True, key=chat_name):
                st.session_state.current_chat = chat_name
                st.rerun()

    st.markdown("---")
    st.caption("Indian GPT - Text Edition")

# Initialize Session States
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {
        "New Chat": [{"role": "assistant", "content": "Namaste! Ami Indian GPT. Amake jekono question korte paro!"}]
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

# Main Header
st.title("🇮🇳 Indian GPT")
st.caption("Advanced Conversational Intelligence Platform")

# Get current messages based on selected session
current_messages = st.session_state.chat_sessions[st.session_state.current_chat]

# Display current chat messages
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Native Streamlit Chat Input
prompt = st.chat_input("Kichu ekta jiggesh koro...")

# Handle User Input & AI Response
if prompt:
    if not api_key:
        st.error("⚠️ System configuration missing. Please configure app secrets.")
    else:
        # Dynamic Chat Titling
        if st.session_state.current_chat.startswith("New Chat"):
            new_name = prompt[:25] + ("..." if len(prompt) > 25 else "")
            if new_name in st.session_state.chat_sessions:
                new_name = f"{new_name} (2)"
            
            st.session_state.chat_sessions[new_name] = st.session_state.chat_sessions.pop(st.session_state.current_chat)
            st.session_state.current_chat = new_name
            current_messages = st.session_state.chat_sessions[new_name]

        # Save user message
        user_msg = {"role": "user", "content": prompt}
        current_messages.append(user_msg)
        
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI Response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                full_response = response.text
                
                message_placeholder.markdown(full_response)
                
                assistant_msg = {"role": "assistant", "content": full_response}
                current_messages.append(assistant_msg)
                
            except Exception as e:
                st.error(f"Error: {e}")
