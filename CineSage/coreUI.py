"""Streamlit user interface for CineSage movie information extraction."""

import streamlit as st
from langchain_core.exceptions import LangChainException

from core import extract_movie_information


st.set_page_config(
    page_title="CineSage | Movie Extractor",
    page_icon="🎬",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container { max-width: 1100px; padding-top: 2rem; }
    .hero {
        padding: 1.5rem 1.75rem;
        border-radius: 1rem;
        background: linear-gradient(135deg, #171a36, #30205c);
        color: white;
        margin-bottom: 1.5rem;
    }
    .hero h1 { margin-bottom: 0.25rem; }
    .hero p { color: #d9d4ef; margin-bottom: 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🎬 CineSage</h1>
        <p>Turn movie descriptions into clear, useful information in seconds.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

left_column, right_column = st.columns([1.05, 0.95], gap="large")

with left_column:
    st.subheader("Movie paragraph")
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
        placeholder="Example: A movie description mentioning its cast, story, and reception...",
        height=300,
        key="movie_paragraph",
        label_visibility="collapsed",
    )

    st.button(
        "Use example",
        on_click=use_example,
        use_container_width=True,
    )

    extract_clicked = st.button(
        "✨ Extract movie information",
        type="primary",
        use_container_width=True,
    )

with right_column:
    st.subheader("What you’ll get")
    st.markdown(
        """
        - **Movie details:** title, type, genre, and release year
        - **People:** director, writers, producers, and cast
        - **Story:** setting, plot, themes, and keywords
        - **Reception:** ratings, reviews, awards, and visual style
        - **Quick summary:** a concise overview of the paragraph
        """
    )
    st.info("The extractor uses only the information present in your paragraph.")

if extract_clicked:
    if not paragraph.strip():
        st.warning("Please paste a movie paragraph before extracting information.")
    else:
        with st.spinner("Analyzing the movie paragraph..."):
            try:
                extraction = extract_movie_information(paragraph.strip())
            except (LangChainException, TypeError, ValueError) as error:
                st.error(f"Unable to extract information: {error}")
            else:
                st.subheader("Raw Model Output")
                st.code(extraction.raw_output, language="json")

                st.subheader("Structured Output")
                st.json(extraction.movie.model_dump())

                st.subheader("Readable Summary")
                st.markdown(extraction.markdown)