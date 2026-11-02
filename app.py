import streamlit as st
import google.generativeai as genai
from PIL import Image
import urllib.parse

# Page Config
st.set_page_config(page_title="Indian GPT - Vision AI", page_icon="🇮🇳", layout="wide")

# Custom CSS for clean UI
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stSidebar { background-color: #f7f7f8; }
    </style>
""", unsafe_allow_html=True)

# Sidebar for API Key & Settings
with st.sidebar:
    st.subheader("🔑 AI Configuration")
    api_key = st.text_input("Enter Google Gemini API Key", type="password", help="Free API key pabe Google AI Studio theke")
    st.markdown("[Get Free Gemini API Key](https://aistudio.google.com/)")
    
    st.markdown("---")
    if st.button("➕ New Chat", use_container_width=True):
        new_chat_name = "New Chat"
        counter = 1
        while new_chat_name in st.session_state.get("chat_sessions", {}):
            new_chat_name = f"New Chat {counter}"
            counter += 1
        
        st.session_state.chat_sessions[new_chat_name] = [{"role": "assistant", "content": "Hi bro! Ami Indian GPT. Amake lekha ba chobi diye jekono question korte paro!"}]
        st.session_state.current_chat = new_chat_name
        st.rerun()

    st.markdown("---")
    st.subheader("📁 Upload Image (Vision AI)")
    uploaded_image = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    
    if uploaded_image:
        img_preview = Image.open(uploaded_image)
        st.image(img_preview, caption="Uploaded Image Preview", use_container_width=True)

    st.markdown("---")
    st.subheader("💬 Chat History")
    
    if "chat_sessions" in st.session_state:
        for chat_name in list(st.session_state.chat_sessions.keys()):
            if st.button(chat_name, use_container_width=True, key=chat_name):
                st.session_state.current_chat = chat_name
                st.rerun()

    st.markdown("---")
    st.caption("Indian GPT - Multimodal Vision Edition")

# Initialize Session States
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {
        "New Chat": [{"role": "assistant", "content": "Hi bro! Ami Indian GPT. Amake lekha ba chobi diye jekono question korte paro!"}]
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

# Main Header
st.title("🇮🇳 Indian GPT (Vision Enabled)")

# Get current messages based on selected session
current_messages = st.session_state.chat_sessions[st.session_state.current_chat]

# Display current chat messages
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message and message["image"]:
            st.image(message["image"])

# Native Streamlit Chat Input
prompt = st.chat_input("Chobi ba lekha niye kichu jiggesh koro...")

# Handle User Input & AI Response
if prompt:
    if not api_key:
        st.warning("⚠️ Bhai, prothome sidebar-e tor Google Gemini API Key-ta din!")
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
        pil_img = None
        if uploaded_image:
            pil_img = Image.open(uploaded_image)
            user_msg["image"] = pil_img
        
        current_messages.append(user_msg)
        
        with st.chat_message("user"):
            st.markdown(prompt)
            if pil_img:
                st.image(pil_img)

        # Generate AI Response using Gemini Vision
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                contents = [prompt]
                if pil_img:
                    contents.append(pil_img)
                
                response = model.generate_content(contents)
                full_response = response.text
                
                message_placeholder.markdown(full_response)
                
                assistant_msg = {"role": "assistant", "content": full_response}
                current_messages.append(assistant_msg)
                
            except Exception as e:
                st.error(f"Error: {e}")
