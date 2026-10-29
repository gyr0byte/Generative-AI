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

result = llm_with_tool.invoke("Use the get_text_length tool to find the length of the following text: 'Hello, this is a sample text for testing the tool.'")

if result.tool_calls:
    tool_call = result.tool_calls[0]
    tool_result = get_text_length.invoke(tool_call['args'])

    final_result = llm_with_tool.invoke(f"The length of the text is: {tool_result}")

    print("Final Result:")
    print(final_result.content)