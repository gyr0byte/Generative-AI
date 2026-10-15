from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
load_dotenv()

model_mistral = ChatMistralAI(
    model = "ministral-14b-latest",
    temperature = 0.8,
)

messages = [
    SystemMessage(content="You are a funny and witty assistant. You are helpful and provide information in a humorous way."),
]

print("Mistral AI Chatbot is ready! Type 0 to quit.")
while True:
    prompt = input("You: ")
    messages.append(HumanMessage(content=prompt))
    if prompt == "0":
        print("Exiting Mistral AI Chatbot. Goodbye!")
        break
    response_mistral = model_mistral.invoke(messages)
    messages.append(AIMessage(content=response_mistral.content))
    print("Mistral: " + response_mistral.content)