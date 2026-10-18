from langchain_community.document_loaders import WebBaseLoader

url = "https://rog.asus.com/us/laptops/rog-strix/rog-strix-scar-16-2025/"

data = WebBaseLoader(url)
docs = data.load()

print(docs[0].page_content) 