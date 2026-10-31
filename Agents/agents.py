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

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Unable to fetch weather data.')}"
    
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    
    return f"The current weather in {city} is {temp}°C with {desc}."

print(get_weather.invoke({"city": "Kathmandu"}))


# Tavily News tool

tavily_client = TavilyClient()

@tool
def get_news(city: str) -> str:
    """Latest news about the city"""

    query = f"latest news on {city}"
    response = tavily_client.search(query, max_results=3)
    
    results = response.get("results", [])
    
    if not results:
        return f"No news found for {city}."
    
    news_list = []
    
    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "")
        content = r.get("content", "")
        
        
        news_list.append(
            f"Title: {title}\nURL: {url}\nContent: {content}"
        )
        
    return f"Latest news for {city}:\n\n" + "\n\n".join(news_list)

print(get_news.invoke({"city": "Kathmandu"}))
    
llm = ChatMistralAI(
    model="ministral-14b-latest"
)

tools = {
    "get_weather": get_weather,
    "get_news": get_news
} 

llm_with_tools = llm.bind_tools(list(tools.values())) 

# Agent LOOP - Very important
messages = []
print("City Intelligence Agent")
print("Type 'exit' to quit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Exiting the agent. Goodbye!")
        break
    
    messages.append(HumanMessage(content=user_input))

    while True:
        result = llm_with_tools.invoke(messages)
        messages.append(result)
        
        #if tool is required 
        
        if result.tool_calls:
            for tool_call in result.tool_calls:
                tool_name = tool_call['name']

                #humnan in the loop
                confirm = input(f"Agents wants to call {tool_name}, Approve? (yes/no): ")
                
                if confirm.lower() == "no":
                    print(f"Tool call to {tool_name} was not approved.")
                    break
                
                # execute the tool
                tool_result = tools[tool_name].invoke(tool_call["args"])
                