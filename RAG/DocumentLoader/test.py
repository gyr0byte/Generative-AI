from langchain_community.document_loaders import TextLoader

data = TextLoader("D:\\Python\\Generative AI\\RAG\\DocumentLoader\\notes.txt").load()

print(data[0].page_content)