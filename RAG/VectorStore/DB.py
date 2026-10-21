from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

from langchain_core.documents import Document

docs = [
    Document(page_content="Python is widely used in Artificial Intelligence.", metadata={"source": "AI_book"}),
    Document(page_content="Pandas is used for data analysis in Python.", metadata={"source": "DataScience_book"}),
    Document(page_content="Neural networks are used in deep learning.", metadata={"source": "DL_book"}),
]

embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2"
)

chroma_db_path = Path(__file__).resolve().parent.parent / "chroma_db"

vecotrstore = Chroma.from_documents(
    documents = docs, 
    embedding = embedding_model,
    persist_directory = str(chroma_db_path)
)
