"""Streamlit interface for the autonomous city-information agent."""

from typing import Any

import streamlit as st
import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_mistralai import ChatMistralAI
from tavily import TavilyClient
import os

load_dotenv()


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Weather is unavailable because OPENWEATHER_API_KEY is not configured."

    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": city, "appid": api_key, "units": "metric"},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Unable to fetch weather data.')}"

    return (
        f"The current weather in {city} is "
        f"{data['main']['temp']}°C with {data['weather'][0]['description']}."
    )


@tool
def get_news(city: str) -> str:
    """Get the latest news about a city."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "News is unavailable because TAVILY_API_KEY is not configured."

    results = TavilyClient(api_key=api_key).search(
        f"latest news on {city}", max_results=3
    ).get("results", [])
    if not results:
        return f"No news found for {city}."

    return "\n\n".join(
        f"Title: {item.get('title', 'No title')}\n"
        f"URL: {item.get('url', '')}\n"
        f"Content: {item.get('content', '')}"
        for item in results
    )


def create_ui_agent() -> Any:
    """Create the agent used by this Streamlit page."""
    return create_agent(
        model=ChatMistralAI(model="ministral-14b-latest"),
        tools=[get_weather, get_news],
        system_prompt=(
            "You are a helpful assistant that can provide weather information "
            "and the latest news for a given city."
        ),
    )


st.set_page_config(page_title="City Intelligence Agent", page_icon="🌍")

st.markdown(
    """
    <style>
    .hero { padding: 1.5rem 0 1rem; text-align: center; }
    .hero p { color: #64748b; margin-top: -0.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


def _message_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            item.get("text", str(item)) if isinstance(item, dict) else str(item)
            for item in content
        )
    return str(content)


def _reset_conversation() -> None:
    st.session_state.messages = []
    st.session_state.agent = create_ui_agent()


if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = create_ui_agent()

with st.sidebar:
    st.header("⚙️ Agent settings")
    st.caption("Available tools")
    st.write("🌤️ Current weather")
    st.write("📰 Latest city news")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        _reset_conversation()
        st.rerun()

st.markdown(
    """
    <div class="hero">
        <h1>🌍 City Intelligence Agent</h1>
        <p>Ask about the weather or latest news for any city.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(_message_text(message.content))
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant", avatar="🌍"):
            st.markdown(_message_text(message.content))
    elif isinstance(message, ToolMessage):
        with st.expander("Tool result", expanded=False):
            st.code(_message_text(message.content))

if prompt := st.chat_input("Ask about a city..."):
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🌍"):
        with st.spinner("Researching..."):
            try:
                result = st.session_state.agent.invoke(
                    {"messages": st.session_state.messages}
                )
            except Exception as error:
                st.error(f"Unable to get a response: {error}")
            else:
                st.session_state.messages = result.get("messages", [])
                assistant_messages = [
                    message
                    for message in st.session_state.messages
                    if isinstance(message, AIMessage)
                ]
                if assistant_messages:
                    st.markdown(_message_text(assistant_messages[-1].content))
                else:
                    st.warning("The agent did not return a response.")