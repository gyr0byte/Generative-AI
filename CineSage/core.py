from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI

model = ChatMistralAI(model_name="ministral-medium-latest")

response = model.invoke("Hello, how are you?")

print(response.content)