# First Step - loading all the libraries
import os
from pathlib import Path
from dotenv import load_dotenv
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path) 

import requests
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient

# Now let's create some tools

# Weather tool
API_KEY = os.getenv("OPENWEATHER_API_KEY")
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    url = 