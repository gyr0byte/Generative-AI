from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

# Components
model = ChatMistralAI(
    model="ministral-14b-latest"
)
parser = StrOutputParser()

# Two different prompts
short_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in 1-2 lines."
)

detailed_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in detail"
)

# Input
toppic = "Machine Learning"

parallel_runnable = RunnableParallel({
    "short": short_prompt | model | parser,
    "detailed": detailed_prompt | model | parser
})

result = parallel_runnable.invoke({"topic": toppic})
print(result['short'])
print(result['detailed'])