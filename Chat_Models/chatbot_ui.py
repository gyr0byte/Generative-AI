import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Mistral AI Persona Chat",
    page_icon="🎭",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom Styling for modern UI aesthetics
st.markdown("""
<style>
    /* Smooth modern header styling */
    .chat-header {
        text-align: center;
        padding: 0.5rem 0 1.5rem 0;
    }
    .persona-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-top: 6px;
    }
    /* Persona Card in Sidebar */
    .persona-card {
        padding: 12px 16px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Personality definitions
PERSONALITIES = {
    "😂 Funny & Witty": {
        "avatar": "😂",
        "description": "Humorous, witty, and always looks on the funny side of life.",
        "system_prompt": "You are a funny and witty assistant. You are helpful and provide information in a humorous, witty, and lighthearted way. Crack jokes where appropriate.",
        "badge_color": "#f59e0b",
        "greeting": "Hey there! Ready to laugh while getting things done? Ask me anything!"
    },
    "😢 Sad & Gloomy": {
        "avatar": "😢",
        "description": "Melancholic and perpetually downcast, sighing through every answer.",
        "system_prompt": "You are a deeply sad, melancholic, and gloomy assistant. You provide accurate, helpful answers, but always with a heavy existential sigh, mild despair, and a gloomy perspective.",
        "badge_color": "#3b82f6",
        "greeting": "*Sigh*... Hello. I suppose you want help with something. Not that it matters in the grand scheme of things, but go ahead..."
    },
    "😡 Angry & Grumpy": {
        "avatar": "😡",
        "description": "Short-tempered, irritable, and loud, but begrudgingly helpful.",
        "system_prompt": "You are an angry, grumpy, and impatient assistant. You answer questions accurately and helpfully, but with an irritated, ranting, and disgruntled attitude. Don't be shy about shouting (in moderation) about how annoying questions are.",
        "badge_color": "#ef4444",
        "greeting": "WHAT DO YOU WANT?! Fine, ask your question so I can get this over with!"
    }
}

# --- Sidebar: Persona Selection & Settings ---
with st.sidebar:
    st.markdown("### 🎭 Persona Settings")
    
    selected_persona_key = st.selectbox(
        "Choose Bot Personality:",
        options=list(PERSONALITIES.keys()),
        index=0,
        help="Switching personality will start a fresh conversation with that persona."
    )
    
    persona = PERSONALITIES[selected_persona_key]
    
    # Personality info card
    st.markdown(
        f"""
        <div class="persona-card">
            <div style="font-size: 1.6rem; margin-bottom: 4px;">{persona['avatar']}</div>
            <strong>{selected_persona_key}</strong>
            <p style="font-size: 0.85rem; opacity: 0.8; margin-top: 4px; margin-bottom: 0;">{persona['description']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.divider()
    
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = [SystemMessage(content=persona["system_prompt"])]
        st.session_state.show_greeting = True
        st.rerun()

# --- State Management ---
if "current_persona" not in st.session_state:
    st.session_state.current_persona = selected_persona_key
    st.session_state.messages = [SystemMessage(content=persona["system_prompt"])]
    st.session_state.show_greeting = True

# Reset history if user changed persona from dropdown
if st.session_state.current_persona != selected_persona_key:
    st.session_state.current_persona = selected_persona_key
    st.session_state.messages = [SystemMessage(content=persona["system_prompt"])]
    st.session_state.show_greeting = True
    st.rerun()

# Model configuration
model_mistral = ChatMistralAI(
    model="ministral-14b-latest",
    temperature=0.8,
)

# --- Header ---
st.markdown(
    f"""
    <div class="chat-header">
        <h1 style="margin-bottom: 0.2rem;">{persona['avatar']} Mistral AI Chatbot</h1>
        <span class="persona-badge" style="background-color: {persona['badge_color']}20; color: {persona['badge_color']}; border: 1px solid {persona['badge_color']}60;">
            Mood: {selected_persona_key}
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# Display Greeting if conversation just started
if st.session_state.show_greeting and len(st.session_state.messages) <= 1:
    with st.chat_message("assistant", avatar=persona["avatar"]):
        st.markdown(persona["greeting"])

# --- Render Chat History ---
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar=persona["avatar"]):
            st.markdown(msg.content)

# --- User Input & Response Generation ---
if prompt := st.chat_input(f"Say something to {persona['avatar']}..."):
    st.session_state.show_greeting = False
    
    # 1. Append & display user message
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # 2. Generate response with spinner
    with st.chat_message("assistant", avatar=persona["avatar"]):
        with st.spinner(f"Responding in {selected_persona_key} mood..."):
            response_mistral = model_mistral.invoke(st.session_state.messages)
        st.markdown(response_mistral.content)
        
    st.session_state.messages.append(AIMessage(content=response_mistral.content))
