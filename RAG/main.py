import os

# Keep model downloads off C:
os.environ["HF_HOME"] = r"D:\HuggingFace"
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cuda"},
    encode_kwargs={"normalize_embeddings": True},
)

vectorstore = Chroma(
    persist_directory="D:\\Python\\Generative AI\\chroma_db",
    embedding_function=embedding_model
)

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 3,
        "fetch_k": 10,
        "lambda_mult": 0.5
        }
)

llm  = ChatMistralAI(
    model_name="ministral-14b-latest",
)

# prompt template for the chat model
prompt_template = ChatPromptTemplate.from_template(
    """You are a helpful assistant that answers questions based on the context provided.
    If you don't know the answer, just say you don't know. Do not try to make up an answer.
    Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    {context}
    Question: {question}
    Answer in Markdown:"""
)

print("RAG model initialized successfully.")
print("Press 0 to exit.")

while True:
    query = input("Enter your question: ")
    if query == "0":
        break

    # Retrieve relevant documents from the vectorstore
    docs = retriever.invoke(query)
    context = "\n".join([doc.page_content for doc in docs])

    # Format the prompt with the retrieved context and user question
    prompt = prompt_template.format(context=context, question=query)

    # Generate the answer using the LLM
    answer = llm.generate(prompt)

    print(f"AI: {answer}")