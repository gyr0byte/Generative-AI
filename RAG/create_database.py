from langchain_google_genai import GoogleGenerativeAIEmbeddings
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
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(docs)

# create embeddings for each chunk
# store into chroma db