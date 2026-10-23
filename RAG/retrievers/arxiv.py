from langchain_community.retrievers import ArxivRetriever

# create the retriever
retriever = ArxivRetriever(
    load_max_docs=2,
    load_all_available_metadata=True,
)

# query arxiv 
docs = retriever.invoke("large language models")

# print results
for doc in docs:
    print(f"Title: {doc.metadata['title']}")
    print(f"Authors: {doc.metadata['authors']}")
    print(f"Abstract: {doc.metadata['summary']}")
    print(f"URL: {doc.metadata['url']}")
    print("\n")