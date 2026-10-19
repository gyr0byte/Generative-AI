from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

splitter = CharacterTextSplitter(
    separator = "",
    chunk_size=10, 
    chunk_overlap=1
)

data = TextLoader("D:\\Python\\Generative AI\\RAG\\DocumentLoader\\notes.txt").load()
chunks = splitter.split_documents(data)

for i in range(len(chunks)):
    print(f"Chunk {i+1}: {chunks[i].page_content}")