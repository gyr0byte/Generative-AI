import hashlib
import os
import tempfile
from pathlib import Path

import streamlit as st
import torch
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mistralai import ChatMistralAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

os.environ["HF_HOME"] = r"D:\HuggingFace"
load_dotenv()

st.set_page_config(page_title="Chat with your PDF", page_icon="📄")
st.title("Chat with your PDF")
st.caption("Upload a PDF and ask questions about its contents.")


@st.cache_resource
def get_embedding_model() -> HuggingFaceEmbeddings:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": device},
        encode_kwargs={"normalize_embeddings": True},
    )


@st.cache_resource
def get_llm() -> ChatMistralAI:
    return ChatMistralAI(model_name="ministral-14b-latest")


def build_vectorstore(file_bytes: bytes, filename: str) -> Chroma:
    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_path = Path(temp_dir) / filename
        pdf_path.write_bytes(file_bytes)
        documents = PyPDFLoader(str(pdf_path)).load()

    if not documents:
        raise ValueError("The uploaded PDF does not contain any readable pages.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_documents(documents)

    if not chunks:
        raise ValueError("The uploaded PDF does not contain readable text.")

    return Chroma.from_documents(
        documents=chunks,
        embedding=get_embedding_model(),
    )


prompt_template = ChatPromptTemplate.from_template(
    """You are a helpful assistant that answers questions using only the provided
context. If the answer is not in the context, say you do not know. Do not make
up information. Answer in Markdown.

Context:
{context}

Question:
{question}
"""
)

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is None:
    st.info("Upload a PDF to begin.")
    st.stop()

file_bytes = uploaded_file.getvalue()
file_key = hashlib.sha256(file_bytes).hexdigest()

if st.session_state.get("file_key") != file_key:
    with st.spinner("Reading and indexing your PDF..."):
        st.session_state["vectorstore"] = build_vectorstore(
            file_bytes,
            uploaded_file.name,
        )
    st.session_state["file_key"] = file_key
    st.session_state["messages"] = []

st.success(f"Ready to answer questions about **{uploaded_file.name}**.")

for message in st.session_state.get("messages", []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a question about your PDF")

if question:
    st.session_state["messages"].append(
        {"role": "user", "content": question}
    )
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the PDF and generating an answer..."):
            retriever = st.session_state["vectorstore"].as_retriever(
                search_type="mmr",
                search_kwargs={"k": 3, "fetch_k": 10, "lambda_mult": 0.5},
            )
            relevant_documents: list[Document] = retriever.invoke(question)
            context = "\n\n".join(
                document.page_content for document in relevant_documents
            )
            prompt = prompt_template.format(
                context=context,
                question=question,
            )
            response = get_llm().invoke(prompt)
            answer = response.content

        st.markdown(answer)
        st.session_state["messages"].append(
            {"role": "assistant", "content": answer}
        )