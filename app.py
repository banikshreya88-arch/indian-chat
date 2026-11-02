import streamlit as st
import requests
import json
import urllib.parse

# Page Config
st.set_page_config(page_title="Indian Chat", page_icon="🇮🇳", layout="wide")

# Custom CSS for clean UI & fixed bottom chat
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .stSidebar {
        background-color: #f7f7f8;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session States
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {
        "New Chat": [{"role": "assistant", "content": "Hi bro i am your personal chatbot indian chat"}]
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

# Sidebar for Chat History & New Chat
with st.sidebar:
    if st.button("➕ New Chat", use_container_width=True):
        new_chat_name = "New Chat"
        counter = 1
        while new_chat_name in st.session_state.chat_sessions:
            new_chat_name = f"New Chat {counter}"
            counter += 1
        
        st.session_state.chat_sessions[new_chat_name] = [{"role": "assistant", "content": "Hi bro i am your personal chatbot indian chat"}]
        st.session_state.current_chat = new_chat_name
        st.rerun()

    st.markdown("---")
    st.subheader("📁 Upload Image")
    uploaded_image = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

    st.markdown("---")
    st.subheader("💬 Chat History")
    
    for chat_name in list(st.session_state.chat_sessions.keys()):
        if st.button(chat_name, use_container_width=True, key=chat_name):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.markdown("---")
    model_choice = st.selectbox("Select Model", ["llama3"])
    st.caption("Indian Chat - Your Private AI")

# Main Header
st.title("🇮🇳 Indian Chat")

# Get current messages based on selected session
current_messages = st.session_state.chat_sessions[st.session_state.current_chat]

# Display current chat messages
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_url" in message and message["image_url"]:
            st.image(message["image_url"])
        elif "image" in message and message["image"]:
            st.image(message["image"])

# Native Streamlit Chat Input (Stays locked & fixed at the very bottom automatically)
prompt = st.chat_input("Ki jante chas? (Ask anything or ask to generate an image...)")

# Handle User Input & AI Response
if prompt:
    if st.session_state.current_chat.startswith("New Chat"):
        new_name = prompt[:25] + ("..." if len(prompt) > 25 else "")
        if new_name in st.session_state.chat_sessions:
            new_name = f"{new_name} (2)"
        
        st.session_state.chat_sessions[new_name] = st.session_state.chat_sessions.pop(st.session_state.current_chat)
        st.session_state.current_chat = new_name
        current_messages = st.session_state.chat_sessions[new_name]

    user_msg = {"role": "user", "content": prompt}
    if uploaded_image:
        user_msg["image"] = uploaded_image
    
    current_messages.append(user_msg)
    
    with st.chat_message("user"):
        st.markdown(prompt)
        if uploaded_image:
            st.image(uploaded_image)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        generated_image_url = None
        
        try:
            is_image_request = any(keyword in prompt.lower() for keyword in ["generate image", "draw", "picture of", "create an image", "chobi banao", "photo banao"])
            
            if is_image_request:
                img_prompt = urllib.parse.quote(prompt)
                generated_image_url = f"https://image.pollinations.ai/prompt/{img_prompt}"
                full_response = f"Elo bhai, tor instructions moto chobi toiri kore diyechi:"
                message_placeholder.markdown(full_response)
                st.image(generated_image_url)
            else:
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": model_choice,
                        "prompt": prompt,
                        "stream": True
                    },
                    stream=True
                )
                
                if response.status_code == 200:
                    for line in response.iter_lines():
                        if line:
                            try:
                                body = json.loads(line.decode("utf-8"))
                            except:
                                body = eval(line.decode("utf-8").replace("false", "False").replace("true", "True").replace("null", "None"))
                            
                            resp_chunk = body.get("response", "")
                            full_response += resp_chunk
                            message_placeholder.markdown(full_response + "▌")
                    
                    message_placeholder.markdown(full_response)
                else:
                    full_response = "Ollama server-er sathe connect kora jachhe na! Check karo Ollama cholche kina."
                    message_placeholder.markdown(full_response)
            
            assistant_msg = {"role": "assistant", "content": full_response}
            if generated_image_url:
                assistant_msg["image_url"] = generated_image_url
                
            current_messages.append(assistant_msg)
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {e}")