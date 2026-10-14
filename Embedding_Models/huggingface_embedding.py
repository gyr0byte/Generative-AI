import os

# Keep model downloads off C:
os.environ["HF_HOME"] = r"D:\HuggingFace"

from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cuda"},
    encode_kwargs={"normalize_embeddings": True},
)

# Embed documents
documents = [
    "Machine learning is a branch of artificial intelligence.",
    "Python is a programming language.",
    "Deep learning uses neural networks.",
]

vectors = embeddings.embed_documents(documents)

print("Documents embedded:", len(vectors))
print("First vector length:", len(vectors[0]))