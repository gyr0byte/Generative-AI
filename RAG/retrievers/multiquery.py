import os

# Keep model downloads off C:
os.environ["HF_HOME"] = r"D:\HuggingFace"
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv

load_dotenv()

docs = [
    Document(page_content="Gradient descent is an optimization algorithm used in machine learning."),
    Document(page_content="Gradient descent minimizes the loss function."),
    Document(page_content="Gradient descent is an optimization that minimizes the loss function."),
    Document(page_content="Neural networks use gradient descent for training."),
    Document(page_content="Support Vector Machines are supervised learning algorithms.")
]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cuda"},
    encode_kwargs={"normalize_embeddings": True},
)

vectorstore = Chroma.from_documents(docs, embeddings)

retriever = vectorstore.as_retriever()

llm = ChatMistralAI(model_name="ministral-14b-latest", temperature=0)

multi_query_retriever = MultiQueryRetriever.from_llms(
    retriever=retriever, 
    llm=llm, 
    num_queries=3
)

query = "What is gradient descent?"

multi_query_docs = multi_query_retriever.invoke(query)