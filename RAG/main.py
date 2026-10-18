from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()  # Load environment variables from .env file



data = TextLoader("D:\\Python\\Generative AI\\RAG\\DocumentLoader\\notes.txt").load()
docs = data.load()

template = ChatPromptTemplate.from_messages([
    ("system", "You are a ai that summarizes documents and answers questions about them."),
    ("human", "{data}")
])

prompt = template.format_messages(data=docs[0].page_content)
model = ChatMistralAI(
    model = "ministral-14b-latest",
    temperature = 0.8,
)

result = model.invoke(prompt)

print(result.content)