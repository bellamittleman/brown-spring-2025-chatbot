import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

# Setup OpenAI client
client = OpenAI()

# Your fine-tuned model ID
FINE_TUNED_MODEL = "ft:gpt-4o-mini-2024-07-18:university-of-mary-washington::AaxgQQAe"  # Update if needed

# Streamlit page setup
st.set_page_config(page_title="Telecom Cybersecurity Advisor", page_icon="🛰️")
st.title("🛰️ Telecom Cybersecurity Advisor")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are an expert AI assistant trained on emergency alerts, public safety communications, cybersecurity policy, "
            "disaster response, and telecommunications regulations. "
            "You must provide answers that are specific to the user's question, cite real-world examples or studies if possible, "
            "and avoid repeating the same answer. Be concise but informative."
        )}
    ]

# Chat input
user_input = st.chat_input("Ask me about telecom cybersecurity, emergency alerts, or FCC policy...")

if user_input:
    # Add user input to the session
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate assistant response
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model=FINE_TUNED_MODEL,
            messages=st.session_state.messages,
            temperature=0.5,  # <-- slightly more creative
            max_tokens=400    # <-- a little more space for answers
        )
        assistant_reply = response.choices[0].message.content.strip()

    # Add assistant response to the session
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

# Display conversation history
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])
