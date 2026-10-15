import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Mistral AI Chatbot",
    page_icon="🤖",
    layout="centered",
)

# Header Section
st.title("🤖 Mistral AI Chatbot")
st.caption("A witty and humorous assistant powered by Mistral AI (UI Layout Preview)")

# Chat Display Area (Static UI preview without backend execution)
with st.chat_message("assistant"):
    st.markdown("Hello! I am your funny and witty assistant. What would you like to chat about today?")

with st.chat_message("user"):
    st.markdown("Can you give me a funny reason why computers are like humans?")

with st.chat_message("assistant"):
    st.markdown("They become completely useless the moment they lose their connection to the network!")

# Chat Input Field (Pure UI element, no functionality attached)
st.chat_input("Type your message here...")
