from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

docs = PyPDFLoader(
    r"D:\Python\Generative AI\RAG\DocumentLoader\deeplearning.pdf"
).load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=10
)
chunks = splitter.split_documents(docs)

template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI that summarizes documents and answers questions about them.",
        ),
        ("human", "{data}"),
    ]
)

prompt = template.format_messages(data=docs)

model = ChatMistralAI(
    model="ministral-14b-latest",
    temperature=0.8,
)
