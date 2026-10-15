from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
load_dotenv()

model_mistral = ChatMistralAI(
    model = "ministral-14b-latest",
    temperature = 0.8,
)

messages = []
print("Mistral AI Chatbot is ready! Type 0 to quit.")
while True:
    prompt = input("You: ")
    messages.append(prompt)
    if prompt == "0":
        print("Exiting Mistral AI Chatbot. Goodbye!")
        break
    response_mistral = model_mistral.invoke(messages)
    messages.append(response_mistral.content)
    print("Mistral: " + response_mistral.content)