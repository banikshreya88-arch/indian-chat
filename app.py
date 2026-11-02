import os
import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Indian GPT",
    page_icon="🇮🇳",
    layout="centered"
)

# Initialize API Key safely from Streamlit Secrets or environment variable
api_key = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("🚨 Gemini API Key not found! Please configure it in Streamlit Secrets.")
    st.stop()

# Configure Google GenAI
genai.configure(api_key=api_key)

# Use the latest stable Flash model
model = genai.GenerativeModel('gemini-2.5-flash')

# App Header
st.title("🇮🇳 Indian GPT")
st.markdown("Toral Indian AI assistant - Ask me anything!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input chat box
if prompt := st.chat_input("Ki jante chas bolo?"):
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Bhabchi..."):
            try:
                # Convert chat history for the model
                chat_history = [
                    {"role": m["role"], "parts": [m["content"]]} 
                    for m in st.session_state.messages
                ]
                
                chat = model.start_chat(history=chat_history[:-1])
                response = chat.send_message(prompt)
                
                bot_reply = response.text
                st.markdown(bot_reply)
                
                # Add assistant response to state
                st.session_state.messages.append({"role": "model", "content": bot_reply})
            except Exception as e:
                st.error(f"Error: {e}")import os
import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Indian GPT",
    page_icon="🇮🇳",
    layout="centered"
)

# Initialize API Key safely from Streamlit Secrets or environment variable
api_key = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("🚨 Gemini API Key not found! Please configure it in Streamlit Secrets.")
    st.stop()

# Configure Google GenAI
genai.configure(api_key=api_key)

# Use the latest stable Flash model
model = genai.GenerativeModel('gemini-2.5-flash')

# App Header
st.title("🇮🇳 Indian GPT")
st.markdown("Toral Indian AI assistant - Ask me anything!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input chat box
if prompt := st.chat_input("Ki jante chas bolo?"):
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Bhabchi..."):
            try:
                # Convert chat history for the model
                chat_history = [
                    {"role": m["role"], "parts": [m["content"]]} 
                    for m in st.session_state.messages
                ]
                
                chat = model.start_chat(history=chat_history[:-1])
                response = chat.send_message(prompt)
                
                bot_reply = response.text
                st.markdown(bot_reply)
                
                # Add assistant response to state
                st.session_state.messages.append({"role": "model", "content": bot_reply})
            except Exception as e:
                st.error(f"Error: {e}")
