from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
load_dotenv()

model_mistral = ChatMistralAI(
    model = "ministral-14b-latest",
    temperature = 0.8,
)

response_mistral = model_mistral.invoke("Write me a poem about AI")
print(response_mistral.content)