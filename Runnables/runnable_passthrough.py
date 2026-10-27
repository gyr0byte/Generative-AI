from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

model = ChatMistralAI(
    model="ministral-14b-latest"
)
parser = StrOutputParser()

code_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a code generator"),
    ("human", "{topic}")
])

explain_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant who explains code in simple terms"),
    ("human", "Explain the following code in simple terms:\n {code}")
])

seq = code_prompt | model | parser 
seq2 = RunnableParallel({
    "code": seq,
    "explain": RunnablePassthrough() | explain_prompt | model | parser
})

result = seq.invoke({"topic": "Write a Python code to calculate the factorial of a number."})
print(result)