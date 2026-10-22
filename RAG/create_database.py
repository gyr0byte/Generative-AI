from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# load the pdf
# split into chunks
# create embeddings for each chunk
# store into chroma db