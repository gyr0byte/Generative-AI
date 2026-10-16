"""Prompt and model logic for extracting useful movie information."""

from functools import lru_cache

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import Optional, List


class Movie(BaseModel):
  title: str
  release_year: Optional[int]
  genre : List[str]
  director: Optional[str]
  writers: Optional[List[str]]
  producers: Optional[List[str]]
  cast: List[str]
  ratings: Optional[dict]
  summary: str

MOVIE_EXTRACTION_PROMPT = """\
You are a careful movie-information extraction assistant.

Read the paragraph and extract useful information using the exact headings
below. Do not use outside knowledge, guess missing values, or correct possible
errors in the source text. If a heading is not supported by the paragraph, write
"Not mentioned".

Use concise values and bullet points where appropriate. Keep names, titles,
numbers, and wording faithful to the paragraph. Return only the extraction,
without an introduction or conclusion.

Movie name:
Media type:
Release year:
Genre:
Director:
Writers:
Producers:
Cast:
- Actor:
  Character: (only if explicitly mentioned)
Setting:
Plot:
Main themes:
Reception:
Ratings:
Music or soundtrack:
Visual style:
Awards:
Keywords:
Quick summary:

Extraction rules:
- Put every named cast member under Cast.
- Keep a rating together with its source, such as "8.6 on IMDb".
- Distinguish Plot (the events of the story) from Quick summary (a concise
  overview of the whole paragraph).
- Do not add information that is not present in the paragraph.

Paragraph:
{paragraph}
"""


movie_extraction_prompt = ChatPromptTemplate.from_messages(
    [("user", MOVIE_EXTRACTION_PROMPT)]
)


@lru_cache(maxsize=1)
def get_model():
    """Create one reusable model instance."""
    from dotenv import load_dotenv
    from langchain_groq import ChatGroq

    load_dotenv()
    return ChatGroq(model_name="openai/gpt-oss-120b", temperature=0.1)


def extract_movie_information(paragraph: str) -> str:
    """Extract movie information from a paragraph with the configured model."""
    response = get_model().invoke(
        movie_extraction_prompt.format_messages(paragraph=paragraph)
    )
    return str(response.content)
