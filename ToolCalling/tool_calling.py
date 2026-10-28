from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from rich import print

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

result = llm.invoke("Hello, how are you?")
result2 = llm_with_tool.invoke("Hello, how are you?")

print(result)
print("="*32)
print(result2)