import os

# Keep model downloads off C:
os.environ["HF_HOME"] = r"D:\HuggingFace"

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

chroma_db_path = Path(__file__).resolve().parent.parent / "chroma_db"

# load the pdf
data = PyPDFLoader(
    r"D:\Python\Generative AI\RAG\DocumentLoader\deeplearning.pdf"
)
docs = data.load()

# split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.split_documents(docs)

# create embeddings for each chunk
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cuda"},
    encode_kwargs={"normalize_embeddings": True},
)

# store into chroma db
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=str(chroma_db_path)
)