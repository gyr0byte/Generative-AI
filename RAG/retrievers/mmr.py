import os

# Keep model downloads off C:
os.environ["HF_HOME"] = r"D:\HuggingFace"
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

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

similarity_retriever = vectorstore.as_retriever(
    search_type="similarity", 
    search_kwargs={"k": 3}
)

print("==== Similarity Search Results ====\n")

similarity_docs = similarity_retriever.invoke("What is gradient descent?")

for doc in similarity_docs:
    print(f"Content: {doc.page_content}")
    print("\n")
    
mmr_retriever = vectorstore.as_retriever(
    search_type="mmr", 
    search_kwargs={"k": 3}
)

print("==== MMR Search Results ====\n")

mmr_docs = mmr_retriever.invoke("What is gradient descent?")

for doc in mmr_docs:
    print(f"Content: {doc.page_content}")
    print("\n")
