import os

# Keep model downloads off C:
os.environ["HF_HOME"] = r"D:\HuggingFace"
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cuda"},
    encode_kwargs={"normalize_embeddings": True},
)

vectorstore = Chroma(
    persist_directory="D:\\Python\\Generative AI\\chroma_db",
    embedding_function=embedding_model
)

