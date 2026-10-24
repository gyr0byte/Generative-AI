import os

# Keep model downloads off C:
os.environ["HF_HOME"] = r"D:\HuggingFace"
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate