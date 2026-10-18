from langchain_community.document_loaders import PyPDFLoader

docs = PyPDFLoader("D:\\Python\\Generative AI\\RAG\\DocumentLoader\\GRU.pdf").load()

print(docs)