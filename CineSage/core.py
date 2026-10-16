"""Prompt templates for extracting structured movie information."""

from langchain_core.prompts import ChatPromptTemplate


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


if __name__ == "__main__":
    from dotenv import load_dotenv
    from langchain_groq import ChatGroq

    load_dotenv()

    paragraph = input("Paste a movie paragraph: ").strip()
    if not paragraph:
        raise SystemExit("A non-empty movie paragraph is required.")

    model = ChatGroq(model_name="openai/gpt-oss-120b")
    response = model.invoke(movie_extraction_prompt.format(paragraph=paragraph))
    print(response.content)
