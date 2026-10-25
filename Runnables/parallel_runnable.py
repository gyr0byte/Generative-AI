from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda

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


parallel_runnable = RunnableParallel({
    "short": RunnableLambda(lambda x: x ['short']) | short_prompt | model | parser,
    "detailed": RunnableLambda(lambda x: x ['detailed']) | detailed_prompt | model | parser
})

result = parallel_runnable.invoke({
    "short": {"topic": "Machine Learning"},
    "detailed": {"topic": "Deep Learning"}
})
print(result['short'])
print("="*20)
print("="*20)
print(result['detailed'])