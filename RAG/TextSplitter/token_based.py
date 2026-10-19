from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter

docs = PyPDFLoader("D:\\Python\\Generative AI\\RAG\\DocumentLoader\\GRU.pdf").load()

splitter = TokenTextSplitter(
    chunk_size=1000, 
    chunk_overlap=10
)

chunks = splitter.split_documents(docs)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}:")
    print(chunk.page_content)
    print("\n---\n")