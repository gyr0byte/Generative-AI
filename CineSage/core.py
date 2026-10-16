"""Prompt templates for extracting structured movie information."""

from langchain_core.prompts import PromptTemplate


MOVIE_EXTRACTION_PROMPT = """\
You are a careful movie-information extraction assistant.

Extract information only from the paragraph below. Do not use outside knowledge,
guess missing values, or correct possible errors in the source text. If a value
is not stated or cannot be determined from the paragraph, use null for a scalar
field and [] for a list field.

Return exactly one valid JSON object and nothing else. Use the following schema:
{{
  "title": "string or null",
  "media_type": "film, series, episode, or null",
  "release_year": "integer or null",
  "genres": ["string"],
  "director": "string or null",
  "writers": ["string"],
  "producers": ["string"],
  "cast": [
    {{
      "actor": "string",
      "character": "string or null"
    }}
  ],
  "setting": "string or null",
  "plot": "string or null",
  "themes": ["string"],
  "reception": "string or null",
  "ratings": [
    {{
      "score": "number or string",
      "source": "string or null"
    }}
  ],
  "music": ["string"],
  "visual_style": "string or null",
  "awards": ["string"],
  "keywords": ["string"],
  "summary": "A concise one- or two-sentence summary of the paragraph"
}}

Extraction rules:
- Keep names, titles, and numbers faithful to the paragraph.
- Put multiple genres, people, themes, keywords, and music references in lists.
- Use the actor field for named cast members. Set character to null unless the
  paragraph explicitly identifies the character they play.
- Preserve a rating together with its source, such as IMDb.
- Distinguish plot (what happens) from summary (a concise overview of the
  entire paragraph).
- Do not add markdown fences, comments, or additional keys.

Paragraph:
{paragraph}
"""


movie_extraction_prompt = PromptTemplate(
    input_variables=["paragraph"],
    template=MOVIE_EXTRACTION_PROMPT,
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
