"""Premium Streamlit interface for CineSage movie information extraction."""

import streamlit as st
from langchain_core.exceptions import LangChainException

from core import extract_movie_information


st.set_page_config(
    page_title="CineSage | Movie Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    :root {
        --ink: #f7f7fb;
        --muted: #a9a9bd;
        --line: rgba(255, 255, 255, 0.10);
        --panel: rgba(255, 255, 255, 0.055);
        --accent: #b7a1ff;
        --accent-strong: #8d6cff;
    }

    .stApp {
        background:
            radial-gradient(circle at 78% 0%, rgba(110, 77, 210, 0.22), transparent 31rem),
            radial-gradient(circle at 0% 25%, rgba(47, 108, 161, 0.12), transparent 28rem),
            #0b0c12;
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }

    .block-container {
        max-width: 1180px;
        padding: 2.2rem 2rem 4rem;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .brand-row {
        align-items: center;
        display: flex;
        gap: 0.75rem;
        margin-bottom: 1.6rem;
    }

    .brand-mark {
        align-items: center;
        background: linear-gradient(135deg, #b7a1ff, #7652e8);
        border-radius: 0.8rem;
        box-shadow: 0 10px 30px rgba(117, 82, 232, 0.28);
        display: flex;
        font-size: 1.3rem;
        height: 2.7rem;
        justify-content: center;
        width: 2.7rem;
    }

    .brand-name {
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }

    .brand-label {
        color: var(--muted);
        font-size: 0.75rem;
        margin-left: auto;
    }

    .hero {
        background: linear-gradient(120deg, rgba(30, 28, 55, 0.94), rgba(22, 17, 45, 0.78));
        border: 1px solid rgba(183, 161, 255, 0.20);
        border-radius: 1.4rem;
        box-shadow: 0 24px 70px rgba(0, 0, 0, 0.22);
        margin-bottom: 1.5rem;
        overflow: hidden;
        padding: 2.25rem 2.4rem;
        position: relative;
    }

    .hero::after {
        border: 1px solid rgba(183, 161, 255, 0.12);
        border-radius: 50%;
        content: "";
        height: 20rem;
        position: absolute;
        right: -7rem;
        top: -10rem;
        width: 20rem;
    }

    .eyebrow {
        color: var(--accent);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .hero h1 {
        font-family: 'Playfair Display', serif;
        font-size: clamp(2.4rem, 5vw, 4.2rem);
        letter-spacing: -0.045em;
        line-height: 1.05;
        margin: 0.45rem 0 0.75rem;
    }

    .hero p {
        color: #c0bed1;
        font-size: 1.02rem;
        line-height: 1.65;
        margin: 0;
        max-width: 42rem;
    }

    .section-label {
        color: var(--muted);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.13em;
        margin: 0 0 0.65rem;
        text-transform: uppercase;
    }

    .input-card, .info-card {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 1.15rem;
        padding: 1.25rem;
    }

    .info-card {
        height: 100%;
    }

    .info-card h3 {
        font-size: 1.15rem;
        margin: 0 0 0.85rem;
    }

    .info-card p {
        color: var(--muted);
        font-size: 0.9rem;
        line-height: 1.6;
    }

    .feature {
        border-top: 1px solid var(--line);
        display: flex;
        gap: 0.75rem;
        padding: 0.75rem 0;
    }

    .feature:first-of-type {
        border-top: 0;
    }

    .feature-icon {
        color: var(--accent);
        font-size: 1rem;
    }

    .feature-copy {
        color: #d8d6e2;
        font-size: 0.88rem;
    }

    .feature-copy span {
        color: var(--muted);
        display: block;
        font-size: 0.77rem;
        margin-top: 0.15rem;
    }

    textarea {
        background: rgba(8, 9, 15, 0.52) !important;
        border-color: var(--line) !important;
        border-radius: 0.8rem !important;
        color: var(--ink) !important;
    }

    textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 1px var(--accent) !important;
    }

    .stButton > button {
        border-radius: 0.7rem;
        font-weight: 600;
        min-height: 2.7rem;
        transition: border-color 0.2s, transform 0.2s;
    }

    .stButton > button:hover {
        border-color: var(--accent) !important;
        transform: translateY(-1px);
    }

    div[data-testid="stAlert"] {
        border-radius: 0.8rem;
    }

    .result-header {
        align-items: center;
        display: flex;
        justify-content: space-between;
        margin: 2rem 0 0.75rem;
    }

    .result-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.75rem;
        margin: 0;
    }

    .result-badge {
        background: rgba(109, 224, 173, 0.10);
        border: 1px solid rgba(109, 224, 173, 0.25);
        border-radius: 999px;
        color: #8ce8bd;
        font-size: 0.75rem;
        padding: 0.35rem 0.7rem;
    }

    [data-testid="stTabs"] button {
        color: var(--muted);
    }

    [data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--ink);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="brand-row">
        <div class="brand-mark">🎬</div>
        <div class="brand-name">CineSage</div>
        <div class="brand-label">MOVIE INTELLIGENCE STUDIO</div>
    </div>
    <div class="hero">
        <div class="eyebrow">Understand the story behind the story</div>
        <h1>From paragraph<br>to cinema insight.</h1>
        <p>Extract the people, plot, themes, reception, and details that make a
        movie description useful — all from a single paragraph.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

left_column, right_column = st.columns([1.08, 0.92], gap="large")

with left_column:
    st.markdown('<p class="section-label">01 · Source material</p>', unsafe_allow_html=True)
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    sample_paragraph = (
        "Interstellar is a visually stunning science fiction epic directed by "
        "Christopher Nolan. Released in 2014, the film stars Matthew McConaughey, "
        "Anne Hathaway, Jessica Chastain, and Michael Caine. The story revolves "
        "around a group of astronauts who travel through a wormhole near Saturn "
        "in search of a new home for humanity as Earth faces environmental collapse. "
        "The movie was widely appreciated for its emotional depth, scientific "
        "accuracy, and Hans Zimmer's powerful soundtrack. It holds a rating of "
        "8.6 on IMDb and is often considered one of the greatest sci-fi films "
        "of the 21st century."
    )

    def use_example() -> None:
        st.session_state["movie_paragraph"] = sample_paragraph

    paragraph = st.text_area(
        "Paste a paragraph to analyze",
        placeholder="Paste a movie description here...",
        height=280,
        key="movie_paragraph",
        label_visibility="collapsed",
    )

    button_column, _ = st.columns([0.42, 0.58])
    with button_column:
        st.button("Use example", on_click=use_example, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    extract_clicked = st.button(
        "✨  Extract movie intelligence",
        type="primary",
        use_container_width=True,
    )

with right_column:
    st.markdown('<p class="section-label">02 · What CineSage finds</p>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="info-card">
            <h3>A sharper view of every description.</h3>
            <p>Every result is validated against a typed movie schema before it
            reaches the screen, so the output stays clear and consistent.</p>
            <div class="feature">
                <div class="feature-icon">✦</div>
                <div class="feature-copy">Movie identity<span>Title, type, genre, and release year</span></div>
            </div>
            <div class="feature">
                <div class="feature-icon">✦</div>
                <div class="feature-copy">People and places<span>Director, cast, setting, and contributors</span></div>
            </div>
            <div class="feature">
                <div class="feature-icon">✦</div>
                <div class="feature-copy">Story and reception<span>Plot, themes, ratings, music, and summary</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if extract_clicked:
    if not paragraph.strip():
        st.warning("Add a movie paragraph to begin your analysis.")
    else:
        with st.spinner("CineSage is reading between the lines..."):
            try:
                extraction = extract_movie_information(paragraph.strip())
            except (LangChainException, TypeError, ValueError) as error:
                st.error(f"Unable to extract information: {error}")
            else:
                st.markdown(
                    """
                    <div class="result-header">
                        <h2 class="result-title">Your cinema brief</h2>
                        <div class="result-badge">✓ VALIDATED EXTRACTION</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                raw_tab, structured_tab, readable_tab = st.tabs(
                    ["Raw model output", "Structured output", "Readable summary"]
                )
                with raw_tab:
                    st.caption("The original response returned by the model.")
                    st.code(extraction.raw_output, language="json")
                with structured_tab:
                    st.caption("The response after Pydantic validation.")
                    st.json(extraction.movie.model_dump())
                with readable_tab:
                    st.caption("A presentation-ready version of the extraction.")
                    st.markdown(extraction.markdown)
