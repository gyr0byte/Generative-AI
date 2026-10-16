"""Movie extraction schema and model logic."""

from functools import lru_cache

from langchain_groq import ChatGroq
from pydantic import BaseModel, Field


class Rating(BaseModel):
    """A rating mentioned in the source paragraph."""

    score: float | str = Field(description="The rating value exactly as stated.")
    source: str | None = Field(
        default=None,
        description="The rating source, such as IMDb, if mentioned.",
    )


class Movie(BaseModel):
    """Information that can be extracted from a movie description."""

    title: str | None = Field(
        default=None,
        description="The movie title, if mentioned.",
    )
    media_type: str | None = Field(
        default=None,
        description="Film, series, episode, or another media type, if mentioned.",
    )
    release_year: int | None = Field(
        default=None,
        description="The release year, if mentioned.",
    )
    genres: list[str] = Field(
        default_factory=list,
        description="Genres explicitly stated in the paragraph.",
    )
    director: str | None = Field(
        default=None,
        description="The director, if mentioned.",
    )
    writers: list[str] = Field(
        default_factory=list,
        description="Writers explicitly mentioned in the paragraph.",
    )
    producers: list[str] = Field(
        default_factory=list,
        description="Producers explicitly mentioned in the paragraph.",
    )
    cast: list[str] = Field(
        default_factory=list,
        description="Named actors only; do not infer character names.",
    )
    setting: list[str] = Field(
        default_factory=list,
        description="Places or locations explicitly mentioned.",
    )
    plot: str | None = Field(
        default=None,
        description="The story events described in the paragraph.",
    )
    themes: list[str] = Field(
        default_factory=list,
        description="Themes explicitly supported by the paragraph.",
    )
    reception: str | None = Field(
        default=None,
        description="Critical or audience reception explicitly mentioned.",
    )
    ratings: list[Rating] = Field(
        default_factory=list,
        description="Ratings and their sources explicitly mentioned.",
    )
    music_or_soundtrack: list[str] = Field(
        default_factory=list,
        description="Named composers, songs, or soundtrack details.",
    )
    visual_style: str | None = Field(
        default=None,
        description="Visual qualities explicitly described.",
    )
    awards: list[str] = Field(
        default_factory=list,
        description="Awards explicitly mentioned.",
    )
    keywords: list[str] = Field(
        default_factory=list,
        description="Important terms grounded in the paragraph.",
    )
    summary: str | None = Field(
        default=None,
        description="A concise one- or two-sentence summary of the paragraph.",
    )

    def to_markdown(self) -> str:
        """Render the validated schema in a readable format for the UI."""
        sections = [
            ("Movie name", self.title),
            ("Media type", self.media_type),
            ("Release year", self.release_year),
            ("Genre", self.genres),
            ("Director", self.director),
            ("Writers", self.writers),
            ("Producers", self.producers),
            ("Cast", self.cast),
            ("Setting", self.setting),
            ("Plot", self.plot),
            ("Main themes", self.themes),
            ("Reception", self.reception),
            (
                "Ratings",
                [
                    f"{rating.score} ({rating.source})"
                    if rating.source
                    else str(rating.score)
                    for rating in self.ratings
                ],
            ),
            ("Music or soundtrack", self.music_or_soundtrack),
            ("Visual style", self.visual_style),
            ("Awards", self.awards),
            ("Keywords", self.keywords),
            ("Quick summary", self.summary),
        ]
        output: list[str] = []
        for label, value in sections:
            output.append(f"**{label}:**")
            if isinstance(value, list):
                output.extend(
                    (f"- {item}" for item in value)
                    if value
                    else ("Not mentioned",)
                )
            else:
                output.append(str(value) if value is not None else "Not mentioned")
            output.append("")
        return "\n".join(output).strip()


@lru_cache(maxsize=1)
def get_model():
    """Create one reusable model configured for Movie structured output."""
    from dotenv import load_dotenv

    load_dotenv()
    model = ChatGroq(model_name="openai/gpt-oss-120b", temperature=0.1)
    return model.with_structured_output(Movie)


def extract_movie_information(paragraph: str) -> str:
    """Extract and validate movie information from a paragraph."""
    if not paragraph.strip():
        raise ValueError("A non-empty movie paragraph is required.")

    movie = get_model().invoke(paragraph)
    if not isinstance(movie, Movie):
        raise TypeError("The model returned an invalid movie extraction.")
    return movie.to_markdown()
