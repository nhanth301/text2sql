from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import config
import os

os.environ["GOOGLE_API_KEY"] = config.google_api_key

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_output_tokens=None,
    timeout=None,
    max_retries=2,
)
