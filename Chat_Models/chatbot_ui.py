import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

st.set_page_config(page_title="Mistral AI Chatbot", page_icon="🤖")
st.title("🤖 Mistral AI Chatbot")

# Model configuration from chatbot.py
model_mistral = ChatMistralAI(
    model="ministral-14b-latest",
    temperature=0.8,
)

# Initialize conversation history with the system message
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a funny and witty assistant. You are helpful and provide information in a humorous way."),
    ]

# Display chat history (skipping the system message)
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# Handle user input and model response
if prompt := st.chat_input("You: "):
    # 1. Add and display user message
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get response from Mistral AI
    response_mistral = model_mistral.invoke(st.session_state.messages)
    st.session_state.messages.append(AIMessage(content=response_mistral.content))
    with st.chat_message("assistant"):
        st.markdown(response_mistral.content)
