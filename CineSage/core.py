from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq

model = ChatGroq(model_name="openai/gpt-oss-120b")

response = model.invoke("Hello, how are you?")

print(response.content)