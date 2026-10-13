from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
load_dotenv()

model_groq = ChatGroq(
    model="openai/gpt-oss-20b"
)

response_groq = model_groq.invoke("Explain about open source in 2 sentences.")
print(response_groq.content)
print("=====================================================")
print("=====================================================")

model_gemini = ChatGoogleGenerativeAI (
    model = "gemini-2.5-flash"
)

response_gemini = model_gemini.invoke("Explain about transformer architechture in 2 sentences.")
print(response_gemini.content)

print("=====================================================")
print("=====================================================")

model_mistral = ChatMistralAI(
    model = "mistral-7b-instruct-v0.1"
)

response_mistral = model_mistral.invoke("Explain about quantization in 2 sentences.")
print(response_mistral.content)