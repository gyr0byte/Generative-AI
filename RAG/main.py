from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

docs = PyPDFLoader(
    r"D:\Python\Generative AI\RAG\DocumentLoader\GRU.pdf"
).load()

template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI that summarizes documents and answers questions about them.",
        ),
        ("human", "{data}"),
    ]
)

prompt = template.format_messages(data=docs[0].page_content)

model = ChatMistralAI(
    model="ministral-14b-latest",
    temperature=0.8,
)

result = model.invoke(prompt)

print(result.content)