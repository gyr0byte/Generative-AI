from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Prompt Template 
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple words."
)

# Model Initialization
model = ChatMistralAI(
    model_name="ministral-14b-latest"
)

# Output Parser
parser = StrOutputParser()

# Using runnable 
runnable = prompt | model | parser

result = runnable.invoke("Quantum Computing")
print(result)