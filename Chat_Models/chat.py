from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-20b"
)

response = model.invoke("Explain latent space in 2 sentences.")
print(response.content)