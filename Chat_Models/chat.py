from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

model_groq = ChatGroq(
    model="openai/gpt-oss-20b"
)

response_groq = model_groq.invoke("Explain about nepal in 2 sentences.")
print(response_groq.content)
print("=====================================================")
print("=====================================================")
from langchain_google_genai import ChatGoogleGenerativeAI

model_gemini = ChatGoogleGenerativeAI (
    model = "gemini-3.7-flash"
)

response_gemini = model_gemini.invoke("Explain about transformer architechture in 2 sentences.")
print(response_gemini.content)