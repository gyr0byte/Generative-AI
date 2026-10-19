from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import ChracterTextSplitter

splitter = ChracterTextSplitter(
    splitter = "",
    chunk_size=10, 
    chunk_overlap=1
)

data = TextLoader("D:\\Python\\Generative AI\\RAG\\DocumentLoader\\notes.txt").load()
chunks = splitter.split_documents(data)

print(chunks[0].page_content)