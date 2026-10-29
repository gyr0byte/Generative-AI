from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from rich import print
from langchain_core.messages import HumanMessage

#1 Creating a tool
@tool
def get_text_length(text: str) -> int:
    """ Calculate the length of the given text. 
    """ #docstring
    return len(text)

llm = ChatMistralAI(
    model="ministral-14b-latest"
)

# tool binding
llm_with_tool = llm.bind_tools([get_text_length])

messages = []

query = HumanMessage(content="Please calculate the length of the following text: 'Hello, how are you doing today?'")

messages.append(query)

result = llm_with_tool.invoke(messages)
print("Result from LLM with tool:")
print(result)