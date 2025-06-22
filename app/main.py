import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Docker live reload test - this comment was added to test live reload

# Get OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not found in environment variables.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(page_title="OpenAI GPT-4 Webchat", page_icon="🤖")
st.title("💬 OpenAI GPT-4 Webchat")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    # Call OpenAI GPT-4
    with st.spinner("OpenAI is typing..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state["messages"]
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"Error: {e}"
        st.session_state["messages"].append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply) 