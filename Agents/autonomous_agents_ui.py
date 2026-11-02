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
    :root {
        --ink: #e8eefc;
        --muted: #91a0bd;
        --line: rgba(148, 163, 184, 0.16);
        --panel: rgba(15, 23, 42, 0.72);
        --accent: #8b5cf6;
        --cyan: #22d3ee;
    }
    .stApp {
        background:
            radial-gradient(circle at 8% 0%, rgba(124, 58, 237, 0.22), transparent 30rem),
            radial-gradient(circle at 92% 18%, rgba(6, 182, 212, 0.13), transparent 28rem),
            #070b16;
        color: var(--ink);
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] {
        background: rgba(8, 13, 27, 0.86);
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 2rem; }
    .block-container { max-width: 920px; padding-top: 2.5rem; }
    .hero { padding: 1rem 0 2rem; text-align: center; }
    .eyebrow {
        color: var(--cyan); font-size: .72rem; font-weight: 700;
        letter-spacing: .18em; text-transform: uppercase;
    }
    .hero h1 {
        background: linear-gradient(110deg, #f8fafc 10%, #c4b5fd 55%, #67e8f9);
        -webkit-background-clip: text; background-clip: text; color: transparent;
        font-size: clamp(2.2rem, 6vw, 4rem); letter-spacing: -.055em;
        margin: .35rem 0 .45rem;
    }
    .hero p { color: var(--muted); font-size: 1.05rem; margin: 0; }
    .status-row {
        align-items: center; display: flex; gap: .55rem; justify-content: center;
        margin-top: 1.2rem; color: #a7f3d0; font-size: .82rem;
    }
    .status-dot {
        background: #34d399; border-radius: 50%; box-shadow: 0 0 14px #34d399;
        height: 7px; width: 7px;
    }
    .welcome {
        background: linear-gradient(145deg, rgba(30, 41, 79, .76), rgba(15, 23, 42, .62));
        border: 1px solid var(--line); border-radius: 22px; margin: 1rem 0 2rem;
        padding: 1.5rem 1.6rem; text-align: center;
    }
    .welcome h3 { margin: 0 0 .45rem; }
    .welcome p { color: var(--muted); margin: 0; }
    .tool-grid { display: grid; gap: .7rem; grid-template-columns: 1fr 1fr; margin-top: 1rem; }
    .tool-card {
        background: rgba(30, 41, 59, .5); border: 1px solid var(--line);
        border-radius: 14px; padding: .8rem 1rem; text-align: left;
    }
    .tool-card strong { display: block; font-size: .9rem; }
    .tool-card span { color: var(--muted); font-size: .76rem; }
    [data-testid="stChatMessage"] {
        background: rgba(15, 23, 42, .56); border: 1px solid var(--line);
        border-radius: 18px; margin: .65rem 0; padding: .8rem 1rem;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: rgba(76, 29, 149, .24); border-color: rgba(167, 139, 250, .25);
    }
    [data-testid="stChatInput"] {
        border-color: rgba(139, 92, 246, .55); border-radius: 16px;
    }
    .stButton > button {
        border: 1px solid var(--line); border-radius: 12px;
        transition: all .2s ease;
    }
    .stButton > button:hover {
        border-color: var(--accent); color: white; transform: translateY(-1px);
    }
    @media (max-width: 640px) {
        .block-container { padding: 1.5rem 1rem 2rem; }
        .tool-grid { grid-template-columns: 1fr; }
    }
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
    st.markdown("## 🌍 City Intelligence")
    st.caption("AUTONOMOUS RESEARCH ASSISTANT")
    st.divider()
    st.markdown("#### Connected capabilities")
    st.markdown("🌤️  **Weather intelligence**")
    st.caption("Live conditions and temperature")
    st.markdown("📰  **News discovery**")
    st.caption("Recent headlines from the web")
    st.divider()
    st.markdown("#### Session")
    st.success("Agent online", icon="✅")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        _reset_conversation()
        st.rerun()

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Autonomous research workspace</div>
        <h1>City Intelligence</h1>
        <p>Ask one question. Get a clear, current answer about any city.</p>
        <div class="status-row"><span class="status-dot"></span> Ready to explore</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome">
            <h3>Where should we begin?</h3>
            <p>Explore live weather, breaking news, or both in one conversation.</p>
            <div class="tool-grid">
                <div class="tool-card"><strong>🌤️ Weather briefing</strong><span>“What is the weather in Tokyo?”</span></div>
                <div class="tool-card"><strong>📰 News briefing</strong><span>“What is happening in London?”</span></div>
            </div>
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