from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2",
    model_kwargs={"temperature": 0.0},
    encode_kwargs={"normalize_embeddings": True},
    dimensions=64
)

text = [
    "I am going to learn GenAI",
    "I am going to learn machine learning",
    "I am going to learn deep learning"
]

vector = embeddings.embed_documents(text)
print(vector)