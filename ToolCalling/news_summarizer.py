from dotenv import load_dotenv
load_dotenv() 
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

search_tool = TavilySearchResults(max_results=5)

llm = ChatMistralAI(
    model="ministral-14b-latest"
)

parser = StrOutputParser()

prompt = ChatPromptTemplate.from_template(
    """You are a news summarizer. 
    You will be given a news article and you will summarize it in a concise manner. 
    Please provide the summary in 3-4 sentences.\n\nArticle: {news}\n\nSummary:"""
)

