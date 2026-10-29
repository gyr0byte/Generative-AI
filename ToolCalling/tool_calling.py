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

result = llm_with_tool.invoke("Return the length of this text: Hello, how are you?")

if result.tool_calls:
    tool_call = result.tool_calls[0]
    
tool_name = tool_call['name']
tool_args = tool_call['args']

tool_result = get_text_length.invoke(tool_args)

final_result = llm_with_tool.invoke(f"The length of the text is: {tool_result}")

print("Final Result:")
print(final_result)