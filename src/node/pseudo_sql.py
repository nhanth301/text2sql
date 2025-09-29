from src.llm.prompt import PSEUDO_SQL_GEN_PROMPT
from src.schema.output_schema import SQLGenerationSchema
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

def pseudo_sql_node(llm: ChatOllama | ChatGoogleGenerativeAI, question: str) -> SQLGenerationSchema:
    try:
        chain = PSEUDO_SQL_GEN_PROMPT | llm.with_structured_output(SQLGenerationSchema)
        chain_result = chain.invoke({'question': question})
        return chain_result
    except Exception as e:
        raise e
