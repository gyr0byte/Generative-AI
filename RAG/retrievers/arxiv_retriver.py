from langchain_community.retrievers import ArxivRetriever

# create the retriever
retriever = ArxivRetriever(
    load_max_docs=2,
    load_all_available_meta=True,
)

# query arxiv 
docs = retriever.invoke("large language models")

# Print results
for doc in docs:
    print(f"Title: {doc.metadata.get('Title', 'N/A')}")
    print(f"Authors: {doc.metadata.get('Authors', 'N/A')}")
    print(f"Abstract: {doc.metadata.get('Summary', 'N/A')}")
    print(f"URL: {doc.metadata.get('Entry ID', 'N/A')}")
    print(f"Summary: {doc.page_content}")
    print("\n")