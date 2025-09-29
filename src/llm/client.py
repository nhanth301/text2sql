from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_together import ChatTogether
from langchain_ollama import ChatOllama
from src.config import config
from src.schema.output_schema import SQLGenerationSchema
import os
import os
# os.environ["OLLAMA_NO_GPU"] = "1"

os.environ["GOOGLE_API_KEY"] = config.google_api_key
# llm = ChatTogether(
#     together_api_key=config.together_api_key,
#     model="mistralai/Mixtral-8x7B-Instruct-v0.1",
#     temperature=0
# )

# print(llm.invoke("hello"))
pro_llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_output_tokens=None,
    timeout=None,
    max_retries=2,
)

llm = ChatOllama(
    model="sqlcoder:7b",
    temperature=0,
)

vip_llm = ChatOllama(
    model="mistral:7b",
    temperature=0
)
