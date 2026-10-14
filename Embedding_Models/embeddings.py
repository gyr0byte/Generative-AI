from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2",
    dimensions=256
)

vector = embeddings.embed_query("I am going to learn GenAI")
print(vector)